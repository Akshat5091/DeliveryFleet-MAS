"""Tool 2: Routing Engine and Congestion Optimization Tool."""
from typing import Dict, Any, List, Optional
import csv
import math
from pathlib import Path
from ...config import TRAFFIC_CSV

# Distance matrix across primary operational zones (km)
ZONE_DISTANCES = {
    ("Zone A", "Zone B"): 14.5,
    ("Zone B", "Zone A"): 14.5,
    ("Zone A", "Zone C"): 18.0,
    ("Zone C", "Zone A"): 18.0,
    ("Zone A", "Zone D"): 26.5,
    ("Zone D", "Zone A"): 26.5,
    ("Zone B", "Zone C"): 12.0,
    ("Zone C", "Zone B"): 12.0,
    ("Zone B", "Zone D"): 21.0,
    ("Zone D", "Zone B"): 21.0,
    ("Zone C", "Zone D"): 16.5,
    ("Zone D", "Zone C"): 16.5,
}

DEFAULT_TRAFFIC_DATA = {
    "Zone A -> Zone B": {"congestion_level": "HIGH", "speed_factor": 0.65, "avg_speed_kmh": 26.0},
    "Zone B -> Zone A": {"congestion_level": "HIGH", "speed_factor": 0.60, "avg_speed_kmh": 24.0},
    "Zone A -> Zone C": {"congestion_level": "MODERATE", "speed_factor": 0.80, "avg_speed_kmh": 35.0},
    "Zone C -> Zone A": {"congestion_level": "LOW", "speed_factor": 0.95, "avg_speed_kmh": 42.0},
    "Zone B -> Zone D": {"congestion_level": "MODERATE", "speed_factor": 0.85, "avg_speed_kmh": 38.0},
    "Zone D -> Zone B": {"congestion_level": "MODERATE", "speed_factor": 0.82, "avg_speed_kmh": 36.0},
    "Zone C -> Zone D": {"congestion_level": "LOW", "speed_factor": 1.00, "avg_speed_kmh": 45.0},
    "Zone D -> Zone C": {"congestion_level": "LOW", "speed_factor": 0.95, "avg_speed_kmh": 43.0},
    "Zone A -> Zone D": {"congestion_level": "SEVERE", "speed_factor": 0.50, "avg_speed_kmh": 20.0},
    "Zone D -> Zone A": {"congestion_level": "HIGH", "speed_factor": 0.65, "avg_speed_kmh": 28.0},
    "Zone B -> Zone C": {"congestion_level": "MODERATE", "speed_factor": 0.80, "avg_speed_kmh": 35.0},
    "Zone C -> Zone B": {"congestion_level": "MODERATE", "speed_factor": 0.78, "avg_speed_kmh": 34.0},
}

class RoutingEngineTool:
    """Tool for computing transit distances, congestion factors, and optimal routes with division-by-zero guards."""
    name: str = "routing_engine"
    description: str = "Calculates fastest route, distance, and congestion-adjusted ETA between pickup and dropoff points."

    def __init__(self, traffic_csv_path: Optional[Path] = None):
        self.traffic_csv_path = traffic_csv_path or TRAFFIC_CSV
        self.traffic_cache: Dict[str, Dict[str, Any]] = dict(DEFAULT_TRAFFIC_DATA)
        self._load_traffic_cache()

    def _load_traffic_cache(self) -> None:
        """Load traffic factors into fast lookup cache with graceful fallback."""
        if not self.traffic_csv_path.exists():
            return

        try:
            with open(self.traffic_csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    route_name = row.get("route", "").strip()
                    if not route_name:
                        continue
                    speed_factor = float(row.get("speed_factor", 0.80))
                    avg_speed = float(row.get("avg_speed_kmh", 35.0))
                    self.traffic_cache[route_name] = {
                        "congestion_level": row.get("congestion_level", "MODERATE"),
                        "speed_factor": max(0.1, speed_factor) if math.isfinite(speed_factor) else 0.80,
                        "avg_speed_kmh": max(10.0, avg_speed) if math.isfinite(avg_speed) else 35.0
                    }
        except Exception:
            pass  # Fallback to DEFAULT_TRAFFIC_DATA

    def _extract_zone(self, location_str: Any) -> str:
        """Helper to extract Zone prefix from detailed location string safely."""
        if not location_str or not isinstance(location_str, str):
            return "Zone A"
        loc_clean = location_str.strip().lower()
        for z in ["Zone A", "Zone B", "Zone C", "Zone D"]:
            if z.lower() in loc_clean:
                return z
        return "Zone A"

    def calculate_route(
        self,
        pickup_location: str,
        dropoff_location: str,
        priority: str = "NORMAL"
    ) -> Dict[str, Any]:
        """Compute primary and alternative routes with congestion-adjusted ETAs and zero-division defenses."""
        p_str = str(pickup_location or "").strip()
        d_str = str(dropoff_location or "").strip()

        # Check for identical pickup and dropoff locations
        if p_str and d_str and p_str.lower() == d_str.lower():
            return {
                "primary_route": f"Intra-Facility Direct Transfer [{p_str}]",
                "distance_km": 0.0,
                "base_eta_mins": 0.0,
                "congestion_adjusted_eta_mins": 0.0,
                "congestion_level": "NONE",
                "speed_factor": 1.0,
                "alternative_routes": [
                    {"name": f"Alternative Internal Bay Transfer [{p_str}]", "distance_km": 0.0, "eta_mins": 0.0},
                    {"name": f"Pedestrian / Hand-Trolley Transfer [{p_str}]", "distance_km": 0.0, "eta_mins": 0.0}
                ]
            }

        src_zone = self._extract_zone(p_str)
        dst_zone = self._extract_zone(d_str)

        if src_zone == dst_zone:
            distance = 6.0
        else:
            distance = ZONE_DISTANCES.get((src_zone, dst_zone), 15.0)

        route_key = f"{src_zone} -> {dst_zone}"
        traffic_info = self.traffic_cache.get(route_key, {
            "congestion_level": "MODERATE",
            "speed_factor": 0.80,
            "avg_speed_kmh": 35.0
        })

        raw_avg_speed = float(traffic_info.get("avg_speed_kmh", 35.0))
        raw_speed_factor = float(traffic_info.get("speed_factor", 0.80))
        if not math.isfinite(raw_avg_speed) or raw_avg_speed <= 0:
            raw_avg_speed = 35.0
        if not math.isfinite(raw_speed_factor) or raw_speed_factor <= 0:
            raw_speed_factor = 0.80

        # Dynamic priority priority-lane / green corridor adjustment
        priority_norm = (priority or "NORMAL").upper()
        if priority_norm in ["CRITICAL", "EMERGENCY"]:
            effective_speed_factor = min(1.2, raw_speed_factor * 1.15)
        elif priority_norm == "HIGH":
            effective_speed_factor = min(1.1, raw_speed_factor * 1.05)
        else:
            effective_speed_factor = raw_speed_factor

        # Strict positive speed clamp avoiding ZeroDivisionError
        speed = max(15.0, raw_avg_speed * effective_speed_factor)
        base_speed = 40.0

        base_eta = (distance / base_speed) * 60.0
        congestion_eta = (distance / speed) * 60.0

        # Alternative route calculations (Expressway bypass vs Surface arterial)
        alt1_dist = round(distance * 1.15, 1)
        alt1_eta = round((alt1_dist / max(10.0, 48.0)) * 60.0, 1)  # Faster bypass
        alt2_dist = round(distance * 0.95, 1)
        alt2_eta = round(congestion_eta * 1.10, 1)                 # Surface arterial

        return {
            "primary_route": f"Express Corridor [{src_zone} to {dst_zone}] via Arterial A1",
            "distance_km": round(distance, 1),
            "base_eta_mins": round(base_eta, 1),
            "congestion_adjusted_eta_mins": round(congestion_eta, 1),
            "congestion_level": traffic_info.get("congestion_level", "MODERATE"),
            "speed_factor": round(effective_speed_factor, 2),
            "alternative_routes": [
                {"name": f"Outer Ring Road Bypass [{src_zone} -> {dst_zone}]", "distance_km": alt1_dist, "eta_mins": alt1_eta},
                {"name": f"City Center Surface Arterial [{src_zone} -> {dst_zone}]", "distance_km": alt2_dist, "eta_mins": alt2_eta}
            ]
        }

