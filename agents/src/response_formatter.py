"""
Response Formatter Agent

Converts technical results to user-friendly messages.
Adapts formatting based on modality (text vs voice).
"""

from typing import Dict, Any
import logging
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ResponseFormatterAgent(BaseAgent):
    """
    Agent responsible for formatting responses for users.

    Purpose:
    - Format success messages
    - Humanize error messages
    - Adapt formatting based on modality
    - Format dates and times naturally
    """

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format response for user.

        Args:
            inputs: Agent input data
                - result (required): Operation result to format
                - modality (required): Output modality (text | voice)
                - action (optional): Action that was performed

        Returns:
            Formatted response message

        Example:
            >>> agent = ResponseFormatterAgent()
            >>> result = await agent.process({
            ...     "result": {"task": {"title": "Review spec", "due_date": "2025-12-28"}},
            ...     "modality": "text",
            ...     "action": "create_task"
            ... })
            {
                "success": True,
                "agent": "ResponseFormatterAgent",
                "data": {
                    "message": "✓ Task created: Review spec (Due: Dec 28)"
                }
            }
        """
        logger.info(f"ResponseFormatterAgent formatting for modality: {inputs.get('modality')}")

        # Validate required inputs
        if not inputs.get("result"):
            return self._format_error(
                "MISSING_INPUT",
                "result is required for formatting",
                {"field": "result"}
            )

        if not inputs.get("modality"):
            return self._format_error(
                "MISSING_INPUT",
                "modality is required for formatting",
                {"field": "modality"}
            )

        result = inputs["result"]
        modality = inputs["modality"]
        action = inputs.get("action", "unknown")

        # Format based on whether result is success or error
        if result.get("success"):
            message = self._format_success_message(result, action, modality)
        else:
            message = self._format_error_message(result, modality)

        return self._format_success({
            "message": message,
            "modality": modality
        })

    def _format_success_message(
        self,
        result: Dict[str, Any],
        action: str,
        modality: str
    ) -> str:
        """Format success message based on action and modality."""
        data = result.get("data", {})

        if action == "create_task":
            return self._format_task_created(data, modality)

        elif action == "list_tasks":
            return self._format_task_list(data, modality)

        elif action == "update_task":
            return self._format_task_updated(data, modality)

        elif action == "complete_task":
            return self._format_task_completed(data, modality)

        elif action == "delete_task":
            return self._format_task_deleted(data, modality)

        else:
            # Generic success message
            return data.get("message", "Operation completed successfully")

    def _format_task_created(self, data: Dict[str, Any], modality: str) -> str:
        """Format task creation success message."""
        task = data.get("task", {})
        title = task.get("title", "Unnamed task")

        if modality == "voice":
            # Concise for voice
            return f"Task created: {title}"

        # Detailed for text
        message = f"✓ Task created: {title}"

        # Add due date if present
        due_date = task.get("due_date")
        due_time = task.get("due_time")
        if due_date:
            formatted_date = self._format_date(due_date)
            if due_time:
                message += f" (Due: {formatted_date} at {due_time})"
            else:
                message += f" (Due: {formatted_date})"

        # Add priority if not medium
        priority = task.get("priority", "medium")
        if priority != "medium":
            message += f" [{priority.upper()} priority]"

        return message

    def _format_task_list(self, data: Dict[str, Any], modality: str) -> str:
        """Format task list success message."""
        tasks = data.get("tasks", [])
        count = len(tasks)

        if count == 0:
            return "No tasks found"

        if modality == "voice":
            # Concise for voice
            if count == 1:
                return f"Found 1 task: {tasks[0]['title']}"
            else:
                return f"Found {count} tasks. Showing first 3: " + ", ".join(
                    [task['title'] for task in tasks[:3]]
                )

        # Detailed for text
        message = f"📋 Found {count} task(s):\n\n"

        for i, task in enumerate(tasks[:10], 1):  # Show max 10 in text
            title = task.get("title", "Unnamed")
            status = task.get("status", "pending")
            priority = task.get("priority", "medium")
            due_date = task.get("due_date")

            status_emoji = {
                "pending": "⏳",
                "in_progress": "🔄",
                "completed": "✅",
                "deleted": "🗑️"
            }.get(status, "•")

            line = f"{i}. {status_emoji} {title}"

            if due_date:
                line += f" (Due: {self._format_date(due_date)})"

            if priority != "medium":
                line += f" [{priority.upper()}]"

            message += line + "\n"

        if count > 10:
            message += f"\n... and {count - 10} more"

        return message

    def _format_task_updated(self, data: Dict[str, Any], modality: str) -> str:
        """Format task update success message."""
        task = data.get("task", {})
        updated_fields = data.get("updated_fields", [])
        title = task.get("title", "Task")

        if modality == "voice":
            return f"Updated {title}: {', '.join(updated_fields)}"

        return f"✓ Task updated: {title}\nUpdated fields: {', '.join(updated_fields)}"

    def _format_task_completed(self, data: Dict[str, Any], modality: str) -> str:
        """Format task completion success message."""
        task = data.get("task", {})
        title = task.get("title", "Task")

        if modality == "voice":
            return f"Completed: {title}"

        return f"✅ Task completed: {title}"

    def _format_task_deleted(self, data: Dict[str, Any], modality: str) -> str:
        """Format task deletion success message."""
        if modality == "voice":
            return "Task deleted"

        return "🗑️ Task deleted successfully"

    def _format_error_message(self, result: Dict[str, Any], modality: str) -> str:
        """Format error message based on modality."""
        error = result.get("error", {})
        code = error.get("code", "UNKNOWN_ERROR")
        message = error.get("message", "An error occurred")
        details = error.get("details", {})

        # Humanize error code
        humanized = self._humanize_error_code(code, message, details)

        if modality == "voice":
            # Concise for voice
            return f"Error: {humanized}"

        # Detailed for text
        error_msg = f"❌ {humanized}"

        # Add details if present and it's a validation error
        if code == "VALIDATION_ERROR" and isinstance(details, dict):
            error_msg += "\n\nValidation errors:"
            for field, field_error in details.items():
                error_msg += f"\n• {field}: {field_error}"

        return error_msg

    def _humanize_error_code(self, code: str, message: str, details: Any) -> str:
        """Humanize error code to user-friendly message."""
        # Map common error codes to friendly messages
        error_map = {
            "VALIDATION_ERROR": "Invalid input",
            "UNAUTHORIZED": "You don't have permission to access this task",
            "TASK_NOT_FOUND": "Task not found",
            "DATABASE_ERROR": "Database error occurred",
            "MCP_CLIENT_ERROR": "Service temporarily unavailable",
            "MISSING_PARAMETER": f"Missing required field: {details.get('field', 'unknown') if isinstance(details, dict) else 'unknown'}",
        }

        return error_map.get(code, message)

    def _format_date(self, date_str: str) -> str:
        """Format ISO date to natural language."""
        try:
            date_obj = datetime.fromisoformat(date_str)
            today = datetime.now().date()
            date_only = date_obj.date()

            if date_only == today:
                return "Today"
            elif date_only == today.replace(day=today.day + 1):
                return "Tomorrow"
            elif date_only == today.replace(day=today.day - 1):
                return "Yesterday"
            else:
                return date_obj.strftime("%b %d")

        except Exception:
            return date_str
