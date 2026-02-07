"""
task_deletion Skill

Deletes a task by invoking the delete_task MCP tool.
Permanently removes the task from the database.
"""

from typing import Dict, Any
import logging
from .base_skill import BaseSkill

logger = logging.getLogger(__name__)


class TaskDeletionSkill(BaseSkill):
    """
    Skill for deleting tasks.

    Wraps the delete_task MCP tool with ownership verification.
    """

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            params: Skill input parameters
                - user_id (required): User ID
                - task_id (required): Task ID to delete

        Returns:
            Skill execution result with deletion confirmation

        Example:
            >>> skill = TaskDeletionSkill(mcp_client)
            >>> result = await skill.execute({
            ...     "user_id": "user_123",
            ...     "task_id": 42
            ... })
            {
                "success": True,
                "skill": "TaskDeletionSkill",
                "data": {
                    "task_id": 42,
                    "message": "Task deleted successfully"
                }
            }
        """
        logger.info(f"TaskDeletionSkill executing with params: {params}")

        # Validate required parameters
        if not params.get("user_id"):
            return self._format_error(
                "MISSING_PARAMETER",
                "user_id is required",
                {"field": "user_id"}
            )

        if not params.get("task_id"):
            return self._format_error(
                "MISSING_PARAMETER",
                "task_id is required",
                {"field": "task_id"}
            )

        # Call delete_task MCP tool
        mcp_params = {
            "user_id": params["user_id"],
            "task_id": params["task_id"]
        }

        result = await self._call_mcp_tool("delete_task", mcp_params)

        # Handle MCP tool errors
        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        # Format successful response
        return self._format_success({
            "task_id": result["task_id"],
            "message": result.get("message", "Task deleted successfully")
        })
