import logging
import sys
from pathlib import Path
from loguru import logger

# 配置日志文件路径
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
API_LOG_FILE = LOG_DIR / "api.log"

# 配置 loguru
logger.remove()  # 移除默认处理器
logger.add(
    API_LOG_FILE,
    rotation="500 MB",  # 日志文件大小超过500MB时轮转
    retention="10 days",  # 保留10天的日志
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    encoding="utf-8"
)
logger.add(sys.stderr, level="INFO")  # 同时输出到控制台 