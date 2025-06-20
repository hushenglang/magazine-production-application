from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.schemas.auth import TokenData
from app.schemas.user import User as UserSchema

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> UserSchema:
    """Get current user from JWT token."""
    token = credentials.credentials
    
    # Verify token
    payload = verify_token(token)
    
    # Extract user data from token
    username: Optional[str] = payload.get("sub")
    user_id: Optional[int] = payload.get("user_id")
    
    if username is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return UserSchema.model_validate(user)


async def get_current_active_user(
    current_user: UserSchema = Depends(get_current_user)
) -> UserSchema:
    """Get current active user (placeholder for future user activation logic)."""
    return current_user


async def get_admin_user(
    current_user: UserSchema = Depends(get_current_user)
) -> UserSchema:
    """Require admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user 