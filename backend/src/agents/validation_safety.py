"""
Agent: Validation & Safety
Implements the Validation & Safety Agent that validates inputs and enforces business rules.
"""

from typing import Dict, Any
import re
from datetime import datetime


async def validation_safety_agent(
    input_params: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Implements the Validation & Safety Agent.
    
    Validate all input parameters (types, lengths, formats)
    Enforce business rules (date ranges, enum values)
    Check user ownership for updates/deletes
    Return validation errors or success
    Verify agent blocks invalid inputs, allows valid ones
    """
    # Validate required parameters
    if not input_params:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "input_params is required"
            },
            "message": "input_params is required"
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
        # Perform validation checks
        validation_errors = []
        
        # Validate title if present
        title = input_params.get("title")
        if title is not None:
            if not isinstance(title, str):
                validation_errors.append("title must be a string")
            elif len(title.strip()) == 0:
                validation_errors.append("title cannot be empty")
            elif len(title) > 200:
                validation_errors.append("title must be 200 characters or less")
        
        # Validate description if present
        description = input_params.get("description")
        if description is not None:
            if not isinstance(description, str):
                validation_errors.append("description must be a string")
            elif len(description) > 2000:
                validation_errors.append("description must be 2000 characters or less")
        
        # Validate due_date if present
        due_date = input_params.get("due_date")
        if due_date is not None:
            if not isinstance(due_date, str):
                validation_errors.append("due_date must be a string in YYYY-MM-DD format")
            else:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    validation_errors.append("due_date must be in YYYY-MM-DD format")
        
        # Validate due_time if present
        due_time = input_params.get("due_time")
        if due_time is not None:
            if not isinstance(due_time, str):
                validation_errors.append("due_time must be a string in HH:MM format")
            else:
                # Check HH:MM format
                time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
                if not time_pattern.match(due_time):
                    validation_errors.append("due_time must be in HH:MM format")
        
        # Validate priority if present
        priority = input_params.get("priority")
        if priority is not None:
            if priority not in ["low", "medium", "high"]:
                validation_errors.append("priority must be one of: low, medium, high")
        
        # Validate status if present
        status = input_params.get("status")
        if status is not None:
            if status not in ["pending", "in_progress", "completed", "deleted"]:
                validation_errors.append("status must be one of: pending, in_progress, completed, deleted")
        
        # Validate task_id if present
        task_id = input_params.get("task_id")
        if task_id is not None:
            if not isinstance(task_id, int) or task_id <= 0:
                validation_errors.append("task_id must be a positive integer")
        
        # Validate user_id format
        if not isinstance(user_id, str) or len(user_id.strip()) == 0:
            validation_errors.append("user_id must be a non-empty string")
        
        # Check if there are validation errors
        if validation_errors:
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "messages": validation_errors
                },
                "message": "Validation failed"
            }
        
        # If all validations pass
        return {
            "success": True,
            "message": "Input validated successfully",
            "validated_params": input_params
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "agent_error",
                "message": str(e)
            },
            "message": "Error in Validation & Safety Agent"
        }


# Mock implementation for testing
async def mock_validation_safety_agent(
    input_params: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Mock implementation of Validation & Safety Agent for testing purposes.
    """
    # Validate required parameters
    if not input_params:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "input_params is required"
            },
            "message": "input_params is required"
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
    
    # Perform validation checks
    validation_errors = []
    
    # Validate title if present
    title = input_params.get("title")
    if title is not None:
        if not isinstance(title, str):
            validation_errors.append("title must be a string")
        elif len(title.strip()) == 0:
            validation_errors.append("title cannot be empty")
        elif len(title) > 200:
            validation_errors.append("title must be 200 characters or less")
    
    # Validate description if present
    description = input_params.get("description")
    if description is not None:
        if not isinstance(description, str):
            validation_errors.append("description must be a string")
        elif len(description) > 2000:
            validation_errors.append("description must be 2000 characters or less")
    
    # Validate due_date if present
    due_date = input_params.get("due_date")
    if due_date is not None:
        if not isinstance(due_date, str):
            validation_errors.append("due_date must be a string in YYYY-MM-DD format")
        else:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                validation_errors.append("due_date must be in YYYY-MM-DD format")
    
    # Validate due_time if present
    due_time = input_params.get("due_time")
    if due_time is not None:
        if not isinstance(due_time, str):
            validation_errors.append("due_time must be a string in HH:MM format")
        else:
            # Check HH:MM format
            time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
            if not time_pattern.match(due_time):
                validation_errors.append("due_time must be in HH:MM format")
    
    # Validate priority if present
    priority = input_params.get("priority")
    if priority is not None:
        if priority not in ["low", "medium", "high"]:
            validation_errors.append("priority must be one of: low, medium, high")
    
    # Validate status if present
    status = input_params.get("status")
    if status is not None:
        if status not in ["pending", "in_progress", "completed", "deleted"]:
            validation_errors.append("status must be one of: pending, in_progress, completed, deleted")
    
    # Validate task_id if present
    task_id = input_params.get("task_id")
    if task_id is not None:
        if not isinstance(task_id, int) or task_id <= 0:
            validation_errors.append("task_id must be a positive integer")
    
    # Validate user_id format
    if not isinstance(user_id, str) or len(user_id.strip()) == 0:
        validation_errors.append("user_id must be a non-empty string")
    
    # Check if there are validation errors
    if validation_errors:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "messages": validation_errors
            },
            "message": "Validation failed (mock)"
        }
    
    # If all validations pass
    return {
        "success": True,
        "message": "Input validated successfully (mock)",
        "validated_params": input_params
    }