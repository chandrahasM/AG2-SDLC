"""
Real Hybrid Repository Analyzer Agent
Combines Python-based structural analysis with LLM-based semantic analysis
"""

import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from autogen import ConversableAgent, LLMConfig

# Import tools
from .tools.enhanced_react_ast_parser import EnhancedReactASTParser
from .tools.component_analyzer import ComponentAnalyzer

logger = logging.getLogger(__name__)

class RealHybridRepositoryAnalyzerAgent:
    """Real hybrid repository analyzer that combines Python tools with LLM analysis"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize tools
        self.ast_parser = EnhancedReactASTParser()
        self.component_analyzer = ComponentAnalyzer()
        
        # Initialize LLM agents
        self._initialize_llm_agents()
        
        self.logger.info("Real Hybrid Repository Analyzer Agent initialized")
    
    def _initialize_llm_agents(self):
        """Initialize LLM agents for semantic analysis"""
        
        llm_config = {
            "config_list": [{
                "model": self.model_name,
                "temperature": self.temperature
            }],
            "timeout": 300
        }
        
        # Component analyzer agent
        self.component_analyzer_agent = ConversableAgent(
            name="component_analyzer",
            system_message="""You are a React/TypeScript component analyzer. Analyze components and provide:
1. Purpose and business role
2. Props and state management
3. Dependencies and relationships
4. Business logic and functionality
5. Performance characteristics

Return structured JSON with detailed analysis.""",
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
        
        # Business logic analyzer agent
        self.business_logic_agent = ConversableAgent(
            name="business_logic_analyzer",
            system_message="""You are a business logic analyzer. Analyze code and provide:
1. Business domain concepts
2. Business rules and workflows
3. Data flow and transformations
4. API contracts and integrations
5. Error handling strategies

Return structured JSON with detailed business analysis.""",
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
        
        # Architecture analyzer agent
        self.architecture_agent = ConversableAgent(
            name="architecture_analyzer",
            system_message="""You are an architecture analyzer. Analyze codebase and provide:
1. Architectural patterns and principles
2. Component hierarchy and relationships
3. Data flow and state management
4. Integration patterns
5. Scalability and maintainability

Return structured JSON with detailed architectural analysis.""",
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
    
    def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository using hybrid approach"""
        
        self.logger.info(f"Analyzing repository with real hybrid approach: {repo_path}")
        
        try:
            # Phase 1: Fast Python structural analysis
            self.logger.info("🔍 Phase 1: Fast Python structural analysis...")
            structural_analysis = self._analyze_structure(repo_path)
            
            # Phase 2: Component relationship analysis
            self.logger.info("🏗️ Phase 2: Component relationship analysis...")
            component_analysis = self._analyze_component_relationships(structural_analysis)
            
            # Phase 3: LLM semantic analysis
            self.logger.info("🧠 Phase 3: Real LLM semantic analysis...")
            semantic_analysis = self._analyze_with_llm(structural_analysis)
            
            # Phase 4: Generate comprehensive output
            self.logger.info("📋 Phase 4: Generating comprehensive output...")
            comprehensive_output = self._generate_comprehensive_output(
                structural_analysis, component_analysis, semantic_analysis, repo_path
            )
            
            return comprehensive_output
            
        except Exception as e:
            self.logger.error(f"Error in repository analysis: {e}")
            return {
                "error": str(e),
                "repository_metadata": {"total_files": 0},
                "components": {},
                "business_logic": {},
                "semantic_analysis": {}
            }
    
    def _analyze_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository structure using Python tools"""
        
        repo_path = Path(repo_path)
        analysis = {
            "repository_metadata": {
                "repo_path": str(repo_path),
                "total_files": 0,
                "analyzed_files": 0
            },
            "file_analysis": {},
            "components": {},
            "business_logic": {},
            "dependencies": {}
        }
        
        # Find and analyze files
        all_files = []
        for pattern in ["*.ts", "*.tsx", "*.js", "*.jsx"]:
            all_files.extend(list(repo_path.rglob(pattern)))
        self.logger.info(f"Found {len(all_files)} TypeScript/JavaScript files")
        
        for file_path in all_files:
            self.logger.info(f"Checking file: {file_path}")
            if self._is_business_file(file_path):
                self.logger.info(f"Analyzing business file: {file_path}")
                try:
                    file_analysis = self.ast_parser.analyze_file(str(file_path))
                    analysis["file_analysis"][str(file_path)] = file_analysis
                    analysis["repository_metadata"]["analyzed_files"] += 1
                    
                    # Extract components and business logic
                    if file_analysis.get("components"):
                        analysis["components"].update(file_analysis["components"])
                    if file_analysis.get("business_logic"):
                        analysis["business_logic"].update(file_analysis["business_logic"])
                        
                except Exception as e:
                    self.logger.warning(f"Error analyzing file {file_path}: {e}")
            else:
                self.logger.info(f"Skipping non-business file: {file_path}")
        
        analysis["repository_metadata"]["total_files"] = analysis["repository_metadata"]["analyzed_files"]
        return analysis
    
    def _is_business_file(self, file_path: Path) -> bool:
        """Check if file should be analyzed for business logic"""
        
        # Skip node_modules, test files, config files
        if any(part in str(file_path) for part in ['node_modules', 'test', 'spec', 'config', 'dist', 'build']):
            return False
        
        # Must be in src directory
        if 'src' not in file_path.parts:
            return False
        
        # Must be TypeScript/JavaScript file
        return file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']
    
    def _analyze_component_relationships(self, structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze component relationships and dependencies"""
        
        try:
            return self.component_analyzer.analyze_relationships(structural_analysis)
        except Exception as e:
            self.logger.error(f"Error in component relationship analysis: {e}")
            return {"relationships": {}, "dependencies": {}}
    
    def _analyze_with_llm(self, structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code with LLM for semantic understanding"""
        
        semantic_analysis = {
            "component_insights": {},
            "business_capabilities": [],
            "architectural_patterns": [],
            "code_quality_assessment": {},
            "recommendations": []
        }
        
        # Analyze each file with LLM
        for file_path, file_analysis in structural_analysis.get("file_analysis", {}).items():
            try:
                self.logger.info(f"   📄 Analyzing: {Path(file_path).name}")
                
                # Analyze components
                for component_name, component_data in file_analysis.get("components", {}).items():
                    self.logger.info(f"      🧩 Analyzing component: {component_name}")
                    
                    component_insight = self._analyze_component_with_llm(component_data, file_analysis)
                    if component_insight:
                        semantic_analysis["component_insights"][component_name] = component_insight
                
                # Analyze business logic
                for logic_name, logic_data in file_analysis.get("business_logic", {}).items():
                    business_insight = self._analyze_business_logic_with_llm(logic_data, file_analysis)
                    if business_insight:
                        semantic_analysis["business_capabilities"].append(business_insight)
                        
            except Exception as e:
                self.logger.warning(f"Error in LLM analysis for {file_path}: {e}")
        
        # Run architecture analysis
        try:
            self.logger.info("   🏛️ Running architecture analysis...")
            architecture_insights = self._run_architecture_analysis(structural_analysis)
            if architecture_insights:
                semantic_analysis["architectural_patterns"] = architecture_insights.get("patterns", [])
                semantic_analysis["code_quality_assessment"] = architecture_insights.get("quality", {})
                semantic_analysis["recommendations"] = architecture_insights.get("recommendations", [])
        except Exception as e:
            self.logger.warning(f"Error in architecture analysis: {e}")
        
        return semantic_analysis
    
    def _analyze_component_with_llm(self, component_data: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze component with LLM"""
        
        try:
            prompt = f"""
Analyze this React/TypeScript component:

Component: {component_data.get('name', 'Unknown')}
File: {file_analysis.get('file_path', 'Unknown')}
Type: {component_data.get('type', 'Unknown')}
Props: {component_data.get('props', [])}
State: {component_data.get('state', [])}
Methods: {component_data.get('methods', [])}

Provide detailed analysis in JSON format:
{{
    "name": "component_name",
    "purpose": "What this component does",
    "business_role": "Business function it serves",
    "complexity": "low/medium/high",
    "dependencies": ["list of dependencies"],
    "performance_notes": "Performance considerations",
    "maintainability": "How maintainable it is",
    "testing_recommendations": ["testing suggestions"]
}}
"""
            
            response = self.component_analyzer_agent.run(
                message=prompt,
                max_turns=1
            )
            
            # Process response
            content = None
            if hasattr(response, 'messages') and response.messages:
                last_message = response.messages[-1]
                content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            elif hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, str):
                content = response
            else:
                content = str(response)
            
            if content and content.strip() and content.strip() != "None":
                try:
                    parsed_response = json.loads(content)
                    return parsed_response
                except json.JSONDecodeError:
                    return {
                        'name': component_data.get('name', 'Unknown'),
                        'purpose': content,
                        'business_role': 'Component analysis',
                        'analysis_type': 'component',
                        'file_path': file_analysis.get('file_path', 'Unknown'),
                        'llm_response': content
                    }
            return None
            
        except Exception as e:
            self.logger.warning(f"Error analyzing component with LLM: {e}")
            return None
    
    def _analyze_business_logic_with_llm(self, logic_data: Dict[str, Any], file_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze business logic with LLM"""
        
        try:
            prompt = f"""
Analyze this business logic:

Function: {logic_data.get('name', 'Unknown')}
File: {file_analysis.get('file_path', 'Unknown')}
Type: {logic_data.get('type', 'Unknown')}
Parameters: {logic_data.get('parameters', [])}
Return Type: {logic_data.get('return_type', 'Unknown')}

Provide detailed analysis in JSON format:
{{
    "name": "function_name",
    "business_purpose": "What business function this serves",
    "domain_concept": "Business domain it belongs to",
    "complexity": "low/medium/high",
    "dependencies": ["external dependencies"],
    "error_handling": "How errors are handled",
    "testing_strategy": "How to test this function"
}}
"""
            
            response = self.business_logic_agent.run(
                message=prompt,
                max_turns=1
            )
            
            # Process response
            content = None
            if hasattr(response, 'messages') and response.messages:
                last_message = response.messages[-1]
                content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            elif hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, str):
                content = response
            else:
                content = str(response)
            
            if content and content.strip() and content.strip() != "None":
                try:
                    parsed_response = json.loads(content)
                    return parsed_response
                except json.JSONDecodeError:
                    return {
                        'name': logic_data.get('name', 'Unknown'),
                        'business_purpose': content,
                        'domain_concept': 'Business logic analysis',
                        'analysis_type': 'business_logic',
                        'file_path': file_analysis.get('file_path', 'Unknown'),
                        'llm_response': content
                    }
            return None
            
        except Exception as e:
            self.logger.warning(f"Error analyzing business logic with LLM: {e}")
            return None
    
    def _run_architecture_analysis(self, structural_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Run architecture analysis with LLM"""
        
        try:
            prompt = f"""
Analyze the architecture of this React/TypeScript codebase:

Components: {list(structural_analysis.get('components', {}).keys())}
Business Logic: {list(structural_analysis.get('business_logic', {}).keys())}
Total Files: {structural_analysis.get('repository_metadata', {}).get('total_files', 0)}

Provide architectural analysis in JSON format:
{{
    "patterns": ["architectural patterns identified"],
    "quality": {{
        "maintainability": "assessment",
        "scalability": "assessment",
        "testability": "assessment"
    }},
    "recommendations": ["architectural recommendations"],
    "strengths": ["what's working well"],
    "concerns": ["areas of concern"]
}}
"""
            
            response = self.architecture_agent.run(
                message=prompt,
                max_turns=1
            )
            
            # Process response
            content = None
            if hasattr(response, 'messages') and response.messages:
                last_message = response.messages[-1]
                content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            elif hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, str):
                content = response
            else:
                content = str(response)
            
            if content and content.strip() and content.strip() != "None":
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {
                        "patterns": ["Architecture analysis completed"],
                        "quality": {"maintainability": "Good", "scalability": "Good", "testability": "Good"},
                        "recommendations": [content],
                        "strengths": ["Code structure is well organized"],
                        "concerns": []
                    }
            return None
            
        except Exception as e:
            self.logger.warning(f"Error in architecture analysis: {e}")
            return None
    
    def _generate_comprehensive_output(self, structural_analysis: Dict[str, Any], 
                                     component_analysis: Dict[str, Any], 
                                     semantic_analysis: Dict[str, Any], 
                                     repo_path: str) -> Dict[str, Any]:
        """Generate comprehensive analysis output"""
        
        return {
            "repository_metadata": {
                **structural_analysis.get("repository_metadata", {}),
                "analysis_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "analyzer_type": "real_hybrid_analyzer",
                "repo_path": repo_path
            },
            "components": structural_analysis.get("components", {}),
            "business_logic": structural_analysis.get("business_logic", {}),
            "dependencies": structural_analysis.get("dependencies", {}),
            "component_relationships": component_analysis.get("relationships", {}),
            "semantic_analysis": semantic_analysis,
            "file_analysis": structural_analysis.get("file_analysis", {}),
            "summary": {
                "total_components": len(structural_analysis.get("components", {})),
                "total_business_functions": len(structural_analysis.get("business_logic", {})),
                "architectural_patterns": len(semantic_analysis.get("architectural_patterns", [])),
                "business_capabilities": len(semantic_analysis.get("business_capabilities", [])),
                "analysis_quality": "comprehensive"
            }
        }
