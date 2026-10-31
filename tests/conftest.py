"""Pytest configuration ensuring src package is always importable."""
import sys
from pathlib import Path

# Add project root (containing src) to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
