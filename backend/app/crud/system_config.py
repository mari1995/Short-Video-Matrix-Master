from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.db.models.system_config import SystemConfig

def get_config(db: Session, key: str) -> Optional[SystemConfig]:
    """获取配置项"""
    return db.query(SystemConfig).filter(SystemConfig.key == key).first()

def get_configs(db: Session, skip: int = 0, limit: int = 100) -> List[SystemConfig]:
    """获取配置列表"""
    return db.query(SystemConfig).offset(skip).limit(limit).all()

def create_config(db: Session, key: str, value: str, description: str = None, is_secret: bool = False) -> SystemConfig:
    """创建配置项"""
    config = SystemConfig(
        key=key,
        value=value,
        description=description,
        is_secret=is_secret
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    return config

def update_config(db: Session, key: str, value: str) -> Optional[SystemConfig]:
    """更新配置项"""
    config = get_config(db, key)
    if config:
        config.value = value
        db.commit()
        db.refresh(config)
    return config

def delete_config(db: Session, key: str) -> bool:
    """删除配置项"""
    config = get_config(db, key)
    if config:
        db.delete(config)
        db.commit()
        return True
    return False

def init_default_configs(db: Session):
    """初始化默认配置"""
    defaults = [
        {
            'key': 'openapi_base_url',
            'value': 'https://api.openai.com/v1',
            'description': 'openapi API 基础URL',
            'is_secret': False
        },
        {
            'key': 'openapi_api_key',
            'value': '',
            'description': 'openapi API 密钥',
            'is_secret': True
        }
    ]
    
    for config in defaults:
        if not get_config(db, config['key']):
            create_config(
                db,
                key=config['key'],
                value=config['value'],
                description=config['description'],
                is_secret=config['is_secret']
            )

def update_config_full(db: Session, key: str, update_data: dict) -> Optional[SystemConfig]:
    """完整更新配置项"""
    config = get_config(db, key)
    if config:
        for field, value in update_data.items():
            setattr(config, field, value)
        db.commit()
        db.refresh(config)
    return config 