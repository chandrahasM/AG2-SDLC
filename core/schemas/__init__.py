"""
Core data schemas for Workflow 1
"""

from .base import BaseAgentOutput, AgentStatus
from .workflow_input import WorkflowInput, RepositoryConfig, AnalysisConfig, DocumentationConfig
from .workflow_output import WorkflowOutput, FinalDesignDocument

__all__ = [
    "BaseAgentOutput",
    "AgentStatus", 
    "WorkflowInput",
    "RepositoryConfig",
    "AnalysisConfig",
    "DocumentationConfig",
    "WorkflowOutput",
    "FinalDesignDocument"
]