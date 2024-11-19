from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.video_analysis import VideoAnalysis
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

@router.get("/overview")
async def get_statistics(db: Session = Depends(get_db)):
    """获取统计概览数据"""
    # 获取总分析次数
    total_analyses = db.query(VideoAnalysis).count()
    
    # 获取今日分析次数
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_analyses = db.query(VideoAnalysis)\
        .filter(VideoAnalysis.created_at >= today_start)\
        .count()
    
    # 获取视频数量
    video_count = db.query(VideoAnalysis)\
        .filter(VideoAnalysis.status == 'completed')\
        .count()
    
    return {
        "total_analyses": total_analyses,
        "today_analyses": today_analyses,
        "video_count": video_count,
        "image_count": 0  # 暂时固定为0，后续可以添加图片统计
    }

@router.get("/recent")
async def get_recent_analyses(
    db: Session = Depends(get_db),
    limit: int = 10
):
    """获取最近的分析记录"""
    recent_analyses = db.query(VideoAnalysis)\
        .order_by(VideoAnalysis.created_at.desc())\
        .limit(limit)\
        .all()
    
    return {
        "items": [
            {
                "file_name": analysis.file_name,
                "created_at": analysis.created_at.timestamp(),
                "status": analysis.status
            }
            for analysis in recent_analyses
        ]
    } 