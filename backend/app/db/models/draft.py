from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class Draft(BaseModel):
    """草稿箱模型"""
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255))
    source_url = Column(String(1024))
    file_url = Column(String(1024))
    file_type = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "source_url": self.source_url,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "description": self.description,
            "created_at": self.created_at.timestamp() if self.created_at else None,
            "updated_at": self.updated_at.timestamp() if self.updated_at else None
        } 