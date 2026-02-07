"""
MCP Server for Todo Intelligence Platform.

Provides 5 MCP tools as the exclusive data access layer:
1. add_task
2. list_tasks
3. update_task
4. complete_task
5. delete_task

Per constitution.md section 5, all database operations MUST flow through these tools.
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from typing import Any

from .db import test_connection, close_connection
from .tools.add_task import add_task_tool
from .tools.list_tasks import list_tasks_tool
from .tools.update_task import update_task_tool
from .tools.complete_task import complete_task_tool
from .tools.delete_task import delete_task_tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================
# MCP Server Instance
# ==============================================

# Create MCP server
app = Server("todo-intelligence-mcp")


# ==============================================
# Tool Registry
# ==============================================

# Register all 5 MCP tools
@app.list_tools()
async def list_tools() -> list[dict[str, Any]]:
    """
    List all available MCP tools.

    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "add_task",
            "description": "Create a new task for a user",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (required)"},
                    "title": {"type": "string", "description": "Task title (1-200 chars)"},
                    "description": {"type": "string", "description": "Task description (optional, max 2000 chars)"},
                    "due_date": {"type": "string", "description": "Due date in ISO 8601 format (YYYY-MM-DD)"},
                    "due_time": {"type": "string", "description": "Due time in HH:MM format"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Task priority"},
                    "status": {"type": "string", "enum": ["pending", "in_progress", "completed"], "description": "Task status"}
                },
                "required": ["user_id", "title"]
            }
        },
        {
            "name": "list_tasks",
            "description": "Query tasks for a user with optional filtering, sorting, and pagination",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (required)"},
                    "filters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "priority": {"type": "string"},
                            "due_before": {"type": "string"},
                            "due_after": {"type": "string"},
                            "search": {"type": "string"}
                        }
                    },
                    "sort": {"type": "string", "description": "Sort order (e.g., created_at_desc)"},
                    "limit": {"type": "integer", "description": "Max results (1-100, default 20)"},
                    "offset": {"type": "integer", "description": "Pagination offset (default 0)"}
                },
                "required": ["user_id"]
            }
        },
        {
            "name": "update_task",
            "description": "Update specific fields of an existing task",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (required)"},
                    "task_id": {"type": "integer", "description": "Task ID to update (required)"},
                    "updates": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "due_date": {"type": "string"},
                            "due_time": {"type": "string"},
                            "priority": {"type": "string"},
                            "status": {"type": "string"}
                        }
                    }
                },
                "required": ["user_id", "task_id", "updates"]
            }
        },
        {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (required)"},
                    "task_id": {"type": "integer", "description": "Task ID to complete (required)"}
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "delete_task",
            "description": "Delete a task from the system",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (required)"},
                    "task_id": {"type": "integer", "description": "Task ID to delete (required)"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    ]


# ==============================================
# Tool Handlers
# ==============================================

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Route tool calls to appropriate handlers.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        Tool result

    Raises:
        ValueError: If tool not found
    """
    logger.info(f"Tool called: {name} with args: {arguments}")

    # Route to appropriate tool handler
    if name == "add_task":
        result = await add_task_tool(arguments)
    elif name == "list_tasks":
        result = await list_tasks_tool(arguments)
    elif name == "update_task":
        result = await update_task_tool(arguments)
    elif name == "complete_task":
        result = await complete_task_tool(arguments)
    elif name == "delete_task":
        result = await delete_task_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

    logger.info(f"Tool {name} result: {result}")
    return [{"type": "text", "text": str(result)}]


# ==============================================
# Server Lifecycle
# ==============================================

async def main():
    """
    Start MCP server.

    Tests database connection and runs server via stdio.
    """
    logger.info("Starting Todo Intelligence MCP Server...")

    # Test database connection
    connected = await test_connection()
    if not connected:
        logger.error("Database connection failed - exiting")
        return

    try:
        # Run server
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    finally:
        # Clean up
        await close_connection()
        logger.info("MCP Server shut down")


if __name__ == "__main__":
    asyncio.run(main())
