"""
Pydantic schemas for the ClauseLens AI application.
"""

from .auth import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData,
    PasswordResetRequest,
    PasswordResetConfirm,
    ChangePassword,
)

from .contract import (
    ContractBase,
    ContractCreate,
    ContractUpdate,
    ContractResponse,
    SecurityFindingBase,
    SecurityFindingCreate,
    SecurityFindingResponse,
    RiskAssessmentBase,
    RiskAssessmentCreate,
    RiskAssessmentResponse,
    ContractAnalysisRequest,
    ContractAnalysisResponse,
    ContractAnalysisResult,
    ContractUploadRequest,
    ContractVerificationRequest,
)

__all__ = [
    # Auth schemas
    "UserBase",
    "UserCreate", 
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "ChangePassword",
    
    # Contract schemas
    "ContractBase",
    "ContractCreate",
    "ContractUpdate", 
    "ContractResponse",
    "SecurityFindingBase",
    "SecurityFindingCreate",
    "SecurityFindingResponse",
    "RiskAssessmentBase",
    "RiskAssessmentCreate",
    "RiskAssessmentResponse",
    "ContractAnalysisRequest",
    "ContractAnalysisResponse",
    "ContractAnalysisResult",
    "ContractUploadRequest",
    "ContractVerificationRequest",
]
