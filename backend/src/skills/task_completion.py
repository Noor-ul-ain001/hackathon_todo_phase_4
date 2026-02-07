"""
Skill: task_completion
Implements the task_completion skill that wraps the MCP complete_task tool.
"""

from typing import Dict, Any
from ..config import settings


async def task_completion_skill(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Implements the task_completion skill that wraps the MCP complete_task tool.
    
    Accept: user_id, task_id
    Invoke: complete_task MCP tool
    Handle: Already completed, not found
    Verify: skill marks task complete
    """
    # Validate required parameters
    if not user_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_id is required"
            },
            "message": "user_id is required"
        }
    
    if not task_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "task_id is required"
            },
            "message": "task_id is required"
        }
    
    # Prepare parameters for MCP tool
    params = {
        "user_id": user_id,
        "task_id": task_id
    }
    
    try:
        # In a real implementation, this would call the MCP tool
        from mcp_server.src.server import call_mcp_tool
        result = await call_mcp_tool("complete_task", params)
        
        # Handle the result
        if result.get("success"):
            return {
                "success": True,
                "task": result.get("task"),
                "message": "Task completed successfully"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", {"message": "Failed to complete task"}),
                "message": "Failed to complete task"
            }
    except Exception as e:
        # Handle MCP tool errors and return formatted result
        return {
            "success": False,
            "error": {
                "type": "skill_error",
                "message": str(e)
            },
            "message": "Error in task completion skill"
        }


# Mock implementation for testing
async def mock_task_completion_skill(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Mock implementation of task_completion skill for testing purposes.
    """
    # Validate required parameters
    if not user_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_id is required"
            },
            "message": "user_id is required"
        }
    
    if not task_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "task_id is required"
            },
            "message": "task_id is required"
        }
    
    # Simulate already completed task
    if task_id == 997:  # Special ID to simulate already completed
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "Task is already completed"
            },
            "message": "Task is already completed"
        }
    
    # Simulate not found error
    if task_id == 998:  # Special ID to simulate not found error
        return {
            "success": False,
            "error": {
                "type": "not_found_error",
                "message": "Task not found"
            },
            "message": "Task not found"
        }
    
    # Generate mock completed task
    completed_task = {
        "task_id": task_id,
        "user_id": user_id,
        "title": f"Task {task_id}",
        "description": f"Description for task {task_id}",
        "due_date": "2025-12-31",
        "due_time": "17:00",
        "priority": "medium",
        "status": "completed",
        "completed_at": "2025-12-27T12:00:00Z",
        "created_at": "2025-12-27T10:00:00Z",
        "updated_at": "2025-12-27T12:00:00Z"
    }
    
    return {
        "success": True,
        "task": completed_task,
        "message": "Task completed successfully (mock)"
    }