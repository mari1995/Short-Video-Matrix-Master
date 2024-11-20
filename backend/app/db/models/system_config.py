from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class SystemConfig(BaseModel):
    """系统配置模型"""
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    config_key = Column(String(255), unique=True)
    config_value = Column(Text)
    description = Column(Text)
    is_secret = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "config_key": self.config_key,
            "config_value": self.config_value,
            "description": self.description,
            "is_secret": self.is_secret,
            "created_at": self.created_at.timestamp() if self.created_at else None,
            "updated_at": self.updated_at.timestamp() if self.updated_at else None
        } 