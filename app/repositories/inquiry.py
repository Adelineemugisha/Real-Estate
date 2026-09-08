from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.inquiry import Inquiry
from app.schemas.inquiry import InquiryCreate, InquiryUpdate

class InquiryRepository:
    @staticmethod
    async def create(db: AsyncSession, inquiry_in: InquiryCreate, user_id: int) -> Inquiry:
        db_inquiry = Inquiry(
            user_id=user_id,
            listing_id=inquiry_in.listing_id,
            message=inquiry_in.message
        )
        db.add(db_inquiry)
        await db.commit()
        await db.refresh(db_inquiry)
        return db_inquiry

    @staticmethod
    async def get_by_id(db: AsyncSession, inquiry_id: int) -> Optional[Inquiry]:
        result = await db.execute(select(Inquiry).where(Inquiry.id == inquiry_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_listing_id(db: AsyncSession, listing_id: int) -> List[Inquiry]:
        result = await db.execute(select(Inquiry).where(Inquiry.listing_id == listing_id))
        return result.scalars().all()

    @staticmethod
    async def get_all(db: AsyncSession) -> List[Inquiry]:
        result = await db.execute(select(Inquiry))
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, inquiry_id: int, inquiry_in: InquiryUpdate) -> Optional[Inquiry]:
        result = await db.execute(select(Inquiry).where(Inquiry.id == inquiry_id))
        db_inquiry = result.scalars().first()
        if not db_inquiry:
            return None
        update_data = inquiry_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_inquiry, key, value)
        await db.commit()
        await db.refresh(db_inquiry)
        return db_inquiry

    @staticmethod
    async def delete(db: AsyncSession, inquiry_id: int) -> bool:
        result = await db.execute(select(Inquiry).where(Inquiry.id == inquiry_id))
        db_inquiry = result.scalars().first()
        if db_inquiry:
            await db.delete(db_inquiry)
            await db.commit()
            return True
        return False
