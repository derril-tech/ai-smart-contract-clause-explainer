"""
Report model for generating and storing analysis reports.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Report(Base):
    """Report model for generating and storing analysis reports."""
    
    __tablename__ = "reports"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Report details
    title: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True
    )
    
    # Report type and format
    report_type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
    )  # security, risk, compliance, executive
    
    format: Mapped[str] = mapped_column(
        String(20), 
        default="pdf",
        nullable=False
    )  # pdf, html, json
    
    # Generation status
    status: Mapped[str] = mapped_column(
        String(20), 
        default="pending",
        nullable=False
    )  # pending, generating, completed, failed
    
    # Report content
    content: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True
    )  # Generated report content
    
    file_path: Mapped[Optional[str]] = mapped_column(
        String(500), 
        nullable=True
    )  # Path to generated file
    
    file_size: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )  # File size in bytes
    
    # Generation metadata
    generation_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True
    )
    generation_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True
    )
    generation_duration: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )  # Duration in seconds
    
    # Report configuration
    config: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True
    )  # Report generation configuration
    
    # Project relationship
    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), 
        ForeignKey("projects.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
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
        back_populates="reports"
    )
    
    # Methods
    def __repr__(self) -> str:
        return f"<Report(id={self.id}, title={self.title}, status={self.status})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if report generation is completed."""
        return self.status == "completed"
    
    @property
    def is_failed(self) -> bool:
        """Check if report generation failed."""
        return self.status == "failed"
    
    @property
    def is_generating(self) -> bool:
        """Check if report is currently being generated."""
        return self.status == "generating"
    
    @property
    def has_file(self) -> bool:
        """Check if report has a generated file."""
        return self.file_path is not None and self.file_size is not None
    
    def to_dict(self) -> dict:
        """Convert report to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "report_type": self.report_type,
            "format": self.format,
            "status": self.status,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "generation_started_at": self.generation_started_at.isoformat() if self.generation_started_at else None,
            "generation_completed_at": self.generation_completed_at.isoformat() if self.generation_completed_at else None,
            "generation_duration": self.generation_duration,
            "config": self.config,
            "project_id": self.project_id,
            "is_completed": self.is_completed,
            "is_failed": self.is_failed,
            "is_generating": self.is_generating,
            "has_file": self.has_file,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
