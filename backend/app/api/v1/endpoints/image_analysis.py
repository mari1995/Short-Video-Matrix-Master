from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.crud import system_config
import requests  # 使用同步请求库
import json
from pydantic import BaseModel

router = APIRouter()

class ImageAnalysisResponse(BaseModel):
    created: str
    data: list[dict]  # 假设每个对象是一个字典
    is_image_safe: bool = None
    prompt: str = None
    resolution: str = None
    seed: int = None
    url: str = None

@router.post("/describe")
def describe_image(
    image_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """解析图片描述"""
    try:
        # 确认 image_file 的文件数据是否有问题
        if image_file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only JPEG, PNG, and GIF are allowed.")
        
        # 获取API配置
        base_url = system_config.get_config(db, 'ideogram_base_url').value
        api_key = system_config.get_config(db, 'ideogram_api_key').value
        
        if not api_key:
            raise HTTPException(status_code=400, detail="Ideogram API key not configured")
        
        # 准备请求
        url = f"{base_url}/ideogram/describe"
        headers = {
            'accept': 'application/json',
            'Authorization': api_key
        }
        
        # 读取文件内容
        file_content = image_file.file.read()  # 使用同步方式读取文件内容
        
        # 准备multipart表单数据
        files = {
            'image_file': (image_file.filename, file_content, image_file.content_type)
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, files=files)
        
        # 打印调用第三方接口的结果情况
        print(f"Response status: {response.status_code}")
        print(f"Response content type: {response.headers.get('Content-Type')}")
        
        result = response.json()
        print(result)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 