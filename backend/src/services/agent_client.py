"""
Agent Client Module - Groq AI Integration

Provides interface for backend API to invoke Groq AI for task management.
Connects to Groq API and processes user requests with natural language understanding.
"""

import os
import logging
import json
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from groq import Groq

logger = logging.getLogger(__name__)


class AgentClient:
    """
    Client for invoking Groq AI for natural language task management.

    Uses Llama 3.1 70B model with function calling for task operations.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Groq agent client.

        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"  # Free Groq model - Fast and efficient

        logger.info(f"AgentClient initialized with Groq AI ({self.model})")

    async def process_chat_message(
        self,
        raw_input: str,
        user_id: str,
        db: AsyncSession = None,
        modality: str = "text",
        language: str = "en-US",
        metadata: Dict[str, Any] = None,
        conversation_context: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message through Groq AI with function calling.

        Args:
            raw_input: User's raw input message
            user_id: User ID
            db: Database session for task operations
            modality: Input modality (text | voice | image)
            language: Input language
            metadata: Additional metadata
            conversation_context: Previous conversation messages

        Returns:
            Agent processing result with AI-generated response
        """
        logger.info(f"Processing message with Groq AI for user {user_id}: {raw_input[:50]}...")

        try:
            # Build conversation history
            messages = []

            # System prompt with task management instructions
            system_prompt = """You are TaskFlow AI Assistant, a helpful AI that manages tasks using natural language.

You can help users:
- Create new tasks (add, create new task)
- List all tasks (show, list, view tasks)
- Complete tasks (mark as done, complete)
- Update tasks (change priority, update status)
- Delete tasks (remove, delete)

Be conversational, friendly, and concise. When performing task operations, confirm what you did.
When users ask general questions, answer helpfully but guide them toward task management features.

IMPORTANT: Always use the provided functions to perform task operations. Never fake or simulate task creation."""

            messages.append({"role": "system", "content": system_prompt})

            # Add conversation context if provided
            if conversation_context:
                for msg in conversation_context[-10:]:  # Last 10 messages for context
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            # Add current user message
            messages.append({"role": "user", "content": raw_input})

            # Define available functions for task management
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "create_task",
                        "description": "Create a new task with a title. Use this when user wants to add, create, or make a new task.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "The title/description of the task"
                                }
                            },
                            "required": ["title"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "list_tasks",
                        "description": "List all tasks for the user. Use this when user wants to see, view, list, or show their tasks.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "complete_task",
                        "description": "Mark a task as completed. Use this when user wants to complete, finish, or mark a task as done.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "integer",
                                    "description": "The ID of the task to complete"
                                }
                            },
                            "required": ["task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "description": "Update a task's properties (title, status, priority). Use when user wants to modify or change a task.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "integer",
                                    "description": "The ID of the task to update"
                                },
                                "title": {
                                    "type": "string",
                                    "description": "New title for the task (optional)"
                                },
                                "status": {
                                    "type": "string",
                                    "enum": ["pending", "in_progress", "completed"],
                                    "description": "New status for the task (optional)"
                                },
                                "priority": {
                                    "type": "string",
                                    "enum": ["low", "medium", "high"],
                                    "description": "New priority level (optional)"
                                }
                            },
                            "required": ["task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_task",
                        "description": "Delete a task permanently. Use when user wants to remove or delete a task.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "integer",
                                    "description": "The ID of the task to delete"
                                }
                            },
                            "required": ["task_id"]
                        }
                    }
                }
            ]

            # Call Groq AI
            logger.info(f"Calling Groq API with {len(messages)} messages...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1024
            )

            # Get the AI's response
            message = response.choices[0].message
            tool_calls_executed = []
            tasks_affected = []

            # Execute function calls if AI requested them
            if message.tool_calls and db:
                logger.info(f"AI requested {len(message.tool_calls)} function call(s)")

                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    logger.info(f"Executing function: {function_name} with args: {function_args}")
                    tool_calls_executed.append(function_name)

                    # Execute the appropriate function
                    if function_name == "create_task":
                        task = await self._create_task(db, user_id, function_args["title"])
                        tasks_affected.append(task.id)

                    elif function_name == "list_tasks":
                        await self._list_tasks(db, user_id)

                    elif function_name == "complete_task":
                        task = await self._complete_task(db, user_id, function_args["task_id"])
                        if task:
                            tasks_affected.append(task.id)

                    elif function_name == "update_task":
                        task_id = function_args.pop("task_id")
                        task = await self._update_task(db, user_id, task_id, function_args)
                        if task:
                            tasks_affected.append(task.id)

                    elif function_name == "delete_task":
                        task = await self._delete_task(db, user_id, function_args["task_id"])
                        if task:
                            tasks_affected.append(task.id)

                # Get final response from AI after function execution
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "content": json.dumps({"status": "success", "tasks_affected": tasks_affected}),
                    "tool_call_id": message.tool_calls[0].id
                })

                # Get AI's final response
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024
                )

                ai_response = final_response.choices[0].message.content

            else:
                # No function calls, just use AI's response
                ai_response = message.content if message.content else "I understand. How can I help you with your tasks?"

            logger.info(f"Groq AI completed processing successfully")

            return {
                "success": True,
                "response": ai_response,
                "intent": {
                    "raw_input": raw_input,
                    "language": language
                },
                "agents_invoked": ["Groq-Llama-3.1-70B"],
                "tool_calls": tool_calls_executed,
                "tasks_affected": tasks_affected
            }

        except Exception as e:
            logger.error(f"Groq AI error: {e}", exc_info=True)
            return {
                "success": False,
                "response": f"I encountered an error processing your request. Please try again. ({str(e)[:100]})",
                "error": {
                    "code": "GROQ_AI_ERROR",
                    "message": str(e)
                },
                "agents_invoked": ["Groq-AI"],
                "tool_calls": [],
                "tasks_affected": []
            }

    # ==========================================
    # Task Operation Methods
    # ==========================================

    async def _create_task(self, db: AsyncSession, user_id: str, title: str):
        """Create a new task in the database."""
        from ..models.task import Task, TaskStatus, TaskPriority

        task = Task(
            user_id=user_id,
            title=title,
            description="",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(task)
        await db.commit()
        await db.refresh(task)

        logger.info(f"Created task {task.id}: {title}")
        return task

    async def _list_tasks(self, db: AsyncSession, user_id: str):
        """List tasks for a user."""
        from ..models.task import Task

        query = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        result = await db.execute(query)
        tasks = result.scalars().all()

        logger.info(f"Listed {len(tasks)} tasks for user {user_id}")
        return tasks

    async def _complete_task(self, db: AsyncSession, user_id: str, task_id: int):
        """Mark a task as completed."""
        from ..models.task import Task, TaskStatus

        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user {user_id}")
            return None

        task.status = TaskStatus.COMPLETED
        task.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)

        logger.info(f"Completed task {task.id}: {task.title}")
        return task

    async def _update_task(self, db: AsyncSession, user_id: str, task_id: int, update_data: dict):
        """Update a task with new data."""
        from ..models.task import Task, TaskStatus, TaskPriority

        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user {user_id}")
            return None

        # Update fields if provided
        if 'title' in update_data:
            task.title = update_data['title']

        if 'status' in update_data:
            status_map = {
                'pending': TaskStatus.PENDING,
                'in_progress': TaskStatus.IN_PROGRESS,
                'completed': TaskStatus.COMPLETED
            }
            task.status = status_map.get(update_data['status'], task.status)

        if 'priority' in update_data:
            priority_map = {
                'low': TaskPriority.LOW,
                'medium': TaskPriority.MEDIUM,
                'high': TaskPriority.HIGH
            }
            task.priority = priority_map.get(update_data['priority'], task.priority)

        task.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)

        logger.info(f"Updated task {task.id}: {task.title}")
        return task

    async def _delete_task(self, db: AsyncSession, user_id: str, task_id: int):
        """Delete a task."""
        from ..models.task import Task

        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user {user_id}")
            return None

        # Store task info before deletion
        task_info = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

        await db.delete(task)
        await db.commit()

        logger.info(f"Deleted task {task_info.id}: {task_info.title}")
        return task_info

    async def close(self):
        """Close the agent client and cleanup resources."""
        logger.info("AgentClient closed")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
