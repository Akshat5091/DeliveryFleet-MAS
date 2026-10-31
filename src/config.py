"""Central Configuration and Path Management for Multi-Agent Delivery Fleet Coordination System."""
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
KB_DIR = DATA_DIR / "knowledge_base"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
RUN_LOGS_DIR = PROJECT_ROOT / "logs"

ORDERS_CSV = DATA_DIR / "orders.csv"
DRIVERS_CSV = DATA_DIR / "drivers.csv"
TRAFFIC_CSV = DATA_DIR / "traffic.csv"
WEATHER_CSV = DATA_DIR / "weather.csv"
DELIVERY_HISTORY_CSV = DATA_DIR / "delivery_history.csv"
CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"

# Model and Token Cost Constants (Gemini Flash 2.5 baseline)
# Pricing per million tokens: $0.075 input / $0.30 output
COST_PER_INPUT_TOKEN = 0.075 / 1_000_000
COST_PER_OUTPUT_TOKEN = 0.30 / 1_000_000

# Safety and Business Thresholds
MAX_LEGAL_DRIVER_HOURS = 9.0
NEAR_FATIGUE_THRESHOLD_HOURS = 8.5
MAX_CRITICAL_ETA_MINUTES = 30
ZONE_B_HEAVY_FREIGHT_LIMIT_KG = 50.0

# Ensure directories exist
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
RUN_LOGS_DIR.mkdir(parents=True, exist_ok=True)
