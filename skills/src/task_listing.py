"""
task_listing Skill

Lists tasks by invoking the list_tasks MCP tool.
Supports filtering, sorting, and pagination.
"""

from typing import Dict, Any
import logging
from .base_skill import BaseSkill

logger = logging.getLogger(__name__)


class TaskListingSkill(BaseSkill):
    """
    Skill for listing tasks with filters, sorting, and pagination.

    Wraps the list_tasks MCP tool.
    """

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List tasks for a user.

        Args:
            params: Skill input parameters
                - user_id (required): User ID
                - filters (optional): Filter criteria
                  - status: Filter by status
                  - priority: Filter by priority
                  - due_before: Tasks due before this date
                  - due_after: Tasks due after this date
                  - search: Search in title/description
                - sort (optional): Sort order (default: created_at_desc)
                - limit (optional): Max results (1-100, default 20)
                - offset (optional): Pagination offset (default 0)

        Returns:
            Skill execution result with task list

        Example:
            >>> skill = TaskListingSkill(mcp_client)
            >>> result = await skill.execute({
            ...     "user_id": "user_123",
            ...     "filters": {"status": "pending", "priority": "high"},
            ...     "sort": "due_date_asc",
            ...     "limit": 10
            ... })
            {
                "success": True,
                "skill": "TaskListingSkill",
                "data": {
                    "tasks": [...],
                    "count": 5,
                    "total_count": 12,
                    "has_more": True
                }
            }
        """
        logger.info(f"TaskListingSkill executing with params: {params}")

        # Validate required parameters
        if not params.get("user_id"):
            return self._format_error(
                "MISSING_PARAMETER",
                "user_id is required",
                {"field": "user_id"}
            )

        # Call list_tasks MCP tool
        mcp_params = {
            "user_id": params["user_id"],
            "filters": params.get("filters", {}),
            "sort": params.get("sort", "created_at_desc"),
            "limit": params.get("limit", 20),
            "offset": params.get("offset", 0)
        }

        result = await self._call_mcp_tool("list_tasks", mcp_params)

        # Handle MCP tool errors
        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        # Format successful response
        return self._format_success({
            "tasks": result["tasks"],
            "count": result["count"],
            "total_count": result.get("total_count", result["count"]),
            "has_more": result.get("has_more", False),
            "message": f"Found {result['count']} task(s)"
        })
