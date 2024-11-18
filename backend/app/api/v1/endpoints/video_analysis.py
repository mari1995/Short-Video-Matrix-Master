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

def extract_key_frames(video_path: str, request: Request, threshold: float = 0.7) -> List[dict]:
    """提取视频关键帧"""
    cap = cv2.VideoCapture(video_path)
    frames_data = []
    prev_frame = None
    frame_count = 0
    
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
            frame_path = str(FRAMES_DIR / frame_filename)
            cv2.imwrite(frame_path, frame)
            relative_path = f"static/uploads/frames/{frame_filename}"
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
            frame_path = str(FRAMES_DIR / frame_filename)
            cv2.imwrite(frame_path, frame)
            relative_path = f"static/uploads/frames/{frame_filename}"
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
    db: Session = Depends(get_db)
):
    """上传视频文件"""
    ensure_dirs()
    
    try:
        # 保存视频文件
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 创建分析记录
        analysis = VideoAnalysis(
            file_name=file.filename,
            file_path=str(file_path),
            status="processing"
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
        
        # 提取关键帧
        frames_data = extract_key_frames(file_path, request)
        
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
async def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """获取分析结果"""
    analysis = db.query(VideoAnalysis).get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis.serialize

@router.get("/list")
async def list_analyses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取分析列表"""
    total = db.query(VideoAnalysis).count()
    analyses = db.query(VideoAnalysis)\
        .order_by(VideoAnalysis.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return {
        "total": total,
        "items": [item.serialize for item in analyses]
    } 

class FrameAnalysisResponse(BaseModel):
    frame_id: int
    timestamp: float
    image_path: str
    descriptions: List[dict] = None  # 添加图片描述字段

@router.post("/analyze-frame")
async def analyze_frame(
    image_path: str,
    db: Session = Depends(get_db)
):
    """分析视频帧图片"""
    try:
        # 获取API配置
        base_url = system_config.get_config(db, 'ideogram_base_url').value
        api_key = system_config.get_config(db, 'ideogram_api_key').value
        
        if not api_key:
            raise HTTPException(status_code=400, detail="Ideogram API key not configured")
        
        # 准备请求
        url = f"{base_url}/ideogram/describe"
        headers = {
            'accept': 'application/json',
            'Authorization': api_key
        }
        
        # 读取文件内容
        with open(image_path, 'rb') as f:
            file_content = f.read()
        
        # 准备multipart表单数据
        form_data = aiohttp.FormData()
        form_data.add_field(
            'image_file',
            file_content,
            filename='frame.jpg',
            content_type='image/jpeg'
        )
        
        # 发送请求
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=form_data) as response:
                if response.content_type != 'application/json':
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Unexpected response type: {response.content_type}. Error: {error_text}"
                    )
                
                result = await response.json()
                return result
                
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 