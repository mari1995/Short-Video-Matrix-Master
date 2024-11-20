from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, BigInteger, ForeignKey
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class YouTubeHistory(BaseModel):
    """YouTube下载历史模型"""
    __tablename__ = "youtube_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    url = Column(String(1024))
    title = Column(String(255))
    author = Column(String(255))
    duration = Column(Integer)
    views = Column(BigInteger)
    thumbnail_url = Column(String(1024))
    description = Column(Text)
    file_url = Column(String(1024))
    file_size = Column(BigInteger)
    status = Column(String(50), default='pending')
    error_message = Column(Text)
    is_shorts = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "author": self.author,
            "duration": self.duration,
            "views": self.views,
            "thumbnail_url": self.thumbnail_url,
            "description": self.description,
            "file_url": self.file_url,
            "file_size": self.file_size,
            "status": self.status,
            "error_message": self.error_message,
            "is_shorts": self.is_shorts,
            "created_at": self.created_at.timestamp() if self.created_at else None,
            "updated_at": self.updated_at.timestamp() if self.updated_at else None
        }