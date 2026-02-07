"""
Task model for Todo Intelligence Platform.

Per constitution.md section 7.1, tasks table stores user tasks with multi-user isolation.
All queries MUST include user_id for isolation (constitution.md section 5.2).
"""

from sqlmodel import SQLModel, Field, Index
from typing import Optional
from datetime import datetime, date, time
from enum import Enum


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    """Task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELETED = "deleted"


class Task(SQLModel, table=True):
    """
    Task model with user isolation.

    CRITICAL: All queries MUST include user_id in WHERE clause (constitution.md section 5.2).

    Indexes per database/schema.md:
    - idx_tasks_user_id
    - idx_tasks_status
    - idx_tasks_priority
    - idx_tasks_due_date
    - idx_tasks_created_at
    - idx_tasks_user_status (composite)
    """

    __tablename__ = "tasks"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # User ownership (CRITICAL for isolation)
    user_id: str = Field(
        foreign_key="users.id",
        nullable=False,
        max_length=255,
        index=True,
        description="Owner of the task (enforces multi-user isolation)"
    )

    # Task details
    title: str = Field(nullable=False, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

    # Due date/time
    due_date: Optional[date] = Field(default=None)
    due_time: Optional[time] = Field(default=None)

    # Priority and status
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, nullable=False)
    status: TaskStatus = Field(default=TaskStatus.PENDING, nullable=False)

    # Completion tracking
    completed_at: Optional[datetime] = Field(default=None)

    # Timestamps (UTC per constitution.md section 7.4)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": 42,
                "user_id": "user_123abc",
                "title": "Review architecture spec",
                "description": "Complete review by EOD",
                "due_date": "2025-12-28",
                "due_time": None,
                "priority": "high",
                "status": "pending",
                "completed_at": None,
                "created_at": "2025-12-27T10:30:00Z",
                "updated_at": "2025-12-27T10:30:00Z"
            }
        }


# Indexes will be created via Alembic migrations (database/schema.md section "Table 2: tasks")
# - CREATE INDEX idx_tasks_user_id ON tasks(user_id);
# - CREATE INDEX idx_tasks_status ON tasks(status);
# - CREATE INDEX idx_tasks_priority ON tasks(priority);
# - CREATE INDEX idx_tasks_due_date ON tasks(due_date);
# - CREATE INDEX idx_tasks_created_at ON tasks(created_at);
# - CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);

__all__ = ["Task", "TaskPriority", "TaskStatus"]
