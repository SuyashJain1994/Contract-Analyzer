import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import logging

from ..config import settings
from ..utils.exceptions import AuthenticationException

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication and JWT tokens"""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    async def authenticate_user(self, email: str, password: str) -> str:
        """Authenticate user and return JWT token"""
        try:
            # For demo purposes, using hardcoded credentials
            # In production, this should check against a database
            if email == "suyash@lawfirm.com" and password == "demo123":
                token_data = {
                    "sub": email,
                    "user_id": 1,
                    "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
                }
                
                token = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
                return token
            else:
                raise AuthenticationException("Invalid credentials", status_code=401)
                
        except AuthenticationException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise AuthenticationException("Authentication failed", status_code=500)
    
    async def get_current_user(self, token: str) -> dict:
        """Validate JWT token and return user info"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email = payload.get("sub")
            user_id = payload.get("user_id")
            
            if email is None or user_id is None:
                raise AuthenticationException("Invalid token", status_code=401)
            
            # In production, fetch user from database
            return {
                "id": user_id,
                "email": email,
                "full_name": "Suyash Kumar",
                "is_active": True
            }
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationException("Token expired", status_code=401)
        except jwt.JWTError:
            raise AuthenticationException("Invalid token", status_code=401)
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            raise AuthenticationException("Token validation failed", status_code=401)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))