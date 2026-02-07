"""
Database connection module for Todo Intelligence Platform.

Provides async PostgreSQL connection using SQLAlchemy 2.0 + SQLModel.

Connection pooling configured per constitution.md section 7.2:
- Pool size: 20 connections
- Max overflow: 10 connections
- Pool recycle: 3600 seconds (1 hour)
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool, AsyncAdaptedQueuePool
from sqlmodel import SQLModel
from typing import AsyncGenerator
import logging

from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)

# ==============================================
# Database Engine
# ==============================================

# Create async engine with connection pooling
# Configure connection args based on database type
connect_args = {}
poolclass = AsyncAdaptedQueuePool

# Check if using PostgreSQL (asyncpg)
if "postgresql" in settings.database_url:
    connect_args = {
        "ssl": "require",  # SSL is required for Neon PostgreSQL
        "server_settings": {
            "application_name": "todo_intelligence_platform"
        }
    }
# Check if using SQLite
elif "sqlite" in settings.database_url:
    connect_args = {"check_same_thread": False}
    poolclass = NullPool  # SQLite doesn't support connection pooling

engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,  # Log SQL queries if enabled
    future=True,
    pool_size=settings.database_pool_size if "postgresql" in settings.database_url else 5,
    max_overflow=settings.database_max_overflow if "postgresql" in settings.database_url else 0,
    pool_recycle=settings.database_pool_recycle,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Test connections before using
    poolclass=poolclass,  # Use connection pooling for PostgreSQL, NullPool for SQLite
    connect_args=connect_args
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
# Database Session Dependency
# ==============================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI to provide database sessions.

    Yields:
        AsyncSession: Database session

    Example:
        @app.get("/tasks")
        async def list_tasks(db: AsyncSession = Depends(get_db)):
            ...
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

async def test_db_connection() -> bool:
    """
    Test database connection.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        logger.info("✓ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False


async def close_db_connection():
    """Close database engine and dispose of connection pool."""
    await engine.dispose()
    logger.info("Database connection pool disposed")


async def create_db_and_tables():
    """
    Create all database tables using SQLModel metadata.

    This function creates all tables defined in the models if they don't exist.
    Safe to call multiple times (uses CREATE TABLE IF NOT EXISTS internally).

    Note: Errors are logged but don't prevent server startup. This allows
    the server to start even if database is temporarily unavailable.
    """
    try:
        # Import all models to register them with SQLModel.metadata
        from ..models import User, Task, Conversation, Message

        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("✓ Database tables created successfully")
    except Exception as e:
        logger.warning(f"⚠ Failed to create database tables: {e}")
        logger.warning("⚠ Server will continue startup, but database operations may fail")
        logger.warning("⚠ Please verify DATABASE_URL in .env file and database credentials")
        # Don't raise - allow server to start anyway
