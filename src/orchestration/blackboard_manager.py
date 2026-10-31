"""Blackboard Shared State Store and Context Synchronization Manager."""
import threading
from typing import Dict, Any, Optional, List, Tuple
from ..schemas.blackboard import BlackboardState, CandidateDriver, RetrievedRule

class BlackboardManager:
    """Central context broker managing Blackboard state per delivery order with thread-safe locking."""

    def __init__(self):
        self._states: Dict[str, BlackboardState] = {}
        self._lock = threading.RLock()

    def initialize_order_state(
        self,
        order_id: str,
        pickup: str,
        dropoff: str,
        weight_kg: float,
        priority: str,
        deadline_mins: int,
        persona: str = "polite",
        customer_notes: str = ""
    ) -> BlackboardState:
        """Create a fresh blackboard entry for incoming order with thread-safe synchronization."""
        if not order_id or not isinstance(order_id, str):
            raise ValueError("order_id must be a non-empty string.")

        safe_notes = str(customer_notes or "")
        safe_persona = str(persona or "polite")

        with self._lock:
            state = BlackboardState(
                order_id=order_id,
                pickup=pickup,
                dropoff=dropoff,
                weight_kg=float(weight_kg),
                priority=str(priority),
                deadline_mins=int(deadline_mins),
                persona=safe_persona,
                customer_notes=safe_notes
            )

            state.log_update(
                agent_name="FleetOrchestrator",
                field_modified="order_profile",
                description=f"Initialized state for order {order_id}"
            )
            self._states[order_id] = state
            return state

    def get_state(self, order_id: str) -> Optional[BlackboardState]:
        """Fetch active blackboard state (thread-safe reference)."""
        with self._lock:
            return self._states.get(order_id)

    def get_state_snapshot(self, order_id: str) -> Optional[BlackboardState]:
        """Fetch an isolated deep copy snapshot of active blackboard state preventing read/write contention."""
        with self._lock:
            state = self._states.get(order_id)
            return state.model_copy(deep=True) if state else None

    def update_field(
        self,
        order_id: str,
        agent_name: str,
        field_name: str,
        value: Any,
        description: str
    ) -> None:
        """Record intermediate agent decision or context update to shared blackboard with lock protection."""
        with self._lock:
            state = self._states.get(order_id)
            if not state:
                raise KeyError(f"Blackboard state for order {order_id} not initialized.")

            if hasattr(state, field_name):
                setattr(state, field_name, value)
                state.log_update(agent_name=agent_name, field_modified=field_name, description=description)
            else:
                raise AttributeError(f"Field '{field_name}' not defined in BlackboardState schema.")

    def batch_update_fields(
        self,
        order_id: str,
        agent_name: str,
        updates: List[Tuple[str, Any, str]]
    ) -> None:
        """Atomically apply multiple updates to blackboard state in a single transaction."""
        with self._lock:
            state = self._states.get(order_id)
            if not state:
                raise KeyError(f"Blackboard state for order {order_id} not initialized.")

            for field_name, value, description in updates:
                if hasattr(state, field_name):
                    setattr(state, field_name, value)
                    state.log_update(agent_name=agent_name, field_modified=field_name, description=description)
                else:
                    raise AttributeError(f"Field '{field_name}' not defined in BlackboardState schema.")

    def list_active_orders(self) -> List[str]:
        """List all active order IDs managed in memory."""
        with self._lock:
            return list(self._states.keys())

    def delete_order_state(self, order_id: str) -> bool:
        """Remove state for an archived order to reclaim memory."""
        with self._lock:
            return self._states.pop(order_id, None) is not None

    def clear_all(self) -> None:
        """Clear all blackboard states."""
        with self._lock:
            self._states.clear()

