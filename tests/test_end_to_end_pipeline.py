"""End-to-End integration tests for Hierarchical and Sequential Orchestrators."""
import pytest
from src.orchestration.hierarchical_orchestrator import HierarchicalOrchestrator
from src.orchestration.sequential_orchestrator import SequentialOrchestrator

@pytest.fixture
def sample_normal_order():
    return {
        "order_id": "TEST-101",
        "pickup": "Zone A - Warehouse 1",
        "dropoff": "Zone B - Tech Park",
        "weight_kg": 15.0,
        "priority": "HIGH",
        "deadline_mins": 45,
        "persona": "polite",
        "notes": "Please deliver to building reception."
    }

@pytest.fixture
def sample_disrupted_order():
    return {
        "order_id": "TEST-105",
        "pickup": "Zone B - Medical Supply",
        "dropoff": "Zone A - City Hospital",
        "weight_kg": 12.0,
        "priority": "CRITICAL",
        "deadline_mins": 25,
        "persona": "urgent",
        "notes": "Emergency blood transfusion kit."
    }

def test_hierarchical_orchestrator_success(sample_normal_order):
    orch = HierarchicalOrchestrator()
    report = orch.process_order(sample_normal_order, prompt_style="ReAct", run_id="TEST-RUN-01")
    assert report.order_id == "TEST-101"
    assert report.delivery_outcome == "SUCCESS"
    assert report.assigned_driver_id != "NONE"
    assert report.final_eta_mins > 0
    assert report.guardrail_summary.passed
    assert len(report.provenance_trail) >= 4

    # Verify Markdown table output
    table_str = report.to_markdown_table()
    assert "| **Order ID** | `TEST-101` |" in table_str
    assert "| **Delivery Outcome** | **`SUCCESS`** |" in table_str

def test_hierarchical_orchestrator_exception_recovery(sample_disrupted_order):
    orch = HierarchicalOrchestrator()
    report = orch.process_order(sample_disrupted_order, prompt_style="ReAct", simulate_exception=True, run_id="TEST-RUN-02")
    assert report.delivery_outcome == "RECOVERED_VIA_EXCEPTION"
    assert report.exception_details is not None
    assert report.exception_details.recovery_action == "REASSIGN_DRIVER"
    assert report.exception_details.time_saved_mins > 0

def test_sequential_orchestrator_success(sample_normal_order):
    orch = SequentialOrchestrator()
    report = orch.process_order(sample_normal_order, prompt_style="Direct", run_id="TEST-RUN-03")
    assert report.delivery_outcome in ["SUCCESS", "FLAGGED"]
    assert report.assigned_driver_id != "NONE"
    assert report.distance_km > 0

def test_unassigned_impossible_weight():
    """Verify that orders exceeding vehicle payload capacity fail gracefully with guardrail block."""
    orch = HierarchicalOrchestrator()
    heavy_order = {
        "order_id": "TEST-HEAVY",
        "pickup": "Zone A - Warehouse 1",
        "dropoff": "Zone B - Tech Park",
        "weight_kg": 99999.0,
        "priority": "NORMAL",
        "deadline_mins": 60,
        "persona": "polite",
        "notes": "Massive industrial equipment"
    }
    report = orch.process_order(heavy_order, run_id="TEST-RUN-HEAVY")
    assert report.delivery_outcome == "UNASSIGNED_NO_ELIGIBLE_DRIVER"
    assert report.assigned_driver_id == "NONE"
    assert not report.guardrail_summary.passed
    assert report.guardrail_summary.action_taken == "BLOCK"

def test_exception_agent_cascading_fatigue_escalation():
    """Verify that when primary and all backup drivers exceed 9.0h fatigue limit, system escalates."""
    from src.agents.crew_exception_agent import CrewExceptionAgent
    from src.schemas.blackboard import CandidateDriver
    
    agent = CrewExceptionAgent()
    drivers = [
        CandidateDriver(driver_id="D01", name="Driver 1", current_zone="Zone A", vehicle_type="Van", capacity_kg=50.0, hours_worked=9.5, rating=4.5, status="AVAILABLE"),
        CandidateDriver(driver_id="D02", name="Driver 2", current_zone="Zone B", vehicle_type="Van", capacity_kg=50.0, hours_worked=9.2, rating=4.8, status="AVAILABLE")
    ]
    replan = agent.recover_disruption(
        order_id="TEST-DISRUPT",
        original_driver_id="D01",
        disruption_cause="VEHICLE_BREAKDOWN",
        pickup_zone="Zone A",
        dropoff_zone="Zone B",
        deadline_mins=30,
        backup_drivers=drivers,
        run_id="TEST-RUN-FATIGUE"
    )
    assert replan.recovery_action == "ESCALATE_DISPATCH_SUPERVISOR"
    assert replan.reassigned_driver_id == "NONE_ESCALATED"
    assert "CRITICAL SAFETY ESCALATION" in replan.rationale

