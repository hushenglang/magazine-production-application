#!/usr/bin/env python3
"""
Script to create an initial admin user for the Magazine Production Application.
Run this script after setting up the database to create the first admin user.
"""

import asyncio
import sys
from getpass import getpass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Add the app directory to Python path
sys.path.append('..')

from app.core.database import AsyncSessionLocal, init_db
from app.core.security import get_password_hash
from app.models.user import User


async def create_admin_user():
    """Create an admin user interactively."""
    
    print("=== Magazine Production Application - Admin User Creation ===\n")
    
    # Initialize database
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully.\n")
    
    # Get user input
    username = input("Enter admin username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return
    
    email = input("Enter admin email (optional): ").strip() or None
    
    password = getpass("Enter admin password: ").strip()
    if not password:
        print("Password cannot be empty!")
        return
    
    confirm_password = getpass("Confirm admin password: ").strip()
    if password != confirm_password:
        print("Passwords do not match!")
        return
    
    # Create admin user
    async with AsyncSessionLocal() as db:
        try:
            # Check if user already exists
            result = await db.execute(select(User).where(User.username == username))
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"User '{username}' already exists!")
                return
            
            # Create new admin user
            hashed_password = get_password_hash(password)
            admin_user = User(
                username=username,
                email=email,
                password_hash=hashed_password,
                role='admin'
            )
            
            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)
            
            print(f"\nAdmin user '{username}' created successfully!")
            print(f"User ID: {admin_user.id}")
            print(f"Email: {admin_user.email}")
            print(f"Role: {admin_user.role}")
            print(f"Created at: {admin_user.created_at}")
            
        except Exception as e:
            await db.rollback()
            print(f"Error creating admin user: {e}")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(create_admin_user()) 