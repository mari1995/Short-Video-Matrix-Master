from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class VideoAnalysis(BaseModel):
    """视频分析记录模型"""
    __tablename__ = "video_analyses"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255))
    file_url = Column(String(1024))
    status = Column(String(50))
    duration = Column(Float, nullable=True)
    frame_count = Column(Integer, nullable=True)
    fps = Column(Float, nullable=True)
    resolution = Column(String(50), nullable=True)
    frames_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def serialize(self):
        try:
            return {
                "id": self.id,
                "file_name": self.file_name,
                "file_url": self.file_url,
                "status": self.status,
                "duration": self.duration,
                "frame_count": self.frame_count,
                "fps": self.fps,
                "resolution": self.resolution,
                "frames_data": self.frames_data,
                "error_message": self.error_message,
                "created_at": self.created_at.timestamp() if self.created_at else None,
                "updated_at": self.updated_at.timestamp() if self.updated_at else None
            }
        except Exception as e:
            print(f"Serialization error for VideoAnalysis {self.id}: {str(e)}")
            # 返回基本信息，确保至少有一些数据返回
            return {
                "id": self.id,
                "file_name": self.file_name,
                "status": self.status,
                "error_message": f"Serialization error: {str(e)}"
            } 