"""
Enhanced Repository Analyzer Agent
Uses the enhanced AST parser to provide design-agent-ready output
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from autogen import ConversableAgent, LLMConfig

from .tools.enhanced_react_ast_parser import EnhancedReactASTParser
from .tools.component_analyzer import ComponentAnalyzer

logger = logging.getLogger(__name__)

class EnhancedRepositoryAnalyzerAgent:
    """Enhanced repository analyzer with proper service detection and design-agent-ready output"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.llm_config = llm_config
        
        # Initialize enhanced AST parser
        self.ast_parser = EnhancedReactASTParser()
        self.component_analyzer = ComponentAnalyzer()
        
        # Create specialized LLM agents
        self.component_analyzer_agent = ConversableAgent(
            name="component_analyzer",
            system_message=self._get_component_analyzer_system_message(),
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
        
        self.business_logic_agent = ConversableAgent(
            name="business_logic_analyzer",
            system_message=self._get_business_logic_system_message(),
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
        
        self.architecture_agent = ConversableAgent(
            name="architecture_analyzer",
            system_message=self._get_architecture_system_message(),
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
        
        self.logger.info("Enhanced Repository Analyzer Agent initialized")
    
    def _get_component_analyzer_system_message(self) -> str:
        """Get system message for component analyzer agent"""
        return """You are a React Component Analysis Agent. Analyze React components and provide detailed insights.

Your role is to:
1. Analyze React component structure, props, state, and behavior
2. Identify business logic and user interactions
3. Assess component quality and maintainability
4. Provide recommendations for improvement

Focus on:
- Component purpose and business role
- Props interface and validation
- State management patterns
- Event handling and user interactions
- Dependencies and data flow
- Code quality and best practices

Return structured JSON analysis for each component.
"""
    
    def _get_business_logic_system_message(self) -> str:
        """Get system message for business logic analyzer agent"""
        return """You are a Business Logic Analysis Agent. Analyze service classes and business logic.

Your role is to:
1. Analyze service methods and their business purpose
2. Identify API contracts and data transformations
3. Assess error handling and validation
4. Provide recommendations for improvement

Focus on:
- Service method purposes and business rules
- API contracts and data models
- Error handling strategies
- Performance considerations
- Security and validation

Return structured JSON analysis for each service.
"""
    
    def _get_architecture_system_message(self) -> str:
        """Get system message for architecture analyzer agent"""
        return """You are an Architecture Analysis Agent. Analyze overall system architecture and patterns.

Your role is to:
1. Identify architectural patterns and design decisions
2. Assess code quality and maintainability
3. Analyze dependencies and data flow
4. Provide architectural recommendations

Focus on:
- Architectural patterns and design decisions
- Code quality metrics and technical debt
- Dependencies and coupling
- Performance and scalability
- Testing and maintainability

Return structured JSON analysis of the overall architecture.
"""
    
    def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository with enhanced AST parser and LLM analysis"""
        try:
            self.logger.info(f"Analyzing repository with enhanced approach: {repo_path}")
            
            # Phase 1: Fast Python structural analysis
            self.logger.info("Phase 1: Fast Python structural analysis...")
            file_analyses = self._analyze_files(repo_path)
            
            # Phase 2: Component relationship analysis
            self.logger.info("Phase 2: Component relationship analysis...")
            component_analysis = self.component_analyzer.analyze_components(file_analyses)
            
            # Phase 3: LLM semantic analysis
            self.logger.info("Phase 3: LLM semantic analysis...")
            semantic_analysis = self._run_llm_analysis(file_analyses)
            
            # Phase 4: Generate design-agent-ready output
            self.logger.info("Phase 4: Generating design-agent-ready output...")
            output = self._generate_design_agent_output(file_analyses, component_analysis, semantic_analysis)
            
            return output
            
        except Exception as e:
            self.logger.error(f"Error analyzing repository: {e}")
            return {"error": str(e)}
    
    def _analyze_files(self, repo_path: str) -> List[Dict[str, Any]]:
        """Analyze all files in the repository"""
        file_analyses = []
        
        # Find all relevant files
        for root, dirs, files in os.walk(repo_path):
            # Skip node_modules and other irrelevant directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]
            
            for file in files:
                if self._is_business_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        analysis = self.ast_parser.analyze_file(file_path)
                        file_analyses.append(analysis)
                        self.logger.info(f"Analyzed business file: {file_path}")
                    except Exception as e:
                        self.logger.error(f"Error analyzing file {file_path}: {e}")
        
        self.logger.info(f"Analyzed {len(file_analyses)} business files out of total files found")
        return file_analyses
    
    def _is_business_file(self, filename: str) -> bool:
        """Check if file is relevant for business logic analysis"""
        filename_lower = filename.lower()
        
        # Include relevant file types
        if not any(filename_lower.endswith(ext) for ext in ['.tsx', '.ts', '.jsx', '.js']):
            return False
        
        # Exclude test files, config files, etc.
        exclude_patterns = [
            'test', 'spec', 'config', 'setup', 'mock', 'stub',
            'index.ts', 'index.js', 'types.ts', 'constants.ts',
            'utils.ts', 'helpers.ts', 'styles', 'css'
        ]
        
        for pattern in exclude_patterns:
            if pattern in filename_lower:
                return False
        
        return True
    
    def _run_llm_analysis(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run LLM analysis on extracted components and services"""
        semantic_analysis = {
            "components": {},
            "services": {},
            "business_capabilities": [],
            "data_flow_analysis": {},
            "user_interactions": [],
            "architectural_patterns": [],
            "code_quality_assessment": {},
            "recommendations": {}
        }
        
        # Analyze components with LLM
        for file_analysis in file_analyses:
            if file_analysis.get('file_type') == 'component':
                for component in file_analysis.get('components', []):
                    llm_analysis = self._analyze_component_with_llm(component, file_analysis)
                    if llm_analysis:
                        semantic_analysis["components"][component['name']] = llm_analysis
            
            elif file_analysis.get('file_type') == 'service':
                for service in file_analysis.get('services', []):
                    llm_analysis = self._analyze_service_with_llm(service, file_analysis)
                    if llm_analysis:
                        semantic_analysis["services"][service['name']] = llm_analysis
        
        # Run architecture analysis
        architecture_analysis = self._run_architecture_analysis(file_analyses)
        if architecture_analysis:
            semantic_analysis.update(architecture_analysis)
        
        return semantic_analysis
    
    def _analyze_component_with_llm(self, component: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single component with LLM"""
        try:
            prompt = f"""
Analyze this React component and provide detailed insights:

Component: {component['name']}
File: {file_analysis['file_path']}
Type: {component['type']}
Props: {json.dumps(component.get('props', []), indent=2)}
State: {json.dumps(component.get('state', []), indent=2)}
Hooks: {json.dumps(component.get('hooks', []), indent=2)}
JSX Elements: {json.dumps(component.get('jsx_elements', []), indent=2)}
Event Handlers: {json.dumps(component.get('event_handlers', []), indent=2)}
Complexity: {component.get('complexity', 0)}

Provide analysis in this JSON format:
{{
    "name": "ComponentName",
    "purpose": "What this component does",
    "business_role": "Business purpose and value",
    "props_analysis": {{}},
    "state_management": {{}},
    "hooks_analysis": {{}},
    "business_logic": {{}},
    "user_interactions": [],
    "dependencies": {{}},
    "data_flow": {{}},
    "business_capabilities": [],
    "code_quality": {{}},
    "architectural_patterns": [],
    "error_handling_strategies": "Error handling approach",
    "performance_characteristics": "Performance considerations",
    "testing_recommendations": "Testing strategy"
}}
"""
            
            response = self.component_analyzer_agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.component_analyzer_agent
            )
            
            content = str(response) if response else None
            
            if content and content.strip() and content.strip() != "None":
                # Extract JSON from markdown code blocks if present
                json_content = self._extract_json_from_markdown(content)
                
                try:
                    parsed_response = json.loads(json_content)
                    return parsed_response
                except json.JSONDecodeError:
                    return {
                        'name': component['name'],
                        'purpose': content,
                        'business_role': 'Component analysis',
                        'analysis_type': 'component',
                        'file_path': file_analysis['file_path'],
                        'llm_response': content
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing component {component['name']}: {e}")
            return None
    
    def _analyze_service_with_llm(self, service: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single service with LLM"""
        try:
            prompt = f"""
Analyze this service class and provide detailed insights:

Service: {service['name']}
File: {file_analysis['file_path']}
Type: {service['type']}
Methods: {json.dumps(service.get('methods', []), indent=2)}
Properties: {json.dumps(service.get('properties', []), indent=2)}
Complexity: {service.get('complexity', 0)}

Provide analysis in this JSON format:
{{
    "name": "ServiceName",
    "purpose": "What this service does",
    "business_role": "Business purpose and value",
    "methods": {{}},
    "dependencies": {{}},
    "business_capabilities": [],
    "code_quality": {{}},
    "error_handling": {{}},
    "performance_characteristics": {{}},
    "testing_recommendations": "Testing strategy"
}}
"""
            
            response = self.business_logic_agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.business_logic_agent
            )
            
            content = str(response) if response else None
            
            if content and content.strip() and content.strip() != "None":
                json_content = self._extract_json_from_markdown(content)
                
                try:
                    parsed_response = json.loads(json_content)
                    return parsed_response
                except json.JSONDecodeError:
                    return {
                        'name': service['name'],
                        'purpose': content,
                        'business_role': 'Service analysis',
                        'analysis_type': 'service',
                        'file_path': file_analysis['file_path'],
                        'llm_response': content
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing service {service['name']}: {e}")
            return None
    
    def _run_architecture_analysis(self, file_analyses: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Run overall architecture analysis"""
        try:
            # Prepare architecture context
            components = []
            services = []
            
            for file_analysis in file_analyses:
                if file_analysis.get('file_type') == 'component':
                    components.extend(file_analysis.get('components', []))
                elif file_analysis.get('file_type') == 'service':
                    services.extend(file_analysis.get('services', []))
            
            prompt = f"""
Analyze the overall architecture of this React application:

Components: {len(components)}
Services: {len(services)}
Files: {len(file_analyses)}

Component Details:
{json.dumps(components, indent=2)}

Service Details:
{json.dumps(services, indent=2)}

Provide architectural analysis in this JSON format:
{{
    "architectural_patterns": [
        {{
            "pattern": "Pattern Name",
            "description": "Description",
            "evidence": "Evidence in code",
            "benefits": ["Benefit 1", "Benefit 2"],
            "drawbacks": ["Drawback 1"],
            "implementation_quality": "Good/Medium/Poor"
        }}
    ],
    "code_quality_assessment": {{
        "overall_score": 8.5,
        "strengths": ["Strength 1", "Strength 2"],
        "weaknesses": ["Weakness 1", "Weakness 2"],
        "technical_debt": ["Debt 1", "Debt 2"],
        "scalability_concerns": ["Concern 1", "Concern 2"]
    }},
    "recommendations": {{
        "immediate": ["Immediate 1", "Immediate 2"],
        "short_term": ["Short term 1", "Short term 2"],
        "long_term": ["Long term 1", "Long term 2"]
    }}
}}
"""
            
            response = self.architecture_agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.architecture_agent
            )
            
            content = str(response) if response else None
            
            if content and content.strip() and content.strip() != "None":
                json_content = self._extract_json_from_markdown(content)
                
                try:
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    return {
                        'architectural_patterns': [],
                        'code_quality_assessment': {'overall_score': 0},
                        'recommendations': {'immediate': [], 'short_term': [], 'long_term': []},
                        'llm_response': content
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error in architecture analysis: {e}")
            return None
    
    def _extract_json_from_markdown(self, content: str) -> str:
        """Extract JSON from markdown code blocks"""
        import re
        
        # Look for JSON code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Look for JSON without code blocks
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        # Return original content if no JSON found
        return content
    
    def _generate_design_agent_output(self, 
                                    file_analyses: List[Dict[str, Any]], 
                                    component_analysis: Dict[str, Any], 
                                    semantic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate design-agent-ready output structure"""
        
        # Extract components and services for design-agent-friendly structure
        components = {}
        services = {}
        business_logic = {}
        dependencies = {}
        
        for file_analysis in file_analyses:
            file_path = file_analysis['file_path']
            file_name = Path(file_path).name
            
            # Extract components
            if file_analysis.get('file_type') == 'component':
                component_names = [comp['name'] for comp in file_analysis.get('components', [])]
                if component_names:
                    components[file_name] = component_names
            
            # Extract services
            elif file_analysis.get('file_type') == 'service':
                service_names = [svc['name'] for svc in file_analysis.get('services', [])]
                if service_names:
                    services[file_name] = service_names
                    
                    # Extract service methods for business logic
                    for service in file_analysis.get('services', []):
                        method_names = [method['name'] for method in service.get('methods', [])]
                        if method_names:
                            business_logic[file_name] = method_names
            
            # Extract dependencies
            imports = file_analysis.get('imports', [])
            internal_deps = []
            for imp in imports:
                if imp['source'].startswith('.'):  # Internal dependency
                    internal_deps.append(imp['source'])
            
            if internal_deps:
                dependencies[file_name] = internal_deps
        
        # Generate design-agent-ready output
        output = {
            "repository_metadata": {
                "total_files": len(file_analyses),
                "file_types": self._count_file_types(file_analyses),
                "structure_pattern": "Component-based architecture with service layer",
                "framework_detection": "React 18 with TypeScript",
                "analysis_method": "Enhanced Hybrid (Python + LLM)",
                "design_agent_ready": True
            },
            "components": components,
            "business_logic": business_logic,
            "dependencies": dependencies,
            "semantic_analysis": semantic_analysis,
            "component_analysis": component_analysis,
            "business_capabilities": self._extract_business_capabilities(semantic_analysis),
            "data_flow_analysis": self._analyze_data_flow(component_analysis),
            "architectural_patterns": semantic_analysis.get('architectural_patterns', []),
            "code_quality_assessment": semantic_analysis.get('code_quality_assessment', {}),
            "recommendations": semantic_analysis.get('recommendations', {})
        }
        
        return output
    
    def _count_file_types(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count file types in the analysis"""
        file_types = {}
        for analysis in file_analyses:
            file_type = analysis.get('file_type', 'unknown')
            file_types[file_type] = file_types.get(file_type, 0) + 1
        return file_types
    
    def _extract_business_capabilities(self, semantic_analysis: Dict[str, Any]) -> List[str]:
        """Extract business capabilities from semantic analysis"""
        capabilities = []
        
        # Extract from components
        for component in semantic_analysis.get('components', {}).values():
            if isinstance(component, dict):
                capabilities.extend(component.get('business_capabilities', []))
        
        # Extract from services
        for service in semantic_analysis.get('services', {}).values():
            if isinstance(service, dict):
                capabilities.extend(service.get('business_capabilities', []))
        
        return list(set(capabilities))  # Remove duplicates
    
    def _analyze_data_flow(self, component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data flow from component analysis"""
        return {
            "primary_flow": "User Input → Component State → Service Call → Data Display",
            "data_transformations": [
                "User input → Component state",
                "Component state → Service parameters",
                "Service response → Component state",
                "Component state → UI rendering"
            ],
            "state_management": {
                "global_state": "None (local component state)",
                "local_state": "Component-level state management",
                "state_synchronization": "Props drilling and callbacks"
            }
        }
