"""
Semantic Code Understanding Tool
Extracts business domain concepts, rules, and workflows from code
"""

import ast
import re
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class BusinessRule:
    rule: str
    implementation: str
    complexity: str
    dependencies: List[str]

@dataclass
class WorkflowStep:
    name: str
    steps: List[str]
    data_flow: str
    exception_handling: str

@dataclass
class BusinessCapability:
    capability: str
    purpose: str
    implementing_components: List[str]
    business_rules: List[BusinessRule]
    workflows: List[WorkflowStep]

class SemanticCodeAnalyzer:
    """Understands what the code actually DOES business-wise"""
    
    def __init__(self):
        self.business_keywords = {
            'user': ['register', 'login', 'authenticate', 'profile', 'account'],
            'payment': ['pay', 'charge', 'transaction', 'billing', 'invoice'],
            'booking': ['reserve', 'book', 'schedule', 'appointment', 'availability'],
            'inventory': ['stock', 'product', 'item', 'catalog', 'warehouse'],
            'order': ['purchase', 'cart', 'checkout', 'fulfillment', 'shipping'],
            'notification': ['email', 'sms', 'alert', 'message', 'notify'],
            'security': ['auth', 'permission', 'role', 'access', 'token'],
            'analytics': ['track', 'log', 'metric', 'report', 'analytics']
        }
        
        self.validation_patterns = [
            r'validate_\w+',
            r'check_\w+',
            r'verify_\w+',
            r'is_valid_\w+',
            r'\w+_validator'
        ]
        
        self.workflow_patterns = [
            r'process_\w+',
            r'handle_\w+',
            r'execute_\w+',
            r'\w+_workflow',
            r'\w+_pipeline'
        ]

    def extract_business_domain(self, code_analysis: Dict) -> Dict:
        """Extracts business domain concepts from code analysis"""
        logger.info("Extracting business domain concepts...")
        
        try:
            functions = code_analysis.get('functions', [])
            classes = code_analysis.get('classes', [])
            
            # Extract business capabilities
            capabilities = self._identify_business_capabilities(functions, classes)
            
            # Extract domain models
            domain_models = self._extract_domain_models(classes)
            
            # Extract service boundaries
            service_boundaries = self._identify_service_boundaries(functions, classes)
            
            return {
                "business_capabilities": capabilities,
                "domain_models": domain_models,
                "service_boundaries": service_boundaries
            }
            
        except Exception as e:
            logger.error(f"Error extracting business domain: {e}")
            return {
                "business_capabilities": [],
                "domain_models": {"entities": [], "aggregates": []},
                "service_boundaries": []
            }

    def _identify_business_capabilities(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Identify business capabilities from functions and classes"""
        capabilities = {}
        
        # Analyze functions for business capabilities
        for func in functions:
            func_name = func.get('name', '').lower()
            file_path = func.get('file_path', '')
            
            # Determine business domain
            domain = self._classify_business_domain(func_name, file_path)
            if not domain:
                continue
                
            if domain not in capabilities:
                capabilities[domain] = {
                    'functions': [],
                    'classes': [],
                    'business_rules': [],
                    'workflows': []
                }
            
            capabilities[domain]['functions'].append(func)
            
            # Extract business rules from function
            rules = self._extract_business_rules_from_function(func)
            capabilities[domain]['business_rules'].extend(rules)
            
            # Extract workflows
            workflows = self._extract_workflows_from_function(func)
            capabilities[domain]['workflows'].extend(workflows)
        
        # Analyze classes for business capabilities
        for cls in classes:
            cls_name = cls.get('name', '').lower()
            file_path = cls.get('file_path', '')
            
            domain = self._classify_business_domain(cls_name, file_path)
            if not domain:
                continue
                
            if domain not in capabilities:
                capabilities[domain] = {
                    'functions': [],
                    'classes': [],
                    'business_rules': [],
                    'workflows': []
                }
            
            capabilities[domain]['classes'].append(cls)
        
        # Convert to structured format
        result = []
        for domain, data in capabilities.items():
            capability = {
                "capability": self._format_capability_name(domain),
                "purpose": self._infer_capability_purpose(domain, data),
                "implementing_components": self._extract_component_names(data),
                "business_rules": data['business_rules'],
                "workflows": data['workflows']
            }
            result.append(capability)
        
        return result

    def _classify_business_domain(self, name: str, file_path: str) -> Optional[str]:
        """Classify a function or class into business domain"""
        # Check file path first
        file_path_lower = file_path.lower()
        for domain in self.business_keywords:
            if domain in file_path_lower:
                return domain
        
        # Check name against business keywords
        name_lower = name.lower()
        for domain, keywords in self.business_keywords.items():
            for keyword in keywords:
                if keyword in name_lower:
                    return domain
        
        return None

    def _extract_business_rules_from_function(self, func: Dict) -> List[Dict]:
        """Extract business rules from function analysis"""
        rules = []
        func_name = func.get('name', '')
        docstring = func.get('docstring', '')
        
        # Check if function is a validation function
        for pattern in self.validation_patterns:
            if re.match(pattern, func_name, re.IGNORECASE):
                rule = {
                    "rule": self._infer_rule_from_function_name(func_name),
                    "implementation": f"{func_name}()",
                    "complexity": self._assess_complexity(func.get('complexity', 1)),
                    "dependencies": self._extract_dependencies_from_calls(func.get('calls', []))
                }
                rules.append(rule)
        
        # Extract rules from docstring
        if docstring:
            docstring_rules = self._extract_rules_from_docstring(docstring, func_name)
            rules.extend(docstring_rules)
        
        return rules

    def _extract_workflows_from_function(self, func: Dict) -> List[Dict]:
        """Extract workflows from function analysis"""
        workflows = []
        func_name = func.get('name', '')
        
        # Check if function represents a workflow
        for pattern in self.workflow_patterns:
            if re.match(pattern, func_name, re.IGNORECASE):
                workflow = {
                    "name": self._format_workflow_name(func_name),
                    "steps": self._infer_workflow_steps(func),
                    "data_flow": self._infer_data_flow(func),
                    "exception_handling": self._infer_exception_handling(func)
                }
                workflows.append(workflow)
        
        return workflows

    def _extract_domain_models(self, classes: List[Dict]) -> Dict:
        """Extract domain models from class analysis"""
        entities = []
        aggregates = []
        
        for cls in classes:
            cls_name = cls.get('name', '')
            base_classes = cls.get('base_classes', [])
            methods = cls.get('methods', [])
            attributes = cls.get('attributes', [])
            
            # Check if it's a domain entity
            if self._is_domain_entity(cls_name, base_classes, methods):
                entity = {
                    "name": cls_name,
                    "responsibility": self._infer_entity_responsibility(cls_name, methods),
                    "attributes": self._categorize_attributes(attributes),
                    "lifecycle_events": self._extract_lifecycle_events(methods),
                    "business_operations": self._extract_business_operations(methods)
                }
                entities.append(entity)
            
            # Check if it's an aggregate root
            if self._is_aggregate_root(cls_name, methods):
                aggregate = {
                    "name": f"{cls_name}Aggregate",
                    "root": cls_name,
                    "children": self._infer_aggregate_children(cls_name, methods),
                    "consistency_boundary": self._infer_consistency_boundary(cls_name)
                }
                aggregates.append(aggregate)
        
        return {
            "entities": entities,
            "aggregates": aggregates
        }

    def _identify_service_boundaries(self, functions: List[Dict], classes: List[Dict]) -> List[Dict]:
        """Identify service boundaries from code analysis"""
        services = {}
        
        # Group by service classes
        for cls in classes:
            cls_name = cls.get('name', '')
            if 'service' in cls_name.lower():
                methods = cls.get('methods', [])
                services[cls_name] = {
                    "class": cls,
                    "methods": methods,
                    "functions": []
                }
        
        # Group standalone functions by file/module
        for func in functions:
            file_path = func.get('file_path', '')
            if 'service' in file_path.lower():
                service_name = Path(file_path).stem.title() + "Service"
                if service_name not in services:
                    services[service_name] = {
                        "class": None,
                        "methods": [],
                        "functions": []
                    }
                services[service_name]['functions'].append(func)
        
        # Convert to structured format
        result = []
        for service_name, data in services.items():
            service = {
                "service": service_name,
                "responsibility": self._infer_service_responsibility(service_name, data),
                "public_interface": self._extract_public_interface(data),
                "internal_implementation": self._extract_internal_implementation(data),
                "data_ownership": self._infer_data_ownership(service_name, data)
            }
            result.append(service)
        
        return result

    # Helper methods
    def _format_capability_name(self, domain: str) -> str:
        """Format domain into capability name"""
        capability_names = {
            'user': 'User Registration and Management',
            'payment': 'Payment Processing',
            'booking': 'Booking and Reservation Management',
            'inventory': 'Inventory Management',
            'order': 'Order Management',
            'notification': 'Notification System',
            'security': 'Security and Authentication',
            'analytics': 'Analytics and Reporting'
        }
        return capability_names.get(domain, domain.title() + " Management")

    def _infer_capability_purpose(self, domain: str, data: Dict) -> str:
        """Infer the purpose of a business capability"""
        purposes = {
            'user': 'Handle user lifecycle from registration to deletion',
            'payment': 'Process payments and manage financial transactions',
            'booking': 'Manage reservations and availability',
            'inventory': 'Track and manage product inventory',
            'order': 'Handle order processing and fulfillment',
            'notification': 'Send notifications and alerts to users',
            'security': 'Manage authentication and authorization',
            'analytics': 'Collect and analyze system metrics'
        }
        return purposes.get(domain, f"Manage {domain} related operations")

    def _extract_component_names(self, data: Dict) -> List[str]:
        """Extract component names from capability data"""
        components = []
        
        for func in data.get('functions', []):
            file_path = func.get('file_path', '')
            component_name = Path(file_path).stem.title().replace('_', '')
            if component_name not in components:
                components.append(component_name)
        
        for cls in data.get('classes', []):
            cls_name = cls.get('name', '')
            if cls_name not in components:
                components.append(cls_name)
        
        return components

    def _infer_rule_from_function_name(self, func_name: str) -> str:
        """Infer business rule from function name"""
        if 'email' in func_name.lower():
            return "Email must be unique across system"
        elif 'password' in func_name.lower():
            return "Password must meet security requirements"
        elif 'validate' in func_name.lower():
            return f"Input validation rule for {func_name.replace('validate_', '')}"
        else:
            return f"Business rule enforced by {func_name}"

    def _assess_complexity(self, complexity: int) -> str:
        """Assess complexity level"""
        if complexity <= 3:
            return "Low"
        elif complexity <= 7:
            return "Medium"
        else:
            return "High"

    def _extract_dependencies_from_calls(self, calls: List[str]) -> List[str]:
        """Extract dependencies from function calls"""
        dependencies = []
        for call in calls:
            if 'database' in call.lower() or 'db' in call.lower():
                dependencies.append("Database")
            elif 'service' in call.lower():
                dependencies.append("External Service")
            elif 'email' in call.lower():
                dependencies.append("Email Service")
        return list(set(dependencies))

    def _extract_rules_from_docstring(self, docstring: str, func_name: str) -> List[Dict]:
        """Extract business rules from docstring"""
        rules = []
        # Simple pattern matching for common rule patterns
        if 'must' in docstring.lower():
            rule = {
                "rule": "Business rule from docstring",
                "implementation": f"{func_name}()",
                "complexity": "Medium",
                "dependencies": []
            }
            rules.append(rule)
        return rules

    def _format_workflow_name(self, func_name: str) -> str:
        """Format function name into workflow name"""
        return func_name.replace('_', ' ').title()

    def _infer_workflow_steps(self, func: Dict) -> List[str]:
        """Infer workflow steps from function"""
        calls = func.get('calls', [])
        steps = []
        
        for call in calls:
            if 'validate' in call.lower():
                steps.append("Validate input")
            elif 'create' in call.lower():
                steps.append("Create record")
            elif 'send' in call.lower():
                steps.append("Send notification")
            elif 'log' in call.lower():
                steps.append("Log event")
        
        return steps or ["Process request", "Return response"]

    def _infer_data_flow(self, func: Dict) -> str:
        """Infer data flow from function"""
        parameters = func.get('parameters', [])
        return_type = func.get('return_type', '')
        
        input_types = [p.get('type', 'Unknown') for p in parameters if p.get('type')]
        
        if input_types and return_type:
            return f"{' → '.join(input_types)} → {return_type}"
        else:
            return "Input → Processing → Output"

    def _infer_exception_handling(self, func: Dict) -> str:
        """Infer exception handling from function"""
        # This would require more detailed AST analysis
        return "Standard error handling"

    def _is_domain_entity(self, cls_name: str, base_classes: List[str], methods: List[Dict]) -> bool:
        """Check if class is a domain entity"""
        # Check for common entity patterns
        entity_indicators = [
            'model' in cls_name.lower(),
            'entity' in cls_name.lower(),
            any('model' in base.lower() for base in base_classes),
            any('entity' in base.lower() for base in base_classes),
            len(methods) > 2  # Has business methods
        ]
        return any(entity_indicators)

    def _infer_entity_responsibility(self, cls_name: str, methods: List[Dict]) -> str:
        """Infer entity responsibility from class name and methods"""
        if 'user' in cls_name.lower():
            return "Represent system user with authentication and profile"
        elif 'hotel' in cls_name.lower():
            return "Represent hotel with rooms and bookings"
        elif 'booking' in cls_name.lower():
            return "Represent reservation with dates and guests"
        else:
            return f"Represent {cls_name.lower()} domain concept"

    def _categorize_attributes(self, attributes: List[Dict]) -> Dict[str, List[str]]:
        """Categorize attributes by type"""
        core = []
        profile = []
        metadata = []
        
        for attr in attributes:
            attr_name = attr.get('name', '').lower()
            if attr_name in ['id', 'email', 'password', 'status']:
                core.append(attr.get('name', ''))
            elif attr_name in ['created_at', 'updated_at', 'last_login']:
                metadata.append(attr.get('name', ''))
            else:
                profile.append(attr.get('name', ''))
        
        return {
            "core": core,
            "profile": profile,
            "metadata": metadata
        }

    def _extract_lifecycle_events(self, methods: List[Dict]) -> List[str]:
        """Extract lifecycle events from methods"""
        events = []
        for method in methods:
            method_name = method.get('name', '').lower()
            if 'create' in method_name:
                events.append("CREATED")
            elif 'verify' in method_name:
                events.append("VERIFIED")
            elif 'suspend' in method_name or 'deactivate' in method_name:
                events.append("SUSPENDED")
            elif 'delete' in method_name:
                events.append("DELETED")
        
        return list(set(events))

    def _extract_business_operations(self, methods: List[Dict]) -> List[str]:
        """Extract business operations from methods"""
        operations = []
        for method in methods:
            method_name = method.get('name', '')
            if not method_name.startswith('_'):  # Public methods
                operations.append(method_name)
        
        return operations

    def _is_aggregate_root(self, cls_name: str, methods: List[Dict]) -> bool:
        """Check if class is an aggregate root"""
        # Simple heuristic: has methods that manage other entities
        method_names = [m.get('name', '').lower() for m in methods]
        aggregate_indicators = [
            any('manage' in name for name in method_names),
            any('add' in name for name in method_names),
            any('remove' in name for name in method_names),
            len(methods) > 5  # Complex entity with many operations
        ]
        return any(aggregate_indicators)

    def _infer_aggregate_children(self, cls_name: str, methods: List[Dict]) -> List[str]:
        """Infer aggregate children from class name and methods"""
        if 'user' in cls_name.lower():
            return ["UserProfile", "UserPreferences", "LoginHistory"]
        elif 'hotel' in cls_name.lower():
            return ["HotelRooms", "HotelAmenities", "HotelReviews"]
        else:
            return []

    def _infer_consistency_boundary(self, cls_name: str) -> str:
        """Infer consistency boundary for aggregate"""
        return f"{cls_name} and immediate related data"

    def _infer_service_responsibility(self, service_name: str, data: Dict) -> str:
        """Infer service responsibility"""
        if 'user' in service_name.lower():
            return "Handle all user-related operations"
        elif 'hotel' in service_name.lower():
            return "Manage hotel information and operations"
        elif 'booking' in service_name.lower():
            return "Process booking and reservation requests"
        else:
            return f"Handle {service_name.replace('Service', '').lower()} operations"

    def _extract_public_interface(self, data: Dict) -> List[str]:
        """Extract public interface methods"""
        interface = []
        
        # From class methods
        if data.get('class'):
            methods = data.get('methods', [])
            for method in methods:
                method_name = method.get('name', '')
                if not method_name.startswith('_'):  # Public method
                    parameters = method.get('parameters', [])
                    param_str = ', '.join([p.get('name', '') for p in parameters if p.get('name') != 'self'])
                    interface.append(f"{method_name}({param_str})")
        
        # From standalone functions
        for func in data.get('functions', []):
            func_name = func.get('name', '')
            if not func_name.startswith('_'):
                parameters = func.get('parameters', [])
                param_str = ', '.join([p.get('name', '') for p in parameters])
                interface.append(f"{func_name}({param_str})")
        
        return interface

    def _extract_internal_implementation(self, data: Dict) -> List[str]:
        """Extract internal implementation details"""
        implementation = []
        
        # Analyze function calls to infer internal dependencies
        all_calls = []
        if data.get('class'):
            for method in data.get('methods', []):
                all_calls.extend(method.get('calls', []))
        
        for func in data.get('functions', []):
            all_calls.extend(func.get('calls', []))
        
        # Categorize calls
        for call in all_calls:
            if 'repository' in call.lower():
                implementation.append("Repository for data access")
            elif 'service' in call.lower():
                implementation.append("External service integration")
            elif 'email' in call.lower():
                implementation.append("Email service for notifications")
        
        return list(set(implementation))

    def _infer_data_ownership(self, service_name: str, data: Dict) -> str:
        """Infer data ownership for service"""
        if 'user' in service_name.lower():
            return "Owns User, UserProfile, UserPreferences entities"
        elif 'hotel' in service_name.lower():
            return "Owns Hotel, Room entities"
        elif 'booking' in service_name.lower():
            return "Owns Booking, Reservation entities"
        else:
            return f"Owns {service_name.replace('Service', '')} related entities"
