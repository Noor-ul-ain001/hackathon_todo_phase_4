"""
Agents module for the Todo Intelligence Platform.

This module contains all the agent implementations that coordinate
the various skills to perform complex tasks. Each agent has a specific
responsibility in the overall system architecture.
"""

from .interface_orchestrator import interface_orchestrator_agent, mock_interface_orchestrator_agent
from .task_reasoning import task_reasoning_agent, mock_task_reasoning_agent
from .validation_safety import validation_safety_agent, mock_validation_safety_agent
from .response_formatter import response_formatter_agent, mock_response_formatter_agent
from .orchestrator import orchestrator_agent, mock_orchestrator_agent
from .visual_context import visual_context_agent, mock_visual_context_agent

__all__ = [
    # Interface Orchestrator Agent
    "interface_orchestrator_agent",
    "mock_interface_orchestrator_agent",
    
    # Task Reasoning Agent
    "task_reasoning_agent",
    "mock_task_reasoning_agent",
    
    # Validation & Safety Agent
    "validation_safety_agent",
    "mock_validation_safety_agent",
    
    # Response Formatter Agent
    "response_formatter_agent",
    "mock_response_formatter_agent",
    
    # Orchestrator Agent
    "orchestrator_agent",
    "mock_orchestrator_agent",
    
    # Visual Context Agent
    "visual_context_agent",
    "mock_visual_context_agent",
]