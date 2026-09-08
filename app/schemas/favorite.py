from pydantic import BaseModel
from datetime import datetime

class FavoriteBase(BaseModel):
    listing_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteOut(FavoriteBase):
    user_id: int
    saved_at: datetime

    class Config:
        from_attributes = True
