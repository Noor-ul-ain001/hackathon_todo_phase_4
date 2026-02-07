"""
Task CRUD API endpoints for Todo Intelligence Platform.
Provides REST API for task management alongside the AI chat interface.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path as PathParam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

from ..db.connection import get_db
from ..models.task import Task, TaskStatus, TaskPriority

router = APIRouter()


# Request/Response Models
class TaskCreate(BaseModel):
    """Request model for creating a task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(default=None, max_length=2000, description="Optional description")
    due_date: str | None = Field(default=None, description="Due date (ISO format)")
    priority: str = Field(default="medium", description="Priority level: low, medium, high")


class TaskUpdate(BaseModel):
    """Request model for updating a task."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    due_date: str | None = Field(default=None)
    priority: str | None = Field(default=None)
    status: str | None = Field(default=None)


class TaskResponse(BaseModel):
    """Response model for a task."""
    id: int
    user_id: str
    title: str
    description: str | None
    status: str
    priority: str
    due_date: str | None = None
    due_time: str | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# GET /api/{user_id}/tasks - List all tasks for user
@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str = PathParam(..., description="User ID"),
    db: AsyncSession = Depends(get_db),
    status_filter: str | None = None
):
    """
    Get all tasks for a user.

    Args:
        user_id: User ID
        status_filter: Optional filter by status (pending, in_progress, completed)

    Returns:
        List of tasks
    """
    try:
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter if provided
        if status_filter:
            query = query.where(Task.status == status_filter)

        # Order by created_at descending (newest first)
        query = query.order_by(Task.created_at.desc())

        result = await db.execute(query)
        tasks = result.scalars().all()

        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tasks: {str(e)}"
        )


# GET /api/{user_id}/tasks/{task_id} - Get specific task
@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str = PathParam(..., description="User ID"),
    task_id: int = PathParam(..., description="Task ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific task by ID."""
    try:
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch task: {str(e)}"
        )


# POST /api/{user_id}/tasks - Create new task
@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str = PathParam(..., description="User ID"),
    task_data: TaskCreate = ...,
    db: AsyncSession = Depends(get_db)
):
    """Create a new task."""
    try:
        # Parse priority
        try:
            priority = TaskPriority(task_data.priority.lower())
        except ValueError:
            priority = TaskPriority.MEDIUM

        # Create task
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            status=TaskStatus.PENDING,
            due_date=task_data.due_date,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


# PUT /api/{user_id}/tasks/{task_id} - Update task
@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str = PathParam(..., description="User ID"),
    task_id: int = PathParam(..., description="Task ID"),
    task_data: TaskUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    """Update a task."""
    try:
        # Find task
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update fields if provided
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.due_date is not None:
            task.due_date = task_data.due_date
        if task_data.priority is not None:
            try:
                task.priority = TaskPriority(task_data.priority.lower())
            except ValueError:
                pass
        if task_data.status is not None:
            try:
                new_status = TaskStatus(task_data.status.lower())
                task.status = new_status

                # Set completed_at if marking as completed
                if new_status == TaskStatus.COMPLETED and task.completed_at is None:
                    task.completed_at = datetime.utcnow()
                elif new_status != TaskStatus.COMPLETED:
                    task.completed_at = None
            except ValueError:
                pass

        task.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)

        return task
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


# PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion
@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str = PathParam(..., description="User ID"),
    task_id: int = PathParam(..., description="Task ID"),
    db: AsyncSession = Depends(get_db)
):
    """Toggle task completion status."""
    try:
        # Find task
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Toggle status
        if task.status == TaskStatus.COMPLETED:
            task.status = TaskStatus.PENDING
            task.completed_at = None
        else:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()

        task.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)

        return task
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle task: {str(e)}"
        )


# DELETE /api/{user_id}/tasks/{task_id} - Delete task
@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str = PathParam(..., description="User ID"),
    task_id: int = PathParam(..., description="Task ID"),
    db: AsyncSession = Depends(get_db)
):
    """Delete a task permanently."""
    try:
        # Verify task exists and belongs to user
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Delete task
        await db.delete(task)
        await db.commit()

        return None
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )
