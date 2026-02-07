"""
Test task fixtures for Todo Intelligence Platform.

Provides test task data for unit and integration tests.
Per constitution.md section 5.2, tasks are isolated by user_id.
"""

from datetime import datetime, date, time
from typing import List, Dict

# Test task data for user_test_001 (Alice)
ALICE_TASKS: List[Dict] = [
    {
        "id": 1,
        "user_id": "user_test_001",
        "title": "Review architecture spec",
        "description": "Complete review by EOD",
        "due_date": date(2025, 12, 28),
        "due_time": None,
        "priority": "high",
        "status": "pending",
        "completed_at": None,
        "created_at": datetime(2025, 12, 27, 10, 30, 0),
        "updated_at": datetime(2025, 12, 27, 10, 30, 0)
    },
    {
        "id": 2,
        "user_id": "user_test_001",
        "title": "Write unit tests",
        "description": "Focus on MCP tools",
        "due_date": date(2025, 12, 29),
        "due_time": time(17, 0, 0),
        "priority": "high",
        "status": "in_progress",
        "completed_at": None,
        "created_at": datetime(2025, 12, 27, 11, 0, 0),
        "updated_at": datetime(2025, 12, 27, 14, 0, 0)
    },
    {
        "id": 3,
        "user_id": "user_test_001",
        "title": "Deploy to staging",
        "description": None,
        "due_date": date(2025, 12, 30),
        "due_time": None,
        "priority": "medium",
        "status": "pending",
        "completed_at": None,
        "created_at": datetime(2025, 12, 27, 12, 0, 0),
        "updated_at": datetime(2025, 12, 27, 12, 0, 0)
    }
]

# Test task data for user_test_002 (Bob)
BOB_TASKS: List[Dict] = [
    {
        "id": 4,
        "user_id": "user_test_002",
        "title": "Prepare presentation",
        "description": "Quarterly review meeting",
        "due_date": date(2025, 12, 29),
        "due_time": time(14, 0, 0),
        "priority": "high",
        "status": "pending",
        "completed_at": None,
        "created_at": datetime(2025, 12, 27, 13, 0, 0),
        "updated_at": datetime(2025, 12, 27, 13, 0, 0)
    },
    {
        "id": 5,
        "user_id": "user_test_002",
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "due_date": date(2025, 12, 28),
        "due_time": None,
        "priority": "low",
        "status": "completed",
        "completed_at": datetime(2025, 12, 27, 15, 0, 0),
        "created_at": datetime(2025, 12, 26, 18, 0, 0),
        "updated_at": datetime(2025, 12, 27, 15, 0, 0)
    }
]

# Combine all test tasks
ALL_TEST_TASKS = ALICE_TASKS + BOB_TASKS


def get_tasks_for_user(user_id: str) -> List[Dict]:
    """
    Get all test tasks for a specific user.

    Args:
        user_id: User ID

    Returns:
        List of task data dictionaries
    """
    return [task for task in ALL_TEST_TASKS if task["user_id"] == user_id]


def get_task_by_id(task_id: int, user_id: str) -> Dict:
    """
    Get a test task by ID with user ownership verification.

    Args:
        task_id: Task ID
        user_id: User ID (for ownership verification)

    Returns:
        Task data dictionary

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    for task in ALL_TEST_TASKS:
        if task["id"] == task_id:
            if task["user_id"] != user_id:
                raise ValueError(f"Task {task_id} does not belong to user {user_id}")
            return task
    raise ValueError(f"Task not found: {task_id}")
