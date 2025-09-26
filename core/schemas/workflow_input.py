"""
Input schemas for Workflow 1
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator
from pathlib import Path


class RepositoryConfig(BaseModel):
    """Configuration for repository analysis"""
    
    local_path: str = Field(..., description="Local file path to code repository")
    file_patterns: List[str] = Field(
        default=["*.py", "*.java", "*.js", "*.ts", "*.md", "*.json", "*.yaml", "*.yml"],
        description="File patterns to analyze"
    )
    exclude_patterns: List[str] = Field(
        default=["**/node_modules/**", "**/__pycache__/**", "**/.git/**", "**/venv/**", "**/env/**"],
        description="Patterns to exclude from analysis"
    )
    max_file_size_mb: int = Field(default=10, description="Maximum file size to analyze in MB")
    depth_level: int = Field(default=10, description="Maximum directory depth to analyze")
    
    @validator('local_path')
    def validate_path(cls, v):
        path = Path(v)
        if not path.exists():
            raise ValueError(f"Repository path does not exist: {v}")
        if not path.is_dir():
            raise ValueError(f"Repository path is not a directory: {v}")
        return str(path.absolute())


class AnalysisConfig(BaseModel):
    """Configuration for analysis parameters"""
    
    focus_areas: List[str] = Field(
        default=["architecture", "dependencies", "patterns", "quality", "testing"],
        description="Areas to focus analysis on"
    )
    include_comments: bool = Field(default=True, description="Include code comments in analysis")
    include_docstrings: bool = Field(default=True, description="Include docstrings in analysis")
    analyze_test_files: bool = Field(default=True, description="Analyze test files separately")
    generate_metrics: bool = Field(default=True, description="Generate code quality metrics")
    language_specific: bool = Field(default=True, description="Use language-specific analysis")


class DocumentationConfig(BaseModel):
    """Configuration for existing documentation analysis"""
    
    design_docs_path: Optional[str] = Field(None, description="Path to existing design documents folder")
    requirements_docs_path: Optional[str] = Field(None, description="Path to existing requirements documents folder")
    include_markdown: bool = Field(default=True, description="Include markdown files in analysis")
    include_confluence: bool = Field(default=False, description="Include Confluence exports")
    include_notion: bool = Field(default=False, description="Include Notion exports")
    
    @validator('design_docs_path', 'requirements_docs_path')
    def validate_doc_paths(cls, v):
        if v is not None:
            path = Path(v)
            if not path.exists():
                raise ValueError(f"Documentation path does not exist: {v}")
            if not path.is_dir():
                raise ValueError(f"Documentation path is not a directory: {v}")
        return v


class WorkflowInput(BaseModel):
    """Main input schema for Workflow 1"""
    
    workflow_name: str = Field(default="code-to-design", description="Name of the workflow")
    execution_id: str = Field(..., description="Unique execution identifier")
    repository: RepositoryConfig = Field(..., description="Repository configuration")
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig, description="Analysis configuration")
    documentation: DocumentationConfig = Field(default_factory=DocumentationConfig, description="Documentation configuration")
    output_format: str = Field(default="markdown", description="Output format for generated documents")
    include_diagrams: bool = Field(default=True, description="Include diagrams in output")
    parallel_execution: bool = Field(default=True, description="Run agents in parallel where possible")
    custom_prompts: Dict[str, str] = Field(default_factory=dict, description="Custom prompts for specific agents")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "workflow_name": "code-to-design",
                "execution_id": "exec_2024_001",
                "repository": {
                    "local_path": "/path/to/my/project",
                    "file_patterns": ["*.py", "*.js", "*.md"],
                    "depth_level": 5
                },
                "analysis": {
                    "focus_areas": ["architecture", "dependencies"],
                    "include_comments": True
                },
                "documentation": {
                    "design_docs_path": "/path/to/design/docs",
                    "requirements_docs_path": "/path/to/requirements"
                }
            }
        }