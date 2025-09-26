"""
Database configuration and session management for Booking Website API
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from contextlib import contextmanager

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./booking_website.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_session():
    """Context manager for database session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    from .models import Base
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables"""
    from .models import Base
    Base.metadata.drop_all(bind=engine)

def init_db():
    """Initialize database with sample data"""
    from .models import User, Hotel, Room, UserRole, RoomType
    
    # Create tables
    create_tables()
    
    # Create sample data
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first():
            return
        
        # Create sample users
        admin_user = User(
            email="admin@booking.com",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        customer_user = User(
            email="customer@example.com",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER,
            is_active=True
        )
        
        db.add(admin_user)
        db.add(customer_user)
        db.commit()
        
        # Create sample hotel
        hotel = Hotel(
            name="Grand Palace Hotel",
            description="A luxurious 5-star hotel in the heart of the city",
            address="123 Main Street, Downtown",
            city="New York",
            country="USA",
            star_rating=5,
            amenities=["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"],
            latitude=40.7128,
            longitude=-74.0060,
            is_active=True
        )
        
        db.add(hotel)
        db.commit()
        
        # Create sample rooms
        rooms_data = [
            {
                "room_number": "101",
                "room_type": RoomType.SINGLE,
                "price_per_night": 150.0,
                "max_occupancy": 1,
                "size_sqm": 20.0,
                "amenities": ["WiFi", "TV", "Mini Bar"],
                "description": "Comfortable single room with city view"
            },
            {
                "room_number": "201",
                "room_type": RoomType.DOUBLE,
                "price_per_night": 250.0,
                "max_occupancy": 2,
                "size_sqm": 30.0,
                "amenities": ["WiFi", "TV", "Mini Bar", "Balcony"],
                "description": "Spacious double room with balcony"
            },
            {
                "room_number": "301",
                "room_type": RoomType.SUITE,
                "price_per_night": 500.0,
                "max_occupancy": 4,
                "size_sqm": 60.0,
                "amenities": ["WiFi", "TV", "Mini Bar", "Balcony", "Jacuzzi"],
                "description": "Luxurious suite with jacuzzi and city view"
            },
            {
                "room_number": "401",
                "room_type": RoomType.PRESIDENTIAL,
                "price_per_night": 1000.0,
                "max_occupancy": 6,
                "size_sqm": 100.0,
                "amenities": ["WiFi", "TV", "Mini Bar", "Balcony", "Jacuzzi", "Butler Service"],
                "description": "Presidential suite with butler service"
            }
        ]
        
        for room_data in rooms_data:
            room = Room(
                hotel_id=hotel.id,
                **room_data
            )
            db.add(room)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize database when run directly
    init_db()
    print("Database initialized successfully!")
