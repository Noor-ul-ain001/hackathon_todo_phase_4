"""
Skills module for the Todo Intelligence Platform.

This module contains all the skill implementations that agents use to interact
with the system. Each skill wraps MCP tools and provides a higher-level
interface for agents to perform specific tasks.
"""

from .task_creation import task_creation_skill, mock_task_creation_skill
from .task_listing import task_listing_skill, mock_task_listing_skill
from .task_update import task_update_skill, mock_task_update_skill
from .task_completion import task_completion_skill, mock_task_completion_skill
from .task_deletion import task_deletion_skill, mock_task_deletion_skill
from .intent_disambiguation import intent_disambiguation_skill, mock_intent_disambiguation_skill
from .ui_intent_normalization import ui_intent_normalization_skill, mock_ui_intent_normalization_skill

__all__ = [
    # Task Creation Skill
    "task_creation_skill",
    "mock_task_creation_skill",
    
    # Task Listing Skill
    "task_listing_skill", 
    "mock_task_listing_skill",
    
    # Task Update Skill
    "task_update_skill",
    "mock_task_update_skill",
    
    # Task Completion Skill
    "task_completion_skill",
    "mock_task_completion_skill",
    
    # Task Deletion Skill
    "task_deletion_skill",
    "mock_task_deletion_skill",
    
    # Intent Disambiguation Skill
    "intent_disambiguation_skill",
    "mock_intent_disambiguation_skill",
    
    # UI Intent Normalization Skill
    "ui_intent_normalization_skill",
    "mock_ui_intent_normalization_skill",
]