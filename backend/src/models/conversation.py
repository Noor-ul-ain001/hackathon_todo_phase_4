"""
Conversation model for Todo Intelligence Platform.

Per constitution.md section 2.2, conversations store stateless chat threads.
All conversation context reconstructed from messages table on each request.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Conversation(SQLModel, table=True):
    """
    Conversation thread model.

    Tracks conversation threads for stateless chat.
    Messages are stored in separate messages table.

    Indexes per database/schema.md:
    - idx_conversations_user_id
    - idx_conversations_updated_at
    """

    __tablename__ = "conversations"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # User ownership (CRITICAL for isolation)
    user_id: str = Field(
        foreign_key="users.id",
        nullable=False,
        max_length=255,
        index=True,
        description="Owner of the conversation"
    )

    # Timestamps (UTC per constitution.md section 7.4)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Last message timestamp"
    )

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": 123,
                "user_id": "user_123abc",
                "created_at": "2025-12-27T10:00:00Z",
                "updated_at": "2025-12-27T10:30:00Z"
            }
        }


# Indexes will be created via Alembic migrations (database/schema.md section "Table 3: conversations")
# - CREATE INDEX idx_conversations_user_id ON conversations(user_id);
# - CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);

__all__ = ["Conversation"]
