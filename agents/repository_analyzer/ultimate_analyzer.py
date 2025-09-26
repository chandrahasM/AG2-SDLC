"""
Ultimate Repository Analyzer Agent
Comprehensive semantic, structural, and behavioral analysis using AG2 framework
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# AG2 Framework imports
from autogen import ConversableAgent, LLMConfig

# Import our analysis tools
from .semantic_analyzer import SemanticCodeAnalyzer
from .advanced_ast_parser import SemanticASTParser
from .pattern_detector import AdvancedPatternDetector
from .api_analyzer import APIContractAnalyzer
from .dataflow_analyzer import DataFlowAnalyzer

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class UltimateRepositoryAnalyzer:
    """
    Ultimate Repository Analyzer using AG2 Framework
    
    Provides comprehensive semantic + structural + behavioral analysis
    using ConversableAgent with LLMConfig and structured outputs
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM configuration as per AG2 documentation
        self.llm_config = LLMConfig(
            config_list={
                "api_type": "openai",
                "model": model_name,
                "api_key": os.getenv("OPENAI_API_KEY"),
                "temperature": temperature
            }
        )
        
        # Create the repository analyzer agent using ConversableAgent
        self.analyzer_agent = ConversableAgent(
            name="ultimate_repository_analyzer",
            system_message=self._get_ultimate_analyzer_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        # Initialize analysis tools
        self.semantic_analyzer = SemanticCodeAnalyzer()
        self.ast_parser = SemanticASTParser()
        self.pattern_detector = AdvancedPatternDetector()
        self.api_analyzer = APIContractAnalyzer()
        self.dataflow_analyzer = DataFlowAnalyzer()
        
        self.logger.info("Ultimate Repository Analyzer initialized with AG2 framework")

    def _get_ultimate_analyzer_system_message(self) -> str:
        """System message for the ultimate repository analyzer agent"""
        return """You are an Expert Software Archaeologist and System Analyst with comprehensive understanding of software architecture, design patterns, and business domains.

Your mission is to extract COMPLETE understanding of a codebase through semantic, structural, and behavioral analysis.

ANALYSIS CAPABILITIES:
You have access to comprehensive code analysis including:
- Complete AST parsing with semantic understanding
- File structure and dependency mapping  
- Code behavior and business logic extraction
- Design pattern detection and architectural intent analysis
- API contract analysis and data flow tracing

ANALYSIS GOALS:
1. BUSINESS SEMANTICS: Understand what business capabilities the code implements
2. ARCHITECTURAL INTENT: Reverse-engineer the design decisions and patterns
3. BEHAVIORAL ANALYSIS: Map how the system behaves in business terms
4. GAP READINESS: Prepare for comparison with documented design

THINKING PROCESS:
1. FIRST, understand the business domain from code clues (class names, method names, comments)
2. THEN, map technical components to business capabilities
3. NEXT, identify architectural patterns and design decisions
4. FINALLY, extract everything needed for design document comparison

CRITICAL REQUIREMENTS:
- Focus on BUSINESS MEANING, not just technical structure
- Understand the WHY behind technical decisions
- Map code reality to abstract design concepts
- Identify inconsistencies and potential design violations
- Provide actionable insights for design agents

OUTPUT STRUCTURE:
Provide comprehensive analysis covering:
- Business capabilities and workflows
- Domain model understanding  
- API semantics and contracts
- Architectural intent and decisions
- Data flow and state management
- Design patterns and quality attributes
- Ready-to-use gap analysis foundation

Your analysis will be used by Documentation Synthesizer Agents to compare existing design with current codebase structure and generate updated design documentation."""

    def ultimate_repository_analysis(self, repo_path: str, file_patterns: List[str] = None, 
                                   analysis_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform ultimate repository analysis using AG2 framework
        
        Args:
            repo_path: Path to repository to analyze
            file_patterns: File patterns to analyze
            analysis_config: Analysis configuration
            
        Returns:
            Comprehensive structured analysis output
        """
        self.logger.info(f"Starting ultimate repository analysis: {repo_path}")
        
        # Set default parameters
        if file_patterns is None:
            file_patterns = ["*.py", "*.java", "*.js", "*.ts", "*.go", "*.rs", "*.md", "*.txt"]
        
        if analysis_config is None:
            analysis_config = {
                "depth_level": "ultimate",
                "focus_areas": ["semantic", "structural", "behavioral", "architectural"],
                "include_business_analysis": True,
                "include_pattern_detection": True,
                "include_api_analysis": True,
                "include_dataflow_analysis": True,
                "generate_design_recommendations": True
            }
        
        try:
            print("🚀 Ultimate Repository Analysis Starting...")
            print("=" * 60)
            
            # Phase 1: Deep Structural Analysis
            print("🔍 Phase 1: Deep Structural Analysis...")
            structural_data = self._perform_deep_structural_analysis(repo_path, file_patterns)
            
            # Phase 2: Semantic Understanding
            print("🧠 Phase 2: Semantic Understanding...")
            semantic_analysis = self._perform_semantic_analysis(structural_data)
            
            # Phase 3: Behavioral Analysis
            print("⚡ Phase 3: Behavioral Analysis...")
            behavioral_analysis = self._perform_behavioral_analysis(structural_data)
            
            # Phase 4: Architectural Intent Detection
            print("🏗️  Phase 4: Architectural Intent Detection...")
            architectural_intent = self._detect_architectural_intent({
                'structural_analysis': structural_data,
                'semantic_analysis': semantic_analysis,
                'behavioral_analysis': behavioral_analysis
            })
            
            # Phase 5: Comprehensive LLM Synthesis
            print("🤖 Phase 5: AG2 LLM Comprehensive Analysis...")
            comprehensive_analysis = self._run_ag2_comprehensive_analysis(
                structural_data, semantic_analysis, behavioral_analysis, 
                architectural_intent, analysis_config
            )
            
            # Phase 6: Structure Final Output
            print("📊 Phase 6: Structuring Ultimate Analysis Output...")
            ultimate_output = self._structure_ultimate_output(
                structural_data, semantic_analysis, behavioral_analysis,
                architectural_intent, comprehensive_analysis, analysis_config
            )
            
            print("✅ Ultimate Repository Analysis Completed Successfully!")
            return ultimate_output
            
        except Exception as e:
            self.logger.error(f"Error during ultimate analysis: {str(e)}")
            return {
                "error": f"Ultimate analysis failed: {str(e)}",
                "structural_analysis": {},
                "semantic_analysis": {},
                "behavioral_analysis": {},
                "architectural_intent": {},
                "gap_analysis_readiness": {}
            }

    def _perform_deep_structural_analysis(self, repo_path: str, file_patterns: List[str]) -> Dict[str, Any]:
        """Perform deep structural analysis using AST parsing"""
        structural_data = {
            "files": [],
            "functions": [],
            "classes": [],
            "imports": [],
            "file_structure": {},
            "dependency_graph": {}
        }
        
        try:
            # Analyze all Python files with semantic AST parsing
            python_files = list(Path(repo_path).rglob("*.py"))
            
            for file_path in python_files:
                try:
                    # Use semantic AST parser for deep analysis
                    file_analysis = self.ast_parser.analyze_with_context(str(file_path))
                    
                    if 'error' not in file_analysis:
                        structural_data["files"].append(file_analysis["file_path"])
                        structural_data["functions"].extend(file_analysis.get("semantic_functions", []))
                        structural_data["classes"].extend(file_analysis.get("semantic_classes", []))
                        
                        # Store detailed file analysis
                        structural_data["file_structure"][file_analysis["file_path"]] = file_analysis
                        
                except Exception as e:
                    self.logger.warning(f"Error analyzing file {file_path}: {e}")
                    continue
            
            # Build comprehensive dependency graph
            structural_data["dependency_graph"] = self._build_comprehensive_dependency_graph(structural_data)
            
            self.logger.info(f"Structural analysis completed: {len(structural_data['functions'])} functions, {len(structural_data['classes'])} classes")
            return structural_data
            
        except Exception as e:
            self.logger.error(f"Error in structural analysis: {e}")
            return structural_data

    def _perform_semantic_analysis(self, structural_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform semantic analysis to understand business domain"""
        try:
            semantic_analysis = self.semantic_analyzer.extract_business_domain(structural_data)
            
            self.logger.info(f"Semantic analysis completed: {len(semantic_analysis.get('business_capabilities', []))} capabilities identified")
            return semantic_analysis
            
        except Exception as e:
            self.logger.error(f"Error in semantic analysis: {e}")
            return {
                "business_capabilities": [],
                "domain_models": {"entities": [], "aggregates": []},
                "service_boundaries": []
            }

    def _perform_behavioral_analysis(self, structural_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform behavioral analysis using API and DataFlow analyzers"""
        try:
            # API contract analysis
            api_analysis = self.api_analyzer.extract_api_semantics(structural_data)
            
            # Data flow analysis
            dataflow_analysis = self.dataflow_analyzer.trace_business_workflows(structural_data)
            
            # Combine behavioral analyses
            behavioral_analysis = {
                **api_analysis,
                **dataflow_analysis,
                "integration_patterns": self._identify_integration_patterns(structural_data),
                "state_management_patterns": self._identify_state_management_patterns(structural_data)
            }
            
            self.logger.info(f"Behavioral analysis completed: {len(behavioral_analysis.get('api_contracts', []))} API contracts, {len(behavioral_analysis.get('business_workflows', []))} workflows")
            return behavioral_analysis
            
        except Exception as e:
            self.logger.error(f"Error in behavioral analysis: {e}")
            return {
                "api_contracts": [],
                "data_contracts": [],
                "business_processes": [],
                "data_flow_graph": {"nodes": [], "edges": []},
                "business_workflows": []
            }

    def _detect_architectural_intent(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect architectural intent and design decisions"""
        try:
            architectural_intent = self.pattern_detector.detect_architectural_intent(analysis_data)
            
            self.logger.info(f"Architectural intent detection completed: {len(architectural_intent.get('design_patterns_detected', []))} patterns detected")
            return architectural_intent
            
        except Exception as e:
            self.logger.error(f"Error detecting architectural intent: {e}")
            return {
                "design_patterns_detected": [],
                "architectural_patterns": [],
                "design_decisions_identified": [],
                "architecture_consistency": {"consistent_patterns": [], "inconsistencies": []},
                "quality_attributes_addressed": []
            }

    def _run_ag2_comprehensive_analysis(self, structural_data: Dict[str, Any], semantic_analysis: Dict[str, Any],
                                      behavioral_analysis: Dict[str, Any], architectural_intent: Dict[str, Any],
                                      analysis_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive analysis using AG2 ConversableAgent"""
        try:
            # Create comprehensive analysis prompt
            analysis_prompt = self._create_ultimate_analysis_prompt(
                structural_data, semantic_analysis, behavioral_analysis, 
                architectural_intent, analysis_config
            )
            
            # Run AG2 agent analysis using the documented approach
            response = self.analyzer_agent.run(message=analysis_prompt, max_turns=1)
            response.process()
            
            # Parse and structure the response
            comprehensive_analysis = self._parse_ag2_response(response.messages)
            
            return comprehensive_analysis
            
        except Exception as e:
            self.logger.error(f"Error in AG2 comprehensive analysis: {e}")
            return {"error": f"AG2 analysis failed: {str(e)}"}

    def _create_ultimate_analysis_prompt(self, structural_data: Dict[str, Any], semantic_analysis: Dict[str, Any],
                                       behavioral_analysis: Dict[str, Any], architectural_intent: Dict[str, Any],
                                       analysis_config: Dict[str, Any]) -> str:
        """Create ultimate analysis prompt for AG2 LLM"""
        
        # Prepare analysis summary
        analysis_summary = {
            "repository_overview": {
                "total_files": len(structural_data.get("files", [])),
                "total_functions": len(structural_data.get("functions", [])),
                "total_classes": len(structural_data.get("classes", [])),
                "business_capabilities": len(semantic_analysis.get("business_capabilities", [])),
                "api_endpoints": len(behavioral_analysis.get("api_contracts", [])),
                "workflows": len(behavioral_analysis.get("business_workflows", [])),
                "design_patterns": len(architectural_intent.get("design_patterns_detected", []))
            },
            "key_business_capabilities": semantic_analysis.get("business_capabilities", [])[:5],
            "critical_api_contracts": behavioral_analysis.get("api_contracts", [])[:5],
            "major_workflows": behavioral_analysis.get("business_workflows", [])[:3],
            "architectural_patterns": architectural_intent.get("architectural_patterns", [])[:3],
            "design_decisions": architectural_intent.get("design_decisions_identified", [])[:5],
            "representative_code_samples": self._select_representative_code_samples(structural_data)
        }
        
        return f"""Analyze this repository comprehensively and provide detailed structural analysis for design agents.

REPOSITORY ANALYSIS SUMMARY:
{json.dumps(analysis_summary, indent=2)}

SEMANTIC ANALYSIS RESULTS:
Business Capabilities: {len(semantic_analysis.get('business_capabilities', []))}
Domain Models: {len(semantic_analysis.get('domain_models', {}).get('entities', []))} entities, {len(semantic_analysis.get('domain_models', {}).get('aggregates', []))} aggregates
Service Boundaries: {len(semantic_analysis.get('service_boundaries', []))}

BEHAVIORAL ANALYSIS RESULTS:
API Contracts: {len(behavioral_analysis.get('api_contracts', []))}
Data Contracts: {len(behavioral_analysis.get('data_contracts', []))}
Business Processes: {len(behavioral_analysis.get('business_processes', []))}
Data Flow Complexity: {behavioral_analysis.get('data_flow_graph', {}).get('complexity_metrics', {})}

ARCHITECTURAL INTENT ANALYSIS:
Design Patterns: {len(architectural_intent.get('design_patterns_detected', []))}
Architectural Patterns: {len(architectural_intent.get('architectural_patterns', []))}
Design Decisions: {len(architectural_intent.get('design_decisions_identified', []))}
Quality Attributes: {len(architectural_intent.get('quality_attributes_addressed', []))}

Please provide a comprehensive analysis in the following JSON structure:

{{
  "system_architecture": {{
    "pattern": "string",
    "confidence": 0.0,
    "components": ["string"],
    "entry_points": ["string"],
    "design_principles": ["string"],
    "architectural_concerns": ["string"]
  }},
  "component_analysis": {{
    "component_count": 0,
    "component_types": ["string"],
    "inter_component_dependencies": ["string"],
    "component_cohesion": 0.0,
    "component_coupling": 0.0
  }},
  "data_flow_analysis": {{
    "data_sources": ["string"],
    "data_transformations": ["string"],
    "data_sinks": ["string"],
    "state_management": "string"
  }},
  "api_design_analysis": {{
    "endpoint_count": 0,
    "api_style": "string",
    "authentication_patterns": ["string"],
    "error_handling_patterns": ["string"],
    "versioning_strategy": "string"
  }},
  "design_patterns": [
    {{
      "name": "string",
      "type": "string",
      "confidence": 0.0,
      "location": "string",
      "description": "string",
      "implementation_quality": 0.0
    }}
  ],
  "code_organization": {{
    "modularity_score": 0.0,
    "separation_of_concerns": 0.0,
    "code_reusability": 0.0,
    "maintainability": 0.0
  }},
  "design_recommendations": [
    {{
      "area": "string",
      "issue": "string",
      "recommendation": "string",
      "priority": "string",
      "impact": "string"
    }}
  ]
}}

Focus on providing insights that would be valuable for design agents to understand the system architecture, component relationships, data flows, business processes, and areas for improvement. Map technical implementation to business capabilities and identify architectural decisions and their rationale."""

    def _structure_ultimate_output(self, structural_data: Dict[str, Any], semantic_analysis: Dict[str, Any],
                                 behavioral_analysis: Dict[str, Any], architectural_intent: Dict[str, Any],
                                 comprehensive_analysis: Dict[str, Any], analysis_config: Dict[str, Any]) -> Dict[str, Any]:
        """Structure the ultimate analysis output"""
        
        ultimate_output = {
            "structural_analysis": {
                "repo_metadata": {
                    "name": Path(structural_data.get("files", ["unknown"])[0] if structural_data.get("files") else "unknown").parent.name,
                    "total_files": len(structural_data.get("files", [])),
                    "total_functions": len(structural_data.get("functions", [])),
                    "total_classes": len(structural_data.get("classes", [])),
                    "languages": ["Python"],  # Extend for other languages
                    "analysis_timestamp": datetime.now().isoformat()
                },
                "architecture_analysis": comprehensive_analysis.get("system_architecture", {}),
                "code_quality_metrics": self._calculate_comprehensive_quality_metrics(structural_data),
                "detected_patterns": comprehensive_analysis.get("design_patterns", [])
            },
            
            "semantic_analysis": {
                "business_capabilities": semantic_analysis.get("business_capabilities", []),
                "domain_models": semantic_analysis.get("domain_models", {}),
                "service_boundaries": semantic_analysis.get("service_boundaries", [])
            },
            
            "behavioral_analysis": {
                "api_contracts": behavioral_analysis.get("api_contracts", []),
                "business_processes": behavioral_analysis.get("business_processes", []),
                "data_flow_graph": behavioral_analysis.get("data_flow_graph", {}),
                "business_workflows": behavioral_analysis.get("business_workflows", []),
                "error_handling_strategy": behavioral_analysis.get("error_handling_strategy", {})
            },
            
            "architectural_intent": {
                "design_decisions_identified": architectural_intent.get("design_decisions_identified", []),
                "architecture_consistency": architectural_intent.get("architecture_consistency", {}),
                "quality_attributes_addressed": architectural_intent.get("quality_attributes_addressed", [])
            },
            
            "gap_analysis_readiness": {
                "mapping_to_design_concepts": self._create_design_concept_mapping(
                    structural_data, semantic_analysis, behavioral_analysis
                ),
                "questions_for_design_reconciliation": self._generate_reconciliation_questions(
                    structural_data, semantic_analysis, behavioral_analysis, architectural_intent
                ),
                "component_traceability": self._create_component_traceability_matrix(
                    structural_data, semantic_analysis
                ),
                "design_gaps_identified": comprehensive_analysis.get("design_recommendations", [])
            }
        }
        
        return ultimate_output

    # Helper methods
    def _build_comprehensive_dependency_graph(self, structural_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive dependency graph"""
        return {
            "function_dependencies": self._build_function_dependency_graph(structural_data.get("functions", [])),
            "class_dependencies": self._build_class_dependency_graph(structural_data.get("classes", [])),
            "module_dependencies": self._build_module_dependency_graph(structural_data.get("files", []))
        }

    def _build_function_dependency_graph(self, functions: List[Dict]) -> Dict[str, List[str]]:
        """Build function dependency graph"""
        dependencies = {}
        
        for func in functions:
            func_name = func.get("name", "")
            calls = func.get("calls", [])
            
            # Find function calls that match other functions
            func_dependencies = []
            for call in calls:
                # Extract function name from call
                call_name = call.split('(')[0].split('.')[-1]
                if any(f.get("name") == call_name for f in functions):
                    func_dependencies.append(call_name)
            
            dependencies[func_name] = func_dependencies
        
        return dependencies

    def _build_class_dependency_graph(self, classes: List[Dict]) -> Dict[str, List[str]]:
        """Build class dependency graph"""
        dependencies = {}
        
        for cls in classes:
            class_name = cls.get("name", "")
            base_classes = cls.get("base_classes", [])
            dependencies[class_name] = base_classes
        
        return dependencies

    def _build_module_dependency_graph(self, files: List[str]) -> Dict[str, List[str]]:
        """Build module dependency graph"""
        # Simplified - would need import analysis
        return {}

    def _identify_integration_patterns(self, structural_data: Dict[str, Any]) -> List[Dict]:
        """Identify integration patterns"""
        patterns = []
        functions = structural_data.get("functions", [])
        
        # Look for external service calls
        for func in functions:
            calls = func.get("calls", [])
            for call in calls:
                if any(pattern in call.lower() for pattern in ["http", "request", "client", "api"]):
                    patterns.append({
                        "pattern": "External API Integration",
                        "function": func.get("name", ""),
                        "call": call
                    })
        
        return patterns

    def _identify_state_management_patterns(self, structural_data: Dict[str, Any]) -> List[Dict]:
        """Identify state management patterns"""
        patterns = []
        classes = structural_data.get("classes", [])
        
        for cls in classes:
            methods = cls.get("methods", [])
            state_methods = [m for m in methods if any(keyword in m.get("name", "").lower() 
                                                     for keyword in ["state", "set_", "get_", "update_"])]
            
            if len(state_methods) > 2:
                patterns.append({
                    "pattern": "Stateful Object",
                    "class": cls.get("name", ""),
                    "state_methods": [m.get("name", "") for m in state_methods]
                })
        
        return patterns

    def _parse_ag2_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse AG2 agent response"""
        try:
            if not messages:
                return {"error": "No response received from AG2 agent"}
            
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
                    self.logger.warning(f"Failed to parse JSON from AG2 response: {e}")
                    return {"error": f"JSON parsing failed: {e}", "raw_content": content}
            else:
                return {"error": "No JSON found in AG2 response", "raw_content": content}
                
        except Exception as e:
            self.logger.error(f"Error parsing AG2 response: {str(e)}")
            return {"error": f"Response parsing failed: {str(e)}"}

    def _select_representative_code_samples(self, structural_data: Dict[str, Any]) -> Dict[str, Any]:
        """Select representative code samples for LLM analysis"""
        functions = structural_data.get("functions", [])
        classes = structural_data.get("classes", [])
        
        # Select high-complexity functions
        high_complexity_functions = sorted(
            [f for f in functions if f.get("semantic_complexity", {}).get("business_rules", 0) > 3],
            key=lambda x: x.get("semantic_complexity", {}).get("business_rules", 0),
            reverse=True
        )[:5]
        
        # Select key classes (those with many methods)
        key_classes = sorted(
            [c for c in classes if len(c.get("semantic_methods", [])) > 3],
            key=lambda x: len(x.get("semantic_methods", [])),
            reverse=True
        )[:3]
        
        return {
            "high_complexity_functions": [f.get("name", "") for f in high_complexity_functions],
            "key_classes": [c.get("name", "") for c in key_classes]
        }

    def _calculate_comprehensive_quality_metrics(self, structural_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive quality metrics"""
        functions = structural_data.get("functions", [])
        classes = structural_data.get("classes", [])
        
        # Calculate complexity metrics
        total_complexity = sum(f.get("semantic_complexity", {}).get("business_rules", 0) for f in functions)
        avg_complexity = total_complexity / len(functions) if functions else 0
        
        # Calculate documentation coverage
        documented_functions = len([f for f in functions if f.get("docstring")])
        documented_classes = len([c for c in classes if c.get("docstring")])
        total_items = len(functions) + len(classes)
        documentation_coverage = (documented_functions + documented_classes) / total_items if total_items > 0 else 0
        
        return {
            "total_functions": len(functions),
            "total_classes": len(classes),
            "average_complexity": avg_complexity,
            "max_complexity": max((f.get("semantic_complexity", {}).get("business_rules", 0) for f in functions), default=0),
            "documentation_coverage": documentation_coverage,
            "maintainability_index": max(0, 100 - (avg_complexity * 5) - (50 * (1 - documentation_coverage))),
            "technical_debt_score": min(100, (avg_complexity * 5) + (50 * (1 - documentation_coverage))),
            "code_duplication": 0.0  # Would need more sophisticated analysis
        }

    def _create_design_concept_mapping(self, structural_data: Dict[str, Any], semantic_analysis: Dict[str, Any],
                                     behavioral_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create mapping from code components to design concepts"""
        mappings = []
        
        # Map classes to design concepts
        classes = structural_data.get("classes", [])
        for cls in classes:
            class_name = cls.get("name", "")
            
            # Determine likely design concept
            if "controller" in class_name.lower():
                concept = "API Controller/Adapter"
                responsibilities = ["HTTP handling", "Request validation", "Response formatting"]
            elif "service" in class_name.lower():
                concept = "Domain Service/Application Service"
                responsibilities = ["Business logic", "Workflow coordination", "Transaction management"]
            elif "repository" in class_name.lower():
                concept = "Data Access Repository"
                responsibilities = ["Data persistence", "Query abstraction", "Data mapping"]
            elif "model" in class_name.lower() or "entity" in class_name.lower():
                concept = "Domain Entity/Value Object"
                responsibilities = ["Data representation", "Business rules", "State management"]
            else:
                concept = "Utility/Helper Component"
                responsibilities = ["Support functions", "Common operations"]
            
            mappings.append({
                "code_component": class_name,
                "likely_design_concept": concept,
                "responsibilities": responsibilities,
                "file_path": cls.get("file_path", "unknown")
            })
        
        return mappings

    def _generate_reconciliation_questions(self, structural_data: Dict[str, Any], semantic_analysis: Dict[str, Any],
                                         behavioral_analysis: Dict[str, Any], architectural_intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate questions for design reconciliation"""
        questions = []
        
        # Check for validation patterns
        functions = structural_data.get("functions", [])
        validation_functions = [f for f in functions if "validate" in f.get("name", "").lower()]
        
        if validation_functions:
            questions.append({
                "question": "Code shows separate validation layers - is this intentional design?",
                "context": f"Found {len(validation_functions)} validation functions across different layers",
                "files": list(set([f.get("file_path", "") for f in validation_functions])),
                "design_implication": "Separation of concerns strategy"
            })
        
        # Check for repository pattern consistency
        classes = structural_data.get("classes", [])
        repo_classes = [c for c in classes if "repository" in c.get("name", "").lower()]
        service_classes = [c for c in classes if "service" in c.get("name", "").lower()]
        
        if repo_classes and service_classes:
            # Check if all services use repositories
            inconsistencies = []
            for service in service_classes:
                service_methods = service.get("semantic_methods", [])
                uses_repo = any(any("repository" in call.lower() for call in method.get("calls", [])) 
                              for method in service_methods)
                if not uses_repo:
                    inconsistencies.append(service.get("name", ""))
            
            if inconsistencies:
                questions.append({
                    "question": "Repository pattern used inconsistently - intended architectural decision?",
                    "context": f"Some services ({', '.join(inconsistencies)}) don't use repository pattern",
                    "files": [c.get("file_path", "") for c in service_classes if c.get("name", "") in inconsistencies],
                    "design_implication": "Architectural consistency"
                })
        
        return questions

    def _create_component_traceability_matrix(self, structural_data: Dict[str, Any], 
                                            semantic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create component traceability matrix"""
        matrix = {
            "business_capability_to_code": {},
            "code_to_business_capability": {},
            "component_relationships": {}
        }
        
        # Map business capabilities to code components
        capabilities = semantic_analysis.get("business_capabilities", [])
        for capability in capabilities:
            capability_name = capability.get("capability", "")
            implementing_components = capability.get("implementing_components", [])
            matrix["business_capability_to_code"][capability_name] = implementing_components
            
            # Reverse mapping
            for component in implementing_components:
                if component not in matrix["code_to_business_capability"]:
                    matrix["code_to_business_capability"][component] = []
                matrix["code_to_business_capability"][component].append(capability_name)
        
        return matrix
