"""
RiskAssessment model for storing risk analysis results.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class RiskAssessment(Base):
    """RiskAssessment model for storing risk analysis results."""
    
    __tablename__ = "risk_assessments"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Risk details
    title: Mapped[str] = mapped_column(
        String(500), 
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    impact: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    mitigation: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    
    # Risk classification
    risk_level: Mapped[str] = mapped_column(
        String(20), 
        nullable=False,
        index=True
    )  # low, medium, high, critical
    
    category: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        index=True
    )  # financial, operational, technical, regulatory
    
    # Risk metrics
    probability: Mapped[float] = mapped_column(
        Float, 
        nullable=False
    )  # 0.0 to 1.0
    
    impact_score: Mapped[Optional[float]] = mapped_column(
        Float, 
        nullable=True
    )  # 0.0 to 1.0
    
    risk_score: Mapped[Optional[float]] = mapped_column(
        Float, 
        nullable=True
    )  # probability * impact_score
    
    # Additional data
    metadata: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True
    )  # Additional risk-specific data
    
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
        back_populates="risks"
    )
    
    # Methods
    def __repr__(self) -> str:
        return f"<RiskAssessment(id={self.id}, risk_level={self.risk_level}, category={self.category})>"
    
    @property
    def risk_level_score(self) -> int:
        """Get numeric risk level score for sorting."""
        scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return scores.get(self.risk_level, 0)
    
    @property
    def is_critical(self) -> bool:
        """Check if risk is critical level."""
        return self.risk_level == "critical"
    
    @property
    def is_high_or_critical(self) -> bool:
        """Check if risk is high or critical level."""
        return self.risk_level in ["high", "critical"]
    
    @property
    def calculated_risk_score(self) -> float:
        """Calculate risk score if not set."""
        if self.risk_score is not None:
            return self.risk_score
        if self.impact_score is not None:
            return self.probability * self.impact_score
        return self.probability
    
    def to_dict(self) -> dict:
        """Convert risk assessment to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "impact": self.impact,
            "mitigation": self.mitigation,
            "risk_level": self.risk_level,
            "category": self.category,
            "probability": self.probability,
            "impact_score": self.impact_score,
            "risk_score": self.calculated_risk_score,
            "metadata": self.metadata,
            "contract_id": self.contract_id,
            "risk_level_score": self.risk_level_score,
            "is_critical": self.is_critical,
            "is_high_or_critical": self.is_high_or_critical,
            "created_at": self.created_at.isoformat(),
        }
