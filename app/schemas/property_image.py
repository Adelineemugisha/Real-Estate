from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PropertyImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class PropertyImageCreate(PropertyImageBase):
    pass

class PropertyImageUpdate(BaseModel):
    image_url: Optional[str] = None
    is_primary: Optional[bool] = None

class PropertyImageOut(PropertyImageBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
