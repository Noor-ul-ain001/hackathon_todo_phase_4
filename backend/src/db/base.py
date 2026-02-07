"""
Database base configuration for SQLModel.

Provides base class for all database models using SQLModel.
"""

from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


# Re-export SQLModel as Base for consistency
Base = SQLModel


# ==============================================
# Base Model Mixin
# ==============================================

class TimestampMixin:
    """
    Mixin for created_at and updated_at timestamps.

    All models should include these fields per constitution.md section 7.4.
    """
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ==============================================
# Metadata
# ==============================================

# All models will inherit from SQLModel
# Alembic will use SQLModel.metadata for autogeneration

__all__ = ["Base", "SQLModel", "TimestampMixin"]
