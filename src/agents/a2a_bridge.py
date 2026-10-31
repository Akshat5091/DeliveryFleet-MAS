"""A2A Protocol Interoperability Bridge connecting CrewAI and Google ADK."""
import uuid
import time
import threading
from typing import Dict, Any, Optional, List
from ..schemas.a2a import A2AMessage, A2ARequest, A2AResponse
from .adk_route_agent import ADKRouteAgent
from ..observability.run_logger import RunLogger

class A2ABridge:
    """Inter-framework communication bus enabling CrewAI agents to send messages to Google ADK agents."""

    def __init__(self, adk_route_agent: Optional[ADKRouteAgent] = None):
        self.adk_route_agent = adk_route_agent or ADKRouteAgent()
        self.logger = RunLogger.get_logger()
        self.message_history: List[A2AMessage] = []
        self._lock = threading.RLock()

    def send_routing_request(
        self,
        from_agent: str,
        task_id: str,
        request: A2ARequest,
        run_id: str = "run-0"
    ) -> A2AResponse:
        """Encapsulate request in standard A2A envelope, route to ADK agent, and return validated response."""
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

        # Dispatch across protocol boundary to ADK agent
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

