from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.db.models.base_model import BaseModel

class SystemConfig(BaseModel):
    """系统配置模型"""
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, comment="配置键")
    value = Column(Text, comment="配置值")
    description = Column(String(255), comment="配置描述")
    is_secret = Column(Boolean, default=False, comment="是否加密存储")
    
    @property
    def serialize(self):
        """返回序列化数据"""
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value if not self.is_secret else '******',
            'description': self.description,
            'is_secret': self.is_secret,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 