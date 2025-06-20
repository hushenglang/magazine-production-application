from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, PasswordChangeRequest
from app.schemas.user import UserCreate, User as UserSchema, UserInDB
from app.services.auth_service import get_current_user, get_admin_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token."""
    
    # Get user by username
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalar_one_or_none()
    
    # Verify user exists and password is correct
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }
    )


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
    current_user: UserSchema = Depends(get_current_user)
):
    """Get current user information."""
    return current_user


@router.post("/register", response_model=UserSchema)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: UserSchema = Depends(get_admin_user)  # Only admins can create users
):
    """Register a new user (Admin only)."""
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user instance
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role
    )
    
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return UserSchema.model_validate(db_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: UserSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change current user's password."""
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == current_user.id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current password
    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()
    
    return {"message": "Password updated successfully"}


@router.post("/logout")
async def logout(
    current_user: UserSchema = Depends(get_current_user)
):
    """Logout user (placeholder - JWT tokens are stateless)."""
    return {"message": "Successfully logged out"} 