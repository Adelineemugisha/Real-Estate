from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.favorite import favorites

class FavoriteRepository:
    @staticmethod
    async def is_favorited(db: AsyncSession, user_id: int, listing_id: int) -> bool:
        stmt = select(favorites).where(favorites.c.user_id == user_id, favorites.c.listing_id == listing_id)
        result = await db.execute(stmt)
        return result.first() is not None

    @staticmethod
    async def add(db: AsyncSession, user_id: int, listing_id: int) -> None:
        ins_stmt = favorites.insert().values(user_id=user_id, listing_id=listing_id)
        await db.execute(ins_stmt)
        await db.commit()

    @staticmethod
    async def remove(db: AsyncSession, user_id: int, listing_id: int) -> None:
        del_stmt = favorites.delete().where(favorites.c.user_id == user_id, favorites.c.listing_id == listing_id)
        await db.execute(del_stmt)
        await db.commit()
