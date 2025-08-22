"""
Project management endpoints for ClauseLens AI API.
Handles project creation, listing, and management.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectList,
    ProjectUpdate
)
from app.services.project import ProjectService

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new project for smart contract analysis.
    
    Args:
        project_data: Project creation data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Created project information
    
    Raises:
        HTTPException: If project creation fails
    """
    project_service = ProjectService(db)
    
    # Create project
    project = await project_service.create_project(
        user_id=current_user.id,
        project_data=project_data
    )
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        chain_id=project.chain_id,
        address=project.address,
        description=project.description,
        status=project.status,
        verification_status=project.verification_status,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.get("/", response_model=ProjectList)
async def list_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all projects for the authenticated user.
    
    Args:
        page: Page number
        limit: Items per page
        status_filter: Filter by project status
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Paginated list of projects
    """
    project_service = ProjectService(db)
    
    # Get projects with pagination
    projects, total = await project_service.list_projects(
        user_id=current_user.id,
        page=page,
        limit=limit,
        status_filter=status_filter
    )
    
    return ProjectList(
        projects=[
            ProjectResponse(
                id=project.id,
                name=project.name,
                chain_id=project.chain_id,
                address=project.address,
                description=project.description,
                status=project.status,
                verification_status=project.verification_status,
                created_at=project.created_at,
                updated_at=project.updated_at
            )
            for project in projects
        ],
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get project details by ID.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Project details
    
    Raises:
        HTTPException: If project not found or access denied
    """
    project_service = ProjectService(db)
    
    # Get project with access control
    project = await project_service.get_project(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        chain_id=project.chain_id,
        address=project.address,
        description=project.description,
        status=project.status,
        verification_status=project.verification_status,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update project information.
    
    Args:
        project_id: Project identifier
        project_data: Project update data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Updated project information
    
    Raises:
        HTTPException: If project not found or access denied
    """
    project_service = ProjectService(db)
    
    # Update project with access control
    project = await project_service.update_project(
        project_id=project_id,
        user_id=current_user.id,
        project_data=project_data
    )
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        chain_id=project.chain_id,
        address=project.address,
        description=project.description,
        status=project.status,
        verification_status=project.verification_status,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a project.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Raises:
        HTTPException: If project not found or access denied
    """
    project_service = ProjectService(db)
    
    # Delete project with access control
    success = await project_service.delete_project(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )


@router.post("/{project_id}/share")
async def share_project(
    project_id: str,
    email: str,
    permission: str = "read",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Share a project with another user.
    
    Args:
        project_id: Project identifier
        email: Email of user to share with
        permission: Permission level (read, write, admin)
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Success message
    
    Raises:
        HTTPException: If sharing fails
    """
    project_service = ProjectService(db)
    
    # Share project
    success = await project_service.share_project(
        project_id=project_id,
        owner_id=current_user.id,
        email=email,
        permission=permission
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to share project"
        )
    
    return {"message": "Project shared successfully"}
