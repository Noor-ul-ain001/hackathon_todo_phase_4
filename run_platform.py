"""
Todo Intelligence Platform - Complete Startup Script

This script starts both the backend and frontend servers.
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path
import threading
import time

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
    print("🚀 Starting Backend Server on port 8000...")
    
    # Change to the project root directory
    os.chdir(project_root)
    
    # Start the backend server using uvicorn
    result = subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "backend.src.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--reload"
    ])
    
    if result.returncode != 0:
        print(f"❌ Backend server failed to start: {result.stderr}")


def start_frontend():
    """Start the frontend Next.js server."""
    print("🎨 Starting Frontend Server on port 3000...")
    
    # Change to the frontend directory
    frontend_dir = project_root / "frontend"
    os.chdir(frontend_dir)
    
    # Install dependencies if not already installed
    print("📦 Installing frontend dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "nodejs"], check=False)  # This might not work on all systems
    
    # For now, we'll assume Node.js is installed globally
    # Install npm dependencies
    result = subprocess.run(["npm", "install"], check=False)
    
    if result.returncode != 0:
        print("⚠️  Frontend dependencies installation failed, continuing anyway...")
    
    # Start the frontend development server
    result = subprocess.run([
        "npm", "run", "dev"
    ])
    
    if result.returncode != 0:
        print(f"❌ Frontend server failed to start: {result.stderr}")


def main():
    """Main function to start the Todo Intelligence Platform."""
    print("🌟 Starting Todo Intelligence Platform...")
    print(f"Project root: {project_root}")
    
    # Initialize the database
    asyncio.run(create_db_and_tables())
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for the backend to start
    time.sleep(3)
    
    # Start frontend in a separate thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    print("✅ Todo Intelligence Platform is starting...")
    print("🌐 Backend: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3000")
    print("💬 Chat interface: http://localhost:3000")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Todo Intelligence Platform...")
        sys.exit(0)


if __name__ == "__main__":
    main()