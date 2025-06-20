# Magazine Production Application - Backend Service

A FastAPI-based REST API service for the Online Magazine Production Application.

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **User Management**: User registration, login, password management
- **Database Integration**: Async SQLAlchemy with MySQL support
- **Security**: Password hashing, CORS protection, input validation
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Logging**: Structured logging with Loguru
- **Environment Configuration**: Flexible configuration management

## Technology Stack

- **Framework**: FastAPI 0.108.0
- **Python**: 3.12+
- **Database**: MySQL 8.4 with SQLAlchemy 2.0
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **Validation**: Pydantic v2
- **Logging**: Loguru
- **ASGI Server**: Uvicorn

## Project Structure

```
app/
├── api/
│   └── routers/
│       └── auth.py          # Authentication endpoints
├── core/
│   ├── config.py           # Application configuration
│   ├── database.py         # Database setup and connection
│   └── security.py         # JWT and password utilities
├── models/
│   └── user.py             # SQLAlchemy User model
├── schemas/
│   ├── auth.py             # Authentication Pydantic schemas
│   └── user.py             # User Pydantic schemas
├── scripts/
│   └── create_admin.py     # Admin user creation script
├── services/               # Business logic services
│   └── auth_service.py     # Authentication & authorization service
├── utils/
│   ├── helpers.py          # Utility functions
│   └── logger.py           # Logging configuration
└── main.py                 # FastAPI application entry point
```

## Quick Start

### 1. Prerequisites

- Python 3.12+
- MySQL 8.4+
- pip or poetry for dependency management

### 2. Installation

```bash
# Clone the repository
cd magazine-production-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

Key configuration variables:
- `SECRET_KEY`: JWT secret key (generate a secure random string)
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: MySQL connection details
- `DEBUG`: Set to `false` in production

### 4. Database Setup

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE magazine_production;
EXIT;

# The application will create tables automatically on first run
```

### 5. Create Admin User

```bash
# Run the admin creation script
python app/scripts/create_admin.py
```

### 6. Run the Application

```bash
# Development mode
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs (development only)
- **ReDoc**: http://localhost:8000/redoc (development only)

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | User login | No |
| GET | `/api/auth/me` | Get current user info | Yes |
| POST | `/api/auth/register` | Create new user | Yes (Admin) |
| POST | `/api/auth/change-password` | Change password | Yes |
| POST | `/api/auth/logout` | User logout | Yes |

### System

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API information | No |
| GET | `/health` | Health check | No |

## Authentication Flow

1. **Login**: POST to `/api/auth/login` with username and password
2. **Receive Token**: Get JWT access token in response
3. **Use Token**: Include token in `Authorization: Bearer <token>` header
4. **Token Expiry**: Tokens expire after 30 minutes (configurable)

### Example Login Request

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "your_password"
     }'
```

### Example Authenticated Request

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
     -H "Authorization: Bearer <your_jwt_token>"
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Style

The project follows Python PEP 8 style guidelines. Use tools like `black` and `flake8` for formatting and linting.

## Deployment

### Environment Variables for Production

```bash
DEBUG=false
SECRET_KEY=<strong-random-secret-key>
DATABASE_URL=mysql+aiomysql://user:password@host:port/database
```

### Docker Deployment (Future)

Docker configuration will be added in future updates.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Magazine Production Application system. 