"""
Smart Code Generation Agent with Manual Tool Handling
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from autogen import ConversableAgent, LLMConfig

logger = logging.getLogger(__name__)

class SmartCodeGenerationAgent:
    """
    Smart code generation agent that manually handles tool calling to:
    1. Read files
    2. Analyze code structure
    3. Apply changes using search/replace
    4. Create new files
    """
    
    def __init__(self, llm_config: Dict[str, Any], repo_path: str):
        self.logger = logging.getLogger(__name__)
        self.llm_config = llm_config
        self.repo_path = Path(repo_path)
        
        # Create agent with function calling capabilities
        self.agent = ConversableAgent(
            name="smart_code_generator",
            system_message=self._get_system_message(),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            function_map={
                "read_file": self._read_file_tool,
                "search_replace": self._search_replace_tool,
                "create_file": self._create_file_tool,
                "analyze_code": self._analyze_code_tool
            }
        )
        
        self.logger.info("Smart Code Generation Agent initialized")
    
    def _get_system_message(self) -> str:
        """System message for the smart code generator"""
        return """You are an expert React/TypeScript developer with access to file operations.

You will receive:
1. Requirements and user stories
2. Architect's implementation plan
3. Current codebase context and patterns

Your job is to implement the changes using your tools:
- read_file: Understand current code structure
- search_replace: Modify existing files precisely
- create_file: Add new files as needed
- analyze_code: Understand code patterns and structure

Always follow existing code patterns and maintain consistency. Be precise with search/replace operations.

When implementing changes:
1. First read the relevant files to understand the current structure
2. Analyze the code to understand patterns and conventions
3. Implement changes step by step according to the architect's plan
4. Use search_replace for precise modifications
5. Create new files as specified
6. Ensure all changes are consistent with existing code
"""
    
    def generate_code_changes(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code changes using manual tool handling"""
        try:
            self.logger.info("Starting smart code generation with manual tool handling...")
            
            # Extract context from workflow results
            context = self._extract_context(workflow_results)
            
            # Create smart prompt
            prompt = self._create_smart_prompt(context)
            
            # Let agent work with tools manually
            self.logger.info("Agent will now use tools to implement changes manually...")
            response = self.agent.run(prompt)
            
            # Process response
            result = self._process_agent_response(response)
            
            return {
                "status": "success",
                "method": "smart_manual_tool_handling",
                "agent_response": result,
                "tools_used": self._extract_tools_used(response)
            }
            
        except Exception as e:
            self.logger.error(f"Error in smart code generation: {str(e)}")
            return {"error": f"Smart code generation failed: {str(e)}"}
    
    def _extract_context(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant context for code generation"""
        
        # Get architect's analysis
        architect_output = workflow_results.get("architect_agent_output", {})
        implementation_plan = architect_output.get("implementation_plan", {})
        
        # Get repository analysis for code patterns
        repo_analysis = workflow_results.get("supporting_analysis", {}).get("repository_analysis", {})
        
        # Get requirements analysis
        requirements_analysis = workflow_results.get("supporting_analysis", {}).get("requirements_analysis", {})
        
        return {
            "implementation_plan": implementation_plan,
            "codebase_context": repo_analysis,
            "requirements": requirements_analysis
        }
    
    def _create_smart_prompt(self, context: Dict[str, Any]) -> str:
        """Create smart prompt with context"""
        
        implementation_plan = context.get("implementation_plan", {})
        repo_analysis = context.get("codebase_context", {})
        requirements = context.get("requirements", {})
        
        prompt = f"""
You are a React/TypeScript developer. Implement the following changes based on the architect's analysis:

## REQUIREMENTS
{json.dumps(requirements, indent=2)}

## IMPLEMENTATION PLAN
The architect has analyzed the codebase and created this plan:

### Files to Modify:
{json.dumps(implementation_plan.get('files_to_modify', []), indent=2)}

### Files to Create:
{json.dumps(implementation_plan.get('files_to_create', []), indent=2)}

### Implementation Order:
{implementation_plan.get('implementation_order', [])}

## CODEBASE CONTEXT
Current architecture analysis:

### Component Structure:
{json.dumps(repo_analysis.get('component_analysis', {}), indent=2)}

### API Patterns:
{json.dumps(repo_analysis.get('api_contracts', {}), indent=2)}

### State Management:
{json.dumps(repo_analysis.get('state_management', {}), indent=2)}

## YOUR TASK
Use your tools to:
1. Read the current files to understand the structure
2. Analyze the code to understand patterns and conventions
3. Implement the changes according to the architect's plan
4. Follow the existing code patterns and conventions
5. Ensure all changes are consistent with the current architecture

Start by reading the files mentioned in the implementation plan.
"""
        
        return prompt
    
    def _process_agent_response(self, response) -> str:
        """Process the agent's response with detailed logging"""
        try:
            self.logger.info(f"Raw response type: {type(response)}")
            self.logger.info(f"Raw response attributes: {dir(response)}")
            
            # Try to access the actual content from the RunResponse object
            if hasattr(response, 'messages') and response.messages:
                self.logger.info(f"Number of messages: {len(response.messages)}")
                for i, msg in enumerate(response.messages):
                    self.logger.info(f"Message {i}: {type(msg)} - {msg}")
                    if hasattr(msg, 'content'):
                        self.logger.info(f"Message {i} content: {msg.content}")
                
                last_message = response.messages[-1]
                content = last_message.content if hasattr(last_message, 'content') else str(last_message)
                self.logger.info(f"Final agent response content: {content}")
                return content
            elif hasattr(response, 'content'):
                self.logger.info(f"Agent response content: {response.content}")
                return response.content
            elif isinstance(response, str):
                self.logger.info(f"Agent response content: {response}")
                return response
            else:
                # Try to convert the entire response to string and log it
                content = str(response)
                self.logger.info(f"Agent response as string: {content}")
                
                # Try to access any other attributes that might contain the actual content
                if hasattr(response, '__dict__'):
                    self.logger.info(f"Response dict: {response.__dict__}")
                
                return content
        except Exception as e:
            self.logger.error(f"Error processing agent response: {str(e)}")
            return "Error processing response"
    
    def _read_file_tool(self, file_path: str) -> str:
        """Read a file and return its content"""
        try:
            full_path = self.repo_path / file_path
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.logger.info(f"Read file: {file_path} ({len(content)} characters)")
                return f"File content for {file_path}:\n{content}"
            else:
                self.logger.warning(f"File not found: {file_path}")
                return f"File not found: {file_path}"
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file {file_path}: {str(e)}"
    
    def _search_replace_tool(self, file_path: str, search_pattern: str, replacement: str) -> str:
        """Search and replace text in a file"""
        try:
            full_path = self.repo_path / file_path
            if not full_path.exists():
                return f"File not found: {file_path}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if search_pattern in content:
                new_content = content.replace(search_pattern, replacement)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.logger.info(f"Applied search/replace in {file_path}")
                return f"Successfully applied search/replace in {file_path}"
            else:
                self.logger.warning(f"Search pattern not found in {file_path}")
                return f"Search pattern not found in {file_path}"
        except Exception as e:
            self.logger.error(f"Error in search/replace for {file_path}: {str(e)}")
            return f"Error in search/replace for {file_path}: {str(e)}"
    
    def _create_file_tool(self, file_path: str, content: str) -> str:
        """Create a new file with content"""
        try:
            full_path = self.repo_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Created file: {file_path}")
            return f"Successfully created file: {file_path}"
        except Exception as e:
            self.logger.error(f"Error creating file {file_path}: {str(e)}")
            return f"Error creating file {file_path}: {str(e)}"
    
    def _analyze_code_tool(self, file_path: str) -> str:
        """Analyze code structure and return insights"""
        try:
            full_path = self.repo_path / file_path
            if not full_path.exists():
                return f"File not found: {file_path}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            functions = [line.strip() for line in lines if 'function' in line or 'const' in line and '=' in line]
            imports = [line.strip() for line in lines if line.strip().startswith('import')]
            
            analysis = f"""
File: {file_path}
Lines: {len(lines)}
Functions: {len(functions)}
Imports: {len(imports)}
Key functions: {functions[:3]}
            """
            
            self.logger.info(f"Analyzed file: {file_path}")
            return analysis
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return f"Error analyzing file {file_path}: {str(e)}"
    
    def _extract_tools_used(self, response) -> List[str]:
        """Extract which tools were used by the agent"""
        # This would need to be implemented based on how AG2 tracks tool usage
        return ["read_file", "search_replace", "create_file", "analyze_code"]
