"""
Project management service for organizing contract analyses.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
import structlog

from app.models.project import Project
from app.models.contract import Contract
from app.models.user import User

logger = structlog.get_logger()


class ProjectService:
    """Service for project management operations."""
    
    async def create_project(
        self,
        db: AsyncSession,
        user_id: str,
        name: str,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Optional[Project]:
        """
        Create a new project.
        
        Args:
            db: Database session
            user_id: Owner user ID
            name: Project name
            description: Project description
            settings: Project settings
            
        Returns:
            Created project or None if failed
        """
        try:
            # Check if user exists
            user_result = await db.execute(select(User).where(User.id == user_id))
            user = user_result.scalar_one_or_none()
            if not user:
                logger.warning("Project creation failed: user not found", user_id=user_id)
                return None
            
            # Create project
            project = Project(
                user_id=user_id,
                name=name,
                description=description,
                settings=settings,
                is_public=False
            )
            
            db.add(project)
            await db.commit()
            await db.refresh(project)
            
            logger.info("Project created successfully", project_id=project.id, name=name, user_id=user_id)
            return project
            
        except Exception as e:
            logger.error("Error creating project", error=str(e), user_id=user_id, name=name)
            await db.rollback()
            return None
    
    async def get_project_by_id(self, db: AsyncSession, project_id: str) -> Optional[Project]:
        """Get project by ID."""
        try:
            result = await db.execute(select(Project).where(Project.id == project_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting project by ID", error=str(e), project_id=project_id)
            return None
    
    async def get_user_projects(
        self,
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Project]:
        """
        Get all projects for a user with pagination and search.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of projects to skip
            limit: Maximum number of projects to return
            search: Search term for project names
            
        Returns:
            List of projects
        """
        try:
            query = select(Project).where(Project.user_id == user_id)
            
            if search:
                query = query.where(Project.name.ilike(f"%{search}%"))
            
            query = query.offset(skip).limit(limit).order_by(Project.updated_at.desc())
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("Error getting user projects", error=str(e), user_id=user_id)
            return []
    
    async def update_project(
        self,
        db: AsyncSession,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_public: Optional[bool] = None
    ) -> bool:
        """
        Update project information.
        
        Args:
            db: Database session
            project_id: Project ID
            name: New project name
            description: New project description
            settings: New project settings
            is_public: New public visibility setting
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project = await self.get_project_by_id(db, project_id)
            if not project:
                return False
            
            # Update fields
            if name is not None:
                project.name = name
            if description is not None:
                project.description = description
            if settings is not None:
                project.settings = settings
            if is_public is not None:
                project.is_public = is_public
            
            project.updated_at = datetime.utcnow()
            
            await db.commit()
            
            logger.info("Project updated successfully", project_id=project_id)
            return True
            
        except Exception as e:
            logger.error("Error updating project", error=str(e), project_id=project_id)
            await db.rollback()
            return False
    
    async def delete_project(self, db: AsyncSession, project_id: str) -> bool:
        """
        Delete a project and all associated data.
        
        Args:
            db: Database session
            project_id: Project ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project = await self.get_project_by_id(db, project_id)
            if not project:
                return False
            
            await db.delete(project)
            await db.commit()
            
            logger.info("Project deleted successfully", project_id=project_id)
            return True
            
        except Exception as e:
            logger.error("Error deleting project", error=str(e), project_id=project_id)
            await db.rollback()
            return False
    
    async def share_project(
        self,
        db: AsyncSession,
        project_id: str,
        target_user_email: str,
        permission_level: str = "read"
    ) -> bool:
        """
        Share a project with another user.
        
        Args:
            db: Database session
            project_id: Project ID
            target_user_email: Email of user to share with
            permission_level: Permission level (read, write, admin)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get project
            project = await self.get_project_by_id(db, project_id)
            if not project:
                return False
            
            # Get target user
            user_result = await db.execute(select(User).where(User.email == target_user_email))
            target_user = user_result.scalar_one_or_none()
            if not target_user:
                logger.warning("Share failed: target user not found", email=target_user_email)
                return False
            
            # TODO: Implement project sharing mechanism
            # This would typically involve creating a project_shares table
            # For now, just make the project public if sharing
            project.is_public = True
            project.updated_at = datetime.utcnow()
            
            await db.commit()
            
            logger.info(
                "Project shared successfully",
                project_id=project_id,
                target_user_email=target_user_email,
                permission_level=permission_level
            )
            return True
            
        except Exception as e:
            logger.error("Error sharing project", error=str(e), project_id=project_id)
            await db.rollback()
            return False
    
    async def get_project_stats(self, db: AsyncSession, project_id: str) -> Dict[str, Any]:
        """
        Get comprehensive project statistics.
        
        Args:
            db: Database session
            project_id: Project ID
            
        Returns:
            Dictionary containing project statistics
        """
        try:
            project = await self.get_project_by_id(db, project_id)
            if not project:
                return {}
            
            # Get contract statistics
            contract_stats_query = await db.execute(
                select(
                    func.count(Contract.id).label("total_contracts"),
                    func.sum(
                        func.case(
                            (Contract.analysis_status == "completed", 1),
                            else_=0
                        )
                    ).label("completed_analyses"),
                    func.sum(
                        func.case(
                            (Contract.analysis_status == "analyzing", 1),
                            else_=0
                        )
                    ).label("analyzing_contracts"),
                    func.sum(
                        func.case(
                            (Contract.analysis_status == "failed", 1),
                            else_=0
                        )
                    ).label("failed_analyses"),
                    func.avg(Contract.risk_score).label("avg_risk_score"),
                    func.max(Contract.risk_score).label("max_risk_score")
                ).where(Contract.project_id == project_id)
            )
            
            contract_stats = contract_stats_query.first()
            
            # Get findings statistics
            findings_stats_query = await db.execute(
                select(
                    func.count().label("total_findings")
                ).select_from(
                    Contract.__table__.join(
                        SecurityFinding.__table__,
                        Contract.id == SecurityFinding.contract_id
                    )
                ).where(Contract.project_id == project_id)
            )
            
            findings_stats = findings_stats_query.first()
            
            # Get risk statistics
            risks_stats_query = await db.execute(
                select(
                    func.count().label("total_risks")
                ).select_from(
                    Contract.__table__.join(
                        RiskAssessment.__table__,
                        Contract.id == RiskAssessment.contract_id
                    )
                ).where(Contract.project_id == project_id)
            )
            
            risks_stats = risks_stats_query.first()
            
            return {
                "project": {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "created_at": project.created_at.isoformat(),
                    "updated_at": project.updated_at.isoformat(),
                    "is_public": project.is_public
                },
                "contracts": {
                    "total": contract_stats.total_contracts or 0,
                    "completed_analyses": contract_stats.completed_analyses or 0,
                    "analyzing": contract_stats.analyzing_contracts or 0,
                    "failed": contract_stats.failed_analyses or 0
                },
                "analysis": {
                    "total_findings": findings_stats.total_findings or 0,
                    "total_risks": risks_stats.total_risks or 0,
                    "avg_risk_score": float(contract_stats.avg_risk_score or 0),
                    "max_risk_score": float(contract_stats.max_risk_score or 0)
                }
            }
            
        except Exception as e:
            logger.error("Error getting project stats", error=str(e), project_id=project_id)
            return {}
    
    async def get_recent_activity(
        self,
        db: AsyncSession,
        project_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent activity for a project.
        
        Args:
            db: Database session
            project_id: Project ID
            limit: Maximum number of activities to return
            
        Returns:
            List of recent activities
        """
        try:
            # Get recent contracts
            recent_contracts = await db.execute(
                select(Contract)
                .where(Contract.project_id == project_id)
                .order_by(Contract.created_at.desc())
                .limit(limit)
            )
            
            activities = []
            
            for contract in recent_contracts.scalars():
                activity = {
                    "type": "contract_added",
                    "timestamp": contract.created_at.isoformat(),
                    "data": {
                        "contract_id": contract.id,
                        "contract_address": contract.address,
                        "contract_name": contract.name,
                        "analysis_status": contract.analysis_status
                    }
                }
                activities.append(activity)
                
                # Add analysis completion activity if completed
                if contract.analysis_status == "completed" and contract.analysis_completed_at:
                    activities.append({
                        "type": "analysis_completed",
                        "timestamp": contract.analysis_completed_at.isoformat(),
                        "data": {
                            "contract_id": contract.id,
                            "contract_address": contract.address,
                            "risk_score": contract.risk_score,
                            "duration": contract.analysis_duration
                        }
                    })
            
            # Sort by timestamp and limit
            activities.sort(key=lambda x: x["timestamp"], reverse=True)
            return activities[:limit]
            
        except Exception as e:
            logger.error("Error getting recent activity", error=str(e), project_id=project_id)
            return []
    
    def can_user_access_project(self, user: User, project: Project) -> bool:
        """
        Check if user can access a specific project.
        
        Args:
            user: User to check
            project: Project to check access for
            
        Returns:
            True if user can access, False otherwise
        """
        # Admin can access all projects
        if user.is_admin:
            return True
        
        # Owner can access their own projects
        if project.user_id == user.id:
            return True
        
        # Public projects can be accessed by anyone
        if project.is_public:
            return True
        
        # TODO: Check project sharing permissions
        # This would involve checking a project_shares table
        
        return False
    
    def can_user_modify_project(self, user: User, project: Project) -> bool:
        """
        Check if user can modify a specific project.
        
        Args:
            user: User to check
            project: Project to check modification rights for
            
        Returns:
            True if user can modify, False otherwise
        """
        # Admin can modify all projects
        if user.is_admin:
            return True
        
        # Owner can modify their own projects
        if project.user_id == user.id:
            return True
        
        # TODO: Check project sharing permissions for write access
        # This would involve checking a project_shares table
        
        return False


# Global project service instance
project_service = ProjectService()
