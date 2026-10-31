"""Tool 5: Shared Blackboard State Read/Write MCP Tool."""
import threading
from typing import Dict, Any, Optional
from ..tools.driver_db import DriverDBTool
from ...schemas.blackboard import BlackboardState, CandidateDriver, RetrievedRule

class BlackboardTool:
    """Tool exposing Blackboard state read/write operations for multi-agent coordination with thread-safe locking."""
    name: str = "blackboard_state_tool"
    description: str = "Reads and writes to the centralized blackboard shared state with execution provenance tracking."

    def __init__(self, state_store: Optional[Dict[str, BlackboardState]] = None):
        self.state_store = state_store if state_store is not None else {}
        self._lock = threading.RLock()

    def get_state(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve complete blackboard state as dictionary (thread-safe)."""
        with self._lock:
            state = self.state_store.get(order_id)
            return state.model_dump() if state else None

    def post_update(
        self,
        order_id: str,
        agent_name: str,
        field_name: str,
        value: Any,
        description: str
    ) -> Dict[str, Any]:
        """Update a specific section of the blackboard with agent audit entry (thread-safe)."""
        with self._lock:
            if order_id not in self.state_store:
                raise KeyError(f"Blackboard state for order {order_id} does not exist.")

            state = self.state_store[order_id]
            if hasattr(state, field_name):
                setattr(state, field_name, value)
                state.log_update(agent_name=agent_name, field_modified=field_name, description=description)
                return {"status": "SUCCESS", "order_id": order_id, "updated_field": field_name}
            else:
                return {"status": "ERROR", "message": f"Field '{field_name}' not in Blackboard schema"}

