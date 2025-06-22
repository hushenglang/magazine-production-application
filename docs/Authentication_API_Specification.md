# Authentication Service API Specification
# Online Magazine Production Application

## Document Information
- **Version**: 1.0
- **Date**: 2025-01-15
- **Author**: hushenglang
- **Status**: Draft
- **Related Document**: Technical_Architecture_Overview.md

## 1. Overview

The Authentication Service provides secure user authentication and authorization capabilities for the Online Magazine Production Application. It implements JWT-based authentication with role-based access control (RBAC).

### 1.1 Base URL
```
http://localhost:8000/api/v1/auth
```

### 1.2 Authentication Method
- **Type**: JWT (JSON Web Token)
- **Header**: `Authorization: Bearer <token>`
- **Token Expiry**: 24 hours (configurable)
- **Refresh Token Expiry**: 7 days (configurable)

### 1.3 User Roles
- **editor**: Standard user with content creation/editing permissions
- **admin**: Administrative user with full system access

## 2. Authentication Endpoints

### 2.1 User Registration

#### POST /register
Register a new user account.

**Request Body:**
```json
{
  "username": "string (required, 3-50 characters, alphanumeric + underscore)",
  "password": "string (required, min 8 characters)",
  "email": "string (required, valid email format)",
  "role": "string (optional, enum: 'editor'|'admin', default: 'editor')"
}
```

**Response - Success (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "editor",
      "created_at": "2025-01-15T10:30:00Z"
    }
  }
}
```

**Response - Error (400 Bad Request):**
```json
{
  "success": false,
  "error": "VALIDATION_ERROR",
  "message": "Username already exists",
  "details": {
    "field": "username",
    "code": "DUPLICATE_VALUE"
  }
}
```

### 2.2 User Login

#### POST /login
Authenticate user and return access/refresh tokens.

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Response - Success (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "editor"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "expires_in": 86400
    }
  }
}
```

**Response - Error (401 Unauthorized):**
```json
{
  "success": false,
  "error": "AUTHENTICATION_FAILED",
  "message": "Invalid username or password"
}
```

### 2.3 Token Refresh

#### POST /refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "string (required)"
}
```

**Response - Success (200 OK):**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "expires_in": 86400
    }
  }
}
```

**Response - Error (401 Unauthorized):**
```json
{
  "success": false,
  "error": "INVALID_TOKEN",
  "message": "Refresh token is invalid or expired"
}
```

### 2.4 User Logout

#### POST /logout
Invalidate user session and tokens.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh_token": "string (optional)"
}
```

**Response - Success (200 OK):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

## 3. User Profile Endpoints

### 3.1 Get Current User

#### GET /me
Retrieve current authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response - Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "editor",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  }
}
```

### 3.2 Update User Profile

#### PUT /me
Update current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "email": "string (optional, valid email format)",
  "username": "string (optional, 3-50 characters)"
}
```

**Response - Success (200 OK):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john.doe@example.com",
      "role": "editor",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T12:45:00Z"
    }
  }
}
```

### 3.3 Change Password

#### POST /change-password
Change current user's password.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "string (required)",
  "new_password": "string (required, min 8 characters)",
  "confirm_password": "string (required, must match new_password)"
}
```

**Response - Success (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

**Response - Error (400 Bad Request):**
```json
{
  "success": false,
  "error": "INVALID_PASSWORD",
  "message": "Current password is incorrect"
}
```

## 4. Admin Endpoints

*Note: These endpoints require admin role authorization.*

### 4.1 List Users

#### GET /users
Retrieve list of all users (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: integer (optional, default: 1)
- `limit`: integer (optional, default: 10, max: 100)
- `role`: string (optional, filter by role)
- `search`: string (optional, search by username or email)

**Response - Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "role": "editor",
        "created_at": "2025-01-15T10:30:00Z",
        "updated_at": "2025-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_items": 50,
      "items_per_page": 10
    }
  }
}
```

### 4.2 Get User by ID

#### GET /users/{user_id}
Retrieve specific user information (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `user_id`: integer (required)

**Response - Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "editor",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  }
}
```

### 4.3 Update User

#### PUT /users/{user_id}
Update user information (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `user_id`: integer (required)

**Request Body:**
```json
{
  "username": "string (optional)",
  "email": "string (optional)",
  "role": "string (optional, enum: 'editor'|'admin')",
  "is_active": "boolean (optional)"
}
```

**Response - Success (200 OK):**
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "admin",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T12:45:00Z"
    }
  }
}
```

### 4.4 Delete User

#### DELETE /users/{user_id}
Delete user account (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `user_id`: integer (required)

**Response - Success (200 OK):**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

**Response - Error (400 Bad Request):**
```json
{
  "success": false,
  "error": "CANNOT_DELETE_SELF",
  "message": "Cannot delete your own account"
}
```

## 5. Error Handling

### 5.1 Common HTTP Status Codes
- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Access denied (insufficient permissions)
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., duplicate username)
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server error

### 5.2 Error Response Format
```json
{
  "success": false,
  "error": "ERROR_CODE",
  "message": "Human readable error message",
  "details": {
    "field": "field_name",
    "code": "VALIDATION_CODE"
  }
}
```

### 5.3 Common Error Codes
- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_FAILED`: Invalid credentials
- `INVALID_TOKEN`: JWT token is invalid or expired
- `ACCESS_DENIED`: Insufficient permissions
- `USER_NOT_FOUND`: User does not exist
- `DUPLICATE_VALUE`: Unique constraint violation
- `PASSWORD_TOO_WEAK`: Password doesn't meet requirements

## 6. Security Considerations

### 6.1 Input Validation
- All inputs are validated using Pydantic schemas
- SQL injection prevention through ORM
- XSS prevention through input sanitization

### 6.2 Password Requirements
- Minimum 4 characters


## 7. Implementation Notes

### 7.1 Dependencies
- FastAPI for API framework
- JWT for token management
- bcrypt for password hashing
- SQLAlchemy for database operations
- Pydantic for request/response validation

### 7.2 Database Considerations
- User passwords are hashed using bcrypt
- Refresh tokens are stored with expiration timestamps

### 7.3 Testing
- Unit tests for all authentication logic
- Integration tests for API endpoints
- Security testing for common vulnerabilities 