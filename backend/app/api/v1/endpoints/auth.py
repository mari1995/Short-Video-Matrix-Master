from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.user import User
from app.core.security import verify_password

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录"""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    return {
        "token": "dummy_token",  # 简化处理，返回固定token
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout():
    """用户登出"""
    return {"message": "Successfully logged out"} 