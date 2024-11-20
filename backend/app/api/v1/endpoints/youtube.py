from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.responses import FileResponse
from typing import Dict
from pydantic import BaseModel
import yt_dlp
import os
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.models.youtube_history import YouTubeHistory
from app.db.models.user import User
from app.db.base import get_db
from app.crud import youtube_history
from app.api.v1.deps import get_current_user

router = APIRouter()

# 定义下载目录
DOWNLOAD_DIR = Path("static/youtube/downloads")

class DownloadRequest(BaseModel):
    url: str

def show_progress(d):
    """处理下载进度"""
    progress_data = {"status": "", "progress": 0, "speed": 0, "eta": 0}
    
    if d['status'] == 'downloading':
        progress_data.update({
            "status": "downloading",
            "downloaded_bytes": d.get('downloaded_bytes', 0),
            "total_bytes": d.get('total_bytes', 0),
            "speed": d.get('speed', 0),
            "eta": d.get('eta', 0),
            "progress": round(d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100, 2) if d.get('total_bytes') else 0
        })
    elif d['status'] == 'finished':
        progress_data.update({
            "status": "finished",
            "progress": 100
        })
    
    return progress_data

def get_video_info(url: str) -> Dict:
    """获取视频信息"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title'),
                "author": info.get('uploader'),
                "length": info.get('duration'),
                "views": info.get('view_count'),
                "thumbnail_url": info.get('thumbnail'),
                "description": info.get('description'),
                "is_shorts": info.get('duration', 0) < 60,
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/info")
async def get_video_info_route(url: str):
    """获取视频信息"""
    try:
        return get_video_info(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download-file/{filename}")
async def download_file(filename: str):
    """下载文件到本地"""
    try:
        file_path = DOWNLOAD_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history")
async def get_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取下载历史"""
    total = db.query(YouTubeHistory).count()
    downloads = db.query(YouTubeHistory)\
        .order_by(YouTubeHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return {
        "total": total,
        "items": [item.serialize() for item in downloads]
    }

@router.post("/download")
async def download_video(
    request: DownloadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载视频"""
    try:
        # 获取视频信息
        info = get_video_info(request.url)
        
        # 创建下载历史记录
        history = YouTubeHistory(
            user_id=current_user.id,
            url=request.url,
            title=info["title"],
            author=info["author"],
            duration=info.get("length"),
            views=info.get("views"),
            thumbnail_url=info.get("thumbnail_url"),
            description=info.get("description"),
            is_shorts=info.get("is_shorts", False),
            status="pending"
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        
        # 确保下载目录存在
        DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        # 准备文件名（移除非法字符）
        safe_title = "".join(c for c in info["title"] if c.isalnum() or c in (' ', '-', '_')).strip()
        output_template = str(DOWNLOAD_DIR / f'{safe_title}.%(ext)s')
        
        # 设置下载选项
        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # 优先下载MP4格式
            'outtmpl': output_template,
            'progress_hooks': [show_progress],
        }
        
        # 如果是Shorts视频，限制质量为1080p
        if info["is_shorts"]:
            ydl_opts['format'] += '[height<=1080]'
        
        progress_info = {"current": None}
        
        def progress_callback(d):
            progress_info["current"] = show_progress(d)
        
        ydl_opts['progress_hooks'] = [progress_callback]
        
        # 执行下载
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])
        
        # 获取下载后的文件路径
        final_path = str(DOWNLOAD_DIR / f'{safe_title}.mp4')
        
        # 检查文件是否存在
        if not os.path.exists(final_path):
            raise Exception("Downloaded file not found")
        
        # 生成完整URL
        file_url = f"http://127.0.0.1:8000/static/youtube/downloads/{os.path.basename(final_path)}"
        
        # 更新历史记录
        youtube_history.update_youtube_history(db, history.id, {
            "file_url": file_url,  # 存储完整URL
            "file_size": os.path.getsize(final_path),
            "status": "success"
        })
        
        return {
            "status": "success",
            "title": info["title"],
            "author": info["author"],
            "file_url": file_url,  # 返回完整URL
            "file_size": os.path.getsize(final_path),
            "is_shorts": info["is_shorts"],
            "progress": progress_info["current"] or {"status": "finished", "progress": 100}
        }
        
    except Exception as e:
        # 更新失败状态
        if history:
            youtube_history.update_youtube_history(db, history.id, {
                "status": "failed",
                "error_message": str(e)
            })
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/history/{history_id}")
async def delete_history(
    history_id: int,
    db: Session = Depends(get_db)
):
    """删除下载历史记录"""
    if youtube_history.delete_youtube_history(db, history_id):
        return {"message": "History deleted successfully"}
    raise HTTPException(status_code=404, detail="History not found")
    

