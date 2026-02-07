"""
Agent: Interface Orchestrator
Implements the Interface Orchestrator Agent that detects modality and normalizes inputs.
"""

from typing import Dict, Any
from ..skills import ui_intent_normalization_skill


async def interface_orchestrator_agent(
    raw_input: str,
    modality: str,  # text, voice, image
    user_id: str,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Implements the Interface Orchestrator Agent.
    
    Detect modality (text/voice/image)
    Invoke ui_intent_normalization skill
    Extract user_id from context
    Return normalized intent to main Orchestrator
    Verify agent correctly normalizes all input types
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
    
    if not user_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_id is required"
            },
            "message": "user_id is required"
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
    
    try:
        # Invoke ui_intent_normalization skill
        normalization_result = await ui_intent_normalization_skill(
            raw_input=raw_input,
            modality=modality
        )
        
        if not normalization_result.get("success"):
            return {
                "success": False,
                "error": normalization_result.get("error"),
                "message": "Failed to normalize intent"
            }
        
        # Extract normalized intent
        normalized_intent = normalization_result.get("intent")
        confidence = normalization_result.get("confidence", 0.0)
        
        # Return normalized intent to main Orchestrator
        result = {
            "success": True,
            "normalized_intent": normalized_intent,
            "confidence": confidence,
            "user_id": user_id,
            "modality": modality,
            "message": "Input normalized successfully"
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "agent_error",
                "message": str(e)
            },
            "message": "Error in Interface Orchestrator Agent"
        }


# Mock implementation for testing
async def mock_interface_orchestrator_agent(
    raw_input: str,
    modality: str,  # text, voice, image
    user_id: str,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Mock implementation of Interface Orchestrator Agent for testing purposes.
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
    
    if not user_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_id is required"
            },
            "message": "user_id is required"
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
    
    # Mock normalized intent
    mock_intent = {
        "action": "create",
        "parameters": {
            "title": "Sample task from " + modality,
            "description": f"Task created from {modality} input: {raw_input}"
        },
        "modality": modality,
        "raw_input": raw_input
    }
    
    return {
        "success": True,
        "normalized_intent": mock_intent,
        "confidence": 0.9,
        "user_id": user_id,
        "modality": modality,
        "message": "Input normalized successfully (mock)"
    }