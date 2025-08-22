"""
SecurityFinding model for storing security analysis results.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class SecurityFinding(Base):
    """SecurityFinding model for storing security analysis results."""
    
    __tablename__ = "security_findings"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Finding details
    title: Mapped[str] = mapped_column(
        String(500), 
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    recommendation: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    
    # Classification
    severity: Mapped[str] = mapped_column(
        String(20), 
        nullable=False,
        index=True
    )  # low, medium, high, critical
    
    category: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        index=True
    )  # access-control, arithmetic, reentrancy, gas, other
    
    # Location information
    line_number: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True
    )
    function_name: Mapped[Optional[str]] = mapped_column(
        String(255), 
        nullable=True
    )
    file_name: Mapped[Optional[str]] = mapped_column(
        String(255), 
        nullable=True
    )
    
    # Analysis metadata
    tool: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
    )  # slither, semgrep, ai-analysis
    
    confidence: Mapped[Optional[float]] = mapped_column(
        nullable=True
    )  # 0.0 to 1.0
    
    # Additional data
    metadata: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True
    )  # Additional tool-specific data
    
    # Contract relationship
    contract_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        ForeignKey("contracts.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )
    
    # Relationships
    contract: Mapped["Contract"] = relationship(
        "Contract", 
        back_populates="findings"
    )
    
    # Methods
    def __repr__(self) -> str:
        return f"<SecurityFinding(id={self.id}, severity={self.severity}, category={self.category})>"
    
    @property
    def severity_score(self) -> int:
        """Get numeric severity score for sorting."""
        scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return scores.get(self.severity, 0)
    
    @property
    def is_critical(self) -> bool:
        """Check if finding is critical severity."""
        return self.severity == "critical"
    
    @property
    def is_high_or_critical(self) -> bool:
        """Check if finding is high or critical severity."""
        return self.severity in ["high", "critical"]
    
    def to_dict(self) -> dict:
        """Convert finding to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "recommendation": self.recommendation,
            "severity": self.severity,
            "category": self.category,
            "line_number": self.line_number,
            "function_name": self.function_name,
            "file_name": self.file_name,
            "tool": self.tool,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "contract_id": self.contract_id,
            "severity_score": self.severity_score,
            "is_critical": self.is_critical,
            "is_high_or_critical": self.is_high_or_critical,
            "created_at": self.created_at.isoformat(),
        }
