"""
intent_disambiguation Skill

Generates clarification questions when user intent is ambiguous.
Helps resolve situations where multiple tasks match or action is unclear.
"""

from typing import Dict, Any, List
import logging
from .base_skill import BaseSkill

logger = logging.getLogger(__name__)


class IntentDisambiguationSkill(BaseSkill):
    """
    Skill for disambiguating ambiguous user intents.

    Does NOT call MCP tools - generates clarification questions instead.
    """

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate clarification questions for ambiguous intent.

        Args:
            params: Skill input parameters
                - user_input (required): Original user input
                - ambiguity_type (required): Type of ambiguity
                  - "multiple_matches": Multiple tasks match the query
                  - "unclear_action": Action is not clear
                  - "missing_info": Required information is missing
                - context (optional): Additional context
                  - matching_tasks: List of tasks that match (for multiple_matches)
                  - possible_actions: List of possible actions (for unclear_action)
                  - missing_fields: List of missing fields (for missing_info)

        Returns:
            Skill execution result with clarification question

        Example:
            >>> skill = IntentDisambiguationSkill(mcp_client)
            >>> result = await skill.execute({
            ...     "user_input": "complete the meeting task",
            ...     "ambiguity_type": "multiple_matches",
            ...     "context": {
            ...         "matching_tasks": [
            ...             {"id": 1, "title": "Client meeting"},
            ...             {"id": 2, "title": "Team meeting"}
            ...         ]
            ...     }
            ... })
            {
                "success": True,
                "skill": "IntentDisambiguationSkill",
                "data": {
                    "clarification_needed": True,
                    "question": "Which meeting task would you like to complete?",
                    "options": [
                        {"id": 1, "label": "Client meeting"},
                        {"id": 2, "label": "Team meeting"}
                    ]
                }
            }
        """
        logger.info(f"IntentDisambiguationSkill executing with params: {params}")

        # Validate required parameters
        if not params.get("user_input"):
            return self._format_error(
                "MISSING_PARAMETER",
                "user_input is required",
                {"field": "user_input"}
            )

        if not params.get("ambiguity_type"):
            return self._format_error(
                "MISSING_PARAMETER",
                "ambiguity_type is required",
                {"field": "ambiguity_type"}
            )

        ambiguity_type = params["ambiguity_type"]
        context = params.get("context", {})
        user_input = params["user_input"]

        # Generate clarification based on ambiguity type
        if ambiguity_type == "multiple_matches":
            return self._handle_multiple_matches(user_input, context)

        elif ambiguity_type == "unclear_action":
            return self._handle_unclear_action(user_input, context)

        elif ambiguity_type == "missing_info":
            return self._handle_missing_info(user_input, context)

        else:
            return self._format_error(
                "INVALID_AMBIGUITY_TYPE",
                f"Unknown ambiguity_type: {ambiguity_type}",
                {"valid_types": ["multiple_matches", "unclear_action", "missing_info"]}
            )

    def _handle_multiple_matches(
        self,
        user_input: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle multiple matching tasks."""
        matching_tasks = context.get("matching_tasks", [])

        if not matching_tasks:
            return self._format_error(
                "NO_MATCHES_PROVIDED",
                "matching_tasks required for multiple_matches ambiguity"
            )

        options = [
            {"id": task["id"], "label": task["title"]}
            for task in matching_tasks
        ]

        return self._format_success({
            "clarification_needed": True,
            "question": "I found multiple tasks. Which one do you mean?",
            "options": options,
            "user_input": user_input
        })

    def _handle_unclear_action(
        self,
        user_input: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle unclear action."""
        possible_actions = context.get("possible_actions", [
            "create", "update", "complete", "delete", "list"
        ])

        options = [
            {"action": action, "label": action.capitalize()}
            for action in possible_actions
        ]

        return self._format_success({
            "clarification_needed": True,
            "question": "What would you like to do with this task?",
            "options": options,
            "user_input": user_input
        })

    def _handle_missing_info(
        self,
        user_input: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle missing information."""
        missing_fields = context.get("missing_fields", [])

        if not missing_fields:
            return self._format_error(
                "NO_MISSING_FIELDS",
                "missing_fields required for missing_info ambiguity"
            )

        field_labels = {
            "title": "task title",
            "task_id": "which task",
            "due_date": "due date",
            "priority": "priority level"
        }

        questions = [
            f"What is the {field_labels.get(field, field)}?"
            for field in missing_fields
        ]

        return self._format_success({
            "clarification_needed": True,
            "question": " ".join(questions),
            "missing_fields": missing_fields,
            "user_input": user_input
        })
