"""
Enhanced contract analysis endpoints with AI integration.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.contract import (
    ContractAnalysisRequest,
    ContractAnalysisResponse,
    ContractUploadRequest,
    ContractVerificationRequest,
    ContractResponse,
    ContractAnalysisResult
)
from app.services.contract_service import contract_service
from app.services.project_service import project_service
from app.services.analysis_service import analysis_service

router = APIRouter()


@router.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(
    request: ContractAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Initiate comprehensive smart contract analysis using AI and static analysis tools.
    
    This endpoint starts a comprehensive analysis process that includes:
    - AI-powered security analysis using GPT-4 and Claude
    - Static analysis using Slither, Mythril, and Semgrep
    - Gas optimization analysis
    - Compliance and best practices checking
    """
    try:
        # Create a default project for the user if none exists
        # In a real implementation, you'd get this from the request
        user_projects = await project_service.get_user_projects(db, current_user.id, limit=1)
        if not user_projects:
            # Create default project
            default_project = await project_service.create_project(
                db=db,
                user_id=current_user.id,
                name="Default Project",
                description="Default project for contract analyses"
            )
            project_id = default_project.id
        else:
            project_id = user_projects[0].id
        
        # Check if contract already exists
        existing_contract = await contract_service.get_contract_by_address(
            db, project_id, request.contract_address, request.chain_id
        )
        
        if existing_contract and existing_contract.analysis_status == "analyzing":
            return ContractAnalysisResponse(
                contract_id=existing_contract.id,
                analysis_id=existing_contract.id,
                status="analyzing",
                estimated_duration=300,
                message="Analysis already in progress"
            )
        
        # Create or update contract
        if existing_contract:
            contract = existing_contract
        else:
            # TODO: Fetch source code from blockchain explorer
            # For now, use placeholder
            contract = await contract_service.create_contract(
                db=db,
                project_id=project_id,
                address=request.contract_address,
                chain_id=request.chain_id,
                source_code="// Source code will be fetched from blockchain explorer",
                name=f"Contract_{request.contract_address[:8]}"
            )
        
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create contract entry"
            )
        
        # Start comprehensive analysis in background
        background_tasks.add_task(
            analysis_service.analyze_contract_comprehensive,
            db,
            contract,
            request.analysis_type or ["security", "risk", "gas", "compliance"],
            True,  # use_ai
            True   # use_static_analysis
        )
        
        return ContractAnalysisResponse(
            contract_id=contract.id,
            analysis_id=contract.id,
            status="pending",
            estimated_duration=300,  # 5 minutes estimate
            message="Comprehensive analysis initiated successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate analysis: {str(e)}"
        )


@router.post("/upload")
async def upload_contract_source(
    request: ContractUploadRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload smart contract source code for comprehensive analysis.
    
    This endpoint allows uploading contract source code files for analysis
    without requiring a deployed contract address. The analysis will include
    all available tools and AI models.
    """
    try:
        # Verify project access
        project = await project_service.get_project_by_id(db, request.project_id)
        if not project or not project_service.can_user_access_project(current_user, project):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or access denied"
            )
        
        # Combine source files into single source code
        combined_source = ""
        file_list = []
        for filename, content in request.source_files.items():
            combined_source += f"// File: {filename}\n{content}\n\n"
            file_list.append(filename)
        
        # Create contract entry
        contract = await contract_service.create_contract(
            db=db,
            project_id=request.project_id,
            address="0x" + "0" * 40,  # Placeholder address for uploaded contracts
            chain_id=1,  # Default to mainnet
            source_code=combined_source,
            name=request.contract_name or f"Uploaded Contract ({', '.join(file_list[:3])})",
            abi=request.abi,
            bytecode=request.bytecode
        )
        
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create contract entry"
            )
        
        # Start comprehensive analysis in background
        background_tasks.add_task(
            analysis_service.analyze_contract_comprehensive,
            db,
            contract,
            ["security", "risk", "gas", "compliance"],
            True,  # use_ai
            True   # use_static_analysis
        )
        
        return {
            "message": "Contract uploaded and comprehensive analysis started",
            "contract_id": contract.id,
            "status": "analyzing",
            "files_uploaded": len(request.source_files),
            "analysis_types": ["security", "risk", "gas", "compliance"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload contract: {str(e)}"
        )


@router.get("/{contract_id}/status")
async def get_analysis_status(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed analysis status and progress information.
    
    Returns comprehensive status including progress, estimated time remaining,
    and preliminary results if available.
    """
    try:
        contract = await contract_service.get_contract_by_id(db, contract_id)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        
        # Check access permissions
        if not contract_service.can_user_access_contract(current_user, contract):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Calculate progress percentage
        progress = 0
        if contract.analysis_status == "pending":
            progress = 0
        elif contract.analysis_status == "analyzing":
            progress = 50  # Assume 50% progress when analyzing
        elif contract.analysis_status == "completed":
            progress = 100
        elif contract.analysis_status == "failed":
            progress = 0
        
        # Estimate remaining time
        estimated_remaining = 0
        if contract.analysis_status == "analyzing" and contract.analysis_started_at:
            elapsed = (datetime.utcnow() - contract.analysis_started_at).total_seconds()
            estimated_total = 300  # 5 minutes
            estimated_remaining = max(0, estimated_total - elapsed)
        
        return {
            "contract_id": contract.id,
            "status": contract.analysis_status,
            "progress": progress,
            "started_at": contract.analysis_started_at,
            "completed_at": contract.analysis_completed_at,
            "duration": contract.analysis_duration,
            "estimated_remaining": estimated_remaining,
            "risk_score": contract.risk_score,
            "summary": contract.analysis_summary,
            "contract_info": {
                "address": contract.address,
                "name": contract.name,
                "chain_id": contract.chain_id
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis status: {str(e)}"
        )


@router.get("/{contract_id}/results", response_model=ContractAnalysisResult)
async def get_comprehensive_analysis_results(
    contract_id: str,
    include_details: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive analysis results including AI and static analysis findings.
    
    Returns detailed analysis results from all analysis tools and AI models,
    including security findings, risk assessments, gas optimizations,
    and compliance issues.
    """
    try:
        contract = await contract_service.get_contract_by_id(db, contract_id)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        
        # Check access permissions
        if not contract_service.can_user_access_contract(current_user, contract):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        if contract.analysis_status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Analysis not completed yet. Current status: {contract.analysis_status}"
            )
        
        # Get comprehensive results
        results = await analysis_service.get_analysis_results(db, contract_id)
        
        # Add analysis metadata
        results["metadata"] = {
            "analysis_duration": contract.analysis_duration,
            "analysis_completed_at": contract.analysis_completed_at,
            "tools_used": ["slither", "mythril", "semgrep", "gpt-4", "claude-3"],
            "analysis_version": "1.0.0"
        }
        
        return ContractAnalysisResult(**results)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis results: {str(e)}"
        )


@router.get("/{contract_id}/findings")
async def get_security_findings(
    contract_id: str,
    severity: Optional[str] = None,
    category: Optional[str] = None,
    tool: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get filtered security findings for a contract.
    
    Allows filtering by severity, category, or analysis tool.
    """
    try:
        contract = await contract_service.get_contract_by_id(db, contract_id)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        
        # Check access permissions
        if not contract_service.can_user_access_contract(current_user, contract):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get filtered findings
        findings = await contract_service.get_contract_findings(
            db, contract_id, severity, category
        )
        
        # Filter by tool if specified
        if tool:
            findings = [f for f in findings if f.tool == tool]
        
        return {
            "contract_id": contract_id,
            "findings": [finding.to_dict() for finding in findings],
            "total_count": len(findings),
            "filters_applied": {
                "severity": severity,
                "category": category,
                "tool": tool
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get security findings: {str(e)}"
        )


@router.get("/{contract_id}/risks")
async def get_risk_assessments(
    contract_id: str,
    risk_level: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get risk assessments for a contract.
    
    Allows filtering by risk level or category.
    """
    try:
        contract = await contract_service.get_contract_by_id(db, contract_id)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        
        # Check access permissions
        if not contract_service.can_user_access_contract(current_user, contract):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get filtered risks
        risks = await contract_service.get_contract_risks(
            db, contract_id, risk_level, category
        )
        
        return {
            "contract_id": contract_id,
            "risks": [risk.to_dict() for risk in risks],
            "total_count": len(risks),
            "filters_applied": {
                "risk_level": risk_level,
                "category": category
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get risk assessments: {str(e)}"
        )


@router.get("/project/{project_id}", response_model=List[ContractResponse])
async def get_project_contracts(
    project_id: str,
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all contracts for a specific project with filtering options.
    
    Returns a paginated list of contracts with optional status filtering.
    """
    try:
        # Verify project access
        project = await project_service.get_project_by_id(db, project_id)
        if not project or not project_service.can_user_access_project(current_user, project):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or access denied"
            )
        
        contracts = await contract_service.get_project_contracts(db, project_id, skip, limit)
        
        # Filter by status if specified
        if status_filter:
            contracts = [c for c in contracts if c.analysis_status == status_filter]
        
        return [ContractResponse(**contract.to_dict()) for contract in contracts]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get project contracts: {str(e)}"
        )
