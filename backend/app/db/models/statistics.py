from sqlalchemy import Column, Integer, Date
from app.db.models.base_model import BaseModel

class DailyStatistics(BaseModel):
    __tablename__ = "daily_statistics"

    date = Column(Date, unique=True, nullable=False)
    visit_count = Column(Integer, default=0)  # 访问次数
    user_count = Column(Integer, default=0)   # 活跃用户数
    new_user_count = Column(Integer, default=0)  # 新增用户数 