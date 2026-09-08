import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from database import Base

favorites = Table(
    "favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("listing_id", Integer, ForeignKey("listings.id", ondelete="CASCADE"), primary_key=True),
    Column("saved_at", DateTime, default=datetime.datetime.utcnow)
)
