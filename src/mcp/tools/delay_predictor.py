"""Tool 3: Machine Learning Delivery Delay Forecasting Tool."""
import threading
from typing import Dict, Any, Optional
import csv
import math
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from ...config import DELIVERY_HISTORY_CSV

class DelayPredictorTool:
    """Tool for forecasting transit delay minutes using a trained Random Forest model with robust input sanitization."""
    name: str = "delay_predictor"
    description: str = "Forecasts expected delivery delay in minutes based on distance, traffic congestion, rainfall, and cargo weight."

    def __init__(self, history_csv_path: Optional[Path] = None):
        self.history_csv_path = history_csv_path or DELIVERY_HISTORY_CSV
        self.model: Optional[RandomForestRegressor] = None
        self._lock = threading.Lock()
        self._train_model()

    def _train_model(self) -> None:
        """Train Random Forest regression model on historical records with synthetic baseline fallback."""
        with self._lock:
            X = []
            y = []
            if self.history_csv_path and self.history_csv_path.exists():
                try:
                    with open(self.history_csv_path, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            X.append([
                                float(row["distance_km"]),
                                float(row["traffic_speed_factor"]),
                                float(row["rainfall_mm"]),
                                float(row["hour_of_day"]),
                                float(row["weight_kg"])
                            ])
                            y.append(float(row["delay_minutes"]))
                except Exception:
                    X.clear()
                    y.clear()

            # Fallback baseline synthetic records if CSV is unreadable or absent
            if len(X) < 10:
                rng = np.random.default_rng(42)
                for _ in range(100):
                    dist = rng.uniform(5.0, 30.0)
                    tf = rng.uniform(0.5, 1.0)
                    rain = rng.uniform(0.0, 20.0)
                    hr = rng.integers(8, 22)
                    wt = rng.uniform(5.0, 50.0)
                    delay = max(0.0, (dist * 0.8) + ((1.0 - tf) * 20.0) + (rain * 0.5) + (wt * 0.1))
                    X.append([dist, tf, rain, float(hr), wt])
                    y.append(delay)

            X_arr = np.array(X)
            y_arr = np.array(y)
            self.model = RandomForestRegressor(n_estimators=30, random_state=42, max_depth=6)
            self.model.fit(X_arr, y_arr)

    def predict_delay(
        self,
        distance_km: float,
        traffic_speed_factor: float = 0.80,
        rainfall_mm: float = 0.0,
        hour_of_day: int = 14,
        weight_kg: float = 15.0
    ) -> Dict[str, Any]:
        """Predict expected delay in minutes for candidate delivery with robust boundary clamping."""
        if self.model is None:
            self._train_model()

        # Sanitize and clamp all numeric inputs to realistic bounds
        try:
            d_val = float(distance_km)
            safe_dist = max(0.0, d_val) if math.isfinite(d_val) else 10.0
        except (ValueError, TypeError):
            safe_dist = 10.0

        if safe_dist == 0.0:
            return {
                "predicted_delay_minutes": 0.0,
                "delay_risk_category": "LOW_DELAY_RISK",
                "inputs_evaluated": {
                    "distance_km": 0.0,
                    "traffic_factor": float(traffic_speed_factor or 0.8),
                    "rainfall_mm": float(rainfall_mm or 0.0),
                    "hour": int(hour_of_day or 14),
                    "weight_kg": float(weight_kg or 15.0)
                }
            }

        try:
            t_val = float(traffic_speed_factor)
            safe_traffic = max(0.1, min(2.0, t_val)) if math.isfinite(t_val) else 0.80
        except (ValueError, TypeError):
            safe_traffic = 0.80

        try:
            r_val = float(rainfall_mm)
            safe_rain = max(0.0, min(200.0, r_val)) if math.isfinite(r_val) else 0.0
        except (ValueError, TypeError):
            safe_rain = 0.0

        try:
            h_val = int(hour_of_day)
            safe_hour = max(0, min(23, h_val))
        except (ValueError, TypeError):
            safe_hour = 14

        try:
            w_val = float(weight_kg)
            safe_weight = max(0.1, min(2000.0, w_val)) if math.isfinite(w_val) else 15.0
        except (ValueError, TypeError):
            safe_weight = 15.0

        feat = np.array([[safe_dist, safe_traffic, safe_rain, float(safe_hour), safe_weight]])
        pred = float(self.model.predict(feat)[0])
        pred = max(0.0, round(pred, 1))

        # Risk level categorization
        if pred > 20.0:
            risk = "CRITICAL_DELAY_RISK"
        elif pred > 10.0:
            risk = "MODERATE_DELAY_RISK"
        else:
            risk = "LOW_DELAY_RISK"

        return {
            "predicted_delay_minutes": pred,
            "delay_risk_category": risk,
            "inputs_evaluated": {
                "distance_km": safe_dist,
                "traffic_factor": safe_traffic,
                "rainfall_mm": safe_rain,
                "hour": safe_hour,
                "weight_kg": safe_weight
            }
        }

