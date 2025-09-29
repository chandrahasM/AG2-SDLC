"""
Code Repository Analyzer Agent
Analyzes React/TypeScript codebase structure, components, and business logic
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

class CodeRepositoryAnalyzerAgent:
    """
    Code Repository Analyzer Agent for React/TypeScript Applications
    
    Analyzes:
    - Component structure and relationships
    - TypeScript interfaces and types
    - Business logic and data flow
    - Dependencies and imports
    - User interactions and workflows
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
        
        # Create the analyzer agent
        self.analyzer_agent = ConversableAgent(
            name="code_repo_analyzer",
            system_message=self._get_analyzer_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        # Initialize analysis tools
        self.ast_parser = ReactASTParser()
        self.component_analyzer = ComponentAnalyzer()
        
        self.logger.info("Code Repository Analyzer Agent initialized")
    
    def _get_analyzer_system_message(self) -> str:
        """System message for the code repository analyzer agent"""
        return """
You are a Code Repository Analyzer Agent specialized in React/TypeScript applications.

Your responsibilities:
1. Analyze React component structure, props, state, and hooks
2. Extract TypeScript interfaces and type definitions
3. Identify business logic patterns and data flow
4. Map component dependencies and relationships
5. Analyze user interactions and workflows
6. Detect architectural patterns and design decisions

You work with structured analysis tools to provide comprehensive insights about the codebase structure, making it ready for design analysis and code generation.

Always provide detailed, structured output that can be consumed by downstream design agents.
"""
    
    def analyze_repository(self, repo_path: str, file_patterns: List[str] = None) -> Dict[str, Any]:
        """
        Analyze a React/TypeScript repository
        
        Args:
            repo_path: Path to the repository
            file_patterns: List of file patterns to analyze (e.g., ['*.tsx', '*.ts'])
        
        Returns:
            Comprehensive analysis of the repository
        """
        if file_patterns is None:
            file_patterns = ['*.tsx', '*.ts', '*.jsx', '*.js']
        
        self.logger.info(f"Analyzing repository: {repo_path}")
        
        try:
            # Phase 1: File Discovery and Analysis
            print("🔍 Phase 1: Discovering and analyzing files...")
            file_analyses = self._analyze_files(repo_path, file_patterns)
            
            # Phase 2: Component Analysis
            print("🏗️ Phase 2: Analyzing components and relationships...")
            component_analysis = self.component_analyzer.analyze_components(file_analyses)
            
            # Phase 3: Business Logic Extraction
            print("💼 Phase 3: Extracting business logic and workflows...")
            business_analysis = self._extract_business_logic(file_analyses)
            
            # Phase 4: Architecture Analysis
            print("🏛️ Phase 4: Analyzing architecture and patterns...")
            architecture_analysis = self._analyze_architecture(file_analyses, component_analysis)
            
            # Phase 5: LLM Synthesis
            print("🤖 Phase 5: LLM synthesis and insights...")
            llm_insights = self._run_llm_analysis(
                file_analyses, component_analysis, business_analysis, architecture_analysis
            )
            
            # Phase 6: Generate Structured Output
            print("📋 Phase 6: Generating structured output...")
            structured_output = self._generate_structured_output(
                file_analyses, component_analysis, business_analysis, 
                architecture_analysis, llm_insights
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
    
    def _run_llm_analysis(self, file_analyses: List[Dict[str, Any]], 
                         component_analysis: Dict[str, Any],
                         business_analysis: Dict[str, Any],
                         architecture_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run LLM analysis for high-level insights"""
        
        # Prepare focused input for LLM
        analysis_summary = {
            'total_files': len(file_analyses),
            'total_components': len(component_analysis.get('components', {})),
            'business_capabilities': component_analysis.get('business_capabilities', []),
            'architecture_patterns': architecture_analysis.get('patterns', []),
            'complexity_metrics': architecture_analysis.get('complexity_metrics', {}),
            'file_structure': architecture_analysis.get('file_structure', {})
        }
        
        prompt = f"""
Analyze this React/TypeScript codebase and provide high-level insights:

{json.dumps(analysis_summary, indent=2)}

Please provide:
1. Overall architecture assessment
2. Key business capabilities identified
3. Design patterns and architectural decisions
4. Potential areas for improvement
5. Recommendations for maintainability and scalability
"""
        
        try:
            response = self.analyzer_agent.run(
                message=prompt,
                max_turns=1
            )
            
            # Process the response
            messages = response.messages
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                else:
                    content = str(last_message)
                
                return {
                    'llm_insights': content,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            
            return {'llm_insights': 'No insights generated', 'analysis_timestamp': datetime.now().isoformat()}
            
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {e}")
            return {'llm_insights': f'Error: {str(e)}', 'analysis_timestamp': datetime.now().isoformat()}
    
    def _generate_structured_output(self, file_analyses: List[Dict[str, Any]],
                                  component_analysis: Dict[str, Any],
                                  business_analysis: Dict[str, Any],
                                  architecture_analysis: Dict[str, Any],
                                  llm_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final structured output"""
        
        return {
            'repository_metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'total_files': len(file_analyses),
                'file_types': architecture_analysis.get('file_structure', {}).get('file_types', {}),
                'structure_pattern': architecture_analysis.get('file_structure', {}).get('structure_pattern', 'Unknown')
            },
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
            'design_agent_ready': True
        }
