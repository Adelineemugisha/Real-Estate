from enum import Enum

class UserRole(str, Enum):
    BUYER = "buyer"
    AGENT = "agent"

class PropertyType(str, Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    CONDO = "condo"
    LAND = "land"

class ListingType(str, Enum):
    SALE = "sale"
    RENT = "rent"

class InquiryStatus(str, Enum):
    PENDING = "pending"
    CONTACTED = "contacted"
    CLOSED = "closed"
