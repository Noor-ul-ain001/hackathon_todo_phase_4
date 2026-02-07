"""
Base Agent Class

All agents inherit from this base class for common functionality.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all agents.

    Agents are autonomous components that:
    - Process inputs and make decisions
    - Invoke skills to perform operations
    - Coordinate with other agents
    - Format and return results
    """

    def __init__(self, skill_client=None, ai_client=None):
        """
        Initialize agent.

        Args:
            skill_client: SkillClient instance for calling skills
            ai_client: AI client (Claude or OpenAI) for reasoning
        """
        self.skill_client = skill_client
        self.ai_client = ai_client
        self.agent_name = self.__class__.__name__
        logger.info(f"Agent initialized: {self.agent_name}")

    @abstractmethod
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process inputs and return result.

        Args:
            inputs: Agent input data

        Returns:
            Agent execution result
        """
        pass

    def _format_success(self, data: Any) -> Dict[str, Any]:
        """
        Format successful result.

        Args:
            data: Result data

        Returns:
            Standardized success response
        """
        return {
            "success": True,
            "agent": self.agent_name,
            "data": data
        }

    def _format_error(
        self,
        code: str,
        message: str,
        details: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Format error result.

        Args:
            code: Error code
            message: Error message
            details: Additional error details

        Returns:
            Standardized error response
        """
        return {
            "success": False,
            "agent": self.agent_name,
            "error": {
                "code": code,
                "message": message,
                "details": details
            }
        }
