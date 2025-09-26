"""
Prompt management for Workflow 1 agents
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class PromptTemplate(BaseModel):
    """Template for agent prompts"""
    
    name: str = Field(..., description="Prompt template name")
    description: str = Field(..., description="Description of what this prompt does")
    template: str = Field(..., description="Prompt template with placeholders")
    variables: List[str] = Field(default_factory=list, description="Required variables for this template")
    category: str = Field(default="general", description="Category of the prompt")


class PromptManager:
    """Manages prompts for all agents in Workflow 1"""
    
    def __init__(self):
        self.prompts: Dict[str, PromptTemplate] = {}
        self._initialize_default_prompts()
    
    def _initialize_default_prompts(self):
        """Initialize default prompts for all agents"""
        
        # Repository Analyzer prompts
        self.prompts["repo_analyze_structure"] = PromptTemplate(
            name="repo_analyze_structure",
            description="Analyze repository structure and architecture",
            template="""
Analyze the following codebase structure and identify architectural patterns:

Repository Path: {repo_path}
File Structure: {file_structure}
File Patterns: {file_patterns}

Please provide:
1. Overall architecture pattern (MVC, microservices, monolithic, etc.)
2. Key components and their relationships
3. Entry points and main modules
4. Configuration and setup files
5. Test structure and organization

Focus on understanding the system's design and organization.
            """,
            variables=["repo_path", "file_structure", "file_patterns"],
            category="repository_analysis"
        )
        
        self.prompts["repo_analyze_dependencies"] = PromptTemplate(
            name="repo_analyze_dependencies",
            description="Analyze code dependencies and relationships",
            template="""
Analyze the dependencies and relationships in this codebase:

Code Files: {code_files}
Import/Require Statements: {imports}
Package Files: {package_files}

Please identify:
1. External dependencies and their purposes
2. Internal module dependencies
3. Circular dependencies (if any)
4. Critical dependencies that could affect system stability
5. Version constraints and compatibility issues

Provide a dependency graph and analysis of the system's coupling.
            """,
            variables=["code_files", "imports", "package_files"],
            category="repository_analysis"
        )
        
        # Documentation Synthesizer prompts
        self.prompts["doc_analyze_gaps"] = PromptTemplate(
            name="doc_analyze_gaps",
            description="Analyze gaps between code and documentation",
            template="""
Compare the actual codebase with existing documentation to identify gaps:

Code Analysis: {code_analysis}
Existing Documentation: {existing_docs}
Documentation Types: {doc_types}

Please identify:
1. Features implemented in code but not documented
2. Documentation that doesn't match the actual implementation
3. Missing documentation for key components
4. Outdated documentation sections
5. Inconsistencies between different documentation sources

Provide a gap analysis with priority levels and recommendations.
            """,
            variables=["code_analysis", "existing_docs", "doc_types"],
            category="documentation_synthesis"
        )
        
        # Design Architect prompts
        self.prompts["design_generate_architecture"] = PromptTemplate(
            name="design_generate_architecture",
            description="Generate comprehensive system architecture documentation",
            template="""
Based on the codebase analysis, generate comprehensive architecture documentation:

Repository Analysis: {repo_analysis}
Documentation Gaps: {doc_gaps}
Test Analysis: {test_analysis}
DevOps Analysis: {devops_analysis}

Please create:
1. System overview and purpose
2. High-level architecture diagram (text-based)
3. Component specifications with responsibilities
4. Data flow diagrams
5. API documentation and interfaces
6. Design principles and patterns used
7. Scalability and performance considerations

Ensure the documentation is comprehensive and accurate to the actual implementation.
            """,
            variables=["repo_analysis", "doc_gaps", "test_analysis", "devops_analysis"],
            category="design_architecture"
        )
        
        # Test Analyst prompts
        self.prompts["test_analyze_coverage"] = PromptTemplate(
            name="test_analyze_coverage",
            description="Analyze test coverage and quality",
            template="""
Analyze the testing strategy and coverage for this codebase:

Code Structure: {code_structure}
Test Files: {test_files}
Test Results: {test_results}
Coverage Reports: {coverage_reports}

Please provide:
1. Test coverage analysis by component
2. Testing gaps and missing test scenarios
3. Test quality assessment
4. Recommendations for improving test strategy
5. Manual test scenarios for areas not covered by automated tests
6. Performance and integration testing recommendations

Focus on identifying areas that need better test coverage.
            """,
            variables=["code_structure", "test_files", "test_results", "coverage_reports"],
            category="test_analysis"
        )
        
        # DevOps Designer prompts
        self.prompts["devops_analyze_deployment"] = PromptTemplate(
            name="devops_analyze_deployment",
            description="Analyze deployment and infrastructure requirements",
            template="""
Analyze the deployment and operational requirements for this system:

Code Analysis: {code_analysis}
Configuration Files: {config_files}
Log Files: {log_files}
Infrastructure Files: {infra_files}

Please provide:
1. Deployment architecture and requirements
2. Infrastructure design recommendations
3. Operational requirements and procedures
4. Monitoring and alerting strategy
5. Security considerations
6. Scalability and performance requirements
7. Disaster recovery and backup strategies

Focus on practical deployment and operational aspects.
            """,
            variables=["code_analysis", "config_files", "log_files", "infra_files"],
            category="devops_design"
        )
        
        # QA Validator prompts
        self.prompts["qa_generate_questions"] = PromptTemplate(
            name="qa_generate_questions",
            description="Generate validation questions and identify areas needing clarification",
            template="""
Based on the comprehensive analysis, generate validation questions and identify areas needing clarification:

Repository Analysis: {repo_analysis}
Documentation Synthesis: {doc_synthesis}
Design Architecture: {design_arch}
Test Analysis: {test_analysis}
DevOps Design: {devops_design}

Please generate:
1. Clarification questions for ambiguous areas
2. Validation points for human review
3. Confidence scores for different analysis areas
4. Priority areas requiring immediate attention
5. Consistency checks across all analyses
6. Recommendations for improving the analysis

Focus on areas where human expertise is needed for validation.
            """,
            variables=["repo_analysis", "doc_synthesis", "design_arch", "test_analysis", "devops_design"],
            category="qa_validation"
        )
    
    def get_prompt(self, prompt_name: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name"""
        return self.prompts.get(prompt_name)
    
    def get_prompts_by_category(self, category: str) -> List[PromptTemplate]:
        """Get all prompts in a category"""
        return [prompt for prompt in self.prompts.values() if prompt.category == category]
    
    def format_prompt(self, prompt_name: str, variables: Dict[str, Any]) -> str:
        """
        Format a prompt template with variables
        
        Args:
            prompt_name: Name of the prompt template
            variables: Variables to substitute in the template
            
        Returns:
            Formatted prompt string
        """
        prompt = self.get_prompt(prompt_name)
        if not prompt:
            raise ValueError(f"Prompt template '{prompt_name}' not found")
        
        try:
            return prompt.template.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing required variable for prompt '{prompt_name}': {e}")
    
    def add_custom_prompt(self, prompt: PromptTemplate):
        """Add a custom prompt template"""
        self.prompts[prompt.name] = prompt
    
    def list_prompts(self) -> List[str]:
        """List all available prompt names"""
        return list(self.prompts.keys())
    
    def validate_prompt_variables(self, prompt_name: str, variables: Dict[str, Any]) -> List[str]:
        """
        Validate that all required variables are provided
        
        Args:
            prompt_name: Name of the prompt template
            variables: Variables to validate
            
        Returns:
            List of missing variables
        """
        prompt = self.get_prompt(prompt_name)
        if not prompt:
            return [f"Prompt template '{prompt_name}' not found"]
        
        missing_vars = []
        for var in prompt.variables:
            if var not in variables:
                missing_vars.append(var)
        
        return missing_vars