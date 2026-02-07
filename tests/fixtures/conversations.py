"""
Test conversation and message fixtures for Todo Intelligence Platform.

Provides test conversation data for stateless chat testing.
Per constitution.md section 2.2, conversations reconstructed from messages.
"""

from datetime import datetime
from typing import List, Dict

# Test conversations
TEST_CONVERSATIONS: List[Dict] = [
    {
        "id": 1,
        "user_id": "user_test_001",
        "created_at": datetime(2025, 12, 27, 10, 0, 0),
        "updated_at": datetime(2025, 12, 27, 10, 30, 0)
    },
    {
        "id": 2,
        "user_id": "user_test_001",
        "created_at": datetime(2025, 12, 27, 14, 0, 0),
        "updated_at": datetime(2025, 12, 27, 14, 15, 0)
    },
    {
        "id": 3,
        "user_id": "user_test_002",
        "created_at": datetime(2025, 12, 27, 11, 0, 0),
        "updated_at": datetime(2025, 12, 27, 11, 30, 0)
    }
]

# Test messages
TEST_MESSAGES: List[Dict] = [
    # Conversation 1 (Alice) - Task creation flow
    {
        "id": 1,
        "user_id": "user_test_001",
        "conversation_id": 1,
        "role": "user",
        "content": "Add meeting with client tomorrow at 3pm",
        "created_at": datetime(2025, 12, 27, 10, 0, 0)
    },
    {
        "id": 2,
        "user_id": "user_test_001",
        "conversation_id": 1,
        "role": "assistant",
        "content": "I've added 'Meeting with client' to your task list for tomorrow at 3:00 PM.",
        "created_at": datetime(2025, 12, 27, 10, 0, 5)
    },
    {
        "id": 3,
        "user_id": "user_test_001",
        "conversation_id": 1,
        "role": "user",
        "content": "Show me my tasks for this week",
        "created_at": datetime(2025, 12, 27, 10, 30, 0)
    },
    {
        "id": 4,
        "user_id": "user_test_001",
        "conversation_id": 1,
        "role": "assistant",
        "content": "You have 3 tasks due this week:\n1. Review architecture spec (Due: Dec 28)\n2. Write tests (Due: Dec 29)\n3. Deploy to staging (Due: Dec 30)",
        "created_at": datetime(2025, 12, 27, 10, 30, 2)
    },

    # Conversation 2 (Alice) - Task completion flow
    {
        "id": 5,
        "user_id": "user_test_001",
        "conversation_id": 2,
        "role": "user",
        "content": "Mark task 2 as complete",
        "created_at": datetime(2025, 12, 27, 14, 0, 0)
    },
    {
        "id": 6,
        "user_id": "user_test_001",
        "conversation_id": 2,
        "role": "assistant",
        "content": "Task 'Write unit tests' has been marked as completed.",
        "created_at": datetime(2025, 12, 27, 14, 0, 3)
    },
    {
        "id": 7,
        "user_id": "user_test_001",
        "conversation_id": 2,
        "role": "user",
        "content": "Thank you",
        "created_at": datetime(2025, 12, 27, 14, 15, 0)
    },
    {
        "id": 8,
        "user_id": "user_test_001",
        "conversation_id": 2,
        "role": "assistant",
        "content": "You're welcome! Is there anything else I can help with?",
        "created_at": datetime(2025, 12, 27, 14, 15, 1)
    },

    # Conversation 3 (Bob) - Task creation
    {
        "id": 9,
        "user_id": "user_test_002",
        "conversation_id": 3,
        "role": "user",
        "content": "Add 'Prepare presentation' for tomorrow at 2pm, high priority",
        "created_at": datetime(2025, 12, 27, 11, 0, 0)
    },
    {
        "id": 10,
        "user_id": "user_test_002",
        "conversation_id": 3,
        "role": "assistant",
        "content": "I've created the task 'Prepare presentation' for tomorrow at 2:00 PM with high priority.",
        "created_at": datetime(2025, 12, 27, 11, 0, 4)
    }
]


def get_conversation_by_id(conversation_id: int, user_id: str) -> Dict:
    """
    Get a test conversation by ID with user ownership verification.

    Args:
        conversation_id: Conversation ID
        user_id: User ID (for ownership verification)

    Returns:
        Conversation data dictionary

    Raises:
        ValueError: If conversation not found or doesn't belong to user
    """
    for conv in TEST_CONVERSATIONS:
        if conv["id"] == conversation_id:
            if conv["user_id"] != user_id:
                raise ValueError(f"Conversation {conversation_id} does not belong to user {user_id}")
            return conv
    raise ValueError(f"Conversation not found: {conversation_id}")


def get_messages_for_conversation(conversation_id: int, user_id: str) -> List[Dict]:
    """
    Get all test messages for a conversation with user ownership verification.

    Args:
        conversation_id: Conversation ID
        user_id: User ID (for ownership verification)

    Returns:
        List of message data dictionaries ordered by created_at

    Raises:
        ValueError: If conversation doesn't belong to user
    """
    # Verify conversation ownership
    get_conversation_by_id(conversation_id, user_id)

    # Return messages for this conversation, ordered by created_at
    messages = [msg for msg in TEST_MESSAGES if msg["conversation_id"] == conversation_id]
    return sorted(messages, key=lambda m: m["created_at"])


def get_conversations_for_user(user_id: str) -> List[Dict]:
    """
    Get all test conversations for a specific user.

    Args:
        user_id: User ID

    Returns:
        List of conversation data dictionaries
    """
    return [conv for conv in TEST_CONVERSATIONS if conv["user_id"] == user_id]
