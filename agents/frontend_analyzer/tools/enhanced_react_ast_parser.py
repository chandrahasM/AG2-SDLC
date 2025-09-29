"""
Enhanced React/TypeScript AST Parser for Frontend Analysis
Analyzes React components, services, hooks, and TypeScript interfaces
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
class ReactComponent:
    name: str
    file_path: str
    line_number: int
    props: List[Dict[str, Any]]
    state: List[Dict[str, Any]]
    hooks: List[Dict[str, Any]]
    lifecycle_methods: List[Dict[str, Any]]
    event_handlers: List[Dict[str, Any]]
    jsx_elements: List[Dict[str, Any]]
    imports: List[Dict[str, Any]]
    exports: List[Dict[str, Any]]
    complexity: int
    dependencies: List[str]

@dataclass
class ServiceClass:
    name: str
    file_path: str
    line_number: int
    methods: List[Dict[str, Any]]
    properties: List[Dict[str, Any]]
    is_exported: bool
    complexity: int

@dataclass
class TypeScriptInterface:
    name: str
    file_path: str
    line_number: int
    properties: List[Dict[str, Any]]
    methods: List[Dict[str, Any]]
    extends: List[str]
    generics: List[str]
    is_exported: bool

class EnhancedReactASTParser:
    """Enhanced parser for React/TypeScript files with service detection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # React component patterns - only detect actual React components
        self.component_patterns = {
            'function_component': r'function\s+(\w+)\s*\([^)]*\)\s*{',
            'arrow_component': r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
            'class_component': r'class\s+(\w+)\s+extends\s+React\.Component',
            'function_no_params': r'function\s+(\w+)\s*\(\s*\)\s*{'
        }
        
        # Service patterns - detect service classes and methods
        self.service_patterns = {
            'class_service': r'class\s+(\w+)\s*{',
            'service_method_async': r'(?:public|private|protected)?\s*async\s+(\w+)\s*\([^)]*\)\s*:\s*Promise<[^>]+>',
            'service_method_sync': r'(?:public|private|protected)?\s*(\w+)\s*\([^)]*\)\s*:\s*[^{]+{',
            'service_export': r'export\s+(?:const|let|var)\s+(\w+)\s*=',
            'service_instance_export': r'export\s+(?:const|let|var)\s+(\w+)\s*=\s*new\s+(\w+)'
        }
        
        # Hook patterns
        self.hook_patterns = {
            'useState': r'useState\s*\([^)]*\)',
            'useEffect': r'useEffect\s*\([^)]*\)',
            'useContext': r'useContext\s*\([^)]*\)',
            'useReducer': r'useReducer\s*\([^)]*\)',
            'useMemo': r'useMemo\s*\([^)]*\)',
            'useCallback': r'useCallback\s*\([^)]*\)',
            'custom_hook': r'use[A-Z]\w*'
        }
        
        # TypeScript patterns
        self.typescript_patterns = {
            'interface': r'interface\s+(\w+)\s*(?:extends\s+[\w,\s]+)?\s*{',
            'type_alias': r'type\s+(\w+)\s*=',
            'enum': r'enum\s+(\w+)\s*{',
            'generic': r'<[^>]+>',
            'property': r'(\w+)(?:\?)?\s*:\s*([^;]+)'
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single React/TypeScript file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use the full file path for better tracking
            full_path = str(Path(file_path).resolve())
            
            analysis = {
                'file_path': full_path,
                'file_type': self._detect_file_type(file_path),
                'components': self._extract_components(content, file_path),
                'services': self._extract_services(content, file_path),
                'interfaces': self._extract_interfaces(content, file_path),
                'hooks': self._extract_hooks(content, file_path),
                'imports': self._extract_imports(content),
                'exports': self._extract_exports(content),
                'dependencies': self._extract_dependencies(content),
                'complexity': self._calculate_complexity(content),
                'business_logic': self._extract_business_logic(content)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {e}")
            return {
                'file_path': file_path,
                'error': str(e)
            }
    
    def _detect_file_type(self, file_path: str) -> str:
        """Detect the type of file (component, hook, service, etc.)"""
        filename = Path(file_path).name.lower()
        
        if 'component' in filename or filename.endswith('.tsx'):
            return 'component'
        elif 'hook' in filename or filename.startswith('use'):
            return 'hook'
        elif 'service' in filename or 'api' in filename:
            return 'service'
        elif 'type' in filename or filename.endswith('.d.ts'):
            return 'types'
        elif 'test' in filename or 'spec' in filename:
            return 'test'
        else:
            return 'utility'
    
    def _extract_components(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract React components from content - only actual components"""
        components = []
        
        # Find function components
        for match in re.finditer(self.component_patterns['function_component'], content, re.MULTILINE):
            component_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            # Only include if it's a React component (has JSX or returns JSX)
            if self._is_react_component(content, match.start()):
                components.append({
                    'name': component_name,
                    'type': 'function',
                    'line_number': line_number,
                    'props': self._extract_props_from_function(content, match.start()),
                    'state': self._extract_state_from_function(content, match.start()),
                    'hooks': self._extract_hooks_from_function(content, match.start()),
                    'jsx_elements': self._extract_jsx_elements(content, match.start()),
                    'event_handlers': self._extract_event_handlers(content, match.start()),
                    'complexity': self._calculate_function_complexity(content, match.start())
                })
        
        # Find function components without parameters
        for match in re.finditer(self.component_patterns['function_no_params'], content, re.MULTILINE):
            component_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            if self._is_react_component(content, match.start()):
                components.append({
                    'name': component_name,
                    'type': 'function',
                    'line_number': line_number,
                    'props': self._extract_props_from_function(content, match.start()),
                    'state': self._extract_state_from_function(content, match.start()),
                    'hooks': self._extract_hooks_from_function(content, match.start()),
                    'jsx_elements': self._extract_jsx_elements(content, match.start()),
                    'event_handlers': self._extract_event_handlers(content, match.start()),
                    'complexity': self._calculate_function_complexity(content, match.start())
                })
        
        # Find arrow function components
        for match in re.finditer(self.component_patterns['arrow_component'], content, re.MULTILINE):
            component_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            if self._is_react_component(content, match.start()):
                components.append({
                    'name': component_name,
                    'type': 'arrow',
                    'line_number': line_number,
                    'props': self._extract_props_from_function(content, match.start()),
                    'state': self._extract_state_from_function(content, match.start()),
                    'hooks': self._extract_hooks_from_function(content, match.start()),
                    'jsx_elements': self._extract_jsx_elements(content, match.start()),
                    'event_handlers': self._extract_event_handlers(content, match.start()),
                    'complexity': self._calculate_function_complexity(content, match.start())
                })
        
        return components
    
    def _is_react_component(self, content: str, start_pos: int) -> bool:
        """Check if a function is actually a React component"""
        # Look for JSX in the function body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return False
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        function_body = content[brace_start:brace_end]
        
        # Check for JSX patterns
        jsx_patterns = [
            r'return\s*<',  # return <JSX>
            r'<\w+',        # <Component
            r'className=',  # className prop
            r'onClick=',    # onClick prop
            r'useState',    # React hooks
            r'useEffect'    # React hooks
        ]
        
        for pattern in jsx_patterns:
            if re.search(pattern, function_body):
                return True
        
        return False
    
    def _extract_services(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract service classes and methods from content"""
        services = []
        
        # Find service classes
        for match in re.finditer(self.service_patterns['class_service'], content, re.MULTILINE):
            service_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            services.append({
                'name': service_name,
                'type': 'class',
                'line_number': line_number,
                'methods': self._extract_service_methods(content, match.start()),
                'properties': self._extract_service_properties(content, match.start()),
                'is_exported': 'export' in content[max(0, match.start()-50):match.start()],
                'complexity': self._calculate_class_complexity(content, match.start())
            })
        
        # Find exported service instances
        for match in re.finditer(self.service_patterns['service_instance_export'], content, re.MULTILINE):
            instance_name = match.group(1)
            class_name = match.group(2)
            line_number = content[:match.start()].count('\n') + 1
            
            services.append({
                'name': instance_name,
                'type': 'instance',
                'class_name': class_name,
                'line_number': line_number,
                'is_exported': True
            })
        
        return services
    
    def _extract_service_methods(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract methods from service class"""
        methods = []
        
        # Find class body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return methods
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        class_body = content[brace_start:brace_end]
        
        # Find async methods
        for match in re.finditer(self.service_patterns['service_method_async'], class_body):
            method_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            methods.append({
                'name': method_name,
                'type': 'async',
                'line_number': line_number,
                'parameters': self._extract_method_parameters(match.group(0)),
                'return_type': 'Promise'
            })
        
        # Find sync methods
        for match in re.finditer(self.service_patterns['service_method_sync'], class_body):
            method_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            methods.append({
                'name': method_name,
                'type': 'sync',
                'line_number': line_number,
                'parameters': self._extract_method_parameters(match.group(0)),
                'return_type': 'any'
            })
        
        return methods
    
    def _extract_service_properties(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract properties from service class"""
        properties = []
        
        # Find class body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return properties
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        class_body = content[brace_start:brace_end]
        
        # Find class properties
        for match in re.finditer(r'(?:public|private|protected)?\s*(\w+)\s*:\s*([^=;]+)', class_body):
            prop_name = match.group(1)
            prop_type = match.group(2).strip()
            
            properties.append({
                'name': prop_name,
                'type': prop_type,
                'is_private': 'private' in match.group(0)
            })
        
        return properties
    
    def _calculate_class_complexity(self, content: str, start_pos: int) -> int:
        """Calculate complexity of a service class"""
        complexity = 1
        
        # Find class body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return complexity
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        class_body = content[brace_start:brace_end]
        
        # Count decision points
        complexity += len(re.findall(r'\b(if|else|while|for|switch|case|&&|\|\|)\b', class_body))
        
        return complexity
    
    def _extract_interfaces(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract TypeScript interfaces from content"""
        interfaces = []
        
        for match in re.finditer(self.typescript_patterns['interface'], content, re.MULTILINE):
            interface_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            interfaces.append({
                'name': interface_name,
                'line_number': line_number,
                'properties': self._extract_interface_properties(content, match.start()),
                'methods': self._extract_interface_methods(content, match.start()),
                'extends': self._extract_interface_extends(content, match.start()),
                'is_exported': 'export' in content[max(0, match.start()-50):match.start()]
            })
        
        return interfaces
    
    def _extract_hooks(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract React hooks from content"""
        hooks = []
        
        for hook_name, pattern in self.hook_patterns.items():
            for match in re.finditer(pattern, content, re.MULTILINE):
                line_number = content[:match.start()].count('\n') + 1
                
                hooks.append({
                    'name': hook_name,
                    'line_number': line_number,
                    'dependencies': self._extract_hook_dependencies(content, match.start()),
                    'return_type': self._extract_hook_return_type(content, match.start()),
                    'is_custom': hook_name == 'custom_hook',
                    'complexity': self._calculate_hook_complexity(content, match.start())
                })
        
        return hooks
    
    def _extract_props_from_function(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract props from a function component"""
        # Find the function parameters
        paren_start = content.find('(', start_pos)
        paren_end = content.find(')', paren_start)
        
        if paren_start == -1 or paren_end == -1:
            return []
        
        params_text = content[paren_start+1:paren_end]
        props = []
        
        # Simple prop extraction (can be enhanced)
        for param in params_text.split(','):
            param = param.strip()
            if param:
                prop_name = param.split(':')[0].strip()
                prop_type = param.split(':')[1].strip() if ':' in param else 'any'
                props.append({
                    'name': prop_name,
                    'type': prop_type,
                    'required': '?' not in param
                })
        
        return props
    
    def _extract_state_from_function(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract state variables from a function component"""
        # Find useState calls within the function
        state_vars = []
        
        # Find the function body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return state_vars
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        function_body = content[brace_start:brace_end]
        
        # Find useState calls
        for match in re.finditer(r'useState\s*\([^)]*\)', function_body):
            state_vars.append({
                'name': 'state_variable',
                'type': 'useState',
                'initial_value': match.group(0)
            })
        
        return state_vars
    
    def _extract_hooks_from_function(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract hooks used in a function component"""
        hooks = []
        
        # Find the function body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return hooks
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        function_body = content[brace_start:brace_end]
        
        # Find all hook calls
        for hook_name, pattern in self.hook_patterns.items():
            for match in re.finditer(pattern, function_body):
                hooks.append({
                    'name': hook_name,
                    'line_number': content[:match.start()].count('\n') + 1,
                    'dependencies': self._extract_hook_dependencies(content, match.start())
                })
        
        return hooks
    
    def _extract_jsx_elements(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract JSX elements from a function component"""
        jsx_elements = []
        
        # Find JSX return statement
        return_match = re.search(r'return\s*\([^)]*\)', content[start_pos:])
        if not return_match:
            return jsx_elements
        
        return_content = return_match.group(0)
        
        # Find JSX elements
        for match in re.finditer(r'<(\w+)(?:\s+[^>]*)?>', return_content):
            element_name = match.group(1)
            jsx_elements.append({
                'name': element_name,
                'type': 'jsx_element',
                'props': self._extract_jsx_props(match.group(0))
            })
        
        return jsx_elements
    
    def _extract_event_handlers(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract event handlers from a function component"""
        handlers = []
        
        # Find function body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return handlers
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        function_body = content[brace_start:brace_end]
        
        # Find event handler functions
        for match in re.finditer(r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{', function_body):
            handler_name = match.group(1)
            if any(event in handler_name.lower() for event in ['handle', 'on', 'click', 'change', 'submit']):
                handlers.append({
                    'name': handler_name,
                    'type': 'event_handler',
                    'line_number': content[:match.start()].count('\n') + 1
                })
        
        return handlers
    
    def _extract_imports(self, content: str) -> List[Dict[str, Any]]:
        """Extract import statements from content"""
        imports = []
        
        for match in re.finditer(r'import\s+(?:{([^}]+)}|\* as (\w+)|(\w+))\s+from\s+[\'"]([^\'"]+)[\'"]', content):
            if match.group(1):  # Named imports
                named_imports = [imp.strip() for imp in match.group(1).split(',')]
                for named_import in named_imports:
                    imports.append({
                        'name': named_import,
                        'source': match.group(4),
                        'type': 'named'
                    })
            elif match.group(2):  # Namespace import
                imports.append({
                    'name': match.group(2),
                    'source': match.group(4),
                    'type': 'namespace'
                })
            elif match.group(3):  # Default import
                imports.append({
                    'name': match.group(3),
                    'source': match.group(4),
                    'type': 'default'
                })
        
        return imports
    
    def _extract_exports(self, content: str) -> List[Dict[str, Any]]:
        """Extract export statements from content"""
        exports = []
        
        # Default exports
        for match in re.finditer(r'export\s+default\s+(\w+)', content):
            exports.append({
                'name': match.group(1),
                'type': 'default'
            })
        
        # Named exports
        for match in re.finditer(r'export\s+(?:const|function|class)\s+(\w+)', content):
            exports.append({
                'name': match.group(1),
                'type': 'named'
            })
        
        return exports
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract external dependencies from content"""
        dependencies = set()
        
        # Find import statements
        for match in re.finditer(r'from\s+[\'"]([^\'"]+)[\'"]', content):
            dep = match.group(1)
            if not dep.startswith('.'):  # External dependency
                dependencies.add(dep.split('/')[0])
        
        return list(dependencies)
    
    def _calculate_complexity(self, content: str) -> int:
        """Calculate cyclomatic complexity of the file"""
        complexity = 1  # Base complexity
        
        # Count decision points
        complexity += len(re.findall(r'\b(if|else|while|for|switch|case|catch|&&|\|\|)\b', content))
        
        return complexity
    
    def _extract_business_logic(self, content: str) -> List[Dict[str, Any]]:
        """Extract business logic patterns from content"""
        business_logic = []
        
        # API calls
        for match in re.finditer(r'(fetch|axios|api)\.(get|post|put|delete)\s*\([^)]*\)', content):
            business_logic.append({
                'type': 'api_call',
                'method': match.group(2),
                'line': content[:match.start()].count('\n') + 1
            })
        
        # State management
        for match in re.finditer(r'setState|useState|useReducer', content):
            business_logic.append({
                'type': 'state_management',
                'pattern': match.group(0),
                'line': content[:match.start()].count('\n') + 1
            })
        
        # Event handling
        for match in re.finditer(r'onClick|onChange|onSubmit', content):
            business_logic.append({
                'type': 'event_handling',
                'pattern': match.group(0),
                'line': content[:match.start()].count('\n') + 1
            })
        
        return business_logic
    
    def _extract_interface_properties(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract properties from TypeScript interface"""
        properties = []
        
        # Find interface body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return properties
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        interface_body = content[brace_start:brace_end]
        
        # Find properties
        for match in re.finditer(r'(\w+)(\?)?\s*:\s*([^;]+)', interface_body):
            properties.append({
                'name': match.group(1),
                'type': match.group(3).strip(),
                'optional': bool(match.group(2))
            })
        
        return properties
    
    def _extract_interface_methods(self, content: str, start_pos: int) -> List[Dict[str, Any]]:
        """Extract methods from TypeScript interface"""
        methods = []
        
        # Find interface body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return methods
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        interface_body = content[brace_start:brace_end]
        
        # Find methods
        for match in re.finditer(r'(\w+)\s*\([^)]*\)\s*:\s*([^;]+)', interface_body):
            methods.append({
                'name': match.group(1),
                'return_type': match.group(2).strip(),
                'parameters': self._extract_method_parameters(match.group(0))
            })
        
        return methods
    
    def _extract_method_parameters(self, method_signature: str) -> List[Dict[str, Any]]:
        """Extract parameters from method signature"""
        parameters = []
        
        # Find parameters in parentheses
        paren_start = method_signature.find('(')
        paren_end = method_signature.find(')', paren_start)
        
        if paren_start == -1 or paren_end == -1:
            return parameters
        
        params_text = method_signature[paren_start+1:paren_end]
        
        # Simple parameter extraction
        for param in params_text.split(','):
            param = param.strip()
            if param:
                param_name = param.split(':')[0].strip()
                param_type = param.split(':')[1].strip() if ':' in param else 'any'
                parameters.append({
                    'name': param_name,
                    'type': param_type
                })
        
        return parameters
    
    def _extract_interface_extends(self, content: str, start_pos: int) -> List[str]:
        """Extract extends clause from TypeScript interface"""
        extends_match = re.search(r'extends\s+([^{]+)', content[start_pos:start_pos+200])
        if extends_match:
            return [ext.strip() for ext in extends_match.group(1).split(',')]
        return []
    
    def _extract_hook_dependencies(self, content: str, start_pos: int) -> List[str]:
        """Extract dependencies from hook call"""
        # Find the dependency array
        bracket_start = content.find('[', start_pos)
        if bracket_start == -1:
            return []
        
        bracket_end = content.find(']', bracket_start)
        if bracket_end == -1:
            return []
        
        deps_text = content[bracket_start+1:bracket_end]
        return [dep.strip() for dep in deps_text.split(',') if dep.strip()]
    
    def _extract_hook_return_type(self, content: str, start_pos: int) -> str:
        """Extract return type from hook call"""
        # Look for type annotation before the hook
        type_match = re.search(r'(\w+)\s*:\s*([^=]+)\s*=', content[max(0, start_pos-100):start_pos])
        if type_match:
            return type_match.group(2).strip()
        return 'any'
    
    def _calculate_hook_complexity(self, content: str, start_pos: int) -> int:
        """Calculate complexity of a hook"""
        complexity = 1
        
        # Find the hook body
        paren_start = content.find('(', start_pos)
        if paren_start == -1:
            return complexity
        
        # Find matching closing parenthesis
        paren_count = 0
        paren_end = paren_start
        for i, char in enumerate(content[paren_start:], paren_start):
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count == 0:
                    paren_end = i
                    break
        
        hook_body = content[paren_start:paren_end]
        
        # Count decision points in hook body
        complexity += len(re.findall(r'\b(if|else|while|for|switch|case|&&|\|\|)\b', hook_body))
        
        return complexity
    
    def _calculate_function_complexity(self, content: str, start_pos: int) -> int:
        """Calculate complexity of a function component"""
        complexity = 1
        
        # Find the function body
        brace_start = content.find('{', start_pos)
        if brace_start == -1:
            return complexity
        
        # Find matching closing brace
        brace_count = 0
        brace_end = brace_start
        for i, char in enumerate(content[brace_start:], brace_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    brace_end = i
                    break
        
        function_body = content[brace_start:brace_end]
        
        # Count decision points
        complexity += len(re.findall(r'\b(if|else|while|for|switch|case|&&|\|\|)\b', function_body))
        
        return complexity
    
    def _extract_jsx_props(self, jsx_element: str) -> List[Dict[str, Any]]:
        """Extract props from JSX element"""
        props = []
        
        # Find all prop patterns
        for match in re.finditer(r'(\w+)=[\'"]([^\'"]*)[\'"]', jsx_element):
            props.append({
                'name': match.group(1),
                'value': match.group(2),
                'type': 'string'
            })
        
        for match in re.finditer(r'(\w+)=\{([^}]+)\}', jsx_element):
            props.append({
                'name': match.group(1),
                'value': match.group(2),
                'type': 'expression'
            })
        
        return props
