"""
Project model for Todo Intelligence Platform.
Manages project organization and task grouping.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Project(SQLModel, table=True):
    """
    Project model for organizing tasks.
    """

    __tablename__ = "projects"

    # Primary Key
    id: int = Field(default=None, primary_key=True)

    # Foreign Key
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)

    # Project details
    name: str = Field(nullable=False, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: str = Field(default="pending", max_length=50)  # pending, active, completed

    # Dates
    due_date: Optional[str] = Field(default=None, max_length=50)

    # Timestamps (UTC)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user_123",
                "name": "AI Integration",
                "description": "Integrate AI agents for task automation",
                "status": "active",
                "due_date": "2025-02-15",
                "created_at": "2025-12-27T10:30:00Z",
                "updated_at": "2025-12-27T10:30:00Z"
            }
        }


__all__ = ["Project"]
