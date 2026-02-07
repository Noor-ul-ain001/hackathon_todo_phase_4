"""
ui_intent_normalization Skill

Normalizes input from different modalities into structured intents.
Handles CLI commands, natural language, voice transcripts, and image data.
"""

from typing import Dict, Any, Optional
import logging
import re
from datetime import datetime, timedelta
from .base_skill import BaseSkill

logger = logging.getLogger(__name__)


class UIIntentNormalizationSkill(BaseSkill):
    """
    Skill for normalizing UI inputs to structured intents.

    Supports:
    - CLI commands: "todo add 'Task title' --due tomorrow"
    - Natural language: "Create a high priority task for the meeting tomorrow at 3pm"
    - Voice transcripts: Similar to natural language but with voice-specific handling
    - Image data: Passed to Visual Context Agent (handled separately)
    """

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize input to structured intent.

        Args:
            params: Skill input parameters
                - raw_input (required): User's raw input (text or transcribed voice)
                - modality (required): Input modality (text | voice | image)
                - input_type (required): Type of input (cli_command | natural_language | image_data)
                - user_id (required): User ID

        Returns:
            Skill execution result with normalized intent

        Example:
            >>> skill = UIIntentNormalizationSkill(mcp_client)
            >>> result = await skill.execute({
            ...     "raw_input": "todo add 'Review spec' --due tomorrow --priority high",
            ...     "modality": "text",
            ...     "input_type": "cli_command",
            ...     "user_id": "user_123"
            ... })
            {
                "success": True,
                "skill": "UIIntentNormalizationSkill",
                "data": {
                    "intent": {
                        "action": "create_task",
                        "parameters": {
                            "user_id": "user_123",
                            "title": "Review spec",
                            "due_date": "2025-12-28",
                            "priority": "high"
                        },
                        "confidence": 1.0,
                        "modality": "text"
                    }
                }
            }
        """
        logger.info(f"UIIntentNormalizationSkill executing with params: {params}")

        # Validate required parameters
        if not params.get("raw_input") and params.get("input_type") != "image_data":
            return self._format_error(
                "MISSING_PARAMETER",
                "raw_input is required for text/voice modality",
                {"field": "raw_input"}
            )

        if not params.get("modality"):
            return self._format_error(
                "MISSING_PARAMETER",
                "modality is required",
                {"field": "modality"}
            )

        if not params.get("input_type"):
            return self._format_error(
                "MISSING_PARAMETER",
                "input_type is required",
                {"field": "input_type"}
            )

        if not params.get("user_id"):
            return self._format_error(
                "MISSING_PARAMETER",
                "user_id is required",
                {"field": "user_id"}
            )

        modality = params["modality"]
        input_type = params["input_type"]
        raw_input = params.get("raw_input", "")
        user_id = params["user_id"]

        # Route to appropriate parser
        if input_type == "cli_command":
            intent = self._parse_cli_command(raw_input, user_id)
        elif input_type == "natural_language":
            intent = self._parse_natural_language(raw_input, user_id, modality)
        elif input_type == "image_data":
            # Image data is handled by Visual Context Agent, not here
            return self._format_error(
                "UNSUPPORTED_INPUT_TYPE",
                "Image data should be processed by Visual Context Agent",
                {"input_type": input_type}
            )
        else:
            return self._format_error(
                "INVALID_INPUT_TYPE",
                f"Unknown input_type: {input_type}",
                {"valid_types": ["cli_command", "natural_language", "image_data"]}
            )

        # Add modality to intent
        intent["modality"] = modality

        return self._format_success({"intent": intent})

    def _parse_cli_command(self, command: str, user_id: str) -> Dict[str, Any]:
        """
        Parse CLI command into structured intent.

        Examples:
            - "todo add 'Task title' --due tomorrow --priority high"
            - "todo list --status pending"
            - "todo complete 42"
            - "todo update 42 --priority high --status in_progress"
            - "todo delete 42"
        """
        command = command.strip()

        # Extract action
        action_patterns = {
            r"^todo\s+add": "create_task",
            r"^todo\s+create": "create_task",
            r"^todo\s+list": "list_tasks",
            r"^todo\s+ls": "list_tasks",
            r"^todo\s+complete": "complete_task",
            r"^todo\s+done": "complete_task",
            r"^todo\s+update": "update_task",
            r"^todo\s+edit": "update_task",
            r"^todo\s+delete": "delete_task",
            r"^todo\s+remove": "delete_task",
        }

        action = None
        for pattern, act in action_patterns.items():
            if re.match(pattern, command, re.IGNORECASE):
                action = act
                break

        if not action:
            return {
                "action": "unknown",
                "parameters": {"user_id": user_id},
                "confidence": 0.0,
                "error": "Could not parse command"
            }

        # Extract parameters based on action
        parameters = {"user_id": user_id}

        if action == "create_task":
            # Extract title (quoted string)
            title_match = re.search(r"['\"]([^'\"]+)['\"]", command)
            if title_match:
                parameters["title"] = title_match.group(1)

            # Extract flags
            parameters.update(self._extract_flags(command))

        elif action == "list_tasks":
            # Extract filter flags
            parameters["filters"] = self._extract_filters(command)

        elif action in ["complete_task", "delete_task"]:
            # Extract task_id (number after action)
            task_id_match = re.search(r"(?:complete|done|delete|remove)\s+(\d+)", command, re.IGNORECASE)
            if task_id_match:
                parameters["task_id"] = int(task_id_match.group(1))

        elif action == "update_task":
            # Extract task_id
            task_id_match = re.search(r"(?:update|edit)\s+(\d+)", command, re.IGNORECASE)
            if task_id_match:
                parameters["task_id"] = int(task_id_match.group(1))

            # Extract updates
            parameters["updates"] = self._extract_flags(command)

        return {
            "action": action,
            "parameters": parameters,
            "confidence": 1.0  # CLI commands are deterministic
        }

    def _extract_flags(self, command: str) -> Dict[str, Any]:
        """Extract --flag value pairs from command."""
        flags = {}

        # --due DATE
        due_match = re.search(r"--due\s+(\S+)", command, re.IGNORECASE)
        if due_match:
            flags["due_date"] = self._parse_date(due_match.group(1))

        # --time TIME
        time_match = re.search(r"--time\s+(\S+)", command, re.IGNORECASE)
        if time_match:
            flags["due_time"] = time_match.group(1)

        # --priority PRIORITY
        priority_match = re.search(r"--priority\s+(\S+)", command, re.IGNORECASE)
        if priority_match:
            flags["priority"] = priority_match.group(1).lower()

        # --status STATUS
        status_match = re.search(r"--status\s+(\S+)", command, re.IGNORECASE)
        if status_match:
            flags["status"] = status_match.group(1).replace("-", "_").lower()

        # --description "TEXT"
        desc_match = re.search(r"--description\s+['\"]([^'\"]+)['\"]", command, re.IGNORECASE)
        if desc_match:
            flags["description"] = desc_match.group(1)

        return flags

    def _extract_filters(self, command: str) -> Dict[str, Any]:
        """Extract filter flags from list command."""
        filters = {}

        # --status STATUS
        status_match = re.search(r"--status\s+(\S+)", command, re.IGNORECASE)
        if status_match:
            filters["status"] = status_match.group(1).replace("-", "_").lower()

        # --priority PRIORITY
        priority_match = re.search(r"--priority\s+(\S+)", command, re.IGNORECASE)
        if priority_match:
            filters["priority"] = priority_match.group(1).lower()

        # --search "QUERY"
        search_match = re.search(r"--search\s+['\"]([^'\"]+)['\"]", command, re.IGNORECASE)
        if search_match:
            filters["search"] = search_match.group(1)

        return filters

    def _parse_natural_language(
        self,
        text: str,
        user_id: str,
        modality: str
    ) -> Dict[str, Any]:
        """
        Parse natural language into structured intent.

        Examples:
            - "Create a task to review the architecture spec tomorrow"
            - "Show me all high priority tasks"
            - "Mark task 42 as complete"
            - "Delete the meeting task"
        """
        text = text.strip().lower()

        # Detect action
        action = self._detect_action(text)

        if action == "unknown":
            return {
                "action": "unknown",
                "parameters": {"user_id": user_id},
                "confidence": 0.0,
                "error": "Could not understand intent"
            }

        # Extract parameters based on action
        parameters = {"user_id": user_id}
        confidence = 0.7  # Natural language has lower confidence than CLI

        if action == "create_task":
            # Extract title (everything after action words, before time/priority keywords)
            title = self._extract_title(text)
            if title:
                parameters["title"] = title
                confidence = 0.9

            # Extract due date/time
            due_info = self._extract_due_info(text)
            parameters.update(due_info)

            # Extract priority
            priority = self._extract_priority(text)
            if priority:
                parameters["priority"] = priority

        elif action == "list_tasks":
            # Extract filters
            parameters["filters"] = self._extract_nl_filters(text)

        elif action in ["complete_task", "delete_task"]:
            # Extract task_id or title reference
            task_id = self._extract_task_id(text)
            if task_id:
                parameters["task_id"] = task_id
            else:
                # Need disambiguation - title reference
                parameters["title_reference"] = self._extract_title_reference(text)

        elif action == "update_task":
            # Extract task_id
            task_id = self._extract_task_id(text)
            if task_id:
                parameters["task_id"] = task_id

            # Extract updates
            updates = {}
            priority = self._extract_priority(text)
            if priority:
                updates["priority"] = priority

            due_info = self._extract_due_info(text)
            updates.update(due_info)

            parameters["updates"] = updates

        return {
            "action": action,
            "parameters": parameters,
            "confidence": confidence
        }

    def _detect_action(self, text: str) -> str:
        """Detect action from natural language."""
        create_patterns = [
            "create", "add", "new task", "make a task", "schedule", "plan"
        ]
        list_patterns = [
            "show", "list", "display", "view", "see", "find", "search"
        ]
        complete_patterns = [
            "complete", "done", "finish", "mark as done", "mark complete"
        ]
        delete_patterns = [
            "delete", "remove", "cancel", "get rid of"
        ]
        update_patterns = [
            "update", "change", "modify", "edit", "set priority", "reschedule"
        ]

        for pattern in create_patterns:
            if pattern in text:
                return "create_task"

        for pattern in complete_patterns:
            if pattern in text:
                return "complete_task"

        for pattern in delete_patterns:
            if pattern in text:
                return "delete_task"

        for pattern in update_patterns:
            if pattern in text:
                return "update_task"

        for pattern in list_patterns:
            if pattern in text:
                return "list_tasks"

        return "unknown"

    def _extract_title(self, text: str) -> Optional[str]:
        """Extract task title from natural language."""
        # Remove action words
        for word in ["create", "add", "new", "task", "to", "a"]:
            text = text.replace(word, " ")

        # Remove time/priority keywords
        for word in ["tomorrow", "today", "high", "priority", "urgent", "low", "medium"]:
            text = text.replace(word, " ")

        # Clean up
        title = " ".join(text.split())
        return title if title else None

    def _extract_due_info(self, text: str) -> Dict[str, Any]:
        """Extract due date and time from natural language."""
        info = {}

        # Date patterns
        if "tomorrow" in text:
            tomorrow = datetime.now() + timedelta(days=1)
            info["due_date"] = tomorrow.strftime("%Y-%m-%d")
        elif "today" in text:
            info["due_date"] = datetime.now().strftime("%Y-%m-%d")
        elif "next week" in text:
            next_week = datetime.now() + timedelta(days=7)
            info["due_date"] = next_week.strftime("%Y-%m-%d")

        # Time patterns
        time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text, re.IGNORECASE)
        if time_match:
            hour = int(time_match.group(1))
            minute = time_match.group(2) or "00"
            am_pm = time_match.group(3)

            if am_pm and am_pm.lower() == "pm" and hour < 12:
                hour += 12
            elif am_pm and am_pm.lower() == "am" and hour == 12:
                hour = 0

            info["due_time"] = f"{hour:02d}:{minute}"

        return info

    def _extract_priority(self, text: str) -> Optional[str]:
        """Extract priority from natural language."""
        if any(word in text for word in ["urgent", "asap", "high priority", "critical", "important"]):
            return "high"
        elif any(word in text for word in ["low priority", "someday", "maybe", "later"]):
            return "low"
        elif "medium" in text or "normal" in text:
            return "medium"
        return None

    def _extract_nl_filters(self, text: str) -> Dict[str, Any]:
        """Extract filters from natural language list query."""
        filters = {}

        if "high priority" in text or "urgent" in text:
            filters["priority"] = "high"
        elif "low priority" in text:
            filters["priority"] = "low"

        if "pending" in text or "incomplete" in text or "not done" in text:
            filters["status"] = "pending"
        elif "completed" in text or "done" in text:
            filters["status"] = "completed"
        elif "in progress" in text or "working on" in text:
            filters["status"] = "in_progress"

        return filters

    def _extract_task_id(self, text: str) -> Optional[int]:
        """Extract task ID from text."""
        task_id_match = re.search(r"task\s+(\d+)|#(\d+)", text)
        if task_id_match:
            return int(task_id_match.group(1) or task_id_match.group(2))
        return None

    def _extract_title_reference(self, text: str) -> Optional[str]:
        """Extract task title reference for disambiguation."""
        # Remove action words
        for word in ["complete", "delete", "the", "task"]:
            text = text.replace(word, " ")
        return " ".join(text.split())

    def _parse_date(self, date_str: str) -> str:
        """Parse date string (tomorrow, today, YYYY-MM-DD)."""
        date_str = date_str.lower()

        if date_str == "tomorrow":
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_str == "today":
            return datetime.now().strftime("%Y-%m-%d")
        elif date_str == "next-week" or date_str == "nextweek":
            return (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        else:
            return date_str  # Assume it's already in ISO format
