"""
User schemas for request/response validation.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: Optional[EmailStr] = Field(None)
    role: str = Field(default="editor", pattern="^(editor|admin)$")


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=4, max_length=128)


class UserUpdate(BaseModel):
    """User update schema."""
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: Optional[EmailStr] = Field(None)
    role: Optional[str] = Field(None, pattern="^(editor|admin)$")


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    username: str
    email: Optional[str]
    role: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserInDB(UserBase):
    """User schema for database operations."""
    id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 