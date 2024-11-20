from app.db.models.user import User
from app.db.models.operation_log import OperationLog
from app.db.models.statistics import DailyStatistics
from app.db.base import Base, engine

# 创建所有表
def init_db():
    Base.metadata.create_all(bind=engine) 