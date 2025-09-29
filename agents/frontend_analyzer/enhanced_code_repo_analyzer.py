"""
Enhanced Hybrid Code Repository Analyzer Agent
Combines fast Python tools with LLM semantic analysis for comprehensive code understanding
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

# Local imports
from .tools.react_ast_parser import ReactASTParser
from .tools.component_analyzer import ComponentAnalyzer

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EnhancedCodeRepositoryAnalyzerAgent:
    """
    Enhanced Hybrid Code Repository Analyzer Agent for React/TypeScript Applications
    
    Features:
    - Fast Python tools for structural analysis
    - LLM agents for semantic understanding of code chunks
    - Chunk-by-chunk analysis for better context
    - Comprehensive business logic extraction
    - Architectural pattern detection
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
        
        # Initialize analysis tools
        self.ast_parser = ReactASTParser()
        self.component_analyzer = ComponentAnalyzer()
        
        self.logger.info("Enhanced Code Repository Analyzer Agent initialized")
    
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

Provide detailed, structured analysis focusing on:
- Component purpose and business meaning
- Props analysis with business context
- State management patterns and business logic
- Hooks usage and lifecycle management
- User interaction patterns
- Dependencies and data flow
- Code quality assessment

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

Focus on:
- Business rules and constraints
- User interaction flows
- Data flow and transformations
- API contracts and service boundaries
- Business capabilities and features
- Domain concepts and terminology
- Error handling and business logic
- Success metrics and validation rules

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

Provide architectural insights for system design and improvement.
"""
    
    def analyze_repository(self, repo_path: str, file_patterns: List[str] = None) -> Dict[str, Any]:
        """
        Analyze a React/TypeScript repository using hybrid approach
        
        Args:
            repo_path: Path to the repository
            file_patterns: List of file patterns to analyze
        
        Returns:
            Comprehensive analysis with semantic insights
        """
        if file_patterns is None:
            file_patterns = ['*.tsx', '*.ts', '*.jsx', '*.js']
        
        self.logger.info(f"Analyzing repository with hybrid approach: {repo_path}")
        
        try:
            # Phase 1: Fast Python Analysis
            print("🔍 Phase 1: Fast Python structural analysis...")
            file_analyses = self._analyze_files(repo_path, file_patterns)
            
            # Phase 2: Chunk-by-Chunk LLM Analysis
            print("🧠 Phase 2: Chunk-by-chunk LLM semantic analysis...")
            semantic_analysis = self._run_chunk_analysis(file_analyses)
            
            # Phase 3: Component Analysis
            print("🏗️ Phase 3: Component relationship analysis...")
            component_analysis = self.component_analyzer.analyze_components(file_analyses)
            
            # Phase 4: Business Logic Extraction
            print("💼 Phase 4: Business logic and workflow extraction...")
            business_analysis = self._extract_business_logic(file_analyses)
            
            # Phase 5: Architecture Analysis
            print("🏛️ Phase 5: Architecture and pattern analysis...")
            architecture_analysis = self._analyze_architecture(file_analyses, component_analysis)
            
            # Phase 6: LLM Synthesis
            print("🤖 Phase 6: High-level LLM synthesis...")
            llm_insights = self._run_llm_synthesis(
                file_analyses, component_analysis, business_analysis, architecture_analysis, semantic_analysis
            )
            
            # Phase 7: Generate Enhanced Output
            print("📋 Phase 7: Generating enhanced structured output...")
            structured_output = self._generate_enhanced_output(
                file_analyses, component_analysis, business_analysis, 
                architecture_analysis, semantic_analysis, llm_insights
            )
            
            return structured_output
            
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
    
    def _run_chunk_analysis(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run chunk-by-chunk LLM analysis on code components"""
        semantic_analysis = {
            'components': {},
            'services': {},
            'business_capabilities': [],
            'data_flow_analysis': {},
            'user_interactions': [],
            'architectural_patterns': []
        }
        
        for file_analysis in file_analyses:
            file_path = file_analysis['file_path']
            file_type = file_analysis.get('file_type', 'unknown')
            
            print(f"   📄 Analyzing chunks in: {Path(file_path).name}")
            
            # Analyze components
            for component in file_analysis.get('components', []):
                component_analysis = self._analyze_component_chunk(component, file_analysis)
                if component_analysis:
                    semantic_analysis['components'][component['name']] = component_analysis
            
            # Analyze services
            for service in file_analysis.get('services', []):
                service_analysis = self._analyze_service_chunk(service, file_analysis)
                if service_analysis:
                    semantic_analysis['services'][service['name']] = service_analysis
            
            # Analyze business logic chunks
            business_chunks = self._extract_business_chunks(file_analysis)
            for chunk in business_chunks:
                business_analysis = self._analyze_business_chunk(chunk, file_analysis)
                if business_analysis:
                    semantic_analysis['business_capabilities'].extend(business_analysis.get('capabilities', []))
                    semantic_analysis['user_interactions'].extend(business_analysis.get('interactions', []))
        
        return semantic_analysis
    
    def _analyze_component_chunk(self, component: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single component chunk with LLM"""
        try:
            # Prepare component context
            component_context = {
                'name': component['name'],
                'type': component['type'],
                'props': component.get('props', []),
                'state': component.get('state', []),
                'hooks': component.get('hooks', []),
                'business_logic': component.get('business_logic', []),
                'file_path': file_analysis['file_path'],
                'file_type': file_analysis.get('file_type', 'unknown')
            }
            
            prompt = f"""
Analyze this React component and provide detailed semantic insights:

Component: {component['name']}
File: {file_analysis['file_path']}
Type: {component['type']}

Props: {json.dumps(component.get('props', []), indent=2)}
State: {json.dumps(component.get('state', []), indent=2)}
Hooks: {json.dumps(component.get('hooks', []), indent=2)}
Business Logic: {json.dumps(component.get('business_logic', []), indent=2)}

Please provide:
1. Component purpose and business role
2. Detailed props analysis with business meaning
3. State management patterns and business logic
4. Hooks usage and lifecycle management
5. User interaction patterns
6. Dependencies and data flow
7. Code quality assessment
8. Business capabilities provided

Return as structured JSON.
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
            self.logger.error(f"Error analyzing component chunk {component['name']}: {e}")
            return None
    
    def _analyze_service_chunk(self, service: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single service chunk with LLM"""
        try:
            # Prepare service context
            service_context = {
                'name': service['name'],
                'type': service['type'],
                'methods': service.get('methods', []),
                'dependencies': service.get('dependencies', []),
                'file_path': file_analysis['file_path'],
                'file_type': file_analysis.get('file_type', 'unknown')
            }
            
            prompt = f"""
Analyze this service/utility and provide detailed semantic insights:

Service: {service['name']}
File: {file_analysis['file_path']}
Type: {service['type']}

Methods: {json.dumps(service.get('methods', []), indent=2)}
Dependencies: {json.dumps(service.get('dependencies', []), indent=2)}

Please provide:
1. Service purpose and business role
2. Method analysis with business meaning
3. API contracts and data transformations
4. Dependencies and integration points
5. Error handling patterns
6. Business capabilities provided
7. Code quality assessment

Return as structured JSON.
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
            self.logger.error(f"Error analyzing service chunk {service['name']}: {e}")
            return None
    
    def _extract_business_chunks(self, file_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract business logic chunks from file analysis"""
        chunks = []
        
        # Extract business logic patterns
        business_logic = file_analysis.get('business_logic', [])
        for logic in business_logic:
            chunks.append({
                'type': 'business_logic',
                'pattern': logic['type'],
                'method': logic.get('method', ''),
                'line': logic.get('line', 0),
                'context': logic
            })
        
        # Extract user interactions
        user_interactions = file_analysis.get('user_interactions', [])
        for interaction in user_interactions:
            chunks.append({
                'type': 'user_interaction',
                'pattern': interaction.get('pattern', ''),
                'line': interaction.get('line', 0),
                'context': interaction
            })
        
        return chunks
    
    def _analyze_business_chunk(self, chunk: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single business logic chunk with LLM"""
        try:
            prompt = f"""
Analyze this business logic chunk and provide semantic insights:

Chunk Type: {chunk['type']}
File: {file_analysis['file_path']}
Pattern: {chunk.get('pattern', '')}
Line: {chunk.get('line', 0)}
Context: {json.dumps(chunk.get('context', {}), indent=2)}

Please provide:
1. Business purpose and meaning
2. Business rules and constraints
3. User workflow implications
4. Data flow and transformations
5. Error handling and validation
6. Success metrics and outcomes

Return as structured JSON.
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
                        'type': chunk['type'],
                        'purpose': content,
                        'analysis_type': 'business_logic',
                        'file_path': file_analysis['file_path']
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing business chunk: {e}")
            return None
    
    def _extract_business_logic(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract business logic patterns from file analyses"""
        business_logic = {
            'api_calls': [],
            'state_management': [],
            'event_handling': [],
            'data_transformations': [],
            'user_workflows': []
        }
        
        for file_analysis in file_analyses:
            file_business_logic = file_analysis.get('business_logic', [])
            
            for logic in file_business_logic:
                if logic['type'] == 'api_call':
                    business_logic['api_calls'].append({
                        'file': file_analysis['file_path'],
                        'method': logic['method'],
                        'line': logic['line']
                    })
                elif logic['type'] == 'state_management':
                    business_logic['state_management'].append({
                        'file': file_analysis['file_path'],
                        'pattern': logic['pattern'],
                        'line': logic['line']
                    })
                elif logic['type'] == 'event_handling':
                    business_logic['event_handling'].append({
                        'file': file_analysis['file_path'],
                        'pattern': logic['pattern'],
                        'line': logic['line']
                    })
        
        return business_logic
    
    def _analyze_architecture(self, file_analyses: List[Dict[str, Any]], 
                            component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze architectural patterns and decisions"""
        architecture = {
            'patterns': component_analysis.get('architecture_patterns', []),
            'file_structure': self._analyze_file_structure(file_analyses),
            'dependency_graph': self._build_dependency_graph(component_analysis),
            'complexity_metrics': self._calculate_complexity_metrics(file_analyses)
        }
        
        return architecture
    
    def _analyze_file_structure(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the file structure and organization"""
        file_types = {}
        
        for file_analysis in file_analyses:
            file_type = file_analysis.get('file_type', 'unknown')
            if file_type not in file_types:
                file_types[file_type] = []
            file_types[file_type].append(file_analysis['file_path'])
        
        return {
            'file_types': file_types,
            'total_files': len(file_analyses),
            'structure_pattern': self._detect_structure_pattern(file_types)
        }
    
    def _detect_structure_pattern(self, file_types: Dict[str, List[str]]) -> str:
        """Detect the overall structure pattern"""
        if 'component' in file_types and len(file_types['component']) > 5:
            return 'Component-based architecture'
        elif 'service' in file_types and 'hook' in file_types:
            return 'Service + Hooks architecture'
        else:
            return 'Mixed architecture'
    
    def _build_dependency_graph(self, component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Build a dependency graph of components"""
        dependencies = component_analysis.get('dependencies', {})
        
        nodes = []
        edges = []
        
        for component_name, dep_data in dependencies.items():
            nodes.append({
                'id': component_name,
                'type': 'component',
                'dependencies': dep_data.get('dependencies', []),
                'dependents': dep_data.get('dependents', [])
            })
            
            for dep in dep_data.get('dependencies', []):
                edges.append({
                    'from': dep,
                    'to': component_name,
                    'type': 'depends_on'
                })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'circular_dependencies': self._detect_circular_dependencies(dependencies)
        }
    
    def _detect_circular_dependencies(self, dependencies: Dict[str, Any]) -> List[List[str]]:
        """Detect circular dependencies between components"""
        circular = []
        
        def has_cycle(component: str, visited: set, rec_stack: set) -> bool:
            visited.add(component)
            rec_stack.add(component)
            
            for dep in dependencies.get(component, {}).get('dependencies', []):
                if dep not in visited:
                    if has_cycle(dep, visited, rec_stack):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(component)
            return False
        
        for component in dependencies:
            if component not in [item for cycle in circular for item in cycle]:
                visited = set()
                rec_stack = set()
                if has_cycle(component, visited, rec_stack):
                    # Find the actual cycle
                    cycle = self._find_cycle(component, dependencies)
                    if cycle:
                        circular.append(cycle)
        
        return circular
    
    def _find_cycle(self, start: str, dependencies: Dict[str, Any]) -> List[str]:
        """Find the actual cycle in dependencies"""
        def dfs(node: str, path: List[str]) -> List[str]:
            if node in path:
                return path[path.index(node):] + [node]
            
            for dep in dependencies.get(node, {}).get('dependencies', []):
                result = dfs(dep, path + [node])
                if result:
                    return result
            return []
        
        return dfs(start, [])
    
    def _calculate_complexity_metrics(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate complexity metrics for the codebase"""
        total_complexity = 0
        file_complexities = []
        component_complexities = []
        
        for file_analysis in file_analyses:
            file_complexity = file_analysis.get('complexity', 0)
            total_complexity += file_complexity
            file_complexities.append({
                'file': file_analysis['file_path'],
                'complexity': file_complexity
            })
            
            for component in file_analysis.get('components', []):
                component_complexities.append({
                    'component': component['name'],
                    'file': file_analysis['file_path'],
                    'complexity': component.get('complexity', 0)
                })
        
        return {
            'total_complexity': total_complexity,
            'average_complexity': total_complexity / len(file_analyses) if file_analyses else 0,
            'file_complexities': file_complexities,
            'component_complexities': component_complexities,
            'most_complex_files': sorted(file_complexities, key=lambda x: x['complexity'], reverse=True)[:5],
            'most_complex_components': sorted(component_complexities, key=lambda x: x['complexity'], reverse=True)[:5]
        }
    
    def _run_llm_synthesis(self, file_analyses: List[Dict[str, Any]], 
                         component_analysis: Dict[str, Any],
                         business_analysis: Dict[str, Any],
                         architecture_analysis: Dict[str, Any],
                         semantic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run high-level LLM synthesis"""
        
        # Prepare comprehensive input for LLM
        analysis_summary = {
            'total_files': len(file_analyses),
            'total_components': len(component_analysis.get('components', {})),
            'semantic_components': len(semantic_analysis.get('components', {})),
            'semantic_services': len(semantic_analysis.get('services', {})),
            'business_capabilities': semantic_analysis.get('business_capabilities', []),
            'architecture_patterns': architecture_analysis.get('patterns', []),
            'complexity_metrics': architecture_analysis.get('complexity_metrics', {}),
            'file_structure': architecture_analysis.get('file_structure', {})
        }
        
        prompt = f"""
Analyze this React/TypeScript codebase and provide comprehensive architectural insights:

{json.dumps(analysis_summary, indent=2)}

Please provide:
1. Overall architecture assessment and patterns
2. Key business capabilities and domain understanding
3. Component relationships and data flow
4. Design patterns and architectural decisions
5. Code quality assessment and technical debt
6. Scalability and maintainability concerns
7. Recommendations for improvement
8. Integration points and external dependencies

Focus on providing actionable insights for design and development teams.
"""
        
        try:
            response = self.architecture_agent.run(
                message=prompt,
                max_turns=1
            )
            
            # Process the response
            if response.messages:
                last_message = response.messages[-1]
                content = last_message.content if hasattr(last_message, 'content') else str(last_message)
                
                return {
                    'llm_insights': content,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            
            return {'llm_insights': 'No insights generated', 'analysis_timestamp': datetime.now().isoformat()}
            
        except Exception as e:
            self.logger.error(f"Error in LLM synthesis: {e}")
            return {'llm_insights': f'Error: {str(e)}', 'analysis_timestamp': datetime.now().isoformat()}
    
    def _generate_enhanced_output(self, file_analyses: List[Dict[str, Any]],
                                 component_analysis: Dict[str, Any],
                                 business_analysis: Dict[str, Any],
                                 architecture_analysis: Dict[str, Any],
                                 semantic_analysis: Dict[str, Any],
                                 llm_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the enhanced structured output"""
        
        return {
            'repository_metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'total_files': len(file_analyses),
                'file_types': architecture_analysis.get('file_structure', {}).get('file_types', {}),
                'structure_pattern': architecture_analysis.get('file_structure', {}).get('structure_pattern', 'Unknown'),
                'analysis_method': 'Hybrid (Python + LLM)',
                'semantic_analysis_enabled': True
            },
            'semantic_analysis': semantic_analysis,
            'component_analysis': {
                'components': component_analysis.get('components', {}),
                'dependencies': component_analysis.get('dependencies', {}),
                'business_capabilities': component_analysis.get('business_capabilities', []),
                'data_flow': component_analysis.get('data_flow', []),
                'user_interactions': component_analysis.get('user_interactions', [])
            },
            'business_logic': business_analysis,
            'architecture_analysis': {
                'patterns': architecture_analysis.get('patterns', []),
                'dependency_graph': architecture_analysis.get('dependency_graph', {}),
                'complexity_metrics': architecture_analysis.get('complexity_metrics', {}),
                'file_structure': architecture_analysis.get('file_structure', {})
            },
            'llm_insights': llm_insights.get('llm_insights', ''),
            'design_agent_ready': True,
            'enhanced_analysis': True
        }
