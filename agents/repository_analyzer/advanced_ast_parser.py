"""
Advanced AST Parser with Semantic Analysis
Goes beyond syntax to understand semantics and business intent
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SemanticASTParser:
    """Goes beyond syntax to understand semantics"""
    
    def __init__(self):
        # Business intent keywords for semantic analysis
        self.business_intent_patterns = {
            'validation': [
                r'validate_\w+', r'check_\w+', r'verify_\w+', r'is_valid_\w+',
                r'\w+_validator', r'ensure_\w+', r'assert_\w+'
            ],
            'transformation': [
                r'transform_\w+', r'convert_\w+', r'map_\w+', r'serialize_\w+',
                r'deserialize_\w+', r'format_\w+', r'parse_\w+'
            ],
            'business_logic': [
                r'calculate_\w+', r'compute_\w+', r'determine_\w+', r'evaluate_\w+',
                r'apply_\w+', r'process_\w+', r'handle_\w+'
            ],
            'data_access': [
                r'get_\w+', r'find_\w+', r'fetch_\w+', r'load_\w+',
                r'save_\w+', r'store_\w+', r'update_\w+', r'delete_\w+'
            ],
            'workflow': [
                r'execute_\w+', r'run_\w+', r'perform_\w+', r'trigger_\w+',
                r'initiate_\w+', r'complete_\w+', r'finalize_\w+'
            ]
        }
        
        # Data transformation patterns
        self.data_flow_patterns = {
            'input_validation': ['request', 'input', 'data', 'payload'],
            'business_processing': ['entity', 'model', 'aggregate', 'service'],
            'output_formatting': ['response', 'output', 'result', 'dto']
        }
        
        # Exception handling patterns
        self.exception_patterns = [
            r'ValidationError', r'BusinessError', r'ServiceError',
            r'\w+Exception', r'\w+Error', r'Invalid\w+', r'Unauthorized\w+'
        ]

    def analyze_with_context(self, filepath: str) -> Dict:
        """Analyzes file with semantic context understanding"""
        logger.info(f"Analyzing file with semantic context: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content, filename=filepath)
            relative_path = str(Path(filepath).name)
            
            # Perform semantic analysis
            analysis = {
                'file_path': relative_path,
                'semantic_functions': self._analyze_functions_semantically(tree, content),
                'semantic_classes': self._analyze_classes_semantically(tree, content),
                'data_transformations': self._analyze_data_transformations(tree, content),
                'business_logic_flow': self._analyze_business_logic_flow(tree, content),
                'error_handling_strategy': self._analyze_error_handling(tree, content),
                'api_semantics': self._analyze_api_semantics(tree, content),
                'dependency_semantics': self._analyze_dependency_semantics(tree, content)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {filepath}: {e}")
            return {
                'file_path': filepath,
                'error': str(e),
                'semantic_functions': [],
                'semantic_classes': [],
                'data_transformations': [],
                'business_logic_flow': [],
                'error_handling_strategy': {},
                'api_semantics': [],
                'dependency_semantics': []
            }

    def _analyze_functions_semantically(self, tree: ast.AST, content: str) -> List[Dict]:
        """Analyze functions with semantic understanding"""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_analysis = self._extract_semantic_function_info(node, content)
                functions.append(func_analysis)
        
        return functions

    def _extract_semantic_function_info(self, node: ast.FunctionDef, content: str) -> Dict:
        """Extract semantic information from function"""
        func_name = node.name
        
        # Determine business intent from name
        business_intent = self._classify_business_intent(func_name)
        
        # Analyze parameters semantically
        semantic_params = self._analyze_parameters_semantically(node.args)
        
        # Analyze return type semantically
        return_semantics = self._analyze_return_semantics(node)
        
        # Analyze function body for business logic
        business_logic = self._extract_business_logic_from_body(node)
        
        # Analyze data flow within function
        data_flow = self._trace_data_flow_in_function(node)
        
        # Extract side effects
        side_effects = self._identify_side_effects(node)
        
        # Calculate semantic complexity
        semantic_complexity = self._calculate_semantic_complexity(node)
        
        return {
            'name': func_name,
            'line_number': node.lineno,
            'is_async': isinstance(node, ast.AsyncFunctionDef),
            'business_intent': business_intent,
            'semantic_purpose': self._infer_semantic_purpose(func_name, business_intent),
            'parameters': semantic_params,
            'return_semantics': return_semantics,
            'business_logic': business_logic,
            'data_flow': data_flow,
            'side_effects': side_effects,
            'semantic_complexity': semantic_complexity,
            'error_handling': self._analyze_function_error_handling(node),
            'dependencies': self._extract_semantic_dependencies(node)
        }

    def _analyze_classes_semantically(self, tree: ast.AST, content: str) -> List[Dict]:
        """Analyze classes with semantic understanding"""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_analysis = self._extract_semantic_class_info(node, content)
                classes.append(class_analysis)
        
        return classes

    def _extract_semantic_class_info(self, node: ast.ClassDef, content: str) -> Dict:
        """Extract semantic information from class"""
        class_name = node.name
        
        # Determine class archetype
        class_archetype = self._classify_class_archetype(class_name, node)
        
        # Analyze class responsibility
        responsibility = self._infer_class_responsibility(class_name, node)
        
        # Analyze class relationships
        relationships = self._analyze_class_relationships(node)
        
        # Extract business invariants
        invariants = self._extract_business_invariants(node)
        
        # Analyze lifecycle methods
        lifecycle = self._analyze_class_lifecycle(node)
        
        return {
            'name': class_name,
            'line_number': node.lineno,
            'class_archetype': class_archetype,
            'responsibility': responsibility,
            'relationships': relationships,
            'business_invariants': invariants,
            'lifecycle': lifecycle,
            'state_management': self._analyze_state_management(node),
            'encapsulation_level': self._assess_encapsulation(node),
            'semantic_methods': [self._extract_semantic_function_info(method, content) 
                                for method in node.body if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))]
        }

    def _analyze_data_transformations(self, tree: ast.AST, content: str) -> List[Dict]:
        """Analyze data transformations in the code"""
        transformations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Look for transformation patterns in function
                transform_info = self._detect_transformation_pattern(node)
                if transform_info:
                    transformations.append(transform_info)
        
        return transformations

    def _analyze_business_logic_flow(self, tree: ast.AST, content: str) -> List[Dict]:
        """Analyze business logic flow patterns"""
        flows = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Analyze control flow for business patterns
                flow_info = self._extract_business_flow(node)
                if flow_info:
                    flows.append(flow_info)
        
        return flows

    def _analyze_error_handling(self, tree: ast.AST, content: str) -> Dict:
        """Analyze error handling strategy"""
        error_handling = {
            'exception_types': [],
            'handling_patterns': [],
            'error_propagation': [],
            'recovery_strategies': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                # Analyze exception handling
                exception_info = self._analyze_exception_handler(node)
                error_handling['handling_patterns'].append(exception_info)
            
            elif isinstance(node, ast.Raise):
                # Analyze error propagation
                raise_info = self._analyze_raise_statement(node)
                error_handling['error_propagation'].append(raise_info)
        
        return error_handling

    def _analyze_api_semantics(self, tree: ast.AST, content: str) -> List[Dict]:
        """Analyze API endpoint semantics"""
        api_endpoints = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for API decorators
                api_info = self._extract_api_endpoint_info(node)
                if api_info:
                    api_endpoints.append(api_info)
        
        return api_endpoints

    def _analyze_dependency_semantics(self, tree: ast.AST, content: str) -> List[Dict]:
        """Analyze semantic dependencies"""
        dependencies = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                dep_info = self._extract_dependency_semantics(node)
                dependencies.append(dep_info)
        
        return dependencies

    # Helper methods for semantic analysis
    def _classify_business_intent(self, func_name: str) -> str:
        """Classify the business intent of a function"""
        func_name_lower = func_name.lower()
        
        for intent, patterns in self.business_intent_patterns.items():
            for pattern in patterns:
                if re.match(pattern, func_name_lower):
                    return intent
        
        return 'general'

    def _infer_semantic_purpose(self, func_name: str, business_intent: str) -> str:
        """Infer the semantic purpose of a function"""
        purpose_templates = {
            'validation': f"Validates {self._extract_domain_concept(func_name)} according to business rules",
            'transformation': f"Transforms {self._extract_domain_concept(func_name)} data format",
            'business_logic': f"Implements business logic for {self._extract_domain_concept(func_name)}",
            'data_access': f"Accesses {self._extract_domain_concept(func_name)} data from storage",
            'workflow': f"Executes {self._extract_domain_concept(func_name)} workflow process"
        }
        
        return purpose_templates.get(business_intent, f"Handles {self._extract_domain_concept(func_name)} operations")

    def _extract_domain_concept(self, name: str) -> str:
        """Extract domain concept from function/class name"""
        # Remove common prefixes/suffixes
        clean_name = re.sub(r'^(get_|set_|create_|update_|delete_|validate_|check_)', '', name.lower())
        clean_name = re.sub(r'(_service|_repository|_controller|_handler)$', '', clean_name)
        
        return clean_name.replace('_', ' ')

    def _analyze_parameters_semantically(self, args: ast.arguments) -> List[Dict]:
        """Analyze function parameters semantically"""
        semantic_params = []
        
        for arg in args.args:
            param_info = {
                'name': arg.arg,
                'type': ast.unparse(arg.annotation) if arg.annotation else None,
                'semantic_role': self._infer_parameter_role(arg.arg),
                'data_category': self._classify_data_category(arg.arg)
            }
            semantic_params.append(param_info)
        
        return semantic_params

    def _infer_parameter_role(self, param_name: str) -> str:
        """Infer the semantic role of a parameter"""
        param_lower = param_name.lower()
        
        if any(word in param_lower for word in ['id', 'key', 'identifier']):
            return 'identifier'
        elif any(word in param_lower for word in ['data', 'payload', 'request']):
            return 'input_data'
        elif any(word in param_lower for word in ['config', 'settings', 'options']):
            return 'configuration'
        elif any(word in param_lower for word in ['callback', 'handler', 'func']):
            return 'behavior'
        else:
            return 'domain_data'

    def _classify_data_category(self, param_name: str) -> str:
        """Classify parameter into data category"""
        param_lower = param_name.lower()
        
        if any(word in param_lower for word in ['user', 'account', 'profile']):
            return 'user_data'
        elif any(word in param_lower for word in ['hotel', 'room', 'booking']):
            return 'business_entity'
        elif any(word in param_lower for word in ['payment', 'transaction', 'billing']):
            return 'financial_data'
        else:
            return 'general_data'

    def _analyze_return_semantics(self, node: ast.FunctionDef) -> Dict:
        """Analyze return value semantics"""
        return_info = {
            'type': ast.unparse(node.returns) if node.returns else None,
            'semantic_meaning': 'unknown',
            'data_category': 'unknown'
        }
        
        if node.returns:
            return_type = ast.unparse(node.returns)
            return_info['semantic_meaning'] = self._infer_return_meaning(node.name, return_type)
            return_info['data_category'] = self._classify_return_category(return_type)
        
        return return_info

    def _infer_return_meaning(self, func_name: str, return_type: str) -> str:
        """Infer the meaning of return value"""
        func_lower = func_name.lower()
        
        if func_lower.startswith('get_') or func_lower.startswith('find_'):
            return 'retrieved_entity'
        elif func_lower.startswith('create_'):
            return 'created_entity'
        elif func_lower.startswith('update_'):
            return 'updated_entity'
        elif func_lower.startswith('validate_') or func_lower.startswith('check_'):
            return 'validation_result'
        elif 'bool' in return_type.lower():
            return 'boolean_result'
        else:
            return 'processed_data'

    def _classify_return_category(self, return_type: str) -> str:
        """Classify return type category"""
        type_lower = return_type.lower()
        
        if 'user' in type_lower:
            return 'user_data'
        elif any(word in type_lower for word in ['hotel', 'room', 'booking']):
            return 'business_entity'
        elif 'response' in type_lower:
            return 'api_response'
        elif any(word in type_lower for word in ['list', 'dict', 'optional']):
            return 'collection_data'
        else:
            return 'simple_data'

    def _extract_business_logic_from_body(self, node: ast.FunctionDef) -> List[str]:
        """Extract business logic patterns from function body"""
        business_logic = []
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.If):
                # Business rule conditions
                condition_logic = self._extract_condition_logic(stmt)
                if condition_logic:
                    business_logic.append(condition_logic)
            
            elif isinstance(stmt, ast.Call):
                # Business operations
                call_logic = self._extract_call_logic(stmt)
                if call_logic:
                    business_logic.append(call_logic)
        
        return business_logic

    def _trace_data_flow_in_function(self, node: ast.FunctionDef) -> Dict:
        """Trace data flow within function"""
        data_flow = {
            'input_processing': [],
            'transformations': [],
            'output_generation': []
        }
        
        # Analyze assignments and transformations
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Assign):
                flow_info = self._analyze_assignment_flow(stmt)
                data_flow['transformations'].append(flow_info)
        
        return data_flow

    def _identify_side_effects(self, node: ast.FunctionDef) -> List[str]:
        """Identify side effects in function"""
        side_effects = []
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Call):
                call_name = self._get_call_name(stmt)
                if call_name:
                    if any(word in call_name.lower() for word in ['save', 'create', 'update', 'delete']):
                        side_effects.append(f"Data modification: {call_name}")
                    elif any(word in call_name.lower() for word in ['send', 'notify', 'email']):
                        side_effects.append(f"External communication: {call_name}")
                    elif any(word in call_name.lower() for word in ['log', 'track', 'record']):
                        side_effects.append(f"Logging/tracking: {call_name}")
        
        return side_effects

    def _calculate_semantic_complexity(self, node: ast.FunctionDef) -> Dict:
        """Calculate semantic complexity metrics"""
        complexity = {
            'business_rules': 0,
            'data_transformations': 0,
            'external_dependencies': 0,
            'error_paths': 0
        }
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.If):
                complexity['business_rules'] += 1
            elif isinstance(stmt, ast.Call):
                call_name = self._get_call_name(stmt)
                if call_name and any(word in call_name.lower() for word in ['transform', 'convert', 'map']):
                    complexity['data_transformations'] += 1
                elif call_name and '.' in call_name:
                    complexity['external_dependencies'] += 1
            elif isinstance(stmt, (ast.ExceptHandler, ast.Raise)):
                complexity['error_paths'] += 1
        
        return complexity

    def _analyze_function_error_handling(self, node: ast.FunctionDef) -> Dict:
        """Analyze error handling in function"""
        error_handling = {
            'try_blocks': 0,
            'exception_types': [],
            'error_recovery': []
        }
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Try):
                error_handling['try_blocks'] += 1
            elif isinstance(stmt, ast.ExceptHandler):
                if stmt.type:
                    error_handling['exception_types'].append(ast.unparse(stmt.type))
        
        return error_handling

    def _extract_semantic_dependencies(self, node: ast.FunctionDef) -> List[Dict]:
        """Extract semantic dependencies from function"""
        dependencies = []
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Call):
                dep_info = self._analyze_call_dependency(stmt)
                if dep_info:
                    dependencies.append(dep_info)
        
        return dependencies

    def _classify_class_archetype(self, class_name: str, node: ast.ClassDef) -> str:
        """Classify class into architectural archetype"""
        class_lower = class_name.lower()
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        
        if 'service' in class_lower:
            return 'service'
        elif 'repository' in class_lower:
            return 'repository'
        elif 'controller' in class_lower:
            return 'controller'
        elif 'model' in class_lower or 'entity' in class_lower:
            return 'entity'
        elif any(base.id in ['BaseModel', 'Enum'] for base in node.bases if isinstance(base, ast.Name)):
            return 'data_model'
        elif len([m for m in methods if not m.startswith('_')]) > 3:
            return 'aggregate'
        else:
            return 'value_object'

    def _infer_class_responsibility(self, class_name: str, node: ast.ClassDef) -> str:
        """Infer class responsibility from structure"""
        archetype = self._classify_class_archetype(class_name, node)
        domain = self._extract_domain_concept(class_name)
        
        responsibility_templates = {
            'service': f"Orchestrates {domain} business operations",
            'repository': f"Manages {domain} data persistence",
            'controller': f"Handles {domain} API requests and responses",
            'entity': f"Represents {domain} business entity with behavior",
            'data_model': f"Defines {domain} data structure and validation",
            'aggregate': f"Manages {domain} aggregate consistency",
            'value_object': f"Represents {domain} immutable value"
        }
        
        return responsibility_templates.get(archetype, f"Handles {domain} operations")

    def _analyze_class_relationships(self, node: ast.ClassDef) -> Dict:
        """Analyze class relationships"""
        relationships = {
            'inheritance': [base.id for base in node.bases if isinstance(base, ast.Name)],
            'composition': [],
            'dependencies': []
        }
        
        # Analyze method calls and attribute access for relationships
        for method in node.body:
            if isinstance(method, ast.FunctionDef):
                for stmt in ast.walk(method):
                    if isinstance(stmt, ast.Call):
                        call_info = self._analyze_relationship_call(stmt)
                        if call_info:
                            relationships['dependencies'].append(call_info)
        
        return relationships

    def _extract_business_invariants(self, node: ast.ClassDef) -> List[str]:
        """Extract business invariants from class"""
        invariants = []
        
        for method in node.body:
            if isinstance(method, ast.FunctionDef):
                # Look for validation methods
                if 'validate' in method.name.lower() or 'check' in method.name.lower():
                    invariant = f"Business rule enforced by {method.name}"
                    invariants.append(invariant)
        
        return invariants

    def _analyze_class_lifecycle(self, node: ast.ClassDef) -> Dict:
        """Analyze class lifecycle methods"""
        lifecycle = {
            'creation': [],
            'modification': [],
            'destruction': []
        }
        
        for method in node.body:
            if isinstance(method, ast.FunctionDef):
                method_lower = method.name.lower()
                if any(word in method_lower for word in ['create', 'new', '__init__']):
                    lifecycle['creation'].append(method.name)
                elif any(word in method_lower for word in ['update', 'modify', 'change', 'set']):
                    lifecycle['modification'].append(method.name)
                elif any(word in method_lower for word in ['delete', 'remove', 'destroy']):
                    lifecycle['destruction'].append(method.name)
        
        return lifecycle

    def _analyze_state_management(self, node: ast.ClassDef) -> Dict:
        """Analyze how class manages state"""
        state_info = {
            'mutable_state': False,
            'state_transitions': [],
            'state_validation': False
        }
        
        # Check for state-related methods
        for method in node.body:
            if isinstance(method, ast.FunctionDef):
                method_lower = method.name.lower()
                if any(word in method_lower for word in ['state', 'status', 'transition']):
                    state_info['state_transitions'].append(method.name)
                elif 'validate' in method_lower:
                    state_info['state_validation'] = True
                elif method.name.startswith('set_'):
                    state_info['mutable_state'] = True
        
        return state_info

    def _assess_encapsulation(self, node: ast.ClassDef) -> str:
        """Assess encapsulation level of class"""
        public_methods = len([m for m in node.body if isinstance(m, ast.FunctionDef) and not m.name.startswith('_')])
        private_methods = len([m for m in node.body if isinstance(m, ast.FunctionDef) and m.name.startswith('_')])
        
        if private_methods > public_methods:
            return 'high'
        elif private_methods > 0:
            return 'medium'
        else:
            return 'low'

    # Additional helper methods
    def _detect_transformation_pattern(self, node: ast.FunctionDef) -> Optional[Dict]:
        """Detect data transformation patterns"""
        func_name = node.name.lower()
        
        if any(word in func_name for word in ['transform', 'convert', 'map', 'serialize']):
            return {
                'function': node.name,
                'transformation_type': self._classify_transformation_type(func_name),
                'input_type': self._infer_input_type(node),
                'output_type': self._infer_output_type(node)
            }
        
        return None

    def _classify_transformation_type(self, func_name: str) -> str:
        """Classify type of transformation"""
        if 'serialize' in func_name:
            return 'serialization'
        elif 'deserialize' in func_name:
            return 'deserialization'
        elif 'convert' in func_name:
            return 'type_conversion'
        elif 'map' in func_name:
            return 'data_mapping'
        else:
            return 'general_transformation'

    def _extract_business_flow(self, node: ast.FunctionDef) -> Optional[Dict]:
        """Extract business flow from function"""
        # Look for sequential business operations
        operations = []
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Call):
                call_name = self._get_call_name(stmt)
                if call_name and self._is_business_operation(call_name):
                    operations.append(call_name)
        
        if len(operations) > 1:
            return {
                'function': node.name,
                'business_operations': operations,
                'flow_type': 'sequential_workflow'
            }
        
        return None

    def _is_business_operation(self, call_name: str) -> bool:
        """Check if call represents a business operation"""
        business_verbs = ['create', 'update', 'delete', 'validate', 'process', 'calculate', 'send', 'notify']
        return any(verb in call_name.lower() for verb in business_verbs)

    def _analyze_exception_handler(self, node: ast.ExceptHandler) -> Dict:
        """Analyze exception handler"""
        return {
            'exception_type': ast.unparse(node.type) if node.type else 'Exception',
            'handling_strategy': self._infer_handling_strategy(node),
            'recovery_action': self._extract_recovery_action(node)
        }

    def _analyze_raise_statement(self, node: ast.Raise) -> Dict:
        """Analyze raise statement"""
        return {
            'exception_type': ast.unparse(node.exc) if node.exc else 'Unknown',
            'context': 'error_propagation'
        }

    def _extract_api_endpoint_info(self, node: ast.FunctionDef) -> Optional[Dict]:
        """Extract API endpoint information"""
        # Check for API decorators
        api_decorators = []
        for decorator in node.decorator_list:
            decorator_name = self._get_decorator_name(decorator)
            if any(word in decorator_name.lower() for word in ['get', 'post', 'put', 'delete', 'patch']):
                api_decorators.append(decorator_name)
        
        if api_decorators:
            return {
                'function': node.name,
                'http_methods': api_decorators,
                'endpoint_purpose': self._infer_endpoint_purpose(node.name),
                'request_handling': self._analyze_request_handling(node),
                'response_generation': self._analyze_response_generation(node)
            }
        
        return None

    def _extract_dependency_semantics(self, node: ast.Import) -> Dict:
        """Extract semantic information about dependencies"""
        if isinstance(node, ast.Import):
            module_name = node.names[0].name
        else:  # ast.ImportFrom
            module_name = node.module or 'relative_import'
        
        return {
            'module': module_name,
            'dependency_type': self._classify_dependency_type(module_name),
            'usage_purpose': self._infer_dependency_purpose(module_name)
        }

    def _classify_dependency_type(self, module_name: str) -> str:
        """Classify dependency type"""
        if any(word in module_name.lower() for word in ['fastapi', 'flask', 'django']):
            return 'web_framework'
        elif any(word in module_name.lower() for word in ['sqlalchemy', 'django.db']):
            return 'database_orm'
        elif any(word in module_name.lower() for word in ['pydantic', 'marshmallow']):
            return 'validation'
        elif any(word in module_name.lower() for word in ['requests', 'httpx']):
            return 'http_client'
        else:
            return 'utility'

    # Utility methods
    def _get_call_name(self, call_node: ast.Call) -> Optional[str]:
        """Get the name of a function call"""
        try:
            if isinstance(call_node.func, ast.Name):
                return call_node.func.id
            elif isinstance(call_node.func, ast.Attribute):
                return ast.unparse(call_node.func)
            else:
                return None
        except:
            return None

    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name"""
        try:
            if isinstance(decorator, ast.Name):
                return decorator.id
            elif isinstance(decorator, ast.Attribute):
                return ast.unparse(decorator)
            else:
                return ast.unparse(decorator)
        except:
            return 'unknown'

    def _extract_condition_logic(self, if_node: ast.If) -> Optional[str]:
        """Extract business logic from if condition"""
        try:
            condition = ast.unparse(if_node.test)
            return f"Business rule: {condition}"
        except:
            return None

    def _extract_call_logic(self, call_node: ast.Call) -> Optional[str]:
        """Extract business logic from function call"""
        call_name = self._get_call_name(call_node)
        if call_name and self._is_business_operation(call_name):
            return f"Business operation: {call_name}"
        return None

    def _analyze_assignment_flow(self, assign_node: ast.Assign) -> str:
        """Analyze data flow in assignment"""
        try:
            targets = [ast.unparse(target) for target in assign_node.targets]
            value = ast.unparse(assign_node.value)
            return f"{value} → {', '.join(targets)}"
        except:
            return "Assignment flow"

    def _analyze_call_dependency(self, call_node: ast.Call) -> Optional[Dict]:
        """Analyze dependency from function call"""
        call_name = self._get_call_name(call_node)
        if call_name and '.' in call_name:
            return {
                'dependency': call_name.split('.')[0],
                'operation': call_name,
                'dependency_type': 'external_service'
            }
        return None

    def _analyze_relationship_call(self, call_node: ast.Call) -> Optional[str]:
        """Analyze relationship from method call"""
        call_name = self._get_call_name(call_node)
        if call_name and '.' in call_name:
            return call_name.split('.')[0]
        return None

    def _infer_input_type(self, node: ast.FunctionDef) -> str:
        """Infer input type from function parameters"""
        if node.args.args:
            first_param = node.args.args[0]
            if first_param.annotation:
                return ast.unparse(first_param.annotation)
        return 'unknown'

    def _infer_output_type(self, node: ast.FunctionDef) -> str:
        """Infer output type from function return"""
        if node.returns:
            return ast.unparse(node.returns)
        return 'unknown'

    def _infer_handling_strategy(self, handler_node: ast.ExceptHandler) -> str:
        """Infer exception handling strategy"""
        if handler_node.body:
            # Analyze what happens in exception handler
            for stmt in handler_node.body:
                if isinstance(stmt, ast.Return):
                    return 'return_error_response'
                elif isinstance(stmt, ast.Raise):
                    return 'propagate_error'
                elif isinstance(stmt, ast.Call):
                    call_name = self._get_call_name(stmt)
                    if call_name and 'log' in call_name.lower():
                        return 'log_and_continue'
        return 'unknown'

    def _extract_recovery_action(self, handler_node: ast.ExceptHandler) -> str:
        """Extract recovery action from exception handler"""
        # Simple heuristic based on handler body
        if len(handler_node.body) > 1:
            return 'complex_recovery'
        else:
            return 'simple_recovery'

    def _infer_endpoint_purpose(self, func_name: str) -> str:
        """Infer API endpoint purpose"""
        func_lower = func_name.lower()
        
        if any(word in func_lower for word in ['get', 'fetch', 'retrieve']):
            return 'data_retrieval'
        elif any(word in func_lower for word in ['create', 'add', 'new']):
            return 'data_creation'
        elif any(word in func_lower for word in ['update', 'modify', 'edit']):
            return 'data_modification'
        elif any(word in func_lower for word in ['delete', 'remove']):
            return 'data_deletion'
        else:
            return 'business_operation'

    def _analyze_request_handling(self, node: ast.FunctionDef) -> List[str]:
        """Analyze request handling patterns"""
        patterns = []
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Call):
                call_name = self._get_call_name(stmt)
                if call_name:
                    if 'validate' in call_name.lower():
                        patterns.append('input_validation')
                    elif 'authenticate' in call_name.lower():
                        patterns.append('authentication')
                    elif 'authorize' in call_name.lower():
                        patterns.append('authorization')
        
        return patterns

    def _analyze_response_generation(self, node: ast.FunctionDef) -> List[str]:
        """Analyze response generation patterns"""
        patterns = []
        
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Return):
                patterns.append('return_response')
            elif isinstance(stmt, ast.Call):
                call_name = self._get_call_name(stmt)
                if call_name:
                    if 'serialize' in call_name.lower():
                        patterns.append('response_serialization')
                    elif 'format' in call_name.lower():
                        patterns.append('response_formatting')
        
        return patterns

    def _infer_dependency_purpose(self, module_name: str) -> str:
        """Infer purpose of dependency"""
        if 'fastapi' in module_name.lower():
            return 'web_api_framework'
        elif 'sqlalchemy' in module_name.lower():
            return 'database_operations'
        elif 'pydantic' in module_name.lower():
            return 'data_validation'
        elif 'requests' in module_name.lower():
            return 'http_requests'
        else:
            return 'utility_functions'
