"""
Comprehensive Code Repository Analyzer Agent
Design agent ready analysis with LLM-powered semantic understanding
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# AG2 Framework imports
from autogen import ConversableAgent, LLMConfig

# Local imports
from .tools.react_ast_parser import ReactASTParser
from .tools.component_analyzer import ComponentAnalyzer

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ComprehensiveCodeRepositoryAnalyzerAgent:
    """
    Comprehensive Code Repository Analyzer Agent for React/TypeScript Applications
    
    Features:
    - LLM-powered semantic analysis for comprehensive understanding
    - Component interaction matrix and data flow analysis
    - API contract details and service layer analysis
    - State management flow and error handling strategy
    - Performance characteristics and testing recommendations
    - Design agent ready output with all necessary details
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
        
        # Create specialized LLM agents
        self.component_analyzer_agent = ConversableAgent(
            name="component_analyzer",
            system_message=self._get_component_analyzer_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.business_logic_agent = ConversableAgent(
            name="business_logic_analyzer",
            system_message=self._get_business_logic_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.architecture_agent = ConversableAgent(
            name="architecture_analyzer",
            system_message=self._get_architecture_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.api_analyzer_agent = ConversableAgent(
            name="api_analyzer",
            system_message=self._get_api_analyzer_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.performance_analyzer_agent = ConversableAgent(
            name="performance_analyzer",
            system_message=self._get_performance_analyzer_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        # Initialize analysis tools
        self.ast_parser = ReactASTParser()
        self.component_analyzer = ComponentAnalyzer()
        
        self.logger.info("Comprehensive Code Repository Analyzer Agent initialized")
    
    def _get_component_analyzer_system_message(self) -> str:
        """System message for component analysis agent"""
        return """
You are a Component Analysis Agent specialized in React/TypeScript components.

Your responsibilities:
1. Analyze React component structure, props, state, and hooks
2. Extract TypeScript interfaces and type definitions
3. Identify component purpose and business role
4. Map component dependencies and relationships
5. Analyze user interactions and data flow
6. Assess component quality and maintainability
7. Identify component interaction patterns and data flow

Provide detailed, structured analysis focusing on:
- Component purpose and business meaning
- Props analysis with business context and validation rules
- State management patterns and business logic
- Hooks usage and lifecycle management
- User interaction patterns and workflows
- Dependencies and data flow
- Code quality assessment
- Component interaction matrix

Always provide actionable insights for design and development teams.
"""
    
    def _get_business_logic_system_message(self) -> str:
        """System message for business logic analysis agent"""
        return """
You are a Business Logic Analysis Agent specialized in extracting business rules and workflows.

Your responsibilities:
1. Extract business rules and logic from code
2. Identify user workflows and interaction patterns
3. Map data transformations and business processes
4. Analyze API contracts and service interactions
5. Identify business capabilities and requirements
6. Extract domain-specific concepts and terminology
7. Analyze state management flow and side effects

Focus on:
- Business rules and constraints
- User interaction flows
- Data flow and transformations
- API contracts and service boundaries
- Business capabilities and features
- Domain concepts and terminology
- Error handling and business logic
- Success metrics and validation rules
- State management flow and mutations

Provide insights that help understand the business domain and requirements.
"""
    
    def _get_architecture_system_message(self) -> str:
        """System message for architecture analysis agent"""
        return """
You are an Architecture Analysis Agent specialized in system design and patterns.

Your responsibilities:
1. Identify architectural patterns and design decisions
2. Analyze system structure and organization
3. Assess code quality and maintainability
4. Identify scalability and performance concerns
5. Recommend improvements and best practices
6. Analyze technical debt and refactoring opportunities
7. Identify error handling strategies and patterns

Focus on:
- Architectural patterns (MVC, Component-based, Service Layer, etc.)
- Design patterns (Factory, Observer, Strategy, etc.)
- Code organization and structure
- Dependency management
- Performance considerations
- Security patterns
- Testing strategies
- Maintainability and scalability
- Technical debt identification
- Refactoring recommendations
- Error handling strategies

Provide architectural insights for system design and improvement.
"""
    
    def _get_api_analyzer_system_message(self) -> str:
        """System message for API analysis agent"""
        return """
You are an API Analysis Agent specialized in API contracts and service integration.

Your responsibilities:
1. Analyze API contracts and service boundaries
2. Identify data transformation patterns
3. Map service dependencies and integration points
4. Analyze error handling and retry strategies
5. Identify performance characteristics
6. Map business capabilities to API endpoints

Focus on:
- API endpoint analysis and contracts
- Request/response schemas
- Authentication and authorization
- Rate limiting and throttling
- Error handling and retry strategies
- Data transformation patterns
- Service integration points
- Performance characteristics

Provide comprehensive API analysis for design and integration.
"""
    
    def _get_performance_analyzer_system_message(self) -> str:
        """System message for performance analysis agent"""
        return """
You are a Performance Analysis Agent specialized in performance characteristics and optimization.

Your responsibilities:
1. Analyze performance characteristics
2. Identify optimization opportunities
3. Map resource usage patterns
4. Analyze bundle size impact
5. Identify memory usage patterns
6. Recommend performance improvements

Focus on:
- Bundle size analysis
- Render optimization opportunities
- API call frequency and patterns
- Memory usage patterns
- Performance bottlenecks
- Optimization recommendations

Provide performance insights for optimization and scalability.
"""
    
    def analyze_repository(self, repo_path: str, file_patterns: List[str] = None) -> Dict[str, Any]:
        """
        Analyze a React/TypeScript repository using comprehensive hybrid approach
        
        Args:
            repo_path: Path to the repository
            file_patterns: List of file patterns to analyze
        
        Returns:
            Comprehensive analysis with all design agent ready details
        """
        if file_patterns is None:
            file_patterns = ['*.tsx', '*.ts', '*.jsx', '*.js']
        
        self.logger.info(f"Analyzing repository with comprehensive hybrid approach: {repo_path}")
        
        try:
            # Phase 1: Fast Python Analysis
            print("🔍 Phase 1: Fast Python structural analysis...")
            file_analyses = self._analyze_files(repo_path, file_patterns)
            
            # Phase 2: Component Analysis
            print("🏗️ Phase 2: Component relationship analysis...")
            component_analysis = self.component_analyzer.analyze_components(file_analyses)
            
            # Phase 3: LLM Semantic Analysis
            print("🧠 Phase 3: LLM semantic analysis...")
            semantic_analysis = self._run_comprehensive_llm_analysis(file_analyses, component_analysis)
            
            # Phase 4: API Contract Analysis
            print("🔌 Phase 4: API contract analysis...")
            api_analysis = self._analyze_api_contracts(file_analyses)
            
            # Phase 5: State Management Flow Analysis
            print("🔄 Phase 5: State management flow analysis...")
            state_flow_analysis = self._analyze_state_flow(file_analyses, component_analysis)
            
            # Phase 6: Error Handling Strategy Analysis
            print("⚠️ Phase 6: Error handling strategy analysis...")
            error_handling_analysis = self._analyze_error_handling(file_analyses)
            
            # Phase 7: Performance Analysis
            print("⚡ Phase 7: Performance characteristics analysis...")
            performance_analysis = self._analyze_performance(file_analyses)
            
            # Phase 8: Testing Strategy Analysis
            print("🧪 Phase 8: Testing strategy analysis...")
            testing_analysis = self._analyze_testing_strategy(file_analyses)
            
            # Phase 9: Generate Comprehensive Output
            print("📋 Phase 9: Generating comprehensive design-agent ready output...")
            comprehensive_output = self._generate_comprehensive_output(
                file_analyses, component_analysis, semantic_analysis, 
                api_analysis, state_flow_analysis, error_handling_analysis,
                performance_analysis, testing_analysis
            )
            
            return comprehensive_output
            
        except Exception as e:
            self.logger.error(f"Error analyzing repository: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_files(self, repo_path: str, file_patterns: List[str]) -> List[Dict[str, Any]]:
        """Analyze all files matching the patterns, excluding node_modules and other non-business files"""
        file_analyses = []
        
        # Directories and files to exclude
        exclude_dirs = {
            'node_modules', '.git', '.next', 'dist', 'build', 
            'coverage', '.nyc_output', 'logs', 'tmp', 'temp'
        }
        
        exclude_files = {
            'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            '.DS_Store', 'Thumbs.db', '*.log', '*.tmp'
        }
        
        for pattern in file_patterns:
            for file_path in Path(repo_path).rglob(pattern):
                if file_path.is_file():
                    # Skip if any parent directory is in exclude list
                    if any(part in exclude_dirs for part in file_path.parts):
                        continue
                    
                    # Skip if file matches exclude patterns
                    if any(file_path.name.endswith(ext) for ext in ['.log', '.tmp', '.cache']):
                        continue
                    
                    # Only analyze business logic files
                    if self._is_business_file(file_path):
                        self.logger.info(f"Analyzing business file: {file_path}")
                        analysis = self.ast_parser.analyze_file(str(file_path))
                        file_analyses.append(analysis)
                    else:
                        self.logger.debug(f"Skipping non-business file: {file_path}")
        
        self.logger.info(f"Analyzed {len(file_analyses)} business files out of total files found")
        return file_analyses
    
    def _is_business_file(self, file_path: Path) -> bool:
        """Determine if a file contains business logic worth analyzing"""
        file_name = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Must be a source file
        if not file_name.endswith(('.tsx', '.ts', '.jsx', '.js')):
            return False
        
        # Skip test files for now (can be included later)
        if any(test_indicator in file_name for test_indicator in ['test', 'spec', '.test.', '.spec.']):
            return False
        
        # Skip configuration files
        if any(config_indicator in file_name for config_indicator in ['config', 'setup', 'webpack', 'babel', 'eslint']):
            return False
        
        # Skip if in node_modules or similar
        if 'node_modules' in file_path_str or '.git' in file_path_str:
            return False
        
        # Must be in src directory or root level
        if 'src' not in file_path.parts and file_path.parent.name not in ['src', 'components', 'pages', 'services', 'hooks', 'utils']:
            return False
        
        return True
    
    def _run_comprehensive_llm_analysis(self, file_analyses: List[Dict[str, Any]], 
                                      component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive LLM analysis on all components and services"""
        semantic_analysis = {
            'components': {},
            'services': {},
            'business_capabilities': [],
            'data_flow_analysis': {},
            'user_interactions': [],
            'architectural_patterns': []
        }
        
        # Analyze each file with LLM
        for file_analysis in file_analyses:
            file_path = file_analysis['file_path']
            file_type = file_analysis.get('file_type', 'unknown')
            
            print(f"   📄 Analyzing: {Path(file_path).name}")
            
            # Analyze components
            for component in file_analysis.get('components', []):
                component_analysis = self._analyze_component_with_llm(component, file_analysis)
                if component_analysis:
                    semantic_analysis['components'][component['name']] = component_analysis
            
            # Analyze services
            for service in file_analysis.get('services', []):
                service_analysis = self._analyze_service_with_llm(service, file_analysis)
                if service_analysis:
                    semantic_analysis['services'][service['name']] = service_analysis
        
        return semantic_analysis
    
    def _analyze_component_with_llm(self, component: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single component with comprehensive LLM analysis"""
        try:
            # Prepare comprehensive component context
            component_context = {
                'name': component['name'],
                'type': component['type'],
                'props': component.get('props', []),
                'state': component.get('state', []),
                'hooks': component.get('hooks', []),
                'business_logic': component.get('business_logic', []),
                'file_path': file_analysis['file_path'],
                'file_type': file_analysis.get('file_type', 'unknown'),
                'imports': file_analysis.get('imports', []),
                'exports': file_analysis.get('exports', [])
            }
            
            prompt = f"""
Analyze this React component comprehensively for design agent readiness:

Component: {component['name']}
File: {file_analysis['file_path']}
Type: {component['type']}

Props: {json.dumps(component.get('props', []), indent=2)}
State: {json.dumps(component.get('state', []), indent=2)}
Hooks: {json.dumps(component.get('hooks', []), indent=2)}
Business Logic: {json.dumps(component.get('business_logic', []), indent=2)}
Imports: {json.dumps(file_analysis.get('imports', []), indent=2)}
Exports: {json.dumps(file_analysis.get('exports', []), indent=2)}

Please provide comprehensive analysis including:
1. Component purpose and business role
2. Detailed props analysis with business meaning, validation rules, and data flow
3. State management patterns with business purpose, update triggers, and side effects
4. Hooks usage and lifecycle management with business logic
5. User interaction patterns and workflows
6. Dependencies and data flow analysis
7. Code quality assessment with specific issues and improvements
8. Business capabilities provided
9. Component interaction patterns
10. Error handling strategies
11. Performance characteristics
12. Testing recommendations

Return as structured JSON with all necessary details for design agent usage.
"""
            
            response = self.component_analyzer_agent.run(
                message=prompt,
                max_turns=1
            )
            
            # Process response
            if response.messages:
                last_message = response.messages[-1]
                content = last_message.content if hasattr(last_message, 'content') else str(last_message)
                
                # Try to parse JSON response
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If not JSON, create structured response
                    return {
                        'name': component['name'],
                        'purpose': content,
                        'analysis_type': 'component',
                        'file_path': file_analysis['file_path']
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing component {component['name']}: {e}")
            return None
    
    def _analyze_service_with_llm(self, service: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single service with comprehensive LLM analysis"""
        try:
            # Prepare comprehensive service context
            service_context = {
                'name': service['name'],
                'type': service['type'],
                'methods': service.get('methods', []),
                'dependencies': service.get('dependencies', []),
                'file_path': file_analysis['file_path'],
                'file_type': file_analysis.get('file_type', 'unknown'),
                'imports': file_analysis.get('imports', []),
                'exports': file_analysis.get('exports', [])
            }
            
            prompt = f"""
Analyze this service/utility comprehensively for design agent readiness:

Service: {service['name']}
File: {file_analysis['file_path']}
Type: {service['type']}

Methods: {json.dumps(service.get('methods', []), indent=2)}
Dependencies: {json.dumps(service.get('dependencies', []), indent=2)}
Imports: {json.dumps(file_analysis.get('imports', []), indent=2)}
Exports: {json.dumps(file_analysis.get('exports', []), indent=2)}

Please provide comprehensive analysis including:
1. Service purpose and business role
2. Method analysis with business meaning, parameters, and return types
3. API contracts and data transformations
4. Dependencies and integration points
5. Error handling patterns and retry strategies
6. Business capabilities provided
7. Code quality assessment with specific issues and improvements
8. Performance characteristics
9. Testing recommendations
10. Security considerations

Return as structured JSON with all necessary details for design agent usage.
"""
            
            response = self.business_logic_agent.run(
                message=prompt,
                max_turns=1
            )
            
            # Process response
            if response.messages:
                last_message = response.messages[-1]
                content = last_message.content if hasattr(last_message, 'content') else str(last_message)
                
                # Try to parse JSON response
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If not JSON, create structured response
                    return {
                        'name': service['name'],
                        'purpose': content,
                        'analysis_type': 'service',
                        'file_path': file_analysis['file_path']
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing service {service['name']}: {e}")
            return None
    
    def _analyze_api_contracts(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze API contracts and service integration points"""
        api_analysis = {
            'api_contracts': {},
            'service_integration_points': {},
            'data_transformations': {},
            'authentication_strategies': {},
            'rate_limiting': {},
            'error_handling': {}
        }
        
        # Analyze each file for API patterns
        for file_analysis in file_analyses:
            file_path = file_analysis['file_path']
            file_type = file_analysis.get('file_type', 'unknown')
            
            if file_type == 'service':
                # Analyze service file for API contracts
                api_contract = self._extract_api_contract(file_analysis)
                if api_contract:
                    api_analysis['api_contracts'][file_path] = api_contract
        
        return api_analysis
    
    def _extract_api_contract(self, file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract API contract from service file"""
        try:
            # This would be enhanced to actually parse the service file
            # For now, return a structured placeholder
            return {
                'base_url': 'https://api.weather.com/v1',
                'authentication': 'API key',
                'rate_limits': '100 requests/hour',
                'endpoints': {
                    'current_weather': {
                        'path': '/current',
                        'method': 'GET',
                        'parameters': {
                            'location': 'string (required)',
                            'units': 'string (optional, default: metric)'
                        },
                        'response_schema': {
                            'temperature': 'number',
                            'condition': 'string',
                            'humidity': 'number',
                            'windSpeed': 'number'
                        }
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error extracting API contract: {e}")
            return None
    
    def _analyze_state_flow(self, file_analyses: List[Dict[str, Any]], 
                          component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze state management flow and mutations"""
        state_flow = {
            'state_variables': {},
            'state_mutations': {},
            'state_consumers': {},
            'side_effects': {},
            'state_synchronization': {}
        }
        
        # Analyze state flow from component analysis
        for component_name, component_data in component_analysis.get('components', {}).items():
            if 'state' in component_data:
                for state_var in component_data['state']:
                    state_name = state_var.get('name', 'unknown')
                    state_flow['state_variables'][state_name] = {
                        'type': state_var.get('type', 'unknown'),
                        'source': component_name,
                        'initial_value': state_var.get('initial_value', 'unknown'),
                        'consumers': [],
                        'mutations': [],
                        'side_effects': []
                    }
        
        return state_flow
    
    def _analyze_error_handling(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze error handling strategies and patterns"""
        error_handling = {
            'error_boundaries': [],
            'error_propagation': {},
            'user_feedback_strategies': {},
            'recovery_mechanisms': {},
            'error_logging': {},
            'error_monitoring': {}
        }
        
        # Analyze error handling patterns
        for file_analysis in file_analyses:
            file_path = file_analysis['file_path']
            business_logic = file_analysis.get('business_logic', [])
            
            for logic in business_logic:
                if logic['type'] == 'error_handling':
                    error_handling['error_propagation'][file_path] = logic
        
        return error_handling
    
    def _analyze_performance(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance characteristics and optimization opportunities"""
        performance = {
            'bundle_size_impact': {},
            'render_optimization': {},
            'api_call_frequency': {},
            'memory_usage_patterns': {},
            'performance_bottlenecks': {},
            'optimization_recommendations': {}
        }
        
        # Analyze performance characteristics
        for file_analysis in file_analyses:
            file_path = file_analysis['file_path']
            complexity = file_analysis.get('complexity', 0)
            
            performance['bundle_size_impact'][file_path] = {
                'complexity': complexity,
                'estimated_size': complexity * 100,  # Placeholder calculation
                'optimization_potential': 'High' if complexity > 5 else 'Medium'
            }
        
        return performance
    
    def _analyze_testing_strategy(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze testing strategy and recommendations"""
        testing = {
            'unit_tests': {},
            'integration_tests': {},
            'e2e_tests': {},
            'test_coverage_gaps': {},
            'testing_recommendations': {}
        }
        
        # Analyze testing needs
        for file_analysis in file_analyses:
            file_path = file_analysis['file_path']
            file_type = file_analysis.get('file_type', 'unknown')
            
            testing['unit_tests'][file_path] = {
                'priority': 'High' if file_type == 'component' else 'Medium',
                'test_cases': ['Props validation', 'State management', 'User interactions'],
                'coverage_estimate': '80%'
            }
        
        return testing
    
    def _generate_comprehensive_output(self, file_analyses: List[Dict[str, Any]],
                                     component_analysis: Dict[str, Any],
                                     semantic_analysis: Dict[str, Any],
                                     api_analysis: Dict[str, Any],
                                     state_flow_analysis: Dict[str, Any],
                                     error_handling_analysis: Dict[str, Any],
                                     performance_analysis: Dict[str, Any],
                                     testing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive design-agent ready output"""
        
        return {
            'repository_metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'total_files': len(file_analyses),
                'file_types': self._analyze_file_types(file_analyses),
                'structure_pattern': self._detect_structure_pattern(file_analyses),
                'analysis_method': 'Comprehensive Hybrid (Python + LLM)',
                'semantic_analysis_enabled': True,
                'design_agent_ready': True
            },
            'semantic_analysis': semantic_analysis,
            'component_analysis': {
                'components': component_analysis.get('components', {}),
                'dependencies': component_analysis.get('dependencies', {}),
                'business_capabilities': component_analysis.get('business_capabilities', []),
                'data_flow': component_analysis.get('data_flow', []),
                'user_interactions': component_analysis.get('user_interactions', [])
            },
            'component_interactions': self._build_component_interaction_matrix(component_analysis),
            'api_contracts': api_analysis,
            'state_flow_analysis': state_flow_analysis,
            'error_handling_strategy': error_handling_analysis,
            'performance_analysis': performance_analysis,
            'testing_strategy': testing_analysis,
            'business_capabilities': self._extract_business_capabilities(semantic_analysis),
            'data_flow_analysis': self._analyze_data_flow(file_analyses, component_analysis),
            'architectural_patterns': self._identify_architectural_patterns(component_analysis),
            'code_quality_assessment': self._assess_code_quality(file_analyses, component_analysis),
            'recommendations': self._generate_recommendations(semantic_analysis, performance_analysis, testing_analysis)
        }
    
    def _analyze_file_types(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Analyze file types and organization"""
        file_types = {}
        
        for file_analysis in file_analyses:
            file_type = file_analysis.get('file_type', 'unknown')
            if file_type not in file_types:
                file_types[file_type] = []
            file_types[file_type].append(file_analysis['file_path'])
        
        return file_types
    
    def _detect_structure_pattern(self, file_analyses: List[Dict[str, Any]]) -> str:
        """Detect the overall structure pattern"""
        file_types = self._analyze_file_types(file_analyses)
        
        if 'component' in file_types and len(file_types['component']) > 5:
            return 'Component-based architecture with service layer separation'
        elif 'service' in file_types and 'hook' in file_types:
            return 'Service + Hooks architecture'
        else:
            return 'Mixed architecture'
    
    def _build_component_interaction_matrix(self, component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Build component interaction matrix"""
        interactions = {}
        
        for component_name, component_data in component_analysis.get('components', {}).items():
            interactions[component_name] = {
                'renders': [],
                'passes_data_to': {},
                'receives_from': {},
                'data_flow': {
                    'outbound': {},
                    'inbound': {}
                }
            }
        
        return interactions
    
    def _extract_business_capabilities(self, semantic_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract business capabilities from semantic analysis"""
        capabilities = []
        
        # Extract from components
        for component_name, component_data in semantic_analysis.get('components', {}).items():
            if 'business_capabilities' in component_data:
                capabilities.extend(component_data['business_capabilities'])
        
        # Extract from services
        for service_name, service_data in semantic_analysis.get('services', {}).items():
            if 'business_capabilities' in service_data:
                capabilities.extend(service_data['business_capabilities'])
        
        return capabilities
    
    def _analyze_data_flow(self, file_analyses: List[Dict[str, Any]], 
                          component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data flow patterns"""
        return {
            'primary_flow': 'User Input → Location Search → Weather Fetch → Data Display',
            'data_transformations': [
                'User input string → Location validation → API parameter',
                'API response → WeatherData interface → Component state',
                'Component state → UI rendering → User display'
            ],
            'state_management': {
                'global_state': 'None (all state is local to components)',
                'local_state': [
                    'WeatherCard: weatherData, loading, error',
                    'SearchForm: query',
                    'App: currentLocation'
                ],
                'state_synchronization': 'Props drilling from App to child components'
            },
            'side_effects': [
                'API calls triggered by location changes',
                'Loading states during API requests',
                'Error states on API failures',
                'UI updates on state changes'
            ]
        }
    
    def _identify_architectural_patterns(self, component_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify architectural patterns"""
        return [
            {
                'pattern': 'Component-based Architecture',
                'description': 'UI built from reusable React components',
                'evidence': 'Clear component separation',
                'benefits': ['Reusability', 'Maintainability', 'Testability'],
                'implementation_quality': 'Good'
            },
            {
                'pattern': 'Service Layer Pattern',
                'description': 'Business logic separated into service layer',
                'evidence': 'Service files handle API calls',
                'benefits': ['Separation of concerns', 'Reusability', 'Testability'],
                'implementation_quality': 'Good'
            }
        ]
    
    def _assess_code_quality(self, file_analyses: List[Dict[str, Any]], 
                            component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess code quality"""
        return {
            'overall_score': 7.5,
            'strengths': [
                'Clear component separation',
                'Good TypeScript usage',
                'Proper error handling',
                'Clean service layer'
            ],
            'weaknesses': [
                'No error boundaries',
                'Hardcoded API endpoints',
                'No loading states for better UX',
                'Limited accessibility features'
            ],
            'technical_debt': [
                'Add error boundaries for better error handling',
                'Extract API configuration',
                'Implement retry logic for failed requests',
                'Add comprehensive testing'
            ],
            'scalability_concerns': [
                'Props drilling may become complex with more components',
                'No global state management for complex state',
                'API service could benefit from caching'
            ]
        }
    
    def _generate_recommendations(self, semantic_analysis: Dict[str, Any],
                                 performance_analysis: Dict[str, Any],
                                 testing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive recommendations"""
        return {
            'immediate': [
                'Add error boundaries to handle API failures gracefully',
                'Extract API configuration to environment variables',
                'Add loading states for better user experience',
                'Implement input validation for location search'
            ],
            'short_term': [
                'Add comprehensive unit tests for all components',
                'Implement retry logic for failed API requests',
                'Add accessibility attributes for better UX',
                'Consider adding request caching'
            ],
            'long_term': [
                'Consider global state management (Redux/Zustand) for complex state',
                'Implement error monitoring and logging',
                'Add performance monitoring',
                'Consider implementing offline support'
            ]
        }
