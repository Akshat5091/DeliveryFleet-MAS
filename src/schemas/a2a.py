"""Agent-to-Agent (A2A) Protocol Standard Models for Inter-Framework Communication."""
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class AgentCard(BaseModel):
    """A2A Agent Card exposing service capabilities for cross-framework discovery."""
    agent_id: str
    framework: str  # "Google-ADK" or "CrewAI"
    description: str
    capabilities: list[str]
    endpoint_url: Optional[str] = None
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)

class A2AMessage(BaseModel):
    """Standardized Agent-to-Agent communication envelope."""
    protocol_version: str = "A2A/1.0"
    message_id: str
    task_id: str
    from_agent: str
    to_agent: str
    message_type: str  # "request", "response", "event", "guardrail_alert"
    payload: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class A2ARequest(BaseModel):
    """Structured request payload sent to the ADK Route Agent."""
    order_id: str
    driver_id: str
    pickup_zone: str
    dropoff_zone: str
    priority: str = "NORMAL"

class A2AResponse(BaseModel):
    """Structured response payload returned by the ADK Route Agent."""
    status: str  # "SUCCESS" or "ERROR"
    route_name: str
    distance_km: float
    base_eta_mins: float
    congestion_adjusted_eta_mins: float
    alternative_routes: list[Dict[str, Any]] = Field(default_factory=list)
    tool_calls_count: int = 1
