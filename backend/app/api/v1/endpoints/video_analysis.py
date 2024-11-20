from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Request
from typing import List
import cv2
import numpy as np
from pathlib import Path
import os
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.video_analysis import VideoAnalysis
import asyncio
import shutil
from app.crud import system_config
import aiohttp
import json
from pydantic import BaseModel
from app.db.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()

UPLOAD_DIR = Path("static/uploads/videos")
FRAMES_DIR = Path("static/uploads/frames")

def ensure_dirs():
    """确保必要的目录存在"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

def get_full_url(request: Request, path: str) -> str:
    """生成完整的URL路径"""
    return f"http://127.0.0.1:8000/{path}"

def extract_key_frames(video_path: str, request: Request, analysis_id: int, threshold: float = 0.7) -> List[dict]:
    """提取视频关键帧"""
    cap = cv2.VideoCapture(video_path)
    frames_data = []
    prev_frame = None
    frame_count = 0
    
    # 创建该分析ID的专属目录
    analysis_frames_dir = FRAMES_DIR / str(analysis_id)
    analysis_frames_dir.mkdir(parents=True, exist_ok=True)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # 每秒只处理一帧
        if frame_count % int(cap.get(cv2.CAP_PROP_FPS)) != 0:
            continue
            
        # 转换为灰度图进行比较
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_frame is None:
            prev_frame = gray
            # 保存第一帧
            frame_filename = f"frame_{frame_count}.jpg"
            frame_path = str(analysis_frames_dir / frame_filename)
            cv2.imwrite(frame_path, frame)
            relative_path = f"static/uploads/frames/{analysis_id}/{frame_filename}"
            frames_data.append({
                "frame_number": frame_count,
                "timestamp": frame_count / cap.get(cv2.CAP_PROP_FPS),
                "path": relative_path,
                "url": get_full_url(request, relative_path)
            })
            continue
            
        # 计算帧差异
        diff = cv2.absdiff(prev_frame, gray)
        diff_score = np.mean(diff)
        
        # 如果差异大于阈值，保存该帧
        if diff_score > threshold:
            frame_filename = f"frame_{frame_count}.jpg"
            frame_path = str(analysis_frames_dir / frame_filename)
            cv2.imwrite(frame_path, frame)
            relative_path = f"static/uploads/frames/{analysis_id}/{frame_filename}"
            frames_data.append({
                "frame_number": frame_count,
                "timestamp": frame_count / cap.get(cv2.CAP_PROP_FPS),
                "path": relative_path,
                "url": get_full_url(request, relative_path),
                "diff_score": float(diff_score)
            })
            prev_frame = gray
            
    cap.release()
    return frames_data

@router.post("/upload")
async def upload_video(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传视频文件"""
    ensure_dirs()
    
    try:
        # 保存视频文件
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 生成完整URL
        file_url = f"http://127.0.0.1:8000/static/uploads/videos/{file.filename}"
            
        # 创建分析记录，添加用户ID
        analysis = VideoAnalysis(
            file_name=file.filename,
            file_url=file_url,
            status="processing",
            user_id=current_user.id
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # 异步处理视频分析
        asyncio.create_task(process_video(str(file_path), analysis.id, db, request))
        
        return {
            "message": "Video uploaded successfully",
            "analysis_id": analysis.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def process_video(file_path: str, analysis_id: int, db: Session, request: Request):
    """处理视频分析"""
    try:
        # 打开视频文件
        cap = cv2.VideoCapture(file_path)
        
        # 获取视频信息
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 提取关键帧，传入analysis_id
        frames_data = extract_key_frames(file_path, request, analysis_id)
        
        # 更新分析记录
        analysis = db.query(VideoAnalysis).get(analysis_id)
        if analysis:
            analysis.duration = duration
            analysis.frame_count = frame_count
            analysis.fps = fps
            analysis.resolution = f"{width}x{height}"
            analysis.frames_data = frames_data
            analysis.status = "completed"
            db.commit()
            
    except Exception as e:
        # 更新错误状态
        analysis = db.query(VideoAnalysis).get(analysis_id)
        if analysis:
            analysis.status = "failed"
            analysis.error_message = str(e)
            db.commit()

@router.get("/analysis/{analysis_id}")
async def get_analysis_detail(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取视频分析详情"""
    # 查询分析记录，并验证所有权
    analysis = db.query(VideoAnalysis)\
        .filter(
            VideoAnalysis.id == analysis_id,
            VideoAnalysis.user_id == current_user.id
        ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found or access denied"
        )
    
    try:
        # 获取完整的分析数据
        analysis_data = analysis.serialize()
        
        # 如果有帧数据，确保每个帧都有完整的URL
        if analysis_data.get('frames_data'):
            for frame in analysis_data['frames_data']:
                if 'url' in frame:
                    # 确保URL是完整的
                    if not frame['url'].startswith('http'):
                        frame['url'] = f"http://127.0.0.1:8000/{frame['url'].lstrip('/')}"
        
        # 记录日志
        print(f"Returning analysis data for ID {analysis_id}: {analysis_data}")
        
        return analysis_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving analysis details: {str(e)}"
        )

@router.get("/list")
async def list_analyses(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取分析列表"""
    # 只查询当前用户的记录
    total = db.query(VideoAnalysis)\
        .filter(VideoAnalysis.user_id == current_user.id)\
        .count()
        
    analyses = db.query(VideoAnalysis)\
        .filter(VideoAnalysis.user_id == current_user.id)\
        .order_by(VideoAnalysis.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
        
    return {
        "total": total,
        "items": [item.serialize() for item in analyses]
    } 

class FrameAnalysisResponse(BaseModel):
    frame_id: int
    timestamp: float
    image_path: str
    descriptions: List[dict] = None  # 添加图片描述字段
