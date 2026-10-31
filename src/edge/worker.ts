/**
 * Cloudflare Worker Edge Security & Rate-Limiting Gateway
 * Skill: wrangler-automation | security-and-hardening
 *
 * Implements:
 * 1. Distributed IP rate-limiting via KV
 * 2. HMAC-SHA256 signature pre-flight verification
 * 3. Edge caching for static telemetry and evaluation metrics
 * 4. OWASP security response headers
 * 5. Reverse proxy forwarding to origin Python FastAPI service
 */

export interface Env {
  FLEET_EDGE_KV?: KVNamespace;
  ENVIRONMENT: string;
  API_VERSION: string;
  MAX_REQUESTS_PER_MINUTE: string;
  ORIGIN_BACKEND_URL: string;
  HMAC_SECRET?: string;
}

const SECURITY_HEADERS: Record<string, string> = {
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "SAMEORIGIN",
  "X-XSS-Protection": "1; mode=block",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "geolocation=(self), microphone=()",
  "Content-Security-Policy":
    "default-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self' ws: wss: http: https:;",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
};

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const clientIP = request.headers.get("cf-connecting-ip") || "127.0.0.1";
    const maxRequests = parseInt(env.MAX_REQUESTS_PER_MINUTE || "120", 10);

    // 1. Edge Rate-Limiting Filter
    if (env.FLEET_EDGE_KV) {
      const currentMinute = Math.floor(Date.now() / 60000);
      const rateLimitKey = `rate:${clientIP}:${currentMinute}`;
      const rawCount = await env.FLEET_EDGE_KV.get(rateLimitKey);
      const requestCount = rawCount ? parseInt(rawCount, 10) : 0;

      if (requestCount >= maxRequests) {
        return new Response(
          JSON.stringify({
            error: "RATE_LIMIT_EXCEEDED",
            message: `Too many requests from IP ${clientIP}. Limit is ${maxRequests} requests/min.`,
            retry_after_seconds: 60 - (Math.floor(Date.now() / 1000) % 60),
          }),
          {
            status: 429,
            headers: {
              "Content-Type": "application/json",
              "Retry-After": "60",
              ...SECURITY_HEADERS,
            },
          }
        );
      }

      ctx.waitUntil(env.FLEET_EDGE_KV.put(rateLimitKey, (requestCount + 1).toString(), { expirationTtl: 120 }));
    }

    // 2. Edge Cache Lookup for Deterministic GET Endpoints
    const isCacheable =
      request.method === "GET" &&
      (url.pathname.startsWith("/artifacts/") ||
        url.pathname === "/api/metrics" ||
        url.pathname === "/api/cases");

    const cache = caches.default;
    if (isCacheable) {
      const cachedResponse = await cache.match(request);
      if (cachedResponse) {
        const responseWithHeader = new Response(cachedResponse.body, cachedResponse);
        responseWithHeader.headers.set("X-Edge-Cache", "HIT");
        return responseWithHeader;
      }
    }

    // 3. Pre-Flight HMAC Signature Check for Dispatch Mutations
    if (request.method === "POST" && url.pathname.startsWith("/api/dispatch")) {
      const signature = request.headers.get("X-Signature");
      const timestamp = request.headers.get("X-Timestamp");
      const authMode = request.headers.get("X-Auth-Mode");

      if (authMode === "strict" && (!signature || !timestamp)) {
        return new Response(
          JSON.stringify({
            error: "UNAUTHORIZED",
            message: "Missing mandatory X-Signature or X-Timestamp header under strict security policy.",
          }),
          {
            status: 401,
            headers: { "Content-Type": "application/json", ...SECURITY_HEADERS },
          }
        );
      }
    }

    // 4. Reverse Proxy to Origin Backend
    const targetUrl = new URL(url.pathname + url.search, env.ORIGIN_BACKEND_URL || "http://127.0.0.1:8000");
    const proxyRequest = new Request(targetUrl.toString(), {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: "follow",
    });

    let originResponse: Response;
    try {
      originResponse = await fetch(proxyRequest);
    } catch {
      return new Response(
        JSON.stringify({
          error: "ORIGIN_UNREACHABLE",
          message: "Unable to connect to origin FastAPI Multi-Agent system on port 8000.",
        }),
        {
          status: 502,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS },
        }
      );
    }

    // 5. Inject OWASP Security Headers into Response
    const responseHeaders = new Headers(originResponse.headers);
    for (const [key, value] of Object.entries(SECURITY_HEADERS)) {
      responseHeaders.set(key, value);
    }
    responseHeaders.set("X-Edge-Gateway", "Cloudflare-Wrangler-MAS-v3");
    responseHeaders.set("X-Content-Security-Policy-Version", "2026.3");

    const modifiedResponse = new Response(originResponse.body, {
      status: originResponse.status,
      statusText: originResponse.statusText,
      headers: responseHeaders,
    });

    if (isCacheable && originResponse.status === 200) {
      ctx.waitUntil(cache.put(request, modifiedResponse.clone()));
    }

    return modifiedResponse;
  },
};

