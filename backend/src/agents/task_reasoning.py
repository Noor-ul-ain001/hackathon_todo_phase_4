"""
Agent: Task Reasoning
Implements the Task Reasoning Agent that interprets user intents and invokes skills.
"""

from typing import Dict, Any
from ..skills import (
    task_creation_skill,
    task_update_skill,
    task_listing_skill,
    task_completion_skill,
    task_deletion_skill,
    intent_disambiguation_skill
)


async def task_reasoning_agent(
    normalized_intent: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Implements the Task Reasoning Agent.
    
    Parse natural language for task operations
    Extract dates, times, priorities from text
    Invoke appropriate skill (task_creation, task_update, etc.)
    Handle ambiguous requests via intent_disambiguation skill
    Verify agent extracts task data and invokes skills correctly
    """
    # Validate required parameters
    if not normalized_intent:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "normalized_intent is required"
            },
            "message": "normalized_intent is required"
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
    
    try:
        action = normalized_intent.get("action", "unknown")
        parameters = normalized_intent.get("parameters", {})
        
        # Based on the action, invoke the appropriate skill
        if action == "create":
            result = await task_creation_skill(
                user_id=user_id,
                title=parameters.get("title", ""),
                description=parameters.get("description"),
                due_date=parameters.get("due_date"),
                due_time=parameters.get("due_time"),
                priority=parameters.get("priority", "medium"),
                status=parameters.get("status", "pending")
            )
        elif action == "list":
            result = await task_listing_skill(
                user_id=user_id,
                filters=parameters.get("filters"),
                sort=parameters.get("sort"),
                limit=parameters.get("limit", 20),
                offset=parameters.get("offset", 0)
            )
        elif action == "update":
            task_id = parameters.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": {
                        "type": "validation_error",
                        "message": "task_id is required for update action"
                    },
                    "message": "task_id is required for update action"
                }
            
            updates = {k: v for k, v in parameters.items() 
                      if k not in ["task_id", "user_id"]}
            
            result = await task_update_skill(
                user_id=user_id,
                task_id=task_id,
                updates=updates
            )
        elif action == "complete":
            task_id = parameters.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": {
                        "type": "validation_error",
                        "message": "task_id is required for complete action"
                    },
                    "message": "task_id is required for complete action"
                }
            
            result = await task_completion_skill(
                user_id=user_id,
                task_id=task_id
            )
        elif action == "delete":
            task_id = parameters.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": {
                        "type": "validation_error",
                        "message": "task_id is required for delete action"
                    },
                    "message": "task_id is required for delete action"
                }
            
            result = await task_deletion_skill(
                user_id=user_id,
                task_id=task_id
            )
        elif action == "help":
            result = {
                "success": True,
                "message": "I can help you manage your tasks. You can ask me to create, list, update, complete, or delete tasks.",
                "available_actions": ["create", "list", "update", "complete", "delete"]
            }
        else:
            # If action is unknown, try to disambiguate
            possible_intents = [
                {"action": "create", "description": "Create a new task"},
                {"action": "list", "description": "List existing tasks"},
                {"action": "update", "description": "Update an existing task"},
                {"action": "complete", "description": "Mark a task as completed"},
                {"action": "delete", "description": "Delete a task"}
            ]
            
            disambiguation_result = await intent_disambiguation_skill(
                user_input=normalized_intent.get("raw_input", ""),
                possible_intents=possible_intents
            )
            
            if disambiguation_result.get("is_ambiguous"):
                result = disambiguation_result
            else:
                result = {
                    "success": False,
                    "error": {
                        "type": "unknown_action",
                        "message": f"Unknown action: {action}"
                    },
                    "message": f"Unknown action: {action}"
                }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "agent_error",
                "message": str(e)
            },
            "message": "Error in Task Reasoning Agent"
        }


# Mock implementation for testing
async def mock_task_reasoning_agent(
    normalized_intent: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Mock implementation of Task Reasoning Agent for testing purposes.
    """
    # Validate required parameters
    if not normalized_intent:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "normalized_intent is required"
            },
            "message": "normalized_intent is required"
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
    
    action = normalized_intent.get("action", "unknown")
    parameters = normalized_intent.get("parameters", {})
    
    # Mock response based on action
    if action == "create":
        mock_result = {
            "success": True,
            "task": {
                "task_id": 123,
                "user_id": user_id,
                "title": parameters.get("title", "Mock Task"),
                "description": parameters.get("description", "Mock description"),
                "due_date": parameters.get("due_date"),
                "due_time": parameters.get("due_time"),
                "priority": parameters.get("priority", "medium"),
                "status": parameters.get("status", "pending"),
                "completed_at": None,
                "created_at": "2025-12-27T10:00:00Z",
                "updated_at": "2025-12-27T10:00:00Z"
            },
            "message": "Task created successfully (mock)"
        }
    elif action == "list":
        mock_result = {
            "success": True,
            "tasks": [
                {
                    "task_id": 123,
                    "user_id": user_id,
                    "title": "Mock Task",
                    "description": "Mock description",
                    "due_date": "2025-12-31",
                    "due_time": "17:00",
                    "priority": "medium",
                    "status": "pending",
                    "completed_at": None,
                    "created_at": "2025-12-27T10:00:00Z",
                    "updated_at": "2025-12-27T10:00:00Z"
                }
            ],
            "count": 1,
            "has_more": False,
            "message": "Tasks retrieved successfully (mock)"
        }
    elif action == "update":
        mock_result = {
            "success": True,
            "task": {
                "task_id": parameters.get("task_id", 123),
                "user_id": user_id,
                "title": parameters.get("title", "Mock Task"),
                "description": parameters.get("description", "Mock description"),
                "due_date": parameters.get("due_date"),
                "due_time": parameters.get("due_time"),
                "priority": parameters.get("priority", "medium"),
                "status": parameters.get("status", "pending"),
                "completed_at": None,
                "created_at": "2025-12-27T10:00:00Z",
                "updated_at": "2025-12-27T11:00:00Z"
            },
            "updated_fields": list(parameters.keys()),
            "message": "Task updated successfully (mock)"
        }
    elif action == "complete":
        mock_result = {
            "success": True,
            "task": {
                "task_id": parameters.get("task_id", 123),
                "user_id": user_id,
                "title": "Mock Task",
                "description": "Mock description",
                "due_date": "2025-12-31",
                "due_time": "17:00",
                "priority": "medium",
                "status": "completed",
                "completed_at": "2025-12-27T12:00:00Z",
                "created_at": "2025-12-27T10:00:00Z",
                "updated_at": "2025-12-27T12:00:00Z"
            },
            "message": "Task completed successfully (mock)"
        }
    elif action == "delete":
        mock_result = {
            "success": True,
            "task_id": parameters.get("task_id", 123),
            "message": "Task deleted successfully (mock)"
        }
    elif action == "help":
        mock_result = {
            "success": True,
            "message": "I can help you manage your tasks. You can ask me to create, list, update, complete, or delete tasks.",
            "available_actions": ["create", "list", "update", "complete", "delete"]
        }
    else:
        mock_result = {
            "success": False,
            "error": {
                "type": "unknown_action",
                "message": f"Unknown action: {action}"
            },
            "message": f"Unknown action: {action}"
        }
    
    return mock_result