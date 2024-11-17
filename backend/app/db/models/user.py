from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(32), unique=True, index=True, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    full_name = Column(String(64))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    role = relationship("Role", back_populates="users")
    logs = relationship("OperationLog", back_populates="user")

class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String(32), unique=True, index=True, nullable=False)
    description = Column(String(256))
    permissions = Column(String(512))  # 存储权限列表，用逗号分隔
    
    users = relationship("User", back_populates="role") 