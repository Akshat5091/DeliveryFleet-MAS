"""Callback Hooks for CrewAI and Google ADK Agent Execution Lifecycle."""
import threading
import time
from typing import Dict, Any, Optional
from .run_logger import RunLogger

class MASCallbackHandler:
    """Unified callback processor linking framework lifecycles to RunLogger with thread-safe span tracking."""

    def __init__(self, logger: Optional[RunLogger] = None):
        self.logger = logger or RunLogger.get_logger()
        self._active_spans: Dict[str, float] = {}
        self._lock = threading.Lock()

    def on_agent_start(self, agent_name: str, framework: str, run_id: str, order_id: str) -> None:
        """Invoked when an agent starts reasoning."""
        key = f"{run_id}:{order_id}:{agent_name}"
        with self._lock:
            self._active_spans[key] = time.time()

    def on_agent_finish(
        self,
        agent_name: str,
        framework: str,
        run_id: str,
        order_id: str,
        input_tokens: int = 150,
        output_tokens: int = 80,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Invoked when an agent completes reasoning."""
        key = f"{run_id}:{order_id}:{agent_name}"
        with self._lock:
            start_time = self._active_spans.pop(key, time.time() - 0.25)
        end_time = time.time()

        self.logger.log_event(
            run_id=run_id,
            order_id=order_id,
            agent_name=agent_name,
            framework=framework,
            event_type="AGENT_COMPLETE",
            start_time=start_time,
            end_time=end_time,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            status=status,
            error_message=error_message,
            metadata=metadata
        )

    def on_tool_call(
        self,
        tool_name: str,
        agent_name: str,
        framework: str,
        run_id: str,
        order_id: str,
        duration_sec: float = 0.05
    ) -> None:
        """Invoked when an agent executes an MCP tool."""
        now = time.time()
        self.logger.log_event(
            run_id=run_id,
            order_id=order_id,
            agent_name=agent_name,
            framework=framework,
            event_type="TOOL_CALL",
            start_time=now - duration_sec,
            end_time=now,
            input_tokens=25,
            output_tokens=30,
            status="SUCCESS",
            metadata={"tool_name": tool_name}
        )

