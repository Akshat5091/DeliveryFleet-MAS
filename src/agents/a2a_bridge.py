"""A2A Protocol Interoperability Bridge connecting CrewAI and Google ADK.
Course: CSE3101 Agentic AI | Group 8 | Multi-Agent Delivery Fleet
Supports both high-speed in-process transport and standard network JSON-RPC over HTTP.
Includes connection circuit-breaker caching for ultra-low latency.
"""
import uuid
import time
import json
import threading
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List
from ..schemas.a2a import A2AMessage, A2ARequest, A2AResponse
from .adk_route_agent import ADKRouteAgent
from ..observability.run_logger import RunLogger

class A2ABridge:
    """Inter-framework communication bus enabling CrewAI agents to send messages to Google ADK agents."""

    def __init__(
        self,
        adk_route_agent: Optional[ADKRouteAgent] = None,
        endpoint_url: str = "http://127.0.0.1:8000/api/a2a/route",
        transport_mode: str = "auto"
    ):
        self.adk_route_agent = adk_route_agent or ADKRouteAgent()
        self.endpoint_url = endpoint_url
        self.transport_mode = transport_mode  # "auto", "network", or "in_process"
        self.logger = RunLogger.get_logger()
        self.message_history: List[A2AMessage] = []
        self._lock = threading.RLock()
        
        # Circuit-breaker cache for network availability
        self._last_network_check: float = 0.0
        self._network_available: bool = False

    def _should_attempt_network(self) -> bool:
        if self.transport_mode == "in_process":
            return False
        if self.transport_mode == "network":
            return True
        # In 'auto' mode: only retry connecting if last check was more than 10 seconds ago
        # or if network was confirmed available
        now = time.time()
        if self._network_available or (now - self._last_network_check > 10.0):
            return True
        return False

    def _call_network_endpoint(self, message: A2AMessage) -> Optional[A2AResponse]:
        """Transmit A2AMessage as JSON-RPC over HTTP to the ADK agent endpoint."""
        now = time.time()
        self._last_network_check = now
        try:
            payload_data = message.model_dump()
            req_body = json.dumps(payload_data).encode("utf-8")
            req = urllib.request.Request(
                self.endpoint_url,
                data=req_body,
                headers={"Content-Type": "application/json", "User-Agent": "DeliveryFleet-A2A-Bridge/1.0"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=0.25) as response:
                if response.status == 200:
                    self._network_available = True
                    resp_json = json.loads(response.read().decode("utf-8"))
                    if "payload" in resp_json:
                        return A2AResponse.model_validate(resp_json["payload"])
                    return A2AResponse.model_validate(resp_json)
        except Exception:
            self._network_available = False
            return None
        return None

    def send_routing_request(
        self,
        from_agent: str,
        task_id: str,
        request: A2ARequest,
        run_id: str = "run-0"
    ) -> A2AResponse:
        """Encapsulate request in standard A2A envelope, route via network or in-process, and return response."""
        req_envelope = A2AMessage(
            message_id=f"msg-{uuid.uuid4().hex[:8]}",
            task_id=task_id,
            from_agent=from_agent,
            to_agent=self.adk_route_agent.agent_id,
            message_type="request",
            payload=request.model_dump()
        )
        with self._lock:
            self.message_history.append(req_envelope)

        response: Optional[A2AResponse] = None

        # Network transport attempt with circuit-breaker shielding
        if self._should_attempt_network():
            response = self._call_network_endpoint(req_envelope)

        # Fallback to local in-process dispatch if network mode is in_process or endpoint unreachable
        if response is None:
            response = self.adk_route_agent.handle_a2a_request(request, run_id=run_id)

        resp_envelope = A2AMessage(
            message_id=f"msg-{uuid.uuid4().hex[:8]}",
            task_id=task_id,
            from_agent=self.adk_route_agent.agent_id,
            to_agent=from_agent,
            message_type="response",
            payload=response.model_dump()
        )
        with self._lock:
            self.message_history.append(resp_envelope)

        return response

    def get_message_history(self) -> List[A2AMessage]:
        """Return thread-safe snapshot of inter-agent messages."""
        with self._lock:
            return list(self.message_history)

    def clear_history(self) -> None:
        """Clear message history safely."""
        with self._lock:
            self.message_history.clear()
