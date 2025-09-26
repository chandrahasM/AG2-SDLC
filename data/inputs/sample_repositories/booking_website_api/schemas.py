"""
Pydantic schemas for Booking Website API
Data validation and serialization schemas
"""

from pydantic import BaseModel, Field, EmailStr, validator, root_validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"

class RoomType(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"
    DELUXE = "deluxe"
    PRESIDENTIAL = "presidential"

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"

# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    date_of_birth: Optional[date] = None
    role: UserRole = UserRole.CUSTOMER

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    date_of_birth: Optional[date] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class HotelBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    address: str = Field(..., min_length=10, max_length=200)
    city: str = Field(..., min_length=2, max_length=50)
    country: str = Field(..., min_length=2, max_length=50)
    star_rating: int = Field(..., ge=1, le=5)
    amenities: List[str] = Field(default_factory=list)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    address: Optional[str] = Field(None, min_length=10, max_length=200)
    city: Optional[str] = Field(None, min_length=2, max_length=50)
    country: Optional[str] = Field(None, min_length=2, max_length=50)
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    amenities: Optional[List[str]] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class HotelResponse(HotelBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=10)
    room_type: RoomType
    price_per_night: float = Field(..., gt=0)
    max_occupancy: int = Field(..., ge=1, le=10)
    size_sqm: Optional[float] = Field(None, gt=0)
    amenities: List[str] = Field(default_factory=list)
    description: Optional[str] = Field(None, max_length=500)

class RoomCreate(RoomBase):
    hotel_id: int

class RoomUpdate(BaseModel):
    room_number: Optional[str] = Field(None, min_length=1, max_length=10)
    room_type: Optional[RoomType] = None
    price_per_night: Optional[float] = Field(None, gt=0)
    max_occupancy: Optional[int] = Field(None, ge=1, le=10)
    size_sqm: Optional[float] = Field(None, gt=0)
    amenities: Optional[List[str]] = None
    description: Optional[str] = Field(None, max_length=500)

class RoomResponse(RoomBase):
    id: int
    hotel_id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    check_in_date: date
    check_out_date: date
    adults: int = Field(..., ge=1, le=10)
    children: int = Field(0, ge=0, le=10)
    special_requests: Optional[str] = Field(None, max_length=500)

    @validator('check_out_date')
    def check_out_after_check_in(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('Check-out date must be after check-in date')
        return v

    @root_validator
    def validate_booking_dates(cls, values):
        check_in = values.get('check_in_date')
        check_out = values.get('check_out_date')
        
        if check_in and check_out:
            # Check if booking is not too far in the future (1 year)
            from datetime import date, timedelta
            max_future_date = date.today() + timedelta(days=365)
            if check_in > max_future_date:
                raise ValueError('Check-in date cannot be more than 1 year in the future')
            
            # Check if booking is not too far in the past
            if check_in < date.today():
                raise ValueError('Check-in date cannot be in the past')
        
        return values

class BookingCreate(BookingBase):
    room_id: int

class BookingUpdate(BaseModel):
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    adults: Optional[int] = Field(None, ge=1, le=10)
    children: Optional[int] = Field(None, ge=0, le=10)
    special_requests: Optional[str] = Field(None, max_length=500)

class BookingResponse(BookingBase):
    id: int
    user_id: int
    room_id: int
    status: BookingStatus
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0)
    payment_method: PaymentMethod
    transaction_id: Optional[str] = Field(None, max_length=100)

class PaymentCreate(PaymentBase):
    booking_id: int

class PaymentResponse(PaymentBase):
    id: int
    booking_id: int
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    comment: Optional[str] = Field(None, max_length=1000)

class ReviewCreate(ReviewBase):
    hotel_id: int
    booking_id: Optional[int] = None

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    hotel_id: int
    booking_id: Optional[int]
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SearchFilters(BaseModel):
    city: Optional[str] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    adults: int = Field(1, ge=1, le=10)
    children: int = Field(0, ge=0, le=10)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    amenities: Optional[List[str]] = None
    room_type: Optional[RoomType] = None

    @root_validator
    def validate_price_range(cls, values):
        min_price = values.get('min_price')
        max_price = values.get('max_price')
        
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError('Minimum price cannot be greater than maximum price')
        
        return values

class SearchResponse(BaseModel):
    hotels: List[HotelResponse]
    total_count: int
    page: int
    per_page: int
    total_pages: int

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
    timestamp: datetime

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database_status: str = "connected"
    services_status: Dict[str, str] = {"email": "active", "payment": "active"}

class StatisticsResponse(BaseModel):
    total_users: int
    total_hotels: int
    total_rooms: int
    total_bookings: int
    total_revenue: float
    average_booking_value: float
    occupancy_rate: float

class NotificationBase(BaseModel):
    title: str = Field(..., max_length=200)
    message: str = Field(..., max_length=1000)
    notification_type: str = Field("email", regex="^(email|sms|push)$")

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    table_name: str
    record_id: int
    action: str
    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
