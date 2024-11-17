import os
import sys
import uvicorn
import logging
from pathlib import Path

def setup_debug_environment():
    """设置调试环境变量和路径"""
    # 添加项目根目录到 Python 路径
    project_root = Path(__file__).parent.parent
    sys.path.append(str(project_root))
    
    # 设置环境变量
    os.environ.update({
        "DEBUG": "1",
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "DEBUG",
        "PYTHONPATH": str(project_root)
    })
    
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                project_root / "logs" / "debug.log",
                encoding='utf-8'
            )
        ]
    )

def run_debug_server():
    """运行调试服务器"""
    try:
        # 设置环境
        setup_debug_environment()
        
        # 启动服务器
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["app"],
            log_level="debug",
            workers=1,
            reload_delay=0.25,
            reload_includes=["*.py", "*.json", "*.yaml"],
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nShutting down debug server...")
    except Exception as e:
        print(f"Error starting debug server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_debug_server() 