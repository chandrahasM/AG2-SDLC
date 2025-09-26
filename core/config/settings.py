"""
Settings and configuration for Workflow 1
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from .agent_config import (
    RepositoryAnalyzerConfig, DocumentationSynthesizerConfig,
    DesignArchitectConfig, TestAnalystConfig, DevOpsDesignerConfig,
    QAValidatorConfig
)


class OrchestratorConfig(BaseModel):
    """Configuration for the workflow orchestrator"""
    
    max_parallel_agents: int = Field(default=4, description="Maximum number of agents to run in parallel")
    agent_timeout: int = Field(default=3600, description="Default timeout for agent execution in seconds")
    retry_delay: int = Field(default=5, description="Delay between retries in seconds")
    log_level: str = Field(default="INFO", description="Logging level")
    output_directory: str = Field(default="./data/outputs", description="Output directory for results")
    intermediate_outputs: bool = Field(default=True, description="Save intermediate outputs")
    cleanup_on_completion: bool = Field(default=False, description="Clean up intermediate files on completion")


class WorkflowConfig(BaseModel):
    """Main workflow configuration"""
    
    workflow_name: str = Field(default="code-to-design", description="Workflow name")
    version: str = Field(default="1.0.0", description="Workflow version")
    description: str = Field(default="Reverse-engineer design documentation from codebase", description="Workflow description")
    
    # Orchestrator configuration
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
    
    # Agent configurations
    repository_analyzer: RepositoryAnalyzerConfig = Field(default_factory=RepositoryAnalyzerConfig)
    documentation_synthesizer: DocumentationSynthesizerConfig = Field(default_factory=DocumentationSynthesizerConfig)
    design_architect: DesignArchitectConfig = Field(default_factory=DesignArchitectConfig)
    test_analyst: TestAnalystConfig = Field(default_factory=TestAnalystConfig)
    devops_designer: DevOpsDesignerConfig = Field(default_factory=DevOpsDesignerConfig)
    qa_validator: QAValidatorConfig = Field(default_factory=QAValidatorConfig)
    
    # Global settings
    llm_model: str = Field(default="gpt-4", description="LLM model to use")
    llm_temperature: float = Field(default=0.1, description="LLM temperature setting")
    max_tokens: int = Field(default=4000, description="Maximum tokens for LLM responses")
    
    # File processing settings
    max_file_size_mb: int = Field(default=10, description="Maximum file size to process in MB")
    supported_languages: List[str] = Field(
        default=["python", "javascript", "typescript", "java", "go", "rust", "csharp", "php"],
        description="Supported programming languages"
    )
    
    # Output settings
    output_formats: List[str] = Field(
        default=["markdown", "json", "html"],
        description="Supported output formats"
    )
    include_diagrams: bool = Field(default=True, description="Include diagrams in output")
    diagram_formats: List[str] = Field(
        default=["text", "mermaid", "plantuml"],
        description="Supported diagram formats"
    )
    
    # Validation settings
    validation_enabled: bool = Field(default=True, description="Enable validation")
    confidence_threshold: float = Field(default=0.7, description="Minimum confidence threshold")
    auto_retry_failed_agents: bool = Field(default=True, description="Automatically retry failed agents")
    
    # Performance settings
    enable_caching: bool = Field(default=True, description="Enable result caching")
    cache_ttl_hours: int = Field(default=24, description="Cache time-to-live in hours")
    max_memory_usage_mb: int = Field(default=2048, description="Maximum memory usage in MB")
    
    class Config:
        schema_extra = {
            "example": {
                "workflow_name": "code-to-design",
                "version": "1.0.0",
                "orchestrator": {
                    "max_parallel_agents": 4,
                    "agent_timeout": 3600,
                    "log_level": "INFO"
                },
                "repository_analyzer": {
                    "max_file_size_mb": 10,
                    "include_comments": True
                },
                "llm_model": "gpt-4",
                "llm_temperature": 0.1
            }
        }


class EnvironmentConfig(BaseModel):
    """Environment-specific configuration"""
    
    environment: str = Field(default="development", description="Environment name")
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    log_file: Optional[str] = Field(None, description="Log file path")
    database_url: Optional[str] = Field(None, description="Database connection URL")
    redis_url: Optional[str] = Field(None, description="Redis connection URL")
    api_keys: Dict[str, str] = Field(default_factory=dict, description="API keys for external services")
    
    # AG2 specific settings
    ag2_api_url: Optional[str] = Field(None, description="AG2 API URL")
    ag2_api_key: Optional[str] = Field(None, description="AG2 API key")
    ag2_workspace_id: Optional[str] = Field(None, description="AG2 workspace ID")
    
    # External service settings
    github_token: Optional[str] = Field(None, description="GitHub API token")
    gitlab_token: Optional[str] = Field(None, description="GitLab API token")
    confluence_url: Optional[str] = Field(None, description="Confluence URL")
    confluence_token: Optional[str] = Field(None, description="Confluence API token")


def load_config(config_path: Optional[str] = None) -> WorkflowConfig:
    """
    Load configuration from file or use defaults
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        WorkflowConfig instance
    """
    if config_path:
        # In a real implementation, this would load from YAML/JSON file
        pass
    
    return WorkflowConfig()


def load_environment_config(env_path: Optional[str] = None) -> EnvironmentConfig:
    """
    Load environment configuration from file or environment variables
    
    Args:
        env_path: Path to environment configuration file
        
    Returns:
        EnvironmentConfig instance
    """
    import os
    
    return EnvironmentConfig(
        environment=os.getenv("ENVIRONMENT", "development"),
        debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
        log_file=os.getenv("LOG_FILE"),
        database_url=os.getenv("DATABASE_URL"),
        redis_url=os.getenv("REDIS_URL"),
        ag2_api_url=os.getenv("AG2_API_URL"),
        ag2_api_key=os.getenv("AG2_API_KEY"),
        ag2_workspace_id=os.getenv("AG2_WORKSPACE_ID"),
        github_token=os.getenv("GITHUB_TOKEN"),
        gitlab_token=os.getenv("GITLAB_TOKEN"),
        confluence_url=os.getenv("CONFLUENCE_URL"),
        confluence_token=os.getenv("CONFLUENCE_TOKEN")
    )