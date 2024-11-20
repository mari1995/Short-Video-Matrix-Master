from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from loguru import logger
from traceback import format_exc
from app.core import security
from app.core.config import settings
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.token import Token, LoginData
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.post("/auth/login", response_model=Token)
async def login_access_token(
    request: Request,
    login_data: LoginData,
    db: Session = Depends(get_db)
) -> Any:
    """JSON格式的登录接口"""
    try:
        # 打印完整的请求路径
        logger.info({
            "action": "login_attempt",
            "request_path": request.url.path,
            "username": login_data.username
        })
        
        # 查询用户
        user = db.query(User).filter(User.username == login_data.username).first()
        
        if not user:
            logger.warning({
                "action": "login_failed",
                "reason": "user_not_found",
                "username": login_data.username,
                "request_id": id(request)
            })
            raise HTTPException(
                status_code=399,
                detail={
                    "error": "auth_failed",
                    "message": "用户名或密码错误",
                    "code": "USER_NOT_FOUND"
                }
            )
        
        # 验证密码
        is_password_correct = security.verify_password(login_data.password, user.hashed_password)
        
        if not is_password_correct:
            logger.warning({
                "action": "login_failed",
                "reason": "invalid_password",
                "username": login_data.username,
                "request_id": id(request)
            })
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "auth_failed",
                    "message": "用户名或密码错误",
                    "code": "INVALID_PASSWORD"
                }
            )
        
        # 检查用户状态
        if not user.is_active:
            logger.warning({
                "action": "login_failed",
                "reason": "inactive_user",
                "username": login_data.username,
                "request_id": id(request)
            })
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "auth_failed",
                    "message": "用户已被禁用",
                    "code": "USER_INACTIVE"
                }
            )
        
        # 生成token，使用用户ID
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = security.create_access_token(
            user_id=user.id,  # 使用用户ID
            expires_delta=access_token_expires
        )
        
        logger.info({
            "action": "login_success",
            "username": login_data.username,
            "user_id": user.id,
            "request_id": id(request)
        })
        
        return {
            "access_token": token,
            "token_type": "bearer",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error({
            "action": "login_error",
            "username": login_data.username if login_data else "unknown",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": format_exc(),
            "request_id": id(request)
        })
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "服务器内部错误",
                "code": "INTERNAL_ERROR"
            }
        )

@router.post("/auth/logout")
async def logout(
    request: Request,
    response: Response
):
    """用户登出"""
    try:
        logger.info({
            "action": "logout_attempt",
            "request_path": request.url.path,
            "request_id": id(request)
        })
        
        # 清除客户端的认证信息
        response.delete_cookie(
            key="access_token",
            path="/",
            domain=None,
            secure=False,
            httponly=True
        )
        
        logger.info({
            "action": "logout_success",
            "request_id": id(request)
        })
        
        return {
            "code": 200,
            "message": "Successfully logged out",
            "data": None
        }
        
    except Exception as e:
        logger.error({
            "action": "logout_error",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": format_exc(),
            "request_id": id(request)
        })
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "登出失败",
                "code": "INTERNAL_ERROR"
            }
        )