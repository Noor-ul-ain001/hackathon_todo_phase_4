"""
Skill: intent_disambiguation
Implements the intent_disambiguation skill that helps resolve ambiguous user requests.
"""

from typing import Dict, Any, List
from ..config import settings


async def intent_disambiguation_skill(
    user_input: str,
    possible_intents: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Implements the intent_disambiguation skill that resolves ambiguous user requests.
    
    Accept: user_input, possible_intents
    Analyze: ambiguity (multiple tasks match, unclear action)
    Return: Clarification question with options
    Verify: skill generates useful clarification
    """
    # Validate required parameters
    if not user_input:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_input is required"
            },
            "message": "user_input is required"
        }
    
    if not possible_intents or not isinstance(possible_intents, list):
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "possible_intents is required and must be a list"
            },
            "message": "possible_intents is required and must be a list"
        }
    
    # Check if there's actual ambiguity (more than one possible intent)
    if len(possible_intents) <= 1:
        return {
            "success": True,
            "is_ambiguous": False,
            "resolved_intent": possible_intents[0] if possible_intents else None,
            "message": "No ambiguity detected, single intent identified"
        }
    
    # Generate clarification question based on the possible intents
    clarification_options = []
    for i, intent in enumerate(possible_intents):
        option = {
            "id": i + 1,
            "description": intent.get("description", f"Option {i + 1}"),
            "action": intent.get("action", "unknown")
        }
        clarification_options.append(option)
    
    clarification_question = f"I found multiple possible interpretations of your request '{user_input}'. Could you clarify which one you mean?"
    
    return {
        "success": True,
        "is_ambiguous": True,
        "clarification_question": clarification_question,
        "options": clarification_options,
        "message": "Ambiguous request detected, clarification needed"
    }


# Mock implementation for testing
async def mock_intent_disambiguation_skill(
    user_input: str,
    possible_intents: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Mock implementation of intent_disambiguation skill for testing purposes.
    """
    # Validate required parameters
    if not user_input:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_input is required"
            },
            "message": "user_input is required"
        }
    
    if not possible_intents or not isinstance(possible_intents, list):
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "possible_intents is required and must be a list"
            },
            "message": "possible_intents is required and must be a list"
        }
    
    # Check if there's actual ambiguity (more than one possible intent)
    if len(possible_intents) <= 1:
        return {
            "success": True,
            "is_ambiguous": False,
            "resolved_intent": possible_intents[0] if possible_intents else None,
            "message": "No ambiguity detected, single intent identified (mock)"
        }
    
    # Generate clarification question based on the possible intents
    clarification_options = []
    for i, intent in enumerate(possible_intents):
        option = {
            "id": i + 1,
            "description": intent.get("description", f"Option {i + 1}"),
            "action": intent.get("action", "unknown"),
            "confidence": intent.get("confidence", 0.5)
        }
        clarification_options.append(option)
    
    clarification_question = f"I found multiple possible interpretations of your request '{user_input}'. Could you clarify which one you mean?"
    
    return {
        "success": True,
        "is_ambiguous": True,
        "clarification_question": clarification_question,
        "options": clarification_options,
        "message": "Ambiguous request detected, clarification needed (mock)"
    }