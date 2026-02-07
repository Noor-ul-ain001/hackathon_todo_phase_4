"""
Database connection for MCP Server.

Connects to the same Neon PostgreSQL database as the backend.
Uses async SQLAlchemy + SQLModel for consistency.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from typing import AsyncGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================
# Database Configuration
# ==============================================

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Connection pool settings (same as backend for consistency)
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "20"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
DATABASE_POOL_RECYCLE = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"

# ==============================================
# Database Engine
# ==============================================

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=DATABASE_ECHO,
    future=True,
    pool_size=DATABASE_POOL_SIZE,
    max_overflow=DATABASE_MAX_OVERFLOW,
    pool_recycle=DATABASE_POOL_RECYCLE,
    pool_pre_ping=True,
    poolclass=AsyncAdaptedQueuePool,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ==============================================
# Database Session Provider
# ==============================================

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session for MCP tools.

    Yields:
        AsyncSession: Database session

    Example:
        async with get_db_session() as session:
            result = await session.execute(query)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


# ==============================================
# Database Connection Testing
# ==============================================

async def test_connection() -> bool:
    """
    Test database connection.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        logger.info("✓ MCP Server database connection successful")
        return True
    except Exception as e:
        logger.error(f"✗ MCP Server database connection failed: {e}")
        return False


async def close_connection():
    """Close database engine and dispose of connection pool."""
    await engine.dispose()
    logger.info("MCP Server database connection pool disposed")
