"""
Base Skill Class

All skills inherit from this base class for common functionality.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseSkill(ABC):
    """
    Base class for all skills.

    Skills are wrappers around MCP tools that provide:
    - Input schema validation
    - Error handling and formatting
    - Logging and monitoring
    """

    def __init__(self, mcp_client):
        """
        Initialize skill.

        Args:
            mcp_client: MCPClient instance for calling MCP tools
        """
        self.mcp_client = mcp_client
        self.skill_name = self.__class__.__name__
        logger.info(f"Skill initialized: {self.skill_name}")

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill.

        Args:
            params: Skill input parameters

        Returns:
            Skill execution result
        """
        pass

    def _format_success(self, data: Any) -> Dict[str, Any]:
        """
        Format successful result.

        Args:
            data: Result data

        Returns:
            Standardized success response
        """
        return {
            "success": True,
            "skill": self.skill_name,
            "data": data
        }

    def _format_error(
        self,
        code: str,
        message: str,
        details: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Format error result.

        Args:
            code: Error code
            message: Error message
            details: Additional error details

        Returns:
            Standardized error response
        """
        return {
            "success": False,
            "skill": self.skill_name,
            "error": {
                "code": code,
                "message": message,
                "details": details
            }
        }

    async def _call_mcp_tool(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call MCP tool with error handling.

        Args:
            tool_name: MCP tool name
            params: Tool parameters

        Returns:
            Tool result
        """
        logger.info(f"{self.skill_name} calling MCP tool: {tool_name}")

        result = await self.mcp_client.call_tool(tool_name, params)

        if not result.get("success"):
            logger.warning(f"{self.skill_name} MCP tool {tool_name} failed: {result.get('error')}")

        return result
