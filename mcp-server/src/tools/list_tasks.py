"""
list_tasks MCP Tool

Query and retrieve tasks for a specific user with filtering, sorting, and pagination.

Per constitution.md section 5.2, MUST include user_id in WHERE clause.
CRITICAL: Never returns other users' tasks.
"""

import sys
from pathlib import Path

# Add backend models to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "backend" / "src"))

from sqlalchemy import select, func, or_
from datetime import date
from typing import Optional, Dict, Any, List
import logging

from models import Task, TaskPriority, TaskStatus
from ..db import get_db_session
from ..validation import (
    validate_user_id,
    validate_priority,
    validate_status,
    validate_due_date,
    collect_validation_errors
)

logger = logging.getLogger(__name__)


# ==============================================
# Parameter Validation
# ==============================================

def validate_list_tasks_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate list_tasks parameters.

    Args:
        params: Tool parameters

    Returns:
        Dict of validation errors (empty if valid)
    """
    validations = {
        "user_id": validate_user_id(params.get("user_id"))
    }

    # Optional: limit (1-100)
    if "limit" in params:
        limit = params["limit"]
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            validations["limit"] = "limit must be an integer between 1 and 100"

    # Optional: offset (>= 0)
    if "offset" in params:
        offset = params["offset"]
        if not isinstance(offset, int) or offset < 0:
            validations["offset"] = "offset must be a non-negative integer"

    # Optional: sort
    valid_sorts = [
        "created_at_asc", "created_at_desc",
        "due_date_asc", "due_date_desc",
        "priority_asc", "priority_desc",
        "title_asc", "title_desc"
    ]
    if "sort" in params and params["sort"]:
        if params["sort"] not in valid_sorts:
            validations["sort"] = f"sort must be one of: {', '.join(valid_sorts)}"

    # Optional: filters
    if "filters" in params and params["filters"]:
        filters = params["filters"]
        if not isinstance(filters, dict):
            validations["filters"] = "filters must be an object"
        else:
            # Validate filter fields using centralized validators
            if "status" in filters and filters["status"]:
                status_error = validate_status(filters["status"])
                if status_error:
                    validations["filters.status"] = status_error

            if "priority" in filters and filters["priority"]:
                priority_error = validate_priority(filters["priority"])
                if priority_error:
                    validations["filters.priority"] = priority_error

            if "due_before" in filters and filters["due_before"]:
                due_before_error = validate_due_date(filters["due_before"])
                if due_before_error:
                    validations["filters.due_before"] = due_before_error

            if "due_after" in filters and filters["due_after"]:
                due_after_error = validate_due_date(filters["due_after"])
                if due_after_error:
                    validations["filters.due_after"] = due_after_error

            if "search" in filters and filters["search"]:
                if not isinstance(filters["search"], str) or len(filters["search"]) > 100:
                    validations["filters.search"] = "search must be a string (max 100 characters)"

    return collect_validation_errors(validations)


# ==============================================
# list_tasks Tool Implementation
# ==============================================

async def list_tasks_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Query tasks for a user with optional filtering, sorting, and pagination.

    Args:
        params: Tool parameters
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
        Tool result with tasks array or error

    Example:
        >>> await list_tasks_tool({
        ...     "user_id": "user_123",
        ...     "filters": {"status": "pending", "priority": "high"},
        ...     "sort": "due_date_asc",
        ...     "limit": 10
        ... })
        {
            "success": True,
            "tasks": [...],
            "count": 2,
            "has_more": False
        }
    """
    logger.info(f"list_tasks called with params: {params}")

    # Validate parameters
    validation_errors = validate_list_tasks_params(params)
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
        filters = params.get("filters", {})
        sort = params.get("sort", "created_at_desc")
        limit = params.get("limit", 20)
        offset = params.get("offset", 0)

        async for session in get_db_session():
            # Build query with user_id filter (CRITICAL for isolation)
            query = select(Task).where(Task.user_id == user_id)

            # Apply filters
            if filters.get("status"):
                query = query.where(Task.status == TaskStatus(filters["status"]))

            if filters.get("priority"):
                query = query.where(Task.priority == TaskPriority(filters["priority"]))

            if filters.get("due_before"):
                due_before_date = date.fromisoformat(filters["due_before"])
                query = query.where(Task.due_date < due_before_date)

            if filters.get("due_after"):
                due_after_date = date.fromisoformat(filters["due_after"])
                query = query.where(Task.due_date > due_after_date)

            if filters.get("search"):
                search_term = f"%{filters['search']}%"
                query = query.where(
                    or_(
                        Task.title.ilike(search_term),
                        Task.description.ilike(search_term)
                    )
                )

            # Apply sorting
            if sort == "created_at_asc":
                query = query.order_by(Task.created_at.asc())
            elif sort == "created_at_desc":
                query = query.order_by(Task.created_at.desc())
            elif sort == "due_date_asc":
                query = query.order_by(Task.due_date.asc().nulls_last())
            elif sort == "due_date_desc":
                query = query.order_by(Task.due_date.desc().nulls_last())
            elif sort == "priority_asc":
                query = query.order_by(Task.priority.asc())
            elif sort == "priority_desc":
                query = query.order_by(Task.priority.desc())
            elif sort == "title_asc":
                query = query.order_by(Task.title.asc())
            elif sort == "title_desc":
                query = query.order_by(Task.title.desc())

            # Get total count (before pagination)
            count_query = select(func.count()).select_from(query.subquery())
            count_result = await session.execute(count_query)
            total_count = count_result.scalar()

            # Apply pagination
            query = query.limit(limit).offset(offset)

            # Execute query
            result = await session.execute(query)
            tasks = result.scalars().all()

            # Format tasks
            formatted_tasks = []
            for task in tasks:
                formatted_tasks.append({
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
                })

            logger.info(f"list_tasks returned {len(formatted_tasks)} tasks for user_id={user_id}")

            return {
                "success": True,
                "tasks": formatted_tasks,
                "count": len(formatted_tasks),
                "total_count": total_count,
                "has_more": (offset + len(formatted_tasks)) < total_count
            }

    except Exception as e:
        logger.error(f"list_tasks failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to query tasks",
                "details": str(e)
            }
        }
