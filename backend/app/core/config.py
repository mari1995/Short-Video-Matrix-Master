from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    # 基础配置
    API_V1_STR: str
    PROJECT_NAME: str
    SECRET_KEY: str
    
    # MySQL数据库配置
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    
    # JWT配置
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # 文件存储路径
    UPLOAD_DIR: str
    YOUTUBE_DOWNLOAD_DIR: str
    FRAMES_DIR: str
    DRAFTS_DIR: str
    
    # API配置
    OPENAPI_BASE_URL: str
    
    # 数据库URL
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
    
    # 确保文件目录存在
    def ensure_dirs(self):
        for dir_path in [
            self.UPLOAD_DIR,
            self.YOUTUBE_DOWNLOAD_DIR,
            self.FRAMES_DIR,
            self.DRAFTS_DIR
        ]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings

settings = get_settings() 