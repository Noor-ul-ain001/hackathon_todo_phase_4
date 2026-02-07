"""
Todo Intelligence Platform - Backend Application
Main entry point for the FastAPI application
"""

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Import API routes
from src.api.chat import router as chat_router
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from src.api.projects import router as projects_router
from src.api.analytics import router as analytics_router
from src.api.user import router as user_router
from src.db.connection import get_db, create_db_and_tables
from src.models import *  # Import all models for database creation

# Create FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    await create_db_and_tables()
    yield
    # Cleanup if needed


app = FastAPI(
    title="Todo Intelligence Platform API",
    description="AI-powered task management system with natural language processing",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:3004"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler to ensure CORS headers on errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to ensure CORS headers are set on all error responses.
    This prevents CORS errors from masking the actual error message.
    """
    print(f"Error occurred: {exc}")
    print(f"Traceback: {traceback.format_exc()}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )

# Include API routes
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(projects_router, prefix="/api", tags=["projects"])
app.include_router(analytics_router, prefix="/api", tags=["analytics"])
app.include_router(user_router, prefix="/api", tags=["user"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "service": "backend"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Todo Intelligence Platform API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/api/{user_id}/chat",
            "/api/{user_id}/tasks",
            "/api/{user_id}/tasks/{task_id}"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )