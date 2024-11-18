from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.db.models.base_model import BaseModel

class YouTubeHistory(BaseModel):
    """YouTube下载历史记录模型"""
    __tablename__ = "youtube_history"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False, comment="视频URL")
    title = Column(String(255), comment="视频标题")
    author = Column(String(255), comment="视频作者")
    duration = Column(Integer, comment="视频时长(秒)")
    views = Column(Integer, comment="观看次数")
    thumbnail_url = Column(String(255), comment="缩略图URL")
    description = Column(Text, comment="视频描述")
    is_shorts = Column(Boolean, default=False, comment="是否为Shorts视频")
    file_path = Column(String(255), comment="文件保存路径")
    file_size = Column(Integer, comment="文件大小(字节)")
    download_time = Column(DateTime(timezone=True), server_default=func.now(), comment="下载时间")
    status = Column(String(50), default="success", comment="下载状态: success/failed")
    error_message = Column(Text, comment="错误信息")

    def __repr__(self):
        return f"<YouTubeHistory {self.title}>"

    @property
    def serialize(self):
        """返回序列化数据"""
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'author': self.author,
            'duration': self.duration,
            'views': self.views,
            'thumbnail_url': self.thumbnail_url,
            'description': self.description,
            'is_shorts': self.is_shorts,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'download_time': self.download_time.isoformat() if self.download_time else None,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    class Config:
        orm_mode = True