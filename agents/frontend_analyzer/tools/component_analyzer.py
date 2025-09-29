"""
Component Analyzer for React/TypeScript
Analyzes component relationships, dependencies, and business logic
"""

import os
import re
import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ComponentDependency:
    component_name: str
    file_path: str
    dependencies: List[str]
    dependents: List[str]
    props_interface: Optional[str]
    state_interface: Optional[str]

@dataclass
class BusinessCapability:
    name: str
    description: str
    components: List[str]
    data_flow: List[str]
    user_interactions: List[str]
    api_calls: List[str]

class ComponentAnalyzer:
    """Analyzes React components and their relationships"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.components = {}
        self.dependencies = {}
        self.business_capabilities = []
    
    def analyze_components(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze all components and their relationships"""
        self.logger.info("Analyzing component relationships and dependencies...")
        
        # Build component registry
        self._build_component_registry(file_analyses)
        
        # Analyze dependencies
        self._analyze_dependencies()
        
        # Extract business capabilities
        self._extract_business_capabilities()
        
        # Analyze data flow
        data_flow = self._analyze_data_flow()
        
        # Analyze user interactions
        user_interactions = self._analyze_user_interactions()
        
        return {
            'components': self.components,
            'dependencies': self.dependencies,
            'business_capabilities': self.business_capabilities,
            'data_flow': data_flow,
            'user_interactions': user_interactions,
            'architecture_patterns': self._detect_architecture_patterns()
        }
    
    def _build_component_registry(self, file_analyses: List[Dict[str, Any]]):
        """Build a registry of all components"""
        for file_analysis in file_analyses:
            if file_analysis.get('file_type') == 'component':
                for component in file_analysis.get('components', []):
                    component_name = component['name']
                    self.components[component_name] = {
                        'name': component_name,
                        'file_path': file_analysis['file_path'],
                        'type': component['type'],
                        'props': component.get('props', []),
                        'state': component.get('state', []),
                        'hooks': component.get('hooks', []),
                        'event_handlers': component.get('event_handlers', []),
                        'jsx_elements': component.get('jsx_elements', []),
                        'complexity': component.get('complexity', 0),
                        'imports': file_analysis.get('imports', []),
                        'exports': file_analysis.get('exports', []),
                        'business_logic': file_analysis.get('business_logic', [])
                    }
    
    def _analyze_dependencies(self):
        """Analyze component dependencies"""
        for component_name, component_data in self.components.items():
            dependencies = []
            dependents = []
            
            # Find components this component depends on
            for import_data in component_data['imports']:
                if import_data['source'].startswith('.'):  # Local import
                    # Check if it's a component import
                    if any(comp_name.lower() in import_data['name'].lower() 
                          for comp_name in self.components.keys()):
                        dependencies.append(import_data['name'])
            
            # Find components that depend on this component
            for other_comp_name, other_comp_data in self.components.items():
                if other_comp_name != component_name:
                    for import_data in other_comp_data['imports']:
                        if (import_data['source'].startswith('.') and 
                            component_name.lower() in import_data['name'].lower()):
                            dependents.append(other_comp_name)
            
            self.dependencies[component_name] = {
                'dependencies': dependencies,
                'dependents': dependents,
                'props_interface': self._extract_props_interface(component_data),
                'state_interface': self._extract_state_interface(component_data)
            }
    
    def _extract_props_interface(self, component_data: Dict[str, Any]) -> Optional[str]:
        """Extract props interface name for a component"""
        props = component_data.get('props', [])
        if props:
            # Look for interface that matches component props
            for prop in props:
                if 'interface' in prop.get('type', '').lower():
                    return prop['type']
        return None
    
    def _extract_state_interface(self, component_data: Dict[str, Any]) -> Optional[str]:
        """Extract state interface name for a component"""
        state = component_data.get('state', [])
        if state:
            # Look for state interface patterns
            for state_var in state:
                if 'interface' in state_var.get('type', '').lower():
                    return state_var['type']
        return None
    
    def _extract_business_capabilities(self):
        """Extract business capabilities from components"""
        capabilities = {}
        
        for component_name, component_data in self.components.items():
            business_logic = component_data.get('business_logic', [])
            
            for logic in business_logic:
                if logic['type'] == 'api_call':
                    capability_name = self._infer_capability_from_api(logic)
                    if capability_name not in capabilities:
                        capabilities[capability_name] = {
                            'name': capability_name,
                            'description': f"Handles {capability_name} operations",
                            'components': [],
                            'data_flow': [],
                            'user_interactions': [],
                            'api_calls': []
                        }
                    
                    capabilities[capability_name]['components'].append(component_name)
                    capabilities[capability_name]['api_calls'].append({
                        'method': logic['method'],
                        'component': component_name,
                        'line': logic['line']
                    })
                
                elif logic['type'] == 'event_handling':
                    capability_name = self._infer_capability_from_event(logic)
                    if capability_name not in capabilities:
                        capabilities[capability_name] = {
                            'name': capability_name,
                            'description': f"Handles {capability_name} user interactions",
                            'components': [],
                            'data_flow': [],
                            'user_interactions': [],
                            'api_calls': []
                        }
                    
                    capabilities[capability_name]['components'].append(component_name)
                    capabilities[capability_name]['user_interactions'].append({
                        'pattern': logic['pattern'],
                        'component': component_name,
                        'line': logic['line']
                    })
        
        self.business_capabilities = list(capabilities.values())
    
    def _infer_capability_from_api(self, api_logic: Dict[str, Any]) -> str:
        """Infer business capability from API call"""
        method = api_logic.get('method', '').lower()
        
        if method in ['get', 'fetch']:
            return 'Data Retrieval'
        elif method in ['post', 'create']:
            return 'Data Creation'
        elif method in ['put', 'update']:
            return 'Data Update'
        elif method in ['delete', 'remove']:
            return 'Data Deletion'
        else:
            return 'API Operations'
    
    def _infer_capability_from_event(self, event_logic: Dict[str, Any]) -> str:
        """Infer business capability from event handling"""
        pattern = event_logic.get('pattern', '').lower()
        
        if 'click' in pattern:
            return 'User Interaction'
        elif 'change' in pattern:
            return 'Form Handling'
        elif 'submit' in pattern:
            return 'Form Submission'
        else:
            return 'Event Handling'
    
    def _analyze_data_flow(self) -> List[Dict[str, Any]]:
        """Analyze data flow between components"""
        data_flows = []
        
        for component_name, component_data in self.components.items():
            # Analyze props flow
            props = component_data.get('props', [])
            for prop in props:
                data_flows.append({
                    'type': 'props',
                    'from': 'parent_component',
                    'to': component_name,
                    'data': prop['name'],
                    'data_type': prop.get('type', 'any')
                })
            
            # Analyze state flow
            state = component_data.get('state', [])
            for state_var in state:
                data_flows.append({
                    'type': 'state',
                    'from': component_name,
                    'to': 'child_components',
                    'data': 'state_variable',
                    'data_type': state_var.get('type', 'any')
                })
            
            # Analyze API data flow
            business_logic = component_data.get('business_logic', [])
            for logic in business_logic:
                if logic['type'] == 'api_call':
                    data_flows.append({
                        'type': 'api_data',
                        'from': 'external_api',
                        'to': component_name,
                        'data': f"{logic['method']}_response",
                        'data_type': 'api_response'
                    })
        
        return data_flows
    
    def _analyze_user_interactions(self) -> List[Dict[str, Any]]:
        """Analyze user interactions and workflows"""
        interactions = []
        
        for component_name, component_data in self.components.items():
            event_handlers = component_data.get('event_handlers', [])
            
            for handler in event_handlers:
                interactions.append({
                    'component': component_name,
                    'handler': handler['name'],
                    'type': 'event_handler',
                    'line': handler['line_number'],
                    'workflow': self._infer_workflow_from_handler(handler)
                })
            
            # Analyze JSX elements for user interactions
            jsx_elements = component_data.get('jsx_elements', [])
            for element in jsx_elements:
                if element['name'].lower() in ['button', 'input', 'form', 'select']:
                    interactions.append({
                        'component': component_name,
                        'element': element['name'],
                        'type': 'interactive_element',
                        'props': element.get('props', [])
                    })
        
        return interactions
    
    def _infer_workflow_from_handler(self, handler: Dict[str, Any]) -> str:
        """Infer user workflow from event handler"""
        handler_name = handler['name'].lower()
        
        if 'submit' in handler_name:
            return 'Form Submission Workflow'
        elif 'click' in handler_name:
            return 'Button Click Workflow'
        elif 'change' in handler_name:
            return 'Input Change Workflow'
        elif 'search' in handler_name:
            return 'Search Workflow'
        else:
            return 'User Interaction Workflow'
    
    def _detect_architecture_patterns(self) -> List[Dict[str, Any]]:
        """Detect architectural patterns in the codebase"""
        patterns = []
        
        # Check for component composition pattern
        if self._has_composition_pattern():
            patterns.append({
                'name': 'Component Composition',
                'description': 'Components are composed of smaller, reusable components',
                'confidence': 0.8,
                'evidence': 'Multiple components with JSX element dependencies'
            })
        
        # Check for container/presentational pattern
        if self._has_container_presentational_pattern():
            patterns.append({
                'name': 'Container/Presentational Pattern',
                'description': 'Separation of data logic (containers) and presentation (components)',
                'confidence': 0.7,
                'evidence': 'Components with different levels of business logic complexity'
            })
        
        # Check for custom hooks pattern
        if self._has_custom_hooks_pattern():
            patterns.append({
                'name': 'Custom Hooks Pattern',
                'description': 'Business logic extracted into custom hooks',
                'confidence': 0.9,
                'evidence': 'Custom hook files and hook usage in components'
            })
        
        return patterns
    
    def _has_composition_pattern(self) -> bool:
        """Check if components use composition pattern"""
        for component_data in self.components.values():
            jsx_elements = component_data.get('jsx_elements', [])
            if len(jsx_elements) > 3:  # Multiple child components
                return True
        return False
    
    def _has_container_presentational_pattern(self) -> bool:
        """Check if there's a container/presentational pattern"""
        has_containers = False
        has_presentational = False
        
        for component_data in self.components.values():
            business_logic = component_data.get('business_logic', [])
            api_calls = [logic for logic in business_logic if logic['type'] == 'api_call']
            
            if len(api_calls) > 0:
                has_containers = True
            elif len(business_logic) == 0:
                has_presentational = True
        
        return has_containers and has_presentational
    
    def _has_custom_hooks_pattern(self) -> bool:
        """Check if custom hooks are used"""
        for component_data in self.components.values():
            hooks = component_data.get('hooks', [])
            custom_hooks = [hook for hook in hooks if hook.get('is_custom', False)]
            if custom_hooks:
                return True
        return False
    
    def analyze_relationships(self, structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze component relationships from structural analysis"""
        try:
            # Extract file analyses from structural analysis
            file_analyses = list(structural_analysis.get("file_analysis", {}).values())
            
            # Run the main analysis
            return self.analyze_components(file_analyses)
            
        except Exception as e:
            self.logger.error(f"Error in component relationship analysis: {e}")
            return {
                "relationships": {},
                "dependencies": {},
                "business_capabilities": [],
                "data_flow": [],
                "user_interactions": [],
                "architecture_patterns": []
            }
