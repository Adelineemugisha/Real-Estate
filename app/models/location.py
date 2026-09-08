from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, unique=True)
    country = Column(String(30), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state_province = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    __table_args__ = (
        CheckConstraint("latitude BETWEEN -90 AND 90", name="check_lat_range"),
        CheckConstraint("longitude BETWEEN -180 AND 180", name="check_lon_range"),
        UniqueConstraint("listing_id", name="uq_location_listing"),
    )

    # Relationships
    listing = relationship("Listing", back_populates="location")
