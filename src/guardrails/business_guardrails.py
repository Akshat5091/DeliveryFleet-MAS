"""Business Compliance and Operational Safety Guardrails."""
from typing import Dict, Any, List, Tuple
import math
from ..config import MAX_LEGAL_DRIVER_HOURS, NEAR_FATIGUE_THRESHOLD_HOURS, ZONE_B_HEAVY_FREIGHT_LIMIT_KG
from ..schemas.decisions import GuardrailEvaluation

class BusinessGuardrails:
    """Evaluates proposed driver assignments and routes against legal and municipal bylaws."""

    def evaluate_dispatch(
        self,
        driver: Dict[str, Any],
        order_weight_kg: float,
        dropoff_location: str,
        estimated_eta_mins: float,
        hour_of_day: int = 14
    ) -> GuardrailEvaluation:
        """Check proposed dispatch against working hours and urban freight constraints."""
        if not driver or not isinstance(driver, dict):
            return GuardrailEvaluation(
                passed=False,
                violations=["NO_DRIVER_ASSIGNED: Driver record is missing, empty, or unallocated."],
                action_taken="BLOCK",
                interventions=1
            )

        violations = []
        action = "ALLOW"
        
        # 1. Legal Maximum Working Hours (Strict 9.0h)
        try:
            hours = float(driver.get("hours_worked", 0.0))
            if not math.isfinite(hours):
                hours = 0.0
        except (ValueError, TypeError):
            hours = 0.0

        driver_id = str(driver.get("driver_id", "UNKNOWN"))

        if hours >= MAX_LEGAL_DRIVER_HOURS:
            violations.append(
                f"FATAL_VIOLATION: Driver {driver_id} has worked {hours:.1f}h (Legal limit {MAX_LEGAL_DRIVER_HOURS}h)"
            )
            action = "BLOCK"

        # 2. Fatigue Pre-emption: If near 8.5h and trip ETA > 30 mins
        elif hours >= NEAR_FATIGUE_THRESHOLD_HOURS and estimated_eta_mins > 30.0:
            violations.append(
                f"FATIGUE_RISK: Driver {driver_id} at {hours:.1f}h cannot undertake {estimated_eta_mins:.1f}m assignment"
            )
            action = "BLOCK"

        # 3. Zone B Heavy Freight Restriction (Peak 17:00-20:00 > 50kg)
        loc_str = str(dropoff_location or "").lower()
        safe_weight = float(order_weight_kg or 0.0)
        safe_hour = int(hour_of_day or 14)

        if "zone b" in loc_str and safe_weight > ZONE_B_HEAVY_FREIGHT_LIMIT_KG:
            if 17 <= safe_hour <= 20:
                violations.append(
                    f"ZONE_RESTRICTION: Zone B prohibits freight > {ZONE_B_HEAVY_FREIGHT_LIMIT_KG}kg during peak hours (Current: {safe_weight}kg at {safe_hour}:00)"
                )
                if action != "BLOCK":
                    action = "FLAG_FOR_REVIEW"

        # 4. Vehicle Payload Capacity Check
        try:
            capacity = float(driver.get("capacity_kg", 0.0))
            if not math.isfinite(capacity):
                capacity = 0.0
        except (ValueError, TypeError):
            capacity = 0.0

        if safe_weight > capacity:
            violations.append(
                f"CAPACITY_OVERLOAD: Order weight {safe_weight}kg exceeds vehicle limit {capacity}kg"
            )
            action = "BLOCK"

        passed = len(violations) == 0
        return GuardrailEvaluation(
            passed=passed,
            violations=violations,
            action_taken=action if not passed else "ALLOW",
            interventions=len(violations)
        )

