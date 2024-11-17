import logging
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

# 日志文件路径
LOG_FILE = Path("logs/api.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# 日志格式
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# 配置日志
logger.configure(
    handlers=[
        {"sink": sys.stdout, "format": LOG_FORMAT},
        {"sink": str(LOG_FILE), "format": LOG_FORMAT, "rotation": "500 MB"}
    ]
)

# 创建一个拦截器来处理FastAPI的日志
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

# 设置日志级别
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO) 