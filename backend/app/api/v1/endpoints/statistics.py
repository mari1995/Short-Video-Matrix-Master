from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.deps import get_current_active_user
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.operation_log import OperationLog
from datetime import datetime, timedelta
from loguru import logger

router = APIRouter()

@router.get("/statistics/overview")
async def get_statistics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """获取系统概览统计数据"""
    try:
        # 获取用户总数
        total_users = db.query(func.count(User.id)).scalar()
        
        # 获取今日活跃用户数（通过操作日志统计）
        today = datetime.now().date()
        today_active_users = db.query(
            func.count(func.distinct(OperationLog.user_id))
        ).filter(
            func.date(OperationLog.created_at) == today
        ).scalar()
        
        # 获取本周新增用户数
        week_start = today - timedelta(days=today.weekday())
        new_users_this_week = db.query(
            func.count(User.id)
        ).filter(
            func.date(User.created_at) >= week_start
        ).scalar()
        
        # 获取用户趋势（最近7天的新增用户数）
        seven_days_ago = today - timedelta(days=7)
        daily_new_users = db.query(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('count')
        ).filter(
            func.date(User.created_at) >= seven_days_ago
        ).group_by(
            func.date(User.created_at)
        ).all()
        
        # 转换为字典格式
        daily_new_users_dict = {
            str(date): count 
            for date, count in daily_new_users
        }
        
        # 填充没有数据的日期
        date_range = [
            (seven_days_ago + timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range(8)
        ]
        
        trend_data = [
            {
                "date": date,
                "value": daily_new_users_dict.get(date, 0)
            }
            for date in date_range
        ]
        
        logger.info({
            "action": "get_statistics_overview",
            "total_users": total_users,
            "today_active_users": today_active_users,
            "new_users_this_week": new_users_this_week
        })
        
        return {
            "total_users": total_users,
            "today_active_users": today_active_users,
            "new_users_this_week": new_users_this_week,
            "user_trend": trend_data
        }
        
    except Exception as e:
        logger.error(f"Error getting statistics overview: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting statistics"
        ) 