from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.location import Location
from app.schemas.location import LocationBase

class LocationRepository:
    @staticmethod
    async def get_by_listing_id(db: AsyncSession, listing_id: int) -> Optional[Location]:
        result = await db.execute(select(Location).where(Location.listing_id == listing_id))
        return result.scalars().first()

    @staticmethod
    async def update(db: AsyncSession, listing_id: int, location_in: LocationBase) -> Optional[Location]:
        result = await db.execute(select(Location).where(Location.listing_id == listing_id))
        db_location = result.scalars().first()
        if db_location:
            db_location.country = location_in.country
            db_location.street_address = location_in.street_address
            db_location.city = location_in.city
            db_location.state_province = location_in.state_province
            db_location.postal_code = location_in.postal_code
            db_location.latitude = location_in.latitude
            db_location.longitude = location_in.longitude
            await db.commit()
            await db.refresh(db_location)
        return db_location
