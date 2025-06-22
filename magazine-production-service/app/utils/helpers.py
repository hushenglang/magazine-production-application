"""
Helper utility functions.
"""

import re
from typing import Optional
from datetime import datetime


def validate_username(username: str) -> bool:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not username or len(username) < 3 or len(username) > 50:
        return False
    
    # Check alphanumeric + underscore pattern
    pattern = r"^[a-zA-Z0-9_]+$"
    return bool(re.match(pattern, username))


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    # Basic email pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not password or len(password) < 4:
        return False
    
    return True


def format_datetime(dt: datetime) -> str:
    """
    Format datetime to ISO string.
    
    Args:
        dt: Datetime object
        
    Returns:
        ISO formatted datetime string
    """
    return dt.isoformat()


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """
    Sanitize string input.
    
    Args:
        value: String to sanitize
        
    Returns:
        Sanitized string or None
    """
    if not value:
        return None
    
    # Strip whitespace and convert empty strings to None
    sanitized = value.strip()
    return sanitized if sanitized else None


def create_api_response(
    success: bool = True,
    message: str = "",
    data: Optional[dict] = None,
    error: Optional[str] = None,
    details: Optional[dict] = None
) -> dict:
    """
    Create standardized API response.
    
    Args:
        success: Whether the operation was successful
        message: Response message
        data: Response data
        error: Error code (if any)
        details: Additional error details
        
    Returns:
        Standardized response dictionary
    """
    response = {
        "success": success,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    if error:
        response["error"] = error
    
    if details:
        response["details"] = details
    
    return response 