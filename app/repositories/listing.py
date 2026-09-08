from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.listing import Listing
from app.models.location import Location
from app.models.property_image import PropertyImage
from app.schemas.listing import ListingCreate, ListingUpdate
from app.services.location import LocationIQService

class ListingRepository:
    @staticmethod
    async def create(db: AsyncSession, listing_in: ListingCreate, agent_id: int) -> Listing:
        db_listing = Listing(
            agent_id=agent_id,
            title=listing_in.title,
            description=listing_in.description,
            price=listing_in.price,
            property_type=listing_in.property_type,
            listing_type=listing_in.listing_type,
            bedrooms=listing_in.bedrooms,
            bathrooms=listing_in.bathrooms,
            square_footage=listing_in.square_footage,
            is_published=True
        )
        db.add(db_listing)
        await db.flush()

        latitude = listing_in.location.latitude
        longitude = listing_in.location.longitude

        if latitude is None or longitude is None:
            address = LocationIQService.build_address(listing_in.location)

            coords = await LocationIQService.geocode(address)
            if coords:
                latitude = coords["lat"]
                longitude = coords["lon"]

        db_loc = Location(
            listing_id=db_listing.id,
            country=listing_in.location.country,
            street_address=listing_in.location.street_address,
            city=listing_in.location.city,
            state_province=listing_in.location.state_province,
            postal_code=listing_in.location.postal_code,
            latitude=latitude,
            longitude=longitude
        )
        db.add(db_loc)

        for img in listing_in.images:
            db_img = PropertyImage(
                listing_id=db_listing.id,
                image_url=img.image_url,
                is_primary=img.is_primary
            )
            db.add(db_img)

        await db.commit()
        return await ListingRepository.get_by_id(db, db_listing.id)

    @staticmethod
    async def get_all(db: AsyncSession, city: Optional[str] = None) -> List[Listing]:
        stmt = select(Listing).options(selectinload(Listing.location), selectinload(Listing.images))
        if city:
            stmt = stmt.join(Location).where(Location.city.ilike(f"%{city}%"))
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, listing_id: int) -> Optional[Listing]:
        stmt = select(Listing).where(Listing.id == listing_id).options(
            selectinload(Listing.location), selectinload(Listing.images)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def update(db: AsyncSession, listing_id: int, listing_in: ListingUpdate) -> Optional[Listing]:
        result = await db.execute(select(Listing).where(Listing.id == listing_id))
        db_listing = result.scalars().first()
        if not db_listing:
            return None
        update_data = listing_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_listing, key, value)
        await db.commit()
        await db.refresh(db_listing)
        return db_listing

    @staticmethod
    async def delete(db: AsyncSession, listing_id: int) -> bool:
        result = await db.execute(select(Listing).where(Listing.id == listing_id))
        db_listing = result.scalars().first()
        if db_listing:
            await db.delete(db_listing)
            await db.commit()
            return True
        return False
