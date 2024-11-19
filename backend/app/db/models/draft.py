from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class Draft(BaseModel):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    source_url = Column(String(1024))  # 原始图片URL
    file_url = Column(String(1024))    # 保存后的文件URL
    file_type = Column(String(50))     # 文件类型：image, video 等
    description = Column(Text, nullable=True)
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