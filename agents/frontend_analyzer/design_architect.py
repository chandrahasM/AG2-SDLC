"""
Design Architect Agent
Updates design documents based on gap analysis and proposes architectural changes
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# AG2 Framework imports
from autogen import ConversableAgent, LLMConfig

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DesignArchitectAgent:
    """
    Design Architect Agent for React/TypeScript Applications
    
    Responsibilities:
    - Update design documents based on gap analysis
    - Propose architectural changes and improvements
    - Design new components and their interfaces
    - Plan implementation strategy
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
        
        # Create the design architect agent
        self.architect_agent = ConversableAgent(
            name="design_architect",
            system_message=self._get_architect_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.logger.info("Design Architect Agent initialized")
    
    def _get_architect_system_message(self) -> str:
        """System message for the design architect agent"""
        return """
You are a Design Architect Agent specialized in React/TypeScript applications.

Your responsibilities:
1. Update design documents based on gap analysis
2. Propose architectural changes and improvements
3. Design new components with detailed interfaces
4. Plan implementation strategy and phases
5. Ensure design consistency and scalability
6. Create detailed technical specifications

You work with gap analysis results to create comprehensive, implementable design updates that guide code generation.

Always provide detailed, structured design specifications that can be directly used for implementation.
"""
    
    def update_design_document(self, existing_design: Dict[str, Any],
                              gap_analysis: Dict[str, Any],
                              impact_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update design document based on gap analysis
        
        Args:
            existing_design: Current design document
            gap_analysis: Gap analysis results
            impact_analysis: Impact analysis results
        
        Returns:
            Updated design document with new specifications
        """
        self.logger.info("Updating design document based on gap analysis...")
        
        try:
            # Phase 1: Analyze existing design structure
            print("📋 Phase 1: Analyzing existing design structure...")
            design_structure = self._analyze_design_structure(existing_design)
            
            # Phase 2: Plan design updates
            print("📝 Phase 2: Planning design updates...")
            update_plan = self._plan_design_updates(gap_analysis, impact_analysis)
            
            # Phase 3: Design new components
            print("🏗️ Phase 3: Designing new components...")
            new_component_designs = self._design_new_components(gap_analysis)
            
            # Phase 4: Update existing components
            print("🔄 Phase 4: Updating existing components...")
            updated_component_designs = self._update_existing_components(gap_analysis)
            
            # Phase 5: Design API changes
            print("🌐 Phase 5: Designing API changes...")
            api_designs = self._design_api_changes(gap_analysis)
            
            # Phase 6: Create implementation plan
            print("📅 Phase 6: Creating implementation plan...")
            implementation_plan = self._create_implementation_plan(update_plan, impact_analysis)
            
            # Phase 7: Generate updated design document
            print("📄 Phase 7: Generating updated design document...")
            updated_design = self._generate_updated_design(
                existing_design, design_structure, update_plan,
                new_component_designs, updated_component_designs,
                api_designs, implementation_plan
            )
            
            # Phase 8: LLM review and validation
            print("🤖 Phase 8: LLM review and validation...")
            llm_validation = self._run_llm_validation(updated_design, gap_analysis)
            
            return {
                'updated_design': updated_design,
                'design_structure': design_structure,
                'update_plan': update_plan,
                'new_components': new_component_designs,
                'updated_components': updated_component_designs,
                'api_designs': api_designs,
                'implementation_plan': implementation_plan,
                'llm_validation': llm_validation,
                'update_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error updating design document: {e}")
            return {
                'error': str(e),
                'update_timestamp': datetime.now().isoformat()
            }
    
    def _analyze_design_structure(self, existing_design: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the structure of existing design document"""
        structure = {
            'has_components': bool(existing_design.get('components')),
            'has_features': bool(existing_design.get('features')),
            'has_user_stories': bool(existing_design.get('user_stories')),
            'has_api_endpoints': bool(existing_design.get('api_endpoints')),
            'has_data_models': bool(existing_design.get('data_models')),
            'has_user_flows': bool(existing_design.get('user_flows')),
            'has_architecture': bool(existing_design.get('architecture')),
            'component_count': len(existing_design.get('components', [])),
            'feature_count': len(existing_design.get('features', [])),
            'api_count': len(existing_design.get('api_endpoints', []))
        }
        
        return structure
    
    def _plan_design_updates(self, gap_analysis: Dict[str, Any], 
                            impact_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Plan the design updates based on gap analysis"""
        update_plan = {
            'new_features_to_add': [],
            'features_to_modify': [],
            'components_to_add': [],
            'components_to_modify': [],
            'apis_to_add': [],
            'apis_to_modify': [],
            'data_models_to_add': [],
            'data_models_to_modify': [],
            'user_flows_to_add': [],
            'user_flows_to_modify': [],
            'priority_order': [],
            'implementation_phases': []
        }
        
        # Plan new features
        for feature in gap_analysis.get('missing_features', []):
            update_plan['new_features_to_add'].append({
                'name': feature['name'],
                'description': feature['description'],
                'priority': feature.get('priority', 'medium'),
                'components_needed': self._identify_components_for_feature(feature),
                'apis_needed': self._identify_apis_for_feature(feature),
                'user_stories': self._generate_user_stories_for_feature(feature)
            })
        
        # Plan feature modifications
        for feature in gap_analysis.get('modified_features', []):
            update_plan['features_to_modify'].append({
                'name': feature['name'],
                'changes': feature['changes'],
                'impact': feature.get('impact', 'medium'),
                'components_affected': self._identify_affected_components(feature),
                'apis_affected': self._identify_affected_apis(feature)
            })
        
        # Plan new components
        for component in gap_analysis.get('new_components_needed', []):
            update_plan['components_to_add'].append({
                'name': component['name'],
                'type': component.get('type', 'component'),
                'description': component['description'],
                'dependencies': component.get('dependencies', []),
                'props_interface': self._design_props_interface(component),
                'state_interface': self._design_state_interface(component),
                'lifecycle_methods': self._design_lifecycle_methods(component),
                'event_handlers': self._design_event_handlers(component)
            })
        
        # Plan component modifications
        for component in gap_analysis.get('existing_components_to_modify', []):
            update_plan['components_to_modify'].append({
                'name': component['name'],
                'changes': component['changes'],
                'impact': component.get('impact', 'medium'),
                'new_props': self._extract_new_props(component['changes']),
                'modified_props': self._extract_modified_props(component['changes']),
                'new_state': self._extract_new_state(component['changes']),
                'modified_state': self._extract_modified_state(component['changes'])
            })
        
        # Plan API changes
        for api_change in gap_analysis.get('api_changes', []):
            if api_change['type'] == 'new':
                update_plan['apis_to_add'].append({
                    'endpoint': api_change['endpoint'],
                    'method': api_change['method'],
                    'description': api_change['description'],
                    'parameters': self._design_api_parameters(api_change),
                    'response_schema': self._design_api_response(api_change),
                    'error_handling': self._design_api_error_handling(api_change)
                })
            elif api_change['type'] == 'modified':
                update_plan['apis_to_modify'].append({
                    'endpoint': api_change['endpoint'],
                    'changes': api_change['changes'],
                    'impact': api_change.get('impact', 'medium'),
                    'backward_compatibility': self._assess_backward_compatibility(api_change)
                })
        
        # Create priority order
        update_plan['priority_order'] = self._create_priority_order(update_plan)
        
        # Create implementation phases
        update_plan['implementation_phases'] = self._create_implementation_phases(update_plan, impact_analysis)
        
        return update_plan
    
    def _identify_components_for_feature(self, feature: Dict[str, Any]) -> List[str]:
        """Identify components needed for a feature"""
        feature_name = feature['name'].lower()
        
        # Simple heuristic based on feature name
        components = []
        if 'forecast' in feature_name:
            components.extend(['ForecastCard', 'ForecastList', 'ForecastChart'])
        elif 'search' in feature_name:
            components.extend(['SearchBar', 'SearchResults', 'SearchFilter'])
        elif 'user' in feature_name:
            components.extend(['UserProfile', 'UserSettings', 'UserDashboard'])
        elif 'weather' in feature_name:
            components.extend(['WeatherCard', 'WeatherDetails', 'WeatherIcon'])
        
        return components
    
    def _identify_apis_for_feature(self, feature: Dict[str, Any]) -> List[str]:
        """Identify APIs needed for a feature"""
        feature_name = feature['name'].lower()
        
        apis = []
        if 'forecast' in feature_name:
            apis.extend(['/api/forecast', '/api/forecast/7day'])
        elif 'search' in feature_name:
            apis.extend(['/api/search', '/api/search/suggestions'])
        elif 'weather' in feature_name:
            apis.extend(['/api/weather', '/api/weather/current'])
        
        return apis
    
    def _generate_user_stories_for_feature(self, feature: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate user stories for a feature"""
        feature_name = feature['name']
        
        stories = [
            {
                'id': f"{feature_name.lower().replace(' ', '_')}_1",
                'title': f"As a user, I want to use {feature_name}",
                'description': f"I want to be able to access and use the {feature_name} functionality",
                'acceptance_criteria': [
                    f"User can access {feature_name}",
                    f"User can interact with {feature_name}",
                    f"User receives appropriate feedback from {feature_name}"
                ],
                'priority': 'high'
            }
        ]
        
        return stories
    
    def _identify_affected_components(self, feature: Dict[str, Any]) -> List[str]:
        """Identify components affected by feature modifications"""
        # This would typically analyze the feature changes to determine affected components
        return []
    
    def _identify_affected_apis(self, feature: Dict[str, Any]) -> List[str]:
        """Identify APIs affected by feature modifications"""
        # This would typically analyze the feature changes to determine affected APIs
        return []
    
    def _design_props_interface(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Design props interface for a new component"""
        component_name = component['name']
        
        # Generate props based on component type and description
        props = []
        
        if 'Card' in component_name:
            props.extend([
                {'name': 'title', 'type': 'string', 'required': True, 'description': 'Card title'},
                {'name': 'subtitle', 'type': 'string', 'required': False, 'description': 'Card subtitle'},
                {'name': 'onClick', 'type': '() => void', 'required': False, 'description': 'Click handler'}
            ])
        elif 'List' in component_name:
            props.extend([
                {'name': 'items', 'type': 'Array<any>', 'required': True, 'description': 'List items'},
                {'name': 'renderItem', 'type': '(item: any) => React.ReactNode', 'required': True, 'description': 'Item renderer'},
                {'name': 'onItemClick', 'type': '(item: any) => void', 'required': False, 'description': 'Item click handler'}
            ])
        elif 'Chart' in component_name:
            props.extend([
                {'name': 'data', 'type': 'Array<any>', 'required': True, 'description': 'Chart data'},
                {'name': 'width', 'type': 'number', 'required': False, 'description': 'Chart width'},
                {'name': 'height', 'type': 'number', 'required': False, 'description': 'Chart height'}
            ])
        
        return {
            'interface_name': f"{component_name}Props",
            'properties': props
        }
    
    def _design_state_interface(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Design state interface for a new component"""
        component_name = component['name']
        
        # Generate state based on component type
        state = []
        
        if 'Card' in component_name:
            state.extend([
                {'name': 'isExpanded', 'type': 'boolean', 'default': False, 'description': 'Card expansion state'},
                {'name': 'isLoading', 'type': 'boolean', 'default': False, 'description': 'Loading state'}
            ])
        elif 'List' in component_name:
            state.extend([
                {'name': 'selectedItems', 'type': 'Array<any>', 'default': '[]', 'description': 'Selected items'},
                {'name': 'filter', 'type': 'string', 'default': "''", 'description': 'Filter text'}
            ])
        elif 'Chart' in component_name:
            state.extend([
                {'name': 'hoveredData', 'type': 'any', 'default': 'null', 'description': 'Hovered data point'},
                {'name': 'selectedRange', 'type': 'Array<number>', 'default': '[]', 'description': 'Selected range'}
            ])
        
        return {
            'interface_name': f"{component_name}State",
            'properties': state
        }
    
    def _design_lifecycle_methods(self, component: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design lifecycle methods for a new component"""
        component_name = component['name']
        
        methods = []
        
        if 'Card' in component_name or 'List' in component_name or 'Chart' in component_name:
            methods.extend([
                {
                    'name': 'useEffect',
                    'description': 'Handle component mounting and data fetching',
                    'dependencies': ['props.data'],
                    'implementation': 'Fetch data when component mounts or props change'
                },
                {
                    'name': 'useCallback',
                    'description': 'Memoize event handlers',
                    'dependencies': ['props.onClick', 'props.onItemClick'],
                    'implementation': 'Prevent unnecessary re-renders of child components'
                }
            ])
        
        return methods
    
    def _design_event_handlers(self, component: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design event handlers for a new component"""
        component_name = component['name']
        
        handlers = []
        
        if 'Card' in component_name:
            handlers.extend([
                {
                    'name': 'handleClick',
                    'description': 'Handle card click events',
                    'parameters': ['event: React.MouseEvent'],
                    'implementation': 'Toggle expansion state or trigger onClick prop'
                }
            ])
        elif 'List' in component_name:
            handlers.extend([
                {
                    'name': 'handleItemClick',
                    'description': 'Handle item click events',
                    'parameters': ['item: any', 'index: number'],
                    'implementation': 'Update selection state and trigger onItemClick prop'
                },
                {
                    'name': 'handleFilterChange',
                    'description': 'Handle filter input changes',
                    'parameters': ['event: React.ChangeEvent<HTMLInputElement>'],
                    'implementation': 'Update filter state and filter items'
                }
            ])
        elif 'Chart' in component_name:
            handlers.extend([
                {
                    'name': 'handleDataHover',
                    'description': 'Handle data point hover events',
                    'parameters': ['data: any', 'event: React.MouseEvent'],
                    'implementation': 'Update hovered data state for tooltip display'
                },
                {
                    'name': 'handleRangeSelect',
                    'description': 'Handle range selection events',
                    'parameters': ['start: number', 'end: number'],
                    'implementation': 'Update selected range state'
                }
            ])
        
        return handlers
    
    def _extract_new_props(self, changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract new props from component changes"""
        new_props = []
        for change in changes:
            if change.get('field') == 'props' and change.get('type') == 'addition':
                new_props.append(change.get('data', {}))
        return new_props
    
    def _extract_modified_props(self, changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract modified props from component changes"""
        modified_props = []
        for change in changes:
            if change.get('field') == 'props' and change.get('type') == 'modification':
                modified_props.append({
                    'name': change.get('name', ''),
                    'old': change.get('old', {}),
                    'new': change.get('new', {})
                })
        return modified_props
    
    def _extract_new_state(self, changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract new state from component changes"""
        new_state = []
        for change in changes:
            if change.get('field') == 'state' and change.get('type') == 'addition':
                new_state.append(change.get('data', {}))
        return new_state
    
    def _extract_modified_state(self, changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract modified state from component changes"""
        modified_state = []
        for change in changes:
            if change.get('field') == 'state' and change.get('type') == 'modification':
                modified_state.append({
                    'name': change.get('name', ''),
                    'old': change.get('old', {}),
                    'new': change.get('new', {})
                })
        return modified_state
    
    def _design_api_parameters(self, api_change: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design API parameters for a new API"""
        endpoint = api_change['endpoint']
        
        parameters = []
        
        if '/forecast' in endpoint:
            parameters.extend([
                {'name': 'location', 'type': 'string', 'required': True, 'description': 'Location for forecast'},
                {'name': 'days', 'type': 'number', 'required': False, 'description': 'Number of forecast days', 'default': 7}
            ])
        elif '/search' in endpoint:
            parameters.extend([
                {'name': 'query', 'type': 'string', 'required': True, 'description': 'Search query'},
                {'name': 'limit', 'type': 'number', 'required': False, 'description': 'Maximum results', 'default': 10}
            ])
        elif '/weather' in endpoint:
            parameters.extend([
                {'name': 'location', 'type': 'string', 'required': True, 'description': 'Location for weather data'},
                {'name': 'units', 'type': 'string', 'required': False, 'description': 'Temperature units', 'default': 'metric'}
            ])
        
        return parameters
    
    def _design_api_response(self, api_change: Dict[str, Any]) -> Dict[str, Any]:
        """Design API response schema for a new API"""
        endpoint = api_change['endpoint']
        
        if '/forecast' in endpoint:
            return {
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
        elif '/search' in endpoint:
            return {
                'type': 'object',
                'properties': {
                    'results': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'name': {'type': 'string'},
                                'description': {'type': 'string'}
                            }
                        }
                    },
                    'total': {'type': 'number'}
                }
            }
        else:
            return {'type': 'object', 'properties': {}}
    
    def _design_api_error_handling(self, api_change: Dict[str, Any]) -> Dict[str, Any]:
        """Design API error handling for a new API"""
        return {
            'error_codes': {
                '400': 'Bad Request - Invalid parameters',
                '404': 'Not Found - Resource not found',
                '500': 'Internal Server Error - Server error'
            },
            'error_response_format': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'message': {'type': 'string'},
                    'code': {'type': 'number'}
                }
            }
        }
    
    def _assess_backward_compatibility(self, api_change: Dict[str, Any]) -> Dict[str, Any]:
        """Assess backward compatibility for API changes"""
        changes = api_change.get('changes', [])
        
        breaking_changes = []
        non_breaking_changes = []
        
        for change in changes:
            if change.get('field') == 'method':
                breaking_changes.append('HTTP method change')
            elif change.get('field') == 'parameters' and change.get('type') == 'addition':
                if change.get('data', {}).get('required', False):
                    breaking_changes.append('New required parameter')
                else:
                    non_breaking_changes.append('New optional parameter')
            elif change.get('field') == 'parameters' and change.get('type') == 'modification':
                breaking_changes.append('Parameter modification')
        
        return {
            'is_backward_compatible': len(breaking_changes) == 0,
            'breaking_changes': breaking_changes,
            'non_breaking_changes': non_breaking_changes,
            'migration_required': len(breaking_changes) > 0
        }
    
    def _create_priority_order(self, update_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create priority order for implementation"""
        priority_order = []
        
        # High priority items first
        for feature in update_plan.get('new_features_to_add', []):
            if feature.get('priority') == 'high':
                priority_order.append({
                    'type': 'feature',
                    'name': feature['name'],
                    'priority': 'high',
                    'dependencies': []
                })
        
        # Medium priority items
        for feature in update_plan.get('new_features_to_add', []):
            if feature.get('priority') == 'medium':
                priority_order.append({
                    'type': 'feature',
                    'name': feature['name'],
                    'priority': 'medium',
                    'dependencies': []
                })
        
        # Low priority items
        for feature in update_plan.get('new_features_to_add', []):
            if feature.get('priority') == 'low':
                priority_order.append({
                    'type': 'feature',
                    'name': feature['name'],
                    'priority': 'low',
                    'dependencies': []
                })
        
        return priority_order
    
    def _create_implementation_phases(self, update_plan: Dict[str, Any], 
                                    impact_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create implementation phases"""
        phases = []
        
        # Phase 1: Foundation
        phases.append({
            'phase': 1,
            'name': 'Foundation',
            'description': 'Set up new components and basic structure',
            'items': [
                'Create new component interfaces',
                'Set up basic component structure',
                'Implement core data models'
            ],
            'duration': '1-2 weeks',
            'dependencies': []
        })
        
        # Phase 2: Core Features
        phases.append({
            'phase': 2,
            'name': 'Core Features',
            'description': 'Implement core new features',
            'items': [
                'Implement new features',
                'Add new API endpoints',
                'Create user workflows'
            ],
            'duration': '2-3 weeks',
            'dependencies': ['Phase 1']
        })
        
        # Phase 3: Integration
        phases.append({
            'phase': 3,
            'name': 'Integration',
            'description': 'Integrate new features with existing system',
            'items': [
                'Update existing components',
                'Integrate with existing APIs',
                'Update user flows'
            ],
            'duration': '1-2 weeks',
            'dependencies': ['Phase 2']
        })
        
        # Phase 4: Testing and Refinement
        phases.append({
            'phase': 4,
            'name': 'Testing and Refinement',
            'description': 'Test and refine the implementation',
            'items': [
                'Unit testing',
                'Integration testing',
                'User acceptance testing',
                'Performance optimization'
            ],
            'duration': '1 week',
            'dependencies': ['Phase 3']
        })
        
        return phases
    
    def _design_new_components(self, gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design new components based on gap analysis"""
        new_components = []
        
        for component in gap_analysis.get('new_components_needed', []):
            component_design = {
                'name': component['name'],
                'type': component.get('type', 'component'),
                'description': component['description'],
                'props_interface': self._design_props_interface(component),
                'state_interface': self._design_state_interface(component),
                'lifecycle_methods': self._design_lifecycle_methods(component),
                'event_handlers': self._design_event_handlers(component),
                'dependencies': component.get('dependencies', []),
                'business_logic': self._design_business_logic(component),
                'styling_requirements': self._design_styling_requirements(component),
                'accessibility_requirements': self._design_accessibility_requirements(component)
            }
            new_components.append(component_design)
        
        return new_components
    
    def _update_existing_components(self, gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Update existing components based on gap analysis"""
        updated_components = []
        
        for component in gap_analysis.get('existing_components_to_modify', []):
            component_design = {
                'name': component['name'],
                'changes': component['changes'],
                'impact': component.get('impact', 'medium'),
                'new_props': self._extract_new_props(component['changes']),
                'modified_props': self._extract_modified_props(component['changes']),
                'new_state': self._extract_new_state(component['changes']),
                'modified_state': self._extract_modified_state(component['changes']),
                'migration_guide': self._create_migration_guide(component),
                'backward_compatibility': self._assess_component_backward_compatibility(component)
            }
            updated_components.append(component_design)
        
        return updated_components
    
    def _design_api_changes(self, gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design API changes based on gap analysis"""
        api_designs = []
        
        for api_change in gap_analysis.get('api_changes', []):
            api_design = {
                'endpoint': api_change['endpoint'],
                'method': api_change.get('method', 'GET'),
                'description': api_change.get('description', ''),
                'parameters': self._design_api_parameters(api_change),
                'response_schema': self._design_api_response(api_change),
                'error_handling': self._design_api_error_handling(api_change),
                'backward_compatibility': self._assess_backward_compatibility(api_change),
                'versioning_strategy': self._design_versioning_strategy(api_change)
            }
            api_designs.append(api_design)
        
        return api_designs
    
    def _design_business_logic(self, component: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design business logic for a component"""
        component_name = component['name']
        
        business_logic = []
        
        if 'Forecast' in component_name:
            business_logic.extend([
                {
                    'name': 'fetchForecastData',
                    'description': 'Fetch forecast data from API',
                    'parameters': ['location: string', 'days: number'],
                    'return_type': 'Promise<ForecastData>',
                    'error_handling': 'Handle API errors and show user feedback'
                },
                {
                    'name': 'formatForecastData',
                    'description': 'Format forecast data for display',
                    'parameters': ['rawData: any'],
                    'return_type': 'FormattedForecastData',
                    'error_handling': 'Handle data formatting errors'
                }
            ])
        elif 'Search' in component_name:
            business_logic.extend([
                {
                    'name': 'performSearch',
                    'description': 'Perform search operation',
                    'parameters': ['query: string', 'filters: SearchFilters'],
                    'return_type': 'Promise<SearchResults>',
                    'error_handling': 'Handle search errors and empty results'
                },
                {
                    'name': 'debounceSearch',
                    'description': 'Debounce search input',
                    'parameters': ['callback: Function', 'delay: number'],
                    'return_type': 'Function',
                    'error_handling': 'Handle debounce errors'
                }
            ])
        
        return business_logic
    
    def _design_styling_requirements(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Design styling requirements for a component"""
        component_name = component['name']
        
        styling = {
            'responsive_design': True,
            'theme_support': True,
            'custom_styles': [],
            'css_variables': [],
            'media_queries': []
        }
        
        if 'Card' in component_name:
            styling['custom_styles'].extend([
                'card-container',
                'card-header',
                'card-content',
                'card-footer'
            ])
            styling['css_variables'].extend([
                '--card-padding',
                '--card-border-radius',
                '--card-shadow'
            ])
        elif 'List' in component_name:
            styling['custom_styles'].extend([
                'list-container',
                'list-item',
                'list-item-selected',
                'list-item-hover'
            ])
            styling['css_variables'].extend([
                '--list-item-padding',
                '--list-item-gap',
                '--list-item-border'
            ])
        
        return styling
    
    def _design_accessibility_requirements(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Design accessibility requirements for a component"""
        return {
            'aria_labels': True,
            'keyboard_navigation': True,
            'screen_reader_support': True,
            'focus_management': True,
            'color_contrast': True,
            'aria_attributes': [
                'aria-label',
                'aria-describedby',
                'aria-expanded',
                'aria-selected'
            ]
        }
    
    def _create_migration_guide(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Create migration guide for component changes"""
        return {
            'breaking_changes': [],
            'deprecated_props': [],
            'new_props': [],
            'migration_steps': [
                'Update component imports',
                'Update prop usage',
                'Update state management',
                'Test component functionality'
            ],
            'backward_compatibility_period': '2 versions'
        }
    
    def _assess_component_backward_compatibility(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Assess backward compatibility for component changes"""
        changes = component.get('changes', [])
        
        breaking_changes = []
        non_breaking_changes = []
        
        for change in changes:
            if change.get('field') == 'props' and change.get('type') == 'modification':
                old_prop = change.get('old', {})
                new_prop = change.get('new', {})
                
                if old_prop.get('required', False) and not new_prop.get('required', False):
                    non_breaking_changes.append('Prop made optional')
                elif not old_prop.get('required', False) and new_prop.get('required', False):
                    breaking_changes.append('Prop made required')
                elif old_prop.get('type') != new_prop.get('type'):
                    breaking_changes.append('Prop type changed')
            elif change.get('field') == 'props' and change.get('type') == 'addition':
                if change.get('data', {}).get('required', False):
                    breaking_changes.append('New required prop added')
                else:
                    non_breaking_changes.append('New optional prop added')
        
        return {
            'is_backward_compatible': len(breaking_changes) == 0,
            'breaking_changes': breaking_changes,
            'non_breaking_changes': non_breaking_changes,
            'migration_required': len(breaking_changes) > 0
        }
    
    def _design_versioning_strategy(self, api_change: Dict[str, Any]) -> Dict[str, Any]:
        """Design versioning strategy for API changes"""
        return {
            'versioning_approach': 'URL versioning',
            'current_version': 'v1',
            'new_version': 'v2',
            'deprecation_timeline': '6 months',
            'migration_support': True,
            'backward_compatibility': 'v1 endpoints maintained for 6 months'
        }
    
    def _create_implementation_plan(self, update_plan: Dict[str, Any], 
                                  impact_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed implementation plan"""
        return {
            'phases': self._create_implementation_phases(update_plan, impact_analysis),
            'priority_order': update_plan.get('priority_order', []),
            'resource_requirements': self._estimate_resource_requirements(update_plan),
            'timeline': self._estimate_timeline(update_plan),
            'risk_assessment': self._assess_implementation_risks(update_plan, impact_analysis),
            'success_metrics': self._define_success_metrics(update_plan)
        }
    
    def _estimate_resource_requirements(self, update_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate resource requirements for implementation"""
        return {
            'developers': 2,
            'designers': 1,
            'testers': 1,
            'estimated_hours': 160,
            'tools_required': ['React', 'TypeScript', 'Testing Library', 'Storybook']
        }
    
    def _estimate_timeline(self, update_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate timeline for implementation"""
        return {
            'total_duration': '6-8 weeks',
            'phase_1': '1-2 weeks',
            'phase_2': '2-3 weeks',
            'phase_3': '1-2 weeks',
            'phase_4': '1 week',
            'buffer_time': '1 week'
        }
    
    def _assess_implementation_risks(self, update_plan: Dict[str, Any], 
                                   impact_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess implementation risks"""
        risks = []
        
        if impact_analysis.get('breaking_changes'):
            risks.append({
                'risk': 'Breaking Changes',
                'impact': 'High',
                'probability': 'Medium',
                'mitigation': 'Implement backward compatibility and gradual migration'
            })
        
        if len(update_plan.get('new_components_needed', [])) > 5:
            risks.append({
                'risk': 'Scope Creep',
                'impact': 'Medium',
                'probability': 'High',
                'mitigation': 'Prioritize features and implement in phases'
            })
        
        return risks
    
    def _define_success_metrics(self, update_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define success metrics for implementation"""
        return [
            {
                'metric': 'Feature Completion',
                'target': '100% of planned features implemented',
                'measurement': 'Feature checklist completion'
            },
            {
                'metric': 'Code Quality',
                'target': '90%+ test coverage',
                'measurement': 'Automated test coverage reports'
            },
            {
                'metric': 'Performance',
                'target': 'Page load time < 2 seconds',
                'measurement': 'Performance monitoring tools'
            },
            {
                'metric': 'User Satisfaction',
                'target': '4.5+ user rating',
                'measurement': 'User feedback and surveys'
            }
        ]
    
    def _generate_updated_design(self, existing_design: Dict[str, Any],
                                design_structure: Dict[str, Any],
                                update_plan: Dict[str, Any],
                                new_component_designs: List[Dict[str, Any]],
                                updated_component_designs: List[Dict[str, Any]],
                                api_designs: List[Dict[str, Any]],
                                implementation_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the updated design document"""
        
        # Start with existing design
        updated_design = existing_design.copy()
        
        # Add new features
        new_features = []
        for feature in update_plan.get('new_features_to_add', []):
            new_features.append({
                'name': feature['name'],
                'description': feature['description'],
                'priority': feature.get('priority', 'medium'),
                'user_stories': feature.get('user_stories', []),
                'components': feature.get('components_needed', []),
                'apis': feature.get('apis_needed', []),
                'status': 'planned'
            })
        
        updated_design['features'].extend(new_features)
        
        # Add new components
        updated_design['components'].extend(new_component_designs)
        
        # Update existing components
        for updated_component in updated_component_designs:
            # Find existing component and update it
            for i, component in enumerate(updated_design.get('components', [])):
                if component['name'] == updated_component['name']:
                    updated_design['components'][i].update(updated_component)
                    break
        
        # Add new API endpoints
        updated_design['api_endpoints'].extend(api_designs)
        
        # Add implementation plan
        updated_design['implementation_plan'] = implementation_plan
        
        # Add version information
        updated_design['version'] = '2.0'
        updated_design['last_updated'] = datetime.now().isoformat()
        updated_design['changes_summary'] = {
            'new_features': len(new_features),
            'new_components': len(new_component_designs),
            'updated_components': len(updated_component_designs),
            'new_apis': len(api_designs)
        }
        
        return updated_design
    
    def _run_llm_validation(self, updated_design: Dict[str, Any], 
                           gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run LLM validation of the updated design"""
        
        design_summary = {
            'version': updated_design.get('version', '1.0'),
            'new_features': len(updated_design.get('features', [])),
            'total_components': len(updated_design.get('components', [])),
            'total_apis': len(updated_design.get('api_endpoints', [])),
            'implementation_phases': len(updated_design.get('implementation_plan', {}).get('phases', []))
        }
        
        prompt = f"""
Review this updated design document and provide validation:

{json.dumps(design_summary, indent=2)}

Please validate:
1. Design completeness and consistency
2. Technical feasibility of the proposed changes
3. Potential issues or conflicts
4. Recommendations for improvement
5. Overall quality assessment
"""
        
        try:
            response = self.architect_agent.run(
                message=prompt,
                max_turns=1
            )
            
            messages = response.messages
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                else:
                    content = str(last_message)
                
                return {
                    'validation_result': content,
                    'validation_timestamp': datetime.now().isoformat()
                }
            
            return {'validation_result': 'No validation generated', 'validation_timestamp': datetime.now().isoformat()}
            
        except Exception as e:
            self.logger.error(f"Error in LLM validation: {e}")
            return {'validation_result': f'Error: {str(e)}', 'validation_timestamp': datetime.now().isoformat()}
