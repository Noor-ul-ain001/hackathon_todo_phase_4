"""
Skill: task_deletion
Implements the task_deletion skill that wraps the MCP delete_task tool.
"""

from typing import Dict, Any
from ..config import settings


async def task_deletion_skill(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Implements the task_deletion skill that wraps the MCP delete_task tool.
    
    Accept: user_id, task_id
    Invoke: delete_task MCP tool
    Handle: Not found, already deleted
    Verify: skill deletes task
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
        result = await call_mcp_tool("delete_task", params)
        
        # Handle the result
        if result.get("success"):
            return {
                "success": True,
                "task_id": result.get("task_id"),
                "message": "Task deleted successfully"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", {"message": "Failed to delete task"}),
                "message": "Failed to delete task"
            }
    except Exception as e:
        # Handle MCP tool errors and return formatted result
        return {
            "success": False,
            "error": {
                "type": "skill_error",
                "message": str(e)
            },
            "message": "Error in task deletion skill"
        }


# Mock implementation for testing
async def mock_task_deletion_skill(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Mock implementation of task_deletion skill for testing purposes.
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
    
    return {
        "success": True,
        "task_id": task_id,
        "message": "Task deleted successfully (mock)"
    }