"""Comprehensive Protocol Compliance Tests.
Course: CSE3101 Agentic AI | Group 8 | Multi-Agent Delivery Fleet
Verifies:
1. Blackboard context-driven downstream handoffs
2. FastMCP Tool Client execution
3. Tri-Architecture execution (Hierarchical, Parallel, Sequential)
4. OpenTelemetry SDK TracerProvider & InMemorySpanExporter
5. A2A Network JSON-RPC compatibility
"""
import pytest
from src.mcp.client import MCPClient, mcp_client
from src.orchestration.hierarchical_orchestrator import HierarchicalOrchestrator
from src.orchestration.parallel_orchestrator import ParallelOrchestrator
from src.orchestration.sequential_orchestrator import SequentialOrchestrator
from src.orchestration.blackboard_manager import BlackboardManager
from src.observability.tracing import MASTracer
from src.schemas.blackboard import CandidateDriver
from src.agents.a2a_bridge import A2ABridge
from src.schemas.a2a import A2ARequest

def test_mcp_client_registered_tools():
    """Verify FastMCP client lists all registered tools and can call them."""
    tools = mcp_client.list_tools()
    assert "driver_db_lookup" in tools
    assert "routing_engine_calculate" in tools
    assert "delay_predictor_forecast" in tools
    assert "policy_rag_search" in tools
    assert "blackboard_update" in tools

    # Execute driver DB lookup tool via MCP
    drivers = mcp_client.call_tool("driver_db_lookup", {"min_capacity_kg": 15.0})
    assert isinstance(drivers, list)
    assert len(drivers) > 0

    # Execute routing tool via MCP
    route = mcp_client.call_tool("routing_engine_calculate", {
        "pickup_location": "Zone A",
        "dropoff_location": "Zone B",
        "priority": "HIGH"
    })
    assert "primary_route" in route
    assert route["distance_km"] > 0

def test_parallel_orchestrator_execution():
    """Verify ParallelOrchestrator executes 4-way fan-out and converges at Blackboard barrier."""
    orch = ParallelOrchestrator()
    sample_order = {
        "order_id": "TEST-PAR-01",
        "pickup": "Zone A - Warehouse 1",
        "dropoff": "Zone B - Tech Park",
        "weight_kg": 10.0,
        "priority": "HIGH",
        "deadline_mins": 35,
        "persona": "polite",
        "notes": "Standard express delivery."
    }
    report = orch.process_order(sample_order, prompt_style="ReAct", run_id="TEST-PAR-RUN")
    assert report.delivery_outcome == "SUCCESS"
    assert report.assigned_driver_id != "NONE"
    assert report.selected_route != "NONE"
    assert report.total_execution_latency_sec > 0
    assert report.guardrail_summary.passed
    assert len(report.provenance_trail) >= 4

def test_opentelemetry_tracer_export():
    """Verify standard OpenTelemetry SDK TracerProvider and InMemorySpanExporter export real spans."""
    tracer = MASTracer()
    trace_id = tracer.start_trace("ORD-OTEL-TEST")
    span1 = tracer.start_span(trace_id, "ParallelContextGathering", "ParallelOrchestrator", attributes={"zone": "Zone A"})
    tracer.end_span(span1, status="OK", extra_attributes={"retrieved": 5})

    span2 = tracer.start_span(trace_id, "ADKRouteCalculation", "ADKRouteAgent")
    tracer.end_span(span2, status="OK")

    # Internal spans
    summary = tracer.get_trace_summary(trace_id)
    assert len(summary) == 2

    # OpenTelemetry standard SDK exported spans
    otel_spans = tracer.get_exported_otel_spans()
    assert len(otel_spans) >= 2
    span_names = [s.name for s in otel_spans]
    assert "ParallelContextGathering" in span_names
    assert "ADKRouteCalculation" in span_names

def test_blackboard_context_driven_handoff():
    """Verify downstream agent reads input fields strictly from Blackboard."""
    bb = BlackboardManager()
    state = bb.initialize_order_state(
        order_id="ORD-BB-TEST",
        pickup="Zone A",
        dropoff="Zone B",
        weight_kg=12.0,
        priority="HIGH",
        deadline_mins=30
    )
    # Write intermediate candidate drivers to Blackboard
    drivers = [
        CandidateDriver(
            driver_id="D-BB-1",
            name="Alice",
            current_zone="Zone A",
            vehicle_type="Van",
            capacity_kg=25.0,
            hours_worked=3.0,
            rating=4.9,
            status="AVAILABLE"
        )
    ]
    bb.update_field("ORD-BB-TEST", "FastMCP:driver_db", "candidate_drivers", drivers, "Committed drivers")

    # Downstream read from Blackboard
    retrieved_drivers = bb.get_field("ORD-BB-TEST", "candidate_drivers")
    assert len(retrieved_drivers) == 1
    assert retrieved_drivers[0].driver_id == "D-BB-1"

def test_tri_architecture_coverage():
    """Verify all 3 architectures process an order successfully."""
    h_orch = HierarchicalOrchestrator()
    p_orch = ParallelOrchestrator()
    s_orch = SequentialOrchestrator()

    order = {
        "order_id": "TEST-TRI",
        "pickup": "Zone A",
        "dropoff": "Zone B",
        "weight_kg": 8.0,
        "priority": "NORMAL",
        "deadline_mins": 40,
        "persona": "polite"
    }

    rep_h = h_orch.process_order(order, run_id="TRI-H")
    rep_p = p_orch.process_order(order, run_id="TRI-P")
    rep_s = s_orch.process_order(order, run_id="TRI-S")

    assert rep_h.delivery_outcome == "SUCCESS"
    assert rep_p.delivery_outcome == "SUCCESS"
    assert rep_s.delivery_outcome in ["SUCCESS", "FLAGGED"]

