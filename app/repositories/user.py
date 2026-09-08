from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.security import SecurityService

class UserRepository:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: AsyncSession) -> List[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, user_in: UserCreate) -> User:
        hashed = SecurityService.hash_password(user_in.password)
        db_user = User(
            email=user_in.email,
            hashed_password=hashed,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            phone_number=user_in.phone_number,
            role=user_in.role
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_in: UserUpdate) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            return None
        update_data = user_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if db_user:
            await db.delete(db_user)
            await db.commit()
            return True
        return False
