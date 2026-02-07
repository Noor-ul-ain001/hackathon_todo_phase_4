"""
Test user fixtures for Todo Intelligence Platform.

Provides test user data for unit and integration tests.
Per constitution.md section 8.3, users must be isolated.
"""

from datetime import datetime
from typing import List, Dict

# Test user data
# Note: Passwords are hashed with bcrypt in actual implementation

TEST_USERS: List[Dict] = [
    {
        "id": "user_test_001",
        "email": "alice@example.com",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY.X7CxUgWV8zYu",  # "password123"
        "created_at": datetime(2025, 12, 1, 10, 0, 0),
        "updated_at": datetime(2025, 12, 1, 10, 0, 0)
    },
    {
        "id": "user_test_002",
        "email": "bob@example.com",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY.X7CxUgWV8zYu",  # "password123"
        "created_at": datetime(2025, 12, 2, 11, 0, 0),
        "updated_at": datetime(2025, 12, 2, 11, 0, 0)
    },
    {
        "id": "user_test_003",
        "email": "charlie@example.com",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY.X7CxUgWV8zYu",  # "password123"
        "created_at": datetime(2025, 12, 3, 12, 0, 0),
        "updated_at": datetime(2025, 12, 3, 12, 0, 0)
    }
]


def get_test_user(email: str) -> Dict:
    """
    Get a test user by email.

    Args:
        email: User email

    Returns:
        User data dictionary

    Raises:
        ValueError: If user not found
    """
    for user in TEST_USERS:
        if user["email"] == email:
            return user
    raise ValueError(f"Test user not found: {email}")


def get_test_user_by_id(user_id: str) -> Dict:
    """
    Get a test user by ID.

    Args:
        user_id: User ID

    Returns:
        User data dictionary

    Raises:
        ValueError: If user not found
    """
    for user in TEST_USERS:
        if user["id"] == user_id:
            return user
    raise ValueError(f"Test user not found: {user_id}")
