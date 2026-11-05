"""Master Build Script: Re-generates all formal evaluation documents for Eval-2.
Runs:
1. scripts/create_formal_docs.py (Updated Problem Statement & Updated Project Plan docx)
2. scripts/update_formal_wip_report.py (Enhanced Work In Progress Report docx with 10 figures)
3. scripts/sync_markdown_report.py (Synchronizes EVAL2_WORK_IN_PROGRESS_REPORT.md)
4. scripts/create_pptx_slide.py (1-Slide Coverage Matrix Presentation & Markdown)
"""
import sys
import subprocess
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

SCRIPTS_DIR = Path(__file__).resolve().parent

def run_step(script_name: str):
    script_path = SCRIPTS_DIR / script_name
    print(f"\n[RUNNING] {script_name} ...")
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, encoding='utf-8')
    if res.returncode == 0:
        print(f"[OK] {script_name} completed successfully.")
        if res.stdout.strip():
            print("     " + res.stdout.strip().replace("\n", "\n     "))
    else:
        print(f"[FAIL] {script_name} failed with code {res.returncode}")
        print("STDERR: " + res.stderr)
        sys.exit(res.returncode)

def main():
    print("=" * 80)
    print("[BUILD] BUILDING ALL EVALUATION PHASE 2 DELIVERABLES")
    print("   Target Directory: DeliveryFleet-MAS/Eval 2 Documents")
    print("=" * 80)
    
    run_step("create_formal_docs.py")
    run_step("update_formal_wip_report.py")
    run_step("sync_markdown_report.py")
    run_step("create_pptx_slide.py")
    run_step("build_human_master_presentation.py")
    run_step("package_submission_zip.py")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] ALL EVAL-2 DELIVERABLES GENERATED & SYNCHRONIZED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    main()
