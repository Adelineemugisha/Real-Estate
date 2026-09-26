from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FavoriteBase(BaseModel):
    listing_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteOut(FavoriteBase):
    user_id: int
    saved_at: datetime

    model_config = ConfigDict(from_attributes=True)
