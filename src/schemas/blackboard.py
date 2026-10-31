"""Blackboard (Shared State) Architecture Pydantic Schema."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class CandidateDriver(BaseModel):
    driver_id: str
    name: str
    current_zone: str
    vehicle_type: str
    capacity_kg: float
    hours_worked: float
    rating: float
    status: str

class RetrievedRule(BaseModel):
    source: str
    snippet: str
    relevance_score: float = 1.0

class BlackboardEntry(BaseModel):
    agent_name: str
    field_modified: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    description: str

class BlackboardState(BaseModel):
    """Global shared state object per delivery order in MAS."""
    order_id: str
    pickup: str
    dropoff: str
    weight_kg: float
    priority: str
    deadline_mins: int
    persona: str = "polite"
    customer_notes: Optional[str] = ""
    masked_notes: Optional[str] = None

    
    # Context populated by Gathering / Retrieval
    candidate_drivers: List[CandidateDriver] = Field(default_factory=list)
    retrieved_rules: List[RetrievedRule] = Field(default_factory=list)
    predicted_delay_mins: float = 0.0
    traffic_factor: float = 1.0
    weather_summary: str = "Clear"

    # Decisions populated by Agents
    assigned_driver_id: Optional[str] = None
    dispatch_rationale: Optional[str] = None
    selected_route: Optional[str] = None
    distance_km: float = 0.0
    estimated_eta_mins: float = 0.0
    
    # Exception handling state
    exception_triggered: bool = False
    exception_reason: Optional[str] = None
    replan_driver_id: Optional[str] = None
    replan_route: Optional[str] = None
    replan_eta_mins: Optional[float] = None
    
    # Safety and Guardrail flags
    guardrail_passed: bool = True
    guardrail_violations: List[str] = Field(default_factory=list)
    interventions_count: int = 0
    
    # Execution Provenance Trail (Auditability)
    provenance_log: List[BlackboardEntry] = Field(default_factory=list)

    def log_update(self, agent_name: str, field_modified: str, description: str) -> None:
        """Record state update to ensure complete execution provenance."""
        self.provenance_log.append(
            BlackboardEntry(
                agent_name=agent_name,
                field_modified=field_modified,
                description=description
            )
        )
