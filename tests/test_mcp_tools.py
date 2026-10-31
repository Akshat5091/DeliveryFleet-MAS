"""Unit tests for the 5 Model Context Protocol (MCP) Tools."""
import pytest
from src.mcp.tools.driver_db import DriverDBTool
from src.mcp.tools.routing_engine import RoutingEngineTool
from src.mcp.tools.delay_predictor import DelayPredictorTool
from src.mcp.tools.chroma_rag import ChromaRAGTool
from src.mcp.tools.blackboard_tool import BlackboardTool
from src.schemas.blackboard import BlackboardState

def test_driver_db_filtering():
    tool = DriverDBTool()
    drivers = tool.get_all_drivers()
    assert len(drivers) >= 10

    # Filter by capacity and hours
    eligible = tool.find_eligible_drivers(min_capacity_kg=30.0, max_shift_hours=9.0)
    for d in eligible:
        assert d["capacity_kg"] >= 30.0
        assert d["hours_worked"] < 9.0
        assert d["status"] == "AVAILABLE"

def test_routing_engine():
    tool = RoutingEngineTool()
    res = tool.calculate_route("Zone A - Warehouse 1", "Zone B - Tech Park")
    assert "Express Corridor" in res["primary_route"]
    assert res["distance_km"] > 0
    assert res["congestion_adjusted_eta_mins"] > 0
    assert len(res["alternative_routes"]) == 2

def test_delay_predictor():
    tool = DelayPredictorTool()
    res = tool.predict_delay(distance_km=15.0, traffic_speed_factor=0.6, rainfall_mm=5.0)
    assert res["predicted_delay_minutes"] >= 0.0
    assert "risk_category" in res["delay_risk_category"].lower() or "delay" in res["delay_risk_category"].lower()

def test_chroma_rag():
    tool = ChromaRAGTool()
    rules = tool.search_rules("Zone B freight rules after 17:00", top_k=2)
    assert len(rules) >= 1
    assert "source" in rules[0]
    assert len(rules[0]["snippet"]) > 0

def test_blackboard_tool():
    state = BlackboardState(
        order_id="TEST-001",
        pickup="Zone A",
        dropoff="Zone B",
        weight_kg=10.0,
        priority="NORMAL",
        deadline_mins=60
    )
    store = {"TEST-001": state}
    tool = BlackboardTool(state_store=store)
    
    # Read state
    data = tool.get_state("TEST-001")
    assert data["order_id"] == "TEST-001"

    # Post update
    res = tool.post_update("TEST-001", "TestAgent", "assigned_driver_id", "D04", "Testing assignment")
    assert res["status"] == "SUCCESS"
    assert state.assigned_driver_id == "D04"
    assert len(state.provenance_log) == 1
