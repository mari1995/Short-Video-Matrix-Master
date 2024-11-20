from pydantic import BaseModel
from typing import Optional

class ConfigBase(BaseModel):
    config_key: str
    config_value: str
    description: Optional[str] = None
    is_secret: bool = False

class ConfigCreate(ConfigBase):
    pass

class ConfigUpdate(BaseModel):
    config_value: str
    description: Optional[str] = None
    is_secret: Optional[bool] = None

class ConfigResponse(ConfigBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 