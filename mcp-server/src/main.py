"""
Todo Intelligence Platform - MCP Server
Main entry point for the Model Context Protocol server
"""

from mcp import Server
from mcp.server.stdio import run_stdio_server
import asyncio
from backend.src.db.connection import get_db, create_db_and_tables
from backend.src.models import *  # Import all models

# Initialize the MCP server
server = Server("todo-mcp-server")

# Import and register the tools
from mcp_server.src.tools.add_task import add_task_tool
from mcp_server.src.tools.list_tasks import list_tasks_tool
from mcp_server.src.tools.update_task import update_task_tool
from mcp_server.src.tools.complete_task import complete_task_tool
from mcp_server.src.tools.delete_task import delete_task_tool

# Register the tools with the server
server.tools.add(add_task_tool)
server.tools.add(list_tasks_tool)
server.tools.add(update_task_tool)
server.tools.add(complete_task_tool)
server.tools.add(delete_task_tool)

async def main():
    """Main function to run the MCP server"""
    # Initialize database
    await create_db_and_tables()
    
    # Run the server
    await run_stdio_server(server)


if __name__ == "__main__":
    asyncio.run(main())