"""
Simple Repository Analyzer Agent for testing
"""

import os
import ast
import json
import logging
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# AG2 Framework imports
from autogen import ConversableAgent, LLMConfig

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class SimpleRepositoryAnalyzerAgent:
    """
    Simple Repository Analyzer Agent for testing
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
        
        # Create the repository analyzer agent
        self.analyzer_agent = ConversableAgent(
            name="repository_analyzer",
            system_message="You are a Repository Analyzer Agent. Analyze the provided codebase and provide structured insights.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        
        self.logger.info("Simple Repository Analyzer Agent initialized")
    
    def analyze_repository(self, repo_path: str, file_patterns: List[str] = None, 
                          analysis_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze repository with simple structural analysis
        """
        self.logger.info(f"Starting simple repository analysis: {repo_path}")
        
        try:
            # Simple file analysis
            print("🔍 Analyzing repository structure...")
            files = []
            functions = []
            classes = []
            
            for file_path in Path(repo_path).rglob("*.py"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Simple AST analysis
                    tree = ast.parse(content, filename=str(file_path))
                    relative_path = str(file_path.relative_to(repo_path))
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            functions.append({
                                "name": node.name,
                                "file_path": relative_path,
                                "line_number": node.lineno,
                                "is_async": False
                            })
                        elif isinstance(node, ast.AsyncFunctionDef):
                            functions.append({
                                "name": node.name,
                                "file_path": relative_path,
                                "line_number": node.lineno,
                                "is_async": True
                            })
                        elif isinstance(node, ast.ClassDef):
                            classes.append({
                                "name": node.name,
                                "file_path": relative_path,
                                "line_number": node.lineno,
                                "base_classes": [base.id for base in node.bases if isinstance(base, ast.Name)]
                            })
                    
                    files.append(relative_path)
                    
                except Exception as e:
                    self.logger.warning(f"Error parsing {file_path}: {e}")
                    continue
            
            # Create analysis prompt
            analysis_prompt = f"""Analyze this repository and provide structured insights:

REPOSITORY STRUCTURE:
- Files: {len(files)}
- Functions: {len(functions)}
- Classes: {len(classes)}

FILES:
{json.dumps(files, indent=2)}

FUNCTIONS:
{json.dumps(functions[:10], indent=2)}

CLASSES:
{json.dumps(classes[:10], indent=2)}

Please provide a JSON analysis with:
1. System architecture pattern
2. Key components identified
3. Main functions and their purposes
4. Design patterns detected
5. Recommendations for improvement

Format as JSON with keys: system_architecture, components, functions, design_patterns, recommendations"""

            # Run LLM analysis
            print("🤖 Running LLM analysis...")
            response = self.analyzer_agent.run(message=analysis_prompt, max_turns=1)
            response.process()
            
            # Parse response
            llm_analysis = self._parse_llm_response(response.messages)
            
            # Create structured output
            system_arch = llm_analysis.get("system_architecture", {})
            if isinstance(system_arch, str):
                system_arch = {"pattern": system_arch, "confidence": 0.8, "components": [], "entry_points": [], "design_principles": []}
            
            structured_output = {
                "system_architecture": system_arch,
                "components": llm_analysis.get("components", []),
                "data_models": [],
                "api_contracts": [],
                "function_registry": functions,
                "class_registry": classes,
                "dependency_graph": {
                    "functions": {},
                    "classes": {},
                    "modules": {},
                    "components": {}
                },
                "code_quality_metrics": {
                    "total_functions": len(functions),
                    "total_classes": len(classes),
                    "average_complexity": 0.0,
                    "max_complexity": 0,
                    "documentation_coverage": 0.0,
                    "maintainability_index": 50.0,
                    "technical_debt_score": 50.0
                },
                "design_recommendations": llm_analysis.get("recommendations", []),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            print("✅ Simple repository analysis completed successfully!")
            return structured_output
            
        except Exception as e:
            self.logger.error(f"Error during simple analysis: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "system_architecture": {},
                "components": [],
                "data_models": [],
                "api_contracts": [],
                "function_registry": [],
                "class_registry": [],
                "dependency_graph": {},
                "code_quality_metrics": {},
                "design_recommendations": []
            }
    
    def _parse_llm_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse LLM response and extract analysis"""
        try:
            if not messages:
                return {"error": "No response received from LLM"}
            
            last_message = messages[-1]
            content = last_message.get('content', '')
            
            # Try to extract JSON from the response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Failed to parse JSON from LLM response: {e}")
                    return {"error": f"JSON parsing failed: {e}"}
            else:
                return {"error": "No JSON found in LLM response"}
                
        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {str(e)}")
            return {"error": f"Response parsing failed: {str(e)}"}
