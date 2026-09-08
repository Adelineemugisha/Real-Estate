import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
from app.models.favorite import favorites
from app.models.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.BUYER)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    listings = relationship("Listing", back_populates="agent", cascade="all, delete-orphan")
    inquiries = relationship("Inquiry", back_populates="buyer")
    saved_properties = relationship("Listing", secondary=favorites, back_populates="favorited_by")
