"""Tests for Academic Evaluation Metrics (Course Rubric: Sensitivity, Specificity, Entropy, Y in R^4) and System Fault Resilience."""
import pytest
import math
from src.evaluation.agent_evaluator import AgentEvaluator, RunEvaluationMetric
from src.evaluation.visualizer import MASVisualizer
from src.agents.a2a_bridge import A2ABridge
from src.schemas.a2a import A2ARequest
from src.agents.crew_dispatch_agent import CrewDispatchAgent
from src.schemas.blackboard import CandidateDriver
from src.orchestration.hierarchical_orchestrator import HierarchicalOrchestrator
from src.orchestration.sequential_orchestrator import SequentialOrchestrator
from pathlib import Path

def test_shannon_entropy_calculation():
    """Verify Shannon Entropy H(X) calculation matches mathematical information theory."""
    evaluator = AgentEvaluator()

    # Case 1: Monopolistic distribution (Single driver takes all jobs) -> Entropy = 0.0 bits
    single_driver = {"D01": 50}
    assert evaluator.compute_shannon_entropy(single_driver) == 0.0

    # Case 2: Uniform distribution across 2 drivers -> Entropy = 1.0 bit (-2 * 0.5 * log2(0.5) = 1.0)
    uniform_two = {"D01": 25, "D02": 25}
    assert evaluator.compute_shannon_entropy(uniform_two) == 1.0

    # Case 3: Uniform distribution across 4 drivers -> Entropy = 2.0 bits (-4 * 0.25 * log2(0.25) = 2.0)
    uniform_four = {"D01": 10, "D02": 10, "D03": 10, "D04": 10}
    assert evaluator.compute_shannon_entropy(uniform_four) == 2.0

def test_query_sensitivity_and_specificity_metrics():
    """Verify Query Sensitivity (Recall) and Specificity (TNR) on clean vs adversarial prompts."""
    evaluator = AgentEvaluator()

    # Adversarial Injection run -> should yield sensitivity 1.0 when blocked
    attack_run = {
        "run_id": "TEST-ATTACK",
        "persona": "injection",
        "outcome": "BLOCKED_BY_GUARDRAIL",
        "input_guard_status": "BLOCKED_INJECTION",
        "assigned_driver": "NONE",
        "guardrail_passed": False
    }
    metric_attack = evaluator.evaluate_run(attack_run)
    assert metric_attack.query_sensitivity == 1.0

    # Clean polite run -> should yield specificity 1.0 when allowed
    clean_run = {
        "run_id": "TEST-CLEAN",
        "persona": "polite",
        "outcome": "SUCCESS",
        "input_guard_status": "CLEAN",
        "assigned_driver": "D04",
        "guardrail_passed": True
    }
    metric_clean = evaluator.evaluate_run(clean_run)
    assert metric_clean.query_specificity == 1.0
    assert metric_clean.agent_accuracy_score >= 0.95

def test_a2a_bridge_thread_safety_and_history():
    """Verify thread-safe message recording, retrieval, and clearance in A2ABridge."""
    bridge = A2ABridge()
    bridge.clear_history()
    assert len(bridge.get_message_history()) == 0

    req = A2ARequest(
        order_id="TEST-A2A-01",
        driver_id="D04",
        pickup_zone="Zone A",
        dropoff_zone="Zone B",
        priority="NORMAL"
    )
    resp = bridge.send_routing_request(
        from_agent="crew_dispatch_agent",
        task_id="task-01",
        request=req,
        run_id="TEST-RUN"
    )
    assert resp.status == "SUCCESS"
    history = bridge.get_message_history()
    assert len(history) == 2  # Request + Response
    assert history[0].message_type == "request"
    assert history[1].message_type == "response"

    bridge.clear_history()
    assert len(bridge.get_message_history()) == 0

def test_proximity_aware_dispatching():
    """Verify that co-located driver in pickup zone is preferred over distant driver."""
    agent = CrewDispatchAgent()
    drivers = [
        CandidateDriver(
            driver_id="D-DISTANT",
            name="Distant Driver",
            current_zone="Zone C",  # 18km away from Zone A
            vehicle_type="Van",
            capacity_kg=50.0,
            hours_worked=1.0,
            rating=4.8,
            status="AVAILABLE"
        ),
        CandidateDriver(
            driver_id="D-COLOCATED",
            name="Co-located Driver",
            current_zone="Zone A",  # In same zone as pickup
            vehicle_type="Van",
            capacity_kg=50.0,
            hours_worked=2.5,
            rating=4.9,
            status="AVAILABLE"
        )
    ]
    dec = agent.decide_assignment(
        order_id="TEST-PROX-01",
        pickup="Zone A - Warehouse",
        dropoff="Zone B - Tech Park",
        weight_kg=15.0,
        priority="NORMAL",
        deadline_mins=40,
        candidate_drivers=drivers,
        prompt_style="ReAct"
    )
    # Co-located driver should be picked because 18km approach transit adds ~30min penalty
    assert dec.assigned_driver_id == "D-COLOCATED"
    assert "co-located in Zone A" in dec.rationale

def test_orchestrator_system_fault_tolerance(monkeypatch):
    """Verify that catastrophic exceptions in agent reasoning are gracefully intercepted."""
    orch = HierarchicalOrchestrator()
    
    # Simulate unexpected failure in driver lookup
    def faulty_find(*args, **kwargs):
        raise RuntimeError("Simulated Database Socket Disconnection")

    monkeypatch.setattr(orch.driver_db, "find_eligible_drivers", faulty_find)

    sample_order = {
        "order_id": "TEST-FAULT-101",
        "pickup": "Zone A - Hub",
        "dropoff": "Zone B - Client",
        "weight_kg": 10.0,
        "priority": "NORMAL",
        "deadline_mins": 30,
        "persona": "polite",
        "notes": "Handle with care"
    }

    report = orch.process_order(sample_order, run_id="TEST-FAULT-RUN")
    assert report.delivery_outcome == "SYSTEM_FAULT_RECOVERED"
    assert not report.guardrail_summary.passed
    assert "Simulated Database Socket Disconnection" in report.guardrail_summary.violations[0]

def test_evaluation_metrics_heatmap_generation(tmp_path):
    """Verify that evaluation_metrics_heatmap is generated cleanly on disk."""
    vis = MASVisualizer(artifacts_dir=tmp_path)
    sample_runs = [
        {"run_id": f"RUN-{i:03d}", "persona": "polite" if i % 4 != 0 else "injection",
         "outcome": "SUCCESS" if i % 4 != 0 else "BLOCKED_BY_GUARDRAIL",
         "input_guard_status": "CLEAN" if i % 4 != 0 else "BLOCKED_INJECTION",
         "assigned_driver": f"D0{(i % 5) + 1}", "guardrail_passed": (i % 4 != 0)}
        for i in range(1, 25)
    ]
    chart_path = vis.plot_evaluation_metrics_heatmap(records=sample_runs)
    assert Path(chart_path).exists()
    assert Path(chart_path).stat().st_size > 10000
