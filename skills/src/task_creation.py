"""
task_creation Skill

Creates a new task by invoking the add_task MCP tool.
Handles task creation from natural language, CLI commands, or structured input.
"""

from typing import Dict, Any
import logging
from .base_skill import BaseSkill

logger = logging.getLogger(__name__)


class TaskCreationSkill(BaseSkill):
    """
    Skill for creating new tasks.

    Wraps the add_task MCP tool with additional logic for:
    - Input normalization
    - Default value handling
    - Success/error formatting
    """

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task.

        Args:
            params: Skill input parameters
                - user_id (required): User ID
                - title (required): Task title
                - description (optional): Task description
                - due_date (optional): Due date (ISO 8601 YYYY-MM-DD)
                - due_time (optional): Due time (HH:MM)
                - priority (optional): Task priority (low|medium|high)
                - status (optional): Task status (pending|in_progress|completed)

        Returns:
            Skill execution result with created task

        Example:
            >>> skill = TaskCreationSkill(mcp_client)
            >>> result = await skill.execute({
            ...     "user_id": "user_123",
            ...     "title": "Review architecture spec",
            ...     "due_date": "2025-12-28",
            ...     "priority": "high"
            ... })
            {
                "success": True,
                "skill": "TaskCreationSkill",
                "data": {
                    "task": {...},
                    "message": "Task created successfully"
                }
            }
        """
        logger.info(f"TaskCreationSkill executing with params: {params}")

        # Validate required parameters
        if not params.get("user_id"):
            return self._format_error(
                "MISSING_PARAMETER",
                "user_id is required",
                {"field": "user_id"}
            )

        if not params.get("title"):
            return self._format_error(
                "MISSING_PARAMETER",
                "title is required",
                {"field": "title"}
            )

        # Call add_task MCP tool
        mcp_params = {
            "user_id": params["user_id"],
            "title": params["title"],
            "description": params.get("description"),
            "due_date": params.get("due_date"),
            "due_time": params.get("due_time"),
            "priority": params.get("priority", "medium"),
            "status": params.get("status", "pending")
        }

        result = await self._call_mcp_tool("add_task", mcp_params)

        # Handle MCP tool errors
        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        # Format successful response
        return self._format_success({
            "task": result["task"],
            "message": f"Task created: {result['task']['title']}"
        })
