"""Tests for Blackboard concurrency, thread-safety, snapshot isolation, and atomic state transactions."""
import pytest
import threading
import time
from src.orchestration.blackboard_manager import BlackboardManager
from src.mcp.tools.blackboard_tool import BlackboardTool
from src.schemas.blackboard import BlackboardState
from src.observability.run_logger import RunLogger
from src.observability.tracing import MASTracer

def test_blackboard_manager_concurrent_writes():
    """Verify that multiple threads concurrently updating distinct fields do not corrupt state or drop audit provenance."""
    bm = BlackboardManager()
    state = bm.initialize_order_state(
        order_id="CONCUR-01",
        pickup="Zone A",
        dropoff="Zone B",
        weight_kg=12.0,
        priority="HIGH",
        deadline_mins=45
    )

    num_threads = 10
    updates_per_thread = 5

    def worker(worker_id: int):
        for i in range(updates_per_thread):
            bm.update_field(
                order_id="CONCUR-01",
                agent_name=f"Worker-{worker_id}",
                field_name="traffic_factor",
                value=round(1.0 + (worker_id * 0.05), 2),
                description=f"Update iteration {i} from worker {worker_id}"
            )
            time.sleep(0.001)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    final_state = bm.get_state("CONCUR-01")
    assert final_state is not None
    # 1 initialization entry + (10 threads * 5 updates) = 51 provenance log entries
    assert len(final_state.provenance_log) == 1 + (num_threads * updates_per_thread)

def test_blackboard_manager_snapshot_isolation():
    """Verify that taking a snapshot returns an isolated deep copy immune to subsequent mutations."""
    bm = BlackboardManager()
    bm.initialize_order_state(
        order_id="SNAP-01",
        pickup="Zone A",
        dropoff="Zone B",
        weight_kg=10.0,
        priority="NORMAL",
        deadline_mins=60
    )

    bm.update_field("SNAP-01", "DispatchAgent", "assigned_driver_id", "D01", "Initial assignment")
    snapshot = bm.get_state_snapshot("SNAP-01")
    assert snapshot is not None
    assert snapshot.assigned_driver_id == "D01"

    # Subsequent mutation on live state
    bm.update_field("SNAP-01", "ExceptionAgent", "assigned_driver_id", "D04", "Reassignment")
    live_state = bm.get_state("SNAP-01")

    assert live_state.assigned_driver_id == "D04"
    assert snapshot.assigned_driver_id == "D01"  # Snapshot remains unchanged
    assert len(snapshot.provenance_log) < len(live_state.provenance_log)

def test_blackboard_manager_batch_update():
    """Verify atomic transaction applying multiple updates in a single lock acquisition."""
    bm = BlackboardManager()
    bm.initialize_order_state(
        order_id="BATCH-01",
        pickup="Zone C",
        dropoff="Zone D",
        weight_kg=25.0,
        priority="CRITICAL",
        deadline_mins=30
    )

    batch = [
        ("assigned_driver_id", "D05", "Assigned truck D05"),
        ("selected_route", "Corridor C-D Bypass", "Selected fastest highway"),
        ("estimated_eta_mins", 22.5, "Calculated bypass ETA"),
        ("guardrail_passed", True, "Passed legal checks")
    ]
    bm.batch_update_fields("BATCH-01", "BatchAgent", batch)

    state = bm.get_state("BATCH-01")
    assert state.assigned_driver_id == "D05"
    assert state.selected_route == "Corridor C-D Bypass"
    assert state.estimated_eta_mins == 22.5
    assert state.guardrail_passed is True
    assert len(state.provenance_log) == 5  # 1 init + 4 batch

def test_blackboard_manager_lifecycle():
    """Verify listing active orders, deleting, and clearing states."""
    bm = BlackboardManager()
    bm.initialize_order_state("ORD-A", "Zone A", "Zone B", 5.0, "NORMAL", 40)
    bm.initialize_order_state("ORD-B", "Zone B", "Zone C", 15.0, "HIGH", 30)

    orders = bm.list_active_orders()
    assert "ORD-A" in orders
    assert "ORD-B" in orders
    assert len(orders) == 2

    deleted = bm.delete_order_state("ORD-A")
    assert deleted is True
    assert bm.get_state("ORD-A") is None
    assert len(bm.list_active_orders()) == 1

    bm.clear_all()
    assert len(bm.list_active_orders()) == 0

def test_blackboard_tool_thread_safety():
    """Verify BlackboardTool concurrent read and write operations."""
    state = BlackboardState(
        order_id="TOOL-CONCUR-01",
        pickup="Zone A",
        dropoff="Zone B",
        weight_kg=8.0,
        priority="NORMAL",
        deadline_mins=50
    )
    store = {"TOOL-CONCUR-01": state}
    tool = BlackboardTool(state_store=store)

    errors = []
    def writer():
        for i in range(10):
            try:
                res = tool.post_update(
                    order_id="TOOL-CONCUR-01",
                    agent_name="ConcurrentAgent",
                    field_name="distance_km",
                    value=float(10.0 + i),
                    description=f"Step {i}"
                )
                if res["status"] != "SUCCESS":
                    errors.append(res)
            except Exception as e:
                errors.append(str(e))

    def reader():
        for _ in range(10):
            try:
                data = tool.get_state("TOOL-CONCUR-01")
                if data is None or data["order_id"] != "TOOL-CONCUR-01":
                    errors.append("Invalid read")
            except Exception as e:
                errors.append(str(e))

    t1 = threading.Thread(target=writer)
    t2 = threading.Thread(target=reader)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert len(errors) == 0
    assert len(state.provenance_log) == 10

def test_tracer_and_logger_concurrency():
    """Verify MASTracer and RunLogger survive concurrent multi-agent event dispatch."""
    tracer = MASTracer()
    logger = RunLogger.get_logger()

    def worker(worker_id: int):
        trace_id = f"trace-{worker_id}"
        tracer.start_trace(trace_id)
        span = tracer.start_span(trace_id, f"Span-{worker_id}", f"Agent-{worker_id}")
        time.sleep(0.002)
        tracer.end_span(span, status="OK")
        logger.log_event(
            run_id=f"RUN-{worker_id}",
            order_id=f"ORD-{worker_id}",
            agent_name=f"Agent-{worker_id}",
            framework="TestFramework",
            event_type="TEST_EVENT",
            start_time=time.time() - 0.01,
            end_time=time.time(),
            input_tokens=50,
            output_tokens=25,
            status="SUCCESS"
        )

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for i in range(8):
        summary = tracer.get_trace_summary(f"trace-{i}")
        assert len(summary) == 1
        assert summary[0]["status"] == "OK"
