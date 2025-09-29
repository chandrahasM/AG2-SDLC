"""
Design Analyzer Agent
Compares existing design with new requirements and identifies gaps
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

class DesignAnalyzerAgent:
    """
    Design Analyzer Agent for React/TypeScript Applications
    
    Responsibilities:
    - Parse existing design documents
    - Compare with new requirements
    - Identify gaps and conflicts
    - Analyze impact of changes
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
        
        # Create the design analyzer agent
        self.analyzer_agent = ConversableAgent(
            name="design_analyzer",
            system_message=self._get_analyzer_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.logger.info("Design Analyzer Agent initialized")
    
    def _get_analyzer_system_message(self) -> str:
        """System message for the design analyzer agent"""
        return """
You are a Design Analyzer Agent specialized in React/TypeScript applications.

Your responsibilities:
1. Parse and understand existing design documents
2. Compare existing design with new requirements
3. Identify gaps, conflicts, and missing features
4. Analyze the impact of proposed changes
5. Provide detailed gap analysis and recommendations

You work with design documents, requirements, and code analysis to ensure design consistency and completeness.

Always provide structured, actionable insights that can guide design updates and code generation.
"""
    
    def analyze_design_gaps(self, existing_design: Dict[str, Any], 
                           new_requirements: Dict[str, Any],
                           code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze gaps between existing design and new requirements
        
        Args:
            existing_design: Current design document structure
            new_requirements: New requirements to implement
            code_analysis: Current code analysis from repository analyzer
        
        Returns:
            Gap analysis and recommendations
        """
        self.logger.info("Analyzing design gaps and requirements...")
        
        try:
            # Phase 1: Parse existing design
            print("📋 Phase 1: Parsing existing design...")
            design_components = self._parse_existing_design(existing_design)
            
            # Phase 2: Parse new requirements
            print("📝 Phase 2: Parsing new requirements...")
            requirement_components = self._parse_new_requirements(new_requirements)
            
            # Phase 3: Compare and identify gaps
            print("🔍 Phase 3: Comparing and identifying gaps...")
            gap_analysis = self._compare_designs(design_components, requirement_components)
            
            # Phase 4: Analyze impact
            print("⚡ Phase 4: Analyzing impact of changes...")
            impact_analysis = self._analyze_impact(gap_analysis, code_analysis)
            
            # Phase 5: Generate recommendations
            print("💡 Phase 5: Generating recommendations...")
            recommendations = self._generate_recommendations(gap_analysis, impact_analysis)
            
            # Phase 6: LLM synthesis
            print("🤖 Phase 6: LLM synthesis and insights...")
            llm_insights = self._run_llm_analysis(
                design_components, requirement_components, gap_analysis, impact_analysis
            )
            
            return {
                'existing_design': design_components,
                'new_requirements': requirement_components,
                'gap_analysis': gap_analysis,
                'impact_analysis': impact_analysis,
                'recommendations': recommendations,
                'llm_insights': llm_insights,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing design gaps: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _parse_existing_design(self, existing_design: Dict[str, Any]) -> Dict[str, Any]:
        """Parse existing design document"""
        design_components = {
            'features': existing_design.get('features', []),
            'components': existing_design.get('components', []),
            'user_stories': existing_design.get('user_stories', []),
            'api_endpoints': existing_design.get('api_endpoints', []),
            'data_models': existing_design.get('data_models', []),
            'user_flows': existing_design.get('user_flows', []),
            'technical_specs': existing_design.get('technical_specs', {}),
            'architecture': existing_design.get('architecture', {})
        }
        
        return design_components
    
    def _parse_new_requirements(self, new_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Parse new requirements"""
        requirement_components = {
            'new_features': new_requirements.get('features', []),
            'modified_features': new_requirements.get('modified_features', []),
            'removed_features': new_requirements.get('removed_features', []),
            'new_components': new_requirements.get('components', []),
            'new_user_stories': new_requirements.get('user_stories', []),
            'new_api_endpoints': new_requirements.get('api_endpoints', []),
            'new_data_models': new_requirements.get('data_models', []),
            'new_user_flows': new_requirements.get('user_flows', []),
            'technical_changes': new_requirements.get('technical_changes', {}),
            'priority': new_requirements.get('priority', 'medium')
        }
        
        return requirement_components
    
    def _compare_designs(self, existing_design: Dict[str, Any], 
                        new_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Compare existing design with new requirements"""
        gap_analysis = {
            'missing_features': [],
            'modified_features': [],
            'removed_features': [],
            'new_components_needed': [],
            'existing_components_to_modify': [],
            'api_changes': [],
            'data_model_changes': [],
            'user_flow_changes': [],
            'technical_gaps': [],
            'conflicts': []
        }
        
        # Compare features
        existing_features = {f['name']: f for f in existing_design.get('features', [])}
        new_features = {f['name']: f for f in new_requirements.get('new_features', [])}
        modified_features = {f['name']: f for f in new_requirements.get('modified_features', [])}
        
        # Find missing features
        for feature_name, feature_data in new_features.items():
            if feature_name not in existing_features:
                gap_analysis['missing_features'].append({
                    'name': feature_name,
                    'description': feature_data.get('description', ''),
                    'priority': feature_data.get('priority', 'medium'),
                    'impact': 'high'
                })
        
        # Find modified features
        for feature_name, feature_data in modified_features.items():
            if feature_name in existing_features:
                existing_feature = existing_features[feature_name]
                changes = self._compare_feature_changes(existing_feature, feature_data)
                if changes:
                    gap_analysis['modified_features'].append({
                        'name': feature_name,
                        'changes': changes,
                        'impact': self._assess_change_impact(changes)
                    })
        
        # Compare components
        existing_components = {c['name']: c for c in existing_design.get('components', [])}
        new_components = {c['name']: c for c in new_requirements.get('new_components', [])}
        
        for component_name, component_data in new_components.items():
            if component_name not in existing_components:
                gap_analysis['new_components_needed'].append({
                    'name': component_name,
                    'type': component_data.get('type', 'component'),
                    'description': component_data.get('description', ''),
                    'dependencies': component_data.get('dependencies', []),
                    'props': component_data.get('props', []),
                    'state': component_data.get('state', [])
                })
            else:
                # Component exists, check if modifications needed
                existing_component = existing_components[component_name]
                component_changes = self._compare_component_changes(existing_component, component_data)
                if component_changes:
                    gap_analysis['existing_components_to_modify'].append({
                        'name': component_name,
                        'changes': component_changes,
                        'impact': self._assess_component_change_impact(component_changes)
                    })
        
        # Compare API endpoints
        existing_apis = {api['endpoint']: api for api in existing_design.get('api_endpoints', [])}
        new_apis = {api['endpoint']: api for api in new_requirements.get('new_api_endpoints', [])}
        
        for endpoint, api_data in new_apis.items():
            if endpoint not in existing_apis:
                gap_analysis['api_changes'].append({
                    'type': 'new',
                    'endpoint': endpoint,
                    'method': api_data.get('method', 'GET'),
                    'description': api_data.get('description', ''),
                    'impact': 'high'
                })
            else:
                existing_api = existing_apis[endpoint]
                api_changes = self._compare_api_changes(existing_api, api_data)
                if api_changes:
                    gap_analysis['api_changes'].append({
                        'type': 'modified',
                        'endpoint': endpoint,
                        'changes': api_changes,
                        'impact': self._assess_api_change_impact(api_changes)
                    })
        
        return gap_analysis
    
    def _compare_feature_changes(self, existing: Dict[str, Any], new: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compare changes between existing and new feature"""
        changes = []
        
        # Compare description
        if existing.get('description') != new.get('description'):
            changes.append({
                'field': 'description',
                'old': existing.get('description', ''),
                'new': new.get('description', ''),
                'type': 'content_change'
            })
        
        # Compare user stories
        existing_stories = {s['id']: s for s in existing.get('user_stories', [])}
        new_stories = {s['id']: s for s in new.get('user_stories', [])}
        
        for story_id, story_data in new_stories.items():
            if story_id not in existing_stories:
                changes.append({
                    'field': 'user_stories',
                    'type': 'addition',
                    'content': story_data
                })
            elif existing_stories[story_id] != story_data:
                changes.append({
                    'field': 'user_stories',
                    'type': 'modification',
                    'old': existing_stories[story_id],
                    'new': story_data
                })
        
        return changes
    
    def _compare_component_changes(self, existing: Dict[str, Any], new: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compare changes between existing and new component"""
        changes = []
        
        # Compare props
        existing_props = {p['name']: p for p in existing.get('props', [])}
        new_props = {p['name']: p for p in new.get('props', [])}
        
        for prop_name, prop_data in new_props.items():
            if prop_name not in existing_props:
                changes.append({
                    'field': 'props',
                    'type': 'addition',
                    'name': prop_name,
                    'data': prop_data
                })
            elif existing_props[prop_name] != prop_data:
                changes.append({
                    'field': 'props',
                    'type': 'modification',
                    'name': prop_name,
                    'old': existing_props[prop_name],
                    'new': prop_data
                })
        
        # Compare state
        existing_state = {s['name']: s for s in existing.get('state', [])}
        new_state = {s['name']: s for s in new.get('state', [])}
        
        for state_name, state_data in new_state.items():
            if state_name not in existing_state:
                changes.append({
                    'field': 'state',
                    'type': 'addition',
                    'name': state_name,
                    'data': state_data
                })
            elif existing_state[state_name] != state_data:
                changes.append({
                    'field': 'state',
                    'type': 'modification',
                    'name': state_name,
                    'old': existing_state[state_name],
                    'new': state_data
                })
        
        return changes
    
    def _compare_api_changes(self, existing: Dict[str, Any], new: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compare changes between existing and new API"""
        changes = []
        
        # Compare method
        if existing.get('method') != new.get('method'):
            changes.append({
                'field': 'method',
                'old': existing.get('method', ''),
                'new': new.get('method', ''),
                'type': 'method_change'
            })
        
        # Compare parameters
        existing_params = {p['name']: p for p in existing.get('parameters', [])}
        new_params = {p['name']: p for p in new.get('parameters', [])}
        
        for param_name, param_data in new_params.items():
            if param_name not in existing_params:
                changes.append({
                    'field': 'parameters',
                    'type': 'addition',
                    'name': param_name,
                    'data': param_data
                })
            elif existing_params[param_name] != param_data:
                changes.append({
                    'field': 'parameters',
                    'type': 'modification',
                    'name': param_name,
                    'old': existing_params[param_name],
                    'new': param_data
                })
        
        return changes
    
    def _assess_change_impact(self, changes: List[Dict[str, Any]]) -> str:
        """Assess the impact of changes"""
        if not changes:
            return 'none'
        
        high_impact_fields = ['user_stories', 'api_endpoints', 'data_models']
        medium_impact_fields = ['props', 'state', 'parameters']
        
        for change in changes:
            if change.get('field') in high_impact_fields:
                return 'high'
            elif change.get('field') in medium_impact_fields:
                return 'medium'
        
        return 'low'
    
    def _assess_component_change_impact(self, changes: List[Dict[str, Any]]) -> str:
        """Assess the impact of component changes"""
        if not changes:
            return 'none'
        
        # Component changes are generally medium to high impact
        return 'medium' if len(changes) < 3 else 'high'
    
    def _assess_api_change_impact(self, changes: List[Dict[str, Any]]) -> str:
        """Assess the impact of API changes"""
        if not changes:
            return 'none'
        
        # API changes are generally high impact
        return 'high'
    
    def _analyze_impact(self, gap_analysis: Dict[str, Any], 
                       code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the impact of changes on existing code"""
        impact_analysis = {
            'affected_components': [],
            'affected_files': [],
            'breaking_changes': [],
            'migration_effort': 'low',
            'testing_requirements': [],
            'deployment_considerations': []
        }
        
        # Analyze component impact
        for component_change in gap_analysis.get('existing_components_to_modify', []):
            component_name = component_change['name']
            changes = component_change['changes']
            
            # Find affected files
            affected_files = self._find_affected_files(component_name, code_analysis)
            impact_analysis['affected_files'].extend(affected_files)
            
            # Check for breaking changes
            breaking_changes = self._identify_breaking_changes(changes)
            if breaking_changes:
                impact_analysis['breaking_changes'].extend(breaking_changes)
            
            impact_analysis['affected_components'].append({
                'name': component_name,
                'changes': changes,
                'affected_files': affected_files,
                'breaking_changes': breaking_changes
            })
        
        # Analyze API impact
        for api_change in gap_analysis.get('api_changes', []):
            if api_change['type'] == 'modified':
                impact_analysis['breaking_changes'].append({
                    'type': 'api_change',
                    'endpoint': api_change['endpoint'],
                    'description': 'API modification may break existing clients'
                })
        
        # Assess migration effort
        impact_analysis['migration_effort'] = self._assess_migration_effort(impact_analysis)
        
        # Generate testing requirements
        impact_analysis['testing_requirements'] = self._generate_testing_requirements(gap_analysis)
        
        return impact_analysis
    
    def _find_affected_files(self, component_name: str, code_analysis: Dict[str, Any]) -> List[str]:
        """Find files affected by component changes"""
        affected_files = []
        
        components = code_analysis.get('component_analysis', {}).get('components', {})
        if component_name in components:
            component_data = components[component_name]
            affected_files.append(component_data.get('file_path', ''))
            
            # Find files that import this component
            dependencies = code_analysis.get('component_analysis', {}).get('dependencies', {})
            for comp_name, dep_data in dependencies.items():
                if component_name in dep_data.get('dependencies', []):
                    if comp_name in components:
                        affected_files.append(components[comp_name].get('file_path', ''))
        
        return list(set(affected_files))
    
    def _identify_breaking_changes(self, changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify breaking changes in component modifications"""
        breaking_changes = []
        
        for change in changes:
            if change.get('field') == 'props' and change.get('type') == 'modification':
                # Prop modification might be breaking
                old_prop = change.get('old', {})
                new_prop = change.get('new', {})
                
                if old_prop.get('required', False) and not new_prop.get('required', False):
                    breaking_changes.append({
                        'type': 'prop_removal',
                        'component': change.get('name', ''),
                        'prop': old_prop.get('name', ''),
                        'description': 'Required prop removed'
                    })
                elif old_prop.get('type') != new_prop.get('type'):
                    breaking_changes.append({
                        'type': 'prop_type_change',
                        'component': change.get('name', ''),
                        'prop': old_prop.get('name', ''),
                        'old_type': old_prop.get('type', ''),
                        'new_type': new_prop.get('type', ''),
                        'description': 'Prop type changed'
                    })
        
        return breaking_changes
    
    def _assess_migration_effort(self, impact_analysis: Dict[str, Any]) -> str:
        """Assess the migration effort required"""
        breaking_changes = impact_analysis.get('breaking_changes', [])
        affected_components = impact_analysis.get('affected_components', [])
        
        if breaking_changes:
            return 'high'
        elif len(affected_components) > 5:
            return 'medium'
        else:
            return 'low'
    
    def _generate_testing_requirements(self, gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate testing requirements based on changes"""
        testing_requirements = []
        
        # Test new components
        for component in gap_analysis.get('new_components_needed', []):
            testing_requirements.append({
                'type': 'component_test',
                'component': component['name'],
                'description': f"Test new component: {component['name']}",
                'priority': 'high'
            })
        
        # Test modified components
        for component in gap_analysis.get('existing_components_to_modify', []):
            testing_requirements.append({
                'type': 'regression_test',
                'component': component['name'],
                'description': f"Regression test for modified component: {component['name']}",
                'priority': 'high'
            })
        
        # Test API changes
        for api_change in gap_analysis.get('api_changes', []):
            testing_requirements.append({
                'type': 'api_test',
                'endpoint': api_change['endpoint'],
                'description': f"Test API changes for: {api_change['endpoint']}",
                'priority': 'high'
            })
        
        return testing_requirements
    
    def _generate_recommendations(self, gap_analysis: Dict[str, Any], 
                                 impact_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on gap and impact analysis"""
        recommendations = []
        
        # Recommendations for missing features
        for feature in gap_analysis.get('missing_features', []):
            recommendations.append({
                'type': 'feature_implementation',
                'priority': feature.get('priority', 'medium'),
                'description': f"Implement missing feature: {feature['name']}",
                'impact': feature.get('impact', 'medium'),
                'effort': 'medium'
            })
        
        # Recommendations for component changes
        for component in gap_analysis.get('existing_components_to_modify', []):
            recommendations.append({
                'type': 'component_refactor',
                'priority': 'high',
                'description': f"Refactor component: {component['name']}",
                'impact': component.get('impact', 'medium'),
                'effort': 'medium'
            })
        
        # Recommendations for breaking changes
        for breaking_change in impact_analysis.get('breaking_changes', []):
            recommendations.append({
                'type': 'breaking_change_mitigation',
                'priority': 'high',
                'description': f"Mitigate breaking change: {breaking_change.get('description', '')}",
                'impact': 'high',
                'effort': 'high'
            })
        
        return recommendations
    
    def _run_llm_analysis(self, existing_design: Dict[str, Any],
                         new_requirements: Dict[str, Any],
                         gap_analysis: Dict[str, Any],
                         impact_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run LLM analysis for high-level insights"""
        
        analysis_summary = {
            'gap_summary': {
                'missing_features': len(gap_analysis.get('missing_features', [])),
                'modified_features': len(gap_analysis.get('modified_features', [])),
                'new_components': len(gap_analysis.get('new_components_needed', [])),
                'modified_components': len(gap_analysis.get('existing_components_to_modify', [])),
                'api_changes': len(gap_analysis.get('api_changes', []))
            },
            'impact_summary': {
                'affected_components': len(impact_analysis.get('affected_components', [])),
                'breaking_changes': len(impact_analysis.get('breaking_changes', [])),
                'migration_effort': impact_analysis.get('migration_effort', 'low')
            }
        }
        
        prompt = f"""
Analyze this design gap analysis and provide strategic insights:

{json.dumps(analysis_summary, indent=2)}

Please provide:
1. Overall assessment of the gap analysis
2. Key risks and challenges identified
3. Strategic recommendations for implementation
4. Priority recommendations for addressing gaps
5. Suggestions for minimizing impact and breaking changes
"""
        
        try:
            response = self.analyzer_agent.run(
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
                    'llm_insights': content,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            
            return {'llm_insights': 'No insights generated', 'analysis_timestamp': datetime.now().isoformat()}
            
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {e}")
            return {'llm_insights': f'Error: {str(e)}', 'analysis_timestamp': datetime.now().isoformat()}
