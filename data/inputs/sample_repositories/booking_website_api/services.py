"""
Business logic services for Booking Website API
Contains service classes for handling business operations
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import logging
from enum import Enum

from .models import User, Hotel, Room, Booking, Payment, Review, UserRole, BookingStatus, PaymentStatus

logger = logging.getLogger(__name__)

class UserService:
    """Service for user-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        logger.info(f"Creating user: {user_data.get('email')}")
        
        user = User(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data.get('phone'),
            date_of_birth=user_data.get('date_of_birth'),
            role=user_data.get('role', UserRole.CUSTOMER)
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

class HotelService:
    """Service for hotel-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_hotel(self, hotel_data: Dict[str, Any]) -> Hotel:
        """Create a new hotel"""
        logger.info(f"Creating hotel: {hotel_data.get('name')}")
        
        hotel = Hotel(
            name=hotel_data['name'],
            description=hotel_data.get('description'),
            address=hotel_data['address'],
            city=hotel_data['city'],
            country=hotel_data['country'],
            star_rating=hotel_data['star_rating'],
            amenities=hotel_data.get('amenities', []),
            latitude=hotel_data.get('latitude'),
            longitude=hotel_data.get('longitude')
        )
        
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        
        return hotel
    
    def get_hotel_by_id(self, hotel_id: int) -> Optional[Hotel]:
        """Get hotel by ID"""
        return self.db.query(Hotel).filter(Hotel.id == hotel_id).first()
    
    def get_hotels_by_city(self, city: str) -> List[Hotel]:
        """Get hotels by city"""
        return self.db.query(Hotel).filter(
            and_(Hotel.city.ilike(f"%{city}%"), Hotel.is_active == True)
        ).all()
    
    def search_hotels(self, filters: Dict[str, Any]) -> List[Hotel]:
        """Search hotels with filters"""
        query = self.db.query(Hotel).filter(Hotel.is_active == True)
        
        if filters.get('city'):
            query = query.filter(Hotel.city.ilike(f"%{filters['city']}%"))
        
        if filters.get('star_rating'):
            query = query.filter(Hotel.star_rating >= filters['star_rating'])
        
        if filters.get('min_price') and filters.get('max_price'):
            # Join with rooms to filter by price
            query = query.join(Room).filter(
                and_(
                    Room.price_per_night >= filters['min_price'],
                    Room.price_per_night <= filters['max_price']
                )
            )
        
        return query.distinct().all()
    
    def update_hotel(self, hotel_id: int, update_data: Dict[str, Any]) -> Optional[Hotel]:
        """Update hotel information"""
        hotel = self.get_hotel_by_id(hotel_id)
        if not hotel:
            return None
        
        for key, value in update_data.items():
            if hasattr(hotel, key) and value is not None:
                setattr(hotel, key, value)
        
        hotel.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(hotel)
        
        return hotel

class RoomService:
    """Service for room-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_room(self, room_data: Dict[str, Any]) -> Room:
        """Create a new room"""
        logger.info(f"Creating room: {room_data.get('room_number')}")
        
        room = Room(
            hotel_id=room_data['hotel_id'],
            room_number=room_data['room_number'],
            room_type=room_data['room_type'],
            price_per_night=room_data['price_per_night'],
            max_occupancy=room_data['max_occupancy'],
            size_sqm=room_data.get('size_sqm'),
            amenities=room_data.get('amenities', []),
            description=room_data.get('description')
        )
        
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        
        return room
    
    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        """Get room by ID"""
        return self.db.query(Room).filter(Room.id == room_id).first()
    
    def get_rooms_by_hotel(self, hotel_id: int, available_only: bool = True) -> List[Room]:
        """Get rooms for a specific hotel"""
        query = self.db.query(Room).filter(Room.hotel_id == hotel_id)
        
        if available_only:
            query = query.filter(Room.is_available == True)
        
        return query.all()
    
    def check_room_availability(self, room_id: int, check_in: date, check_out: date) -> bool:
        """Check if room is available for given dates"""
        conflicting_bookings = self.db.query(Booking).filter(
            and_(
                Booking.room_id == room_id,
                Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN]),
                or_(
                    and_(Booking.check_in_date <= check_in, Booking.check_out_date > check_in),
                    and_(Booking.check_in_date < check_out, Booking.check_out_date >= check_out),
                    and_(Booking.check_in_date >= check_in, Booking.check_out_date <= check_out)
                )
            )
        ).first()
        
        return conflicting_bookings is None
    
    def get_available_rooms(self, hotel_id: int, check_in: date, check_out: date, 
                          room_type: Optional[str] = None) -> List[Room]:
        """Get available rooms for given criteria"""
        query = self.db.query(Room).filter(
            and_(Room.hotel_id == hotel_id, Room.is_available == True)
        )
        
        if room_type:
            query = query.filter(Room.room_type == room_type)
        
        available_rooms = []
        for room in query.all():
            if self.check_room_availability(room.id, check_in, check_out):
                available_rooms.append(room)
        
        return available_rooms

class BookingService:
    """Service for booking-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.room_service = RoomService(db)
    
    def create_booking(self, booking_data: Dict[str, Any]) -> Booking:
        """Create a new booking"""
        logger.info(f"Creating booking for user {booking_data.get('user_id')}")
        
        # Check room availability
        if not self.room_service.check_room_availability(
            booking_data['room_id'],
            booking_data['check_in_date'],
            booking_data['check_out_date']
        ):
            raise ValueError("Room is not available for selected dates")
        
        # Calculate total amount
        room = self.room_service.get_room_by_id(booking_data['room_id'])
        nights = (booking_data['check_out_date'] - booking_data['check_in_date']).days
        total_amount = room.price_per_night * nights
        
        booking = Booking(
            user_id=booking_data['user_id'],
            room_id=booking_data['room_id'],
            check_in_date=booking_data['check_in_date'],
            check_out_date=booking_data['check_out_date'],
            adults=booking_data['adults'],
            children=booking_data.get('children', 0),
            special_requests=booking_data.get('special_requests'),
            total_amount=total_amount
        )
        
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        
        return booking
    
    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        """Get booking by ID"""
        return self.db.query(Booking).filter(Booking.id == booking_id).first()
    
    def get_user_bookings(self, user_id: int, status: Optional[BookingStatus] = None) -> List[Booking]:
        """Get bookings for a specific user"""
        query = self.db.query(Booking).filter(Booking.user_id == user_id)
        
        if status:
            query = query.filter(Booking.status == status)
        
        return query.order_by(Booking.created_at.desc()).all()
    
    def update_booking_status(self, booking_id: int, status: BookingStatus) -> bool:
        """Update booking status"""
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return False
        
        booking.status = status
        booking.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def cancel_booking(self, booking_id: int) -> bool:
        """Cancel a booking"""
        return self.update_booking_status(booking_id, BookingStatus.CANCELLED)
    
    def get_booking_revenue(self, start_date: date, end_date: date) -> float:
        """Calculate total revenue for a date range"""
        result = self.db.query(func.sum(Booking.total_amount)).filter(
            and_(
                Booking.status == BookingStatus.CONFIRMED,
                Booking.check_in_date >= start_date,
                Booking.check_in_date <= end_date
            )
        ).scalar()
        
        return result or 0.0

class PaymentService:
    """Service for payment-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_payment(self, payment_data: Dict[str, Any]) -> Payment:
        """Create a new payment"""
        logger.info(f"Processing payment for booking {payment_data.get('booking_id')}")
        
        payment = Payment(
            booking_id=payment_data['booking_id'],
            user_id=payment_data['user_id'],
            amount=payment_data['amount'],
            payment_method=payment_data['payment_method'],
            transaction_id=payment_data.get('transaction_id')
        )
        
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        
        return payment
    
    def process_payment(self, payment_id: int, success: bool) -> bool:
        """Process payment (simulate payment gateway)"""
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            return False
        
        payment.status = PaymentStatus.COMPLETED if success else PaymentStatus.FAILED
        payment.updated_at = datetime.utcnow()
        self.db.commit()
        
        # Update booking status if payment successful
        if success:
            booking_service = BookingService(self.db)
            booking_service.update_booking_status(payment.booking_id, BookingStatus.CONFIRMED)
        
        return True
    
    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        """Get payment by ID"""
        return self.db.query(Payment).filter(Payment.id == payment_id).first()
    
    def get_user_payments(self, user_id: int) -> List[Payment]:
        """Get payments for a specific user"""
        return self.db.query(Payment).filter(
            Payment.user_id == user_id
        ).order_by(Payment.created_at.desc()).all()
    
    def refund_payment(self, payment_id: int) -> bool:
        """Refund a payment"""
        payment = self.get_payment_by_id(payment_id)
        if not payment or payment.status != PaymentStatus.COMPLETED:
            return False
        
        payment.status = PaymentStatus.REFUNDED
        payment.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

class ReviewService:
    """Service for review-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_review(self, review_data: Dict[str, Any]) -> Review:
        """Create a new review"""
        logger.info(f"Creating review for hotel {review_data.get('hotel_id')}")
        
        review = Review(
            user_id=review_data['user_id'],
            hotel_id=review_data['hotel_id'],
            booking_id=review_data.get('booking_id'),
            rating=review_data['rating'],
            title=review_data.get('title'),
            comment=review_data.get('comment')
        )
        
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        
        return review
    
    def get_hotel_reviews(self, hotel_id: int) -> List[Review]:
        """Get reviews for a specific hotel"""
        return self.db.query(Review).filter(
            Review.hotel_id == hotel_id
        ).order_by(Review.created_at.desc()).all()
    
    def get_hotel_average_rating(self, hotel_id: int) -> float:
        """Calculate average rating for a hotel"""
        result = self.db.query(func.avg(Review.rating)).filter(
            Review.hotel_id == hotel_id
        ).scalar()
        
        return round(result or 0.0, 2)

class NotificationService:
    """Service for notification-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def send_notification(self, user_id: int, title: str, message: str, 
                         notification_type: str = "email") -> None:
        """Send notification to user"""
        logger.info(f"Sending {notification_type} notification to user {user_id}")
        
        # In a real implementation, this would integrate with email/SMS services
        # For now, we'll just log the notification
        
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get notifications for a user"""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        return query.order_by(Notification.created_at.desc()).all()
