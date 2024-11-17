from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base_model import BaseModel

class OperationLog(BaseModel):
    __tablename__ = "operation_logs"

    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(32), nullable=False)  # 操作类型：CREATE, UPDATE, DELETE, LOGIN等
    resource = Column(String(32), nullable=False)  # 操作的资源：USER, ROLE等
    resource_id = Column(Integer)  # 资源ID
    details = Column(String(512))  # 操作详情
    ip_address = Column(String(64))  # 操作IP地址
    
    user = relationship("User", back_populates="logs") 