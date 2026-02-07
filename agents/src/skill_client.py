"""
Skill Client Module for Agents

Provides communication interface between agents and skills.
Agents invoke skills through this client.
"""

import sys
from pathlib import Path
import logging
from typing import Dict, Any

# Add skills to path
skills_path = str(Path(__file__).resolve().parents[2] / "skills" / "src")
sys.path.insert(0, skills_path)

from task_creation import TaskCreationSkill
from task_listing import TaskListingSkill
from task_update import TaskUpdateSkill
from task_completion import TaskCompletionSkill
from task_deletion import TaskDeletionSkill
from intent_disambiguation import IntentDisambiguationSkill
from ui_intent_normalization import UIIntentNormalizationSkill
from mcp_client import MCPClient

logger = logging.getLogger(__name__)


class SkillClient:
    """Client for invoking skills from agents."""

    def __init__(self, mcp_client: MCPClient = None):
        """
        Initialize skill client.

        Args:
            mcp_client: Optional MCPClient instance (creates new if not provided)
        """
        self.mcp_client = mcp_client or MCPClient()

        # Initialize all skills
        self.task_creation = TaskCreationSkill(self.mcp_client)
        self.task_listing = TaskListingSkill(self.mcp_client)
        self.task_update = TaskUpdateSkill(self.mcp_client)
        self.task_completion = TaskCompletionSkill(self.mcp_client)
        self.task_deletion = TaskDeletionSkill(self.mcp_client)
        self.intent_disambiguation = IntentDisambiguationSkill(self.mcp_client)
        self.ui_intent_normalization = UIIntentNormalizationSkill(self.mcp_client)

        logger.info("SkillClient initialized with all 7 skills")

    async def create_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call task_creation skill."""
        return await self.task_creation.execute(params)

    async def list_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call task_listing skill."""
        return await self.task_listing.execute(params)

    async def update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call task_update skill."""
        return await self.task_update.execute(params)

    async def complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call task_completion skill."""
        return await self.task_completion.execute(params)

    async def delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call task_deletion skill."""
        return await self.task_deletion.execute(params)

    async def disambiguate_intent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call intent_disambiguation skill."""
        return await self.intent_disambiguation.execute(params)

    async def normalize_ui_intent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call ui_intent_normalization skill."""
        return await self.ui_intent_normalization.execute(params)

    async def close(self):
        """Close the MCP client."""
        if self.mcp_client:
            await self.mcp_client.close()
        logger.info("SkillClient closed")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
