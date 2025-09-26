"""
API & Contract Analyzer
Extracts API semantics, contracts, data models, and interfaces
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class APIEndpoint:
    path: str
    methods: List[str]
    handler_function: str
    purpose: str
    input_semantics: Dict[str, Any]
    output_semantics: Dict[str, Any]
    side_effects: List[str]
    business_capability: str

@dataclass
class DataContract:
    name: str
    type: str
    fields: List[Dict[str, Any]]
    validation_rules: List[str]
    relationships: List[Dict[str, Any]]
    usage_context: List[str]

@dataclass
class BusinessProcess:
    process: str
    trigger: str
    steps: List[Dict[str, Any]]
    outcomes: List[str]
    data_transformations: List[str]

class APIContractAnalyzer:
    """Analyzes API contracts, data models, and interfaces"""
    
    def __init__(self):
        # HTTP method patterns
        self.http_methods = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']
        
        # API framework patterns
        self.api_frameworks = {
            'fastapi': {
                'decorators': [r'@app\.(get|post|put|delete|patch)', r'@router\.(get|post|put|delete|patch)'],
                'dependency_patterns': ['Depends', 'HTTPException', 'status'],
                'response_patterns': ['Response', 'JSONResponse']
            },
            'flask': {
                'decorators': [r'@app\.route', r'@bp\.route'],
                'dependency_patterns': ['request', 'jsonify', 'abort'],
                'response_patterns': ['jsonify', 'Response']
            },
            'django': {
                'decorators': [r'@api_view', r'@require_http_methods'],
                'dependency_patterns': ['HttpResponse', 'JsonResponse'],
                'response_patterns': ['HttpResponse', 'JsonResponse']
            }
        }
        
        # Data model patterns
        self.data_model_patterns = {
            'pydantic': {
                'base_classes': ['BaseModel', 'BaseSettings'],
                'field_patterns': ['Field', 'validator', 'root_validator'],
                'validation_patterns': ['validator', 'validates']
            },
            'sqlalchemy': {
                'base_classes': ['Base', 'Model', 'db.Model'],
                'field_patterns': ['Column', 'relationship', 'ForeignKey'],
                'validation_patterns': ['validates', 'hybrid_property']
            },
            'dataclass': {
                'decorators': ['@dataclass'],
                'field_patterns': ['field', 'Field'],
                'validation_patterns': ['__post_init__']
            }
        }
        
        # Business operation patterns
        self.business_operations = {
            'crud': ['create', 'read', 'update', 'delete', 'get', 'post', 'put', 'patch'],
            'authentication': ['login', 'logout', 'register', 'authenticate', 'authorize'],
            'validation': ['validate', 'verify', 'check', 'confirm'],
            'transformation': ['transform', 'convert', 'serialize', 'deserialize', 'format'],
            'notification': ['notify', 'send', 'email', 'sms', 'alert'],
            'processing': ['process', 'handle', 'execute', 'run', 'perform'],
            'search': ['search', 'find', 'filter', 'query', 'lookup']
        }
        
        # Error handling patterns
        self.error_patterns = {
            'http_errors': ['HTTPException', 'abort', '400', '401', '403', '404', '500'],
            'validation_errors': ['ValidationError', 'ValueError', 'TypeError'],
            'business_errors': ['BusinessError', 'DomainError', 'ApplicationError']
        }

    def extract_api_semantics(self, code_analysis: Dict) -> Dict:
        """Extract API semantics and contracts"""
        logger.info("Extracting API semantics and contracts...")
        
        try:
            functions = code_analysis.get('functions', [])
            classes = code_analysis.get('classes', [])
            
            # Extract API endpoints
            api_endpoints = self._extract_api_endpoints(functions, classes)
            
            # Extract data contracts
            data_contracts = self._extract_data_contracts(classes)
            
            # Extract business processes
            business_processes = self._extract_business_processes(functions, api_endpoints)
            
            # Extract error handling strategy
            error_handling = self._extract_error_handling_strategy(functions, classes)
            
            # Extract interface contracts
            interface_contracts = self._extract_interface_contracts(classes)
            
            return {
                "api_contracts": api_endpoints,
                "data_contracts": data_contracts,
                "business_processes": business_processes,
                "error_handling_strategy": error_handling,
                "interface_contracts": interface_contracts,
                "integration_patterns": self._identify_integration_patterns(functions, classes),
                "security_contracts": self._extract_security_contracts(functions, classes)
            }
            
        except Exception as e:
            logger.error(f"Error extracting API semantics: {e}")
            return {
                "api_contracts": [],
                "data_contracts": [],
                "business_processes": [],
                "error_handling_strategy": {},
                "interface_contracts": [],
                "integration_patterns": [],
                "security_contracts": {}
            }

    def _extract_api_endpoints(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Extract API endpoint information"""
        endpoints = []
        
        for func in functions:
            endpoint_info = self._analyze_api_function(func)
            if endpoint_info:
                endpoints.append(endpoint_info)
        
        # Also check methods in classes (for class-based views)
        for cls in classes:
            methods = cls.get('methods', [])
            for method in methods:
                endpoint_info = self._analyze_api_function(method, cls)
                if endpoint_info:
                    endpoints.append(endpoint_info)
        
        return endpoints

    def _analyze_api_function(self, func: Dict, parent_class: Optional[Dict] = None) -> Optional[Dict]:
        """Analyze function for API endpoint patterns"""
        func_name = func.get('name', '')
        decorators = func.get('decorators', [])
        parameters = func.get('parameters', [])
        calls = func.get('calls', [])
        
        # Check for API decorators
        http_methods = []
        endpoint_path = None
        
        for decorator in decorators:
            # FastAPI patterns
            fastapi_match = re.search(r'app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', decorator)
            if fastapi_match:
                http_methods.append(fastapi_match.group(1).upper())
                endpoint_path = fastapi_match.group(2)
                break
            
            # Flask patterns
            flask_match = re.search(r'route\(["\']([^"\']+)["\'].*methods=\[([^\]]+)\]', decorator)
            if flask_match:
                endpoint_path = flask_match.group(1)
                methods_str = flask_match.group(2)
                http_methods.extend([m.strip().strip('"\'') for m in methods_str.split(',')])
                break
            
            # Simple method detection
            for method in self.http_methods:
                if method in decorator.lower():
                    http_methods.append(method.upper())
        
        if not http_methods:
            return None
        
        # Infer endpoint path if not found
        if not endpoint_path:
            endpoint_path = self._infer_endpoint_path(func_name, parent_class)
        
        # Analyze endpoint semantics
        endpoint = {
            "path": endpoint_path,
            "methods": http_methods,
            "handler_function": func_name,
            "purpose": self._infer_endpoint_purpose(func_name, http_methods[0] if http_methods else 'GET'),
            "input_semantics": self._analyze_input_semantics(parameters, calls),
            "output_semantics": self._analyze_output_semantics(func, calls),
            "side_effects": self._identify_side_effects(calls),
            "business_capability": self._map_to_business_capability(func_name, calls),
            "authentication_required": self._check_authentication_required(decorators, calls),
            "authorization_rules": self._extract_authorization_rules(decorators, calls),
            "rate_limiting": self._check_rate_limiting(decorators),
            "caching_strategy": self._identify_caching_strategy(decorators, calls),
            "validation_rules": self._extract_validation_rules(parameters, calls)
        }
        
        return endpoint

    def _extract_data_contracts(self, classes: List[Dict]) -> List[Dict]:
        """Extract data contracts and models"""
        contracts = []
        
        for cls in classes:
            contract_info = self._analyze_data_model(cls)
            if contract_info:
                contracts.append(contract_info)
        
        return contracts

    def _analyze_data_model(self, cls: Dict) -> Optional[Dict]:
        """Analyze class for data model patterns"""
        class_name = cls.get('name', '')
        base_classes = cls.get('base_classes', [])
        methods = cls.get('methods', [])
        attributes = cls.get('attributes', [])
        decorators = cls.get('decorators', [])
        
        # Check if it's a data model
        model_type = self._identify_model_type(class_name, base_classes, decorators)
        if not model_type:
            return None
        
        # Extract field information
        fields = self._extract_model_fields(attributes, methods, model_type)
        
        # Extract validation rules
        validation_rules = self._extract_model_validation_rules(methods, model_type)
        
        # Extract relationships
        relationships = self._extract_model_relationships(attributes, methods, model_type)
        
        # Determine usage context
        usage_context = self._determine_usage_context(class_name, methods)
        
        contract = {
            "name": class_name,
            "type": model_type,
            "purpose": self._infer_model_purpose(class_name, model_type),
            "fields": fields,
            "validation_rules": validation_rules,
            "relationships": relationships,
            "usage_context": usage_context,
            "serialization_rules": self._extract_serialization_rules(methods),
            "business_rules": self._extract_business_rules_from_model(methods),
            "lifecycle_events": self._extract_model_lifecycle_events(methods)
        }
        
        return contract

    def _extract_business_processes(self, functions: List[Dict], api_endpoints: List[Dict]) -> List[Dict]:
        """Extract business processes from functions and endpoints"""
        processes = []
        
        # Group related functions into processes
        process_groups = self._group_functions_into_processes(functions)
        
        for process_name, process_functions in process_groups.items():
            process = {
                "process": process_name,
                "trigger": self._identify_process_trigger(process_functions, api_endpoints),
                "steps": self._extract_process_steps(process_functions),
                "outcomes": self._identify_process_outcomes(process_functions),
                "data_transformations": self._trace_data_transformations(process_functions),
                "error_scenarios": self._identify_error_scenarios(process_functions),
                "performance_characteristics": self._analyze_performance_characteristics(process_functions),
                "dependencies": self._identify_process_dependencies(process_functions)
            }
            processes.append(process)
        
        return processes

    def _extract_error_handling_strategy(self, functions: List[Dict], classes: List[Dict]) -> Dict:
        """Extract comprehensive error handling strategy"""
        strategy = {
            "validation_errors": {"handling": [], "recovery": [], "logging": []},
            "business_errors": {"handling": [], "recovery": [], "logging": []},
            "system_errors": {"handling": [], "recovery": [], "logging": []},
            "error_propagation_patterns": [],
            "error_response_formats": [],
            "error_monitoring": []
        }
        
        # Analyze error handling in functions
        for func in functions:
            error_info = func.get('error_handling', {})
            if error_info:
                self._categorize_error_handling(error_info, strategy)
        
        # Analyze error classes
        error_classes = [cls for cls in classes if 'error' in cls.get('name', '').lower() or 'exception' in cls.get('name', '').lower()]
        for error_cls in error_classes:
            strategy['error_response_formats'].append({
                "error_type": error_cls.get('name', ''),
                "structure": self._analyze_error_class_structure(error_cls)
            })
        
        return strategy

    def _extract_interface_contracts(self, classes: List[Dict]) -> List[Dict]:
        """Extract interface contracts"""
        interfaces = []
        
        for cls in classes:
            if self._is_interface_class(cls):
                interface = {
                    "name": cls.get('name', ''),
                    "type": "interface",
                    "purpose": self._infer_interface_purpose(cls),
                    "methods": self._extract_interface_methods(cls),
                    "contracts": self._extract_interface_contracts_details(cls),
                    "implementations": self._find_interface_implementations(cls, classes)
                }
                interfaces.append(interface)
        
        return interfaces

    def _identify_integration_patterns(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Identify integration patterns"""
        patterns = []
        
        # Check for external service calls
        external_calls = []
        for func in functions:
            calls = func.get('calls', [])
            for call in calls:
                if any(pattern in call.lower() for pattern in ['http', 'request', 'client', 'api']):
                    external_calls.append(call)
        
        if external_calls:
            patterns.append({
                "pattern": "External Service Integration",
                "type": "integration",
                "evidence": external_calls[:5],  # First 5 examples
                "description": "Integration with external services via HTTP calls"
            })
        
        # Check for message queue patterns
        message_patterns = []
        for func in functions:
            calls = func.get('calls', [])
            for call in calls:
                if any(pattern in call.lower() for pattern in ['queue', 'publish', 'subscribe', 'message']):
                    message_patterns.append(call)
        
        if message_patterns:
            patterns.append({
                "pattern": "Message Queue Integration",
                "type": "integration",
                "evidence": message_patterns[:5],
                "description": "Asynchronous message processing integration"
            })
        
        return patterns

    def _extract_security_contracts(self, functions: List[Dict], classes: List[Dict]) -> Dict:
        """Extract security contracts and patterns"""
        security = {
            "authentication_patterns": [],
            "authorization_patterns": [],
            "input_validation_patterns": [],
            "security_headers": [],
            "encryption_patterns": [],
            "audit_patterns": []
        }
        
        # Analyze functions for security patterns
        for func in functions:
            decorators = func.get('decorators', [])
            calls = func.get('calls', [])
            
            # Check for authentication decorators
            for decorator in decorators:
                if any(pattern in decorator.lower() for pattern in ['auth', 'login', 'token']):
                    security['authentication_patterns'].append(decorator)
            
            # Check for authorization calls
            for call in calls:
                if any(pattern in call.lower() for pattern in ['authorize', 'permission', 'role', 'access']):
                    security['authorization_patterns'].append(call)
                elif any(pattern in call.lower() for pattern in ['validate', 'sanitize', 'escape']):
                    security['input_validation_patterns'].append(call)
                elif any(pattern in call.lower() for pattern in ['encrypt', 'decrypt', 'hash', 'sign']):
                    security['encryption_patterns'].append(call)
                elif any(pattern in call.lower() for pattern in ['log', 'audit', 'track']):
                    security['audit_patterns'].append(call)
        
        return security

    # Helper methods
    def _infer_endpoint_path(self, func_name: str, parent_class: Optional[Dict] = None) -> str:
        """Infer endpoint path from function name"""
        # Convert function name to path
        path = func_name.replace('_', '-')
        
        # Add class prefix if applicable
        if parent_class:
            class_name = parent_class.get('name', '').lower()
            if 'controller' in class_name:
                class_name = class_name.replace('controller', '')
            path = f"/{class_name}/{path}"
        else:
            path = f"/{path}"
        
        return path

    def _infer_endpoint_purpose(self, func_name: str, http_method: str) -> str:
        """Infer the purpose of an API endpoint"""
        func_lower = func_name.lower()
        
        if http_method == 'GET':
            if 'list' in func_lower or 'all' in func_lower:
                return "List resources"
            elif 'get' in func_lower or 'find' in func_lower:
                return "Retrieve specific resource"
            else:
                return "Query operation"
        elif http_method == 'POST':
            if 'create' in func_lower:
                return "Create new resource"
            else:
                return "Process operation"
        elif http_method == 'PUT':
            return "Update resource completely"
        elif http_method == 'PATCH':
            return "Update resource partially"
        elif http_method == 'DELETE':
            return "Delete resource"
        else:
            return "Custom operation"

    def _analyze_input_semantics(self, parameters: List[Dict], calls: List[str]) -> Dict:
        """Analyze input semantics for endpoint"""
        input_semantics = {
            "required": [],
            "optional": [],
            "validation_rules": [],
            "data_types": {}
        }
        
        for param in parameters:
            param_name = param.get('name', '')
            param_type = param.get('type', '')
            
            if param_name not in ['self', 'cls']:
                if param.get('default') is None:
                    input_semantics['required'].append(param_name)
                else:
                    input_semantics['optional'].append(param_name)
                
                if param_type:
                    input_semantics['data_types'][param_name] = param_type
        
        # Extract validation rules from calls
        for call in calls:
            if 'validate' in call.lower():
                input_semantics['validation_rules'].append(f"Validation: {call}")
        
        return input_semantics

    def _analyze_output_semantics(self, func: Dict, calls: List[str]) -> Dict:
        """Analyze output semantics for endpoint"""
        output_semantics = {
            "success_type": func.get('return_type', 'Unknown'),
            "error_types": [],
            "status_codes": [],
            "response_format": "JSON"
        }
        
        # Analyze calls for response patterns
        for call in calls:
            if 'exception' in call.lower() or 'error' in call.lower():
                output_semantics['error_types'].append(call)
            elif any(code in call for code in ['200', '201', '400', '401', '404', '500']):
                # Extract status codes
                status_match = re.search(r'(\d{3})', call)
                if status_match:
                    output_semantics['status_codes'].append(status_match.group(1))
        
        return output_semantics

    def _identify_side_effects(self, calls: List[str]) -> List[str]:
        """Identify side effects from function calls"""
        side_effects = []
        
        for call in calls:
            call_lower = call.lower()
            if any(word in call_lower for word in ['save', 'create', 'update', 'delete']):
                side_effects.append(f"Data modification: {call}")
            elif any(word in call_lower for word in ['send', 'notify', 'email', 'publish']):
                side_effects.append(f"External communication: {call}")
            elif any(word in call_lower for word in ['log', 'track', 'audit']):
                side_effects.append(f"Logging/auditing: {call}")
            elif any(word in call_lower for word in ['cache', 'store', 'session']):
                side_effects.append(f"State modification: {call}")
        
        return side_effects

    def _map_to_business_capability(self, func_name: str, calls: List[str]) -> str:
        """Map function to business capability"""
        func_lower = func_name.lower()
        
        # Check function name patterns
        for capability, operations in self.business_operations.items():
            if any(op in func_lower for op in operations):
                return capability.title()
        
        # Check function calls
        for call in calls:
            call_lower = call.lower()
            for capability, operations in self.business_operations.items():
                if any(op in call_lower for op in operations):
                    return capability.title()
        
        return "General"

    def _check_authentication_required(self, decorators: List[str], calls: List[str]) -> bool:
        """Check if endpoint requires authentication"""
        # Check decorators
        for decorator in decorators:
            if any(pattern in decorator.lower() for pattern in ['auth', 'login', 'token', 'jwt']):
                return True
        
        # Check function calls
        for call in calls:
            if any(pattern in call.lower() for pattern in ['authenticate', 'check_auth', 'verify_token']):
                return True
        
        return False

    def _extract_authorization_rules(self, decorators: List[str], calls: List[str]) -> List[str]:
        """Extract authorization rules"""
        rules = []
        
        # Check decorators for authorization
        for decorator in decorators:
            if any(pattern in decorator.lower() for pattern in ['role', 'permission', 'admin', 'authorize']):
                rules.append(f"Decorator: {decorator}")
        
        # Check function calls
        for call in calls:
            if any(pattern in call.lower() for pattern in ['authorize', 'check_permission', 'require_role']):
                rules.append(f"Runtime check: {call}")
        
        return rules

    def _check_rate_limiting(self, decorators: List[str]) -> Optional[str]:
        """Check for rate limiting"""
        for decorator in decorators:
            if any(pattern in decorator.lower() for pattern in ['rate_limit', 'throttle', 'limit']):
                return decorator
        return None

    def _identify_caching_strategy(self, decorators: List[str], calls: List[str]) -> Optional[str]:
        """Identify caching strategy"""
        # Check decorators
        for decorator in decorators:
            if 'cache' in decorator.lower():
                return f"Decorator caching: {decorator}"
        
        # Check function calls
        for call in calls:
            if 'cache' in call.lower():
                return f"Manual caching: {call}"
        
        return None

    def _extract_validation_rules(self, parameters: List[Dict], calls: List[str]) -> List[str]:
        """Extract validation rules"""
        rules = []
        
        # Check parameter types for validation
        for param in parameters:
            param_type = param.get('type', '')
            if param_type:
                rules.append(f"Type validation: {param.get('name', 'unknown')} must be {param_type}")
        
        # Check function calls for validation
        for call in calls:
            if 'validate' in call.lower():
                rules.append(f"Custom validation: {call}")
        
        return rules

    def _identify_model_type(self, class_name: str, base_classes: List[str], decorators: List[str]) -> Optional[str]:
        """Identify the type of data model"""
        # Check for Pydantic models
        if any('basemodel' in base.lower() for base in base_classes):
            return 'pydantic'
        
        # Check for SQLAlchemy models
        if any(pattern in ' '.join(base_classes).lower() for pattern in ['base', 'model', 'db.model']):
            return 'sqlalchemy'
        
        # Check for dataclass
        if any('@dataclass' in decorator for decorator in decorators):
            return 'dataclass'
        
        # Check for enum
        if any('enum' in base.lower() for base in base_classes):
            return 'enum'
        
        # Check by naming convention
        if any(suffix in class_name.lower() for suffix in ['model', 'entity', 'schema', 'dto']):
            return 'data_model'
        
        return None

    def _extract_model_fields(self, attributes: List[Dict], methods: List[Dict], model_type: str) -> List[Dict]:
        """Extract fields from data model"""
        fields = []
        
        # Extract from attributes
        for attr in attributes:
            field_info = {
                "name": attr.get('name', ''),
                "type": attr.get('type', 'Unknown'),
                "required": True,  # Default assumption
                "validation": [],
                "description": None
            }
            fields.append(field_info)
        
        # For Pydantic models, look for Field definitions
        if model_type == 'pydantic':
            for method in methods:
                if 'validator' in method.get('name', ''):
                    # This is a validator method
                    field_name = method.get('name', '').replace('validate_', '')
                    for field in fields:
                        if field['name'] == field_name:
                            field['validation'].append(f"Custom validator: {method.get('name', '')}")
        
        return fields

    def _extract_model_validation_rules(self, methods: List[Dict], model_type: str) -> List[str]:
        """Extract validation rules from model"""
        rules = []
        
        for method in methods:
            method_name = method.get('name', '')
            if 'validate' in method_name:
                rules.append(f"Validation method: {method_name}")
            elif method_name == '__post_init__' and model_type == 'dataclass':
                rules.append("Post-initialization validation")
        
        return rules

    def _extract_model_relationships(self, attributes: List[Dict], methods: List[Dict], model_type: str) -> List[Dict]:
        """Extract relationships from model"""
        relationships = []
        
        for attr in attributes:
            attr_type = attr.get('type', '').lower()
            if any(pattern in attr_type for pattern in ['foreignkey', 'relationship', 'reference']):
                relationships.append({
                    "field": attr.get('name', ''),
                    "type": "relationship",
                    "target": self._extract_relationship_target(attr_type),
                    "cardinality": self._infer_cardinality(attr_type)
                })
        
        return relationships

    def _determine_usage_context(self, class_name: str, methods: List[Dict]) -> List[str]:
        """Determine usage context of the model"""
        contexts = []
        
        # Check class name for context clues
        class_lower = class_name.lower()
        if 'request' in class_lower:
            contexts.append('API Request')
        elif 'response' in class_lower:
            contexts.append('API Response')
        elif 'create' in class_lower:
            contexts.append('Creation')
        elif 'update' in class_lower:
            contexts.append('Update')
        elif 'entity' in class_lower or 'model' in class_lower:
            contexts.append('Data Persistence')
        
        return contexts

    def _extract_serialization_rules(self, methods: List[Dict]) -> List[str]:
        """Extract serialization rules"""
        rules = []
        
        for method in methods:
            method_name = method.get('name', '')
            if any(pattern in method_name for pattern in ['serialize', 'to_dict', 'to_json', 'model_dump']):
                rules.append(f"Serialization method: {method_name}")
        
        return rules

    def _extract_business_rules_from_model(self, methods: List[Dict]) -> List[str]:
        """Extract business rules from model methods"""
        rules = []
        
        for method in methods:
            method_name = method.get('name', '')
            if not method_name.startswith('_') and 'validate' not in method_name:
                # Public business methods
                if method.get('business_logic'):
                    rules.extend(method['business_logic'])
        
        return rules

    def _extract_model_lifecycle_events(self, methods: List[Dict]) -> List[str]:
        """Extract model lifecycle events"""
        events = []
        
        for method in methods:
            method_name = method.get('name', '')
            if method_name in ['__init__', '__post_init__']:
                events.append('CREATED')
            elif 'update' in method_name:
                events.append('UPDATED')
            elif 'delete' in method_name or 'remove' in method_name:
                events.append('DELETED')
            elif 'validate' in method_name:
                events.append('VALIDATED')
        
        return list(set(events))

    def _group_functions_into_processes(self, functions: List[Dict]) -> Dict[str, List[Dict]]:
        """Group related functions into business processes"""
        processes = {}
        
        for func in functions:
            func_name = func.get('name', '').lower()
            
            # Determine process category
            process_category = None
            for category, operations in self.business_operations.items():
                if any(op in func_name for op in operations):
                    process_category = category
                    break
            
            if not process_category:
                process_category = 'general'
            
            if process_category not in processes:
                processes[process_category] = []
            
            processes[process_category].append(func)
        
        return processes

    def _identify_process_trigger(self, process_functions: List[Dict], api_endpoints: List[Dict]) -> str:
        """Identify what triggers the process"""
        # Check if any function is an API endpoint
        func_names = [f.get('name', '') for f in process_functions]
        
        for endpoint in api_endpoints:
            if endpoint.get('handler_function') in func_names:
                return f"API call to {endpoint.get('path', 'unknown')}"
        
        # Check for event patterns
        for func in process_functions:
            func_name = func.get('name', '').lower()
            if 'handle' in func_name or 'process' in func_name:
                return f"Event handler: {func.get('name', 'unknown')}"
        
        return "Manual trigger"

    def _extract_process_steps(self, process_functions: List[Dict]) -> List[Dict]:
        """Extract steps in the business process"""
        steps = []
        
        for func in process_functions:
            step = {
                "step": func.get('semantic_purpose', func.get('name', 'Unknown')),
                "component": func.get('name', 'Unknown'),
                "business_rules": func.get('business_logic', []),
                "data_transformations": self._extract_function_transformations(func),
                "dependencies": func.get('dependencies', [])
            }
            steps.append(step)
        
        return steps

    def _identify_process_outcomes(self, process_functions: List[Dict]) -> List[str]:
        """Identify possible outcomes of the process"""
        outcomes = set()
        
        for func in process_functions:
            # Check return type
            return_type = func.get('return_type')
            if return_type:
                outcomes.add(f"Returns {return_type}")
            
            # Check for error handling
            error_handling = func.get('error_handling', {})
            if error_handling.get('exception_types'):
                for exc_type in error_handling['exception_types']:
                    outcomes.add(f"Error: {exc_type}")
            
            # Check side effects
            side_effects = func.get('side_effects', [])
            for effect in side_effects:
                outcomes.add(effect)
        
        return list(outcomes)

    def _trace_data_transformations(self, process_functions: List[Dict]) -> List[str]:
        """Trace data transformations in the process"""
        transformations = []
        
        for func in process_functions:
            data_flow = func.get('data_flow', {})
            if data_flow.get('transformations'):
                transformations.extend(data_flow['transformations'])
        
        return transformations

    def _identify_error_scenarios(self, process_functions: List[Dict]) -> List[str]:
        """Identify error scenarios in the process"""
        scenarios = []
        
        for func in process_functions:
            error_handling = func.get('error_handling', {})
            if error_handling.get('exception_types'):
                scenarios.extend(error_handling['exception_types'])
        
        return list(set(scenarios))

    def _analyze_performance_characteristics(self, process_functions: List[Dict]) -> Dict:
        """Analyze performance characteristics of the process"""
        characteristics = {
            "async_operations": 0,
            "database_calls": 0,
            "external_calls": 0,
            "complexity_score": 0
        }
        
        for func in process_functions:
            if func.get('is_async'):
                characteristics['async_operations'] += 1
            
            calls = func.get('calls', [])
            for call in calls:
                if any(pattern in call.lower() for pattern in ['db', 'database', 'session']):
                    characteristics['database_calls'] += 1
                elif any(pattern in call.lower() for pattern in ['http', 'request', 'client']):
                    characteristics['external_calls'] += 1
            
            complexity = func.get('semantic_complexity', {})
            characteristics['complexity_score'] += complexity.get('business_rules', 0)
        
        return characteristics

    def _identify_process_dependencies(self, process_functions: List[Dict]) -> List[str]:
        """Identify dependencies of the process"""
        dependencies = set()
        
        for func in process_functions:
            func_dependencies = func.get('dependencies', [])
            for dep in func_dependencies:
                dependencies.add(dep.get('dependency', dep) if isinstance(dep, dict) else dep)
        
        return list(dependencies)

    def _categorize_error_handling(self, error_info: Dict, strategy: Dict):
        """Categorize error handling information"""
        exception_types = error_info.get('exception_types', [])
        
        for exc_type in exception_types:
            if any(pattern in exc_type.lower() for pattern in ['validation', 'value', 'type']):
                strategy['validation_errors']['handling'].append(exc_type)
            elif any(pattern in exc_type.lower() for pattern in ['business', 'domain', 'application']):
                strategy['business_errors']['handling'].append(exc_type)
            else:
                strategy['system_errors']['handling'].append(exc_type)

    def _analyze_error_class_structure(self, error_cls: Dict) -> Dict:
        """Analyze structure of error class"""
        return {
            "base_classes": error_cls.get('base_classes', []),
            "attributes": [attr.get('name', '') for attr in error_cls.get('attributes', [])],
            "methods": [method.get('name', '') for method in error_cls.get('methods', [])]
        }

    def _is_interface_class(self, cls: Dict) -> bool:
        """Check if class is an interface"""
        base_classes = cls.get('base_classes', [])
        return any(pattern in ' '.join(base_classes).lower() for pattern in ['abc', 'abstract', 'interface', 'protocol'])

    def _infer_interface_purpose(self, cls: Dict) -> str:
        """Infer the purpose of an interface"""
        class_name = cls.get('name', '').lower()
        
        if 'repository' in class_name:
            return "Data access contract"
        elif 'service' in class_name:
            return "Business service contract"
        elif 'handler' in class_name:
            return "Event handling contract"
        else:
            return "Generic interface contract"

    def _extract_interface_methods(self, cls: Dict) -> List[Dict]:
        """Extract methods from interface"""
        methods = []
        
        for method in cls.get('methods', []):
            if not method.get('name', '').startswith('_'):
                method_info = {
                    "name": method.get('name', ''),
                    "parameters": method.get('parameters', []),
                    "return_type": method.get('return_type'),
                    "purpose": method.get('semantic_purpose', 'Unknown')
                }
                methods.append(method_info)
        
        return methods

    def _extract_interface_contracts_details(self, cls: Dict) -> List[str]:
        """Extract contract details from interface"""
        contracts = []
        
        # Check docstring for contract details
        docstring = cls.get('docstring', '')
        if docstring:
            contracts.append(f"Documentation contract: {docstring[:100]}...")
        
        # Check method signatures for contracts
        methods = cls.get('methods', [])
        for method in methods:
            if method.get('return_type'):
                contracts.append(f"{method.get('name', 'unknown')} must return {method.get('return_type')}")
        
        return contracts

    def _find_interface_implementations(self, interface_cls: Dict, all_classes: List[Dict]) -> List[str]:
        """Find implementations of an interface"""
        implementations = []
        interface_name = interface_cls.get('name', '')
        
        for cls in all_classes:
            base_classes = cls.get('base_classes', [])
            if interface_name in base_classes:
                implementations.append(cls.get('name', ''))
        
        return implementations

    def _extract_relationship_target(self, attr_type: str) -> str:
        """Extract relationship target from attribute type"""
        # Simple pattern matching for relationship targets
        match = re.search(r'(\w+)', attr_type)
        return match.group(1) if match else 'Unknown'

    def _infer_cardinality(self, attr_type: str) -> str:
        """Infer relationship cardinality"""
        if 'list' in attr_type.lower() or 'many' in attr_type.lower():
            return 'one-to-many'
        else:
            return 'one-to-one'

    def _extract_function_transformations(self, func: Dict) -> List[str]:
        """Extract data transformations from function"""
        transformations = []
        
        data_flow = func.get('data_flow', {})
        if isinstance(data_flow, dict) and 'transformations' in data_flow:
            transformations.extend(data_flow['transformations'])
        elif isinstance(data_flow, str):
            transformations.append(data_flow)
        
        return transformations

    def _infer_model_purpose(self, class_name: str, model_type: str) -> str:
        """Infer the purpose of a data model"""
        class_lower = class_name.lower()
        
        if 'request' in class_lower:
            return "API request data structure"
        elif 'response' in class_lower:
            return "API response data structure"
        elif 'create' in class_lower:
            return "Data creation schema"
        elif 'update' in class_lower:
            return "Data update schema"
        elif model_type == 'sqlalchemy':
            return "Database entity model"
        elif model_type == 'pydantic':
            return "Data validation schema"
        else:
            return "Data structure definition"
