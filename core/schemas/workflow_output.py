"""
Output schemas for Workflow 1
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from .base import BaseAgentOutput


class RepositoryAnalysisOutput(BaseAgentOutput):
    """Output from Repository Analyzer Agent"""
    
    repo_metadata: Dict[str, Any] = Field(..., description="Repository metadata and statistics")
    architecture_analysis: Dict[str, Any] = Field(..., description="Architectural patterns and structure")
    code_quality_metrics: Dict[str, Any] = Field(..., description="Code quality metrics and analysis")
    detected_patterns: List[Dict[str, Any]] = Field(..., description="Detected design patterns and conventions")
    file_structure: Dict[str, Any] = Field(..., description="File and directory structure analysis")
    dependencies: Dict[str, Any] = Field(..., description="Internal and external dependencies")


class DocumentationSynthesisOutput(BaseAgentOutput):
    """Output from Documentation Synthesizer Agent"""
    
    documentation_accuracy_score: float = Field(..., ge=0.0, le=1.0, description="Accuracy score of existing documentation")
    major_discrepancies: List[Dict[str, Any]] = Field(..., description="Major discrepancies between code and docs")
    undocumented_features: List[Dict[str, Any]] = Field(..., description="Features present in code but not documented")
    reconciliation_notes: Dict[str, Any] = Field(..., description="Notes on reconciling code and documentation")
    existing_docs_analysis: Dict[str, Any] = Field(..., description="Analysis of existing documentation")


class DesignArchitectOutput(BaseAgentOutput):
    """Output from Design Architect Agent"""
    
    system_overview: str = Field(..., description="Comprehensive system overview")
    architecture_diagram: str = Field(..., description="Text-based architecture diagram")
    component_specifications: List[Dict[str, Any]] = Field(..., description="Detailed component specifications")
    api_documentation: Dict[str, Any] = Field(..., description="API interfaces and contracts")
    data_flow_diagrams: List[str] = Field(..., description="Data flow diagrams")
    design_principles: List[str] = Field(..., description="Identified design principles")


class TestAnalysisOutput(BaseAgentOutput):
    """Output from Test Analyst Agent"""
    
    test_coverage_analysis: Dict[str, Any] = Field(..., description="Test coverage analysis")
    testing_gaps: List[Dict[str, Any]] = Field(..., description="Identified testing gaps")
    proposed_test_strategy: Dict[str, Any] = Field(..., description="Proposed test strategy improvements")
    manual_test_scenarios: List[Dict[str, Any]] = Field(..., description="Generated manual test scenarios")
    test_quality_metrics: Dict[str, Any] = Field(..., description="Test quality metrics")


class DevOpsDesignOutput(BaseAgentOutput):
    """Output from DevOps Designer Agent"""
    
    deployment_architecture: str = Field(..., description="Deployment architecture description")
    infrastructure_design: Dict[str, Any] = Field(..., description="Infrastructure design specifications")
    operational_requirements: List[Dict[str, Any]] = Field(..., description="Operational requirements")
    monitoring_strategy: Dict[str, Any] = Field(..., description="Monitoring and alerting strategy")
    deployment_patterns: List[Dict[str, Any]] = Field(..., description="Identified deployment patterns")


class QAValidationOutput(BaseAgentOutput):
    """Output from QA Validator Agent"""
    
    clarification_questions: List[Dict[str, Any]] = Field(..., description="Generated clarification questions")
    validation_points: List[Dict[str, Any]] = Field(..., description="Validation points for human review")
    confidence_scores: Dict[str, float] = Field(..., description="Confidence scores for different areas")
    priority_areas: List[Dict[str, Any]] = Field(..., description="Areas requiring priority attention")
    consistency_check_results: Dict[str, Any] = Field(..., description="Consistency check results")


class FinalDesignDocument(BaseModel):
    """Final comprehensive design document"""
    
    document_id: str = Field(..., description="Unique document identifier")
    generated_at: datetime = Field(default_factory=datetime.now, description="When document was generated")
    workflow_execution_id: str = Field(..., description="Associated workflow execution ID")
    
    # Executive Summary
    executive_summary: str = Field(..., description="Executive summary of the system")
    
    # System Overview
    system_overview: str = Field(..., description="Comprehensive system overview")
    architecture_diagram: str = Field(..., description="System architecture diagram")
    
    # Technical Details
    component_specifications: List[Dict[str, Any]] = Field(..., description="Component specifications")
    api_documentation: Dict[str, Any] = Field(..., description="API documentation")
    data_flow_diagrams: List[str] = Field(..., description="Data flow diagrams")
    
    # Quality and Testing
    code_quality_metrics: Dict[str, Any] = Field(..., description="Code quality metrics")
    test_strategy: Dict[str, Any] = Field(..., description="Test strategy and coverage")
    
    # Operations
    deployment_architecture: str = Field(..., description="Deployment architecture")
    operational_requirements: List[Dict[str, Any]] = Field(..., description="Operational requirements")
    
    # Validation and Gaps
    documentation_gaps: List[Dict[str, Any]] = Field(..., description="Identified documentation gaps")
    validation_questions: List[Dict[str, Any]] = Field(..., description="Questions for human validation")
    
    # Metadata
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score")
    agent_outputs: Dict[str, BaseAgentOutput] = Field(..., description="Individual agent outputs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class WorkflowOutput(BaseModel):
    """Final output from Workflow 1"""
    
    workflow_name: str = Field(..., description="Name of the workflow")
    execution_id: str = Field(..., description="Execution identifier")
    status: str = Field(..., description="Overall workflow status")
    started_at: datetime = Field(..., description="When workflow started")
    completed_at: Optional[datetime] = Field(None, description="When workflow completed")
    total_execution_time: Optional[float] = Field(None, description="Total execution time in seconds")
    
    # Agent outputs
    repository_analysis: Optional[RepositoryAnalysisOutput] = Field(None, description="Repository analysis results")
    documentation_synthesis: Optional[DocumentationSynthesisOutput] = Field(None, description="Documentation synthesis results")
    design_architect: Optional[DesignArchitectOutput] = Field(None, description="Design architect results")
    test_analysis: Optional[TestAnalysisOutput] = Field(None, description="Test analysis results")
    devops_design: Optional[DevOpsDesignOutput] = Field(None, description="DevOps design results")
    qa_validation: Optional[QAValidationOutput] = Field(None, description="QA validation results")
    
    # Final document
    final_design_document: Optional[FinalDesignDocument] = Field(None, description="Final comprehensive design document")
    
    # Summary
    summary: Dict[str, Any] = Field(..., description="Workflow execution summary")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    warnings: List[str] = Field(default_factory=list, description="Any warnings generated")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }