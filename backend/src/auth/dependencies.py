"""
FastAPI dependencies for authentication.

Provides dependency injection for protected routes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from src.db.connection import get_db
from src.models.user import User
from .security import verify_token

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract token
    token = credentials.credentials

    # Verify token
    payload = verify_token(token, token_type="access")
    if payload is None:
        raise credentials_exception

    # Get user_id from payload
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active user (can add more checks here).

    Args:
        current_user: Current authenticated user

    Returns:
        User object

    Raises:
        HTTPException: If user is inactive or disabled
    """
    # Add additional checks here if needed (e.g., is_active flag)
    # For now, just return the user
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get the current user if token is provided, otherwise return None.
    Useful for routes that can work with or without authentication.

    Args:
        credentials: Optional HTTP Bearer token credentials
        db: Database session

    Returns:
        User object or None
    """
    if credentials is None:
        return None

    try:
        token = credentials.credentials
        payload = verify_token(token, token_type="access")
        if payload is None:
            return None

        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            return None

        statement = select(User).where(User.id == user_id)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()
        return user
    except Exception:
        return None


__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_optional_current_user",
    "security"
]
