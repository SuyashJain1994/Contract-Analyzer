from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from .config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ContractAnalysis(Base):
    __tablename__ = "contract_analyses"
    
    id = Column(String, primary_key=True, index=True)  # UUID
    user_id = Column(Integer, index=True, nullable=False)
    filename = Column(String, nullable=False)
    contract_type = Column(String, nullable=False)
    analysis_depth = Column(String, nullable=False)
    file_size = Column(Integer)
    
    # Analysis results (stored as JSON text)
    summary = Column(Text)
    risks_json = Column(Text)  # JSON string of risks
    insights_json = Column(Text)  # JSON string of insights
    key_terms_json = Column(Text)  # JSON string of key terms
    
    # Scores
    compliance_score = Column(Float)
    overall_risk_score = Column(Float)
    
    # Status
    status = Column(String, default="processing")  # processing, completed, failed
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()