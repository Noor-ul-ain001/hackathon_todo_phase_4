"""
Parameter validation module for MCP tools.

Provides reusable validation functions per constitution.md section 8.4.
"""

from typing import Dict, Any, Optional
from datetime import date, time as dt_time
import re


# ==============================================
# Common Validation Functions
# ==============================================

def validate_user_id(user_id: Any) -> Optional[str]:
    """
    Validate user_id parameter.

    Args:
        user_id: User ID to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not user_id:
        return "user_id is required"
    if not isinstance(user_id, str):
        return "user_id must be a string"
    if len(user_id.strip()) == 0:
        return "user_id cannot be empty"
    return None


def validate_task_id(task_id: Any) -> Optional[str]:
    """
    Validate task_id parameter.

    Args:
        task_id: Task ID to validate

    Returns:
        Error message if invalid, None if valid
    """
    if task_id is None:
        return "task_id is required"
    if not isinstance(task_id, int):
        return "task_id must be an integer"
    if task_id <= 0:
        return "task_id must be a positive integer"
    return None


def validate_title(title: Any) -> Optional[str]:
    """
    Validate task title.

    Args:
        title: Title to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not title:
        return "title is required"
    if not isinstance(title, str):
        return "title must be a string"
    if len(title.strip()) == 0:
        return "title cannot be empty"
    if len(title) > 200:
        return "title cannot exceed 200 characters"
    return None


def validate_description(description: Any) -> Optional[str]:
    """
    Validate task description (optional field).

    Args:
        description: Description to validate

    Returns:
        Error message if invalid, None if valid
    """
    if description is None or description == "":
        return None  # Optional field
    if not isinstance(description, str):
        return "description must be a string"
    if len(description) > 2000:
        return "description cannot exceed 2000 characters"
    return None


def validate_due_date(due_date: Any) -> Optional[str]:
    """
    Validate due_date (ISO 8601 format YYYY-MM-DD).

    Args:
        due_date: Date string to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not due_date:
        return None  # Optional field
    if not isinstance(due_date, str):
        return "due_date must be a string"
    try:
        date.fromisoformat(due_date)
        return None
    except ValueError:
        return "due_date must be in ISO 8601 format (YYYY-MM-DD)"


def validate_due_time(due_time: Any) -> Optional[str]:
    """
    Validate due_time (HH:MM format).

    Args:
        due_time: Time string to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not due_time:
        return None  # Optional field
    if not isinstance(due_time, str):
        return "due_time must be a string"
    try:
        dt_time.fromisoformat(due_time)
        return None
    except ValueError:
        return "due_time must be in HH:MM format"


def validate_priority(priority: Any) -> Optional[str]:
    """
    Validate priority (low | medium | high).

    Args:
        priority: Priority to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not priority:
        return None  # Optional field (default: medium)
    if not isinstance(priority, str):
        return "priority must be a string"
    if priority not in ["low", "medium", "high"]:
        return "priority must be one of: low, medium, high"
    return None


def validate_status(status: Any) -> Optional[str]:
    """
    Validate status (pending | in_progress | completed | deleted).

    Args:
        status: Status to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not status:
        return None  # Optional field (default: pending)
    if not isinstance(status, str):
        return "status must be a string"
    if status not in ["pending", "in_progress", "completed", "deleted"]:
        return "status must be one of: pending, in_progress, completed, deleted"
    return None


# ==============================================
# Input Sanitization
# ==============================================

def sanitize_string(value: str) -> str:
    """
    Sanitize string input.

    Args:
        value: String to sanitize

    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return ""

    # Trim whitespace
    sanitized = value.strip()

    # Remove null bytes and control characters (except newlines/tabs for description)
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)

    return sanitized


def sanitize_sql_like_pattern(pattern: str) -> str:
    """
    Sanitize SQL LIKE pattern to prevent injection.

    Args:
        pattern: Search pattern

    Returns:
        Sanitized pattern
    """
    # Escape SQL LIKE wildcards
    sanitized = pattern.replace('%', '\\%').replace('_', '\\_')
    return sanitized


# ==============================================
# Validation Helper
# ==============================================

def collect_validation_errors(validations: Dict[str, Optional[str]]) -> Dict[str, str]:
    """
    Collect validation errors from validation results.

    Args:
        validations: Dict of field -> error message (None if valid)

    Returns:
        Dict of validation errors (empty if all valid)

    Example:
        >>> errors = collect_validation_errors({
        ...     "user_id": None,  # Valid
        ...     "title": "title is required",  # Invalid
        ...     "priority": None  # Valid
        ... })
        >>> errors
        {"title": "title is required"}
    """
    return {field: error for field, error in validations.items() if error is not None}
