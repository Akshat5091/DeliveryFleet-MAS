"""Real-Time Telematics Simulator for Autonomous Multi-Agent Delivery Fleet.
Generates streaming GPS coordinates, heading, speed, and vehicle diagnostics.
"""
import time
import math
import random
from typing import Dict, Any, List
from datetime import datetime, timezone

ZONE_CENTROIDS = {
    "Zone A": {"lat": 28.6139, "lon": 77.2090},
    "Zone B": {"lat": 28.5355, "lon": 77.3910},
    "Zone C": {"lat": 28.4595, "lon": 77.0266},
    "Zone D": {"lat": 28.7041, "lon": 77.1025},
}

class TelematicsSimulator:
    def __init__(self):
        self._vehicles: Dict[str, Dict[str, Any]] = {}
        self._init_vehicles()

    def _init_vehicles(self):
        initial_configs = [
            ("D01", "Rajesh Sharma", "Zone A", "Van (80kg)", 75.0),
            ("D02", "Priya Verma", "Zone B", "Electric Bike (15kg)", 88.0),
            ("D03", "Amit Patel", "Zone A", "Motorcycle (25kg)", 92.0),
            ("D04", "Sunita Rao", "Zone C", "Small Cargo Van (150kg)", 64.0),
            ("D05", "Vikram Singh", "Zone B", "Medium Cargo Van (200kg)", 53.0),
            ("D06", "Ananya Deshmukh", "Zone A", "Electric Scooter (15kg)", 95.0),
            ("D07", "Rohan Mehta", "Zone D", "Van (80kg)", 70.0),
            ("D08", "Neha Gupta", "Zone B", "Motorcycle (25kg)", 82.0),
            ("D09", "Deepak Joshi", "Zone A", "Heavy Freight Truck (300kg)", 41.0),
            ("D10", "Kavita Reddy", "Zone C", "Electric Van (100kg)", 80.0),
        ]

        for vid, name, zone, vtype, battery in initial_configs:
            centroid = ZONE_CENTROIDS.get(zone, ZONE_CENTROIDS["Zone A"])
            offset_lat = (random.random() - 0.5) * 0.04
            offset_lon = (random.random() - 0.5) * 0.04
            self._vehicles[vid] = {
                "driver_id": vid,
                "driver_name": name,
                "zone": zone,
                "vehicle_type": vtype,
                "lat": round(centroid["lat"] + offset_lat, 5),
                "lon": round(centroid["lon"] + offset_lon, 5),
                "speed_kmh": round(random.uniform(20.0, 48.0), 1),
                "heading_deg": random.randint(0, 359),
                "battery_fuel_pct": battery,
                "status": "EN_ROUTE" if vid != "D09" else "SHIFT_LIMIT_BLOCKED",
                "assigned_order": f"ORD-{random.randint(100, 199)}" if vid != "D09" else None,
                "odometer_km": round(random.uniform(120.0, 450.0), 1),
                "last_update_utc": datetime.now(timezone.utc).isoformat()
            }

    def tick(self) -> List[Dict[str, Any]]:
        """Advance simulation tick by moving each active vehicle along its heading."""
        now_iso = datetime.now(timezone.utc).isoformat()
        results = []

        for vid, v in self._vehicles.items():
            if v["status"] == "SHIFT_LIMIT_BLOCKED":
                v["speed_kmh"] = 0.0
                v["last_update_utc"] = now_iso
                results.append(dict(v))
                continue

            # Move slightly along heading
            heading_rad = math.radians(v["heading_deg"])
            step_km = (v["speed_kmh"] * 1.5) / 3600.0  # 1.5 sec movement
            delta_lat = (step_km / 111.0) * math.cos(heading_rad)
            delta_lon = (step_km / (111.0 * math.cos(math.radians(v["lat"])))) * math.sin(heading_rad)

            v["lat"] = round(v["lat"] + delta_lat, 5)
            v["lon"] = round(v["lon"] + delta_lon, 5)
            v["odometer_km"] = round(v["odometer_km"] + step_km, 2)
            v["battery_fuel_pct"] = max(5.0, round(v["battery_fuel_pct"] - 0.02, 1))

            # Introduce small heading drift
            v["heading_deg"] = (v["heading_deg"] + random.randint(-8, 8)) % 360
            v["speed_kmh"] = round(max(15.0, min(60.0, v["speed_kmh"] + random.uniform(-2.5, 2.5))), 1)
            v["last_update_utc"] = now_iso
            results.append(dict(v))

        return results

    def get_snapshot(self) -> List[Dict[str, Any]]:
        return list(self._vehicles.values())

