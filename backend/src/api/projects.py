"""
Project CRUD API endpoints for Todo Intelligence Platform.
Provides REST API for project management.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path as PathParam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

from ..db.connection import get_db
from ..models.project import Project
from ..models.task import Task

router = APIRouter()


# Request/Response Models
class ProjectCreate(BaseModel):
    """Request model for creating a project."""
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: str | None = Field(default=None, max_length=2000, description="Optional description")
    due_date: str | None = Field(default=None, description="Due date (YYYY-MM-DD format)")


class ProjectUpdate(BaseModel):
    """Request model for updating a project."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    due_date: str | None = Field(default=None)
    status: str | None = Field(default=None)


class ProjectStats(BaseModel):
    """Project statistics."""
    total_tasks: int = 0
    completed_tasks: int = 0
    progress: int = 0  # Percentage
    members: int = 1  # Default to 1 for single user


class ProjectResponse(BaseModel):
    """Response model for a project."""
    id: int
    user_id: str
    name: str
    description: str | None
    status: str
    due_date: str | None = None
    created_at: datetime
    updated_at: datetime
    tasks: ProjectStats | None = None

    class Config:
        from_attributes = True


# GET /api/{user_id}/projects - List all projects for user
@router.get("/{user_id}/projects", response_model=List[ProjectResponse])
async def get_projects(
    user_id: str = PathParam(..., description="User ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all projects for a user with task statistics.
    """
    try:
        # Get all projects for user
        query = select(Project).where(Project.user_id == user_id).order_by(Project.created_at.desc())
        result = await db.execute(query)
        projects = result.scalars().all()

        # Enhance with task stats
        response_projects = []
        for project in projects:
            # Count total tasks (future: add project_id to Task model)
            # For now, return project without task stats
            project_dict = {
                "id": project.id,
                "user_id": project.user_id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "due_date": project.due_date,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
                "tasks": {
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "progress": 0 if project.status != "completed" else 100,
                    "members": 1
                }
            }
            response_projects.append(ProjectResponse(**project_dict))

        return response_projects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch projects: {str(e)}"
        )


# GET /api/{user_id}/projects/{project_id} - Get specific project
@router.get("/{user_id}/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    user_id: str = PathParam(..., description="User ID"),
    project_id: int = PathParam(..., description="Project ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific project by ID."""
    try:
        query = select(Project).where(
            Project.id == project_id,
            Project.user_id == user_id
        )
        result = await db.execute(query)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch project: {str(e)}"
        )


# POST /api/{user_id}/projects - Create new project
@router.post("/{user_id}/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    user_id: str = PathParam(..., description="User ID"),
    project_data: ProjectCreate = ...,
    db: AsyncSession = Depends(get_db)
):
    """Create a new project."""
    try:
        project = Project(
            user_id=user_id,
            name=project_data.name,
            description=project_data.description,
            status="pending",
            due_date=project_data.due_date,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(project)
        await db.commit()
        await db.refresh(project)

        return project
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )


# PUT /api/{user_id}/projects/{project_id} - Update project
@router.put("/{user_id}/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    user_id: str = PathParam(..., description="User ID"),
    project_id: int = PathParam(..., description="Project ID"),
    project_data: ProjectUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    """Update a project."""
    try:
        query = select(Project).where(
            Project.id == project_id,
            Project.user_id == user_id
        )
        result = await db.execute(query)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        # Update fields if provided
        if project_data.name is not None:
            project.name = project_data.name
        if project_data.description is not None:
            project.description = project_data.description
        if project_data.due_date is not None:
            project.due_date = project_data.due_date
        if project_data.status is not None:
            project.status = project_data.status

        project.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(project)

        return project
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update project: {str(e)}"
        )


# DELETE /api/{user_id}/projects/{project_id} - Delete project
@router.delete("/{user_id}/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    user_id: str = PathParam(..., description="User ID"),
    project_id: int = PathParam(..., description="Project ID"),
    db: AsyncSession = Depends(get_db)
):
    """Delete a project permanently."""
    try:
        query = select(Project).where(
            Project.id == project_id,
            Project.user_id == user_id
        )
        result = await db.execute(query)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        await db.delete(project)
        await db.commit()

        return None
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete project: {str(e)}"
        )
