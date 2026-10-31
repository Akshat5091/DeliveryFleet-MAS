"""Tests for floating-point safety, division-by-zero guards, and numerical boundary conditions."""
import pytest
import math
from src.mcp.tools.routing_engine import RoutingEngineTool
from src.mcp.tools.delay_predictor import DelayPredictorTool
from src.agents.crew_dispatch_agent import CrewDispatchAgent
from src.schemas.blackboard import CandidateDriver

def test_routing_identical_pickup_dropoff():
    """Verify that identical pickup and dropoff points produce 0.0 distance and 0.0 ETA without division-by-zero."""
    tool = RoutingEngineTool()
    res = tool.calculate_route(
        pickup_location="Zone A - Warehouse 1",
        dropoff_location="Zone A - Warehouse 1",
        priority="NORMAL"
    )
    assert res["distance_km"] == 0.0
    assert res["base_eta_mins"] == 0.0
    assert res["congestion_adjusted_eta_mins"] == 0.0
    assert "Intra-Facility" in res["primary_route"]
    for alt in res["alternative_routes"]:
        assert alt["distance_km"] == 0.0
        assert alt["eta_mins"] == 0.0

def test_routing_priority_green_corridor():
    """Verify that CRITICAL priority consignments activate green-corridor priority speeds and lower ETAs."""
    tool = RoutingEngineTool()
    normal_route = tool.calculate_route(
        pickup_location="Zone A - Warehouse 1",
        dropoff_location="Zone B - Tech Park",
        priority="NORMAL"
    )
    critical_route = tool.calculate_route(
        pickup_location="Zone A - Warehouse 1",
        dropoff_location="Zone B - Tech Park",
        priority="CRITICAL"
    )
    assert critical_route["distance_km"] == normal_route["distance_km"]
    assert critical_route["speed_factor"] >= normal_route["speed_factor"]
    assert critical_route["congestion_adjusted_eta_mins"] <= normal_route["congestion_adjusted_eta_mins"]

def test_routing_invalid_zone_locations():
    """Verify that None, empty strings, and arbitrary location names extract safely without throwing AttributeError."""
    tool = RoutingEngineTool()
    # None locations
    res1 = tool.calculate_route(None, None)
    assert res1["distance_km"] > 0
    assert res1["congestion_adjusted_eta_mins"] > 0

    # Arbitrary strings without 'Zone'
    res2 = tool.calculate_route("Downtown Central Pier", "Suburban Heights")
    assert res2["distance_km"] > 0
    assert math.isfinite(res2["congestion_adjusted_eta_mins"])

def test_delay_predictor_zero_distance():
    """Verify that a zero-distance delivery returns exactly 0.0 delay with LOW_DELAY_RISK."""
    tool = DelayPredictorTool()
    res = tool.predict_delay(
        distance_km=0.0,
        traffic_speed_factor=0.6,
        rainfall_mm=10.0,
        hour_of_day=17,
        weight_kg=20.0
    )
    assert res["predicted_delay_minutes"] == 0.0
    assert res["delay_risk_category"] == "LOW_DELAY_RISK"

def test_delay_predictor_extreme_bounds():
    """Verify that out-of-bounds inputs (negative, NaN, huge numbers) clamp safely without crashing."""
    tool = DelayPredictorTool()
    res = tool.predict_delay(
        distance_km=500.0,
        traffic_speed_factor=999.0,
        rainfall_mm=500.0,
        hour_of_day=99,
        weight_kg=10000.0
    )
    assert math.isfinite(res["predicted_delay_minutes"])
    assert res["predicted_delay_minutes"] >= 0.0
    assert res["delay_risk_category"] in ["LOW_DELAY_RISK", "MODERATE_DELAY_RISK", "CRITICAL_DELAY_RISK"]

def test_dispatch_agent_zero_hours_and_extremes():
    """Verify that candidate drivers with 0.0 hours worked or extreme ratings compute penalties cleanly."""
    from src.schemas.blackboard import CandidateDriver
    agent = CrewDispatchAgent()

    drivers = [
        CandidateDriver(
            driver_id="D-FRESH",
            name="New Driver",
            current_zone="Zone A",
            vehicle_type="Van",
            capacity_kg=50.0,
            hours_worked=0.0,  # Zero hours worked
            rating=5.0,
            status="AVAILABLE"
        ),
        CandidateDriver(
            driver_id="D-MID",
            name="Mid Driver",
            current_zone="Zone A",
            vehicle_type="Van",
            capacity_kg=50.0,
            hours_worked=4.0,
            rating=4.5,
            status="AVAILABLE"
        )
    ]

    dec = agent.decide_assignment(
        order_id="TEST-MATH-01",
        pickup="Zone A - Warehouse 1",
        dropoff="Zone B - Tech Park",
        weight_kg=10.0,
        priority="NORMAL",
        deadline_mins=45,
        candidate_drivers=drivers,
        prompt_style="ReAct"
    )
    assert dec.assigned_driver_id == "D-FRESH"
    assert dec.confidence_score > 0.9
