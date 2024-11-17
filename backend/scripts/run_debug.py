import uvicorn
import os
import sys

if __name__ == "__main__":
    # 设置环境变量
    os.environ["DEBUG"] = "1"
    
    # 设置 Python 路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
        workers=1
    ) 