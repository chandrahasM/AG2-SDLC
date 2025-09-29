"""
Frontend Multi-Agent Workflow Orchestrator
Coordinates all agents for React/TypeScript analysis and code generation
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Import all agents
from .code_repo_analyzer import CodeRepositoryAnalyzerAgent
from .design_analyzer import DesignAnalyzerAgent
from .design_architect import DesignArchitectAgent
from .code_generation import CodeGenerationAgent

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class FrontendWorkflowOrchestrator:
    """
    Frontend Multi-Agent Workflow Orchestrator
    
    Coordinates the complete workflow:
    1. Code Repository Analysis
    2. Design Gap Analysis
    3. Design Architecture Updates
    4. Code Generation
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        self.logger = logging.getLogger(__name__)
        
        # Initialize all agents
        self.code_repo_analyzer = CodeRepositoryAnalyzerAgent(model_name, temperature)
        self.design_analyzer = DesignAnalyzerAgent(model_name, temperature)
        self.design_architect = DesignArchitectAgent(model_name, temperature)
        self.code_generator = CodeGenerationAgent(model_name, temperature)
        
        self.logger.info("Frontend Workflow Orchestrator initialized")
    
    def run_complete_workflow(self, repo_path: str, new_requirements: Dict[str, Any],
                            existing_design: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the complete frontend analysis and code generation workflow
        
        Args:
            repo_path: Path to the React/TypeScript repository
            new_requirements: New requirements to implement
            existing_design: Optional existing design document
        
        Returns:
            Complete workflow results including generated code
        """
        self.logger.info("Starting complete frontend workflow...")
        
        try:
            # Phase 1: Code Repository Analysis
            print("🔍 Phase 1: Analyzing code repository...")
            print(f"   📁 Repository path: {repo_path}")
            print(f"   📋 File patterns: ['*.tsx', '*.ts', '*.jsx', '*.js']")
            
            code_analysis = self.code_repo_analyzer.analyze_repository(repo_path)
            
            # Log Code Repository Analyzer outputs
            print(f"   ✅ Code Analysis Results:")
            print(f"      - Files analyzed: {code_analysis.get('repository_metadata', {}).get('total_files', 0)}")
            print(f"      - Components found: {len(code_analysis.get('component_analysis', {}).get('components', {}))}")
            print(f"      - Business capabilities: {len(code_analysis.get('component_analysis', {}).get('business_capabilities', []))}")
            print(f"      - Architecture patterns: {len(code_analysis.get('architecture_analysis', {}).get('patterns', []))}")
            
            # Phase 2: Design Gap Analysis
            print("\n📋 Phase 2: Analyzing design gaps...")
            if existing_design is None:
                existing_design = self._load_existing_design(repo_path)
            
            print(f"   📥 Design Analyzer Inputs:")
            print(f"      - Existing design features: {len(existing_design.get('features', []))}")
            print(f"      - Existing components: {len(existing_design.get('components', []))}")
            print(f"      - New requirements features: {len(new_requirements.get('features', []))}")
            print(f"      - New requirements components: {len(new_requirements.get('components', []))}")
            
            gap_analysis = self.design_analyzer.analyze_design_gaps(
                existing_design, new_requirements, code_analysis
            )
            
            # Log Design Analyzer outputs
            print(f"   ✅ Gap Analysis Results:")
            print(f"      - Missing features: {len(gap_analysis.get('gap_analysis', {}).get('missing_features', []))}")
            print(f"      - Modified features: {len(gap_analysis.get('gap_analysis', {}).get('modified_features', []))}")
            print(f"      - New components needed: {len(gap_analysis.get('gap_analysis', {}).get('new_components_needed', []))}")
            print(f"      - Components to modify: {len(gap_analysis.get('gap_analysis', {}).get('existing_components_to_modify', []))}")
            print(f"      - API changes: {len(gap_analysis.get('gap_analysis', {}).get('api_changes', []))}")
            
            # Phase 3: Design Architecture Updates
            print("\n🏗️ Phase 3: Updating design architecture...")
            print(f"   📥 Design Architect Inputs:")
            print(f"      - Gap analysis results: {len(gap_analysis.get('gap_analysis', {}))} gap categories")
            print(f"      - Impact analysis results: {len(gap_analysis.get('impact_analysis', {}))} impact categories")
            
            design_updates = self.design_architect.update_design_document(
                existing_design, 
                gap_analysis.get('gap_analysis', {}),
                gap_analysis.get('impact_analysis', {})
            )
            
            # Log Design Architect outputs
            print(f"   ✅ Design Updates Results:")
            print(f"      - New components designed: {len(design_updates.get('new_components', []))}")
            print(f"      - Updated components designed: {len(design_updates.get('updated_components', []))}")
            print(f"      - API designs created: {len(design_updates.get('api_designs', []))}")
            print(f"      - Implementation phases: {len(design_updates.get('implementation_plan', {}).get('phases', []))}")
            
            # Phase 4: Code Generation
            print("\n💻 Phase 4: Generating code...")
            print(f"   📥 Code Generator Inputs:")
            print(f"      - Design specifications: {len(design_updates.get('updated_design', {}))} design elements")
            print(f"      - Code analysis: {code_analysis.get('repository_metadata', {}).get('total_files', 0)} analyzed files")
            
            generated_code = self.code_generator.generate_code(
                design_updates.get('updated_design', {}),
                code_analysis
            )
            
            # Log Code Generator outputs
            print(f"   ✅ Code Generation Results:")
            print(f"      - New component files: {len(generated_code.get('new_components', []))}")
            print(f"      - Updated component files: {len(generated_code.get('updated_components', []))}")
            print(f"      - API service files: {len(generated_code.get('api_services', []))}")
            print(f"      - TypeScript type files: {len(generated_code.get('typescript_types', []))}")
            print(f"      - Custom hook files: {len(generated_code.get('custom_hooks', []))}")
            print(f"      - Test files: {len(generated_code.get('test_files', []))}")
            
            # Phase 5: Generate Workflow Summary
            print("\n📊 Phase 5: Generating workflow summary...")
            workflow_summary = self._generate_workflow_summary(
                code_analysis, gap_analysis, design_updates, generated_code
            )
            
            # Create compact output for context window
            compact_output = self._create_compact_output(
                code_analysis, gap_analysis, design_updates, generated_code, workflow_summary
            )
            
            return {
                'workflow_status': 'completed',
                'code_analysis': code_analysis,
                'gap_analysis': gap_analysis,
                'design_updates': design_updates,
                'generated_code': generated_code,
                'workflow_summary': workflow_summary,
                'compact_output': compact_output,  # For downstream processing
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in complete workflow: {e}")
            return {
                'workflow_status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _load_existing_design(self, repo_path: str) -> Dict[str, Any]:
        """Load existing design document from repository"""
        design_file_path = os.path.join(repo_path, 'design-document.md')
        
        if os.path.exists(design_file_path):
            try:
                with open(design_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse markdown design document
                return self._parse_design_document(content)
            except Exception as e:
                self.logger.warning(f"Could not load design document: {e}")
        
        # Return default design structure
        return {
            'features': [],
            'components': [],
            'api_endpoints': [],
            'data_models': [],
            'user_stories': [],
            'user_flows': [],
            'architecture': {},
            'technical_specs': {}
        }
    
    def _parse_design_document(self, content: str) -> Dict[str, Any]:
        """Parse markdown design document into structured format"""
        # Simple markdown parsing - can be enhanced
        lines = content.split('\n')
        
        design = {
            'features': [],
            'components': [],
            'api_endpoints': [],
            'data_models': [],
            'user_stories': [],
            'user_flows': [],
            'architecture': {},
            'technical_specs': {}
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('## Features'):
                current_section = 'features'
            elif line.startswith('## Components'):
                current_section = 'components'
            elif line.startswith('## API Endpoints'):
                current_section = 'api_endpoints'
            elif line.startswith('## Data Models'):
                current_section = 'data_models'
            elif line.startswith('## User Stories'):
                current_section = 'user_stories'
            elif line.startswith('## User Flows'):
                current_section = 'user_flows'
            elif line.startswith('## Technical Specifications'):
                current_section = 'technical_specs'
            elif line.startswith('## Architecture'):
                current_section = 'architecture'
            elif line.startswith('###') and current_section:
                # Parse subsection
                pass
            elif line.startswith('-') and current_section:
                # Parse list item
                if current_section in design:
                    design[current_section].append(line[1:].strip())
        
        return design
    
    def _generate_workflow_summary(self, code_analysis: Dict[str, Any],
                                 gap_analysis: Dict[str, Any],
                                 design_updates: Dict[str, Any],
                                 generated_code: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive workflow summary"""
        
        summary = {
            'workflow_overview': {
                'total_phases': 4,
                'status': 'completed',
                'duration': 'estimated 5-10 minutes'
            },
            'code_analysis_summary': {
                'total_files_analyzed': code_analysis.get('repository_metadata', {}).get('total_files', 0),
                'components_found': len(code_analysis.get('component_analysis', {}).get('components', {})),
                'business_capabilities': len(code_analysis.get('component_analysis', {}).get('business_capabilities', [])),
                'architecture_patterns': len(code_analysis.get('architecture_analysis', {}).get('patterns', []))
            },
            'gap_analysis_summary': {
                'missing_features': len(gap_analysis.get('gap_analysis', {}).get('missing_features', [])),
                'modified_features': len(gap_analysis.get('gap_analysis', {}).get('modified_features', [])),
                'new_components_needed': len(gap_analysis.get('gap_analysis', {}).get('new_components_needed', [])),
                'existing_components_to_modify': len(gap_analysis.get('gap_analysis', {}).get('existing_components_to_modify', [])),
                'api_changes': len(gap_analysis.get('gap_analysis', {}).get('api_changes', []))
            },
            'design_updates_summary': {
                'new_components_designed': len(design_updates.get('new_components', [])),
                'updated_components_designed': len(design_updates.get('updated_components', [])),
                'api_designs_created': len(design_updates.get('api_designs', [])),
                'implementation_phases': len(design_updates.get('implementation_plan', {}).get('phases', []))
            },
            'generated_code_summary': {
                'new_component_files': len(generated_code.get('new_components', [])),
                'updated_component_files': len(generated_code.get('updated_components', [])),
                'api_service_files': len(generated_code.get('api_services', [])),
                'typescript_type_files': len(generated_code.get('typescript_types', [])),
                'custom_hook_files': len(generated_code.get('custom_hooks', [])),
                'test_files': len(generated_code.get('test_files', [])),
                'documentation_files': len(generated_code.get('documentation', {}))
            },
            'recommendations': [
                'Review generated code for accuracy and completeness',
                'Test all new components and updated functionality',
                'Update existing tests to cover new features',
                'Review and update documentation as needed',
                'Consider performance implications of new features',
                'Plan deployment strategy for new components'
            ],
            'next_steps': [
                'Implement generated code in the project',
                'Run tests to ensure functionality works as expected',
                'Update project documentation',
                'Deploy changes to development environment',
                'Conduct user acceptance testing',
                'Plan production deployment'
            ]
        }
        
        return summary
    
    def _create_compact_output(self, code_analysis: Dict[str, Any],
                             gap_analysis: Dict[str, Any],
                             design_updates: Dict[str, Any],
                             generated_code: Dict[str, Any],
                             workflow_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Create a compact output suitable for downstream processing"""
        
        # Extract only essential business logic information
        compact_code_analysis = {
            'repository_metadata': {
                'total_files': code_analysis.get('repository_metadata', {}).get('total_files', 0),
                'file_types': code_analysis.get('repository_metadata', {}).get('file_types', {}),
                'structure_pattern': code_analysis.get('repository_metadata', {}).get('structure_pattern', 'Unknown')
            },
            'components': {
                'count': len(code_analysis.get('component_analysis', {}).get('components', {})),
                'list': list(code_analysis.get('component_analysis', {}).get('components', {}).keys()),
                'dependencies': code_analysis.get('component_analysis', {}).get('dependencies', {}),
                'business_capabilities': code_analysis.get('component_analysis', {}).get('business_capabilities', [])
            },
            'architecture_patterns': code_analysis.get('architecture_analysis', {}).get('patterns', []),
            'business_logic': {
                'api_calls': len(code_analysis.get('business_logic', {}).get('api_calls', [])),
                'state_management': len(code_analysis.get('business_logic', {}).get('state_management', [])),
                'event_handling': len(code_analysis.get('business_logic', {}).get('event_handling', []))
            }
        }
        
        # Extract essential gap analysis
        compact_gap_analysis = {
            'missing_features': gap_analysis.get('gap_analysis', {}).get('missing_features', []),
            'new_components_needed': gap_analysis.get('gap_analysis', {}).get('new_components_needed', []),
            'existing_components_to_modify': gap_analysis.get('gap_analysis', {}).get('existing_components_to_modify', []),
            'api_changes': gap_analysis.get('gap_analysis', {}).get('api_changes', []),
            'recommendations': gap_analysis.get('recommendations', [])
        }
        
        # Extract essential design updates
        compact_design_updates = {
            'new_components': design_updates.get('new_components', []),
            'updated_components': design_updates.get('updated_components', []),
            'api_designs': design_updates.get('api_designs', []),
            'implementation_plan': {
                'phases': design_updates.get('implementation_plan', {}).get('phases', []),
                'priority_order': design_updates.get('implementation_plan', {}).get('priority_order', [])
            }
        }
        
        # Extract essential generated code
        compact_generated_code = {
            'new_components': [
                {
                    'name': comp.get('component_name', ''),
                    'file_path': comp.get('file_path', ''),
                    'type': comp.get('type', 'component')
                } for comp in generated_code.get('new_components', [])
            ],
            'updated_components': [
                {
                    'name': comp.get('component_name', ''),
                    'file_path': comp.get('file_path', ''),
                    'changes': comp.get('changes', [])
                } for comp in generated_code.get('updated_components', [])
            ],
            'api_services': [
                {
                    'endpoint': api.get('endpoint', ''),
                    'method': api.get('method', 'GET'),
                    'file_path': api.get('file_path', '')
                } for api in generated_code.get('api_services', [])
            ],
            'typescript_types': [
                {
                    'type_name': type_file.get('type_name', ''),
                    'file_path': type_file.get('file_path', '')
                } for type_file in generated_code.get('typescript_types', [])
            ],
            'test_files': [
                {
                    'component_name': test.get('component_name', ''),
                    'file_path': test.get('file_path', ''),
                    'test_type': test.get('test_type', 'component')
                } for test in generated_code.get('test_files', [])
            ]
        }
        
        return {
            'code_analysis': compact_code_analysis,
            'gap_analysis': compact_gap_analysis,
            'design_updates': compact_design_updates,
            'generated_code': compact_generated_code,
            'workflow_summary': workflow_summary,
            'agent_flow': {
                'code_repo_analyzer': {
                    'input': 'Repository path and file patterns',
                    'output': f"Analyzed {compact_code_analysis['repository_metadata']['total_files']} files, found {compact_code_analysis['components']['count']} components"
                },
                'design_analyzer': {
                    'input': 'Existing design + new requirements + code analysis',
                    'output': f"Found {len(compact_gap_analysis['missing_features'])} missing features, {len(compact_gap_analysis['new_components_needed'])} new components needed"
                },
                'design_architect': {
                    'input': 'Gap analysis + impact analysis',
                    'output': f"Designed {len(compact_design_updates['new_components'])} new components, {len(compact_design_updates['api_designs'])} API designs"
                },
                'code_generator': {
                    'input': 'Design specifications + code analysis',
                    'output': f"Generated {len(compact_generated_code['new_components'])} component files, {len(compact_generated_code['test_files'])} test files"
                }
            }
        }
    
    def run_weather_app_example(self) -> Dict[str, Any]:
        """Run the complete workflow with the weather app example"""
        
        # Define new requirements for 7-day forecast
        new_requirements = {
            'features': [
                {
                    'name': '7-Day Weather Forecast',
                    'description': 'Display 7-day weather forecast with daily temperatures and conditions',
                    'priority': 'high',
                    'user_stories': [
                        {
                            'id': 'forecast_1',
                            'title': 'As a user, I want to see a 7-day weather forecast',
                            'description': 'I want to be able to view weather forecast for the next 7 days',
                            'acceptance_criteria': [
                                'User can see forecast for next 7 days',
                                'Each day shows temperature and condition',
                                'Forecast updates when location changes'
                            ],
                            'priority': 'high'
                        }
                    ]
                }
            ],
            'components': [
                {
                    'name': 'ForecastCard',
                    'type': 'component',
                    'description': 'Display forecast for a single day',
                    'dependencies': ['WeatherCard'],
                    'props': [
                        {'name': 'forecastData', 'type': 'ForecastData', 'required': True, 'description': 'Forecast data for the day'},
                        {'name': 'onDayClick', 'type': '() => void', 'required': False, 'description': 'Click handler for day selection'}
                    ],
                    'state': [
                        {'name': 'isSelected', 'type': 'boolean', 'default': False, 'description': 'Whether this day is selected'},
                        {'name': 'isHovered', 'type': 'boolean', 'default': False, 'description': 'Hover state'}
                    ]
                },
                {
                    'name': 'ForecastList',
                    'type': 'component',
                    'description': 'Display list of forecast cards',
                    'dependencies': ['ForecastCard'],
                    'props': [
                        {'name': 'forecasts', 'type': 'ForecastData[]', 'required': True, 'description': 'Array of forecast data'},
                        {'name': 'selectedDay', 'type': 'string', 'required': False, 'description': 'Currently selected day'}
                    ],
                    'state': [
                        {'name': 'selectedIndex', 'type': 'number', 'default': 0, 'description': 'Index of selected day'}
                    ]
                }
            ],
            'api_endpoints': [
                {
                    'endpoint': '/api/forecast',
                    'method': 'GET',
                    'description': 'Get 7-day weather forecast',
                    'parameters': [
                        {'name': 'location', 'type': 'string', 'required': True, 'description': 'Location for forecast'},
                        {'name': 'days', 'type': 'number', 'required': False, 'description': 'Number of forecast days', 'default': 7}
                    ],
                    'response_schema': {
                        'type': 'object',
                        'properties': {
                            'location': {'type': 'string'},
                            'forecast': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'date': {'type': 'string'},
                                        'temperature': {'type': 'number'},
                                        'condition': {'type': 'string'},
                                        'humidity': {'type': 'number'},
                                        'windSpeed': {'type': 'number'}
                                    }
                                }
                            }
                        }
                    }
                }
            ],
            'data_models': [
                {
                    'name': 'ForecastData',
                    'description': 'Data model for forecast information',
                    'properties': [
                        {'name': 'date', 'type': 'string', 'description': 'Date of the forecast'},
                        {'name': 'temperature', 'type': 'number', 'description': 'Temperature in Celsius'},
                        {'name': 'condition', 'type': 'string', 'description': 'Weather condition'},
                        {'name': 'humidity', 'type': 'number', 'description': 'Humidity percentage'},
                        {'name': 'windSpeed', 'type': 'number', 'description': 'Wind speed in km/h'}
                    ]
                }
            ],
            'user_flows': [
                {
                    'name': 'View 7-Day Forecast',
                    'description': 'User views 7-day weather forecast',
                    'steps': [
                        'User opens weather app',
                        'User searches for location',
                        'App displays current weather',
                        'User clicks on forecast tab',
                        'App displays 7-day forecast',
                        'User can click on individual days for details'
                    ]
                }
            ],
            'priority': 'high'
        }
        
        # Run the complete workflow
        repo_path = "data/inputs/sample_repositories/react_weather_app"
        
        return self.run_complete_workflow(repo_path, new_requirements)
