class ContractAnalyzerException(Exception):
    """Base exception for Contract Analyzer application"""
    
    def __init__(self, message: str, status_code: int = 500, detail: str = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)

class DocumentProcessingException(ContractAnalyzerException):
    """Exception raised during document processing"""
    pass

class AIAnalysisException(ContractAnalyzerException):
    """Exception raised during AI analysis"""
    pass

class AuthenticationException(ContractAnalyzerException):
    """Exception raised during authentication"""
    pass

class ValidationException(ContractAnalyzerException):
    """Exception raised during data validation"""
    pass