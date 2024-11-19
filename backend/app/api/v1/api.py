from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,                # 认证相关
    video_analysis,      # 视频分析
    system_config,       # 系统配置
    image_analysis,      # 图片分析
    files,              # 文件管理
    youtube,            # YouTube下载
    drafts              # 草稿箱
)

api_router = APIRouter()

# 认证相关路由
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证管理"]
)

# 视频分析路由
api_router.include_router(
    video_analysis.router,
    prefix="/video-analysis",
    tags=["视频分析"]
)

# 系统配置路由
api_router.include_router(
    system_config.router,
    prefix="/system-config",
    tags=["系统配置"]
)

# 图片分析路由
api_router.include_router(
    image_analysis.router,
    prefix="/image-analysis",
    tags=["图片分析"]
)

# 文件管理路由
api_router.include_router(
    files.router,
    prefix="/files",
    tags=["文件管理"]
)

# YouTube下载路由
api_router.include_router(
    youtube.router,
    prefix="/youtube",
    tags=["YouTube下载"]
)

# 草稿箱路由
api_router.include_router(
    drafts.router,
    prefix="/drafts",
    tags=["草稿箱"]
) 