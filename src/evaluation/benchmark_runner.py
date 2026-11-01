"""Automated Benchmark Runner executing 72 Multi-Factor Agentic Evaluations.
Course: CSE3101 Agentic AI | Group 8 | Multi-Agent Delivery Fleet
Factorial Matrix: 3 Architectures x 2 Prompt Styles x 4 Personas x 3 Consignments = 72 Runs.
"""
import sys
import time
import csv
import json
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
from typing import List, Dict, Any, Optional
from pathlib import Path
from ..config import ARTIFACTS_DIR, ORDERS_CSV
from ..orchestration.hierarchical_orchestrator import HierarchicalOrchestrator
from ..orchestration.parallel_orchestrator import ParallelOrchestrator
from ..orchestration.sequential_orchestrator import SequentialOrchestrator
from .personas import get_persona_prompt
from ..observability.run_logger import RunLogger

class BenchmarkRunner:
    """Executes systematic multi-agent benchmark matrix across architectures, prompt styles, and personas."""

    def __init__(self):
        self.hierarchical_orch = HierarchicalOrchestrator()
        self.parallel_orch = ParallelOrchestrator()
        self.sequential_orch = SequentialOrchestrator()
        self.logger = RunLogger.get_logger()
        self.results: List[Dict[str, Any]] = []

    def _load_sample_orders(self) -> List[Dict[str, Any]]:
        """Load subset of 3 distinct orders representing standard, heavy freight, and critical medical consignments."""
        orders = []
        with open(ORDERS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["order_id"] in ["ORD-101", "ORD-103", "ORD-105"]:
                    orders.append(row)
        return orders

    def run_full_suite(self) -> List[Dict[str, Any]]:
        """Execute full 72-run benchmark suite (3 architectures x 2 prompt styles x 4 personas x 3 orders)."""
        orders = self._load_sample_orders()
        architectures = ["Hierarchical", "Parallel", "Sequential"]
        prompt_styles = ["ReAct", "Direct"]
        personas = ["polite", "urgent", "abusive", "injection"]

        run_count = 0
        self.results = []
        print(f"🏁 Starting MAS Multi-Factor Evaluation Suite (Target: 72 runs across 3 architectures)...")

        for arch in architectures:
            for style in prompt_styles:
                for persona in personas:
                    for base_order in orders:
                        run_count += 1
                        run_id = f"RUN-{run_count:03d}"

                        # Prepare order instance with persona-varied notes
                        test_order = dict(base_order)
                        test_order["persona"] = persona
                        test_order["notes"] = get_persona_prompt(persona, base_order.get("notes", "Standard dispatch"))

                        # Execute on selected architecture
                        if arch == "Hierarchical":
                            report = self.hierarchical_orch.process_order(
                                order=test_order,
                                prompt_style=style,
                                simulate_exception=(base_order["order_id"] == "ORD-105"),
                                run_id=run_id
                            )
                        elif arch == "Parallel":
                            report = self.parallel_orch.process_order(
                                order=test_order,
                                prompt_style=style,
                                simulate_exception=(base_order["order_id"] == "ORD-105"),
                                run_id=run_id
                            )
                        else:
                            report = self.sequential_orch.process_order(
                                order=test_order,
                                prompt_style=style,
                                run_id=run_id
                            )

                        result_record = {
                            "run_id": run_id,
                            "architecture": arch,
                            "prompt_style": style,
                            "persona": persona,
                            "order_id": test_order["order_id"],
                            "priority": test_order["priority"],
                            "outcome": report.delivery_outcome,
                            "input_guard_status": report.input_guard_status,
                            "assigned_driver": report.assigned_driver_id,
                            "latency_sec": report.total_execution_latency_sec,
                            "tokens": report.total_tokens_consumed,
                            "cost_usd": report.estimated_cost_usd,
                            "guardrail_passed": report.guardrail_summary.passed,
                            "interventions": report.guardrail_summary.interventions
                        }
                        self.results.append(result_record)
                        print(f"  [{run_id}] Arch: {arch:12} | Style: {style:6} | Persona: {persona:9} | "
                              f"Outcome: {report.delivery_outcome:18} | Latency: {report.total_execution_latency_sec:.3f}s")

        # Save results to disk
        self._save_results()
        print(f"✅ Successfully completed and logged all {len(self.results)} benchmark runs.")

        # Compute and persist academic course evaluation metrics (Sensitivity, Specificity, Entropy, Accuracy)
        try:
            from .agent_evaluator import AgentEvaluator
            evaluator = AgentEvaluator()
            metrics = evaluator.evaluate_batch(self.results)
            evaluator.save_metrics_summary(metrics)
            print("📈 Academic course evaluation metrics computed and saved to artifacts/evaluation_metrics.json.")
        except Exception as e:
            print(f"⚠️ Warning: Could not compute course evaluation metrics: {e}")

        return self.results

    def _save_results(self) -> None:
        """Persist structured benchmark runs to JSON artifact."""
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        out_path = ARTIFACTS_DIR / "benchmark_results.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run_full_suite()
