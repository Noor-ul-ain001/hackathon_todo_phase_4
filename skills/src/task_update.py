"""
task_update Skill

Updates a task by invoking the update_task MCP tool.
Supports partial updates of task fields.
"""

from typing import Dict, Any
import logging
from .base_skill import BaseSkill

logger = logging.getLogger(__name__)


class TaskUpdateSkill(BaseSkill):
    """
    Skill for updating existing tasks.

    Wraps the update_task MCP tool with ownership verification.
    """

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing task.

        Args:
            params: Skill input parameters
                - user_id (required): User ID
                - task_id (required): Task ID to update
                - updates (required): Fields to update
                  - title (optional): New title
                  - description (optional): New description
                  - due_date (optional): New due date
                  - due_time (optional): New due time
                  - priority (optional): New priority
                  - status (optional): New status

        Returns:
            Skill execution result with updated task

        Example:
            >>> skill = TaskUpdateSkill(mcp_client)
            >>> result = await skill.execute({
            ...     "user_id": "user_123",
            ...     "task_id": 42,
            ...     "updates": {"priority": "high", "status": "in_progress"}
            ... })
            {
                "success": True,
                "skill": "TaskUpdateSkill",
                "data": {
                    "task": {...},
                    "updated_fields": ["priority", "status"],
                    "message": "Task updated successfully"
                }
            }
        """
        logger.info(f"TaskUpdateSkill executing with params: {params}")

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

        if not params.get("updates"):
            return self._format_error(
                "MISSING_PARAMETER",
                "updates object is required",
                {"field": "updates"}
            )

        # Call update_task MCP tool
        mcp_params = {
            "user_id": params["user_id"],
            "task_id": params["task_id"],
            "updates": params["updates"]
        }

        result = await self._call_mcp_tool("update_task", mcp_params)

        # Handle MCP tool errors
        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        # Format successful response
        updated_fields = result.get("updated_fields", [])
        return self._format_success({
            "task": result["task"],
            "updated_fields": updated_fields,
            "message": f"Task updated: {', '.join(updated_fields)}"
        })
