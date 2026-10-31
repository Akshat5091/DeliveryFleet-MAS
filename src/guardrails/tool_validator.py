"""Tool Return Validation and Schema Guardrail."""
from typing import Dict, Any, List, Tuple
import math

class ToolValidator:
    """Validates runtime outputs returned from MCP tools and incoming client orders before agent ingestion."""

    @staticmethod
    def validate_driver_data(driver: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Ensure driver record contains physically valid numbers and mandatory keys."""
        errors = []
        if not isinstance(driver, dict):
            return (False, ["Driver record must be a dictionary."])

        required_keys = ["driver_id", "current_zone", "capacity_kg", "hours_worked", "status"]
        for k in required_keys:
            if k not in driver or driver[k] is None:
                errors.append(f"Missing mandatory key: {k}")

        if "hours_worked" in driver:
            try:
                hrs = float(driver["hours_worked"])
                if not math.isfinite(hrs) or hrs < 0:
                    errors.append("Invalid negative shift hours")
            except (ValueError, TypeError):
                errors.append("Non-numeric shift hours")

        if "capacity_kg" in driver:
            try:
                cap = float(driver["capacity_kg"])
                if not math.isfinite(cap) or cap <= 0:
                    errors.append("Invalid non-positive vehicle capacity")
            except (ValueError, TypeError):
                errors.append("Non-numeric vehicle capacity")

        if "rating" in driver:
            try:
                rt = float(driver["rating"])
                if not math.isfinite(rt) or rt < 1.0 or rt > 5.0:
                    errors.append("Driver rating must be between 1.0 and 5.0")
            except (ValueError, TypeError):
                errors.append("Non-numeric driver rating")

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_route_data(route_info: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate distance and ETA values from routing tool."""
        errors = []
        if not isinstance(route_info, dict):
            return (False, ["Route info must be a dictionary."])

        if "distance_km" not in route_info:
            errors.append("Invalid or missing transit distance")
        else:
            try:
                dist = float(route_info["distance_km"])
                if not math.isfinite(dist) or dist < 0:
                    errors.append("Invalid or missing transit distance")
            except (ValueError, TypeError):
                errors.append("Invalid or missing transit distance")

        if "congestion_adjusted_eta_mins" not in route_info:
            errors.append("Invalid or non-positive ETA")
        else:
            try:
                eta = float(route_info["congestion_adjusted_eta_mins"])
                if not math.isfinite(eta) or eta < 0:
                    errors.append("Invalid or non-positive ETA")
            except (ValueError, TypeError):
                errors.append("Invalid or non-positive ETA")

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_order_data(order: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate consignment order payload before MAS ingestion."""
        errors = []
        if not isinstance(order, dict):
            return (False, ["Order payload must be a dictionary."])

        order_id = str(order.get("order_id", "")).strip()
        if not order_id:
            errors.append("order_id is required and cannot be empty.")

        pickup = str(order.get("pickup", "")).strip()
        if not pickup:
            errors.append("pickup location is required and cannot be empty.")

        dropoff = str(order.get("dropoff", "")).strip()
        if not dropoff:
            errors.append("dropoff location is required and cannot be empty.")

        if "weight_kg" not in order:
            errors.append("weight_kg is required.")
        else:
            try:
                wt = float(order["weight_kg"])
                if not math.isfinite(wt) or wt <= 0:
                    errors.append("weight_kg must be a positive number.")
            except (ValueError, TypeError):
                errors.append("weight_kg must be a valid numeric value.")

        if "deadline_mins" not in order:
            errors.append("deadline_mins is required.")
        else:
            try:
                dl = int(order["deadline_mins"])
                if dl <= 0:
                    errors.append("deadline_mins must be a positive integer.")
            except (ValueError, TypeError):
                errors.append("deadline_mins must be a valid integer.")

        priority = str(order.get("priority", "NORMAL")).upper()
        if priority not in ["LOW", "NORMAL", "HIGH", "CRITICAL", "EMERGENCY"]:
            errors.append(f"Invalid priority level: '{priority}'. Expected one of LOW, NORMAL, HIGH, CRITICAL.")

        return (len(errors) == 0, errors)

