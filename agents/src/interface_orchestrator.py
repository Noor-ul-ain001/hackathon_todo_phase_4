"""
Interface Orchestrator Agent

First point of contact; normalizes all inputs to structured intents.
Detects modality and invokes ui_intent_normalization skill.
"""

from typing import Dict, Any
import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class InterfaceOrchestratorAgent(BaseAgent):
    """
    Agent responsible for normalizing user inputs from all modalities.

    Purpose:
    - Detect input modality (text, voice, image)
    - Invoke ui_intent_normalization skill
    - Pass normalized intent to main Orchestrator
    """

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize user input to structured intent.

        Args:
            inputs: Agent input data
                - raw_input (required): User's raw input
                - modality (optional): Input modality (auto-detected if not provided)
                - user_id (required): User ID
                - metadata (optional): Additional metadata

        Returns:
            Normalized intent object

        Example:
            >>> agent = InterfaceOrchestratorAgent(skill_client)
            >>> result = await agent.process({
            ...     "raw_input": "todo add 'Review spec' --due tomorrow",
            ...     "modality": "text",
            ...     "user_id": "user_123"
            ... })
            {
                "success": True,
                "agent": "InterfaceOrchestratorAgent",
                "data": {
                    "intent": {
                        "action": "create_task",
                        "parameters": {...},
                        "confidence": 1.0,
                        "modality": "text"
                    }
                }
            }
        """
        logger.info(f"InterfaceOrchestratorAgent processing: {inputs.get('raw_input')[:50]}...")

        # Validate required inputs
        if not inputs.get("user_id"):
            return self._format_error(
                "MISSING_INPUT",
                "user_id is required",
                {"field": "user_id"}
            )

        raw_input = inputs.get("raw_input", "")
        modality = inputs.get("modality")
        user_id = inputs["user_id"]
        metadata = inputs.get("metadata", {})

        # Auto-detect modality if not provided
        if not modality:
            modality = self._detect_modality(raw_input, metadata)

        # Determine input type
        input_type = self._determine_input_type(raw_input, metadata)

        # Special handling for image data
        if input_type == "image_data":
            return self._format_success({
                "intent": {
                    "action": "process_image",
                    "parameters": {
                        "user_id": user_id,
                        "image_data": metadata.get("image_data")
                    },
                    "confidence": 1.0,
                    "modality": "image"
                }
            })

        # Call ui_intent_normalization skill
        skill_params = {
            "raw_input": raw_input,
            "modality": modality,
            "input_type": input_type,
            "user_id": user_id
        }

        result = await self.skill_client.normalize_ui_intent(skill_params)

        if not result.get("success"):
            return self._format_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("details")
            )

        # Return normalized intent
        return self._format_success({
            "intent": result["data"]["intent"]
        })

    def _detect_modality(self, raw_input: str, metadata: Dict[str, Any]) -> str:
        """
        Auto-detect modality from input and metadata.

        Args:
            raw_input: User's raw input
            metadata: Additional metadata

        Returns:
            Detected modality (text | voice | image)
        """
        # Check metadata for explicit modality markers
        if metadata.get("image_data") or metadata.get("image_url"):
            return "image"

        if metadata.get("voice_transcript") or metadata.get("audio_data"):
            return "voice"

        # Default to text
        return "text"

    def _determine_input_type(self, raw_input: str, metadata: Dict[str, Any]) -> str:
        """
        Determine input type for normalization.

        Args:
            raw_input: User's raw input
            metadata: Additional metadata

        Returns:
            Input type (cli_command | natural_language | image_data)
        """
        # Check for image data
        if metadata.get("image_data") or metadata.get("image_url"):
            return "image_data"

        # Check if input looks like a CLI command
        if raw_input.strip().startswith("todo "):
            return "cli_command"

        # Otherwise, treat as natural language
        return "natural_language"
