"""
Base schemas for all agents in Workflow 1
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    """Status of agent execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BaseAgentOutput(BaseModel):
    """Base output schema for all agents"""
    
    agent_name: str = Field(..., description="Name of the agent that generated this output")
    execution_id: str = Field(..., description="Unique execution identifier")
    status: AgentStatus = Field(..., description="Current status of the agent")
    timestamp: datetime = Field(default_factory=datetime.now, description="When this output was generated")
    execution_time_seconds: Optional[float] = Field(None, description="Time taken to execute in seconds")
    error_message: Optional[str] = Field(None, description="Error message if execution failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentCapability(BaseModel):
    """Describes what an agent can do"""
    
    name: str = Field(..., description="Name of the capability")
    description: str = Field(..., description="What this capability does")
    input_types: List[str] = Field(..., description="Types of inputs this capability accepts")
    output_types: List[str] = Field(..., description="Types of outputs this capability produces")
    dependencies: List[str] = Field(default_factory=list, description="Other capabilities this depends on")


class AgentConfig(BaseModel):
    """Configuration for an agent"""
    
    name: str = Field(..., description="Agent name")
    version: str = Field(default="1.0.0", description="Agent version")
    capabilities: List[AgentCapability] = Field(..., description="What this agent can do")
    max_execution_time: int = Field(default=3600, description="Maximum execution time in seconds")
    retry_count: int = Field(default=3, description="Number of retries on failure")
    timeout: int = Field(default=300, description="Timeout for individual operations in seconds")
    enabled: bool = Field(default=True, description="Whether this agent is enabled")