"""
Todo Intelligence Platform - Startup Script

This script initializes the database and starts the backend services.
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def create_db_and_tables():
    """Create database tables if they don't exist."""
    from backend.src.db.connection import engine
    from backend.src.models.task import Task
    from backend.src.models.user import User
    from backend.src.models.conversation import Conversation
    from backend.src.models.message import Message
    from sqlmodel import SQLModel
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    print("✓ Database tables created successfully")


def start_backend():
    """Start the backend FastAPI server."""
    print("🚀 Starting Backend Server...")
    
    # Change to the project root directory
    os.chdir(project_root)
    
    # Start the backend server using uvicorn
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "backend.src.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ])


def main():
    """Main function to start the Todo Intelligence Platform."""
    print("🌟 Starting Todo Intelligence Platform...")
    print(f"Project root: {project_root}")
    
    # Initialize the database
    asyncio.run(create_db_and_tables())
    
    # Start the backend server
    start_backend()


if __name__ == "__main__":
    main()