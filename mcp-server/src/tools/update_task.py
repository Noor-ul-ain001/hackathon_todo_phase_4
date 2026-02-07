"""
update_task MCP Tool

Update specific fields of an existing task with ownership verification.

Per constitution.md section 5.2, MUST verify task belongs to user_id.
"""

import sys
from pathlib import Path

# Add backend models to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "backend" / "src"))

from sqlalchemy import select
from datetime import datetime, date, time as dt_time
from typing import Dict, Any
import logging

from models import Task, TaskPriority, TaskStatus
from ..db import get_db_session
from ..validation import (
    validate_user_id,
    validate_task_id,
    validate_title,
    validate_description,
    validate_due_date,
    validate_due_time,
    validate_priority,
    validate_status,
    collect_validation_errors
)

logger = logging.getLogger(__name__)


# ==============================================
# Parameter Validation
# ==============================================

def validate_update_task_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate update_task parameters.

    Args:
        params: Tool parameters

    Returns:
        Dict of validation errors (empty if valid)
    """
    validations = {
        "user_id": validate_user_id(params.get("user_id")),
        "task_id": validate_task_id(params.get("task_id"))
    }

    # Required: updates
    if not params.get("updates"):
        validations["updates"] = "updates object is required"
    elif not isinstance(params["updates"], dict):
        validations["updates"] = "updates must be an object"
    elif len(params["updates"]) == 0:
        validations["updates"] = "updates must contain at least one field"
    else:
        updates = params["updates"]

        # Validate update fields using centralized validators
        if "title" in updates:
            title_error = validate_title(updates["title"])
            if title_error:
                validations["updates.title"] = title_error

        if "description" in updates:
            desc_error = validate_description(updates["description"])
            if desc_error:
                validations["updates.description"] = desc_error

        if "due_date" in updates:
            due_date_error = validate_due_date(updates["due_date"])
            if due_date_error:
                validations["updates.due_date"] = due_date_error

        if "due_time" in updates:
            due_time_error = validate_due_time(updates["due_time"])
            if due_time_error:
                validations["updates.due_time"] = due_time_error

        if "priority" in updates:
            priority_error = validate_priority(updates["priority"])
            if priority_error:
                validations["updates.priority"] = priority_error

        if "status" in updates:
            status_error = validate_status(updates["status"])
            if status_error:
                validations["updates.status"] = status_error

    return collect_validation_errors(validations)


# ==============================================
# update_task Tool Implementation
# ==============================================

async def update_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update specific fields of an existing task.

    Args:
        params: Tool parameters
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
        Tool result with updated task or error

    Example:
        >>> await update_task_tool({
        ...     "user_id": "user_123",
        ...     "task_id": 42,
        ...     "updates": {"priority": "high", "status": "in_progress"}
        ... })
        {
            "success": True,
            "task": {...},
            "updated_fields": ["priority", "status"]
        }
    """
    logger.info(f"update_task called with params: {params}")

    # Validate parameters
    validation_errors = validate_update_task_params(params)
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
        updates = params["updates"]

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

            # Apply updates
            updated_fields = []

            if "title" in updates:
                task.title = updates["title"].strip()
                updated_fields.append("title")

            if "description" in updates:
                task.description = updates["description"].strip() if updates["description"] else None
                updated_fields.append("description")

            if "due_date" in updates:
                task.due_date = date.fromisoformat(updates["due_date"]) if updates["due_date"] else None
                updated_fields.append("due_date")

            if "due_time" in updates:
                task.due_time = dt_time.fromisoformat(updates["due_time"]) if updates["due_time"] else None
                updated_fields.append("due_time")

            if "priority" in updates:
                task.priority = TaskPriority(updates["priority"])
                updated_fields.append("priority")

            if "status" in updates:
                task.status = TaskStatus(updates["status"])
                updated_fields.append("status")

            # Update timestamp
            task.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(task)

            logger.info(f"Task {task_id} updated: {updated_fields}")

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
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                },
                "updated_fields": updated_fields
            }

    except Exception as e:
        logger.error(f"update_task failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to update task",
                "details": str(e)
            }
        }
