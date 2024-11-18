from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.crud import system_config
from pydantic import BaseModel

router = APIRouter()

class ConfigCreate(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    is_secret: bool = False

class ConfigUpdate(BaseModel):
    value: str
    description: Optional[str] = None
    is_secret: Optional[bool] = None

@router.get("/")
async def get_configs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取所有配置"""
    configs = system_config.get_configs(db, skip=skip, limit=limit)
    return [config.serialize for config in configs]

@router.get("/{key}")
async def get_config(key: str, db: Session = Depends(get_db)):
    """获取指定配置"""
    config = system_config.get_config(db, key)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config.serialize

@router.post("/")
async def create_config(
    config_create: ConfigCreate,
    db: Session = Depends(get_db)
):
    """创建新配置"""
    if system_config.get_config(db, config_create.key):
        raise HTTPException(status_code=400, detail="Config key already exists")
    
    config = system_config.create_config(
        db,
        key=config_create.key,
        value=config_create.value,
        description=config_create.description,
        is_secret=config_create.is_secret
    )
    return config.serialize

@router.put("/{key}")
async def update_config(
    key: str,
    config_update: ConfigUpdate,
    db: Session = Depends(get_db)
):
    """更新配置"""
    config = system_config.get_config(db, key)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    
    update_data = {
        "value": config_update.value
    }
    if config_update.description is not None:
        update_data["description"] = config_update.description
    if config_update.is_secret is not None:
        update_data["is_secret"] = config_update.is_secret
    
    updated_config = system_config.update_config_full(db, key, update_data)
    return updated_config.serialize

@router.delete("/{key}")
async def delete_config(key: str, db: Session = Depends(get_db)):
    """删除配置"""
    if key in ['openai_base_url', 'openai_api_key']:
        raise HTTPException(status_code=400, detail="Cannot delete system default configs")
    
    if system_config.delete_config(db, key):
        return {"message": "Config deleted successfully"}
    raise HTTPException(status_code=404, detail="Config not found") 