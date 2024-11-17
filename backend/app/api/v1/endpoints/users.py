from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import security
from app.core.deps import get_current_active_user, get_current_user
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.user import UserCreate, User as UserSchema

router = APIRouter()

@router.post("/users", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """创建新用户"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=user_in.is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users", response_model=List[UserSchema])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """获取用户列表"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/me", response_model=UserSchema)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """获取当前用户信息"""
    return current_user 