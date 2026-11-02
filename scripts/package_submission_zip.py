"""Utility script to build the clean submission archive DeliveryFleet_MAS_Group8_Eval2.zip.
Excludes .git, __pycache__, .venv, node_modules, and cache files.
"""
import zipfile
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
PARENT_DIR = REPO_DIR.parent
ZIP_OUT = PARENT_DIR / "DeliveryFleet_MAS_Group8_Eval2.zip"

EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache", ".mypy_cache"}
EXCLUDE_EXTS = {".pyc", ".pyo"}

def package_zip():
    print(f"Creating submission zip: {ZIP_OUT}")
    count = 0
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in REPO_DIR.rglob("*"):
            if any(part in EXCLUDE_DIRS for part in f.parts):
                continue
            if f.suffix in EXCLUDE_EXTS or f.name.startswith("~$"):
                continue
            if f.is_file():
                arcname = f.relative_to(PARENT_DIR)
                z.write(f, arcname)
                count += 1
    size_mb = round(ZIP_OUT.stat().st_size / (1024 * 1024), 2)
    print(f"[OK] Packaged {count} files into {ZIP_OUT} ({size_mb} MB)")

if __name__ == "__main__":
    package_zip()

