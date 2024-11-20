from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class OperationLog(BaseModel):
    """操作日志模型"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(50))
    path = Column(String(255))
    method = Column(String(10))
    params = Column(Text)
    status_code = Column(Integer)
    response = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "path": self.path,
            "method": self.method,
            "params": self.params,
            "status_code": self.status_code,
            "response": self.response,
            "ip_address": self.ip_address,
            "created_at": self.created_at.timestamp() if self.created_at else None
        }