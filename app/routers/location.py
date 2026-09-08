from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.schemas.location import LocationOut, LocationBase
from sqlalchemy.future import select
from app.models.location import Location
from app.repositories.location import LocationRepository
from app.services.location import LocationIQService
from app.services.user import UserService
from pydantic import BaseModel

router = APIRouter(prefix="/api/locations", tags=["Locations"])


class GeocodeRequest(BaseModel):
    address: str


@router.get("/{listing_id}", response_model=LocationOut)
async def get_property_location(listing_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location).where(Location.listing_id == listing_id))
    location = result.scalars().first()
    if not location:
        raise HTTPException(status_code=404, detail="Location metadata not found for this property")
    return location


@router.put("/{listing_id}", response_model=LocationOut)
async def update_location(listing_id: int, location_in: LocationBase, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    updated = await LocationRepository.update(db, listing_id, location_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated


@router.post("/geocode")
async def geocode_address(request: GeocodeRequest):
    coords = await LocationIQService.geocode(request.address)
    if not coords:
        raise HTTPException(status_code=404, detail="Address not found")
    return coords