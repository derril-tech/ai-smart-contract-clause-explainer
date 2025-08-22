"""
Contract analysis and management schemas.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


class ContractBase(BaseModel):
    """Base contract schema."""
    address: str = Field(..., regex=r'^0x[a-fA-F0-9]{40}$')
    chain_id: int = Field(..., ge=1)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    source_code: str = Field(..., min_length=1)


class ContractCreate(ContractBase):
    """Schema for creating a new contract."""
    abi: Optional[List[Dict[str, Any]]] = None
    bytecode: Optional[str] = None


class ContractUpdate(BaseModel):
    """Schema for updating contract information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    source_code: Optional[str] = Field(None, min_length=1)
    abi: Optional[List[Dict[str, Any]]] = None
    bytecode: Optional[str] = None


class ContractResponse(ContractBase):
    """Schema for contract response."""
    id: str
    project_id: str
    analysis_status: str
    analysis_started_at: Optional[datetime] = None
    analysis_completed_at: Optional[datetime] = None
    analysis_duration: Optional[int] = None
    analysis_summary: Optional[str] = None
    risk_score: Optional[float] = None
    findings_count: Dict[str, int]
    risks_count: Dict[str, int]
    has_critical_issues: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SecurityFindingBase(BaseModel):
    """Base security finding schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1)
    recommendation: str = Field(..., min_length=1)
    severity: str = Field(..., regex="^(low|medium|high|critical)$")
    category: str = Field(..., regex="^(access-control|arithmetic|reentrancy|gas|other)$")
    line_number: Optional[int] = Field(None, ge=1)
    function_name: Optional[str] = Field(None, min_length=1, max_length=255)
    file_name: Optional[str] = Field(None, min_length=1, max_length=255)
    tool: str = Field(..., regex="^(slither|semgrep|ai-analysis)$")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


class SecurityFindingCreate(SecurityFindingBase):
    """Schema for creating a security finding."""
    contract_id: str


class SecurityFindingResponse(SecurityFindingBase):
    """Schema for security finding response."""
    id: str
    contract_id: str
    severity_score: int
    is_critical: bool
    is_high_or_critical: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class RiskAssessmentBase(BaseModel):
    """Base risk assessment schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1)
    impact: str = Field(..., min_length=1)
    mitigation: str = Field(..., min_length=1)
    risk_level: str = Field(..., regex="^(low|medium|high|critical)$")
    category: str = Field(..., regex="^(financial|operational|technical|regulatory)$")
    probability: float = Field(..., ge=0.0, le=1.0)
    impact_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    risk_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


class RiskAssessmentCreate(RiskAssessmentBase):
    """Schema for creating a risk assessment."""
    contract_id: str


class RiskAssessmentResponse(RiskAssessmentBase):
    """Schema for risk assessment response."""
    id: str
    contract_id: str
    risk_level_score: int
    is_critical: bool
    is_high_or_critical: bool
    calculated_risk_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContractAnalysisRequest(BaseModel):
    """Schema for contract analysis request."""
    contract_address: str = Field(..., regex=r'^0x[a-fA-F0-9]{40}$')
    chain_id: int = Field(..., ge=1)
    analysis_type: List[str] = Field(default_factory=list)
    
    @validator('analysis_type')
    def validate_analysis_type(cls, v):
        """Validate analysis type values."""
        valid_types = ['security', 'risk', 'gas', 'compliance']
        for analysis_type in v:
            if analysis_type not in valid_types:
                raise ValueError(f'Invalid analysis type: {analysis_type}. Must be one of {valid_types}')
        return v


class ContractAnalysisResponse(BaseModel):
    """Schema for contract analysis response."""
    contract_id: str
    analysis_id: str
    status: str
    estimated_duration: Optional[int] = None  # seconds
    message: str


class ContractAnalysisResult(BaseModel):
    """Schema for contract analysis results."""
    contract: ContractResponse
    findings: List[SecurityFindingResponse]
    risks: List[RiskAssessmentResponse]
    summary: Dict[str, Any]
    
    class Config:
        from_attributes = True


class ContractUploadRequest(BaseModel):
    """Schema for contract source code upload."""
    project_id: str
    contract_name: Optional[str] = Field(None, min_length=1, max_length=255)
    source_files: Dict[str, str] = Field(..., min_items=1)  # filename -> content
    abi: Optional[List[Dict[str, Any]]] = None
    bytecode: Optional[str] = None
    
    @validator('source_files')
    def validate_source_files(cls, v):
        """Validate source files."""
        if not v:
            raise ValueError('At least one source file is required')
        for filename, content in v.items():
            if not filename.strip():
                raise ValueError('Filename cannot be empty')
            if not content.strip():
                raise ValueError(f'Source file {filename} cannot be empty')
        return v


class ContractVerificationRequest(BaseModel):
    """Schema for contract verification request."""
    contract_address: str = Field(..., regex=r'^0x[a-fA-F0-9]{40}$')
    chain_id: int = Field(..., ge=1)
    compiler_version: str = Field(..., min_length=1)
    optimization_used: bool = False
    runs: int = Field(default=200, ge=0)
    constructor_arguments: Optional[str] = None
    source_code: str = Field(..., min_length=1)
