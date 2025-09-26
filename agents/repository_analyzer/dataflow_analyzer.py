"""
Data Flow & Dependency Mapper
Maps how data flows through business processes and identifies workflows
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class DataFlowNode:
    name: str
    type: str  # 'function', 'class', 'data'
    inputs: List[str]
    outputs: List[str]
    transformations: List[str]
    side_effects: List[str]

@dataclass
class BusinessWorkflow:
    name: str
    trigger: str
    steps: List[Dict[str, Any]]
    data_flow: List[str]
    decision_points: List[Dict[str, Any]]
    error_paths: List[str]
    performance_impact: Dict[str, Any]

@dataclass
class StateTransition:
    from_state: str
    to_state: str
    trigger: str
    conditions: List[str]
    actions: List[str]

class DataFlowAnalyzer:
    """Maps data flows and business workflows"""
    
    def __init__(self):
        # Data transformation patterns
        self.transformation_patterns = {
            'serialization': [r'serialize', r'to_json', r'to_dict', r'model_dump'],
            'deserialization': [r'deserialize', r'from_json', r'parse', r'load'],
            'validation': [r'validate', r'verify', r'check', r'sanitize'],
            'formatting': [r'format', r'render', r'display', r'pretty'],
            'conversion': [r'convert', r'transform', r'map', r'cast'],
            'aggregation': [r'sum', r'count', r'group', r'aggregate', r'collect'],
            'filtering': [r'filter', r'where', r'select', r'find'],
            'sorting': [r'sort', r'order', r'rank', r'arrange']
        }
        
        # State management patterns
        self.state_patterns = {
            'creation': [r'create', r'new', r'initialize', r'setup'],
            'modification': [r'update', r'modify', r'change', r'edit', r'set'],
            'deletion': [r'delete', r'remove', r'destroy', r'cleanup'],
            'retrieval': [r'get', r'fetch', r'load', r'read', r'find'],
            'persistence': [r'save', r'store', r'persist', r'commit'],
            'transition': [r'transition', r'move', r'change_state', r'switch']
        }
        
        # Business process patterns
        self.process_patterns = {
            'workflow': [r'workflow', r'process', r'pipeline', r'chain'],
            'orchestration': [r'orchestrate', r'coordinate', r'manage', r'control'],
            'aggregation': [r'aggregate', r'combine', r'merge', r'consolidate'],
            'distribution': [r'distribute', r'dispatch', r'route', r'forward'],
            'notification': [r'notify', r'alert', r'inform', r'broadcast'],
            'monitoring': [r'monitor', r'track', r'observe', r'watch'],
            'scheduling': [r'schedule', r'queue', r'defer', r'batch']
        }
        
        # Data source patterns
        self.data_source_patterns = {
            'database': [r'db', r'database', r'sql', r'query', r'session'],
            'api': [r'api', r'http', r'request', r'client', r'service'],
            'file': [r'file', r'csv', r'json', r'xml', r'read', r'write'],
            'cache': [r'cache', r'redis', r'memcached', r'store'],
            'queue': [r'queue', r'message', r'publish', r'subscribe'],
            'stream': [r'stream', r'kafka', r'event', r'real_time']
        }

    def trace_business_workflows(self, analysis_data: Dict) -> Dict:
        """Maps data flows through business processes"""
        logger.info("Tracing business workflows and data flows...")
        
        try:
            functions = analysis_data.get('functions', [])
            classes = analysis_data.get('classes', [])
            
            # Build data flow graph
            data_flow_graph = self._build_data_flow_graph(functions, classes)
            
            # Identify business workflows
            business_workflows = self._identify_business_workflows(functions, data_flow_graph)
            
            # Trace data transformations
            data_transformations = self._trace_data_transformations(functions, classes)
            
            # Identify state management patterns
            state_management = self._analyze_state_management(functions, classes)
            
            # Map external integrations
            external_integrations = self._map_external_integrations(functions, classes)
            
            # Analyze performance implications
            performance_analysis = self._analyze_performance_implications(functions, data_flow_graph)
            
            return {
                "data_flow_graph": data_flow_graph,
                "business_workflows": business_workflows,
                "data_transformations": data_transformations,
                "state_management": state_management,
                "external_integrations": external_integrations,
                "performance_analysis": performance_analysis,
                "data_lineage": self._trace_data_lineage(functions, classes),
                "workflow_patterns": self._identify_workflow_patterns(business_workflows)
            }
            
        except Exception as e:
            logger.error(f"Error tracing business workflows: {e}")
            return {
                "data_flow_graph": {"nodes": [], "edges": []},
                "business_workflows": [],
                "data_transformations": [],
                "state_management": {},
                "external_integrations": [],
                "performance_analysis": {},
                "data_lineage": [],
                "workflow_patterns": []
            }

    def _build_data_flow_graph(self, functions: List[Dict], classes: List[Dict]) -> Dict:
        """Build comprehensive data flow graph"""
        nodes = []
        edges = []
        
        # Create nodes for functions
        for func in functions:
            node = self._create_function_node(func)
            nodes.append(node)
        
        # Create nodes for classes (data containers)
        for cls in classes:
            if self._is_data_container(cls):
                node = self._create_class_node(cls)
                nodes.append(node)
        
        # Create edges based on function calls and data flow
        edges = self._create_data_flow_edges(functions, classes)
        
        # Identify critical paths
        critical_paths = self._identify_critical_paths(nodes, edges)
        
        return {
            "nodes": nodes,
            "edges": edges,
            "critical_paths": critical_paths,
            "complexity_metrics": self._calculate_graph_complexity(nodes, edges)
        }

    def _create_function_node(self, func: Dict) -> Dict:
        """Create data flow node for function"""
        func_name = func.get('name', 'unknown')
        parameters = func.get('parameters', [])
        calls = func.get('calls', [])
        
        # Determine inputs (parameters + external data sources)
        inputs = [param.get('name', '') for param in parameters if param.get('name') not in ['self', 'cls']]
        
        # Add external data sources
        for call in calls:
            data_source = self._identify_data_source(call)
            if data_source and data_source not in inputs:
                inputs.append(f"external:{data_source}")
        
        # Determine outputs (return type + side effects)
        outputs = []
        return_type = func.get('return_type')
        if return_type:
            outputs.append(return_type)
        
        # Add side effect outputs
        side_effects = func.get('side_effects', [])
        for effect in side_effects:
            outputs.append(f"side_effect:{effect}")
        
        # Identify transformations
        transformations = self._identify_function_transformations(func)
        
        return {
            "id": func_name,
            "name": func_name,
            "type": "function",
            "inputs": inputs,
            "outputs": outputs,
            "transformations": transformations,
            "side_effects": side_effects,
            "complexity": func.get('semantic_complexity', {}),
            "business_intent": func.get('business_intent', 'unknown'),
            "file_path": func.get('file_path', 'unknown')
        }

    def _create_class_node(self, cls: Dict) -> Dict:
        """Create data flow node for class (data container)"""
        class_name = cls.get('name', 'unknown')
        methods = cls.get('methods', [])
        attributes = cls.get('attributes', [])
        
        # Determine data operations
        operations = []
        for method in methods:
            method_name = method.get('name', '')
            if not method_name.startswith('_'):
                operations.append(method_name)
        
        # Identify state transitions
        state_transitions = self._identify_class_state_transitions(methods)
        
        return {
            "id": class_name,
            "name": class_name,
            "type": "data_container",
            "attributes": [attr.get('name', '') for attr in attributes],
            "operations": operations,
            "state_transitions": state_transitions,
            "relationships": cls.get('relationships', {}),
            "file_path": cls.get('file_path', 'unknown')
        }

    def _create_data_flow_edges(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Create edges representing data flow between nodes"""
        edges = []
        
        # Create function-to-function edges
        for func in functions:
            func_name = func.get('name', '')
            calls = func.get('calls', [])
            
            for call in calls:
                # Find target function
                target_func = self._find_function_by_call(call, functions)
                if target_func:
                    edge = {
                        "source": func_name,
                        "target": target_func.get('name', ''),
                        "type": "function_call",
                        "data_passed": self._infer_data_passed(func, target_func),
                        "transformation": self._infer_call_transformation(call)
                    }
                    edges.append(edge)
        
        # Create function-to-class edges (data operations)
        for func in functions:
            func_name = func.get('name', '')
            calls = func.get('calls', [])
            
            for call in calls:
                target_class = self._find_class_by_call(call, classes)
                if target_class:
                    edge = {
                        "source": func_name,
                        "target": target_class.get('name', ''),
                        "type": "data_operation",
                        "operation": self._infer_data_operation(call),
                        "data_affected": self._infer_affected_data(call)
                    }
                    edges.append(edge)
        
        return edges

    def _identify_business_workflows(self, functions: List[Dict], data_flow_graph: Dict) -> List[Dict]:
        """Identify business workflows from function analysis"""
        workflows = []
        
        # Group functions by business capability
        capability_groups = defaultdict(list)
        for func in functions:
            capability = func.get('business_intent', 'general')
            capability_groups[capability].append(func)
        
        # Create workflows for each capability
        for capability, funcs in capability_groups.items():
            if len(funcs) > 1:  # Only create workflows with multiple steps
                workflow = self._create_business_workflow(capability, funcs, data_flow_graph)
                workflows.append(workflow)
        
        # Identify cross-capability workflows
        cross_workflows = self._identify_cross_capability_workflows(functions, data_flow_graph)
        workflows.extend(cross_workflows)
        
        return workflows

    def _create_business_workflow(self, capability: str, functions: List[Dict], data_flow_graph: Dict) -> Dict:
        """Create a business workflow from related functions"""
        # Sort functions by likely execution order
        ordered_functions = self._order_functions_by_execution(functions, data_flow_graph)
        
        # Create workflow steps
        steps = []
        for i, func in enumerate(ordered_functions):
            step = {
                "step_number": i + 1,
                "step_name": func.get('semantic_purpose', func.get('name', 'unknown')),
                "function": func.get('name', ''),
                "inputs": self._extract_step_inputs(func),
                "outputs": self._extract_step_outputs(func),
                "business_rules": func.get('business_logic', []),
                "error_handling": func.get('error_handling', {}),
                "performance_impact": self._assess_step_performance(func)
            }
            steps.append(step)
        
        # Identify decision points
        decision_points = self._identify_decision_points(ordered_functions)
        
        # Trace data flow through workflow
        workflow_data_flow = self._trace_workflow_data_flow(ordered_functions)
        
        # Identify error paths
        error_paths = self._identify_workflow_error_paths(ordered_functions)
        
        return {
            "name": f"{capability.title()} Workflow",
            "capability": capability,
            "trigger": self._identify_workflow_trigger(ordered_functions),
            "steps": steps,
            "data_flow": workflow_data_flow,
            "decision_points": decision_points,
            "error_paths": error_paths,
            "performance_characteristics": self._analyze_workflow_performance(ordered_functions),
            "state_changes": self._identify_workflow_state_changes(ordered_functions)
        }

    def _trace_data_transformations(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Trace data transformations throughout the system"""
        transformations = []
        
        # Analyze function-level transformations
        for func in functions:
            func_transformations = self._extract_function_transformations(func)
            transformations.extend(func_transformations)
        
        # Analyze class-level transformations (serialization, etc.)
        for cls in classes:
            class_transformations = self._extract_class_transformations(cls)
            transformations.extend(class_transformations)
        
        # Group and categorize transformations
        categorized_transformations = self._categorize_transformations(transformations)
        
        return categorized_transformations

    def _analyze_state_management(self, functions: List[Dict], classes: List[Dict]) -> Dict:
        """Analyze state management patterns"""
        state_management = {
            "state_containers": [],
            "state_transitions": [],
            "state_persistence": [],
            "state_validation": []
        }
        
        # Identify state containers (classes that manage state)
        for cls in classes:
            if self._is_state_container(cls):
                container_info = {
                    "name": cls.get('name', ''),
                    "state_attributes": self._extract_state_attributes(cls),
                    "state_operations": self._extract_state_operations(cls),
                    "lifecycle_methods": self._extract_lifecycle_methods(cls)
                }
                state_management["state_containers"].append(container_info)
        
        # Identify state transitions
        for func in functions:
            transitions = self._identify_function_state_transitions(func)
            state_management["state_transitions"].extend(transitions)
        
        # Identify state persistence patterns
        persistence_patterns = self._identify_persistence_patterns(functions, classes)
        state_management["state_persistence"] = persistence_patterns
        
        # Identify state validation patterns
        validation_patterns = self._identify_state_validation_patterns(functions, classes)
        state_management["state_validation"] = validation_patterns
        
        return state_management

    def _map_external_integrations(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Map external system integrations"""
        integrations = []
        
        # Analyze function calls for external integrations
        for func in functions:
            calls = func.get('calls', [])
            for call in calls:
                integration = self._identify_external_integration(call, func)
                if integration:
                    integrations.append(integration)
        
        # Group integrations by type
        grouped_integrations = defaultdict(list)
        for integration in integrations:
            grouped_integrations[integration['type']].append(integration)
        
        # Create integration summaries
        integration_summaries = []
        for integration_type, integration_list in grouped_integrations.items():
            summary = {
                "type": integration_type,
                "count": len(integration_list),
                "endpoints": list(set([i.get('endpoint', 'unknown') for i in integration_list])),
                "functions": list(set([i.get('function', 'unknown') for i in integration_list])),
                "data_formats": list(set([i.get('data_format', 'unknown') for i in integration_list])),
                "error_handling": self._analyze_integration_error_handling(integration_list)
            }
            integration_summaries.append(summary)
        
        return integration_summaries

    def _analyze_performance_implications(self, functions: List[Dict], data_flow_graph: Dict) -> Dict:
        """Analyze performance implications of data flows"""
        performance = {
            "bottlenecks": [],
            "async_operations": [],
            "database_operations": [],
            "external_calls": [],
            "complexity_hotspots": []
        }
        
        # Identify potential bottlenecks
        nodes = data_flow_graph.get('nodes', [])
        edges = data_flow_graph.get('edges', [])
        
        # Find nodes with high fan-in (potential bottlenecks)
        node_fan_in = defaultdict(int)
        for edge in edges:
            node_fan_in[edge.get('target', '')] += 1
        
        for node_id, fan_in_count in node_fan_in.items():
            if fan_in_count > 3:  # Threshold for bottleneck
                node = next((n for n in nodes if n.get('id') == node_id), None)
                if node:
                    performance['bottlenecks'].append({
                        "node": node_id,
                        "fan_in": fan_in_count,
                        "type": node.get('type', 'unknown'),
                        "complexity": node.get('complexity', {})
                    })
        
        # Identify async operations
        for func in functions:
            if func.get('is_async'):
                performance['async_operations'].append({
                    "function": func.get('name', ''),
                    "purpose": func.get('semantic_purpose', 'unknown'),
                    "complexity": func.get('semantic_complexity', {})
                })
        
        # Identify database operations
        for func in functions:
            calls = func.get('calls', [])
            db_calls = [call for call in calls if self._is_database_call(call)]
            if db_calls:
                performance['database_operations'].append({
                    "function": func.get('name', ''),
                    "database_calls": db_calls,
                    "call_count": len(db_calls)
                })
        
        # Identify external calls
        for func in functions:
            calls = func.get('calls', [])
            external_calls = [call for call in calls if self._is_external_call(call)]
            if external_calls:
                performance['external_calls'].append({
                    "function": func.get('name', ''),
                    "external_calls": external_calls,
                    "call_count": len(external_calls)
                })
        
        return performance

    def _trace_data_lineage(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Trace data lineage through the system"""
        lineage = []
        
        # Identify data entities
        data_entities = [cls for cls in classes if self._is_data_entity(cls)]
        
        for entity in data_entities:
            entity_lineage = {
                "entity": entity.get('name', ''),
                "sources": self._find_data_sources(entity, functions),
                "transformations": self._find_data_transformations(entity, functions),
                "destinations": self._find_data_destinations(entity, functions),
                "lifecycle": self._trace_entity_lifecycle(entity, functions)
            }
            lineage.append(entity_lineage)
        
        return lineage

    def _identify_workflow_patterns(self, workflows: List[Dict]) -> List[Dict]:
        """Identify common workflow patterns"""
        patterns = []
        
        # Analyze workflow structures for common patterns
        for workflow in workflows:
            steps = workflow.get('steps', [])
            
            # Check for pipeline pattern
            if self._is_pipeline_pattern(steps):
                patterns.append({
                    "pattern": "Pipeline",
                    "workflow": workflow.get('name', ''),
                    "description": "Sequential data processing pipeline"
                })
            
            # Check for scatter-gather pattern
            if self._is_scatter_gather_pattern(steps):
                patterns.append({
                    "pattern": "Scatter-Gather",
                    "workflow": workflow.get('name', ''),
                    "description": "Parallel processing with result aggregation"
                })
            
            # Check for saga pattern
            if self._is_saga_pattern(steps):
                patterns.append({
                    "pattern": "Saga",
                    "workflow": workflow.get('name', ''),
                    "description": "Distributed transaction with compensation"
                })
            
            # Check for event-driven pattern
            if self._is_event_driven_pattern(steps):
                patterns.append({
                    "pattern": "Event-Driven",
                    "workflow": workflow.get('name', ''),
                    "description": "Event-based workflow orchestration"
                })
        
        return patterns

    # Helper methods
    def _is_data_container(self, cls: Dict) -> bool:
        """Check if class is a data container"""
        class_name = cls.get('name', '').lower()
        base_classes = cls.get('base_classes', [])
        
        # Check for data model indicators
        data_indicators = [
            'model' in class_name,
            'entity' in class_name,
            'schema' in class_name,
            'dto' in class_name,
            any('basemodel' in base.lower() for base in base_classes),
            any('dataclass' in str(cls.get('decorators', [])))
        ]
        
        return any(data_indicators)

    def _identify_data_source(self, call: str) -> Optional[str]:
        """Identify data source from function call"""
        call_lower = call.lower()
        
        for source_type, patterns in self.data_source_patterns.items():
            if any(pattern in call_lower for pattern in patterns):
                return source_type
        
        return None

    def _identify_function_transformations(self, func: Dict) -> List[str]:
        """Identify transformations performed by function"""
        transformations = []
        func_name = func.get('name', '').lower()
        calls = func.get('calls', [])
        
        # Check function name for transformation patterns
        for transform_type, patterns in self.transformation_patterns.items():
            if any(re.search(pattern, func_name) for pattern in patterns):
                transformations.append(transform_type)
        
        # Check function calls for transformations
        for call in calls:
            call_lower = call.lower()
            for transform_type, patterns in self.transformation_patterns.items():
                if any(re.search(pattern, call_lower) for pattern in patterns):
                    transformations.append(f"calls_{transform_type}")
        
        return list(set(transformations))

    def _identify_class_state_transitions(self, methods: List[Dict]) -> List[Dict]:
        """Identify state transitions in class methods"""
        transitions = []
        
        for method in methods:
            method_name = method.get('name', '').lower()
            
            # Check for state transition patterns
            for state_type, patterns in self.state_patterns.items():
                if any(re.search(pattern, method_name) for pattern in patterns):
                    transitions.append({
                        "method": method.get('name', ''),
                        "state_operation": state_type,
                        "complexity": method.get('complexity', 0)
                    })
        
        return transitions

    def _find_function_by_call(self, call: str, functions: List[Dict]) -> Optional[Dict]:
        """Find function that matches the call"""
        # Simple matching - extract function name from call
        call_name = call.split('(')[0].split('.')[-1]
        
        for func in functions:
            if func.get('name') == call_name:
                return func
        
        return None

    def _find_class_by_call(self, call: str, classes: List[Dict]) -> Optional[Dict]:
        """Find class that matches the call"""
        # Look for class instantiation or method calls
        for cls in classes:
            class_name = cls.get('name', '')
            if class_name in call:
                return cls
        
        return None

    def _infer_data_passed(self, source_func: Dict, target_func: Dict) -> List[str]:
        """Infer what data is passed between functions"""
        # Simple inference based on parameter types
        source_return = source_func.get('return_type', '')
        target_params = target_func.get('parameters', [])
        
        data_passed = []
        if source_return:
            data_passed.append(source_return)
        
        # Check if return type matches any target parameter
        for param in target_params:
            param_type = param.get('type', '')
            if param_type and param_type == source_return:
                data_passed.append(f"matches_param:{param.get('name', '')}")
        
        return data_passed

    def _infer_call_transformation(self, call: str) -> Optional[str]:
        """Infer transformation from function call"""
        call_lower = call.lower()
        
        for transform_type, patterns in self.transformation_patterns.items():
            if any(re.search(pattern, call_lower) for pattern in patterns):
                return transform_type
        
        return None

    def _infer_data_operation(self, call: str) -> str:
        """Infer data operation from call"""
        call_lower = call.lower()
        
        if any(pattern in call_lower for pattern in ['create', 'new', 'add']):
            return 'create'
        elif any(pattern in call_lower for pattern in ['update', 'modify', 'set']):
            return 'update'
        elif any(pattern in call_lower for pattern in ['delete', 'remove']):
            return 'delete'
        elif any(pattern in call_lower for pattern in ['get', 'find', 'fetch']):
            return 'read'
        else:
            return 'unknown'

    def _infer_affected_data(self, call: str) -> str:
        """Infer what data is affected by the call"""
        # Extract potential data type from call
        parts = call.split('.')
        if len(parts) > 1:
            return parts[0]  # Assume first part is the data type
        else:
            return 'unknown'

    def _identify_critical_paths(self, nodes: List[Dict], edges: List[Dict]) -> List[List[str]]:
        """Identify critical paths in the data flow graph"""
        # Simple critical path identification
        paths = []
        
        # Find entry points (nodes with no incoming edges)
        incoming_counts = defaultdict(int)
        for edge in edges:
            incoming_counts[edge.get('target', '')] += 1
        
        entry_points = [node.get('id', '') for node in nodes if incoming_counts[node.get('id', '')] == 0]
        
        # Find exit points (nodes with no outgoing edges)
        outgoing_counts = defaultdict(int)
        for edge in edges:
            outgoing_counts[edge.get('source', '')] += 1
        
        exit_points = [node.get('id', '') for node in nodes if outgoing_counts[node.get('id', '')] == 0]
        
        # Simple path construction (would need more sophisticated algorithm for real critical path)
        for entry in entry_points:
            for exit in exit_points:
                if entry != exit:
                    paths.append([entry, exit])
        
        return paths

    def _calculate_graph_complexity(self, nodes: List[Dict], edges: List[Dict]) -> Dict:
        """Calculate complexity metrics for the data flow graph"""
        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "average_fan_out": len(edges) / len(nodes) if nodes else 0,
            "cyclomatic_complexity": len(edges) - len(nodes) + 1 if nodes else 0
        }

    def _order_functions_by_execution(self, functions: List[Dict], data_flow_graph: Dict) -> List[Dict]:
        """Order functions by likely execution order"""
        # Simple topological sort based on function calls
        ordered = []
        remaining = functions.copy()
        
        while remaining:
            # Find functions with no dependencies in remaining set
            no_deps = []
            for func in remaining:
                func_calls = func.get('calls', [])
                has_deps = any(self._find_function_by_call(call, remaining) for call in func_calls)
                if not has_deps:
                    no_deps.append(func)
            
            if not no_deps:
                # If no functions without dependencies, take the first one
                no_deps = [remaining[0]]
            
            # Add to ordered list and remove from remaining
            ordered.extend(no_deps)
            for func in no_deps:
                remaining.remove(func)
        
        return ordered

    def _extract_step_inputs(self, func: Dict) -> List[str]:
        """Extract inputs for workflow step"""
        inputs = []
        parameters = func.get('parameters', [])
        
        for param in parameters:
            if param.get('name') not in ['self', 'cls']:
                inputs.append(param.get('name', ''))
        
        return inputs

    def _extract_step_outputs(self, func: Dict) -> List[str]:
        """Extract outputs for workflow step"""
        outputs = []
        return_type = func.get('return_type')
        
        if return_type:
            outputs.append(return_type)
        
        # Add side effects as outputs
        side_effects = func.get('side_effects', [])
        outputs.extend(side_effects)
        
        return outputs

    def _assess_step_performance(self, func: Dict) -> Dict:
        """Assess performance impact of workflow step"""
        complexity = func.get('semantic_complexity', {})
        
        return {
            "complexity_score": complexity.get('business_rules', 0) + complexity.get('external_dependencies', 0),
            "async_operation": func.get('is_async', False),
            "external_calls": complexity.get('external_dependencies', 0),
            "database_operations": complexity.get('data_transformations', 0)
        }

    def _identify_decision_points(self, functions: List[Dict]) -> List[Dict]:
        """Identify decision points in workflow"""
        decision_points = []
        
        for func in functions:
            complexity = func.get('semantic_complexity', {})
            business_rules = complexity.get('business_rules', 0)
            
            if business_rules > 2:  # Functions with multiple business rules likely have decisions
                decision_points.append({
                    "function": func.get('name', ''),
                    "decision_complexity": business_rules,
                    "business_logic": func.get('business_logic', [])
                })
        
        return decision_points

    def _trace_workflow_data_flow(self, functions: List[Dict]) -> List[str]:
        """Trace data flow through workflow"""
        data_flow = []
        
        for i, func in enumerate(functions):
            if i == 0:
                # First function - input from external source
                params = func.get('parameters', [])
                if params:
                    data_flow.append(f"Input: {', '.join([p.get('name', '') for p in params if p.get('name') not in ['self', 'cls']])}")
            
            # Function processing
            return_type = func.get('return_type')
            if return_type:
                data_flow.append(f"{func.get('name', '')} → {return_type}")
        
        return data_flow

    def _identify_workflow_error_paths(self, functions: List[Dict]) -> List[str]:
        """Identify error paths in workflow"""
        error_paths = []
        
        for func in functions:
            error_handling = func.get('error_handling', {})
            exception_types = error_handling.get('exception_types', [])
            
            for exc_type in exception_types:
                error_paths.append(f"{func.get('name', '')} → {exc_type}")
        
        return error_paths

    def _analyze_workflow_performance(self, functions: List[Dict]) -> Dict:
        """Analyze performance characteristics of workflow"""
        total_complexity = 0
        async_count = 0
        external_calls = 0
        
        for func in functions:
            complexity = func.get('semantic_complexity', {})
            total_complexity += complexity.get('business_rules', 0)
            
            if func.get('is_async'):
                async_count += 1
            
            external_calls += complexity.get('external_dependencies', 0)
        
        return {
            "total_complexity": total_complexity,
            "async_operations": async_count,
            "external_dependencies": external_calls,
            "estimated_performance": "high" if total_complexity < 10 else "medium" if total_complexity < 20 else "low"
        }

    def _identify_workflow_state_changes(self, functions: List[Dict]) -> List[str]:
        """Identify state changes in workflow"""
        state_changes = []
        
        for func in functions:
            side_effects = func.get('side_effects', [])
            for effect in side_effects:
                if 'modification' in effect.lower() or 'create' in effect.lower() or 'update' in effect.lower():
                    state_changes.append(effect)
        
        return state_changes

    def _extract_function_transformations(self, func: Dict) -> List[Dict]:
        """Extract transformations from function"""
        transformations = []
        func_name = func.get('name', '')
        
        # Get transformations identified earlier
        func_transformations = self._identify_function_transformations(func)
        
        for transform_type in func_transformations:
            transformation = {
                "function": func_name,
                "type": transform_type,
                "input_type": self._infer_transformation_input(func),
                "output_type": self._infer_transformation_output(func),
                "complexity": func.get('complexity', 0)
            }
            transformations.append(transformation)
        
        return transformations

    def _extract_class_transformations(self, cls: Dict) -> List[Dict]:
        """Extract transformations from class methods"""
        transformations = []
        methods = cls.get('methods', [])
        
        for method in methods:
            method_transformations = self._extract_function_transformations(method)
            for transform in method_transformations:
                transform['class'] = cls.get('name', '')
            transformations.extend(method_transformations)
        
        return transformations

    def _categorize_transformations(self, transformations: List[Dict]) -> List[Dict]:
        """Categorize and group transformations"""
        categories = defaultdict(list)
        
        for transform in transformations:
            transform_type = transform.get('type', 'unknown')
            categories[transform_type].append(transform)
        
        categorized = []
        for category, transforms in categories.items():
            categorized.append({
                "category": category,
                "count": len(transforms),
                "functions": list(set([t.get('function', '') for t in transforms])),
                "complexity": sum([t.get('complexity', 0) for t in transforms])
            })
        
        return categorized

    def _is_state_container(self, cls: Dict) -> bool:
        """Check if class is a state container"""
        methods = cls.get('methods', [])
        method_names = [m.get('name', '').lower() for m in methods]
        
        # Check for state management methods
        state_indicators = [
            any('get_state' in name or 'set_state' in name for name in method_names),
            any('transition' in name for name in method_names),
            any('save' in name or 'persist' in name for name in method_names),
            len([name for name in method_names if name.startswith('set_')]) > 2
        ]
        
        return any(state_indicators)

    def _extract_state_attributes(self, cls: Dict) -> List[str]:
        """Extract state attributes from class"""
        attributes = cls.get('attributes', [])
        state_attrs = []
        
        for attr in attributes:
            attr_name = attr.get('name', '').lower()
            if any(indicator in attr_name for indicator in ['state', 'status', 'phase', 'stage']):
                state_attrs.append(attr.get('name', ''))
        
        return state_attrs

    def _extract_state_operations(self, cls: Dict) -> List[str]:
        """Extract state operations from class"""
        methods = cls.get('methods', [])
        operations = []
        
        for method in methods:
            method_name = method.get('name', '').lower()
            if any(pattern in method_name for pattern in ['set_', 'update_', 'change_', 'transition_']):
                operations.append(method.get('name', ''))
        
        return operations

    def _extract_lifecycle_methods(self, cls: Dict) -> List[str]:
        """Extract lifecycle methods from class"""
        methods = cls.get('methods', [])
        lifecycle_methods = []
        
        for method in methods:
            method_name = method.get('name', '')
            if method_name in ['__init__', '__del__', '__enter__', '__exit__'] or \
               any(pattern in method_name.lower() for pattern in ['create', 'destroy', 'cleanup', 'initialize']):
                lifecycle_methods.append(method_name)
        
        return lifecycle_methods

    def _identify_function_state_transitions(self, func: Dict) -> List[Dict]:
        """Identify state transitions in function"""
        transitions = []
        calls = func.get('calls', [])
        
        for call in calls:
            call_lower = call.lower()
            if any(pattern in call_lower for pattern in ['set_state', 'transition', 'change_state', 'update_status']):
                transitions.append({
                    "function": func.get('name', ''),
                    "transition_call": call,
                    "type": "state_change"
                })
        
        return transitions

    def _identify_persistence_patterns(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Identify state persistence patterns"""
        patterns = []
        
        # Check for repository patterns
        repo_classes = [cls for cls in classes if 'repository' in cls.get('name', '').lower()]
        if repo_classes:
            patterns.append({
                "pattern": "Repository Pattern",
                "classes": [cls.get('name', '') for cls in repo_classes],
                "description": "Data persistence abstraction"
            })
        
        # Check for ORM patterns
        orm_indicators = []
        for func in functions:
            calls = func.get('calls', [])
            for call in calls:
                if any(pattern in call.lower() for pattern in ['session.', 'query.', 'save()', 'commit()']):
                    orm_indicators.append(call)
        
        if orm_indicators:
            patterns.append({
                "pattern": "ORM Pattern",
                "indicators": orm_indicators[:5],
                "description": "Object-relational mapping for persistence"
            })
        
        return patterns

    def _identify_state_validation_patterns(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Identify state validation patterns"""
        patterns = []
        
        # Check for validation functions
        validation_functions = [func for func in functions if 'validate' in func.get('name', '').lower()]
        if validation_functions:
            patterns.append({
                "pattern": "Validation Functions",
                "functions": [func.get('name', '') for func in validation_functions],
                "description": "Explicit state validation"
            })
        
        # Check for validation in models
        for cls in classes:
            methods = cls.get('methods', [])
            validation_methods = [m for m in methods if 'validate' in m.get('name', '').lower()]
            if validation_methods:
                patterns.append({
                    "pattern": "Model Validation",
                    "class": cls.get('name', ''),
                    "methods": [m.get('name', '') for m in validation_methods],
                    "description": "Built-in model validation"
                })
        
        return patterns

    def _identify_external_integration(self, call: str, func: Dict) -> Optional[Dict]:
        """Identify external integration from function call"""
        call_lower = call.lower()
        
        # HTTP/REST API calls
        if any(pattern in call_lower for pattern in ['http', 'request', 'get(', 'post(', 'put(', 'delete(']):
            return {
                "type": "HTTP_API",
                "function": func.get('name', ''),
                "call": call,
                "endpoint": self._extract_endpoint_from_call(call),
                "data_format": "JSON"
            }
        
        # Database calls
        if any(pattern in call_lower for pattern in ['query', 'execute', 'session', 'db.']):
            return {
                "type": "Database",
                "function": func.get('name', ''),
                "call": call,
                "endpoint": "database",
                "data_format": "SQL"
            }
        
        # Message queue calls
        if any(pattern in call_lower for pattern in ['publish', 'subscribe', 'queue', 'message']):
            return {
                "type": "Message_Queue",
                "function": func.get('name', ''),
                "call": call,
                "endpoint": "message_broker",
                "data_format": "Message"
            }
        
        return None

    def _analyze_integration_error_handling(self, integrations: List[Dict]) -> Dict:
        """Analyze error handling for integrations"""
        error_handling = {
            "retry_patterns": [],
            "timeout_handling": [],
            "fallback_strategies": []
        }
        
        # This would require more detailed analysis of the actual integration code
        # For now, return basic structure
        return error_handling

    def _is_database_call(self, call: str) -> bool:
        """Check if call is a database operation"""
        call_lower = call.lower()
        return any(pattern in call_lower for pattern in ['db.', 'session.', 'query', 'execute', 'commit', 'rollback'])

    def _is_external_call(self, call: str) -> bool:
        """Check if call is to external system"""
        call_lower = call.lower()
        return any(pattern in call_lower for pattern in ['http', 'request', 'client.', 'api.', 'service.'])

    def _is_data_entity(self, cls: Dict) -> bool:
        """Check if class represents a data entity"""
        class_name = cls.get('name', '').lower()
        base_classes = cls.get('base_classes', [])
        
        entity_indicators = [
            'model' in class_name,
            'entity' in class_name,
            any('base' in base.lower() for base in base_classes),
            any('model' in base.lower() for base in base_classes)
        ]
        
        return any(entity_indicators)

    def _find_data_sources(self, entity: Dict, functions: List[Dict]) -> List[str]:
        """Find data sources for entity"""
        entity_name = entity.get('name', '')
        sources = []
        
        for func in functions:
            return_type = func.get('return_type', '')
            if entity_name in return_type:
                sources.append(func.get('name', ''))
        
        return sources

    def _find_data_transformations(self, entity: Dict, functions: List[Dict]) -> List[str]:
        """Find transformations applied to entity"""
        entity_name = entity.get('name', '')
        transformations = []
        
        for func in functions:
            parameters = func.get('parameters', [])
            for param in parameters:
                param_type = param.get('type', '')
                if entity_name in param_type:
                    func_transformations = self._identify_function_transformations(func)
                    transformations.extend(func_transformations)
        
        return list(set(transformations))

    def _find_data_destinations(self, entity: Dict, functions: List[Dict]) -> List[str]:
        """Find destinations for entity data"""
        entity_name = entity.get('name', '')
        destinations = []
        
        for func in functions:
            calls = func.get('calls', [])
            parameters = func.get('parameters', [])
            
            # Check if entity is used as parameter
            for param in parameters:
                param_type = param.get('type', '')
                if entity_name in param_type:
                    # Check what this function does with the entity
                    for call in calls:
                        if any(pattern in call.lower() for pattern in ['save', 'store', 'send', 'publish']):
                            destinations.append(call)
        
        return destinations

    def _trace_entity_lifecycle(self, entity: Dict, functions: List[Dict]) -> List[str]:
        """Trace lifecycle of entity"""
        entity_name = entity.get('name', '')
        lifecycle = []
        
        for func in functions:
            func_name = func.get('name', '').lower()
            return_type = func.get('return_type', '')
            
            # Check if function creates entity
            if entity_name in return_type and any(pattern in func_name for pattern in ['create', 'new', 'build']):
                lifecycle.append(f"Created by {func.get('name', '')}")
            
            # Check if function modifies entity
            parameters = func.get('parameters', [])
            for param in parameters:
                param_type = param.get('type', '')
                if entity_name in param_type and any(pattern in func_name for pattern in ['update', 'modify', 'change']):
                    lifecycle.append(f"Modified by {func.get('name', '')}")
        
        return lifecycle

    def _is_pipeline_pattern(self, steps: List[Dict]) -> bool:
        """Check if steps form a pipeline pattern"""
        # Simple check - sequential processing where output of one step feeds into next
        if len(steps) < 2:
            return False
        
        for i in range(len(steps) - 1):
            current_outputs = steps[i].get('outputs', [])
            next_inputs = steps[i + 1].get('inputs', [])
            
            # Check if there's data flow between steps
            if not any(output in next_inputs for output in current_outputs):
                return False
        
        return True

    def _is_scatter_gather_pattern(self, steps: List[Dict]) -> bool:
        """Check if steps form a scatter-gather pattern"""
        # Look for parallel processing followed by aggregation
        return len(steps) > 3 and any('aggregate' in step.get('step_name', '').lower() for step in steps)

    def _is_saga_pattern(self, steps: List[Dict]) -> bool:
        """Check if steps form a saga pattern"""
        # Look for compensation or rollback mechanisms
        return any(any(keyword in step.get('step_name', '').lower() for keyword in ['compensate', 'rollback', 'undo']) for step in steps)

    def _is_event_driven_pattern(self, steps: List[Dict]) -> bool:
        """Check if steps form an event-driven pattern"""
        # Look for event handling or publishing
        return any(any(keyword in step.get('step_name', '').lower() for keyword in ['event', 'publish', 'handle', 'notify']) for step in steps)

    def _infer_transformation_input(self, func: Dict) -> str:
        """Infer input type for transformation"""
        parameters = func.get('parameters', [])
        if parameters:
            first_param = parameters[0]
            return first_param.get('type', 'Unknown')
        return 'Unknown'

    def _infer_transformation_output(self, func: Dict) -> str:
        """Infer output type for transformation"""
        return func.get('return_type', 'Unknown')

    def _extract_endpoint_from_call(self, call: str) -> str:
        """Extract endpoint from HTTP call"""
        # Simple extraction - look for URL patterns
        url_match = re.search(r'["\']([^"\']*://[^"\']+)["\']', call)
        if url_match:
            return url_match.group(1)
        return 'unknown_endpoint'

    def _identify_cross_capability_workflows(self, functions: List[Dict], data_flow_graph: Dict) -> List[Dict]:
        """Identify workflows that span multiple business capabilities"""
        cross_workflows = []
        
        # This would require more sophisticated analysis of function call chains
        # For now, return empty list
        return cross_workflows
