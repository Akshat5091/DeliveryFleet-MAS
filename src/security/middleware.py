"""Security and Hardening Module for DeliveryFleet-MAS.
Skill: security-and-hardening
Provides:
1. HMAC-SHA256 signature verification & generation for mutation endpoints.
2. Idempotency store for mission dispatch deduplication.
3. OWASP security response headers.
"""
import os
import time
import hmac
import hashlib
import threading
from typing import Dict, Any, Optional, Tuple
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

DEFAULT_HMAC_SECRET = os.getenv("DELIVERYFLEET_HMAC_SECRET", "mas-production-sec-key-2026")
HMAC_TOLERANCE_SECONDS = int(os.getenv("HMAC_TOLERANCE_SECONDS", "300"))

class IdempotencyStore:
    """Thread-safe cache for idempotency key deduplication."""
    def __init__(self, ttl_seconds: int = 3600):
        self._lock = threading.Lock()
        self._store: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if key not in self._store:
                return None
            created_at, payload = self._store[key]
            if time.time() - created_at > self._ttl:
                del self._store[key]
                return None
            return payload

    def set(self, key: str, payload: Dict[str, Any]):
        with self._lock:
            self._store[key] = (time.time(), payload)

    def size(self) -> int:
        with self._lock:
            return len(self._store)

idempotency_store = IdempotencyStore()

def generate_hmac_signature(body: str, timestamp_str: str, secret: str = DEFAULT_HMAC_SECRET) -> str:
    """Compute HMAC-SHA256 hex digest for body + timestamp."""
    message = f"{timestamp_str}:{body}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()

def verify_hmac_signature(
    body: str,
    signature: Optional[str],
    timestamp_str: Optional[str],
    secret: str = DEFAULT_HMAC_SECRET,
    tolerance_sec: int = HMAC_TOLERANCE_SECONDS
) -> bool:
    """Verify HMAC signature with replay window validation."""
    if not signature or not timestamp_str:
        return False

    try:
        ts = int(timestamp_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_TIMESTAMP", "message": "Timestamp must be a valid integer UNIX epoch."}
        )

    current_time = int(time.time())
    if abs(current_time - ts) > tolerance_sec:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "TIMESTAMP_EXPIRED",
                "message": f"Request timestamp drift ({abs(current_time - ts)}s) exceeds allowable window ({tolerance_sec}s)."
            }
        )

    expected_sig = generate_hmac_signature(body, timestamp_str, secret)
    if not hmac.compare_digest(expected_sig, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_HMAC_SIGNATURE", "message": "Computed signature does not match header."}
        )

    return True

