"""Model Context Protocol (MCP) Client for interacting with FastMCP registered tools.
Course: CSE3101 Agentic AI | Group 8 | Multi-Agent Delivery Fleet
"""
import asyncio
import inspect
from typing import Any, Dict, List, Optional
from .server import mcp_server

class MCPClient:
    """Production-grade MCP Client calling tools registered with the FastMCP LogisticsFleetMCPServer."""

    def __init__(self, server=mcp_server):
        self.server = server

    def list_tools(self) -> List[str]:
        """List names of all registered tools on the MCP server."""
        try:
            tools = self.server._tool_manager.list_tools()
            return [t.name for t in tools]
        except Exception:
            return [
                "driver_db_lookup",
                "routing_engine_calculate",
                "delay_predictor_forecast",
                "policy_rag_search",
                "blackboard_update"
            ]

    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve schema and documentation for a specific MCP tool."""
        tool = self.server._tool_manager.get_tool(name)
        if not tool:
            return None
        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters if hasattr(tool, "parameters") else {}
        }

    async def call_tool_async(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """Asynchronously call an MCP tool using FastMCP's internal protocol session handler."""
        args = arguments or {}
        tool = self.server._tool_manager.get_tool(name)
        if tool is None:
            raise KeyError(f"Tool '{name}' not found on MCP Server '{self.server.name}'")

        res = tool.run(args)
        if inspect.iscoroutine(res):
            return await res
        return res

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """Synchronously execute a registered MCP tool across thread and event-loop boundaries."""
        args = arguments or {}
        tool = self.server._tool_manager.get_tool(name)
        if tool is None:
            raise KeyError(f"Tool '{name}' not found on MCP Server '{self.server.name}'")

        # Detect active running asyncio event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Already inside an event loop: call underlying function directly
            if hasattr(tool, "fn") and callable(tool.fn):
                return tool.fn(**args)
            return asyncio.ensure_future(self.call_tool_async(name, args))
        else:
            return asyncio.run(self.call_tool_async(name, args))

# Singleton client instance
mcp_client = MCPClient()

