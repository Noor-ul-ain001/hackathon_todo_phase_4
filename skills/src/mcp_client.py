"""
MCP Client Module for Skills

Provides communication interface between skills and MCP server.
Skills invoke MCP tools through this client.
"""

import httpx
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class MCPClient:
    """Client for communicating with MCP server."""

    def __init__(self, mcp_server_url: Optional[str] = None):
        """
        Initialize MCP client.

        Args:
            mcp_server_url: URL of MCP server (defaults to env var MCP_SERVER_URL)
        """
        self.mcp_server_url = mcp_server_url or os.getenv(
            "MCP_SERVER_URL",
            "http://localhost:8001"
        )
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info(f"MCPClient initialized with server: {self.mcp_server_url}")

    async def call_tool(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call an MCP tool.

        Args:
            tool_name: Name of the MCP tool (add_task, list_tasks, etc.)
            params: Tool parameters

        Returns:
            Tool response

        Raises:
            httpx.HTTPError: If HTTP request fails
        """
        logger.info(f"Calling MCP tool: {tool_name} with params: {params}")

        try:
            response = await self.client.post(
                f"{self.mcp_server_url}/tools/{tool_name}",
                json=params
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"MCP tool {tool_name} returned: {result.get('success', False)}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"MCP tool {tool_name} failed: {e}")
            return {
                "success": False,
                "error": {
                    "code": "MCP_CLIENT_ERROR",
                    "message": f"Failed to call MCP tool {tool_name}",
                    "details": str(e)
                }
            }

    async def add_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call add_task MCP tool."""
        return await self.call_tool("add_task", params)

    async def list_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call list_tasks MCP tool."""
        return await self.call_tool("list_tasks", params)

    async def update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call update_task MCP tool."""
        return await self.call_tool("update_task", params)

    async def complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call complete_task MCP tool."""
        return await self.call_tool("complete_task", params)

    async def delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call delete_task MCP tool."""
        return await self.call_tool("delete_task", params)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
        logger.info("MCPClient closed")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
