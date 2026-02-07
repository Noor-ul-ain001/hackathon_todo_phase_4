"""
Skill: task_listing
Implements the task_listing skill that wraps the MCP list_tasks tool.
"""

from typing import Dict, Any, Optional, List
from ..config import settings


async def task_listing_skill(
    user_id: str,
    filters: Optional[Dict[str, Any]] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
) -> Dict[str, Any]:
    """
    Implements the task_listing skill that wraps the MCP list_tasks tool.
    
    Accept: user_id, filters, sort, limit
    Invoke: list_tasks MCP tool
    Handle: Empty results, pagination
    Verify: skill returns formatted task list
    """
    # Prepare parameters for MCP tool
    params = {
        "user_id": user_id,
        "filters": filters or {},
        "sort": sort,
        "limit": limit,
        "offset": offset
    }
    
    try:
        # In a real implementation, this would call the MCP tool
        from mcp_server.src.server import call_mcp_tool
        result = await call_mcp_tool("list_tasks", params)
        
        # Handle the result
        if result.get("success"):
            return {
                "success": True,
                "tasks": result.get("tasks", []),
                "count": result.get("count", 0),
                "has_more": result.get("has_more", False),
                "message": "Tasks retrieved successfully"
            }
        else:
            return {
                "success": False,
                "tasks": [],
                "error": result.get("error", {"message": "Failed to list tasks"}),
                "message": "Failed to list tasks"
            }
    except Exception as e:
        # Handle MCP tool errors and return formatted result
        return {
            "success": False,
            "tasks": [],
            "error": {
                "type": "skill_error",
                "message": str(e)
            },
            "message": "Error in task listing skill"
        }


# Mock implementation for testing
async def mock_task_listing_skill(
    user_id: str,
    filters: Optional[Dict[str, Any]] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
) -> Dict[str, Any]:
    """
    Mock implementation of task_listing skill for testing purposes.
    """
    # Validate required parameters
    if not user_id:
        return {
            "success": False,
            "tasks": [],
            "error": {
                "type": "validation_error",
                "message": "user_id is required"
            },
            "message": "user_id is required"
        }
    
    # Generate mock tasks based on filters
    mock_tasks = [
        {
            "task_id": 1,
            "user_id": user_id,
            "title": "Sample Task",
            "description": "This is a sample task for testing",
            "due_date": "2025-12-31",
            "due_time": "17:00",
            "priority": "medium",
            "status": "pending",
            "completed_at": None,
            "created_at": "2025-12-27T10:00:00Z",
            "updated_at": "2025-12-27T10:00:00Z"
        }
    ]
    
    # Apply filters if provided
    if filters:
        status_filter = filters.get('status')
        if status_filter:
            mock_tasks = [task for task in mock_tasks if task['status'] == status_filter]
    
    # Apply pagination
    total_count = len(mock_tasks)
    paginated_tasks = mock_tasks[offset:offset + limit]
    
    return {
        "success": True,
        "tasks": paginated_tasks,
        "count": len(paginated_tasks),
        "has_more": offset + limit < total_count,
        "message": "Tasks retrieved successfully (mock)"
    }