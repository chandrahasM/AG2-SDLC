"""
Code Generation Agent
Generates React/TypeScript code based on design specifications
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

class CodeGenerationAgent:
    """
    Code Generation Agent for React/TypeScript Applications
    
    Responsibilities:
    - Generate React components based on design specifications
    - Create TypeScript interfaces and types
    - Generate API service functions
    - Create test files
    - Generate documentation
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
        
        # Create the code generation agent
        self.generator_agent = ConversableAgent(
            name="code_generator",
            system_message=self._get_generator_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.logger.info("Code Generation Agent initialized")
    
    def _get_generator_system_message(self) -> str:
        """System message for the code generation agent"""
        return """
You are a Code Generation Agent specialized in React/TypeScript applications.

Your responsibilities:
1. Generate React components based on design specifications
2. Create TypeScript interfaces and type definitions
3. Generate API service functions and hooks
4. Create comprehensive test files
5. Generate documentation and comments
6. Ensure code follows best practices and patterns

You work with design specifications to generate production-ready, maintainable code that follows React and TypeScript best practices.

Always generate clean, well-documented, and testable code that can be directly integrated into the project.
"""
    
    def generate_code(self, design_specifications: Dict[str, Any],
                     code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate code based on design specifications
        
        Args:
            design_specifications: Design specifications from design architect
            code_analysis: Current code analysis from repository analyzer
        
        Returns:
            Generated code files and implementation details
        """
        self.logger.info("Generating code based on design specifications...")
        
        try:
            # Phase 1: Analyze design specifications
            print("📋 Phase 1: Analyzing design specifications...")
            spec_analysis = self._analyze_design_specifications(design_specifications)
            
            # Phase 2: Generate new components
            print("🏗️ Phase 2: Generating new components...")
            new_components = self._generate_new_components(spec_analysis.get('new_components', []))
            
            # Phase 3: Update existing components
            print("🔄 Phase 3: Updating existing components...")
            updated_components = self._update_existing_components(spec_analysis.get('updated_components', []))
            
            # Phase 4: Generate API services
            print("🌐 Phase 4: Generating API services...")
            api_services = self._generate_api_services(spec_analysis.get('api_designs', []))
            
            # Phase 5: Generate TypeScript types
            print("📝 Phase 5: Generating TypeScript types...")
            typescript_types = self._generate_typescript_types(spec_analysis)
            
            # Phase 6: Generate custom hooks
            print("🪝 Phase 6: Generating custom hooks...")
            custom_hooks = self._generate_custom_hooks(spec_analysis)
            
            # Phase 7: Generate tests
            print("🧪 Phase 7: Generating tests...")
            test_files = self._generate_test_files(new_components, updated_components, api_services)
            
            # Phase 8: Generate documentation
            print("📚 Phase 8: Generating documentation...")
            documentation = self._generate_documentation(spec_analysis, new_components, updated_components)
            
            # Phase 9: LLM code review
            print("🤖 Phase 9: LLM code review...")
            code_review = self._run_code_review(new_components, updated_components, api_services)
            
            return {
                'new_components': new_components,
                'updated_components': updated_components,
                'api_services': api_services,
                'typescript_types': typescript_types,
                'custom_hooks': custom_hooks,
                'test_files': test_files,
                'documentation': documentation,
                'code_review': code_review,
                'generation_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            return {
                'error': str(e),
                'generation_timestamp': datetime.now().isoformat()
            }
    
    def _analyze_design_specifications(self, design_specifications: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze design specifications to extract generation requirements"""
        spec_analysis = {
            'new_components': [],
            'updated_components': [],
            'api_designs': [],
            'data_models': [],
            'user_flows': [],
            'implementation_plan': design_specifications.get('implementation_plan', {})
        }
        
        # Extract new components from design specifications
        if 'new_components' in design_specifications:
            spec_analysis['new_components'] = design_specifications['new_components']
        
        # Extract updated components
        if 'updated_components' in design_specifications:
            spec_analysis['updated_components'] = design_specifications['updated_components']
        
        # Extract API designs
        if 'api_designs' in design_specifications:
            spec_analysis['api_designs'] = design_specifications['api_designs']
        
        # Extract data models
        if 'data_models' in design_specifications:
            spec_analysis['data_models'] = design_specifications['data_models']
        
        # Extract user flows
        if 'user_flows' in design_specifications:
            spec_analysis['user_flows'] = design_specifications['user_flows']
        
        return spec_analysis
    
    def _generate_new_components(self, new_components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate new React components"""
        generated_components = []
        
        for component_spec in new_components:
            component_name = component_spec['name']
            component_type = component_spec.get('type', 'component')
            
            # Generate component code
            component_code = self._generate_component_code(component_spec)
            
            # Generate component file
            component_file = {
                'file_path': f"src/components/{component_name}.tsx",
                'content': component_code,
                'component_name': component_name,
                'type': component_type,
                'dependencies': component_spec.get('dependencies', []),
                'props_interface': component_spec.get('props_interface', {}),
                'state_interface': component_spec.get('state_interface', {}),
                'business_logic': component_spec.get('business_logic', [])
            }
            
            generated_components.append(component_file)
        
        return generated_components
    
    def _generate_component_code(self, component_spec: Dict[str, Any]) -> str:
        """Generate the actual React component code"""
        component_name = component_spec['name']
        props_interface = component_spec.get('props_interface', {})
        state_interface = component_spec.get('state_interface', {})
        business_logic = component_spec.get('business_logic', [])
        event_handlers = component_spec.get('event_handlers', [])
        lifecycle_methods = component_spec.get('lifecycle_methods', [])
        
        # Generate imports
        imports = self._generate_component_imports(component_spec)
        
        # Generate props interface
        props_interface_code = self._generate_props_interface_code(props_interface)
        
        # Generate state interface
        state_interface_code = self._generate_state_interface_code(state_interface)
        
        # Generate business logic functions
        business_logic_code = self._generate_business_logic_code(business_logic)
        
        # Generate event handlers
        event_handlers_code = self._generate_event_handlers_code(event_handlers)
        
        # Generate lifecycle methods
        lifecycle_methods_code = self._generate_lifecycle_methods_code(lifecycle_methods)
        
        # Generate JSX
        jsx_code = self._generate_jsx_code(component_spec)
        
        # Combine all parts
        component_code = f"""
{imports}

{props_interface_code}

{state_interface_code}

{self._generate_component_comment(component_spec)}

const {component_name}: React.FC<{props_interface.get('interface_name', f'{component_name}Props')}> = ({{
{self._generate_props_destructuring(props_interface)}
}}) => {{
{business_logic_code}

{event_handlers_code}

{lifecycle_methods_code}

{jsx_code}
}};

export default {component_name};
"""
        
        return component_code.strip()
    
    def _generate_component_imports(self, component_spec: Dict[str, Any]) -> str:
        """Generate imports for the component"""
        component_name = component_spec['name']
        
        imports = [
            "import React from 'react';",
            "import './styles.css';"
        ]
        
        # Add hooks imports
        if component_spec.get('lifecycle_methods'):
            imports.append("import { useEffect, useState, useCallback } from 'react';")
        
        # Add business logic imports
        business_logic = component_spec.get('business_logic', [])
        if business_logic:
            imports.append("import { apiService } from '../services/apiService';")
        
        # Add dependencies
        dependencies = component_spec.get('dependencies', [])
        for dep in dependencies:
            if dep.startswith('@'):
                imports.append(f"import {dep} from '{dep}';")
            else:
                imports.append(f"import {dep} from '../{dep}';")
        
        return '\n'.join(imports)
    
    def _generate_props_interface_code(self, props_interface: Dict[str, Any]) -> str:
        """Generate props interface code"""
        if not props_interface:
            return ""
        
        interface_name = props_interface.get('interface_name', 'Props')
        properties = props_interface.get('properties', [])
        
        if not properties:
            return f"interface {interface_name} {{}}"
        
        interface_code = f"interface {interface_name} {{\n"
        
        for prop in properties:
            prop_name = prop.get('name', '')
            prop_type = prop.get('type', 'any')
            required = prop.get('required', False)
            description = prop.get('description', '')
            
            optional_marker = '?' if not required else ''
            comment = f"  // {description}\n" if description else ""
            
            interface_code += f"{comment}  {prop_name}{optional_marker}: {prop_type};\n"
        
        interface_code += "}"
        
        return interface_code
    
    def _generate_state_interface_code(self, state_interface: Dict[str, Any]) -> str:
        """Generate state interface code"""
        if not state_interface:
            return ""
        
        interface_name = state_interface.get('interface_name', 'State')
        properties = state_interface.get('properties', [])
        
        if not properties:
            return f"interface {interface_name} {{}}"
        
        interface_code = f"interface {interface_name} {{\n"
        
        for prop in properties:
            prop_name = prop.get('name', '')
            prop_type = prop.get('type', 'any')
            default_value = prop.get('default', '')
            description = prop.get('description', '')
            
            comment = f"  // {description}\n" if description else ""
            
            interface_code += f"{comment}  {prop_name}: {prop_type};\n"
        
        interface_code += "}"
        
        return interface_code
    
    def _generate_business_logic_code(self, business_logic: List[Dict[str, Any]]) -> str:
        """Generate business logic code"""
        if not business_logic:
            return ""
        
        logic_code = ""
        
        for logic in business_logic:
            function_name = logic.get('name', '')
            description = logic.get('description', '')
            parameters = logic.get('parameters', [])
            return_type = logic.get('return_type', 'void')
            error_handling = logic.get('error_handling', '')
            
            # Generate function signature
            param_list = ', '.join(parameters)
            function_signature = f"const {function_name} = async ({param_list}): Promise<{return_type}> => {{"
            
            # Generate function body
            function_body = f"""
    try {{
        // {description}
        // TODO: Implement {function_name}
        throw new Error('Not implemented');
    }} catch (error) {{
        console.error('Error in {function_name}:', error);
        {error_handling}
        throw error;
    }}
}};"""
            
            logic_code += f"\n{function_signature}{function_body}\n"
        
        return logic_code
    
    def _generate_event_handlers_code(self, event_handlers: List[Dict[str, Any]]) -> str:
        """Generate event handlers code"""
        if not event_handlers:
            return ""
        
        handlers_code = ""
        
        for handler in event_handlers:
            handler_name = handler.get('name', '')
            description = handler.get('description', '')
            parameters = handler.get('parameters', [])
            implementation = handler.get('implementation', '')
            
            # Generate handler function
            param_list = ', '.join(parameters)
            handler_function = f"const {handler_name} = useCallback(({param_list}) => {{"
            
            # Generate handler body
            handler_body = f"""
        // {description}
        {implementation}
    }}, []);"""
            
            handlers_code += f"\n{handler_function}{handler_body}\n"
        
        return handlers_code
    
    def _generate_lifecycle_methods_code(self, lifecycle_methods: List[Dict[str, Any]]) -> str:
        """Generate lifecycle methods code"""
        if not lifecycle_methods:
            return ""
        
        methods_code = ""
        
        for method in lifecycle_methods:
            method_name = method.get('name', '')
            description = method.get('description', '')
            dependencies = method.get('dependencies', [])
            implementation = method.get('implementation', '')
            
            if method_name == 'useEffect':
                deps_array = ', '.join(dependencies) if dependencies else '[]'
                method_code = f"""
useEffect(() => {{
    // {description}
    {implementation}
}}, [{deps_array}]);"""
            elif method_name == 'useCallback':
                deps_array = ', '.join(dependencies) if dependencies else '[]'
                method_code = f"""
const memoizedFunction = useCallback(() => {{
    // {description}
    {implementation}
}}, [{deps_array}]);"""
            else:
                method_code = f"""
// {description}
{implementation}"""
            
            methods_code += method_code
        
        return methods_code
    
    def _generate_jsx_code(self, component_spec: Dict[str, Any]) -> str:
        """Generate JSX code for the component"""
        component_name = component_spec['name']
        
        # Generate basic JSX structure
        jsx_code = f"""
return (
    <div className="{component_name.lower()}-container">
        <h2>{component_name}</h2>
        <div className="{component_name.lower()}-content">
            {{/* TODO: Implement {component_name} content */}}
        </div>
    </div>
);"""
        
        return jsx_code
    
    def _generate_component_comment(self, component_spec: Dict[str, Any]) -> str:
        """Generate component comment"""
        component_name = component_spec['name']
        description = component_spec.get('description', '')
        
        return f"""
/**
 * {component_name} Component
 * 
 * {description}
 * 
 * @component
 */"""
    
    def _generate_props_destructuring(self, props_interface: Dict[str, Any]) -> str:
        """Generate props destructuring"""
        properties = props_interface.get('properties', [])
        
        if not properties:
            return ""
        
        prop_names = [prop.get('name', '') for prop in properties]
        return ', '.join(prop_names)
    
    def _update_existing_components(self, updated_components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Update existing components based on specifications"""
        updated_component_files = []
        
        for component_spec in updated_components:
            component_name = component_spec['name']
            changes = component_spec.get('changes', [])
            
            # Generate updated component code
            updated_code = self._generate_updated_component_code(component_spec)
            
            # Create updated component file
            updated_file = {
                'file_path': f"src/components/{component_name}.tsx",
                'content': updated_code,
                'component_name': component_name,
                'changes': changes,
                'migration_guide': component_spec.get('migration_guide', {})
            }
            
            updated_component_files.append(updated_file)
        
        return updated_component_files
    
    def _generate_updated_component_code(self, component_spec: Dict[str, Any]) -> str:
        """Generate updated component code"""
        component_name = component_spec['name']
        changes = component_spec.get('changes', [])
        
        # Generate migration comments
        migration_comments = self._generate_migration_comments(changes)
        
        # Generate updated component code
        updated_code = f"""
// Updated {component_name} Component
{migration_comments}

// TODO: Apply the following changes:
{self._generate_change_instructions(changes)}

// Original component code would be here with applied changes
"""
        
        return updated_code
    
    def _generate_migration_comments(self, changes: List[Dict[str, Any]]) -> str:
        """Generate migration comments for changes"""
        comments = []
        
        for change in changes:
            field = change.get('field', '')
            change_type = change.get('type', '')
            
            if change_type == 'addition':
                comments.append(f"// NEW: Added {field}")
            elif change_type == 'modification':
                comments.append(f"// MODIFIED: Updated {field}")
            elif change_type == 'removal':
                comments.append(f"// REMOVED: {field}")
        
        return '\n'.join(comments)
    
    def _generate_change_instructions(self, changes: List[Dict[str, Any]]) -> str:
        """Generate change instructions"""
        instructions = []
        
        for change in changes:
            field = change.get('field', '')
            change_type = change.get('type', '')
            data = change.get('data', {})
            
            if change_type == 'addition':
                instructions.append(f"- Add {field}: {data}")
            elif change_type == 'modification':
                old_data = change.get('old', {})
                new_data = change.get('new', {})
                instructions.append(f"- Update {field}: {old_data} -> {new_data}")
            elif change_type == 'removal':
                instructions.append(f"- Remove {field}: {data}")
        
        return '\n'.join(instructions)
    
    def _generate_api_services(self, api_designs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate API service functions"""
        api_services = []
        
        for api_design in api_designs:
            endpoint = api_design['endpoint']
            method = api_design.get('method', 'GET')
            parameters = api_design.get('parameters', [])
            response_schema = api_design.get('response_schema', {})
            
            # Generate API service function
            service_function = self._generate_api_service_function(api_design)
            
            # Create API service file
            service_file = {
                'file_path': f"src/services/api{endpoint.replace('/', '').replace('api', '')}.ts",
                'content': service_function,
                'endpoint': endpoint,
                'method': method,
                'parameters': parameters,
                'response_schema': response_schema
            }
            
            api_services.append(service_file)
        
        return api_services
    
    def _generate_api_service_function(self, api_design: Dict[str, Any]) -> str:
        """Generate API service function"""
        endpoint = api_design['endpoint']
        method = api_design.get('method', 'GET')
        parameters = api_design.get('parameters', [])
        response_schema = api_design.get('response_schema', {})
        error_handling = api_design.get('error_handling', {})
        
        # Generate function signature
        param_list = ', '.join([f"{param['name']}: {param['type']}" for param in parameters])
        function_name = f"fetch{endpoint.replace('/', '').replace('api', '').title()}"
        
        # Generate function body
        function_body = f"""
export const {function_name} = async ({param_list}): Promise<any> => {{
    try {{
        const response = await fetch('{endpoint}', {{
            method: '{method}',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: method !== 'GET' ? JSON.stringify({{ {', '.join([param['name'] for param in parameters])} }}) : undefined,
        }});
        
        if (!response.ok) {{
            throw new Error(`HTTP error! status: ${{response.status}}`);
        }}
        
        const data = await response.json();
        return data;
    }} catch (error) {{
        console.error('Error fetching {endpoint}:', error);
        throw error;
    }}
}};"""
        
        return function_body
    
    def _generate_typescript_types(self, spec_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate TypeScript type definitions"""
        typescript_types = []
        
        # Generate types for new components
        for component in spec_analysis.get('new_components', []):
            component_name = component['name']
            
            # Generate props type
            props_interface = component.get('props_interface', {})
            if props_interface:
                type_file = {
                    'file_path': f"src/types/{component_name}Types.ts",
                    'content': self._generate_props_interface_code(props_interface),
                    'type_name': props_interface.get('interface_name', f'{component_name}Props')
                }
                typescript_types.append(type_file)
            
            # Generate state type
            state_interface = component.get('state_interface', {})
            if state_interface:
                type_file = {
                    'file_path': f"src/types/{component_name}State.ts",
                    'content': self._generate_state_interface_code(state_interface),
                    'type_name': state_interface.get('interface_name', f'{component_name}State')
                }
                typescript_types.append(type_file)
        
        # Generate API types
        for api_design in spec_analysis.get('api_designs', []):
            endpoint = api_design['endpoint']
            response_schema = api_design.get('response_schema', {})
            
            if response_schema:
                type_file = {
                    'file_path': f"src/types/api{endpoint.replace('/', '').replace('api', '')}Types.ts",
                    'content': self._generate_api_response_type(response_schema, endpoint),
                    'type_name': f"{endpoint.replace('/', '').replace('api', '')}Response"
                }
                typescript_types.append(type_file)
        
        return typescript_types
    
    def _generate_api_response_type(self, response_schema: Dict[str, Any], endpoint: str) -> str:
        """Generate API response type"""
        type_name = f"{endpoint.replace('/', '').replace('api', '')}Response"
        
        if not response_schema:
            return f"export interface {type_name} {{}}"
        
        properties = response_schema.get('properties', {})
        
        type_code = f"export interface {type_name} {{\n"
        
        for prop_name, prop_schema in properties.items():
            prop_type = self._convert_json_schema_to_typescript(prop_schema)
            type_code += f"  {prop_name}: {prop_type};\n"
        
        type_code += "}"
        
        return type_code
    
    def _convert_json_schema_to_typescript(self, schema: Dict[str, Any]) -> str:
        """Convert JSON schema to TypeScript type"""
        if 'type' in schema:
            if schema['type'] == 'string':
                return 'string'
            elif schema['type'] == 'number':
                return 'number'
            elif schema['type'] == 'boolean':
                return 'boolean'
            elif schema['type'] == 'array':
                items = schema.get('items', {})
                item_type = self._convert_json_schema_to_typescript(items)
                return f"{item_type}[]"
            elif schema['type'] == 'object':
                properties = schema.get('properties', {})
                if properties:
                    object_type = "{\n"
                    for prop_name, prop_schema in properties.items():
                        prop_type = self._convert_json_schema_to_typescript(prop_schema)
                        object_type += f"    {prop_name}: {prop_type};\n"
                    object_type += "  }"
                    return object_type
                else:
                    return "object"
        
        return "any"
    
    def _generate_custom_hooks(self, spec_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate custom hooks"""
        custom_hooks = []
        
        # Generate hooks for new components
        for component in spec_analysis.get('new_components', []):
            component_name = component['name']
            business_logic = component.get('business_logic', [])
            
            if business_logic:
                hook_name = f"use{component_name}"
                hook_code = self._generate_custom_hook_code(hook_name, business_logic)
                
                hook_file = {
                    'file_path': f"src/hooks/{hook_name}.ts",
                    'content': hook_code,
                    'hook_name': hook_name,
                    'business_logic': business_logic
                }
                
                custom_hooks.append(hook_file)
        
        return custom_hooks
    
    def _generate_custom_hook_code(self, hook_name: str, business_logic: List[Dict[str, Any]]) -> str:
        """Generate custom hook code"""
        hook_code = f"""
import {{ useState, useEffect, useCallback }} from 'react';

export const {hook_name} = () => {{
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    
    // Business logic functions
{self._generate_business_logic_code(business_logic)}
    
    return {{
        data,
        loading,
        error,
        // Expose business logic functions
        // TODO: Add specific functions based on business logic
    }};
}};"""
        
        return hook_code
    
    def _generate_test_files(self, new_components: List[Dict[str, Any]], 
                            updated_components: List[Dict[str, Any]], 
                            api_services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate test files"""
        test_files = []
        
        # Generate tests for new components
        for component in new_components:
            component_name = component['component_name']
            test_code = self._generate_component_test_code(component)
            
            test_file = {
                'file_path': f"src/components/__tests__/{component_name}.test.tsx",
                'content': test_code,
                'component_name': component_name,
                'test_type': 'component'
            }
            
            test_files.append(test_file)
        
        # Generate tests for API services
        for api_service in api_services:
            endpoint = api_service['endpoint']
            test_code = self._generate_api_test_code(api_service)
            
            test_file = {
                'file_path': f"src/services/__tests__/api{endpoint.replace('/', '').replace('api', '')}.test.ts",
                'content': test_code,
                'endpoint': endpoint,
                'test_type': 'api'
            }
            
            test_files.append(test_file)
        
        return test_files
    
    def _generate_component_test_code(self, component: Dict[str, Any]) -> str:
        """Generate component test code"""
        component_name = component['component_name']
        
        test_code = f"""
import React from 'react';
import {{ render, screen, fireEvent }} from '@testing-library/react';
import {component_name} from '../{component_name}';

describe('{component_name}', () => {{
    it('renders without crashing', () => {{
        render(<{component_name} />);
        expect(screen.getByText('{component_name}')).toBeInTheDocument();
    }});
    
    it('handles user interactions', () => {{
        render(<{component_name} />);
        // TODO: Add specific interaction tests
    }});
    
    it('displays data correctly', () => {{
        render(<{component_name} />);
        // TODO: Add data display tests
    }});
}});"""
        
        return test_code
    
    def _generate_api_test_code(self, api_service: Dict[str, Any]) -> str:
        """Generate API test code"""
        endpoint = api_service['endpoint']
        method = api_service['method']
        
        test_code = f"""
import {{ fetch{endpoint.replace('/', '').replace('api', '').title()} }} from '../api{endpoint.replace('/', '').replace('api', '')}';

// Mock fetch
global.fetch = jest.fn();

describe('API {endpoint}', () => {{
    beforeEach(() => {{
        (fetch as jest.Mock).mockClear();
    }});
    
    it('fetches data successfully', async () => {{
        const mockData = {{}};
        (fetch as jest.Mock).mockResolvedValueOnce({{
            ok: true,
            json: async () => mockData,
        }});
        
        const result = await fetch{endpoint.replace('/', '').replace('api', '').title()}();
        expect(result).toEqual(mockData);
    }});
    
    it('handles errors correctly', async () => {{
        (fetch as jest.Mock).mockRejectedValueOnce(new Error('API Error'));
        
        await expect(fetch{endpoint.replace('/', '').replace('api', '').title()}()).rejects.toThrow('API Error');
    }});
}});"""
        
        return test_code
    
    def _generate_documentation(self, spec_analysis: Dict[str, Any], 
                               new_components: List[Dict[str, Any]], 
                               updated_components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate documentation"""
        documentation = {
            'readme': self._generate_readme(spec_analysis, new_components, updated_components),
            'component_docs': self._generate_component_documentation(new_components),
            'api_docs': self._generate_api_documentation(spec_analysis.get('api_designs', [])),
            'migration_guide': self._generate_migration_guide(updated_components)
        }
        
        return documentation
    
    def _generate_readme(self, spec_analysis: Dict[str, Any], 
                        new_components: List[Dict[str, Any]], 
                        updated_components: List[Dict[str, Any]]) -> str:
        """Generate README documentation"""
        readme = f"""
# Frontend Code Generation

This document describes the generated code for the frontend application.

## Generated Components

### New Components
{chr(10).join([f"- {comp['component_name']}: {comp['file_path']}" for comp in new_components])}

### Updated Components
{chr(10).join([f"- {comp['component_name']}: {comp['file_path']}" for comp in updated_components])}

## Implementation Plan

{spec_analysis.get('implementation_plan', {}).get('phases', [])}

## Getting Started

1. Install dependencies
2. Run the development server
3. Test the new components

## Testing

Run tests with:
```bash
npm test
```

## Documentation

See individual component files for detailed documentation.
"""
        
        return readme
    
    def _generate_component_documentation(self, new_components: List[Dict[str, Any]]) -> str:
        """Generate component documentation"""
        docs = []
        
        for component in new_components:
            component_name = component['component_name']
            props_interface = component.get('props_interface', {})
            state_interface = component.get('state_interface', {})
            
            doc = f"""
## {component_name}

### Props
{self._generate_props_documentation(props_interface)}

### State
{self._generate_state_documentation(state_interface)}

### Usage
```tsx
import {component_name} from './{component_name}';

<{component_name} />
```
"""
            docs.append(doc)
        
        return '\n'.join(docs)
    
    def _generate_props_documentation(self, props_interface: Dict[str, Any]) -> str:
        """Generate props documentation"""
        if not props_interface:
            return "No props defined."
        
        properties = props_interface.get('properties', [])
        if not properties:
            return "No props defined."
        
        props_doc = []
        for prop in properties:
            prop_name = prop.get('name', '')
            prop_type = prop.get('type', 'any')
            required = prop.get('required', False)
            description = prop.get('description', '')
            
            required_text = "Required" if required else "Optional"
            props_doc.append(f"- `{prop_name}` ({prop_type}): {description} - {required_text}")
        
        return '\n'.join(props_doc)
    
    def _generate_state_documentation(self, state_interface: Dict[str, Any]) -> str:
        """Generate state documentation"""
        if not state_interface:
            return "No state defined."
        
        properties = state_interface.get('properties', [])
        if not properties:
            return "No state defined."
        
        state_doc = []
        for prop in properties:
            prop_name = prop.get('name', '')
            prop_type = prop.get('type', 'any')
            description = prop.get('description', '')
            
            state_doc.append(f"- `{prop_name}` ({prop_type}): {description}")
        
        return '\n'.join(state_doc)
    
    def _generate_api_documentation(self, api_designs: List[Dict[str, Any]]) -> str:
        """Generate API documentation"""
        if not api_designs:
            return "No APIs defined."
        
        api_docs = []
        for api_design in api_designs:
            endpoint = api_design['endpoint']
            method = api_design.get('method', 'GET')
            description = api_design.get('description', '')
            parameters = api_design.get('parameters', [])
            
            api_doc = f"""
## {method} {endpoint}

{description}

### Parameters
{chr(10).join([f"- `{param['name']}` ({param['type']}): {param.get('description', '')}" for param in parameters])}
"""
            api_docs.append(api_doc)
        
        return '\n'.join(api_docs)
    
    def _generate_migration_guide(self, updated_components: List[Dict[str, Any]]) -> str:
        """Generate migration guide"""
        if not updated_components:
            return "No components updated."
        
        migration_guide = []
        for component in updated_components:
            component_name = component['component_name']
            changes = component.get('changes', [])
            migration_guide_item = component.get('migration_guide', {})
            
            guide = f"""
## {component_name} Migration Guide

### Changes
{chr(10).join([f"- {change.get('field', '')}: {change.get('type', '')}" for change in changes])}

### Migration Steps
{chr(10).join([f"- {step}" for step in migration_guide_item.get('migration_steps', [])])}
"""
            migration_guide.append(guide)
        
        return '\n'.join(migration_guide)
    
    def _run_code_review(self, new_components: List[Dict[str, Any]], 
                        updated_components: List[Dict[str, Any]], 
                        api_services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run LLM code review"""
        
        code_summary = {
            'new_components': len(new_components),
            'updated_components': len(updated_components),
            'api_services': len(api_services),
            'total_files': len(new_components) + len(updated_components) + len(api_services)
        }
        
        prompt = f"""
Review the generated code and provide feedback:

{json.dumps(code_summary, indent=2)}

Please review:
1. Code quality and best practices
2. TypeScript usage and type safety
3. React patterns and performance
4. Error handling and edge cases
5. Test coverage and quality
6. Documentation completeness
7. Overall maintainability
"""
        
        try:
            response = self.generator_agent.run(
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
                    'review_result': content,
                    'review_timestamp': datetime.now().isoformat()
                }
            
            return {'review_result': 'No review generated', 'review_timestamp': datetime.now().isoformat()}
            
        except Exception as e:
            self.logger.error(f"Error in code review: {e}")
            return {'review_result': f'Error: {str(e)}', 'review_timestamp': datetime.now().isoformat()}
