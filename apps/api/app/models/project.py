"""
Project model for organizing contract analyses.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Project(Base):
    """Project model for organizing contract analyses."""
    
    __tablename__ = "projects"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Project details
    name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True
    )
    
    # Ownership
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    
    # Project settings
    is_public: Mapped[bool] = mapped_column(
        default=False, 
        nullable=False
    )
    settings: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True
    )  # JSON string for project settings
    
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
    user: Mapped["User"] = relationship(
        "User", 
        back_populates="projects"
    )
    contracts: Mapped[List["Contract"]] = relationship(
        "Contract", 
        back_populates="project", 
        cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(
        "Report", 
        back_populates="project", 
        cascade="all, delete-orphan"
    )
    
    # Methods
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name}, user_id={self.user_id})>"
    
    @property
    def contract_count(self) -> int:
        """Get the number of contracts in this project."""
        return len(self.contracts)
    
    @property
    def completed_analyses(self) -> int:
        """Get the number of completed contract analyses."""
        return len([c for c in self.contracts if c.analysis_status == "completed"])
    
    @property
    def critical_findings_count(self) -> int:
        """Get the total number of critical findings across all contracts."""
        count = 0
        for contract in self.contracts:
            count += len([f for f in contract.findings if f.severity == "critical"])
        return count
    
    def to_dict(self) -> dict:
        """Convert project to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "is_public": self.is_public,
            "contract_count": self.contract_count,
            "completed_analyses": self.completed_analyses,
            "critical_findings_count": self.critical_findings_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
