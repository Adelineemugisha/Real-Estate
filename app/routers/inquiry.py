from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from app.schemas.inquiry import InquiryCreate, InquiryUpdate, InquiryOut
from app.services.user import UserService
from app.repositories.inquiry import InquiryRepository
from app.models.inquiry import Inquiry

router = APIRouter(prefix="/api/inquiries", tags=["Inquiries & Leads"])

@router.post("/", response_model=InquiryOut, status_code=status.HTTP_201_CREATED)
async def create_property_inquiry(
    inquiry_in: InquiryCreate,
    current_user = Depends(UserService.require_buyer_or_agent),
    db: AsyncSession = Depends(get_db)
):
    new_inquiry = Inquiry(
        user_id=current_user.id,
        listing_id=inquiry_in.listing_id,
        message=inquiry_in.message
    )
    db.add(new_inquiry)
    await db.commit()
    await db.refresh(new_inquiry)
    return new_inquiry

@router.get("/", response_model=List[InquiryOut])
async def get_all_inquiries(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(UserService.require_buyer_or_agent)
):
    return await InquiryRepository.get_all(db)

@router.get("/{inquiry_id}", response_model=InquiryOut)
async def get_inquiry(inquiry_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    inquiry = await InquiryRepository.get_by_id(db, inquiry_id)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry

@router.put("/{inquiry_id}", response_model=InquiryOut)
async def update_inquiry(inquiry_id: int, inquiry_in: InquiryUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    updated = await InquiryRepository.update(db, inquiry_id, inquiry_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return updated

@router.delete("/{inquiry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inquiry(inquiry_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(UserService.require_buyer_or_agent)):
    success = await InquiryRepository.delete(db, inquiry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return None