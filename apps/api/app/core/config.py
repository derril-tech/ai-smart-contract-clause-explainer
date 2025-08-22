"""
Configuration management for ClauseLens AI API.
Uses Pydantic settings for type-safe environment variable handling.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseSettings, validator
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "ClauseLens AI API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://clauselens.ai"]
    ALLOWED_HOSTS: List[str] = ["localhost", "clauselens.ai"]
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Blockchain APIs
    ETHERSCAN_API_KEYS: Dict[str, str] = {}
    BLOCKSCOUT_API_URLS: Dict[str, str] = {}
    
    # Storage
    STORAGE_BUCKET: Optional[str] = None
    STORAGE_REGION: str = "us-east-1"
    
    # Email
    SMTP_URL: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@clauselens.ai"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".sol", ".json", ".md", ".txt"]
    
    # Analysis Tools
    SLITHER_TIMEOUT: int = 300  # 5 minutes
    SEMGREP_TIMEOUT: int = 120  # 2 minutes
    FUZZ_TIMEOUT: int = 600  # 10 minutes
    
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v):
        """Validate and format database URL."""
        if not v:
            raise ValueError("DATABASE_URL is required")
        return v
    
    @validator("SECRET_KEY", pre=True)
    def validate_secret_key(cls, v):
        """Validate secret key length."""
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def validate_allowed_origins(cls, v):
        """Ensure allowed origins is a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ETHERSCAN_API_KEYS", pre=True)
    def validate_etherscan_keys(cls, v):
        """Parse Etherscan API keys from environment."""
        if isinstance(v, str):
            # Parse JSON string like '{"1":"key1","10":"key2"}'
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v or {}
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that all required settings are properly configured."""
    required_settings = [
        "DATABASE_URL",
        "SECRET_KEY",
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")

# Validate on import
validate_settings()
