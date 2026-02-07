"""
Script to create a test user in the database for Phase 3 testing.
"""

import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.connection import get_db
from src.models.user import User


async def create_test_user():
    """Create a test user for development."""
    async for db in get_db():
        # Check if user already exists
        from sqlalchemy import select
        query = select(User).where(User.id == "user_123")
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"[OK] Test user 'user_123' already exists")
            return

        # Create new test user
        test_user = User(
            id="user_123",
            email="test@example.com",
            password_hash=None,  # No password for testing
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(test_user)
        await db.commit()
        await db.refresh(test_user)

        print(f"[OK] Created test user: {test_user.id} ({test_user.email})")


if __name__ == "__main__":
    asyncio.run(create_test_user())
