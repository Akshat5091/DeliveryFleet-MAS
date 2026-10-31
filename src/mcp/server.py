"""Model Context Protocol (MCP) Server exposing external fleet dispatch tools."""
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from .tools.driver_db import DriverDBTool
from .tools.routing_engine import RoutingEngineTool
from .tools.delay_predictor import DelayPredictorTool
from .tools.chroma_rag import ChromaRAGTool
from .tools.blackboard_tool import BlackboardTool

# Initialize FastMCP Server
mcp_server = FastMCP(
    name="LogisticsFleetMCPServer",
    instructions="MCP Server exposing fleet driver DB, routing engine, ML delay forecaster, and policy RAG search."
)

# Instantiations of the 5 underlying tools
_driver_db = DriverDBTool()
_routing_engine = RoutingEngineTool()
_delay_predictor = DelayPredictorTool()
_chroma_rag = ChromaRAGTool()
_blackboard_tool = BlackboardTool()

@mcp_server.tool()
def driver_db_lookup(
    zone: Optional[str] = None,
    min_capacity_kg: float = 0.0,
    max_shift_hours: float = 9.0
) -> List[Dict[str, Any]]:
    """MCP Tool: Query available fleet drivers filtered by operational zone and vehicle payload capacity."""
    return _driver_db.find_eligible_drivers(
        zone=zone,
        min_capacity_kg=min_capacity_kg,
        max_shift_hours=max_shift_hours
    )

@mcp_server.tool()
def routing_engine_calculate(
    pickup_location: str,
    dropoff_location: str,
    priority: str = "NORMAL"
) -> Dict[str, Any]:
    """MCP Tool: Calculate primary transit corridor, alternative routes, and congestion-adjusted ETA."""
    return _routing_engine.calculate_route(
        pickup_location=pickup_location,
        dropoff_location=dropoff_location,
        priority=priority
    )

@mcp_server.tool()
def delay_predictor_forecast(
    distance_km: float,
    traffic_speed_factor: float = 0.80,
    rainfall_mm: float = 0.0,
    hour_of_day: int = 14,
    weight_kg: float = 15.0
) -> Dict[str, Any]:
    """MCP Tool: ML Random Forest regression tool forecasting expected delay in minutes."""
    return _delay_predictor.predict_delay(
        distance_km=distance_km,
        traffic_speed_factor=traffic_speed_factor,
        rainfall_mm=rainfall_mm,
        hour_of_day=hour_of_day,
        weight_kg=weight_kg
    )

@mcp_server.tool()
def policy_rag_search(
    query: str,
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """MCP Tool: Vector RAG search across company operating policies, driver hour limits, and zone rules."""
    return _chroma_rag.search_rules(query=query, top_k=top_k)

@mcp_server.tool()
def blackboard_update(
    order_id: str,
    agent_name: str,
    field_name: str,
    value: Any,
    description: str
) -> Dict[str, Any]:
    """MCP Tool: Write an intermediate state update to the central Blackboard with provenance trail."""
    return _blackboard_tool.post_update(
        order_id=order_id,
        agent_name=agent_name,
        field_name=field_name,
        value=value,
        description=description
    )

def get_direct_tools():
    """Return dictionary of instantiated tools for direct in-process calling without network overhead."""
    return {
        "driver_db": _driver_db,
        "routing_engine": _routing_engine,
        "delay_predictor": _delay_predictor,
        "chroma_rag": _chroma_rag,
        "blackboard_tool": _blackboard_tool
    }

if __name__ == "__main__":
    mcp_server.run()
