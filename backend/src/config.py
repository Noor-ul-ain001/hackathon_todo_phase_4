"""
Configuration module for Todo Intelligence Platform backend.

Loads environment variables and provides configuration settings for:
- Database connection
- Authentication (JWT)
- API settings
- External services
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ==============================================
    # Application
    # ==============================================
    app_name: str = "Todo Intelligence Platform"
    app_version: str = "1.0.0"
    environment: str = "development"  # development | staging | production
    debug: bool = False

    # ==============================================
    # Database (Neon PostgreSQL)
    # ==============================================
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_recycle: int = 3600  # seconds
    database_echo: bool = False  # Set to True for SQL logging

    # ==============================================
    # API
    # ==============================================
    api_base_url: str = "http://localhost:7860"
    api_port: int = 7860
    api_host: str = "0.0.0.0"

    # ==============================================
    # Authentication (JWT)
    # ==============================================
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60  # 1 hour
    jwt_refresh_token_expire_days: int = 7  # 7 days

    # ==============================================
    # MCP Server
    # ==============================================
    mcp_server_url: str = "http://localhost:8001"

    # ==============================================
    # External Services (AI APIs)
    # ==============================================
    groq_api_key: Optional[str] = None  # For Groq LLM API
    google_vision_api_key: Optional[str] = None  # For OCR

    # ==============================================
    # Monitoring (Stage 8)
    # ==============================================
    sentry_dsn: Optional[str] = None
    log_level: str = "INFO"  # DEBUG | INFO | WARNING | ERROR | CRITICAL

    # ==============================================
    # Rate Limiting (Stage 7)
    # ==============================================
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

# Debug: Print database URL (remove password for security)
import re
db_url_safe = re.sub(r'://([^:]+):([^@]+)@', r'://\1:****@', settings.database_url)
print(f"[CONFIG] Loaded DATABASE_URL: {db_url_safe}")
