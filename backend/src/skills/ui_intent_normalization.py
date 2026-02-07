"""
Skill: ui_intent_normalization
Implements the ui_intent_normalization skill that converts UI-specific input to structured intents.
"""

from typing import Dict, Any, Optional
from ..config import settings


async def ui_intent_normalization_skill(
    raw_input: str,
    modality: str,  # text, voice, image
    input_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Implements the ui_intent_normalization skill that converts UI-specific input to structured intents.
    
    Accept: raw_input, modality (text/voice/image), input_type
    Parse: CLI commands, natural language, voice transcripts, image data
    Extract: Action (create/update/list/complete/delete) + parameters
    Return: Structured intent object with confidence score
    Verify: skill normalizes all input types correctly
    """
    # Validate required parameters
    if not raw_input:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "raw_input is required"
            },
            "message": "raw_input is required"
        }
    
    if modality not in ["text", "voice", "image"]:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "modality must be one of: text, voice, image"
            },
            "message": "modality must be one of: text, voice, image"
        }
    
    # Process input based on modality
    try:
        # Parse the raw input to extract intent
        intent = parse_intent(raw_input, modality, input_type)
        
        return {
            "success": True,
            "intent": intent,
            "confidence": intent.get("confidence", 0.8),  # Default confidence
            "message": "Intent normalized successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "skill_error",
                "message": str(e)
            },
            "message": "Error in intent normalization"
        }


def parse_intent(raw_input: str, modality: str, input_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse the raw input to extract structured intent based on modality.
    """
    # Normalize the input text
    normalized_input = raw_input.strip().lower()
    
    # Determine the action based on keywords in the input
    action = "unknown"
    parameters = {}
    
    # Handle different modalities
    if modality == "text" or modality == "voice":
        # Parse natural language or CLI commands
        if any(word in normalized_input for word in ["create", "add", "make", "new"]):
            action = "create"
        elif any(word in normalized_input for word in ["update", "change", "modify", "edit"]):
            action = "update"
        elif any(word in normalized_input for word in ["list", "show", "display", "get", "view"]):
            action = "list"
        elif any(word in normalized_input for word in ["complete", "done", "finish", "mark"]):
            action = "complete"
        elif any(word in normalized_input for word in ["delete", "remove", "cancel"]):
            action = "delete"
        elif any(word in normalized_input for word in ["help", "what", "how"]):
            action = "help"
        
        # Extract parameters based on common patterns
        parameters = extract_parameters(normalized_input)
    
    elif modality == "image":
        # For image modality, the input would typically be processed by OCR first
        # Here we'll just return a basic structure
        action = "extract"
        parameters = {"raw_text": raw_input}
    
    # Create the intent object
    intent = {
        "action": action,
        "parameters": parameters,
        "modality": modality,
        "raw_input": raw_input,
        "confidence": 0.8  # Default confidence score
    }
    
    return intent


def extract_parameters(text: str) -> Dict[str, Any]:
    """
    Extract parameters from text input.
    """
    import re
    from datetime import datetime, timedelta
    
    parameters = {}
    
    # Extract title (everything after action words)
    title_match = re.search(r'(?:create|add|make|new|update|change|modify|edit)\s+(.+?)(?:\s+due|\s+by|\s+at|\s+on|$)', text)
    if title_match:
        parameters["title"] = title_match.group(1).strip()
    
    # Extract due date patterns
    date_patterns = [
        r'due\s+(tomorrow|today|\w+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}|\d{1,2}/\d{1,2}(?:/\d{2,4})?|\d{4}-\d{2}-\d{2})',
        r'(?:by|on)\s+(tomorrow|today|\w+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}|\d{1,2}/\d{1,2}(?:/\d{2,4})?|\d{4}-\d{2}-\d{2})',
        r'for\s+(tomorrow|today|\w+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}|\d{1,2}/\d{1,2}(?:/\d{2,4})?|\d{4}-\d{2}-\d{2})'
    ]
    
    for pattern in date_patterns:
        date_match = re.search(pattern, text)
        if date_match:
            date_str = date_match.group(1)
            # Convert relative dates
            if date_str == "today":
                parameters["due_date"] = datetime.now().strftime('%Y-%m-%d')
            elif date_str == "tomorrow":
                parameters["due_date"] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                # For now, just store the raw date string
                parameters["due_date"] = date_str
            break
    
    # Extract priority
    if "high" in text:
        parameters["priority"] = "high"
    elif "low" in text:
        parameters["priority"] = "low"
    elif "medium" in text:
        parameters["priority"] = "medium"
    
    # Extract description
    desc_match = re.search(r'(?:description|desc|about):\s*(.+?)(?:\s+due|\s+by|\s+at|\s+on|$)', text)
    if desc_match:
        parameters["description"] = desc_match.group(1).strip()
    
    return parameters


# Mock implementation for testing
async def mock_ui_intent_normalization_skill(
    raw_input: str,
    modality: str,  # text, voice, image
    input_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Mock implementation of ui_intent_normalization skill for testing purposes.
    """
    # Validate required parameters
    if not raw_input:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "raw_input is required"
            },
            "message": "raw_input is required"
        }
    
    if modality not in ["text", "voice", "image"]:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "modality must be one of: text, voice, image"
            },
            "message": "modality must be one of: text, voice, image"
        }
    
    # Process input based on modality
    try:
        # Parse the raw input to extract intent
        intent = parse_intent(raw_input, modality, input_type)
        
        return {
            "success": True,
            "intent": intent,
            "confidence": intent.get("confidence", 0.8),  # Default confidence
            "message": "Intent normalized successfully (mock)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "skill_error",
                "message": str(e)
            },
            "message": "Error in intent normalization"
        }