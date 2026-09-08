from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from decimal import Decimal
from datetime import datetime
from app.schemas.location import LocationBase, LocationOut
from app.schemas.property_image import PropertyImageBase, PropertyImageOut

class ListingBase(BaseModel):
    title: str = Field(..., max_length=150)
    description: str
    price: Decimal = Field(..., gte=0)
    property_type: Literal["house", "apartment", "condo", "land"]
    listing_type: Literal["sale", "rent"]
    bedrooms: int = 0
    bathrooms: float = 0.0
    square_footage: Optional[int] = None

class ListingCreate(ListingBase):
    location: LocationBase
    images: List[PropertyImageBase] = []

class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    property_type: Optional[Literal["house", "apartment", "condo", "land"]] = None
    listing_type: Optional[Literal["sale", "rent"]] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_footage: Optional[int] = None
    is_published: Optional[bool] = None

class ListingOut(ListingBase):
    id: int
    agent_id: int
    is_published: bool
    created_at: datetime
    location: Optional[LocationOut]
    images: List[PropertyImageOut] = []

    class Config:
        from_attributes = True
