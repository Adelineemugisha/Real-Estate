from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from app.services.user import UserService
from app.repositories.favorite import FavoriteRepository
from app.schemas.favorite import FavoriteOut
from sqlalchemy.future import select
from app.models.favorite import favorites
from app.models.listing import Listing

router = APIRouter(prefix="/api/favorites", tags=["Favorites Wishlist"])

@router.post("/{listing_id}")
async def toggle_favorite_property(
    listing_id: int,
    current_user = Depends(UserService.require_buyer_or_agent),
    db: AsyncSession = Depends(get_db)
):
    if await FavoriteRepository.is_favorited(db, current_user.id, listing_id):
        await FavoriteRepository.remove(db, current_user.id, listing_id)
        return {"status": "success", "action": "removed_from_wishlist"}
    else:
        await FavoriteRepository.add(db, current_user.id, listing_id)
        return {"status": "success", "action": "added_to_wishlist"}

@router.get("/", response_model=List[FavoriteOut])
async def get_user_favorites(
    current_user = Depends(UserService.require_buyer_or_agent),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(favorites, Listing)
        .join(Listing, favorites.c.listing_id == Listing.id)
        .where(favorites.c.user_id == current_user.id)
    )
    rows = result.all()
    return [
        {
            "user_id": row[0].user_id,
            "listing_id": row[0].listing_id,
            "saved_at": row[0].saved_at,
            "listing": {
                "id": row[1].id,
                "title": row[1].title,
                "price": row[1].price,
            }
        }
        for row in rows
    ]