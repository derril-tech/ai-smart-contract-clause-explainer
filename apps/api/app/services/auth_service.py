"""
Authentication and authorization service.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from app.core.config import settings
from app.models.user import User

logger = structlog.get_logger()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication and authorization operations."""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.warning("JWT token verification failed", error=str(e))
            return None
    
    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            # Get user by email
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                logger.warning("Authentication failed: user not found", email=email)
                return None
            
            if not self.verify_password(password, user.hashed_password):
                logger.warning("Authentication failed: invalid password", email=email)
                return None
            
            if not user.is_active:
                logger.warning("Authentication failed: user inactive", email=email)
                return None
            
            # Update last login
            user.last_login = datetime.utcnow()
            await db.commit()
            
            logger.info("User authenticated successfully", user_id=user.id, email=email)
            return user
            
        except Exception as e:
            logger.error("Authentication error", error=str(e), email=email)
            return None
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email address."""
        try:
            result = await db.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by email", error=str(e), email=email)
            return None
    
    async def get_user_by_id(self, db: AsyncSession, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by ID", error=str(e), user_id=user_id)
            return None
    
    async def create_user(self, db: AsyncSession, email: str, password: str, name: str, role: str = "user") -> Optional[User]:
        """Create a new user."""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(db, email)
            if existing_user:
                logger.warning("User creation failed: email already exists", email=email)
                return None
            
            # Create new user
            hashed_password = self.get_password_hash(password)
            user = User(
                email=email,
                hashed_password=hashed_password,
                name=name,
                role=role,
                is_active=True,
                is_verified=False
            )
            
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            logger.info("User created successfully", user_id=user.id, email=email)
            return user
            
        except Exception as e:
            logger.error("Error creating user", error=str(e), email=email)
            await db.rollback()
            return None
    
    async def update_user_password(self, db: AsyncSession, user_id: str, new_password: str) -> bool:
        """Update user password."""
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                return False
            
            user.hashed_password = self.get_password_hash(new_password)
            await db.commit()
            
            logger.info("User password updated", user_id=user_id)
            return True
            
        except Exception as e:
            logger.error("Error updating user password", error=str(e), user_id=user_id)
            await db.rollback()
            return False
    
    async def verify_user_email(self, db: AsyncSession, user_id: str) -> bool:
        """Verify user email address."""
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                return False
            
            user.is_verified = True
            await db.commit()
            
            logger.info("User email verified", user_id=user_id)
            return True
            
        except Exception as e:
            logger.error("Error verifying user email", error=str(e), user_id=user_id)
            await db.rollback()
            return False
    
    def check_permissions(self, user: User, required_role: str = None, project_id: str = None) -> bool:
        """Check if user has required permissions."""
        # Check if user is active
        if not user.is_active:
            return False
        
        # Check role permissions
        if required_role:
            if required_role == "admin" and not user.is_admin:
                return False
            elif required_role == "analyst" and not user.is_analyst:
                return False
        
        # Check project access
        if project_id and not user.can_access_project(project_id):
            return False
        
        return True
