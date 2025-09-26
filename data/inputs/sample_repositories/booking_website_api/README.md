# Booking Website API

A comprehensive hotel booking system built with FastAPI, featuring user management, hotel listings, room reservations, payment processing, and review systems.

## Features

### Core Functionality
- **User Management**: Registration, authentication, profile management
- **Hotel Management**: Hotel listings, search, and filtering
- **Room Management**: Room types, availability, and pricing
- **Booking System**: Reservation creation, modification, and cancellation
- **Payment Processing**: Multiple payment methods and transaction handling
- **Review System**: Hotel reviews and ratings
- **Notification System**: Email and SMS notifications
- **Admin Panel**: Administrative functions for hotel management

### Technical Features
- **RESTful API**: Well-structured REST endpoints
- **Database Integration**: SQLAlchemy ORM with PostgreSQL/SQLite
- **Authentication**: JWT-based authentication with role-based access
- **Data Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Comprehensive error handling and logging
- **Background Tasks**: Asynchronous task processing
- **CORS Support**: Cross-origin resource sharing enabled
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## API Endpoints

### Authentication & Users
- `POST /users/` - Create new user
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Hotels
- `GET /hotels/` - List all hotels
- `GET /hotels/{hotel_id}` - Get hotel details
- `POST /hotels/` - Create hotel (Admin only)
- `PUT /hotels/{hotel_id}` - Update hotel (Admin only)
- `DELETE /hotels/{hotel_id}` - Delete hotel (Admin only)

### Rooms
- `GET /hotels/{hotel_id}/rooms` - Get hotel rooms
- `GET /rooms/{room_id}` - Get room details
- `POST /rooms/` - Create room (Admin only)
- `PUT /rooms/{room_id}` - Update room (Admin only)
- `DELETE /rooms/{room_id}` - Delete room (Admin only)

### Bookings
- `POST /bookings/` - Create booking
- `GET /bookings/` - Get user bookings
- `GET /bookings/{booking_id}` - Get booking details
- `PUT /bookings/{booking_id}` - Update booking
- `DELETE /bookings/{booking_id}` - Cancel booking

### Payments
- `POST /payments/` - Process payment
- `GET /payments/` - Get payment history
- `POST /payments/{payment_id}/refund` - Refund payment

### Search
- `POST /search` - Search hotels with filters
- `GET /search/suggestions` - Get search suggestions

### Reviews
- `POST /reviews/` - Create review
- `GET /hotels/{hotel_id}/reviews` - Get hotel reviews
- `PUT /reviews/{review_id}` - Update review
- `DELETE /reviews/{review_id}` - Delete review

## Data Models

### User
- Personal information (name, email, phone)
- Role-based access (Customer, Admin, Manager, Staff)
- Account status and timestamps

### Hotel
- Basic information (name, description, address)
- Location data (city, country, coordinates)
- Star rating and amenities
- Status and timestamps

### Room
- Room details (number, type, size)
- Pricing and occupancy
- Amenities and availability
- Hotel association

### Booking
- Reservation details (dates, guests)
- Status tracking
- Special requests
- Financial information

### Payment
- Transaction details
- Payment method and status
- Booking association
- Audit trail

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables:
   ```bash
   export DATABASE_URL="sqlite:///./booking_website.db"
   export SECRET_KEY="your-secret-key"
   ```
4. Initialize the database:
   ```bash
   python database.py
   ```
5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

### Starting the Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Calls

#### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePass123"
  }'
```

#### Search Hotels
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "New York",
    "check_in_date": "2024-01-15",
    "check_out_date": "2024-01-17",
    "adults": 2,
    "children": 0
  }'
```

#### Create a Booking
```bash
curl -X POST "http://localhost:8000/bookings/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "room_id": 1,
    "check_in_date": "2024-01-15",
    "check_out_date": "2024-01-17",
    "adults": 2,
    "children": 0
  }'
```

## Architecture

### Project Structure
```
booking_website_api/
├── main.py              # FastAPI application
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── services.py          # Business logic services
├── database.py          # Database configuration
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

### Design Patterns
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic separation
- **Dependency Injection**: FastAPI's built-in DI
- **Factory Pattern**: Object creation
- **Observer Pattern**: Event handling

### Security Features
- JWT token authentication
- Password hashing with bcrypt
- Role-based access control
- Input validation and sanitization
- CORS configuration
- Rate limiting (configurable)

## Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

## Deployment

### Docker
```bash
docker build -t booking-api .
docker run -p 8000:8000 booking-api
```

### Production Considerations
- Use PostgreSQL for production
- Configure Redis for caching
- Set up proper logging
- Implement monitoring
- Use environment variables for secrets
- Enable HTTPS
- Set up backup strategies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
