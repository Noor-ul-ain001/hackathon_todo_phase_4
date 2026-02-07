"""
delete_task MCP Tool

Delete a task from the database with ownership verification.

Per constitution.md section 5.2, MUST verify task belongs to user_id.
"""

import sys
from pathlib import Path

# Add backend models to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "backend" / "src"))

from sqlalchemy import select, delete
from typing import Dict, Any
import logging

from models import Task
from ..db import get_db_session

logger = logging.getLogger(__name__)


# Import validation functions
from ..validation import validate_user_id, validate_task_id, collect_validation_errors


# ==============================================
# Parameter Validation
# ==============================================

def validate_delete_task_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate delete_task parameters.

    Args:
        params: Tool parameters

    Returns:
        Dict of validation errors (empty if valid)
    """
    return collect_validation_errors({
        "user_id": validate_user_id(params.get("user_id")),
        "task_id": validate_task_id(params.get("task_id"))
    })


# ==============================================
# delete_task Tool Implementation
# ==============================================

async def delete_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a task from the database.

    Args:
        params: Tool parameters
            - user_id (required): User ID
            - task_id (required): Task ID to delete

    Returns:
        Tool result with success confirmation or error

    Example:
        >>> await delete_task_tool({
        ...     "user_id": "user_123",
        ...     "task_id": 42
        ... })
        {
            "success": True,
            "task_id": 42,
            "message": "Task deleted successfully"
        }
    """
    logger.info(f"delete_task called with params: {params}")

    # Validate parameters
    validation_errors = validate_delete_task_params(params)
    if validation_errors:
        logger.warning(f"Validation failed: {validation_errors}")
        return {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid parameters",
                "details": validation_errors
            }
        }

    try:
        user_id = params["user_id"].strip()
        task_id = params["task_id"]

        async for session in get_db_session():
            # Verify ownership before deletion (CRITICAL for user isolation)
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Task {task_id} not found or doesn't belong to user {user_id}")
                # Return success (idempotent - already deleted or doesn't exist)
                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "Task does not exist or was already deleted"
                }

            # Delete task
            await session.delete(task)
            await session.commit()

            logger.info(f"Task {task_id} deleted for user {user_id}")

            return {
                "success": True,
                "task_id": task_id,
                "message": "Task deleted successfully"
            }

    except Exception as e:
        logger.error(f"delete_task failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to delete task",
                "details": str(e)
            }
        }
