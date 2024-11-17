from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "管理后台系统"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = True  # 添加调试模式配置

    class Config:
        case_sensitive = True

settings = Settings() 