"""
API module for the Todo Intelligence Platform.

This module contains all the API endpoints for the application.
Currently includes the chat endpoint for the conversational interface.
"""

from .chat import router as chat_router

__all__ = [
    "chat_router"
]