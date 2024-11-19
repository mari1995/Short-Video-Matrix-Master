from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.crud import system_config
import aiohttp
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class ImageAnalysisRequest(BaseModel):
    image_url: str


class Description(BaseModel):
    text: str


class ImageAnalysisResponse(BaseModel):
    created: str
    data: List[dict]
    is_image_safe: Optional[bool] = None
    prompt: Optional[str] = None
    resolution: Optional[str] = None
    seed: Optional[int] = None
    url: Optional[str] = None


@router.post("/describe")
async def describe_image(
        request: ImageAnalysisRequest,
        db: Session = Depends(get_db)
):
    """解析图片描述"""
    try:
        # 获取API配置
        base_url = system_config.get_config(db, 'openapi_base_url').value
        api_key = system_config.get_config(db, 'openapi_api_key').value

        if not api_key:
            raise HTTPException(status_code=400, detail="openapi API key not configured")

        # 从URL下载图片内容
        async with aiohttp.ClientSession() as session:
            async with session.get(request.image_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to download image")
                file_content = await response.read()

        # 准备请求
        url = f"{base_url}/ideogram/describe"
        headers = {
            'accept': 'application/json',
            'Authorization': api_key
        }

        # 准备multipart表单数据
        form_data = aiohttp.FormData()
        form_data.add_field('image_file', file_content, filename='image.jpg', content_type='image/jpeg')

        # 发送请求到openapi API
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=form_data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"openapi API error: {error_text}"
                    )

                result = await response.json()

                # 转换为我们需要的格式
                return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
