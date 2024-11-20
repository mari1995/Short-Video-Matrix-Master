from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_redoc_html
)
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.api.v1.endpoints import login, dashboard, youtube, files, video_analysis, system_config, image_analysis, \
    drafts, video_editor
from app.core.config import settings
from app.core.logger import logger
from app.db.base import SessionLocal
from app.db.init_db import init_db
from app.db.models import init_db as create_tables
from app.middleware.logging import log_request_middleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 添加日志中间件
# app.middleware("http")(log_request_middleware)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# 自定义 swagger 文档路由
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


# 自定义 redoc 文档路由
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )


@app.on_event("startup")
async def startup_event():
    create_tables()
    db = SessionLocal()
    init_db(db)
    db.close()
    logger.info("Application startup")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")


# 包含路由
app.include_router(
    login.router,
    prefix=settings.API_V1_STR,
    tags=["认证管理"],
)

app.include_router(
    dashboard.router,
    prefix=settings.API_V1_STR,
    tags=["仪表盘"],
)
app.include_router(
    youtube.router,
    prefix=f"{settings.API_V1_STR}/youtube",
    tags=["YouTube下载器"],
)
app.include_router(
    files.router,
    prefix=f"{settings.API_V1_STR}/files",
    tags=["文件管理"],
)
app.include_router(
    video_analysis.router,
    prefix=f"{settings.API_V1_STR}/video-analysis",
    tags=["视频分析"],
)
app.include_router(
    system_config.router,
    prefix=f"{settings.API_V1_STR}/system-config",
    tags=["配置中心"],
)
app.include_router(
    image_analysis.router,
    prefix=f"{settings.API_V1_STR}/image-analysis",
    tags=["图片分析"],
)

app.include_router(
    drafts.router,
    prefix=f"{settings.API_V1_STR}/drafts",
    tags=["草稿箱"],
)

app.include_router(
    video_editor.router,
    prefix=f"{settings.API_V1_STR}/video-editor",
    tags=["视频编辑器"],
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

# 自定义静态文件处理
@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    file_location = f"static/{file_path}"
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-cache"
    }
    return FileResponse(
        path=file_location,
        headers=headers,
        filename=file_path.split('/')[-1]
    )
