# Coding Rules - Magazine Production Backend Service

## Document Information
- **Version**: 1.0
- **Date**: 2025-01-15
- **Purpose**: Development guidelines and coding standards for the Magazine Production API
- **Framework**: FastAPI with Python 3.12

## 1. Project Structure Rules

### 1.1 Directory Organization
```
app/
├── api/                    # API layer
│   └── routers/           # FastAPI route handlers
├── core/                  # Core application configuration
├── models/                # SQLAlchemy database models  
├── schemas/               # Pydantic models for request/response
├── services/              # Business logic layer
├── utils/                 # Utility functions and helpers
└── main.py               # Application entry point
```

### 1.2 File Naming Conventions
- **Files**: Use snake_case (e.g., `auth_service.py`)
- **Classes**: Use PascalCase (e.g., `UserService`, `ContentModel`)
- **Functions/Variables**: Use snake_case (e.g., `get_current_user`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE`)

## 2. Code Organization Rules

### 2.1 Import Organization
```python
# Standard library imports
from datetime import datetime
from typing import Optional, List

# Third-party library imports  
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# Local application imports
from app.core.config import settings
from app.models.user import User
```

### 2.2 Router Structure
- Each router should handle one main resource (users, content, magazines)
- Use consistent HTTP status codes
- Include proper error handling
- Add comprehensive documentation with docstrings

### 2.3 Service Layer Rules
- Business logic must be in service classes, not in routers
- Services should be dependency-injectable
- Use async/await for database operations
- Handle exceptions at service level

## 3. Package Management Rules

### 3.1 Package Manager
- Use **UV** as the primary package manager for faster dependency resolution
- UV provides better performance and more reliable dependency resolution than pip
- Install UV globally: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 3.2 Virtual Environment Management
```bash
# Create virtual environment with UV
uv venv --python 3.12

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### 3.3 Dependency Management
- Use `pyproject.toml` for project configuration and dependencies
- Separate development and production dependencies
- Pin exact versions for production stability

```toml
# pyproject.toml
[project]
name = "magazine-production-service"
version = "1.0.0"
dependencies = [
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    "sqlalchemy[asyncio]==2.0.23",
    "aiomysql==0.2.0",
    "pydantic[email]==2.5.0",
    "python-jose[cryptography]==3.3.0",
    "passlib[bcrypt]==1.7.4",
    "python-multipart==0.0.6",
    "structlog==23.2.0"
]

[project.optional-dependencies]
dev = [
    "pytest==7.4.3",
    "pytest-asyncio==0.21.1",
    "httpx==0.25.2",
    "black==23.11.0",
    "ruff==0.1.6",
    "mypy==1.7.1"
]
```

### 3.4 Installation Commands
```bash
# Install production dependencies
uv pip install -e .

# Install with development dependencies
uv pip install -e ".[dev]"

# Install from requirements file (legacy support)
uv pip install -r requirements.txt
```

### 3.5 Dependency Updates
- Review and test dependency updates regularly
- Use `uv pip list --outdated` to check for updates
- Update dependencies in controlled batches
- Always test thoroughly after updates

```bash
# Check outdated packages
uv pip list --outdated

# Update specific package
uv pip install --upgrade package-name

# Generate updated requirements
uv pip freeze > requirements.txt
```

### 3.6 Security Considerations
- Regularly audit dependencies for security vulnerabilities
- Use `pip-audit` or similar tools for security scanning
- Avoid packages with known vulnerabilities
- Keep dependencies up-to-date with security patches

```bash
# Security audit
pip-audit

# Check for known vulnerabilities
uv pip install pip-audit
pip-audit --requirement requirements.txt
```

### 3.7 Lock Files and Reproducible Builds
- Generate and commit lock files for reproducible builds
- Use `uv pip freeze` to capture exact versions
- Document the Python version requirement clearly
- Ensure consistent environments across development and production

### 3.8 Package Development Guidelines
- Follow semantic versioning for internal packages
- Include proper package metadata in `pyproject.toml`
- Add comprehensive package documentation
- Implement proper package testing before release

## 4. Database Rules

### 4.1 Model Definitions
- Use SQLAlchemy ORM models in `models/` directory
- Include proper relationships and constraints
- Add created_at/updated_at timestamps
- Use appropriate field types and lengths

### 4.2 Database Operations
- Use async database operations with aiomysql
- Implement proper connection pooling
- Use database transactions for multi-table operations
- Add proper indexes for query optimization

### 4.3 Migration Rules
- Use Alembic for database migrations
- Never modify existing migrations
- Include descriptive migration messages
- Test migrations on staging before production

## 5. Authentication & Security Rules

### 5.1 JWT Token Management
- Use JWT for stateless authentication
- Implement proper token expiration (30 minutes default)
- Store sensitive data in environment variables
- Use bcrypt for password hashing

### 5.2 Route Protection
- Implement role-based access control (editor, admin)
- Use dependency injection for authentication
- Validate user permissions for each protected endpoint
- Return appropriate HTTP status codes for auth failures

### 5.3 Input Validation
- Use Pydantic schemas for request validation
- Sanitize user inputs before processing
- Validate file uploads (type, size, content)
- Implement rate limiting for API endpoints

## 6. API Design Rules

### 6.1 RESTful Endpoints
```
GET    /api/users          # List users
POST   /api/users          # Create user
GET    /api/users/{id}     # Get user by ID
PUT    /api/users/{id}     # Update user
DELETE /api/users/{id}     # Delete user
```

### 6.2 Response Format
```python
# Success response
{
    "success": true,
    "data": {...},
    "message": "Operation completed successfully"
}

# Error response
{
    "success": false,
    "error": "Error description",
    "details": {...}
}
```

### 6.3 HTTP Status Codes
- 200: OK (successful GET, PUT)
- 201: Created (successful POST)
- 204: No Content (successful DELETE)
- 400: Bad Request (validation errors)
- 401: Unauthorized (authentication required)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error (server errors)

## 7. Error Handling Rules

### 7.1 Exception Handling
- Use custom exception classes for business logic errors
- Catch and handle database exceptions appropriately
- Log all errors with appropriate context
- Never expose internal error details to clients

### 7.2 Logging Standards
```python
import structlog

logger = structlog.get_logger(__name__)

# Log with context
logger.info("User created", user_id=user.id, username=user.username)
logger.error("Database error", error=str(e), query=query)
```

## 8. Performance Rules

### 8.1 Database Optimization
- Use SELECT queries with specific fields, avoid SELECT *
- Implement proper pagination for list endpoints
- Use database indexes for frequently queried fields
- Batch database operations when possible

### 8.2 Caching Strategy
- Cache frequently accessed data (user sessions, configurations)  
- Use appropriate cache TTL values
- Implement cache invalidation strategies
- Consider Redis for distributed caching

### 8.3 File Handling
- Implement async file operations
- Validate file types and sizes before processing
- Use background tasks for heavy image processing
- Store files efficiently (local storage or object storage)

## 9. Testing Rules

### 9.1 Test Coverage
- Maintain minimum 80% test coverage
- Test all business logic in services
- Test API endpoints with various scenarios
- Include integration tests for database operations

### 9.2 Test Structure
```python
# test_user_service.py
import pytest
from app.services.user_service import UserService

class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user_success(self):
        # Test implementation
        pass
        
    @pytest.mark.asyncio  
    async def test_create_user_duplicate_email(self):
        # Test implementation
        pass
```

## 10. Environment & Configuration Rules

### 10.1 Environment Variables
- Store all sensitive data in environment variables
- Use .env files for local development
- Document all required environment variables
- Provide sensible defaults where appropriate

### 10.2 Configuration Management
- Use Pydantic Settings for configuration
- Validate configuration on application startup
- Support different configurations for dev/staging/prod
- Never commit secrets to version control

## 11. Documentation Rules

### 11.1 Code Documentation
- Add docstrings to all functions and classes
- Use type hints for all function parameters and return values
- Document complex business logic with inline comments
- Keep documentation up-to-date with code changes

### 11.2 API Documentation
- Use FastAPI automatic documentation features
- Provide examples for request/response schemas
- Document authentication requirements
- Include error response examples

## 12. Deployment Rules

### 12.1 Container Requirements
- Use Python 3.12 base image
- Install dependencies using UV package manager
- Set appropriate environment variables
- Include health check endpoints

### 12.2 Production Considerations
- Disable debug mode in production
- Use proper logging levels
- Implement monitoring and health checks
- Set up automated backups for database

## 13. Code Review Guidelines

### 13.1 Review Checklist
- [ ] Code follows naming conventions
- [ ] Proper error handling implemented
- [ ] Security considerations addressed
- [ ] Tests included for new functionality
- [ ] Documentation updated
- [ ] Database migrations included if needed
- [ ] Performance implications considered

### 13.2 Quality Standards
- No hardcoded values (use configuration)
- Proper separation of concerns
- DRY principle followed
- SOLID principles applied
- Code is readable and maintainable 