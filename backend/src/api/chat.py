"""
API Endpoint: Chat Endpoint

Stateless conversational API endpoint for Todo Intelligence Platform.
Handles text, voice, and image inputs through agent system.

Per constitution.md:
- Stateless architecture: no session state, all context from database
- Single endpoint for all modalities
- User isolation enforced
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Path as PathParam, Query
from pydantic import BaseModel, Field
import logging
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db.connection import get_db
from ..services.agent_client import AgentClient
from ..services.conversation_service import ConversationService
from ..models.message import Message

logger = logging.getLogger(__name__)


# ==============================================
# Request/Response Models
# ==============================================

class ChatRequest(BaseModel):
    """Chat request model."""
    conversation_id: Optional[int] = Field(None, description="Conversation ID (creates new if not provided)")
    message: str = Field(..., description="User message or command")
    modality: str = Field("text", description="Input modality: text | voice | image")
    language: str = Field("en-US", description="Input language: en-US | ur-PK")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata (image data, etc.)")


class ChatResponse(BaseModel):
    """Chat response model."""
    conversation_id: int = Field(..., description="Conversation ID")
    response: str = Field(..., description="Agent response message")
    tool_calls: list = Field(default_factory=list, description="MCP tools that were invoked")
    tasks_affected: list = Field(default_factory=list, description="Task IDs that were affected")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution metadata")


# Create the API router
router = APIRouter()

# Global agent client instance (initialized on first request)
_agent_client: Optional[AgentClient] = None


async def get_agent_client() -> AgentClient:
    """Get or create agent client instance."""
    global _agent_client
    if _agent_client is None:
        _agent_client = AgentClient()
        logger.info("AgentClient initialized")
    return _agent_client


# ==============================================
# Chat Endpoint
# ==============================================

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str = PathParam(..., description="User ID"),
    request: ChatRequest = ...,
    db: AsyncSession = Depends(get_db)
) -> ChatResponse:
    """
    Main chat endpoint - handles all modalities (text, voice, image).

    Stateless architecture:
    1. Load conversation context from database (if conversation_id provided)
    2. Invoke agent system to process message
    3. Save user message and agent response to database
    4. Return formatted response (no state kept in memory)

    Args:
        user_id: User ID from URL path (will be validated via JWT in Stage 7)
        request: Chat request with message, modality, and optional conversation_id
        db: Database session

    Returns:
        Chat response with agent's reply and metadata

    Example:
        POST /api/user_123/chat
        {
            "message": "todo add 'Review spec' --due tomorrow",
            "modality": "text"
        }

        Response:
        {
            "conversation_id": 1,
            "response": "✓ Task created: Review spec (Due: Dec 28)",
            "tool_calls": [...],
            "tasks_affected": [42],
            "metadata": {...}
        }
    """
    start_time = time.time()
    logger.info(f"Chat endpoint called: user={user_id}, modality={request.modality}")

    conversation_id = None  # Initialize to avoid UnboundLocalError in exception handler

    try:
        # Validate required parameters
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message is required")

        if request.modality not in ["text", "voice", "image"]:
            logger.warning(f"Invalid modality: {request.modality}, defaulting to 'text'")
            request.modality = "text"

        # Initialize services
        conversation_service = ConversationService(db)
        agent_client = await get_agent_client()

        # Step 1: Get or create conversation
        conversation_id, is_new = await conversation_service.get_or_create_conversation(
            request.conversation_id,
            user_id
        )
        logger.info(f"Conversation {conversation_id} (new={is_new})")

        # Step 2: Load conversation context (for continuity)
        context = await conversation_service.load_conversation_context(
            conversation_id,
            user_id,
            limit=10
        )
        logger.info(f"Loaded {len(context)} messages for context")

        # Step 3: Save user message
        await conversation_service.save_message(
            conversation_id,
            user_id,
            "user",
            request.message
        )

        # Step 4: Process through agent system (with conversation context)
        agent_result = await agent_client.process_chat_message(
            raw_input=request.message,
            user_id=user_id,
            db=db,
            modality=request.modality,
            language=request.language,
            metadata=request.metadata,
            conversation_context=context  # Pass conversation context to AI
        )

        # Handle agent errors
        if not agent_result.get("success"):
            error_response = agent_result.get("response", "Failed to process request")
            await conversation_service.save_message(
                conversation_id,
                user_id,
                "assistant",
                error_response
            )

            return ChatResponse(
                conversation_id=conversation_id,
                response=error_response,
                tool_calls=[],
                tasks_affected=[],
                metadata={
                    "error": agent_result.get("error"),
                    "agents_invoked": agent_result.get("agents_invoked", []),
                    "execution_time_ms": int((time.time() - start_time) * 1000),
                    "modality": request.modality,
                    "language": request.language
                }
            )

        # Extract response
        response_message = agent_result["response"]
        tool_calls = agent_result.get("tool_calls", [])
        tasks_affected = agent_result.get("tasks_affected", [])

        # Step 5: Save agent response
        saved_message = await conversation_service.save_message(
            conversation_id,
            user_id,
            "assistant",
            response_message
        )

        # Step 6: Return formatted response
        execution_time = int((time.time() - start_time) * 1000)

        logger.info(f"Chat endpoint completed in {execution_time}ms")

        return ChatResponse(
            conversation_id=conversation_id,
            response=response_message,
            tool_calls=tool_calls,
            tasks_affected=tasks_affected,
            metadata={
                "message_id": saved_message.id,
                "agents_invoked": agent_result.get("agents_invoked", []),
                "execution_time_ms": execution_time,
                "modality": request.modality,
                "language": request.language,
                "intent": agent_result.get("intent", {})
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)

        # Save error message to conversation (if we have a conversation_id)
        error_message = "I'm sorry, I encountered an error processing your request. Please try again."

        if conversation_id:
            try:
                await conversation_service.save_message(
                    conversation_id,
                    user_id,
                    "assistant",
                    error_message
                )
            except Exception:
                pass  # Ignore errors when trying to save error message

        return ChatResponse(
            conversation_id=conversation_id if conversation_id else -1,
            response=error_message,
            tool_calls=[],
            tasks_affected=[],
            metadata={
                "error": str(e),
                "execution_time_ms": int((time.time() - start_time) * 1000),
                "modality": request.modality,
                "language": getattr(request, 'language', 'en-US')
            }
        )


@router.get("/{user_id}/chat/history")
async def get_chat_history(
    user_id: str = PathParam(..., description="User ID"),
    conversation_id: int = Query(..., description="Conversation ID"),
    limit: int = Query(50, le=100, description="Maximum number of messages to retrieve"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get conversation history.

    Retrieves messages from a specific conversation with pagination support.

    Args:
        user_id: User ID from URL path
        conversation_id: Conversation ID to load messages from
        limit: Maximum number of messages (default: 50, max: 100)
        db: Database session

    Returns:
        Dict containing messages array and conversation_id

    Example:
        GET /api/user_123/chat/history?conversation_id=1&limit=50

        Response:
        {
            "messages": [
                {
                    "id": 1,
                    "role": "user",
                    "content": "Hello",
                    "created_at": "2025-12-30T10:00:00Z"
                },
                ...
            ],
            "conversation_id": 1
        }
    """
    logger.info(f"Loading chat history: user={user_id}, conversation={conversation_id}, limit={limit}")

    try:
        # Verify conversation exists and belongs to user
        conversation_service = ConversationService(db)

        # This will validate ownership or create new if invalid
        verified_conv_id, _ = await conversation_service.get_or_create_conversation(
            conversation_id,
            user_id
        )

        # If conversation ID changed, user doesn't own the requested conversation
        if verified_conv_id != conversation_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied: conversation does not belong to user"
            )

        # Load messages with full details
        query = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at).limit(limit)

        result = await db.execute(query)
        messages = result.scalars().all()

        # Format for frontend
        formatted_messages = [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]

        logger.info(f"Retrieved {len(formatted_messages)} messages from conversation {conversation_id}")

        return {
            "messages": formatted_messages,
            "conversation_id": conversation_id
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error loading chat history: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load conversation history: {str(e)}"
        )