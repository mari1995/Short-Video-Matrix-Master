from fastapi import APIRouter, HTTPException, Depends, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.video_editor import VideoGeneration
from typing import List
from datetime import datetime
import shutil
from pathlib import Path
import cv2
import numpy as np
import asyncio
import json

router = APIRouter()

EDITOR_UPLOAD_DIR = Path("static/uploads/editor")
EDITOR_OUTPUT_DIR = Path("static/uploads/editor/output")

def ensure_dirs():
    """确保必要的目录存在"""
    EDITOR_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    EDITOR_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/generate")
async def generate_video(
    request: Request,
    images: List[UploadFile] = File(...),
    settings: str = Form(...),
    music: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """生成视频"""
    ensure_dirs()
    
    try:
        # 解析设置
        settings_dict = json.loads(settings)
        duration = float(settings_dict.get('duration', 10))
        transition = settings_dict.get('transition', 'fade')
        
        # 保存图片
        image_paths = []
        image_urls = []
        for image in images:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{image.filename}"
            file_path = EDITOR_UPLOAD_DIR / filename
            
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            image_paths.append(str(file_path))
            image_urls.append(f"http://127.0.0.1:8000/static/uploads/editor/{filename}")
        
        # 保存音乐文件
        music_path = None
        if music:
            music_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{music.filename}"
            music_path = EDITOR_UPLOAD_DIR / music_filename
            with music_path.open("wb") as buffer:
                shutil.copyfileobj(music.file, buffer)
        
        # 创建生成记录
        generation = VideoGeneration(
            title=f"Video_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            status="processing",
            duration=duration,
            transition=transition,
            source_images=image_urls
        )
        db.add(generation)
        db.commit()
        db.refresh(generation)
        
        # 异步处理视频生成
        asyncio.create_task(process_video_generation(
            generation.id,
            image_paths,
            str(music_path) if music_path else None,
            duration,
            transition,
            db
        ))
        
        return generation.serialize()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def process_video_generation(
    generation_id: int,
    image_paths: List[str],
    music_path: str,
    duration: float,
    transition: str,
    db: Session
):
    """处理视频生成"""
    try:
        # 读取图片
        images = []
        for path in image_paths:
            img = cv2.imread(path)
            if img is None:
                raise Exception(f"Failed to read image: {path}")
            images.append(img)
        
        # 统一图片尺寸
        target_size = (1920, 1080)  # 1080p
        resized_images = []
        for img in images:
            resized = cv2.resize(img, target_size)
            resized_images.append(resized)
        
        # 生成视频文件名
        output_filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = EDITOR_OUTPUT_DIR / output_filename
        
        # 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 30
        out = cv2.VideoWriter(str(output_path), fourcc, fps, target_size)
        
        # 计算每张图片的持续帧数
        frames_per_image = int(duration * fps / len(images))
        
        # 写入视频帧
        for i, img in enumerate(resized_images):
            # 写入当前图片的帧
            for _ in range(frames_per_image):
                out.write(img)
                
            # 如果不是最后一张图片，添加转场效果
            if i < len(resized_images) - 1:
                next_img = resized_images[i + 1]
                transition_frames = int(fps / 2)  # 0.5秒转场
                
                if transition == 'fade':
                    for j in range(transition_frames):
                        alpha = j / transition_frames
                        blended = cv2.addWeighted(img, 1 - alpha, next_img, alpha, 0)
                        out.write(blended)
                        
                elif transition == 'slide':
                    for j in range(transition_frames):
                        offset = int((j / transition_frames) * target_size[0])
                        frame = img.copy()
                        frame[:, :offset] = next_img[:, :offset]
                        out.write(frame)
                        
                elif transition == 'zoom':
                    for j in range(transition_frames):
                        scale = 1 + (j / transition_frames) * 0.2
                        center = (target_size[0] // 2, target_size[1] // 2)
                        M = cv2.getRotationMatrix2D(center, 0, scale)
                        zoomed = cv2.warpAffine(img, M, target_size)
                        alpha = j / transition_frames
                        blended = cv2.addWeighted(zoomed, 1 - alpha, next_img, alpha, 0)
                        out.write(blended)
        
        out.release()
        
        # 如果有音乐，添加音乐（这里需要使用其他库，如moviepy）
        if music_path:
            # TODO: 添加音乐处理逻辑
            pass
        
        # 更新生成记录
        generation = db.query(VideoGeneration).get(generation_id)
        if generation:
            generation.status = "completed"
            generation.output_url = f"http://127.0.0.1:8000/static/uploads/editor/output/{output_filename}"
            db.commit()
            
    except Exception as e:
        # 更新错误状态
        generation = db.query(VideoGeneration).get(generation_id)
        if generation:
            generation.status = "failed"
            generation.error_message = str(e)
            db.commit()

@router.get("/history")
async def get_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取生成历史"""
    total = db.query(VideoGeneration).count()
    generations = db.query(VideoGeneration)\
        .order_by(VideoGeneration.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return {
        "total": total,
        "items": [item.serialize() for item in generations]
    }

@router.get("/status/{generation_id}")
async def get_status(
    generation_id: int,
    db: Session = Depends(get_db)
):
    """获取生成状态"""
    generation = db.query(VideoGeneration).get(generation_id)
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return generation.serialize() 