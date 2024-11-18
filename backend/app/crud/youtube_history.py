from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.youtube_history import YouTubeHistory
from sqlalchemy import desc

def get_youtube_history(db: Session, skip: int = 0, limit: int = 100) -> List[YouTubeHistory]:
    """获取下载历史列表"""
    return db.query(YouTubeHistory)\
        .order_by(desc(YouTubeHistory.download_time))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_youtube_history_by_id(db: Session, history_id: int) -> Optional[YouTubeHistory]:
    """根据ID获取下载记录"""
    return db.query(YouTubeHistory).filter(YouTubeHistory.id == history_id).first()

def get_youtube_history_by_url(db: Session, url: str) -> Optional[YouTubeHistory]:
    """根据URL获取下载记录"""
    return db.query(YouTubeHistory).filter(YouTubeHistory.url == url).first()

def create_youtube_history(db: Session, history_data: dict) -> YouTubeHistory:
    """创建下载记录"""
    history = YouTubeHistory(**history_data)
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def update_youtube_history(
    db: Session, 
    history_id: int, 
    history_data: dict
) -> Optional[YouTubeHistory]:
    """更新下载记录"""
    history = get_youtube_history_by_id(db, history_id)
    if history:
        for key, value in history_data.items():
            setattr(history, key, value)
        db.commit()
        db.refresh(history)
    return history

def delete_youtube_history(db: Session, history_id: int) -> bool:
    """删除下载记录"""
    history = get_youtube_history_by_id(db, history_id)
    if history:
        db.delete(history)
        db.commit()
        return True
    return False

def get_youtube_history_count(db: Session) -> int:
    """获取下载记录总数"""
    return db.query(YouTubeHistory).count()

def get_youtube_history_by_status(
    db: Session, 
    status: str,
    skip: int = 0,
    limit: int = 100
) -> List[YouTubeHistory]:
    """根据状态获取下载记录"""
    return db.query(YouTubeHistory)\
        .filter(YouTubeHistory.status == status)\
        .order_by(desc(YouTubeHistory.download_time))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_recent_youtube_history(
    db: Session,
    limit: int = 10
) -> List[YouTubeHistory]:
    """获取最近的下载记录"""
    return db.query(YouTubeHistory)\
        .order_by(desc(YouTubeHistory.download_time))\
        .limit(limit)\
        .all()

def cleanup_old_history(db: Session, days: int) -> int:
    """清理指定天数之前的历史记录"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted = db.query(YouTubeHistory)\
        .filter(YouTubeHistory.download_time < cutoff_date)\
        .delete()
    db.commit()
    return deleted 