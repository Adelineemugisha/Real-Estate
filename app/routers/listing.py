from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from database import get_db
from app.schemas.listing import ListingCreate, ListingUpdate, ListingOut
from app.repositories.listing import ListingRepository
from app.services.user import UserService

router = APIRouter(prefix="/api/listings", tags=["Listings"])

@router.post("/", response_model=ListingOut, status_code=status.HTTP_201_CREATED)
async def create_listing(
    listing_in: ListingCreate, 
    current_user = Depends(UserService.require_buyer_or_agent), 
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "agent":
        raise HTTPException(status_code=403, detail="Only agents can create listings")
    return await ListingRepository.create(db, listing_in, current_user.id)

@router.get("/", response_model=List[ListingOut])
async def read_listings(city: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await ListingRepository.get_all(db, city)

@router.get("/{listing_id}", response_model=ListingOut)
async def read_listing(listing_id: int, db: AsyncSession = Depends(get_db)):
    listing = await ListingRepository.get_by_id(db, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.put("/{listing_id}", response_model=ListingOut)
async def update_listing(listing_id: int, listing_in: ListingUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    existing = await ListingRepository.get_by_id(db, listing_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if existing.agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this listing")
    updated = await ListingRepository.update(db, listing_id, listing_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Listing not found")
    return updated

@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(listing_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    existing = await ListingRepository.get_by_id(db, listing_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if existing.agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this listing")
    success = await ListingRepository.delete(db, listing_id)
    if not success:
        raise HTTPException(status_code=404, detail="Listing not found")
    return None