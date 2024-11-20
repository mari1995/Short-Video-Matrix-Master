from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class VideoGeneration(BaseModel):
    """视频生成记录模型"""
    __tablename__ = "video_generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255))
    status = Column(String(50))
    duration = Column(Float)
    transition = Column(String(50))
    output_url = Column(String(1024))
    error_message = Column(Text)
    source_images = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "duration": self.duration,
            "transition": self.transition,
            "output_url": self.output_url,
            "error_message": self.error_message,
            "source_images": self.source_images,
            "created_at": self.created_at.timestamp() if self.created_at else None,
            "updated_at": self.updated_at.timestamp() if self.updated_at else None
        } 