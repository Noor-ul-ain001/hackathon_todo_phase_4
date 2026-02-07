"""
task_completion Skill

Marks a task as completed by invoking the complete_task MCP tool.
Sets status to 'completed' and records completion timestamp.
"""

from typing import Dict, Any
import logging
from .base_skill import BaseSkill

logger = logging.getLogger(__name__)


class TaskCompletionSkill(BaseSkill):
    """
    Skill for marking tasks as completed.

    Wraps the complete_task MCP tool.
    """

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            params: Skill input parameters
                - user_id (required): User ID
                - task_id (required): Task ID to complete

        Returns:
            Skill execution result with completed task

        Example:
            >>> skill = TaskCompletionSkill(mcp_client)
            >>> result = await skill.execute({
            ...     "user_id": "user_123",
            ...     "task_id": 42
            ... })
            {
                "success": True,
                "skill": "TaskCompletionSkill",
                "data": {
                    "task": {...},
                    "message": "Task completed: Review architecture spec"
                }
            }
        """
        logger.info(f"TaskCompletionSkill executing with params: {params}")

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

        # Call complete_task MCP tool
        mcp_params = {
            "user_id": params["user_id"],
            "task_id": params["task_id"]
        }

        result = await self._call_mcp_tool("complete_task", mcp_params)

        # Handle MCP tool errors
        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        # Format successful response
        task = result["task"]
        message = result.get("message", f"Task completed: {task['title']}")

        return self._format_success({
            "task": task,
            "message": message
        })
