"""
FastAPI Sample Application for Testing Workflow 1
A comprehensive web API with multiple components to demonstrate analysis capabilities
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import os
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sample FastAPI Application",
    description="A comprehensive FastAPI application for testing Workflow 1",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security configuration
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic models
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    stock_quantity: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_available: bool

class OrderBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime

# In-memory storage (in production, use a database)
users_db: Dict[int, Dict[str, Any]] = {}
products_db: Dict[int, Dict[str, Any]] = {}
orders_db: Dict[int, Dict[str, Any]] = {}
user_counter = 1
product_counter = 1
order_counter = 1

# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Find user in database
    user = None
    for user_data in users_db.values():
        if user_data["username"] == username:
            user = user_data
            break
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

# Service layer
class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def create_user(user_data: UserCreate) -> Dict[str, Any]:
        """Create a new user"""
        global user_counter
        
        # Check if username or email already exists
        for user in users_db.values():
            if user["username"] == user_data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
            if user["email"] == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create user
        user_id = user_counter
        user_counter += 1
        
        user = {
            "id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "role": user_data.role,
            "hashed_password": get_password_hash(user_data.password),
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        
        users_db[user_id] = user
        logger.info(f"Created new user: {user_data.username}")
        return user
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user credentials"""
        for user in users_db.values():
            if user["username"] == username and verify_password(password, user["hashed_password"]):
                return user
        return None

class ProductService:
    """Service class for product operations"""
    
    @staticmethod
    def create_product(product_data: ProductCreate, current_user: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product"""
        global product_counter
        
        # Check if user has permission to create products
        if current_user["role"] not in [UserRole.ADMIN, UserRole.MODERATOR]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        product_id = product_counter
        product_counter += 1
        
        product = {
            "id": product_id,
            "name": product_data.name,
            "description": product_data.description,
            "price": product_data.price,
            "category": product_data.category,
            "stock_quantity": product_data.stock_quantity,
            "is_available": product_data.stock_quantity > 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "created_by": current_user["id"]
        }
        
        products_db[product_id] = product
        logger.info(f"Created new product: {product_data.name}")
        return product
    
    @staticmethod
    def get_products(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all products with pagination"""
        return list(products_db.values())[skip:skip + limit]
    
    @staticmethod
    def get_product(product_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific product"""
        return products_db.get(product_id)

class OrderService:
    """Service class for order operations"""
    
    @staticmethod
    def create_order(order_data: OrderCreate, current_user: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order"""
        global order_counter
        
        # Check if product exists and is available
        product = ProductService.get_product(order_data.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        if not product["is_available"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not available"
            )
        
        if product["stock_quantity"] < order_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )
        
        order_id = order_counter
        order_counter += 1
        
        total_price = product["price"] * order_data.quantity
        
        order = {
            "id": order_id,
            "user_id": current_user["id"],
            "product_id": order_data.product_id,
            "quantity": order_data.quantity,
            "total_price": total_price,
            "status": "pending",
            "created_at": datetime.utcnow()
        }
        
        orders_db[order_id] = order
        
        # Update product stock
        product["stock_quantity"] -= order_data.quantity
        product["is_available"] = product["stock_quantity"] > 0
        product["updated_at"] = datetime.utcnow()
        
        logger.info(f"Created new order: {order_id}")
        return order

# API Routes
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the FastAPI Sample Application"}

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Authentication routes
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    user = UserService.create_user(user_data)
    return UserResponse(**{k: v for k, v in user.items() if k != "hashed_password"})

@app.post("/auth/login", response_model=Token)
async def login_user(login_data: UserLogin):
    """Login user and return access token"""
    user = UserService.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    # Update last login
    user["last_login"] = datetime.utcnow()
    
    return {"access_token": access_token, "token_type": "bearer"}

# Product routes
@app.post("/products/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new product"""
    product = ProductService.create_product(product_data, current_user)
    return ProductResponse(**product)

@app.get("/products/", response_model=List[ProductResponse])
async def get_products(skip: int = 0, limit: int = 100):
    """Get all products"""
    products = ProductService.get_products(skip, limit)
    return [ProductResponse(**product) for product in products]

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Get a specific product"""
    product = ProductService.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product)

# Order routes
@app.post("/orders/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new order"""
    order = OrderService.create_order(order_data, current_user)
    return OrderResponse(**order)

@app.get("/orders/", response_model=List[OrderResponse])
async def get_user_orders(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user's orders"""
    user_orders = [order for order in orders_db.values() if order["user_id"] == current_user["id"]]
    return [OrderResponse(**order) for order in user_orders]

# Admin routes
@app.get("/admin/users", response_model=List[UserResponse])
async def get_all_users(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get all users (admin only)"""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = [{k: v for k, v in user.items() if k != "hashed_password"} for user in users_db.values()]
    return [UserResponse(**user) for user in users]

@app.get("/admin/stats", response_model=Dict[str, Any])
async def get_admin_stats(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get admin statistics"""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {
        "total_users": len(users_db),
        "total_products": len(products_db),
        "total_orders": len(orders_db),
        "active_products": len([p for p in products_db.values() if p["is_available"]]),
        "pending_orders": len([o for o in orders_db.values() if o["status"] == "pending"])
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
