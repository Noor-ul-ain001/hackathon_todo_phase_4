"""
Conversation Service

Manages conversation and message persistence in Neon PostgreSQL.
Implements stateless conversation loading and message storage.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

# Add backend models to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.conversation import Conversation
from src.models.message import Message

logger = logging.getLogger(__name__)


class ConversationService:
    """
    Service for managing conversations and messages.

    Handles:
    - Creating new conversations
    - Loading conversation context from database
    - Saving messages to conversations
    - Ensuring stateless architecture (no session state)
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize conversation service.

        Args:
            db_session: SQLAlchemy async database session
        """
        self.db = db_session
        logger.info("ConversationService initialized")

    async def get_or_create_conversation(
        self,
        conversation_id: Optional[int],
        user_id: str
    ) -> Tuple[int, bool]:
        """
        Get existing conversation or create new one.

        Args:
            conversation_id: Optional conversation ID
            user_id: User ID

        Returns:
            Tuple of (conversation_id, is_new)

        Example:
            >>> service = ConversationService(db_session)
            >>> conv_id, is_new = await service.get_or_create_conversation(None, "user_123")
            >>> print(f"Conversation {conv_id}, new={is_new}")
        """
        if conversation_id is None:
            # Create new conversation
            logger.info(f"Creating new conversation for user {user_id}")

            new_conversation = Conversation(
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(new_conversation)
            await self.db.commit()
            await self.db.refresh(new_conversation)

            logger.info(f"Created conversation {new_conversation.id}")
            return new_conversation.id, True

        else:
            # Verify conversation exists and belongs to user
            logger.info(f"Loading existing conversation {conversation_id} for user {user_id}")

            query = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            result = await self.db.execute(query)
            conversation = result.scalar_one_or_none()

            if not conversation:
                logger.warning(f"Conversation {conversation_id} not found or unauthorized")
                # Create new conversation instead
                return await self.get_or_create_conversation(None, user_id)

            return conversation.id, False

    async def load_conversation_context(
        self,
        conversation_id: int,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Load recent messages from conversation for context.

        Args:
            conversation_id: Conversation ID
            user_id: User ID (for security verification)
            limit: Maximum number of messages to load

        Returns:
            List of messages in format [{"role": "user", "content": "..."}]

        Example:
            >>> context = await service.load_conversation_context(123, "user_123", 10)
            >>> print(f"Loaded {len(context)} messages")
        """
        logger.info(f"Loading context for conversation {conversation_id} (limit={limit})")

        # Query messages ordered by creation time
        query = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at).limit(limit)

        result = await self.db.execute(query)
        messages = result.scalars().all()

        # Format messages for agent context
        context = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]

        logger.info(f"Loaded {len(context)} messages from conversation {conversation_id}")
        return context

    async def save_message(
        self,
        conversation_id: int,
        user_id: str,
        role: str,
        content: str
    ) -> Message:
        """
        Save a message to the conversation.

        Args:
            conversation_id: Conversation ID
            user_id: User ID
            role: Message role ("user" or "assistant")
            content: Message content

        Returns:
            Saved message object

        Example:
            >>> msg = await service.save_message(123, "user_123", "user", "Hello!")
            >>> print(f"Message {msg.id} saved")
        """
        logger.info(f"Saving {role} message to conversation {conversation_id}")

        # Create message
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )

        self.db.add(message)

        # Update conversation timestamp
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.db.execute(query)
        conversation = result.scalar_one_or_none()

        if conversation:
            conversation.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(message)

        logger.info(f"Message {message.id} saved successfully")
        return message

    async def get_conversation_summary(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent conversations for a user.

        Args:
            user_id: User ID
            limit: Maximum number of conversations

        Returns:
            List of conversation summaries

        Example:
            >>> conversations = await service.get_conversation_summary("user_123", 5)
            >>> for conv in conversations:
            ...     print(f"{conv['id']}: {conv['message_count']} messages")
        """
        logger.info(f"Getting conversation summary for user {user_id}")

        # Query conversations ordered by last update
        query = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(desc(Conversation.updated_at)).limit(limit)

        result = await self.db.execute(query)
        conversations = result.scalars().all()

        # Get message count for each conversation
        summaries = []
        for conv in conversations:
            msg_count_query = select(Message).where(
                Message.conversation_id == conv.id
            )
            msg_result = await self.db.execute(msg_count_query)
            messages = msg_result.scalars().all()

            summaries.append({
                "id": conv.id,
                "user_id": conv.user_id,
                "message_count": len(messages),
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            })

        logger.info(f"Found {len(summaries)} conversations for user {user_id}")
        return summaries
