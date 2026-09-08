from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.property_image import PropertyImage
from app.schemas.property_image import PropertyImageCreate, PropertyImageUpdate

class PropertyImageRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, image_id: int) -> Optional[PropertyImage]:
        result = await db.execute(select(PropertyImage).where(PropertyImage.id == image_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_listing_id(db: AsyncSession, listing_id: int) -> List[PropertyImage]:
        result = await db.execute(select(PropertyImage).where(PropertyImage.listing_id == listing_id))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, image_in: PropertyImageCreate, listing_id: int) -> PropertyImage:
        db_image = PropertyImage(
            listing_id=listing_id,
            image_url=image_in.image_url,
            is_primary=image_in.is_primary
        )
        db.add(db_image)
        await db.commit()
        await db.refresh(db_image)
        return db_image

    @staticmethod
    async def update(db: AsyncSession, image_id: int, image_in: PropertyImageUpdate) -> Optional[PropertyImage]:
        result = await db.execute(select(PropertyImage).where(PropertyImage.id == image_id))
        db_image = result.scalars().first()
        if not db_image:
            return None
        update_data = image_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_image, key, value)
        await db.commit()
        await db.refresh(db_image)
        return db_image

    @staticmethod
    async def delete(db: AsyncSession, image_id: int) -> bool:
        result = await db.execute(select(PropertyImage).where(PropertyImage.id == image_id))
        image = result.scalars().first()
        if image:
            await db.delete(image)
            await db.commit()
            return True
        return False
