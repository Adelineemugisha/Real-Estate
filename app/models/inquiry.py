import datetime
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from app.models.enums import InquiryStatus

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(InquiryStatus), nullable=False, default=InquiryStatus.PENDING)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)

    buyer = relationship("User", back_populates="inquiries")
    listing = relationship("Listing", back_populates="inquiries")
