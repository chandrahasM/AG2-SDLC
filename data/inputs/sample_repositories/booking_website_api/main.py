"""
Booking Website API - FastAPI Application
A comprehensive booking system with hotels, rooms, reservations, and payments
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from enum import Enum
import uvicorn
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Booking Website API",
    description="A comprehensive hotel booking system with rooms, reservations, and payments",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

# Security
security = HTTPBearer()

# Enums
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

# Pydantic Models
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    date_of_birth: Optional[date] = None
    role: UserRole = UserRole.CUSTOMER

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

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

class SearchResponse(BaseModel):
    hotels: List[HotelResponse]
    total_count: int
    page: int
    per_page: int
    total_pages: int

# Dependency functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    # Mock implementation - in real app, validate JWT token
    return {
        "id": 1,
        "email": "user@example.com",
        "role": UserRole.CUSTOMER
    }

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    """Ensure user is admin"""
    if current_user["role"] not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Booking Website API",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# User endpoints
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    """Create a new user"""
    # Mock implementation
    logger.info(f"Creating user: {user.email}")
    background_tasks.add_task(send_welcome_email, user.email)
    
    return UserResponse(
        id=1,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        date_of_birth=user.date_of_birth,
        role=user.role,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        first_name="John",
        last_name="Doe",
        phone="+1234567890",
        role=current_user["role"],
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.put("/users/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current user profile"""
    # Mock implementation
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        first_name=user_update.first_name or "John",
        last_name=user_update.last_name or "Doe",
        phone=user_update.phone,
        date_of_birth=user_update.date_of_birth,
        role=current_user["role"],
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

# Hotel endpoints
@app.post("/hotels/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(
    hotel: HotelCreate,
    current_user: dict = Depends(get_admin_user)
):
    """Create a new hotel (Admin only)"""
    logger.info(f"Creating hotel: {hotel.name}")
    
    return HotelResponse(
        id=1,
        name=hotel.name,
        description=hotel.description,
        address=hotel.address,
        city=hotel.city,
        country=hotel.country,
        star_rating=hotel.star_rating,
        amenities=hotel.amenities,
        latitude=hotel.latitude,
        longitude=hotel.longitude,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.get("/hotels/", response_model=List[HotelResponse])
async def get_hotels(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    star_rating: Optional[int] = None
):
    """Get list of hotels with optional filtering"""
    # Mock implementation
    hotels = []
    return hotels

@app.get("/hotels/{hotel_id}", response_model=HotelResponse)
async def get_hotel(hotel_id: int):
    """Get hotel by ID"""
    if hotel_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid hotel ID"
        )
    
    # Mock implementation
    return HotelResponse(
        id=hotel_id,
        name="Grand Hotel",
        description="A luxurious hotel in the city center",
        address="123 Main Street",
        city="New York",
        country="USA",
        star_rating=5,
        amenities=["WiFi", "Pool", "Spa", "Gym"],
        latitude=40.7128,
        longitude=-74.0060,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.put("/hotels/{hotel_id}", response_model=HotelResponse)
async def update_hotel(
    hotel_id: int,
    hotel_update: HotelUpdate,
    current_user: dict = Depends(get_admin_user)
):
    """Update hotel (Admin only)"""
    # Mock implementation
    return HotelResponse(
        id=hotel_id,
        name=hotel_update.name or "Grand Hotel",
        description=hotel_update.description,
        address=hotel_update.address or "123 Main Street",
        city=hotel_update.city or "New York",
        country=hotel_update.country or "USA",
        star_rating=hotel_update.star_rating or 5,
        amenities=hotel_update.amenities or ["WiFi", "Pool"],
        latitude=hotel_update.latitude,
        longitude=hotel_update.longitude,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

# Room endpoints
@app.post("/rooms/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room: RoomCreate,
    current_user: dict = Depends(get_admin_user)
):
    """Create a new room (Admin only)"""
    logger.info(f"Creating room: {room.room_number}")
    
    return RoomResponse(
        id=1,
        hotel_id=room.hotel_id,
        room_number=room.room_number,
        room_type=room.room_type,
        price_per_night=room.price_per_night,
        max_occupancy=room.max_occupancy,
        size_sqm=room.size_sqm,
        amenities=room.amenities,
        description=room.description,
        is_available=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.get("/hotels/{hotel_id}/rooms", response_model=List[RoomResponse])
async def get_hotel_rooms(
    hotel_id: int,
    available_only: bool = True,
    room_type: Optional[RoomType] = None
):
    """Get rooms for a specific hotel"""
    # Mock implementation
    rooms = []
    return rooms

@app.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int):
    """Get room by ID"""
    # Mock implementation
    return RoomResponse(
        id=room_id,
        hotel_id=1,
        room_number="101",
        room_type=RoomType.DOUBLE,
        price_per_night=150.0,
        max_occupancy=2,
        size_sqm=25.0,
        amenities=["WiFi", "TV", "Mini Bar"],
        description="Comfortable double room with city view",
        is_available=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

# Search endpoints
@app.post("/search", response_model=SearchResponse)
async def search_hotels(filters: SearchFilters):
    """Search for hotels with filters"""
    logger.info(f"Searching hotels with filters: {filters}")
    
    # Mock implementation
    return SearchResponse(
        hotels=[],
        total_count=0,
        page=1,
        per_page=20,
        total_pages=0
    )

# Booking endpoints
@app.post("/bookings/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking: BookingCreate,
    current_user: dict = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    """Create a new booking"""
    logger.info(f"Creating booking for user {current_user['id']}")
    
    # Calculate total amount (mock)
    total_amount = 150.0 * (booking.check_out_date - booking.check_in_date).days
    
    booking_response = BookingResponse(
        id=1,
        user_id=current_user["id"],
        room_id=booking.room_id,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        adults=booking.adults,
        children=booking.children,
        special_requests=booking.special_requests,
        status=BookingStatus.PENDING,
        total_amount=total_amount,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    if background_tasks:
        background_tasks.add_task(send_booking_confirmation, booking_response.id)
    
    return booking_response

@app.get("/bookings/", response_model=List[BookingResponse])
async def get_user_bookings(
    current_user: dict = Depends(get_current_user),
    status: Optional[BookingStatus] = None
):
    """Get user's bookings"""
    # Mock implementation
    bookings = []
    return bookings

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get booking by ID"""
    # Mock implementation
    return BookingResponse(
        id=booking_id,
        user_id=current_user["id"],
        room_id=1,
        check_in_date=date.today() + timedelta(days=7),
        check_out_date=date.today() + timedelta(days=10),
        adults=2,
        children=0,
        special_requests="Late checkout requested",
        status=BookingStatus.CONFIRMED,
        total_amount=450.0,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.put("/bookings/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update booking"""
    # Mock implementation
    return BookingResponse(
        id=booking_id,
        user_id=current_user["id"],
        room_id=1,
        check_in_date=booking_update.check_in_date or date.today() + timedelta(days=7),
        check_out_date=booking_update.check_out_date or date.today() + timedelta(days=10),
        adults=booking_update.adults or 2,
        children=booking_update.children or 0,
        special_requests=booking_update.special_requests,
        status=BookingStatus.CONFIRMED,
        total_amount=450.0,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Cancel booking"""
    logger.info(f"Cancelling booking {booking_id} for user {current_user['id']}")
    # Mock implementation
    return None

# Payment endpoints
@app.post("/payments/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a payment for a booking"""
    logger.info(f"Processing payment for booking {payment.booking_id}")
    
    return PaymentResponse(
        id=1,
        booking_id=payment.booking_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        transaction_id=payment.transaction_id,
        status=PaymentStatus.COMPLETED,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.get("/payments/", response_model=List[PaymentResponse])
async def get_user_payments(current_user: dict = Depends(get_current_user)):
    """Get user's payment history"""
    # Mock implementation
    payments = []
    return payments

# Background tasks
async def send_welcome_email(email: str):
    """Send welcome email to new user"""
    logger.info(f"Sending welcome email to {email}")
    # Mock implementation

async def send_booking_confirmation(booking_id: int):
    """Send booking confirmation email"""
    logger.info(f"Sending booking confirmation for booking {booking_id}")
    # Mock implementation

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal server error",
        "status_code": 500,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
