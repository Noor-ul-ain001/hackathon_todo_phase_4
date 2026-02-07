"""
complete_task MCP Tool

Mark a task as completed with ownership verification.

Per constitution.md section 5.2, MUST verify task belongs to user_id.
"""

import sys
from pathlib import Path

# Add backend models to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "backend" / "src"))

from sqlalchemy import select
from datetime import datetime
from typing import Dict, Any
import logging

from models import Task, TaskStatus
from ..db import get_db_session

logger = logging.getLogger(__name__)


# Import validation functions
from ..validation import validate_user_id, validate_task_id, collect_validation_errors


# ==============================================
# Parameter Validation
# ==============================================

def validate_complete_task_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate complete_task parameters.

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
# complete_task Tool Implementation
# ==============================================

async def complete_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        params: Tool parameters
            - user_id (required): User ID
            - task_id (required): Task ID to complete

    Returns:
        Tool result with completed task or error

    Example:
        >>> await complete_task_tool({
        ...     "user_id": "user_123",
        ...     "task_id": 42
        ... })
        {
            "success": True,
            "task": {
                "task_id": 42,
                "status": "completed",
                "completed_at": "2025-12-27T16:00:00",
                ...
            }
        }
    """
    logger.info(f"complete_task called with params: {params}")

    # Validate parameters
    validation_errors = validate_complete_task_params(params)
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
            # Verify ownership (CRITICAL for user isolation)
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Task {task_id} not found or doesn't belong to user {user_id}")
                return {
                    "success": False,
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Task does not belong to this user or does not exist"
                    }
                }

            # Check if already completed (idempotent)
            if task.status == TaskStatus.COMPLETED:
                logger.info(f"Task {task_id} already completed")
                # Return success (idempotent operation)
                return {
                    "success": True,
                    "task": {
                        "task_id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "status": task.status.value,
                        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                        "updated_at": task.updated_at.isoformat()
                    },
                    "message": "Task was already completed"
                }

            # Mark as completed
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(task)

            logger.info(f"Task {task_id} marked as completed")

            return {
                "success": True,
                "task": {
                    "task_id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "due_time": task.due_time.isoformat() if task.due_time else None,
                    "priority": task.priority.value,
                    "status": task.status.value,
                    "completed_at": task.completed_at.isoformat(),
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }

    except Exception as e:
        logger.error(f"complete_task failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to complete task",
                "details": str(e)
            }
        }
