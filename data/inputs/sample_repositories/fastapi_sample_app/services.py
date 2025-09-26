"""
Service layer for FastAPI Sample Application
Business logic and data access operations
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
import logging

from .models import User, Product, Order, UserRole, OrderStatus
from .schemas import UserCreate, ProductCreate, OrderCreate

logger = logging.getLogger(__name__)

class UserService:
    """Service class for user operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate, hashed_password: str) -> User:
        """Create a new user"""
        # Check if username or email already exists
        existing_user = self.db.query(User).filter(
            or_(User.username == user_data.username, User.email == user_data.email)
        ).first()
        
        if existing_user:
            if existing_user.username == user_data.username:
                raise ValueError("Username already registered")
            else:
                raise ValueError("Email already registered")
        
        # Create new user
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            hashed_password=hashed_password
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        logger.info(f"Created new user: {user_data.username}")
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def update_user_last_login(self, user: User):
        """Update user's last login timestamp"""
        user.last_login = datetime.utcnow()
        self.db.commit()
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user"""
        user = self.get_user_by_id(user_id)
        if user:
            user.is_active = False
            self.db.commit()
            return True
        return False

class ProductService:
    """Service class for product operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_product(self, product_data: ProductCreate, created_by: int) -> Product:
        """Create a new product"""
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category,
            stock_quantity=product_data.stock_quantity,
            is_available=product_data.stock_quantity > 0,
            created_by=created_by
        )
        
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        logger.info(f"Created new product: {product_data.name}")
        return product
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a specific product"""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_products(self, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[Product]:
        """Get products with optional filtering"""
        query = self.db.query(Product)
        
        if category:
            query = query.filter(Product.category == category)
        
        return query.offset(skip).limit(limit).all()
    
    def update_product_stock(self, product_id: int, quantity_change: int) -> bool:
        """Update product stock quantity"""
        product = self.get_product(product_id)
        if product:
            product.stock_quantity += quantity_change
            product.is_available = product.stock_quantity > 0
            product.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def search_products(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name or description"""
        return self.db.query(Product).filter(
            or_(
                Product.name.contains(search_term),
                Product.description.contains(search_term)
            )
        ).offset(skip).limit(limit).all()

class OrderService:
    """Service class for order operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, order_data: OrderCreate, user_id: int) -> Order:
        """Create a new order"""
        # Get product and check availability
        product = self.db.query(Product).filter(Product.id == order_data.product_id).first()
        if not product:
            raise ValueError("Product not found")
        
        if not product.is_available:
            raise ValueError("Product is not available")
        
        if product.stock_quantity < order_data.quantity:
            raise ValueError("Insufficient stock")
        
        # Calculate total price
        total_price = product.price * order_data.quantity
        
        # Create order
        order = Order(
            user_id=user_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            total_price=total_price,
            status=OrderStatus.PENDING
        )
        
        self.db.add(order)
        
        # Update product stock
        product.stock_quantity -= order_data.quantity
        product.is_available = product.stock_quantity > 0
        product.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(order)
        
        logger.info(f"Created new order: {order.id}")
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get a specific order"""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders for a specific user"""
        return self.db.query(Order).filter(
            Order.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination"""
        return self.db.query(Order).offset(skip).limit(limit).all()
    
    def update_order_status(self, order_id: int, status: OrderStatus) -> bool:
        """Update order status"""
        order = self.get_order(order_id)
        if order:
            order.status = status
            self.db.commit()
            return True
        return False
    
    def get_orders_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by status"""
        return self.db.query(Order).filter(
            Order.status == status
        ).offset(skip).limit(limit).all()

class AnalyticsService:
    """Service class for analytics and reporting"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        total_users = self.db.query(User).count()
        total_products = self.db.query(Product).count()
        total_orders = self.db.query(Order).count()
        active_products = self.db.query(Product).filter(Product.is_available == True).count()
        pending_orders = self.db.query(Order).filter(Order.status == OrderStatus.PENDING).count()
        
        return {
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "active_products": active_products,
            "pending_orders": pending_orders
        }
    
    def get_sales_by_category(self) -> Dict[str, float]:
        """Get sales totals by product category"""
        from sqlalchemy import func
        
        results = self.db.query(
            Product.category,
            func.sum(Order.total_price).label('total_sales')
        ).join(Order).group_by(Product.category).all()
        
        return {category: float(total_sales) for category, total_sales in results}
    
    def get_user_activity(self, days: int = 30) -> Dict[str, int]:
        """Get user activity statistics"""
        since_date = datetime.utcnow() - timedelta(days=days)
        
        new_users = self.db.query(User).filter(User.created_at >= since_date).count()
        active_users = self.db.query(User).filter(User.last_login >= since_date).count()
        
        return {
            "new_users": new_users,
            "active_users": active_users
        }
