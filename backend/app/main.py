from typing import Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from loguru import logger
from app.core.config import settings
from app.db.models import init_db as create_tables
from app.db.init_db import init_db
from app.api.v1.endpoints import login, users, dashboard, statistics
from app.db.base import SessionLocal
from app.core.logger import logger
from starlette.responses import JSONResponse
from traceback import format_exc

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="通用管理后台API文档",
    version="1.0.0",
    openapi_url=None,
    docs_url=None,
)


# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# 自定义OpenAPI文档
def custom_openapi():
    try:
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version="1.0.0",
            description="通用管理后台API文档",
            routes=app.routes,
        )
        
        # 添加安全配置和schema定义
        openapi_schema["components"] = {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "schemas": {
                "Token": {
                    "title": "Token",
                    "type": "object",
                    "properties": {
                        "access_token": {"title": "Access Token", "type": "string"},
                        "token_type": {"title": "Token Type", "type": "string"}
                    },
                    "required": ["access_token", "token_type"]
                },
                "LoginData": {
                    "title": "LoginData",
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "password": {"title": "Password", "type": "string"}
                    },
                    "required": ["username", "password"]
                },
                "UserBase": {
                    "title": "UserBase",
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "email": {"title": "Email", "type": "string", "format": "email"},
                        "full_name": {"title": "Full Name", "type": "string", "nullable": true},
                        "is_active": {"title": "Is Active", "type": "boolean", "default": true}
                    },
                    "required": ["username", "email"]
                },
                "User": {
                    "title": "User",
                    "type": "object",
                    "properties": {
                        "id": {"title": "ID", "type": "integer"},
                        "username": {"title": "Username", "type": "string"},
                        "email": {"title": "Email", "type": "string", "format": "email"},
                        "full_name": {"title": "Full Name", "type": "string", "nullable": true},
                        "is_active": {"title": "Is Active", "type": "boolean"},
                        "is_superuser": {"title": "Is Superuser", "type": "boolean"}
                    },
                    "required": ["id", "username", "email", "is_active", "is_superuser"]
                },
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {
                                "$ref": "#/components/schemas/ValidationError"
                            }
                        }
                    }
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"}
                    },
                    "required": ["loc", "msg", "type"]
                }
            }
        }
        openapi_schema["security"] = [{"bearerAuth": []}]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    except Exception as e:
        logger.error(f"Error generating OpenAPI schema: {str(e)}\n{format_exc()}")
        raise

# 只保留 ReDoc 路由
@app.get("/docs", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{settings.PROJECT_NAME} - API文档",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

# 添加OpenAPI JSON端点
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    try:
        return JSONResponse(content=custom_openapi())
    except Exception as e:
        logger.error(f"Error serving OpenAPI JSON: {str(e)}\n{format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error generating API documentation"}
        )

@app.on_event("startup")
async def startup_event():
    create_tables()
    db = SessionLocal()
    init_db(db)
    db.close()

# 包含路由
app.include_router(
    login.router,
    prefix=settings.API_V1_STR,
    tags=["认证管理"],
)
app.include_router(
    users.router,
    prefix=settings.API_V1_STR,
    tags=["用户管理"],
)
app.include_router(
    dashboard.router,
    prefix=settings.API_V1_STR,
    tags=["仪表盘"],
)
app.include_router(
    statistics.router,
    prefix=settings.API_V1_STR,
    tags=["统计数据"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Admin Backend API",
        "docs": [
            {"name": "Swagger UI", "url": "/docs"},
            {"name": "ReDoc", "url": "/redoc"}
        ]
    }