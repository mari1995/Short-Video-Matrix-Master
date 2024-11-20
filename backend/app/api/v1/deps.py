from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.db.base import get_db
from app.db.models.user import User
from loguru import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": "auth_failed",
            "message": "认证失败",
            "code": "INVALID_TOKEN"
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 验证令牌并获取用户ID
        user_id = verify_token(token)
        if user_id is None:
            logger.warning(f"Invalid token: {token}")
            raise credentials_exception
            
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception
        
    # 通过用户ID查询用户
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.warning(f"User not found: {user_id}")
        raise credentials_exception
        
    # 检查用户状态
    if not user.is_active:
        logger.warning(f"Inactive user attempted access: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "auth_failed",
                "message": "用户已被禁用",
                "code": "USER_INACTIVE"
            }
        )
        
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "auth_failed",
                "message": "用户已被禁用",
                "code": "USER_INACTIVE"
            }
        )
    return current_user

def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前超级用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "auth_failed",
                "message": "需要超级管理员权限",
                "code": "PERMISSION_DENIED"
            }
        )
    return current_user