import datetime
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from database import Base
from app.models.favorite import favorites
from app.models.enums import PropertyType, ListingType

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False)
    listing_type = Column(Enum(ListingType), nullable=False)
    bedrooms = Column(Integer, default=0)
    bathrooms = Column(Numeric(3, 1), default=0.0)
    square_footage = Column(Integer, nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_positive_price"),
        CheckConstraint("square_footage > 0", name="check_positive_sqft"),
    )

    # Relationships
    agent = relationship("User", back_populates="listings")
    location = relationship("Location", back_populates="listing", uselist=False, cascade="all, delete-orphan")
    images = relationship("PropertyImage", back_populates="listing", cascade="all, delete-orphan")
    inquiries = relationship("Inquiry", back_populates="listing", cascade="all, delete-orphan")
    favorited_by = relationship("User", secondary=favorites, back_populates="saved_properties")
