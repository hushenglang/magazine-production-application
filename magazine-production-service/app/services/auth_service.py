"""
Authentication service for user management and token operations.
"""

from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, ChangePasswordRequest
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_tokens, 
    verify_token
)


class AuthService:
    """Authentication service class."""
    
    @staticmethod
    async def register_user(db: AsyncSession, user_data: RegisterRequest) -> Dict[str, Any]:
        """
        Register a new user.
        """
        # Check if username already exists
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error": "VALIDATION_ERROR",
                    "message": "Username already exists",
                    "details": {
                        "field": "username",
                        "code": "DUPLICATE_VALUE"
                    }
                }
            )
        
        # Check if email already exists (if provided)
        if user_data.email:
            stmt = select(User).where(User.email == user_data.email)
            result = await db.execute(stmt)
            existing_email = result.scalar_one_or_none()
            
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "success": False,
                        "error": "VALIDATION_ERROR",
                        "message": "Email already exists",
                        "details": {
                            "field": "email",
                            "code": "DUPLICATE_VALUE"
                        }
                    }
                )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            password_hash=hashed_password,
            email=user_data.email,
            role=user_data.role or "editor"
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "role": new_user.role,
                    "created_at": new_user.created_at.isoformat()
                }
            }
        }
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password.
        """
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    async def login_user(db: AsyncSession, login_data: LoginRequest) -> Dict[str, Any]:
        """
        Login user and return tokens.
        """
        user = await AuthService.authenticate_user(db, login_data.username, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error": "AUTHENTICATION_FAILED",
                    "message": "Invalid username or password"
                }
            )
        
        tokens = create_tokens(user.id, user.username, user.role)
        
        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                },
                "tokens": tokens
            }
        }
    
    @staticmethod
    async def refresh_tokens(refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.
        """
        payload = verify_token(refresh_token, token_type="refresh")
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error": "INVALID_TOKEN",
                    "message": "Refresh token is invalid or expired"
                }
            )
        
        user_id = int(payload.get("sub"))
        username = payload.get("username")
        role = payload.get("role")
        
        tokens = create_tokens(user_id, username, role)
        
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "data": {
                "tokens": tokens
            }
        }
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        """
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        Get user by username.
        """
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_user_profile(
        db: AsyncSession, 
        user_id: int, 
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user profile.
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
        
        # Check for username uniqueness if updating username
        if "username" in update_data and update_data["username"] != user.username:
            stmt = select(User).where(User.username == update_data["username"])
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "success": False,
                        "error": "VALIDATION_ERROR",
                        "message": "Username already exists",
                        "details": {
                            "field": "username",
                            "code": "DUPLICATE_VALUE"
                        }
                    }
                )
        
        # Check for email uniqueness if updating email
        if "email" in update_data and update_data["email"] != user.email:
            stmt = select(User).where(User.email == update_data["email"])
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "success": False,
                        "error": "VALIDATION_ERROR", 
                        "message": "Email already exists",
                        "details": {
                            "field": "email",
                            "code": "DUPLICATE_VALUE"
                        }
                    }
                )
        
        # Update user fields
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        
        return {
            "success": True,
            "message": "Profile updated successfully",
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
    
    @staticmethod
    async def change_password(
        db: AsyncSession, 
        user_id: int, 
        password_data: ChangePasswordRequest
    ) -> Dict[str, Any]:
        """
        Change user password.
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
        
        # Verify current password
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error": "INVALID_PASSWORD",
                    "message": "Current password is incorrect"
                }
            )
        
        # Update password
        user.password_hash = get_password_hash(password_data.new_password)
        await db.commit()
        
        return {
            "success": True,
            "message": "Password changed successfully"
        }
    
    @staticmethod
    async def get_all_users(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10,
        role: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all users with pagination and filtering (admin only).
        """
        stmt = select(User)
        
        # Apply role filter
        if role:
            stmt = stmt.where(User.role == role)
        
        # Apply search filter
        if search:
            stmt = stmt.where(
                (User.username.ilike(f"%{search}%")) | 
                (User.email.ilike(f"%{search}%"))
            )
        
        # Get total count
        count_stmt = select(User.id)
        if role:
            count_stmt = count_stmt.where(User.role == role)
        if search:
            count_stmt = count_stmt.where(
                (User.username.ilike(f"%{search}%")) | 
                (User.email.ilike(f"%{search}%"))
            )
        
        count_result = await db.execute(count_stmt)
        total_items = len(count_result.all())
        
        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        users = result.scalars().all()
        
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            })
        
        total_pages = (total_items + limit - 1) // limit
        current_page = (skip // limit) + 1
        
        return {
            "success": True,
            "data": {
                "users": users_data,
                "pagination": {
                    "current_page": current_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "items_per_page": limit
                }
            }
        }
    
    @staticmethod
    async def update_user_by_admin(
        db: AsyncSession, 
        user_id: int, 
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user by admin.
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
        
        # Apply similar validation as in update_user_profile
        # Check for username uniqueness if updating username
        if "username" in update_data and update_data["username"] != user.username:
            stmt = select(User).where(User.username == update_data["username"])
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "success": False,
                        "error": "VALIDATION_ERROR",
                        "message": "Username already exists",
                        "details": {
                            "field": "username",
                            "code": "DUPLICATE_VALUE"
                        }
                    }
                )
        
        # Update user fields
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        
        return {
            "success": True,
            "message": "User updated successfully",
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
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int, current_user_id: int) -> Dict[str, Any]:
        """
        Delete user (admin only).
        """
        if user_id == current_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error": "CANNOT_DELETE_SELF",
                    "message": "Cannot delete your own account"
                }
            )
        
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
        
        # Hard delete the user
        await db.delete(user)
        await db.commit()
        
        return {
            "success": True,
            "message": "User deleted successfully"
        } 