"""
Agent: Response Formatter
Implements the Response Formatter Agent that formats responses for different modalities.
"""

from typing import Dict, Any


async def response_formatter_agent(
    agent_result: Dict[str, Any],
    modality: str = "text"  # text, voice, image
) -> Dict[str, Any]:
    """
    Implements the Response Formatter Agent.
    
    Convert technical results to user messages
    Adapt to modality (concise for voice, detailed for text)
    Humanize error codes
    Format success confirmations
    Verify agent produces appropriate responses for each modality
    """
    # Validate required parameters
    if not agent_result:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "agent_result is required"
            },
            "message": "agent_result is required",
            "formatted_response": "An error occurred: agent result is required"
        }
    
    if modality not in ["text", "voice", "image"]:
        modality = "text"  # Default to text if invalid
    
    try:
        # Determine if the result is a success or failure
        is_success = agent_result.get("success", False)
        
        if is_success:
            # Format success response
            formatted_response = format_success_response(agent_result, modality)
        else:
            # Format error response
            formatted_response = format_error_response(agent_result, modality)
        
        return {
            "success": True,
            "formatted_response": formatted_response,
            "modality": modality,
            "original_result": agent_result,
            "message": "Response formatted successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "agent_error",
                "message": str(e)
            },
            "formatted_response": "An error occurred while formatting the response",
            "message": "Error in Response Formatter Agent"
        }


def format_success_response(agent_result: Dict[str, Any], modality: str) -> str:
    """
    Format a successful agent result for the specified modality.
    """
    # Extract relevant information from the agent result
    message = agent_result.get("message", "Operation completed successfully")
    task = agent_result.get("task")
    tasks = agent_result.get("tasks")
    
    if task:
        # Format for a single task
        title = task.get("title", "Untitled")
        status = task.get("status", "unknown")
        due_date = task.get("due_date")
        priority = task.get("priority", "unknown")
        
        if modality == "voice":
            # Concise response for voice
            if status == "completed":
                return f"Task '{title}' has been completed."
            elif status == "pending":
                due_str = f" due {due_date}" if due_date else ""
                return f"Task '{title}' has been created{due_str}."
            else:
                return f"Task '{title}' has been updated."
        else:
            # More detailed response for text/image
            due_str = f" (due: {due_date})" if due_date else ""
            priority_str = f" (priority: {priority})" if priority else ""
            return f"✅ {message}: '{title}'{due_str}{priority_str}"
    
    elif tasks:
        # Format for multiple tasks (list operation)
        count = len(tasks)
        if modality == "voice":
            return f"You have {count} tasks."
        else:
            task_list = [f"• {task.get('title', 'Untitled')}" for task in tasks]
            task_str = "\n".join(task_list)
            return f"You have {count} tasks:\n{task_str}"
    
    else:
        # Generic success message
        if modality == "voice":
            return message.replace("successfully", "").replace("(mock)", "").strip()
        else:
            return f"✅ {message}"


def format_error_response(agent_result: Dict[str, Any], modality: str) -> str:
    """
    Format an error agent result for the specified modality.
    """
    error = agent_result.get("error", {})
    error_type = error.get("type", "unknown_error")
    error_message = error.get("message", "An unknown error occurred")
    
    if modality == "voice":
        # Simple, human-friendly error for voice
        if "validation" in error_type.lower():
            return "I couldn't understand your request. Please try rephrasing."
        elif "authorization" in error_type.lower():
            return "You don't have permission to perform this action."
        elif "not_found" in error_type.lower():
            return "The item you're looking for was not found."
        else:
            return "Sorry, something went wrong. Please try again."
    else:
        # More detailed error for text/image
        if "validation" in error_type.lower():
            return f"❌ Validation Error: {error_message}"
        elif "authorization" in error_type.lower():
            return f"❌ Authorization Error: {error_message}"
        elif "not_found" in error_type.lower():
            return f"❌ Not Found: {error_message}"
        else:
            return f"❌ Error: {error_message}"


# Mock implementation for testing
async def mock_response_formatter_agent(
    agent_result: Dict[str, Any],
    modality: str = "text"
) -> Dict[str, Any]:
    """
    Mock implementation of Response Formatter Agent for testing purposes.
    """
    # Validate required parameters
    if not agent_result:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "agent_result is required"
            },
            "message": "agent_result is required",
            "formatted_response": "An error occurred: agent result is required"
        }
    
    if modality not in ["text", "voice", "image"]:
        modality = "text"  # Default to text if invalid
    
    # Determine if the result is a success or failure
    is_success = agent_result.get("success", False)
    
    if is_success:
        # Format success response
        formatted_response = format_success_response(agent_result, modality)
    else:
        # Format error response
        formatted_response = format_error_response(agent_result, modality)
    
    return {
        "success": True,
        "formatted_response": formatted_response,
        "modality": modality,
        "original_result": agent_result,
        "message": "Response formatted successfully (mock)"
    }