from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from loguru import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        logger.debug({
            "action": "verify_password",
            "plain_password_length": len(plain_password),
            "hashed_password_length": len(hashed_password)
        })
        result = pwd_context.verify(plain_password, hashed_password)
        logger.debug({
            "action": "password_verification_result",
            "result": result
        })
        return result
    except Exception as e:
        logger.error({
            "action": "password_verification_error",
            "error": str(e)
        })
        return False

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt 