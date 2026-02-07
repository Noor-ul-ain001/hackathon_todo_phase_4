"""
Validation & Safety Agent

Validates all inputs and enforces business rules.
Ensures data quality and security before operations.
"""

from typing import Dict, Any, List
import logging
import re
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ValidationSafetyAgent(BaseAgent):
    """
    Agent responsible for validation and safety checks.

    Purpose:
    - Validate required fields
    - Check data types and formats
    - Enforce length constraints
    - Sanitize inputs
    - Return comprehensive error lists
    """

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input data.

        Args:
            inputs: Agent input data
                - data (required): Data to validate
                - validation_rules (optional): Specific rules to apply
                - action (required): Action being performed (for context)

        Returns:
            Validation result with errors if any

        Example:
            >>> agent = ValidationSafetyAgent()
            >>> result = await agent.process({
            ...     "data": {"user_id": "user_123", "title": "Review spec"},
            ...     "action": "create_task"
            ... })
            {
                "success": True,
                "agent": "ValidationSafetyAgent",
                "data": {
                    "valid": True,
                    "sanitized_data": {...}
                }
            }
        """
        logger.info(f"ValidationSafetyAgent validating for action: {inputs.get('action')}")

        # Validate required inputs
        if not inputs.get("data"):
            return self._format_error(
                "MISSING_INPUT",
                "data is required for validation",
                {"field": "data"}
            )

        if not inputs.get("action"):
            return self._format_error(
                "MISSING_INPUT",
                "action is required for validation",
                {"field": "action"}
            )

        data = inputs["data"]
        action = inputs["action"]

        # Collect all validation errors
        errors = []

        # Validate based on action
        if action == "create_task":
            errors.extend(self._validate_create_task(data))
        elif action == "update_task":
            errors.extend(self._validate_update_task(data))
        elif action in ["complete_task", "delete_task"]:
            errors.extend(self._validate_task_operation(data))
        elif action == "list_tasks":
            errors.extend(self._validate_list_tasks(data))

        # If there are validation errors, return them
        if errors:
            return self._format_success({
                "valid": False,
                "errors": errors
            })

        # Sanitize data
        sanitized_data = self._sanitize_data(data)

        # All validation passed
        return self._format_success({
            "valid": True,
            "sanitized_data": sanitized_data,
            "errors": []
        })

    def _validate_create_task(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Validate create_task data."""
        errors = []

        # Required: user_id
        if not data.get("user_id"):
            errors.append({"field": "user_id", "message": "user_id is required"})
        elif not isinstance(data["user_id"], str) or not data["user_id"].strip():
            errors.append({"field": "user_id", "message": "user_id must be a non-empty string"})

        # Required: title
        if not data.get("title"):
            errors.append({"field": "title", "message": "title is required"})
        elif not isinstance(data["title"], str):
            errors.append({"field": "title", "message": "title must be a string"})
        elif not data["title"].strip():
            errors.append({"field": "title", "message": "title cannot be empty"})
        elif len(data["title"]) > 200:
            errors.append({"field": "title", "message": "title cannot exceed 200 characters"})

        # Optional: description
        if "description" in data and data["description"]:
            if not isinstance(data["description"], str):
                errors.append({"field": "description", "message": "description must be a string"})
            elif len(data["description"]) > 2000:
                errors.append({"field": "description", "message": "description cannot exceed 2000 characters"})

        # Optional: due_date
        if "due_date" in data and data["due_date"]:
            if not self._is_valid_date(data["due_date"]):
                errors.append({"field": "due_date", "message": "due_date must be in ISO 8601 format (YYYY-MM-DD)"})

        # Optional: due_time
        if "due_time" in data and data["due_time"]:
            if not self._is_valid_time(data["due_time"]):
                errors.append({"field": "due_time", "message": "due_time must be in HH:MM format"})

        # Optional: priority
        if "priority" in data and data["priority"]:
            if data["priority"] not in ["low", "medium", "high"]:
                errors.append({"field": "priority", "message": "priority must be one of: low, medium, high"})

        # Optional: status
        if "status" in data and data["status"]:
            if data["status"] not in ["pending", "in_progress", "completed"]:
                errors.append({"field": "status", "message": "status must be one of: pending, in_progress, completed"})

        return errors

    def _validate_update_task(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Validate update_task data."""
        errors = []

        # Required: user_id
        if not data.get("user_id"):
            errors.append({"field": "user_id", "message": "user_id is required"})

        # Required: task_id
        if not data.get("task_id"):
            errors.append({"field": "task_id", "message": "task_id is required"})
        elif not isinstance(data["task_id"], int) or data["task_id"] <= 0:
            errors.append({"field": "task_id", "message": "task_id must be a positive integer"})

        # Required: updates
        if not data.get("updates"):
            errors.append({"field": "updates", "message": "updates object is required"})
        elif not isinstance(data["updates"], dict):
            errors.append({"field": "updates", "message": "updates must be an object"})
        elif len(data["updates"]) == 0:
            errors.append({"field": "updates", "message": "updates must contain at least one field"})
        else:
            # Validate update fields
            updates = data["updates"]

            if "title" in updates:
                if not updates["title"] or not updates["title"].strip():
                    errors.append({"field": "updates.title", "message": "title cannot be empty"})
                elif len(updates["title"]) > 200:
                    errors.append({"field": "updates.title", "message": "title cannot exceed 200 characters"})

            if "description" in updates and updates["description"] is not None:
                if len(updates["description"]) > 2000:
                    errors.append({"field": "updates.description", "message": "description cannot exceed 2000 characters"})

            if "due_date" in updates and updates["due_date"]:
                if not self._is_valid_date(updates["due_date"]):
                    errors.append({"field": "updates.due_date", "message": "due_date must be in ISO 8601 format"})

            if "due_time" in updates and updates["due_time"]:
                if not self._is_valid_time(updates["due_time"]):
                    errors.append({"field": "updates.due_time", "message": "due_time must be in HH:MM format"})

            if "priority" in updates and updates["priority"]:
                if updates["priority"] not in ["low", "medium", "high"]:
                    errors.append({"field": "updates.priority", "message": "priority must be low, medium, or high"})

            if "status" in updates and updates["status"]:
                if updates["status"] not in ["pending", "in_progress", "completed", "deleted"]:
                    errors.append({"field": "updates.status", "message": "status must be pending, in_progress, completed, or deleted"})

        return errors

    def _validate_task_operation(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Validate task operation (complete/delete)."""
        errors = []

        # Required: user_id
        if not data.get("user_id"):
            errors.append({"field": "user_id", "message": "user_id is required"})

        # Required: task_id
        if not data.get("task_id"):
            errors.append({"field": "task_id", "message": "task_id is required"})
        elif not isinstance(data["task_id"], int) or data["task_id"] <= 0:
            errors.append({"field": "task_id", "message": "task_id must be a positive integer"})

        return errors

    def _validate_list_tasks(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Validate list_tasks data."""
        errors = []

        # Required: user_id
        if not data.get("user_id"):
            errors.append({"field": "user_id", "message": "user_id is required"})

        # Optional: filters
        if "filters" in data and data["filters"]:
            filters = data["filters"]
            if not isinstance(filters, dict):
                errors.append({"field": "filters", "message": "filters must be an object"})
            else:
                if "status" in filters and filters["status"]:
                    if filters["status"] not in ["pending", "in_progress", "completed", "deleted"]:
                        errors.append({"field": "filters.status", "message": "status must be pending, in_progress, completed, or deleted"})

                if "priority" in filters and filters["priority"]:
                    if filters["priority"] not in ["low", "medium", "high"]:
                        errors.append({"field": "filters.priority", "message": "priority must be low, medium, or high"})

                if "due_before" in filters and filters["due_before"]:
                    if not self._is_valid_date(filters["due_before"]):
                        errors.append({"field": "filters.due_before", "message": "due_before must be in ISO 8601 format"})

                if "due_after" in filters and filters["due_after"]:
                    if not self._is_valid_date(filters["due_after"]):
                        errors.append({"field": "filters.due_after", "message": "due_after must be in ISO 8601 format"})

        return errors

    def _is_valid_date(self, date_str: str) -> bool:
        """Check if string is a valid ISO 8601 date."""
        try:
            datetime.fromisoformat(date_str)
            return True
        except ValueError:
            return False

    def _is_valid_time(self, time_str: str) -> bool:
        """Check if string is a valid HH:MM time."""
        pattern = r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
        return bool(re.match(pattern, time_str))

    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input data."""
        sanitized = {}

        for key, value in data.items():
            if isinstance(value, str):
                # Trim whitespace
                value = value.strip()
                # Remove null bytes and control characters
                value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)

            sanitized[key] = value

        return sanitized
