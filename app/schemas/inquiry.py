from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime

class InquiryBase(BaseModel):
    listing_id: int
    message: str

class InquiryCreate(InquiryBase):
    pass

class InquiryUpdate(BaseModel):
    message: Optional[str] = None
    status: Optional[Literal["pending", "contacted", "closed"]] = None

class InquiryOut(InquiryBase):
    id: int
    user_id: Optional[int]
    status: Literal["pending", "contacted", "closed"]
    sent_at: datetime

    class Config:
        from_attributes = True
