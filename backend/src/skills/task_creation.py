"""
Skill: task_creation
Implements the task_creation skill that wraps the MCP add_task tool.
"""

import asyncio
from typing import Dict, Any, Optional
from ..config import settings


async def task_creation_skill(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    due_time: Optional[str] = None,
    priority: Optional[str] = "medium",
    status: Optional[str] = "pending",
) -> Dict[str, Any]:
    """
    Implements the task_creation skill that wraps the MCP add_task tool.
    
    Accept: user_id, title, description, due_date, priority, status
    Invoke: add_task MCP tool
    Handle: MCP tool errors and return formatted result
    Verify: skill correctly wraps MCP tool
    """
    # Prepare parameters for MCP tool
    params = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "due_time": due_time,
        "priority": priority,
        "status": status,
    }
    
    # Remove None values to use MCP tool defaults
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        # In a real implementation, this would call the MCP tool
        # For now, we'll simulate the call
        from mcp_server.src.server import call_mcp_tool
        result = await call_mcp_tool("add_task", params)
        
        # Handle the result
        if result.get("success"):
            return {
                "success": True,
                "task": result.get("task"),
                "message": "Task created successfully"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", {"message": "Failed to create task"}),
                "message": "Failed to create task"
            }
    except Exception as e:
        # Handle MCP tool errors and return formatted result
        return {
            "success": False,
            "error": {
                "type": "skill_error",
                "message": str(e)
            },
            "message": "Error in task creation skill"
        }


# For now, since we don't have the actual MCP server running, 
# I'll create a mock implementation for testing
async def mock_task_creation_skill(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    due_time: Optional[str] = None,
    priority: Optional[str] = "medium",
    status: Optional[str] = "pending",
) -> Dict[str, Any]:
    """
    Mock implementation of task_creation skill for testing purposes.
    """
    import uuid
    from datetime import datetime
    
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
    
    if not title or len(title.strip()) == 0:
        return {
            "success": False,
            "error": {
                "type": "validation_error", 
                "message": "title is required"
            },
            "message": "title is required"
        }
    
    # Generate a mock task
    mock_task = {
        "task_id": int(uuid.uuid4().hex[:8], 16) % 1000000,  # Generate a random ID
        "user_id": user_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "due_time": due_time,
        "priority": priority,
        "status": status,
        "completed_at": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "task": mock_task,
        "message": "Task created successfully (mock)"
    }