from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode JWT token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return {"username": username}
        except JWTError:
            raise credentials_exception

# Simple user database (replace with real database in production)
fake_users_db = {
    "demo": {
        "username": "demo",
        "name": "Demo User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # demo123
    },
    "admin": {
        "username": "admin", 
        "name": "Admin User",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DUE.NhuA.Og1VmlbEmu6u8qZ9Z.4em"  # admin123
    }
}

def authenticate_user(username: str, password: str):
    """Authenticate a user"""
    user = fake_users_db.get(username)
    if not user:
        return False
    if not AuthService.verify_password(password, user["hashed_password"]):
        return False
    return user

def get_user(username: str):
    """Get user by username"""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return {
            "username": user_dict["username"],
            "name": user_dict["name"]
        }

# At the end of app/services/auth.py, make sure you have:
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token (standalone function)"""
    return AuthService.create_access_token(data, expires_delta)

# At the end of app/services/auth.py, add:

def verify_token(token: str) -> dict:
    """Verify and decode JWT token (standalone function)"""
    return AuthService.verify_token(token)
