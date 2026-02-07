"""
User Profile and Settings API endpoints for Todo Intelligence Platform.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path as PathParam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict
from datetime import datetime
from pydantic import BaseModel, Field

from ..db.connection import get_db
from ..models.user import User
from ..models.task import Task, TaskStatus
from ..models.project import Project

router = APIRouter()


# Request/Response Models
class UserProfileResponse(BaseModel):
    """User profile response."""
    id: str
    email: str
    name: str = "User"  # Default name
    role: str = "User"
    join_date: str
    bio: str = ""
    location: str = ""
    website: str = ""
    tasks_completed: int = 0
    projects_managed: int = 0
    streak: int = 0

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """User profile update request."""
    name: str | None = None
    email: str | None = None
    bio: str | None = None
    location: str | None = None
    website: str | None = None


class UserSettings(BaseModel):
    """User settings."""
    notifications: Dict[str, bool] = {
        "email": True,
        "push": True,
        "sms": False
    }
    theme: str = "light"
    language: str = "en"


class UserSettingsUpdate(BaseModel):
    """User settings update request."""
    notifications: Dict[str, bool] | None = None
    theme: str | None = None
    language: str | None = None


# GET /api/{user_id}/profile - Get user profile
@router.get("/{user_id}/profile", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: str = PathParam(..., description="User ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user profile with statistics.
    """
    try:
        # Get user
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Get task statistics
        task_query = select(Task).where(Task.user_id == user_id)
        task_result = await db.execute(task_query)
        tasks = task_result.scalars().all()
        tasks_completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)

        # Get project statistics
        project_query = select(Project).where(Project.user_id == user_id)
        project_result = await db.execute(project_query)
        projects = project_result.scalars().all()
        projects_managed = len(projects)

        # Calculate streak (simplified - consecutive days with completed tasks)
        # In production, you'd calculate this from actual completion dates
        streak = min(tasks_completed // 2, 30)  # Simple estimate

        # Format join date
        join_date = user.created_at.strftime("%b %d, %Y")

        # Extract name from email (before @)
        name = user.email.split('@')[0].capitalize()

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            name=name,
            role="User",
            join_date=join_date,
            bio=f"Task management user with {tasks_completed} completed tasks.",
            location="",
            website="",
            tasks_completed=tasks_completed,
            projects_managed=projects_managed,
            streak=streak
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user profile: {str(e)}"
        )


# PUT /api/{user_id}/profile - Update user profile
@router.put("/{user_id}/profile", response_model=UserProfileResponse)
async def update_user_profile(
    user_id: str = PathParam(..., description="User ID"),
    profile_data: UserProfileUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    """
    Update user profile.
    Note: Extended profile fields would need a separate UserProfile table.
    For now, only email can be updated in the User table.
    """
    try:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update email if provided
        if profile_data.email is not None:
            user.email = profile_data.email

        user.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(user)

        # Return full profile
        return await get_user_profile(user_id, db)

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user profile: {str(e)}"
        )


# GET /api/{user_id}/settings - Get user settings
@router.get("/{user_id}/settings", response_model=UserSettings)
async def get_user_settings(
    user_id: str = PathParam(..., description="User ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user settings.
    Note: Settings are currently stored as defaults.
    In production, you'd have a UserSettings table.
    """
    try:
        # Verify user exists
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Return default settings
        return UserSettings(
            notifications={
                "email": True,
                "push": True,
                "sms": False
            },
            theme="light",
            language="en"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user settings: {str(e)}"
        )


# PUT /api/{user_id}/settings - Update user settings
@router.put("/{user_id}/settings", response_model=UserSettings)
async def update_user_settings(
    user_id: str = PathParam(..., description="User ID"),
    settings_data: UserSettingsUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    """
    Update user settings.
    Note: Settings updates are accepted but not persisted yet.
    In production, you'd have a UserSettings table.
    """
    try:
        # Verify user exists
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # In production, you would save these to a UserSettings table
        # For now, return the updated settings
        current_settings = UserSettings()

        if settings_data.notifications is not None:
            current_settings.notifications = settings_data.notifications
        if settings_data.theme is not None:
            current_settings.theme = settings_data.theme
        if settings_data.language is not None:
            current_settings.language = settings_data.language

        return current_settings

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user settings: {str(e)}"
        )
