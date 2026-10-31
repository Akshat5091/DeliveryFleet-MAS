"""Tool 1: Driver Fleet Database Lookup Tool."""
import threading
from typing import List, Dict, Any, Optional
import csv
from pathlib import Path
from ...config import DRIVERS_CSV, MAX_LEGAL_DRIVER_HOURS

DEFAULT_DRIVERS_DATA = [
    {"driver_id": "D01", "name": "Rajesh Sharma", "current_zone": "Zone A", "vehicle_type": "Van", "capacity_kg": 80.0, "status": "AVAILABLE", "current_orders": 0, "hours_worked": 4.5, "rating": 4.9},
    {"driver_id": "D02", "name": "Vikram Singh", "current_zone": "Zone B", "vehicle_type": "Bike", "capacity_kg": 20.0, "status": "AVAILABLE", "current_orders": 1, "hours_worked": 6.0, "rating": 4.7},
    {"driver_id": "D03", "name": "Amit Patel", "current_zone": "Zone C", "vehicle_type": "Van", "capacity_kg": 100.0, "status": "AVAILABLE", "current_orders": 0, "hours_worked": 8.8, "rating": 4.8},
    {"driver_id": "D04", "name": "Suresh Kumar", "current_zone": "Zone A", "vehicle_type": "Electric Van", "capacity_kg": 75.0, "status": "AVAILABLE", "current_orders": 0, "hours_worked": 2.5, "rating": 4.95},
    {"driver_id": "D05", "name": "Manoj Verma", "current_zone": "Zone D", "vehicle_type": "Truck", "capacity_kg": 250.0, "status": "AVAILABLE", "current_orders": 0, "hours_worked": 3.0, "rating": 4.6},
    {"driver_id": "D06", "name": "Pooja Nair", "current_zone": "Zone B", "vehicle_type": "Van", "capacity_kg": 85.0, "status": "BUSY", "current_orders": 2, "hours_worked": 5.5, "rating": 4.85},
    {"driver_id": "D07", "name": "Rohan Das", "current_zone": "Zone C", "vehicle_type": "Electric Scooter", "capacity_kg": 25.0, "status": "AVAILABLE", "current_orders": 0, "hours_worked": 1.5, "rating": 4.75},
    {"driver_id": "D08", "name": "Kavita Rao", "current_zone": "Zone D", "vehicle_type": "Van", "capacity_kg": 90.0, "status": "AVAILABLE", "current_orders": 1, "hours_worked": 7.2, "rating": 4.65},
    {"driver_id": "D09", "name": "Deepak Joshi", "current_zone": "Zone A", "vehicle_type": "Truck", "capacity_kg": 300.0, "status": "OFF_DUTY", "current_orders": 0, "hours_worked": 9.2, "rating": 4.5},
    {"driver_id": "D10", "name": "Sunil Mehra", "current_zone": "Zone B", "vehicle_type": "Electric Van", "capacity_kg": 70.0, "status": "AVAILABLE", "current_orders": 0, "hours_worked": 3.8, "rating": 4.9},
]

class DriverDBTool:
    """Tool for querying available fleet drivers, vehicle capacity, and shift hours with in-memory caching."""
    name: str = "driver_db_lookup"
    description: str = "Query fleet database for active drivers filtered by zone, minimum capacity, and legal shift limits."

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or DRIVERS_CSV
        self._cache: Optional[List[Dict[str, Any]]] = None
        self._lock = threading.RLock()

    def get_all_drivers(self, force_reload: bool = False) -> List[Dict[str, Any]]:
        """Retrieve all driver records from fleet storage with thread-safe caching and fault tolerance."""
        with self._lock:
            if self._cache is not None and not force_reload:
                return [dict(d) for d in self._cache]

            drivers = []
            if self.csv_path and self.csv_path.exists():
                try:
                    with open(self.csv_path, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            try:
                                drivers.append({
                                    "driver_id": row["driver_id"].strip(),
                                    "name": row["name"].strip(),
                                    "current_zone": row["current_zone"].strip(),
                                    "vehicle_type": row["vehicle_type"].strip(),
                                    "capacity_kg": max(0.0, float(row["capacity_kg"])),
                                    "status": row["status"].strip().upper(),
                                    "current_orders": max(0, int(row.get("current_orders", 0))),
                                    "hours_worked": max(0.0, float(row["hours_worked"])),
                                    "rating": max(1.0, min(5.0, float(row.get("rating", 4.5))))
                                })
                            except (ValueError, KeyError):
                                continue
                except Exception:
                    drivers.clear()

            if not drivers:
                drivers = [dict(d) for d in DEFAULT_DRIVERS_DATA]

            self._cache = drivers
            return [dict(d) for d in self._cache]

    def find_eligible_drivers(
        self,
        zone: Optional[str] = None,
        min_capacity_kg: float = 0.0,
        max_shift_hours: float = MAX_LEGAL_DRIVER_HOURS,
        include_busy: bool = False
    ) -> List[Dict[str, Any]]:
        """Filter drivers satisfying physical capacity and legal working hour constraints."""
        all_drivers = self.get_all_drivers()
        safe_min_cap = max(0.0, float(min_capacity_kg or 0.0))
        safe_max_hours = max(0.0, float(max_shift_hours if max_shift_hours is not None else MAX_LEGAL_DRIVER_HOURS))

        eligible = []
        for d in all_drivers:
            if not include_busy and d["status"] != "AVAILABLE":
                continue
            if d["hours_worked"] >= safe_max_hours:
                continue
            if d["capacity_kg"] < safe_min_cap:
                continue
            if zone and d["current_zone"].lower() != zone.lower():
                continue
            eligible.append(d)
        
        # Sort by combination of rating (descending) and current working hours (ascending)
        eligible.sort(key=lambda x: (-x["rating"], x["hours_worked"]))
        return eligible

    def get_driver_by_id(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Lookup single driver record by identifier."""
        if not driver_id:
            return None
        target_id = str(driver_id).strip().upper()
        for d in self.get_all_drivers():
            if d["driver_id"].upper() == target_id:
                return dict(d)
        return None

    def update_driver_status(
        self,
        driver_id: str,
        new_status: str,
        additional_hours: float = 0.0
    ) -> bool:
        """Update driver operational status and shift hours in memory (thread-safe)."""
        with self._lock:
            # Ensure cache is initialized
            if self._cache is None:
                self.get_all_drivers()

            target_id = str(driver_id).strip().upper()
            for d in (self._cache or []):
                if d["driver_id"].upper() == target_id:
                    d["status"] = str(new_status).strip().upper()
                    if additional_hours > 0:
                        d["hours_worked"] = round(d["hours_worked"] + additional_hours, 2)
                    return True
            return False

