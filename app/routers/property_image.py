from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from app.schemas.property_image import PropertyImageCreate, PropertyImageUpdate, PropertyImageOut
from sqlalchemy.future import select
from app.models.property_image import PropertyImage
from app.services.user import UserService
from app.repositories.property_image import PropertyImageRepository

router = APIRouter(prefix="/api/property-images", tags=["Property Images"])

@router.post("/{listing_id}", response_model=PropertyImageOut, status_code=status.HTTP_201_CREATED)
async def create_property_image(
    listing_id: int,
    image_in: PropertyImageCreate,
    current_user = Depends(UserService.require_buyer_or_agent),
    db: AsyncSession = Depends(get_db)
):
    return await PropertyImageRepository.create(db, image_in, listing_id)

@router.get("/listing/{listing_id}", response_model=List[PropertyImageOut])
async def get_listing_images(listing_id: int, db: AsyncSession = Depends(get_db)):
    return await PropertyImageRepository.get_by_listing_id(db, listing_id)

@router.put("/{image_id}", response_model=PropertyImageOut)
async def update_property_image(
    image_id: int,
    image_in: PropertyImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(UserService.require_buyer_or_agent)
):
    updated = await PropertyImageRepository.update(db, image_id, image_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Image not found")
    return updated

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property_image(
    image_id: int,
    current_user = Depends(UserService.require_buyer_or_agent),
    db: AsyncSession = Depends(get_db)
):
    success = await PropertyImageRepository.delete(db, image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image record not found")
    return None