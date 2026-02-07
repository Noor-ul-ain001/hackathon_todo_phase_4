"""
Skill: task_update
Implements the task_update skill that wraps the MCP update_task tool.
"""

from typing import Dict, Any, Optional
from ..config import settings


async def task_update_skill(
    user_id: str,
    task_id: int,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Implements the task_update skill that wraps the MCP update_task tool.
    
    Accept: user_id, task_id, updates object
    Invoke: update_task MCP tool
    Handle: Ownership errors, not found errors
    Verify: skill correctly updates and handles errors
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
    
    if not updates or len(updates) == 0:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "at least one field to update is required"
            },
            "message": "at least one field to update is required"
        }
    
    # Prepare parameters for MCP tool
    params = {
        "user_id": user_id,
        "task_id": task_id,
        "updates": updates
    }
    
    try:
        # In a real implementation, this would call the MCP tool
        from mcp_server.src.server import call_mcp_tool
        result = await call_mcp_tool("update_task", params)
        
        # Handle the result
        if result.get("success"):
            return {
                "success": True,
                "task": result.get("task"),
                "updated_fields": list(updates.keys()),
                "message": "Task updated successfully"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", {"message": "Failed to update task"}),
                "message": "Failed to update task"
            }
    except Exception as e:
        # Handle MCP tool errors and return formatted result
        return {
            "success": False,
            "error": {
                "type": "skill_error",
                "message": str(e)
            },
            "message": "Error in task update skill"
        }


# Mock implementation for testing
async def mock_task_update_skill(
    user_id: str,
    task_id: int,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Mock implementation of task_update skill for testing purposes.
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
    
    if not updates or len(updates) == 0:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "at least one field to update is required"
            },
            "message": "at least one field to update is required"
        }
    
    # Simulate ownership check failure for testing
    if task_id == 999:  # Special ID to simulate ownership error
        return {
            "success": False,
            "error": {
                "type": "authorization_error",
                "message": "Task does not belong to this user"
            },
            "message": "Task does not belong to this user"
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
    
    # Generate mock updated task
    updated_task = {
        "task_id": task_id,
        "user_id": user_id,
        "title": updates.get("title", f"Task {task_id}"),
        "description": updates.get("description", f"Description for task {task_id}"),
        "due_date": updates.get("due_date", "2025-12-31"),
        "due_time": updates.get("due_time", "17:00"),
        "priority": updates.get("priority", "medium"),
        "status": updates.get("status", "pending"),
        "completed_at": updates.get("status") == "completed" and "2025-12-27T12:00:00Z" or None,
        "created_at": "2025-12-27T10:00:00Z",
        "updated_at": "2025-12-27T11:00:00Z"
    }
    
    return {
        "success": True,
        "task": updated_task,
        "updated_fields": list(updates.keys()),
        "message": "Task updated successfully (mock)"
    }