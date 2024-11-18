from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from app.db.models.base_model import BaseModel

class VideoAnalysis(BaseModel):
    """视频分析记录模型"""
    __tablename__ = "video_analysis"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False, comment="视频文件名")
    file_path = Column(String(255), nullable=False, comment="视频文件路径")
    duration = Column(Float, comment="视频时长(秒)")
    frame_count = Column(Integer, comment="总帧数")
    fps = Column(Float, comment="帧率")
    resolution = Column(String(50), comment="分辨率")
    frames_data = Column(JSON, comment="关键帧数据")
    status = Column(String(50), default="processing", comment="分析状态")
    error_message = Column(String(255), comment="错误信息")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'duration': self.duration,
            'frame_count': self.frame_count,
            'fps': self.fps,
            'resolution': self.resolution,
            'frames_data': self.frames_data,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 