"""
Repository Analyzer Agent using AG2 Framework
Provides comprehensive structural analysis for downstream design agents
"""

import os
import ast
import json
import hashlib
import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# AG2 Framework imports
from autogen import ConversableAgent, LLMConfig

# Pydantic for structured outputs
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


# Pydantic models for comprehensive structural analysis
class FunctionSignature(BaseModel):
    """Function signature and metadata"""
    name: str = Field(..., description="Function name")
    file_path: str = Field(..., description="File path")
    line_number: int = Field(..., description="Line number")
    parameters: List[Dict[str, Any]] = Field(..., description="Parameter details")
    return_type: Optional[str] = Field(None, description="Return type annotation")
    is_async: bool = Field(False, description="Is async function")
    is_class_method: bool = Field(False, description="Is class method")
    decorators: List[str] = Field(..., description="Function decorators")
    docstring: Optional[str] = Field(None, description="Function docstring")
    complexity: int = Field(..., description="Cyclomatic complexity")
    calls: List[str] = Field(..., description="Functions this calls")
    called_by: List[str] = Field(..., description="Functions that call this")


class ClassDefinition(BaseModel):
    """Class definition and metadata"""
    name: str = Field(..., description="Class name")
    file_path: str = Field(..., description="File path")
    line_number: int = Field(..., description="Line number")
    base_classes: List[str] = Field(..., description="Base classes")
    decorators: List[str] = Field(..., description="Class decorators")
    docstring: Optional[str] = Field(None, description="Class docstring")
    methods: List[FunctionSignature] = Field(..., description="Class methods")
    attributes: List[Dict[str, Any]] = Field(..., description="Class attributes")
    imports: List[str] = Field(..., description="Classes this imports")


class ComponentDefinition(BaseModel):
    """System component definition"""
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type (API, Service, Model, etc.)")
    files: List[str] = Field(..., description="Files in this component")
    purpose: str = Field(..., description="Component purpose")
    interfaces: List[Dict[str, Any]] = Field(..., description="Public interfaces")
    dependencies: List[str] = Field(..., description="Component dependencies")
    functions: List[FunctionSignature] = Field(..., description="Key functions")


class DataModel(BaseModel):
    """Data model definition"""
    name: str = Field(..., description="Model name")
    file_path: str = Field(..., description="File path")
    fields: List[Dict[str, Any]] = Field(..., description="Model fields")
    relationships: List[Dict[str, Any]] = Field(..., description="Model relationships")
    validators: List[Dict[str, Any]] = Field(..., description="Validation rules")
    serializers: List[Dict[str, Any]] = Field(..., description="Serialization methods")


class APIContract(BaseModel):
    """API endpoint contract"""
    path: str = Field(..., description="API path")
    methods: List[str] = Field(..., description="HTTP methods")
    handler_function: str = Field(..., description="Handler function name")
    request_schema: Optional[str] = Field(None, description="Request schema")
    response_schema: Optional[str] = Field(None, description="Response schema")
    parameters: List[Dict[str, Any]] = Field(..., description="Path/query parameters")
    dependencies: List[str] = Field(..., description="Endpoint dependencies")


class DependencyGraph(BaseModel):
    """Dependency relationship graph"""
    functions: Dict[str, List[str]] = Field(..., description="Function call graph")
    classes: Dict[str, List[str]] = Field(..., description="Class inheritance graph")
    modules: Dict[str, List[str]] = Field(..., description="Module import graph")
    components: Dict[str, List[str]] = Field(..., description="Component dependency graph")


class RepositoryAnalysisOutput(BaseModel):
    """Complete repository analysis output for design agents"""
    system_architecture: Dict[str, Any] = Field(..., description="Overall system architecture")
    components: List[ComponentDefinition] = Field(..., description="System components")
    data_models: List[DataModel] = Field(..., description="Data models")
    api_contracts: List[APIContract] = Field(..., description="API contracts")
    function_registry: List[FunctionSignature] = Field(..., description="All functions")
    class_registry: List[ClassDefinition] = Field(..., description="All classes")
    dependency_graph: DependencyGraph = Field(..., description="Dependency relationships")
    code_quality_metrics: Dict[str, Any] = Field(..., description="Quality metrics")
    design_recommendations: List[Dict[str, Any]] = Field(..., description="Design recommendations")
    analysis_timestamp: str = Field(..., description="Analysis timestamp")


class RepositoryAnalyzerAgent:
    """
    Advanced Repository Analyzer Agent for Design Agent Integration
    
    Provides comprehensive structural analysis including:
    - Function interconnections and call graphs
    - Component dependencies and interfaces
    - Data model relationships
    - API contracts and schemas
    - Code quality and design recommendations
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM configuration
        self.llm_config = LLMConfig(
            config_list={
                "api_type": "openai",
                "model": model_name,
                "api_key": os.getenv("OPENAI_API_KEY"),
                "temperature": temperature
            }
        )
        
        # Create the repository analyzer agent
        self.analyzer_agent = ConversableAgent(
            name="repository_analyzer",
            system_message=self._get_analyzer_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.logger.info("Advanced Repository Analyzer Agent initialized")
    
    def _get_analyzer_system_message(self) -> str:
        """System message for the repository analyzer agent"""
        return """You are an Advanced Repository Analyzer Agent specialized in comprehensive codebase structural analysis.

Your role is to analyze codebases and provide detailed structural insights for downstream design agents.

You will receive:
1. Complete code structure analysis (functions, classes, dependencies)
2. Component mapping and relationships
3. Data model definitions
4. API contract information
5. Strategic code samples for context

Your task is to synthesize this information into a comprehensive structural analysis covering:

1. **System Architecture Analysis:**
   - Overall architectural pattern and style
   - Component organization and responsibilities
   - System boundaries and interfaces
   - Design principles and patterns used

2. **Component Deep Dive:**
   - Detailed component purposes and responsibilities
   - Public interfaces and APIs
   - Internal structure and organization
   - Dependencies and relationships

3. **Data Flow Analysis:**
   - How data flows through the system
   - Input/output transformations
   - State management patterns
   - Data validation and serialization

4. **API Contract Analysis:**
   - Endpoint definitions and contracts
   - Request/response schemas
   - Authentication and authorization
   - Error handling patterns

5. **Design Quality Assessment:**
   - Code organization and modularity
   - Separation of concerns
   - Design pattern usage
   - Areas for improvement

Provide your analysis in a structured JSON format optimized for design agents.
Focus on architectural insights, component relationships, and design recommendations."""

    def analyze_repository(self, repo_path: str, file_patterns: List[str] = None, 
                          analysis_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze repository with comprehensive structural analysis
        
        Args:
            repo_path: Path to repository to analyze
            file_patterns: File patterns to analyze
            analysis_config: Analysis configuration
            
        Returns:
            Comprehensive structural analysis for design agents
        """
        self.logger.info(f"Starting comprehensive repository analysis: {repo_path}")
        
        # Set default parameters
        if file_patterns is None:
            file_patterns = ["*.py", "*.java", "*.js", "*.md", "*.ts", "*.go", "*.rs"]
        
        if analysis_config is None:
            analysis_config = {
                "depth_level": "deep",
                "focus_areas": ["architecture", "components", "dependencies", "apis"],
                "include_comments": True,
                "include_docstrings": True
            }
        
        try:
            # Phase 1: Deep Code Structure Analysis
            print("🔍 Phase 1: Deep code structure analysis...")
            code_structure = self._analyze_code_structure(repo_path, file_patterns)
            
            # Phase 2: Component Mapping and Relationships
            print("🏗️  Phase 2: Component mapping and relationships...")
            component_map = self._map_components(code_structure)
            
            # Phase 3: Data Model Analysis
            print("📊 Phase 3: Data model analysis...")
            data_models = self._analyze_data_models(code_structure)
            
            # Phase 4: API Contract Analysis
            print("🌐 Phase 4: API contract analysis...")
            api_contracts = self._analyze_api_contracts(code_structure)
            
            # Phase 5: Dependency Graph Construction
            print("🔗 Phase 5: Dependency graph construction...")
            dependency_graph = self._build_dependency_graph(code_structure)
            
            # Phase 6: Quality Metrics Calculation
            print("📈 Phase 6: Quality metrics calculation...")
            quality_metrics = self._calculate_quality_metrics(code_structure)
            
            # Phase 7: Strategic Code Selection for LLM
            print("🎯 Phase 7: Strategic code selection for LLM analysis...")
            representative_code = self._select_representative_code(code_structure, component_map)
            
            # Phase 8: LLM Analysis with Focused Input
            print("🤖 Phase 8: LLM analysis with focused input...")
            llm_analysis = self._run_llm_analysis(
                code_structure, component_map, data_models, 
                api_contracts, dependency_graph, quality_metrics, 
                representative_code, analysis_config
            )
            
            # Phase 9: Generate Design Agent Ready Output
            print("📋 Phase 9: Generating design agent ready output...")
            structured_output = self._generate_design_ready_output(
                code_structure, component_map, data_models, api_contracts,
                dependency_graph, quality_metrics, llm_analysis
            )
            
            print("✅ Comprehensive repository analysis completed successfully!")
            return structured_output
            
        except Exception as e:
            self.logger.error(f"Error during comprehensive analysis: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "system_architecture": {},
                "components": [],
                "data_models": [],
                "api_contracts": [],
                "function_registry": [],
                "class_registry": [],
                "dependency_graph": {},
                "code_quality_metrics": {},
                "design_recommendations": []
            }
    
    def _analyze_code_structure(self, repo_path: str, file_patterns: List[str]) -> Dict[str, Any]:
        """Deep analysis of code structure using AST"""
        from .helpers import analyze_code_structure
        return analyze_code_structure(repo_path, file_patterns)
    
    def _map_components(self, code_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Map system components and their relationships"""
        from .helpers import map_components
        return map_components(code_structure)
    
    def _analyze_data_models(self, code_structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze data models and their relationships"""
        from .helpers import analyze_data_models
        return analyze_data_models(code_structure)
    
    def _analyze_api_contracts(self, code_structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze API contracts and endpoints"""
        from .helpers import analyze_api_contracts
        return analyze_api_contracts(code_structure)
    
    def _build_dependency_graph(self, code_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive dependency graph"""
        from .helpers import build_dependency_graph
        return build_dependency_graph(code_structure)
    
    def _calculate_quality_metrics(self, code_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive quality metrics"""
        from .helpers import calculate_quality_metrics
        return calculate_quality_metrics(code_structure)
    
    def _select_representative_code(self, code_structure: Dict[str, Any], 
                                   component_map: Dict[str, Any]) -> Dict[str, Any]:
        """Select representative code samples for LLM analysis"""
        from .helpers import select_representative_code
        return select_representative_code(code_structure, component_map)
    
    def _run_llm_analysis(self, code_structure: Dict[str, Any], component_map: Dict[str, Any],
                          data_models: List[Dict[str, Any]], api_contracts: List[Dict[str, Any]],
                          dependency_graph: Dict[str, Any], quality_metrics: Dict[str, Any],
                          representative_code: Dict[str, Any], analysis_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run LLM analysis with focused input"""
        from .helpers import create_comprehensive_analysis_prompt
        analysis_prompt = create_comprehensive_analysis_prompt(
            code_structure, component_map, data_models, api_contracts,
            dependency_graph, quality_metrics, representative_code, analysis_config
        )
        
        response = self.analyzer_agent.run(message=analysis_prompt, max_turns=1)
        response.process()
        
        return self._parse_llm_response(response.messages)
    
    def _parse_llm_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse LLM response and extract analysis"""
        try:
            if not messages:
                return {"error": "No response received from LLM"}
            
            last_message = messages[-1]
            content = last_message.get('content', '')
            
            # Try to extract JSON from the response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Failed to parse JSON from LLM response: {e}")
                    return {"error": f"JSON parsing failed: {e}"}
            else:
                return {"error": "No JSON found in LLM response"}
                
        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {str(e)}")
            return {"error": f"Response parsing failed: {str(e)}"}
    
    def _generate_design_ready_output(self, code_structure: Dict[str, Any], 
                                     component_map: Dict[str, Any], data_models: List[Dict[str, Any]],
                                     api_contracts: List[Dict[str, Any]], dependency_graph: Dict[str, Any],
                                     quality_metrics: Dict[str, Any], llm_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive output optimized for design agents"""
        try:
            # Create Pydantic models for structured output
            function_registry = [
                FunctionSignature(**func) for func in code_structure.get('functions', [])
            ]
            class_registry = [
                ClassDefinition(**cls) for cls in code_structure.get('classes', [])
            ]
            
            components = [
                ComponentDefinition(**comp) for comp in component_map.get('components', [])
            ]
            
            data_models_structured = [
                DataModel(**model) for model in data_models
            ]
            
            api_contracts_structured = [
                APIContract(**contract) for contract in api_contracts
            ]
            
            dependency_graph_structured = DependencyGraph(**dependency_graph)
            
            # Generate design recommendations
            design_recommendations = self._generate_design_recommendations(
                quality_metrics, llm_analysis, component_map
            )
            
            # Create comprehensive output
            output = RepositoryAnalysisOutput(
                system_architecture=llm_analysis.get('system_architecture', {}),
                components=components,
                data_models=data_models_structured,
                api_contracts=api_contracts_structured,
                function_registry=function_registry,
                class_registry=class_registry,
                dependency_graph=dependency_graph_structured,
                code_quality_metrics=quality_metrics,
                design_recommendations=design_recommendations,
                analysis_timestamp=datetime.now().isoformat()
            )
            
            return output.model_dump()
            
        except Exception as e:
            self.logger.error(f"Error generating design ready output: {str(e)}")
            return {
                "error": f"Output generation failed: {str(e)}",
                "system_architecture": {},
                "components": [],
                "data_models": [],
                "api_contracts": [],
                "function_registry": [],
                "class_registry": [],
                "dependency_graph": {},
                "code_quality_metrics": {},
                "design_recommendations": []
            }
    
    def _generate_design_recommendations(self, quality_metrics: Dict[str, Any], 
                                        llm_analysis: Dict[str, Any], 
                                        component_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate design recommendations based on analysis"""
        recommendations = []
        
        # Quality-based recommendations
        if quality_metrics.get('average_complexity', 0) > 10:
            recommendations.append({
                "area": "Code Complexity",
                "issue": "High average complexity",
                "recommendation": "Refactor complex functions into smaller, focused functions",
                "priority": "high"
            })
        
        if quality_metrics.get('documentation_coverage', 0) < 0.7:
            recommendations.append({
                "area": "Documentation",
                "issue": "Low documentation coverage",
                "recommendation": "Add comprehensive docstrings and API documentation",
                "priority": "medium"
            })
        
        # Architecture-based recommendations
        if llm_analysis.get('system_architecture', {}).get('pattern') == 'Unknown':
            recommendations.append({
                "area": "Architecture",
                "issue": "Unclear architectural pattern",
                "recommendation": "Define and implement a clear architectural pattern",
                "priority": "high"
            })
        
        return recommendations