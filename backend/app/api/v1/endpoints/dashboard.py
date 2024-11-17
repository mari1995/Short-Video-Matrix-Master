from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.deps import get_current_active_user
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.operation_log import OperationLog
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """获取仪表盘统计数据"""
    # 获取用户总数
    total_users = db.query(func.count(User.id)).scalar()
    
    # 获取今日活跃用户数
    today = datetime.now().date()
    today_active_users = db.query(func.count(func.distinct(OperationLog.user_id)))\
        .filter(func.date(OperationLog.created_at) == today)\
        .scalar()
    
    # 获取最近7天的操作日志统计
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_logs = db.query(func.date(OperationLog.created_at), 
                          func.count(OperationLog.id))\
        .filter(OperationLog.created_at >= seven_days_ago)\
        .group_by(func.date(OperationLog.created_at))\
        .all()
    
    # 获取最近的操作日志
    recent_activities = db.query(OperationLog)\
        .order_by(OperationLog.created_at.desc())\
        .limit(5)\
        .all()
    
    return {
        "total_users": total_users,
        "today_active_users": today_active_users,
        "recent_logs": [{"date": str(date), "count": count} 
                       for date, count in recent_logs],
        "recent_activities": [
            {
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "created_at": str(log.created_at)
            } for log in recent_activities
        ]
    } 