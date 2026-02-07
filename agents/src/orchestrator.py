"""
Orchestrator Agent

Central coordinator that routes intents to specialized agents.
Manages multi-agent workflows and error handling.
"""

from typing import Dict, Any
import logging
from .base_agent import BaseAgent
from .task_reasoning import TaskReasoningAgent
from .validation_safety import ValidationSafetyAgent
from .response_formatter import ResponseFormatterAgent
from .visual_context import VisualContextAgent

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    """
    Main orchestrator that coordinates all specialized agents.

    Purpose:
    - Receive normalized intent from Interface Orchestrator
    - Route to appropriate specialized agents
    - Validate inputs before operations
    - Format responses via Response Formatter
    - Handle errors from sub-agents
    - Coordinate multi-agent workflows
    """

    def __init__(self, skill_client=None, ai_client=None):
        """Initialize orchestrator with all specialized agents."""
        super().__init__(skill_client, ai_client)

        # Initialize specialized agents
        self.task_reasoning = TaskReasoningAgent(skill_client, ai_client)
        self.validation_safety = ValidationSafetyAgent(skill_client, ai_client)
        self.response_formatter = ResponseFormatterAgent(skill_client, ai_client)
        self.visual_context = VisualContextAgent(skill_client, ai_client)

        logger.info("OrchestratorAgent initialized with all specialized agents")

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate request processing through specialized agents.

        Args:
            inputs: Agent input data
                - intent (required): Normalized intent from Interface Orchestrator
                - user_id (required): User ID
                - modality (required): Input modality

        Returns:
            Final formatted response

        Example:
            >>> orchestrator = OrchestratorAgent(skill_client)
            >>> result = await orchestrator.process({
            ...     "intent": {
            ...         "action": "create_task",
            ...         "parameters": {"title": "Review spec"},
            ...         "confidence": 0.9,
            ...         "modality": "text"
            ...     },
            ...     "user_id": "user_123",
            ...     "modality": "text"
            ... })
            {
                "success": True,
                "agent": "OrchestratorAgent",
                "data": {
                    "message": "✓ Task created: Review spec",
                    "modality": "text"
                }
            }
        """
        logger.info(f"OrchestratorAgent orchestrating request for action: {inputs.get('intent', {}).get('action')}")

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
        user_id = inputs["user_id"]
        modality = inputs.get("modality", "text")
        action = intent.get("action")
        parameters = intent.get("parameters", {})

        # Route based on action
        if action == "process_image":
            return await self._handle_image_processing(parameters, user_id, modality)

        # For task operations, follow the standard workflow:
        # 1. Validate inputs
        # 2. Execute task operation (via Task Reasoning Agent)
        # 3. Format response

        # Step 1: Validate inputs
        validation_result = await self._validate_inputs(parameters, action)
        if not validation_result.get("data", {}).get("valid", False):
            # Validation failed - format and return errors
            formatted_response = await self._format_response(
                validation_result,
                modality,
                action
            )
            return formatted_response

        # Use sanitized data for operations
        sanitized_data = validation_result["data"]["sanitized_data"]

        # Step 2: Execute task operation
        task_inputs = {
            "intent": {
                "action": action,
                "parameters": sanitized_data,
                "confidence": intent.get("confidence", 1.0)
            },
            "user_id": user_id
        }

        operation_result = await self.task_reasoning.process(task_inputs)

        # Step 3: Format response
        formatted_response = await self._format_response(
            operation_result,
            modality,
            action
        )

        return formatted_response

    async def _validate_inputs(
        self,
        data: Dict[str, Any],
        action: str
    ) -> Dict[str, Any]:
        """Validate inputs using Validation & Safety Agent."""
        logger.info(f"OrchestratorAgent validating inputs for action: {action}")

        validation_inputs = {
            "data": data,
            "action": action
        }

        return await self.validation_safety.process(validation_inputs)

    async def _format_response(
        self,
        result: Dict[str, Any],
        modality: str,
        action: str
    ) -> Dict[str, Any]:
        """Format response using Response Formatter Agent."""
        logger.info(f"OrchestratorAgent formatting response for modality: {modality}")

        formatter_inputs = {
            "result": result,
            "modality": modality,
            "action": action
        }

        formatted = await self.response_formatter.process(formatter_inputs)

        # Return the formatted response wrapped in orchestrator's response
        return self._format_success(formatted.get("data", {}))

    async def _handle_image_processing(
        self,
        parameters: Dict[str, Any],
        user_id: str,
        modality: str
    ) -> Dict[str, Any]:
        """Handle image processing through Visual Context Agent."""
        logger.info("OrchestratorAgent handling image processing")

        visual_inputs = {
            "image_data": parameters.get("image_data"),
            "user_id": user_id
        }

        result = await self.visual_context.process(visual_inputs)

        # If image processing succeeds, the extracted data becomes a create_task intent
        if result.get("success") and result.get("data", {}).get("extracted_data"):
            extracted = result["data"]["extracted_data"]

            # Create task with extracted data
            task_params = {
                "user_id": user_id,
                "title": extracted.get("title"),
                "due_date": extracted.get("due_date"),
                "due_time": extracted.get("due_time"),
                "priority": extracted.get("priority"),
            }

            # Validate and create task
            validation_result = await self._validate_inputs(task_params, "create_task")

            if not validation_result.get("data", {}).get("valid", False):
                formatted_response = await self._format_response(
                    validation_result,
                    modality,
                    "create_task"
                )
                return formatted_response

            sanitized_data = validation_result["data"]["sanitized_data"]

            task_inputs = {
                "intent": {
                    "action": "create_task",
                    "parameters": sanitized_data,
                    "confidence": extracted.get("confidence", 0.5)
                },
                "user_id": user_id
            }

            operation_result = await self.task_reasoning.process(task_inputs)
            formatted_response = await self._format_response(
                operation_result,
                modality,
                "create_task"
            )
            return formatted_response

        # Image processing failed
        formatted_response = await self._format_response(
            result,
            modality,
            "process_image"
        )
        return formatted_response
