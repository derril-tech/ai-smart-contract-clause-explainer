"""
Analysis results endpoints for ClauseLens AI API.
Handles retrieval of analysis results and findings.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.analysis import (
    AnalysisResultsResponse,
    AnalysisFindingsResponse,
    RiskAssessmentResponse
)
from app.services.analysis import AnalysisService

router = APIRouter()


@router.get("/{project_id}/results", response_model=AnalysisResultsResponse)
async def get_analysis_results(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get analysis results for a project.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Complete analysis results
    
    Raises:
        HTTPException: If project not found or analysis not completed
    """
    analysis_service = AnalysisService(db)
    
    # Get analysis results
    results = await analysis_service.get_analysis_results(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis results not found"
        )
    
    return results


@router.get("/{project_id}/findings", response_model=AnalysisFindingsResponse)
async def get_analysis_findings(
    project_id: str,
    severity: str = None,
    category: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get security findings from analysis.
    
    Args:
        project_id: Project identifier
        severity: Filter by severity level
        category: Filter by finding category
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Filtered security findings
    
    Raises:
        HTTPException: If project not found
    """
    analysis_service = AnalysisService(db)
    
    # Get filtered findings
    findings = await analysis_service.get_findings(
        project_id=project_id,
        user_id=current_user.id,
        severity=severity,
        category=category
    )
    
    if findings is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return findings


@router.get("/{project_id}/risks", response_model=RiskAssessmentResponse)
async def get_risk_assessment(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive risk assessment.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Risk assessment with categories and privilege mapping
    
    Raises:
        HTTPException: If project not found
    """
    analysis_service = AnalysisService(db)
    
    # Get risk assessment
    assessment = await analysis_service.get_risk_assessment(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found"
        )
    
    return assessment


@router.get("/{project_id}/storage-layout")
async def get_storage_layout(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get contract storage layout analysis.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Storage layout information
    
    Raises:
        HTTPException: If project not found
    """
    analysis_service = AnalysisService(db)
    
    # Get storage layout
    layout = await analysis_service.get_storage_layout(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if not layout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Storage layout not found"
        )
    
    return layout


@router.get("/{project_id}/gas-profile")
async def get_gas_profile(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get gas usage profile analysis.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Gas usage profile information
    
    Raises:
        HTTPException: If project not found
    """
    analysis_service = AnalysisService(db)
    
    # Get gas profile
    profile = await analysis_service.get_gas_profile(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gas profile not found"
        )
    
    return profile


@router.get("/{project_id}/oracle-dependencies")
async def get_oracle_dependencies(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get oracle dependency analysis.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Oracle dependencies and risks
    
    Raises:
        HTTPException: If project not found
    """
    analysis_service = AnalysisService(db)
    
    # Get oracle dependencies
    dependencies = await analysis_service.get_oracle_dependencies(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if dependencies is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return dependencies


@router.get("/{project_id}/mev-exposure")
async def get_mev_exposure(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get MEV (Maximal Extractable Value) exposure analysis.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        MEV exposure assessment
    
    Raises:
        HTTPException: If project not found
    """
    analysis_service = AnalysisService(db)
    
    # Get MEV exposure
    exposure = await analysis_service.get_mev_exposure(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if exposure is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return exposure
