"""OpenTelemetry-Compatible Tracing & Provenance Ledger."""
import threading
import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class TraceSpan(BaseModel):
    """Execution span representing an atomic unit of agentic reasoning or tool invocation."""
    span_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_span_id: Optional[str] = None
    trace_id: str
    name: str
    agent_name: str
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "OK"

class MASTracer:
    """Manages distributed traces across CrewAI and Google ADK frameworks with thread-safe synchronization."""

    def __init__(self):
        self.traces: Dict[str, List[TraceSpan]] = {}
        self._lock = threading.RLock()

    def start_trace(self, trace_id: str) -> str:
        """Initialize trace for a given order."""
        with self._lock:
            if trace_id not in self.traces:
                self.traces[trace_id] = []
            return trace_id

    def start_span(
        self,
        trace_id: str,
        name: str,
        agent_name: str,
        parent_span_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> TraceSpan:
        """Start a new child span within the active order trace."""
        with self._lock:
            self.start_trace(trace_id)
            span = TraceSpan(
                trace_id=trace_id,
                parent_span_id=parent_span_id,
                name=name,
                agent_name=agent_name,
                start_time=time.time(),
                attributes=attributes or {}
            )
            self.traces[trace_id].append(span)
            return span

    def end_span(
        self,
        span: TraceSpan,
        status: str = "OK",
        extra_attributes: Optional[Dict[str, Any]] = None
    ) -> None:
        """End span and compute execution duration."""
        with self._lock:
            span.end_time = time.time()
            span.duration_ms = round((span.end_time - span.start_time) * 1000.0, 2)
            span.status = status
            if extra_attributes:
                span.attributes.update(extra_attributes)

    def get_trace_summary(self, trace_id: str) -> List[Dict[str, Any]]:
        """Return serialized hierarchy of spans for a trace."""
        with self._lock:
            spans = self.traces.get(trace_id, [])
            return [s.model_dump() for s in spans]

