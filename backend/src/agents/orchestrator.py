"""
Agent: Orchestrator
Implements the Orchestrator Agent that coordinates other agents.
"""

from typing import Dict, Any
from .interface_orchestrator import interface_orchestrator_agent
from .task_reasoning import task_reasoning_agent
from .validation_safety import validation_safety_agent
from .response_formatter import response_formatter_agent


async def orchestrator_agent(
    raw_input: str,
    user_id: str,
    modality: str = "text",  # text, voice, image
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Implements the Orchestrator Agent.
    
    Receive normalized intent from Interface Orchestrator
    Route to appropriate agents (Task Reasoning, Validation, Visual Context)
    Coordinate multi-agent workflows
    Collect results and pass to Response Formatter
    Return final response
    Verify agent coordinates all sub-agents correctly
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
        modality = "text"  # Default to text if invalid
    
    try:
        # Step 1: Interface Orchestrator - Normalize the input
        interface_result = await interface_orchestrator_agent(
            raw_input=raw_input,
            modality=modality,
            user_id=user_id,
            context=context
        )
        
        if not interface_result.get("success"):
            # Format error response directly
            error_response = await response_formatter_agent(
                agent_result=interface_result,
                modality=modality
            )
            return {
                "success": False,
                "interface_result": interface_result,
                "formatted_response": error_response.get("formatted_response", "An error occurred"),
                "message": "Interface orchestration failed"
            }
        
        # Extract normalized intent
        normalized_intent = interface_result.get("normalized_intent")
        confidence = interface_result.get("confidence", 0.0)
        
        # Step 2: Validation & Safety - Validate the parameters
        validation_result = await validation_safety_agent(
            input_params=normalized_intent.get("parameters", {}),
            user_id=user_id
        )
        
        if not validation_result.get("success"):
            # Format error response
            error_response = await response_formatter_agent(
                agent_result=validation_result,
                modality=modality
            )
            return {
                "success": False,
                "validation_result": validation_result,
                "formatted_response": error_response.get("formatted_response", "An error occurred"),
                "message": "Validation failed"
            }
        
        # Step 3: Task Reasoning - Process the intent
        task_result = await task_reasoning_agent(
            normalized_intent=normalized_intent,
            user_id=user_id
        )
        
        # Step 4: Response Formatter - Format the final response
        response_result = await response_formatter_agent(
            agent_result=task_result,
            modality=modality
        )
        
        # Return the final result
        return {
            "success": True,
            "interface_result": interface_result,
            "validation_result": validation_result,
            "task_result": task_result,
            "formatted_response": response_result.get("formatted_response"),
            "modality": modality,
            "confidence": confidence,
            "message": "Request processed successfully"
        }
        
    except Exception as e:
        # Format error response in case of exception
        error_result = {
            "success": False,
            "error": {
                "type": "agent_error",
                "message": str(e)
            },
            "message": "Error in Orchestrator Agent"
        }
        
        error_response = await response_formatter_agent(
            agent_result=error_result,
            modality=modality
        )
        
        return {
            "success": False,
            "error": {
                "type": "agent_error",
                "message": str(e)
            },
            "formatted_response": error_response.get("formatted_response", "An error occurred"),
            "message": "Error in Orchestrator Agent"
        }


# Mock implementation for testing
async def mock_orchestrator_agent(
    raw_input: str,
    user_id: str,
    modality: str = "text",
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Mock implementation of Orchestrator Agent for testing purposes.
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
        modality = "text"  # Default to text if invalid
    
    # Mock the workflow
    mock_interface_result = {
        "success": True,
        "normalized_intent": {
            "action": "create",
            "parameters": {
                "title": "Test task from orchestrator",
                "description": f"Task created from {modality} input: {raw_input}"
            },
            "modality": modality,
            "raw_input": raw_input
        },
        "confidence": 0.9,
        "user_id": user_id,
        "modality": modality,
        "message": "Input normalized successfully (mock)"
    }
    
    mock_validation_result = {
        "success": True,
        "message": "Input validated successfully (mock)",
        "validated_params": {"title": "Test task from orchestrator"}
    }
    
    mock_task_result = {
        "success": True,
        "task": {
            "task_id": 456,
            "user_id": user_id,
            "title": "Test task from orchestrator",
            "description": f"Task created from {modality} input: {raw_input}",
            "due_date": None,
            "due_time": None,
            "priority": "medium",
            "status": "pending",
            "completed_at": None,
            "created_at": "2025-12-27T10:00:00Z",
            "updated_at": "2025-12-27T10:00:00Z"
        },
        "message": "Task created successfully (mock)"
    }
    
    response_result = await mock_response_formatter_agent(
        agent_result=mock_task_result,
        modality=modality
    )
    
    return {
        "success": True,
        "interface_result": mock_interface_result,
        "validation_result": mock_validation_result,
        "task_result": mock_task_result,
        "formatted_response": response_result.get("formatted_response"),
        "modality": modality,
        "confidence": 0.9,
        "message": "Request processed successfully (mock)"
    }