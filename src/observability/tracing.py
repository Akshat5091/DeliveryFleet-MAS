"""OpenTelemetry-Compatible Tracing & Provenance Ledger.
Course: CSE3101 Agentic AI | Group 8 | Multi-Agent Delivery Fleet
Fully integrates OpenTelemetry TracerProvider, SimpleSpanProcessor, and InMemorySpanExporter.
"""
import threading
import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# OpenTelemetry Standard SDK imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

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
    """Manages distributed traces across CrewAI and Google ADK frameworks backed by OpenTelemetry SDK."""

    def __init__(self):
        self.traces: Dict[str, List[TraceSpan]] = {}
        self._lock = threading.RLock()

        # Initialize OpenTelemetry TracerProvider and In-Memory Span Processor
        self.otel_exporter = InMemorySpanExporter()
        self.tracer_provider = TracerProvider()
        self.tracer_provider.add_span_processor(SimpleSpanProcessor(self.otel_exporter))
        self.otel_tracer = self.tracer_provider.get_tracer("DeliveryFleet-MAS", "3.0.0")
        self._active_otel_spans: Dict[str, Any] = {}

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
        """Start a new child span within the active order trace and record in OpenTelemetry SDK."""
        with self._lock:
            self.start_trace(trace_id)
            attrs = attributes or {}
            span = TraceSpan(
                trace_id=trace_id,
                parent_span_id=parent_span_id,
                name=name,
                agent_name=agent_name,
                start_time=time.time(),
                attributes=attrs
            )
            self.traces[trace_id].append(span)

            # Create corresponding OpenTelemetry standard span
            try:
                otel_span = self.otel_tracer.start_span(
                    name=name,
                    attributes={
                        "order.id": trace_id,
                        "agent.name": agent_name,
                        "span.id": span.span_id,
                        **{str(k): str(v) for k, v in attrs.items()}
                    }
                )
                self._active_otel_spans[span.span_id] = otel_span
            except Exception:
                pass

            return span

    def end_span(
        self,
        span: TraceSpan,
        status: str = "OK",
        extra_attributes: Optional[Dict[str, Any]] = None
    ) -> None:
        """End span, compute execution duration, and export through OpenTelemetry processor."""
        with self._lock:
            span.end_time = time.time()
            span.duration_ms = round((span.end_time - span.start_time) * 1000.0, 2)
            span.status = status
            if extra_attributes:
                span.attributes.update(extra_attributes)

            # End OpenTelemetry standard span
            otel_span = self._active_otel_spans.pop(span.span_id, None)
            if otel_span:
                try:
                    if extra_attributes:
                        for k, v in extra_attributes.items():
                            otel_span.set_attribute(str(k), str(v))
                    otel_span.set_attribute("mas.status", status)
                    otel_span.set_attribute("mas.duration_ms", span.duration_ms)
                    otel_span.end()
                except Exception:
                    pass

    def get_trace_summary(self, trace_id: str) -> List[Dict[str, Any]]:
        """Return serialized hierarchy of spans for a trace."""
        with self._lock:
            spans = self.traces.get(trace_id, [])
            return [s.model_dump() for s in spans]

    def get_exported_otel_spans(self) -> List[Any]:
        """Return raw OpenTelemetry SDK spans captured by the in-memory exporter."""
        return list(self.otel_exporter.get_finished_spans())

    def clear(self) -> None:
        """Clear all active and exported traces."""
        with self._lock:
            self.traces.clear()
            self._active_otel_spans.clear()
            self.otel_exporter.clear()
