from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging
from typing import List, Optional
import asyncio

from .config import settings
from .database import engine, Base
from .services.document_processor import DocumentProcessor
from .services.ai_analyzer import AIAnalyzer
from .services.auth import AuthService
from .models import schemas
from .utils.exceptions import ContractAnalyzerException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LegalAI Pro - Contract Analyzer",
    description="AI-powered legal contract analysis platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
auth_service = AuthService()

# Services
document_processor = DocumentProcessor()
ai_analyzer = AIAnalyzer()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main application page"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/upload", response_model=schemas.UploadResponse)
async def upload_contract(
    files: List[UploadFile] = File(...),
    contract_type: str = "general",
    analysis_depth: str = "standard",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Upload and analyze contract files"""
    try:
        # Verify authentication
        user = await auth_service.get_current_user(credentials.credentials)
        
        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        results = []
        for file in files:
            # Validate file
            if not file.filename:
                continue
                
            # Check file size (50MB limit)
            content = await file.read()
            if len(content) > 50 * 1024 * 1024:
                raise HTTPException(status_code=413, detail=f"File {file.filename} too large")
            
            # Process document
            try:
                extracted_text = await document_processor.extract_text(content, file.filename)
                
                # Analyze with AI
                analysis = await ai_analyzer.analyze_contract(
                    text=extracted_text,
                    contract_type=contract_type,
                    analysis_depth=analysis_depth,
                    filename=file.filename
                )
                
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "analysis": analysis
                })
                
            except Exception as e:
                logger.error(f"Error processing {file.filename}: {str(e)}")
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        return schemas.UploadResponse(
            success=True,
            message=f"Processed {len(results)} files",
            results=results
        )
        
    except ContractAnalyzerException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/analysis/{analysis_id}", response_model=schemas.AnalysisResult)
async def get_analysis(
    analysis_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get analysis results by ID"""
    try:
        user = await auth_service.get_current_user(credentials.credentials)
        # TODO: Implement database retrieval
        raise HTTPException(status_code=404, detail="Analysis not found")
    except Exception as e:
        logger.error(f"Get analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/auth/login", response_model=schemas.TokenResponse)
async def login(credentials: schemas.LoginRequest):
    """Authenticate user and return JWT token"""
    try:
        token = await auth_service.authenticate_user(credentials.email, credentials.password)
        return schemas.TokenResponse(access_token=token, token_type="bearer")
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/dashboard/stats", response_model=schemas.DashboardStats)
async def get_dashboard_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get dashboard statistics"""
    try:
        user = await auth_service.get_current_user(credentials.credentials)
        # TODO: Implement real stats from database
        return schemas.DashboardStats(
            contracts_analyzed=1247,
            high_risk_detected=23,
            risk_avoided="$2.3M",
            time_saved="89%"
        )
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.exception_handler(ContractAnalyzerException)
async def contract_analyzer_exception_handler(request, exc: ContractAnalyzerException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)