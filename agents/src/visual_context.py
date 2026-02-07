"""
Visual Context Agent

Extracts task information from images using Claude's vision API.
Handles image validation, quality assessment, and text extraction.
"""

from typing import Dict, Any
import logging
import base64
import re
import os
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class VisualContextAgent(BaseAgent):
    """
    Agent responsible for processing image inputs.

    Purpose:
    - Validate image format and size
    - Assess image quality
    - Perform OCR to extract text
    - Parse extracted text for task information
    - Return structured task data

    Note: Full implementation requires OCR integration (Phase 5)
    """

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process image and extract task information using Claude's vision API.

        Args:
            inputs: Agent input data
                - image_data (required): Base64 encoded image (data:image/png;base64,...)
                - user_id (required): User ID

        Returns:
            Extracted task data with confidence scores

        Example:
            >>> agent = VisualContextAgent()
            >>> result = await agent.process({
            ...     "image_data": "data:image/png;base64,...",
            ...     "user_id": "user_123"
            ... })
            {
                "success": True,
                "agent": "VisualContextAgent",
                "data": {
                    "extracted_text": "Buy groceries tomorrow",
                    "tasks_found": [
                        {
                            "title": "Buy groceries",
                            "due_date": "2025-12-28",
                            "priority": "medium"
                        }
                    ],
                    "confidence": 0.85
                }
            }
        """
        logger.info("VisualContextAgent processing image")

        # Validate required inputs
        if not inputs.get("image_data"):
            return self._format_error(
                "MISSING_INPUT",
                "image_data is required",
                {"field": "image_data"}
            )

        if not inputs.get("user_id"):
            return self._format_error(
                "MISSING_INPUT",
                "user_id is required",
                {"field": "user_id"}
            )

        image_data = inputs["image_data"]
        user_id = inputs["user_id"]

        try:
            # Step 1: Validate image format
            if not self._validate_image_format(image_data):
                return self._format_error(
                    "INVALID_FORMAT",
                    "Image format not supported. Use PNG, JPG, or WebP",
                    {"supported_formats": ["image/png", "image/jpeg", "image/webp"]}
                )

            # Step 2: Validate image size
            if not self._validate_image_size(image_data):
                return self._format_error(
                    "IMAGE_TOO_LARGE",
                    "Image size exceeds 10MB limit",
                    {"max_size_mb": 10}
                )

            # Step 3: Extract text and task information from image
            extraction_result = await self._analyze_image_with_claude(image_data, user_id)

            if not extraction_result.get("success"):
                return self._format_error(
                    "EXTRACTION_FAILED",
                    extraction_result.get("error", "Failed to extract text from image"),
                    {}
                )

            logger.info(f"Successfully extracted data from image for user {user_id}")

            return {
                "success": True,
                "agent": "VisualContextAgent",
                "data": extraction_result["data"]
            }

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}", exc_info=True)
            return self._format_error(
                "PROCESSING_ERROR",
                f"Failed to process image: {str(e)}",
                {}
            )

    def _validate_image_format(self, image_data: str) -> bool:
        """Validate image format (PNG, JPG, WebP)."""
        if not image_data.startswith("data:image/"):
            return False

        allowed_formats = ["data:image/png", "data:image/jpeg", "data:image/jpg", "data:image/webp"]
        return any(image_data.startswith(fmt) for fmt in allowed_formats)

    def _validate_image_size(self, image_data: str) -> bool:
        """Check if image size is under 10MB."""
        try:
            # Extract base64 part
            if ";base64," in image_data:
                base64_data = image_data.split(";base64,")[1]
            else:
                base64_data = image_data

            # Calculate size in bytes (base64 is ~4/3 of original size)
            size_bytes = (len(base64_data) * 3) / 4
            size_mb = size_bytes / (1024 * 1024)

            return size_mb <= 10
        except Exception:
            return False

    async def _analyze_image_with_claude(self, image_data: str, user_id: str) -> Dict[str, Any]:
        """
        Analyze image using Claude's vision API to extract task information.

        Returns structured task data extracted from the image.
        """
        try:
            # Import here to avoid issues if anthropic is not installed
            try:
                from anthropic import Anthropic
            except ImportError:
                logger.warning("Anthropic SDK not installed, using fallback OCR")
                return await self._fallback_ocr(image_data)

            # Get API key from environment
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logger.warning("ANTHROPIC_API_KEY not set, using fallback OCR")
                return await self._fallback_ocr(image_data)

            # Initialize Claude client
            client = Anthropic(api_key=api_key)

            # Extract media type and base64 data
            if ";base64," in image_data:
                media_type_part = image_data.split(";base64,")[0]
                media_type = media_type_part.replace("data:", "")
                base64_data = image_data.split(";base64,")[1]
            else:
                media_type = "image/png"
                base64_data = image_data

            # Call Claude API with vision
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": """Analyze this image and extract any task-related information. Look for:
- Task titles/descriptions
- Due dates or deadlines
- Priority indicators (urgent, high, medium, low)
- Any to-do items or action items

Return a JSON response with this structure:
{
  "extracted_text": "full text found in image",
  "tasks_found": [
    {
      "title": "task title",
      "due_date": "YYYY-MM-DD or null",
      "priority": "high/medium/low or null",
      "description": "any additional details"
    }
  ],
  "confidence": 0.0-1.0
}

If no tasks are found, return an empty tasks_found array."""
                            }
                        ],
                    }
                ],
            )

            # Parse response
            response_text = message.content[0].text
            logger.info(f"Claude vision response: {response_text}")

            # Try to extract JSON from response
            import json

            # Find JSON in response (might be wrapped in markdown code blocks)
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result_data = json.loads(json_match.group(0))
            else:
                # Fallback: create structure from plain text
                result_data = {
                    "extracted_text": response_text,
                    "tasks_found": [],
                    "confidence": 0.5
                }

            return {
                "success": True,
                "data": result_data
            }

        except Exception as e:
            logger.error(f"Error calling Claude vision API: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    async def _fallback_ocr(self, image_data: str) -> Dict[str, Any]:
        """
        Fallback OCR method when Claude API is not available.
        Returns a helpful message instead of failing.
        """
        return {
            "success": True,
            "data": {
                "extracted_text": "Image uploaded successfully",
                "tasks_found": [],
                "confidence": 0.0,
                "message": "Image processing requires ANTHROPIC_API_KEY environment variable. Please add your API key to use vision capabilities."
            }
        }
