"""
Task Reasoning Agent

Handles business logic for task operations.
Parses natural language and invokes appropriate task management skills.
"""

from typing import Dict, Any
import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class TaskReasoningAgent(BaseAgent):
    """
    Agent responsible for task management operations.

    Purpose:
    - Parse natural language for task details
    - Extract dates/times, priorities, statuses
    - Invoke appropriate task skills
    - Handle ambiguous requests with disambiguation
    """

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process task operation intent.

        Args:
            inputs: Agent input data
                - intent (required): Normalized intent from Interface Orchestrator
                  - action: create_task | list_tasks | update_task | complete_task | delete_task
                  - parameters: Action-specific parameters
                  - confidence: Confidence score
                - user_id (required): User ID

        Returns:
            Task operation result

        Example:
            >>> agent = TaskReasoningAgent(skill_client)
            >>> result = await agent.process({
            ...     "intent": {
            ...         "action": "create_task",
            ...         "parameters": {"title": "Review spec", "due_date": "2025-12-28"},
            ...         "confidence": 0.9
            ...     },
            ...     "user_id": "user_123"
            ... })
            {
                "success": True,
                "agent": "TaskReasoningAgent",
                "data": {
                    "task": {...},
                    "message": "Task created: Review spec"
                }
            }
        """
        logger.info(f"TaskReasoningAgent processing intent: {inputs.get('intent', {}).get('action')}")

        # Validate required inputs
        if not inputs.get("intent"):
            return self._format_error(
                "MISSING_INPUT",
                "intent is required",
                {"field": "intent"}
            )

        if not inputs.get("user_id"):
            return self._format_error(
                "MISSING_INPUT",
                "user_id is required",
                {"field": "user_id"}
            )

        intent = inputs["intent"]
        action = intent.get("action")
        parameters = intent.get("parameters", {})
        confidence = intent.get("confidence", 0.0)
        user_id = inputs["user_id"]

        # Ensure user_id is in parameters
        parameters["user_id"] = user_id

        # Check if disambiguation is needed (low confidence or missing key info)
        if confidence < 0.5 or self._needs_disambiguation(action, parameters):
            return await self._handle_disambiguation(action, parameters, intent)

        # Route to appropriate skill based on action
        if action == "create_task":
            return await self._handle_create_task(parameters)

        elif action == "list_tasks":
            return await self._handle_list_tasks(parameters)

        elif action == "update_task":
            return await self._handle_update_task(parameters)

        elif action == "complete_task":
            return await self._handle_complete_task(parameters)

        elif action == "delete_task":
            return await self._handle_delete_task(parameters)

        else:
            return self._format_error(
                "UNKNOWN_ACTION",
                f"Unknown action: {action}",
                {"action": action}
            )

    async def _handle_create_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle task creation."""
        logger.info("TaskReasoningAgent creating task")

        result = await self.skill_client.create_task(parameters)

        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        return self._format_success(result["data"])

    async def _handle_list_tasks(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle task listing."""
        logger.info("TaskReasoningAgent listing tasks")

        result = await self.skill_client.list_tasks(parameters)

        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        return self._format_success(result["data"])

    async def _handle_update_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle task update."""
        logger.info("TaskReasoningAgent updating task")

        # Check if we have a task_id or need to search by title
        if not parameters.get("task_id") and parameters.get("title_reference"):
            # Need to find task by title first
            search_result = await self.skill_client.list_tasks({
                "user_id": parameters["user_id"],
                "filters": {"search": parameters["title_reference"]},
                "limit": 5
            })

            if not search_result.get("success"):
                return self._format_error(
                    search_result["error"]["code"],
                    search_result["error"]["message"],
                    search_result["error"].get("details")
                )

            tasks = search_result["data"]["tasks"]

            if len(tasks) == 0:
                return self._format_error(
                    "TASK_NOT_FOUND",
                    f"No tasks found matching '{parameters['title_reference']}'",
                    {"search_term": parameters["title_reference"]}
                )

            if len(tasks) > 1:
                # Need disambiguation
                return await self._handle_disambiguation(
                    "update_task",
                    parameters,
                    {"user_input": parameters.get("title_reference")},
                    matching_tasks=tasks
                )

            # Use the found task
            parameters["task_id"] = tasks[0]["task_id"]

        result = await self.skill_client.update_task(parameters)

        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        return self._format_success(result["data"])

    async def _handle_complete_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle task completion."""
        logger.info("TaskReasoningAgent completing task")

        # Check if we have a task_id or need to search by title
        if not parameters.get("task_id") and parameters.get("title_reference"):
            # Need to find task by title first
            search_result = await self.skill_client.list_tasks({
                "user_id": parameters["user_id"],
                "filters": {"search": parameters["title_reference"]},
                "limit": 5
            })

            if not search_result.get("success"):
                return self._format_error(
                    search_result["error"]["code"],
                    search_result["error"]["message"],
                    search_result["error"].get("details")
                )

            tasks = search_result["data"]["tasks"]

            if len(tasks) == 0:
                return self._format_error(
                    "TASK_NOT_FOUND",
                    f"No tasks found matching '{parameters['title_reference']}'",
                    {"search_term": parameters["title_reference"]}
                )

            if len(tasks) > 1:
                # Need disambiguation
                return await self._handle_disambiguation(
                    "complete_task",
                    parameters,
                    {"user_input": parameters.get("title_reference")},
                    matching_tasks=tasks
                )

            # Use the found task
            parameters["task_id"] = tasks[0]["task_id"]

        result = await self.skill_client.complete_task(parameters)

        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        return self._format_success(result["data"])

    async def _handle_delete_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle task deletion."""
        logger.info("TaskReasoningAgent deleting task")

        # Check if we have a task_id or need to search by title
        if not parameters.get("task_id") and parameters.get("title_reference"):
            # Need to find task by title first
            search_result = await self.skill_client.list_tasks({
                "user_id": parameters["user_id"],
                "filters": {"search": parameters["title_reference"]},
                "limit": 5
            })

            if not search_result.get("success"):
                return self._format_error(
                    search_result["error"]["code"],
                    search_result["error"]["message"],
                    search_result["error"].get("details")
                )

            tasks = search_result["data"]["tasks"]

            if len(tasks) == 0:
                return self._format_error(
                    "TASK_NOT_FOUND",
                    f"No tasks found matching '{parameters['title_reference']}'",
                    {"search_term": parameters["title_reference"]}
                )

            if len(tasks) > 1:
                # Need disambiguation
                return await self._handle_disambiguation(
                    "delete_task",
                    parameters,
                    {"user_input": parameters.get("title_reference")},
                    matching_tasks=tasks
                )

            # Use the found task
            parameters["task_id"] = tasks[0]["task_id"]

        result = await self.skill_client.delete_task(parameters)

        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        return self._format_success(result["data"])

    def _needs_disambiguation(self, action: str, parameters: Dict[str, Any]) -> bool:
        """Check if action needs disambiguation."""
        # If we have a title_reference but no task_id, we might need disambiguation
        if action in ["update_task", "complete_task", "delete_task"]:
            if not parameters.get("task_id") and parameters.get("title_reference"):
                return True

        # If creating task but title is missing or very short
        if action == "create_task":
            title = parameters.get("title", "")
            if not title or len(title.strip()) < 3:
                return True

        return False

    async def _handle_disambiguation(
        self,
        action: str,
        parameters: Dict[str, Any],
        intent: Dict[str, Any],
        matching_tasks: list = None
    ) -> Dict[str, Any]:
        """Handle disambiguation by calling intent_disambiguation skill."""
        logger.info("TaskReasoningAgent requesting disambiguation")

        disambig_params = {
            "user_input": intent.get("user_input", ""),
            "ambiguity_type": "multiple_matches" if matching_tasks else "missing_info",
            "context": {}
        }

        if matching_tasks:
            disambig_params["context"]["matching_tasks"] = matching_tasks
        else:
            # Determine missing fields
            missing_fields = []
            if action == "create_task" and not parameters.get("title"):
                missing_fields.append("title")
            elif action in ["update_task", "complete_task", "delete_task"] and not parameters.get("task_id"):
                missing_fields.append("task_id")

            disambig_params["context"]["missing_fields"] = missing_fields

        result = await self.skill_client.disambiguate_intent(disambig_params)

        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        return self._format_success(result["data"])
