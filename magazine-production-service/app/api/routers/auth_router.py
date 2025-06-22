"""
Authentication API router.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse,
    RefreshTokenRequest, RefreshTokenResponse,
    LogoutRequest, LogoutResponse,
    ChangePasswordRequest, ChangePasswordResponse,
    ErrorResponse
)
from app.schemas.user import UserResponse, UserUpdate
from app.api.auth_dependencies import get_current_active_user, get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        409: {"model": ErrorResponse, "description": "User already exists"}
    }
)
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    
    - **username**: Unique username (3-50 characters, alphanumeric + underscore)
    - **password**: Password (minimum 4 characters)
    - **email**: Valid email address (optional)
    - **role**: User role (editor|admin, default: editor)
    """
    return await AuthService.register_user(db, user_data)


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication failed"}
    }
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access/refresh tokens.
    
    - **username**: User's username
    - **password**: User's password
    """
    return await AuthService.login_user(db, login_data)


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid refresh token"}
    }
)
async def refresh_token(
    token_data: RefreshTokenRequest
):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    """
    return await AuthService.refresh_tokens(token_data.refresh_token)


@router.post(
    "/logout",
    response_model=LogoutResponse
)
async def logout(
    logout_data: LogoutRequest = LogoutRequest(),
    current_user: User = Depends(get_current_active_user)
):
    """
    Invalidate user session and tokens.
    
    Note: In this implementation, we rely on token expiration.
    In production, you might want to maintain a blacklist of tokens.
    """
    return {
        "success": True,
        "message": "Logout successful"
    }


@router.get(
    "/me",
    response_model=dict,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication required"}
    }
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve current authenticated user's profile.
    """
    return {
        "success": True,
        "data": {
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "role": current_user.role,
                "created_at": current_user.created_at.isoformat(),
                "updated_at": current_user.updated_at.isoformat()
            }
        }
    }


@router.put(
    "/me",
    response_model=dict,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        401: {"model": ErrorResponse, "description": "Authentication required"}
    }
)
async def update_current_user_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile information.
    
    - **email**: New email address (optional)
    - **username**: New username (optional)
    """
    # Convert Pydantic model to dict, excluding None values
    update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
    
    return await AuthService.update_user_profile(db, current_user.id, update_dict)


@router.post(
    "/change-password",
    response_model=ChangePasswordResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid password"},
        401: {"model": ErrorResponse, "description": "Authentication required"}
    }
)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change current user's password.
    
    - **current_password**: Current password
    - **new_password**: New password (minimum 4 characters)
    - **confirm_password**: Confirm new password (must match new_password)
    """
    return await AuthService.change_password(db, current_user.id, password_data)


# Admin endpoints
@router.get(
    "/users",
    response_model=dict,
    responses={
        403: {"model": ErrorResponse, "description": "Admin access required"}
    }
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    role: Optional[str] = Query(None, regex="^(editor|admin)$", description="Filter by role"),
    search: Optional[str] = Query(None, description="Search by username or email"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve list of all users (admin only).
    
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 10, max: 100)
    - **role**: Filter by role (editor|admin)
    - **search**: Search by username or email
    """
    skip = (page - 1) * limit
    return await AuthService.get_all_users(db, skip, limit, role, search)


@router.get(
    "/users/{user_id}",
    response_model=dict,
    responses={
        403: {"model": ErrorResponse, "description": "Admin access required"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve specific user information (admin only).
    
    - **user_id**: User ID
    """
    user = await AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": "USER_NOT_FOUND",
                "message": "User not found"
            }
        )
    
    return {
        "success": True,
        "data": {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            }
        }
    }


@router.put(
    "/users/{user_id}",
    response_model=dict,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        403: {"model": ErrorResponse, "description": "Admin access required"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user information (admin only).
    
    - **user_id**: User ID
    - **username**: New username (optional)
    - **email**: New email address (optional)  
    - **role**: New role (editor|admin, optional)
    """
    # Convert Pydantic model to dict, excluding None values
    update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
    
    return await AuthService.update_user_by_admin(db, user_id, update_dict)


@router.delete(
    "/users/{user_id}",
    response_model=dict,
    responses={
        400: {"model": ErrorResponse, "description": "Cannot delete self"},
        403: {"model": ErrorResponse, "description": "Admin access required"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete user account (admin only).
    
    - **user_id**: User ID
    
    Note: Users cannot delete their own account.
    """
    return await AuthService.delete_user(db, user_id, current_user.id) 