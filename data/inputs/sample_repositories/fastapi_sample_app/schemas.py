"""
Pydantic schemas for FastAPI Sample Application
Data validation and serialization models
"""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    role: UserRole = Field(UserRole.USER, description="User role")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, description="Password")
    
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
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1)

# Product schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    category: str = Field(..., min_length=1, max_length=50, description="Product category")
    stock_quantity: int = Field(..., ge=0, description="Stock quantity")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    stock_quantity: Optional[int] = Field(None, ge=0)

class ProductResponse(ProductBase):
    id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

# Order schemas
class OrderBase(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Order quantity")

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_price: float
    status: OrderStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Analytics schemas
class DashboardStats(BaseModel):
    total_users: int
    total_products: int
    total_orders: int
    active_products: int
    pending_orders: int

class SalesByCategory(BaseModel):
    category: str
    total_sales: float

class UserActivity(BaseModel):
    new_users: int
    active_users: int

# Pagination schemas
class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Number of records to return")

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool

# Error schemas
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
    timestamp: datetime

# Search schemas
class ProductSearch(BaseModel):
    search_term: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    in_stock_only: bool = False

class OrderFilter(BaseModel):
    status: Optional[OrderStatus] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

# Health check schema
class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    database: str = "connected"
