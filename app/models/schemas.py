from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ContractType(str, Enum):
    EMPLOYMENT = "employment"
    SERVICE = "service"
    NDA = "nda"
    LEASE = "lease"
    PARTNERSHIP = "partnership"
    GENERAL = "general"

class AnalysisDepth(str, Enum):
    STANDARD = "standard"
    DEEP = "deep"
    COMPLIANCE = "compliance"
    RISK_ASSESSMENT = "risk_assessment"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Request Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UploadRequest(BaseModel):
    contract_type: ContractType = ContractType.GENERAL
    analysis_depth: AnalysisDepth = AnalysisDepth.STANDARD

# Response Models
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

class RiskItem(BaseModel):
    type: str
    severity: RiskLevel
    description: str
    recommendation: str
    confidence: float
    location: Optional[str] = None

class Insight(BaseModel):
    category: str
    title: str
    description: str
    impact: str
    recommendation: str

class AnalysisResult(BaseModel):
    id: str
    filename: str
    contract_type: ContractType
    analysis_depth: AnalysisDepth
    created_at: datetime
    
    # Analysis Results
    summary: str
    key_terms: List[Dict[str, Any]]
    risks: List[RiskItem]
    insights: List[Insight]
    compliance_score: float
    overall_risk_score: float
    
    # Recommendations
    negotiation_points: List[str]
    missing_clauses: List[str]
    improvements: List[str]

class FileAnalysisResult(BaseModel):
    filename: str
    status: str
    analysis: Optional[AnalysisResult] = None
    error: Optional[str] = None

class UploadResponse(BaseModel):
    success: bool
    message: str
    results: List[FileAnalysisResult]

class DashboardStats(BaseModel):
    contracts_analyzed: int
    high_risk_detected: int
    risk_avoided: str
    time_saved: str

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime

# Database Models
class ContractAnalysisCreate(BaseModel):
    filename: str
    contract_type: ContractType
    analysis_depth: AnalysisDepth
    file_size: int
    user_id: int

class ContractAnalysisUpdate(BaseModel):
    status: Optional[str] = None
    analysis_result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None