"""
Report generation endpoints for ClauseLens AI API.
Handles report creation and management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.report import (
    ReportCreate,
    ReportResponse,
    ReportList
)
from app.services.report import ReportService

router = APIRouter()


@router.post("/{project_id}/generate", response_model=ReportResponse)
async def generate_report(
    project_id: str,
    report_data: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a comprehensive analysis report.
    
    Args:
        project_id: Project identifier
        report_data: Report generation parameters
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Report generation response with status
    
    Raises:
        HTTPException: If report generation fails
    """
    report_service = ReportService(db)
    
    # Generate report
    report = await report_service.generate_report(
        project_id=project_id,
        user_id=current_user.id,
        report_data=report_data
    )
    
    return ReportResponse(
        report_id=report.id,
        status=report.status,
        download_url=report.download_url,
        estimated_completion=report.estimated_completion
    )


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report_status(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get report status and download URL.
    
    Args:
        report_id: Report identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Report status and download information
    
    Raises:
        HTTPException: If report not found
    """
    report_service = ReportService(db)
    
    # Get report status
    report = await report_service.get_report_status(
        report_id=report_id,
        user_id=current_user.id
    )
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report


@router.get("/project/{project_id}/reports", response_model=ReportList)
async def list_project_reports(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all reports for a project.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        List of project reports
    
    Raises:
        HTTPException: If project not found
    """
    report_service = ReportService(db)
    
    # Get project reports
    reports = await report_service.list_project_reports(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if reports is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return reports


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a report.
    
    Args:
        report_id: Report identifier
        current_user: Current authenticated user
        db: Database session
    
    Raises:
        HTTPException: If report not found
    """
    report_service = ReportService(db)
    
    # Delete report
    success = await report_service.delete_report(
        report_id=report_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )


@router.post("/{report_id}/share")
async def share_report(
    report_id: str,
    email: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Share a report via email.
    
    Args:
        report_id: Report identifier
        email: Email address to share with
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Success message
    
    Raises:
        HTTPException: If sharing fails
    """
    report_service = ReportService(db)
    
    # Share report
    success = await report_service.share_report(
        report_id=report_id,
        user_id=current_user.id,
        email=email
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to share report"
        )
    
    return {"message": "Report shared successfully"}


@router.get("/{report_id}/download")
async def download_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Download a generated report.
    
    Args:
        report_id: Report identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Report file for download
    
    Raises:
        HTTPException: If report not found or not ready
    """
    report_service = ReportService(db)
    
    # Get report download
    download = await report_service.download_report(
        report_id=report_id,
        user_id=current_user.id
    )
    
    if not download:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not ready"
        )
    
    return download
