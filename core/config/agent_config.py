"""
Agent configuration for Workflow 1
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from ..schemas.base import AgentCapability


class AgentConfig(BaseModel):
    """Configuration for individual agents"""
    
    name: str = Field(..., description="Agent name")
    version: str = Field(default="1.0.0", description="Agent version")
    enabled: bool = Field(default=True, description="Whether agent is enabled")
    max_execution_time: int = Field(default=3600, description="Maximum execution time in seconds")
    retry_count: int = Field(default=3, description="Number of retries on failure")
    timeout: int = Field(default=300, description="Timeout for individual operations in seconds")
    capabilities: List[AgentCapability] = Field(default_factory=list, description="Agent capabilities")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Agent-specific parameters")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "repository_analyzer",
                "version": "1.0.0",
                "enabled": True,
                "max_execution_time": 1800,
                "retry_count": 3,
                "timeout": 300,
                "capabilities": [
                    {
                        "name": "file_analysis",
                        "description": "Analyze file structure and content",
                        "input_types": ["file_path"],
                        "output_types": ["analysis_result"]
                    }
                ],
                "parameters": {
                    "max_file_size_mb": 10,
                    "include_comments": True
                }
            }
        }


class RepositoryAnalyzerConfig(AgentConfig):
    """Configuration for Repository Analyzer Agent"""
    
    name: str = Field(default="repository_analyzer", description="Agent name")
    max_file_size_mb: int = Field(default=10, description="Maximum file size to analyze in MB")
    include_comments: bool = Field(default=True, description="Include code comments in analysis")
    include_docstrings: bool = Field(default=True, description="Include docstrings in analysis")
    analyze_test_files: bool = Field(default=True, description="Analyze test files separately")
    generate_metrics: bool = Field(default=True, description="Generate code quality metrics")
    language_specific: bool = Field(default=True, description="Use language-specific analysis")


class DocumentationSynthesizerConfig(AgentConfig):
    """Configuration for Documentation Synthesizer Agent"""
    
    name: str = Field(default="documentation_synthesizer", description="Agent name")
    include_markdown: bool = Field(default=True, description="Include markdown files in analysis")
    include_confluence: bool = Field(default=False, description="Include Confluence exports")
    include_notion: bool = Field(default=False, description="Include Notion exports")
    similarity_threshold: float = Field(default=0.7, description="Similarity threshold for document matching")
    gap_analysis_depth: int = Field(default=3, description="Depth of gap analysis")


class DesignArchitectConfig(AgentConfig):
    """Configuration for Design Architect Agent"""
    
    name: str = Field(default="design_architect", description="Agent name")
    include_diagrams: bool = Field(default=True, description="Include diagrams in output")
    diagram_format: str = Field(default="text", description="Diagram format (text, mermaid, etc.)")
    template_path: Optional[str] = Field(None, description="Path to custom templates")
    output_format: str = Field(default="markdown", description="Output format for documents")
    detail_level: str = Field(default="comprehensive", description="Level of detail (basic, detailed, comprehensive)")


class TestAnalystConfig(AgentConfig):
    """Configuration for Test Analyst Agent"""
    
    name: str = Field(default="test_analyst", description="Agent name")
    analyze_coverage: bool = Field(default=True, description="Analyze test coverage")
    generate_scenarios: bool = Field(default=True, description="Generate manual test scenarios")
    include_performance_tests: bool = Field(default=True, description="Include performance test analysis")
    test_framework_detection: bool = Field(default=True, description="Detect test frameworks")


class DevOpsDesignerConfig(AgentConfig):
    """Configuration for DevOps Designer Agent"""
    
    name: str = Field(default="devops_designer", description="Agent name")
    analyze_logs: bool = Field(default=True, description="Analyze deployment and system logs")
    detect_infrastructure: bool = Field(default=True, description="Detect infrastructure patterns")
    generate_monitoring: bool = Field(default=True, description="Generate monitoring strategies")
    include_security: bool = Field(default=True, description="Include security considerations")


class QAValidatorConfig(AgentConfig):
    """Configuration for QA Validator Agent"""
    
    name: str = Field(default="qa_validator", description="Agent name")
    generate_questions: bool = Field(default=True, description="Generate clarification questions")
    validate_consistency: bool = Field(default=True, description="Validate document consistency")
    assess_confidence: bool = Field(default=True, description="Assess confidence scores")
    prioritize_issues: bool = Field(default=True, description="Prioritize validation issues")
    question_count_limit: int = Field(default=20, description="Maximum number of questions to generate")