"""
Contract analysis endpoints for ClauseLens AI API.
Handles contract ingestion, verification, and analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.contract import (
    ContractAnalysisRequest,
    ContractAnalysisResponse,
    ContractVerificationResponse
)
from app.services.contract import ContractService

router = APIRouter()


@router.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(
    analysis_request: ContractAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start analysis of a smart contract.
    
    Args:
        analysis_request: Contract analysis request data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Analysis response with status and estimated duration
    
    Raises:
        HTTPException: If analysis fails to start
    """
    contract_service = ContractService(db)
    
    # Start contract analysis
    analysis = await contract_service.start_analysis(
        user_id=current_user.id,
        analysis_request=analysis_request
    )
    
    return ContractAnalysisResponse(
        analysis_id=analysis.id,
        status=analysis.status,
        estimated_duration=analysis.estimated_duration,
        project_id=analysis.project_id
    )


@router.post("/upload", response_model=ContractVerificationResponse)
async def upload_contract_source(
    project_id: str,
    source_files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload contract source code files.
    
    Args:
        project_id: Project identifier
        source_files: Contract source code files
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Verification response with contract details
    
    Raises:
        HTTPException: If upload or verification fails
    """
    contract_service = ContractService(db)
    
    # Upload and verify source files
    verification = await contract_service.upload_source_files(
        project_id=project_id,
        user_id=current_user.id,
        source_files=source_files
    )
    
    return ContractVerificationResponse(
        project_id=verification.project_id,
        verification_status=verification.status,
        contracts=verification.contracts,
        message=verification.message
    )


@router.get("/{project_id}/status")
async def get_analysis_status(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the status of contract analysis.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Analysis status and progress information
    
    Raises:
        HTTPException: If project not found
    """
    contract_service = ContractService(db)
    
    # Get analysis status
    status_info = await contract_service.get_analysis_status(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if not status_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return status_info


@router.get("/{project_id}/contracts")
async def get_project_contracts(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all contracts for a project.
    
    Args:
        project_id: Project identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        List of contracts in the project
    
    Raises:
        HTTPException: If project not found
    """
    contract_service = ContractService(db)
    
    # Get project contracts
    contracts = await contract_service.get_project_contracts(
        project_id=project_id,
        user_id=current_user.id
    )
    
    if contracts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {"contracts": contracts}


@router.get("/{contract_id}/source")
async def get_contract_source(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get contract source code.
    
    Args:
        contract_id: Contract identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Contract source code and metadata
    
    Raises:
        HTTPException: If contract not found
    """
    contract_service = ContractService(db)
    
    # Get contract source
    source = await contract_service.get_contract_source(
        contract_id=contract_id,
        user_id=current_user.id
    )
    
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    return source


@router.post("/{contract_id}/verify")
async def verify_contract(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Verify contract on blockchain explorer.
    
    Args:
        contract_id: Contract identifier
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Verification result
    
    Raises:
        HTTPException: If verification fails
    """
    contract_service = ContractService(db)
    
    # Verify contract
    result = await contract_service.verify_contract(
        contract_id=contract_id,
        user_id=current_user.id
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract verification failed"
        )
    
    return result
