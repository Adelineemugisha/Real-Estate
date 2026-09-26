from pydantic import BaseModel, ConfigDict
from typing import Optional

class LocationBase(BaseModel):
    country: str
    street_address: str
    city: str
    state_province: str
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class LocationCreate(LocationBase):
    pass

class LocationOut(LocationBase):
    id: int
    listing_id: int

    model_config = ConfigDict(from_attributes=True)
