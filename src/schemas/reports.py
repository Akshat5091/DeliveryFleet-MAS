"""Final Delivery Report Schema with JSON and Markdown Table formatters."""
from typing import List, Optional, Dict, Any
import json
from pydantic import BaseModel, Field
from .decisions import DispatchDecision, RoutePlan, ExceptionReplan, GuardrailEvaluation
from .blackboard import BlackboardEntry

class FinalDeliveryReport(BaseModel):
    """End-to-end structured mission report for an order dispatch."""
    order_id: str
    priority: str
    customer_persona: str
    input_guard_status: str
    assigned_driver_id: str
    assigned_driver_name: str
    selected_route: str
    distance_km: float
    final_eta_mins: float
    predicted_delay_mins: float
    delivery_outcome: str  # "SUCCESS", "RECOVERED_VIA_EXCEPTION", "BLOCKED_BY_GUARDRAIL"
    total_execution_latency_sec: float
    total_tokens_consumed: int
    estimated_cost_usd: float
    guardrail_summary: GuardrailEvaluation
    exception_details: Optional[ExceptionReplan] = None
    provenance_trail: List[BlackboardEntry] = Field(default_factory=list)

    def to_json(self, indent: int = 2) -> str:
        """Render report as indented JSON string."""
        return self.model_dump_json(indent=indent)

    def to_markdown_table(self) -> str:
        """Render key operational metrics as a Markdown Table."""
        lines = [
            "### 📦 Final Delivery Dispatch Report",
            "",
            "| Parameter | Value | Description |",
            "| :--- | :--- | :--- |",
            f"| **Order ID** | `{self.order_id}` | Unique consignment identifier |",
            f"| **Priority** | `{self.priority}` | SLA dispatch urgency |",
            f"| **Customer Persona** | `{self.customer_persona}` | Input communication style |",
            f"| **Input Guard Status** | `{self.input_guard_status}` | Prompt security assessment |",
            f"| **Assigned Driver** | `{self.assigned_driver_id} ({self.assigned_driver_name})` | Optimal vehicle assignment |",
            f"| **Selected Route** | `{self.selected_route}` | Multi-factor optimized transit |",
            f"| **Distance** | `{self.distance_km:.1f} km` | Path transit length |",
            f"| **Final ETA** | `{self.final_eta_mins:.1f} mins` | Congestion-adjusted arrival time |",
            f"| **Predicted Delay** | `{self.predicted_delay_mins:.1f} mins` | ML regression forecast |",
            f"| **Delivery Outcome** | **`{self.delivery_outcome}`** | Operational fulfillment state |",
            f"| **End-to-End Latency** | `{self.total_execution_latency_sec:.3f} s` | Total MAS computation time |",
            f"| **Total Tokens** | `{self.total_tokens_consumed:,}` | Agent reasoning token usage |",
            f"| **Estimated Cost** | `${self.estimated_cost_usd:.5f}` | Cloud LLM inference expenditure |",
            f"| **Guardrail Status** | `{'PASS' if self.guardrail_summary.passed else 'INTERCEPTED'}` | Safety check result |"
        ]
        if self.exception_details:
            lines.extend([
                "",
                "#### 🚨 Dynamic Exception Recovery Event",
                f"- **Disruption Cause:** `{self.exception_details.disruption_cause}`",
                f"- **Recovery Action:** `{self.exception_details.recovery_action}`",
                f"- **Reassigned Driver:** `{self.exception_details.reassigned_driver_id}`",
                f"- **Time Saved:** `{self.exception_details.time_saved_mins:.1f} minutes`"
            ])
        return "\n".join(lines)
