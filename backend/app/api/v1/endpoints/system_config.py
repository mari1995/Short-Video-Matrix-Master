from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.crud import system_config
from pydantic import BaseModel
from app.api.v1.deps import get_current_user
from app.db.models.user import User
from app.db.models.system_config import SystemConfig

router = APIRouter()

class ConfigCreate(BaseModel):
    config_key: str
    config_value: str
    description: Optional[str] = None
    is_secret: bool = False

class ConfigUpdate(BaseModel):
    config_value: str
    description: Optional[str] = None
    is_secret: Optional[bool] = None

@router.get("/")
async def get_configs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取所有配置"""
    configs = db.query(SystemConfig).filter(SystemConfig.user_id == current_user.id).all()
    return [config.serialize() for config in configs]

@router.get("/{key}")
async def get_config(
    key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定配置"""
    config = system_config.get_config(db, key)
    if not config or config.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Config not found")
    return config.serialize()

@router.post("/")
async def create_config(
    config_create: ConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建配置"""
    # 检查配置是否已存在
    if system_config.get_config(db, config_create.config_key):
        raise HTTPException(
            status_code=400,
            detail=f"Config with key {config_create.config_key} already exists"
        )
    
    # 创建配置
    config = system_config.create_config(
        db=db,
        user_id=current_user.id,
        key=config_create.config_key,
        value=config_create.config_value,
        description=config_create.description,
        is_secret=config_create.is_secret
    )
    return config.serialize()

@router.put("/{key}")
async def update_config(
    key: str,
    config_update: ConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新配置"""
    config = system_config.get_config(db, key)
    if not config or config.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Config not found")
    
    config = system_config.update_config(
        db=db,
        key=key,
        value=config_update.config_value,
        description=config_update.description,
        is_secret=config_update.is_secret
    )
    return config.serialize()

@router.delete("/{key}")
async def delete_config(
    key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除配置"""
    if key in ['openai_base_url', 'openai_api_key']:
        raise HTTPException(status_code=400, detail="Cannot delete system default configs")
    
    config = system_config.get_config(db, key)
    if not config or config.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Config not found")
    
    system_config.delete_config(db, key)
    return {"message": "Config deleted successfully"} 