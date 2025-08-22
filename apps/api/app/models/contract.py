"""
Contract model for smart contract analysis.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Contract(Base):
    """Contract model for smart contract analysis."""
    
    __tablename__ = "contracts"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Contract identification
    address: Mapped[str] = mapped_column(
        String(42), 
        nullable=False, 
        index=True
    )  # Ethereum address format
    chain_id: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        index=True
    )  # Chain ID (1 for Ethereum mainnet, etc.)
    name: Mapped[Optional[str]] = mapped_column(
        String(255), 
        nullable=True
    )
    
    # Contract data
    source_code: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    abi: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True
    )
    bytecode: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True
    )
    
    # Analysis status
    analysis_status: Mapped[str] = mapped_column(
        String(20), 
        default="pending",
        nullable=False
    )  # pending, analyzing, completed, failed
    
    # Analysis metadata
    analysis_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True
    )
    analysis_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True
    )
    analysis_duration: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True
    )  # Duration in seconds
    
    # Analysis results
    analysis_summary: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True
    )
    risk_score: Mapped[Optional[float]] = mapped_column(
        nullable=True
    )  # 0.0 to 1.0
    
    # Project relationship
    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        ForeignKey("projects.id", ondelete="CASCADE"), 
        nullable=False
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    
    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", 
        back_populates="contracts"
    )
    findings: Mapped[List["SecurityFinding"]] = relationship(
        "SecurityFinding", 
        back_populates="contract", 
        cascade="all, delete-orphan"
    )
    risks: Mapped[List["RiskAssessment"]] = relationship(
        "RiskAssessment", 
        back_populates="contract", 
        cascade="all, delete-orphan"
    )
    
    # Methods
    def __repr__(self) -> str:
        return f"<Contract(id={self.id}, address={self.address}, chain_id={self.chain_id})>"
    
    @property
    def findings_count(self) -> dict:
        """Get count of findings by severity."""
        counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for finding in self.findings:
            counts[finding.severity] += 1
        return counts
    
    @property
    def risks_count(self) -> dict:
        """Get count of risks by level."""
        counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for risk in self.risks:
            counts[risk.risk_level] += 1
        return counts
    
    @property
    def has_critical_issues(self) -> bool:
        """Check if contract has critical findings or risks."""
        critical_findings = any(f.severity == "critical" for f in self.findings)
        critical_risks = any(r.risk_level == "critical" for r in self.risks)
        return critical_findings or critical_risks
    
    def to_dict(self) -> dict:
        """Convert contract to dictionary for API responses."""
        return {
            "id": self.id,
            "address": self.address,
            "chain_id": self.chain_id,
            "name": self.name,
            "analysis_status": self.analysis_status,
            "analysis_started_at": self.analysis_started_at.isoformat() if self.analysis_started_at else None,
            "analysis_completed_at": self.analysis_completed_at.isoformat() if self.analysis_completed_at else None,
            "analysis_duration": self.analysis_duration,
            "analysis_summary": self.analysis_summary,
            "risk_score": self.risk_score,
            "project_id": self.project_id,
            "findings_count": self.findings_count,
            "risks_count": self.risks_count,
            "has_critical_issues": self.has_critical_issues,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
