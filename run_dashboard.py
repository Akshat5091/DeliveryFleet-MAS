"""Root runner script for DeliveryFleet-MAS Interactive Web Dashboard.
Course: CSE3101 Agentic AI | Group 8 | Eval-2 Working Prototype
"""
import sys
from pathlib import Path
import uvicorn

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

def main():
    print("=" * 80)
    print("[MAS] STARTING DELIVERYFLEET-MAS INTERACTIVE DASHBOARD")
    print("   Course: CSE3101 Agentic AI | Group 8 | Eval-2 Working Prototype")
    print("   Dual-Framework: Google ADK + CrewAI | FastMCP Tools | Blackboard State")
    print("   Host: http://127.0.0.1:8000")
    print("=" * 80)
    uvicorn.run("src.web.app:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    main()
