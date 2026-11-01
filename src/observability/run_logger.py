"""Run Event Logger capturing per-agent metrics, latency, tokens, cost, and errors.
Course: CSE3101 Agentic AI | Group 8 | Multi-Agent Delivery Fleet
Robust persistence with error ledger, directory guarantee, and thread safety.
"""
import threading
from typing import List, Dict, Any, Optional
import json
import time
import sys
from pathlib import Path
from pydantic import BaseModel, Field
from ..config import RUN_LOGS_DIR, COST_PER_INPUT_TOKEN, COST_PER_OUTPUT_TOKEN

class AgentEvent(BaseModel):
    """Event record emitted by agent callback hooks."""
    run_id: str
    order_id: str
    agent_name: str
    framework: str  # "CrewAI" or "Google-ADK"
    event_type: str # "AGENT_START", "AGENT_COMPLETE", "TOOL_CALL", "GUARDRAIL_INTERCEPTION", "ERROR"
    start_time: float
    end_time: float
    latency_seconds: float
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    status: str = "SUCCESS"
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RunLogger:
    """Central singleton logger aggregating MAS execution events for heatmap and boxplot analytics with thread safety."""
    _instance: Optional["RunLogger"] = None
    _init_lock = threading.Lock()

    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or (RUN_LOGS_DIR / "run_events.jsonl")
        self.events: List[AgentEvent] = []
        self.persistence_errors: List[str] = []
        self._lock = threading.RLock()
        
        # Ensure log directory exists
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.persistence_errors.append(f"Directory creation failure: {e}")

    @classmethod
    def get_logger(cls) -> "RunLogger":
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = RunLogger()
        return cls._instance

    def log_event(
        self,
        run_id: str,
        order_id: str,
        agent_name: str,
        framework: str,
        event_type: str,
        start_time: float,
        end_time: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentEvent:
        """Create, append, and persist an execution event safely across threads."""
        latency = max(0.001, end_time - start_time)
        safe_in = max(0, int(input_tokens or 0))
        safe_out = max(0, int(output_tokens or 0))
        cost = (safe_in * COST_PER_INPUT_TOKEN) + (safe_out * COST_PER_OUTPUT_TOKEN)
        
        event = AgentEvent(
            run_id=str(run_id),
            order_id=str(order_id),
            agent_name=str(agent_name),
            framework=str(framework),
            event_type=str(event_type),
            start_time=float(start_time),
            end_time=float(end_time),
            latency_seconds=round(latency, 4),
            input_tokens=safe_in,
            output_tokens=safe_out,
            estimated_cost_usd=round(cost, 6),
            status=str(status),
            error_message=error_message,
            metadata=metadata or {}
        )
        with self._lock:
            self.events.append(event)
            
            # Append to persistent JSONL log with active error tracking
            try:
                self.log_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(event.model_dump_json() + "\n")
            except Exception as e:
                err_msg = f"Failed to persist event {event.run_id} ({event.agent_name}): {e}"
                self.persistence_errors.append(err_msg)
                sys.stderr.write(f"[RunLogger Warning] {err_msg}\n")

        return event

    def get_all_events(self) -> List[AgentEvent]:
        """Return all logged in-memory events (thread-safe snapshot)."""
        with self._lock:
            return list(self.events)

    def get_persistence_errors(self) -> List[str]:
        """Return ledger of any persistence errors encountered."""
        with self._lock:
            return list(self.persistence_errors)

    def clear(self) -> None:
        """Reset in-memory log list and error ledger."""
        with self._lock:
            self.events.clear()
            self.persistence_errors.clear()
