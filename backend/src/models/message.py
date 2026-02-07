"""
Message model for Todo Intelligence Platform.

Per constitution.md section 2.2, messages enable stateless conversation reconstruction.
Each request loads conversation history from this table.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role (sender)."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """
    Conversation message model.

    Stores user and assistant messages for stateless context reconstruction.
    Messages ordered by created_at for conversation history.

    Indexes per database/schema.md:
    - idx_messages_user_id
    - idx_messages_conversation_id
    - idx_messages_created_at
    - idx_messages_conv_created (composite)
    """

    __tablename__ = "messages"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # User ownership (CRITICAL for isolation)
    user_id: str = Field(
        foreign_key="users.id",
        nullable=False,
        max_length=255,
        index=True,
        description="Message owner"
    )

    # Conversation reference
    conversation_id: int = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True,
        description="Parent conversation"
    )

    # Message content
    role: MessageRole = Field(nullable=False, max_length=20)
    content: str = Field(nullable=False, max_length=5000, description="Message text")

    # Timestamp (UTC per constitution.md section 7.4)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Message timestamp (for ordering)"
    )

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": 456,
                "user_id": "user_123abc",
                "conversation_id": 123,
                "role": "user",
                "content": "Add meeting with client tomorrow at 3pm",
                "created_at": "2025-12-27T10:30:00Z"
            }
        }


# Indexes will be created via Alembic migrations (database/schema.md section "Table 4: messages")
# - CREATE INDEX idx_messages_user_id ON messages(user_id);
# - CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
# - CREATE INDEX idx_messages_created_at ON messages(created_at);
# - CREATE INDEX idx_messages_conv_created ON messages(conversation_id, created_at);

__all__ = ["Message", "MessageRole"]
