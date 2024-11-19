from fastapi import Request, Response
from loguru import logger
import time
from typing import Callable
import json
from fastapi import UploadFile

async def log_request_middleware(request: Request, call_next: Callable) -> Response:
    """记录请求和响应的中间件"""
    request_id = str(time.time())
    await log_request(request, request_id)
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    await log_response(response, request_id, process_time)
    return response

async def log_request(request: Request, request_id: str):
    """记录请求详情"""
    body = None
    if request.method in ["POST", "PUT"]:
        content_type = request.headers.get('content-type', '')
        if 'multipart/form-data' in content_type:
            # 处理文件上传
            form = await request.form()
            body = {}
            for key, value in form.items():
                if isinstance(value, UploadFile):
                    # 对于文件，只记录文件名和大小
                    body[key] = {
                        'filename': value.filename,
                        'content_type': value.content_type,
                        'size': 'unknown'  # 文件大小在这里无法获取
                    }
                else:
                    body[key] = str(value)
        else:
            try:
                body = await request.json()
            except:
                body = "Could not parse body"

    log_dict = {
        "request_id": request_id,
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "path_params": request.path_params,
        "query_params": dict(request.query_params),
        "body": body
    }

    logger.info(f"API Request | {json.dumps(log_dict, ensure_ascii=False)}")

async def log_response(response: Response, request_id: str, process_time: float):
    """记录响应详情"""
    log_dict = {
        "request_id": request_id,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "process_time": f"{process_time:.3f}s"
    }

    # 尝试获取响应体
    try:
        body = json.loads(response.body.decode())
        log_dict["body"] = body
    except:
        log_dict["body"] = "Could not parse response body"

    logger.info(f"API Response | {json.dumps(log_dict, ensure_ascii=False)}") 