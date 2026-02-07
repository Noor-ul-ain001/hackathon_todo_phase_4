"""
add_task MCP Tool

Creates a new task for a user with validation and user isolation.

Per constitution.md section 5.2, MUST include user_id in database operations.
"""

import sys
from pathlib import Path

# Add backend models to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "backend" / "src"))

from sqlalchemy import select
from datetime import datetime, date, time as dt_time
from typing import Optional, Dict, Any
import logging

from models import Task, TaskPriority, TaskStatus
from ..db import get_db_session
from ..validation import (
    validate_user_id,
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

def validate_add_task_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate add_task parameters.

    Args:
        params: Tool parameters

    Returns:
        Dict of validation errors (empty if valid)
    """
    return collect_validation_errors({
        "user_id": validate_user_id(params.get("user_id")),
        "title": validate_title(params.get("title")),
        "description": validate_description(params.get("description")),
        "due_date": validate_due_date(params.get("due_date")),
        "due_time": validate_due_time(params.get("due_time")),
        "priority": validate_priority(params.get("priority")),
        "status": validate_status(params.get("status"))
    })


# ==============================================
# add_task Tool Implementation
# ==============================================

async def add_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new task for a user.

    Args:
        params: Tool parameters
            - user_id (required): User ID
            - title (required): Task title
            - description (optional): Task description
            - due_date (optional): Due date (ISO 8601)
            - due_time (optional): Due time (HH:MM)
            - priority (optional): Task priority (low|medium|high)
            - status (optional): Task status (pending|in_progress|completed)

    Returns:
        Tool result with created task or error

    Example:
        >>> await add_task_tool({
        ...     "user_id": "user_123",
        ...     "title": "Review architecture spec",
        ...     "due_date": "2025-12-28",
        ...     "priority": "high"
        ... })
        {
            "success": True,
            "task": {
                "task_id": 42,
                "user_id": "user_123",
                "title": "Review architecture spec",
                ...
            }
        }
    """
    logger.info(f"add_task called with params: {params}")

    # Validate parameters
    validation_errors = validate_add_task_params(params)
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
        # Extract and sanitize parameters
        user_id = params["user_id"].strip()
        title = params["title"].strip()
        description = params.get("description", "").strip() if params.get("description") else None

        # Parse optional fields
        due_date_obj = date.fromisoformat(params["due_date"]) if params.get("due_date") else None
        due_time_obj = dt_time.fromisoformat(params["due_time"]) if params.get("due_time") else None
        priority = TaskPriority(params.get("priority", "medium"))
        status = TaskStatus(params.get("status", "pending"))

        # Create task
        async for session in get_db_session():
            new_task = Task(
                user_id=user_id,
                title=title,
                description=description,
                due_date=due_date_obj,
                due_time=due_time_obj,
                priority=priority,
                status=status,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

            logger.info(f"Task created: ID={new_task.id}, user_id={user_id}")

            return {
                "success": True,
                "task": {
                    "task_id": new_task.id,
                    "user_id": new_task.user_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                    "due_time": new_task.due_time.isoformat() if new_task.due_time else None,
                    "priority": new_task.priority.value,
                    "status": new_task.status.value,
                    "completed_at": new_task.completed_at.isoformat() if new_task.completed_at else None,
                    "created_at": new_task.created_at.isoformat(),
                    "updated_at": new_task.updated_at.isoformat()
                }
            }

    except Exception as e:
        logger.error(f"add_task failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to create task",
                "details": str(e)
            }
        }
