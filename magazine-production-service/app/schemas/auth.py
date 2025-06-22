"""
Authentication schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class RegisterRequest(BaseModel):
    """User registration request schema."""
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=4, max_length=128)
    email: Optional[EmailStr] = Field(None)
    role: Optional[str] = Field(default="editor", pattern="^(editor|admin)$")


class RegisterResponse(BaseModel):
    """User registration response schema."""
    success: bool
    message: str
    data: dict


class LoginRequest(BaseModel):
    """User login request schema."""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class LoginResponse(BaseModel):
    """User login response schema."""
    success: bool
    message: str
    data: dict


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str = Field(..., min_length=1)


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema."""
    success: bool
    message: str
    data: dict


class LogoutRequest(BaseModel):
    """Logout request schema."""
    pass


class LogoutResponse(BaseModel):
    """Logout response schema."""
    success: bool
    message: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""
    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=4, max_length=128)
    confirm_password: str = Field(..., min_length=4, max_length=128)
    
    def validate_passwords_match(self):
        """Validate that new password and confirm password match."""
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class ChangePasswordResponse(BaseModel):
    """Change password response schema."""
    success: bool
    message: str


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str
    message: str
    details: Optional[dict] = None 