"""
Contract analysis service.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import structlog

from app.models.contract import Contract
from app.models.project import Project
from app.models.finding import SecurityFinding
from app.models.risk import RiskAssessment
from app.models.user import User

logger = structlog.get_logger()


class ContractService:
    """Service for contract analysis operations."""
    
    async def create_contract(
        self, 
        db: AsyncSession, 
        project_id: str, 
        address: str, 
        chain_id: int, 
        source_code: str,
        name: Optional[str] = None,
        abi: Optional[Dict] = None,
        bytecode: Optional[str] = None
    ) -> Optional[Contract]:
        """Create a new contract for analysis."""
        try:
            # Validate project exists
            project_result = await db.execute(select(Project).where(Project.id == project_id))
            project = project_result.scalar_one_or_none()
            if not project:
                logger.warning("Contract creation failed: project not found", project_id=project_id)
                return None
            
            # Check if contract already exists in project
            existing_contract = await self.get_contract_by_address(db, project_id, address, chain_id)
            if existing_contract:
                logger.warning("Contract already exists in project", project_id=project_id, address=address)
                return existing_contract
            
            # Create new contract
            contract = Contract(
                project_id=project_id,
                address=address,
                chain_id=chain_id,
                name=name or f"Contract_{address[:8]}",
                source_code=source_code,
                abi=abi,
                bytecode=bytecode,
                analysis_status="pending"
            )
            
            db.add(contract)
            await db.commit()
            await db.refresh(contract)
            
            logger.info("Contract created successfully", contract_id=contract.id, address=address)
            return contract
            
        except Exception as e:
            logger.error("Error creating contract", error=str(e), project_id=project_id, address=address)
            await db.rollback()
            return None
    
    async def get_contract_by_id(self, db: AsyncSession, contract_id: str) -> Optional[Contract]:
        """Get contract by ID."""
        try:
            result = await db.execute(select(Contract).where(Contract.id == contract_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting contract by ID", error=str(e), contract_id=contract_id)
            return None
    
    async def get_contract_by_address(
        self, 
        db: AsyncSession, 
        project_id: str, 
        address: str, 
        chain_id: int
    ) -> Optional[Contract]:
        """Get contract by address and chain ID within a project."""
        try:
            result = await db.execute(
                select(Contract).where(
                    and_(
                        Contract.project_id == project_id,
                        Contract.address == address,
                        Contract.chain_id == chain_id
                    )
                )
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting contract by address", error=str(e), address=address)
            return None
    
    async def get_project_contracts(
        self, 
        db: AsyncSession, 
        project_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Contract]:
        """Get all contracts for a project with pagination."""
        try:
            result = await db.execute(
                select(Contract)
                .where(Contract.project_id == project_id)
                .offset(skip)
                .limit(limit)
                .order_by(Contract.created_at.desc())
            )
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting project contracts", error=str(e), project_id=project_id)
            return []
    
    async def update_contract_status(
        self, 
        db: AsyncSession, 
        contract_id: str, 
        status: str
    ) -> bool:
        """Update contract analysis status."""
        try:
            contract = await self.get_contract_by_id(db, contract_id)
            if not contract:
                return False
            
            contract.analysis_status = status
            
            if status == "analyzing":
                contract.analysis_started_at = datetime.utcnow()
            elif status in ["completed", "failed"]:
                contract.analysis_completed_at = datetime.utcnow()
                if contract.analysis_started_at:
                    duration = (contract.analysis_completed_at - contract.analysis_started_at).total_seconds()
                    contract.analysis_duration = int(duration)
            
            await db.commit()
            
            logger.info("Contract status updated", contract_id=contract_id, status=status)
            return True
            
        except Exception as e:
            logger.error("Error updating contract status", error=str(e), contract_id=contract_id)
            await db.rollback()
            return False
    
    async def update_contract_analysis_results(
        self, 
        db: AsyncSession, 
        contract_id: str, 
        analysis_summary: str,
        risk_score: float,
        findings: List[Dict[str, Any]],
        risks: List[Dict[str, Any]]
    ) -> bool:
        """Update contract with analysis results."""
        try:
            contract = await self.get_contract_by_id(db, contract_id)
            if not contract:
                return False
            
            # Update contract analysis results
            contract.analysis_summary = analysis_summary
            contract.risk_score = risk_score
            
            # Create security findings
            for finding_data in findings:
                finding = SecurityFinding(
                    contract_id=contract_id,
                    title=finding_data["title"],
                    description=finding_data["description"],
                    recommendation=finding_data["recommendation"],
                    severity=finding_data["severity"],
                    category=finding_data["category"],
                    line_number=finding_data.get("line_number"),
                    function_name=finding_data.get("function_name"),
                    file_name=finding_data.get("file_name"),
                    tool=finding_data.get("tool", "ai-analysis"),
                    confidence=finding_data.get("confidence"),
                    metadata=finding_data.get("metadata")
                )
                db.add(finding)
            
            # Create risk assessments
            for risk_data in risks:
                risk = RiskAssessment(
                    contract_id=contract_id,
                    title=risk_data["title"],
                    description=risk_data["description"],
                    impact=risk_data["impact"],
                    mitigation=risk_data["mitigation"],
                    risk_level=risk_data["risk_level"],
                    category=risk_data["category"],
                    probability=risk_data["probability"],
                    impact_score=risk_data.get("impact_score"),
                    risk_score=risk_data.get("risk_score"),
                    metadata=risk_data.get("metadata")
                )
                db.add(risk)
            
            await db.commit()
            
            logger.info("Contract analysis results updated", contract_id=contract_id)
            return True
            
        except Exception as e:
            logger.error("Error updating contract analysis results", error=str(e), contract_id=contract_id)
            await db.rollback()
            return False
    
    async def delete_contract(self, db: AsyncSession, contract_id: str) -> bool:
        """Delete a contract and all its associated data."""
        try:
            contract = await self.get_contract_by_id(db, contract_id)
            if not contract:
                return False
            
            await db.delete(contract)
            await db.commit()
            
            logger.info("Contract deleted", contract_id=contract_id)
            return True
            
        except Exception as e:
            logger.error("Error deleting contract", error=str(e), contract_id=contract_id)
            await db.rollback()
            return False
    
    async def get_contract_findings(
        self, 
        db: AsyncSession, 
        contract_id: str,
        severity: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[SecurityFinding]:
        """Get security findings for a contract with optional filtering."""
        try:
            query = select(SecurityFinding).where(SecurityFinding.contract_id == contract_id)
            
            if severity:
                query = query.where(SecurityFinding.severity == severity)
            if category:
                query = query.where(SecurityFinding.category == category)
            
            query = query.order_by(SecurityFinding.severity_score.desc(), SecurityFinding.created_at.desc())
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("Error getting contract findings", error=str(e), contract_id=contract_id)
            return []
    
    async def get_contract_risks(
        self, 
        db: AsyncSession, 
        contract_id: str,
        risk_level: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[RiskAssessment]:
        """Get risk assessments for a contract with optional filtering."""
        try:
            query = select(RiskAssessment).where(RiskAssessment.contract_id == contract_id)
            
            if risk_level:
                query = query.where(RiskAssessment.risk_level == risk_level)
            if category:
                query = query.where(RiskAssessment.category == category)
            
            query = query.order_by(RiskAssessment.risk_level_score.desc(), RiskAssessment.created_at.desc())
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("Error getting contract risks", error=str(e), contract_id=contract_id)
            return []
    
    def can_user_access_contract(self, user: User, contract: Contract) -> bool:
        """Check if user can access a specific contract."""
        # Admin can access all contracts
        if user.is_admin:
            return True
        
        # Check if user owns the project
        return contract.project.user_id == user.id
