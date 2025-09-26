# FastAPI Sample Application

This is a comprehensive FastAPI web application designed for testing Workflow 1: Code to Design. It demonstrates various architectural patterns and components that the workflow can analyze.

## Features

- **RESTful API**: Complete CRUD operations for users, products, and orders
- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **Database Models**: SQLAlchemy ORM models with relationships
- **Service Layer**: Business logic separated into service classes
- **Data Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Comprehensive error handling and logging
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Architecture

The application follows a clean architecture pattern:

- **Models**: SQLAlchemy ORM models for data persistence
- **Schemas**: Pydantic models for data validation and serialization
- **Services**: Business logic and data access operations
- **API Routes**: FastAPI route handlers
- **Database**: SQLAlchemy session management

## Components

### Models (`models.py`)
- `User`: User authentication and profile management
- `Product`: Product catalog management
- `Order`: Order processing and tracking

### Services (`services.py`)
- `UserService`: User registration, authentication, and management
- `ProductService`: Product CRUD operations and inventory management
- `OrderService`: Order processing and status management
- `AnalyticsService`: Business intelligence and reporting

### Schemas (`schemas.py`)
- Request/response validation models
- Data serialization schemas
- Error handling schemas

### API Endpoints
- **Authentication**: `/auth/register`, `/auth/login`
- **Users**: `/users/`, `/users/{id}`
- **Products**: `/products/`, `/products/{id}`
- **Orders**: `/orders/`, `/orders/{id}`
- **Admin**: `/admin/users`, `/admin/stats`
- **Health**: `/health`

## Design Patterns Demonstrated

- **MVC Pattern**: Clear separation of models, views (API routes), and controllers (services)
- **Service Layer Pattern**: Business logic separated into service classes
- **Repository Pattern**: Data access abstracted through service classes
- **Dependency Injection**: FastAPI's dependency system for database sessions
- **Factory Pattern**: Database session factory
- **Strategy Pattern**: Different authentication strategies
- **Observer Pattern**: Logging and monitoring
- **Builder Pattern**: Pydantic model construction

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DATABASE_URL="sqlite:///./sample_app.db"
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

This application is designed to be analyzed by Workflow 1 to demonstrate:
- Code structure analysis
- Architecture pattern detection
- Dependency analysis
- Code quality metrics
- Design pattern recognition
- API documentation generation

## File Structure

```
fastapi_sample_app/
├── main.py              # Main FastAPI application
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic validation schemas
├── services.py          # Business logic services
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## API Usage Examples

### Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "TestPass123",
       "full_name": "Test User"
     }'
```

### Login and get token
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "TestPass123"
     }'
```

### Create a product (requires authentication)
```bash
curl -X POST "http://localhost:8000/products/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Sample Product",
       "description": "A sample product for testing",
       "price": 29.99,
       "category": "Electronics",
       "stock_quantity": 100
     }'
```

## Database Schema

The application uses the following main entities:

- **Users**: Authentication and user management
- **Products**: Product catalog with inventory tracking
- **Orders**: Order processing with status tracking

Relationships:
- Users can have multiple orders
- Products can be in multiple orders
- Orders belong to one user and one product
