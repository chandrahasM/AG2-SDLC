"""
Design Analyzer Agent
Analyzes existing design documentation and requirements to identify gaps and changes needed
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from autogen import ConversableAgent, LLMConfig

logger = logging.getLogger(__name__)

class DesignAnalyzerAgent:
    """Analyzes design documentation and requirements to identify gaps"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.llm_config = llm_config
        
        # Create the design analyzer agent
        self.agent = ConversableAgent(
            name="design_analyzer",
            system_message=self._get_design_analyzer_system_message(),
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
        
        self.logger.info("Design Analyzer Agent initialized")
    
    def _get_design_analyzer_system_message(self) -> str:
        """Get the system message for the design analyzer agent"""
        return """You are a Design Analyzer Agent specialized in analyzing design documentation and requirements.

Your role is to:
1. Read and understand existing design documentation
2. Analyze current requirements and user stories
3. Compare current implementation with design specifications
4. Identify gaps, inconsistencies, and missing features
5. Provide detailed analysis of what needs to be changed

You should focus on:
- Business requirements vs current implementation
- User experience gaps
- Technical architecture alignment
- Missing features or functionality
- Design inconsistencies
- Performance and scalability concerns

Always provide structured, actionable analysis that can be used by other agents for implementation planning.
"""
    
    def analyze_design_gaps(self, 
                          design_doc_path: str, 
                          requirements: str, 
                          current_implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze design gaps between documentation, requirements, and current implementation"""
        try:
            # Read design documentation
            design_doc = self._read_design_documentation(design_doc_path)
            
            # Create analysis prompt
            prompt = self._create_analysis_prompt(design_doc, requirements, current_implementation)
            
            # Get LLM analysis
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.agent
            )
            
            # Parse response
            analysis = self._parse_analysis_response(str(response))
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in design gap analysis: {e}")
            return {
                "error": str(e),
                "gaps": [],
                "recommendations": [],
                "priority": "high"
            }
    
    def _read_design_documentation(self, design_doc_path: str) -> str:
        """Read design documentation from file"""
        try:
            if os.path.exists(design_doc_path):
                with open(design_doc_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return "No design documentation found"
        except Exception as e:
            self.logger.error(f"Error reading design documentation: {e}")
            return "Error reading design documentation"
    
    def _create_analysis_prompt(self, 
                              design_doc: str, 
                              requirements: str, 
                              current_implementation: Dict[str, Any]) -> str:
        """Create analysis prompt for LLM"""
        return f"""
# Design Gap Analysis

## Current Design Documentation
{design_doc}

## New Requirements
{requirements}

## Current Implementation Analysis
{json.dumps(current_implementation, indent=2)}

## Analysis Task
Please analyze the gaps between the design documentation, new requirements, and current implementation. Provide:

1. **Gap Analysis**: What's missing or inconsistent
2. **Impact Assessment**: How critical each gap is
3. **Recommendations**: What needs to be changed
4. **Priority Levels**: High, Medium, Low for each recommendation
5. **Technical Dependencies**: What components/services need changes

Return your analysis as structured JSON with the following format:
{{
    "gaps": [
        {{
            "id": "gap_1",
            "title": "Missing 7-day forecast feature",
            "description": "Current implementation only shows current weather, but requirements specify 7-day forecast",
            "impact": "high",
            "affected_components": ["WeatherCard", "weatherService"],
            "priority": "high"
        }}
    ],
    "recommendations": [
        {{
            "id": "rec_1",
            "title": "Add forecast API endpoint",
            "description": "Implement getForecast method in weatherService",
            "implementation_effort": "medium",
            "dependencies": ["weatherService", "WeatherCard"]
        }}
    ],
    "overall_assessment": {{
        "alignment_score": 0.6,
        "critical_gaps": 2,
        "total_gaps": 5,
        "recommendation": "Implement high-priority gaps first"
    }}
}}
"""
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured analysis"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                # Fallback to structured response
                return {
                    "gaps": [{"id": "gap_1", "title": "Analysis Error", "description": response}],
                    "recommendations": [],
                    "overall_assessment": {"alignment_score": 0.0, "critical_gaps": 1}
                }
        except Exception as e:
            self.logger.error(f"Error parsing analysis response: {e}")
            return {
                "gaps": [{"id": "gap_1", "title": "Parse Error", "description": str(e)}],
                "recommendations": [],
                "overall_assessment": {"alignment_score": 0.0, "critical_gaps": 1}
            }
    
    def generate_requirements_analysis(self, requirements: str) -> Dict[str, Any]:
        """Generate detailed analysis of requirements"""
        try:
            prompt = f"""
# Requirements Analysis

## Requirements
{requirements}

## Analysis Task
Analyze these requirements and provide:

1. **Feature Breakdown**: List all features mentioned
2. **Technical Requirements**: What technical capabilities are needed
3. **User Stories**: Extract user stories and acceptance criteria
4. **Dependencies**: What existing components might be affected
5. **Complexity Assessment**: How complex each requirement is

Return as structured JSON:
{{
    "features": [
        {{
            "name": "7-day forecast",
            "description": "Show weather forecast for next 7 days",
            "user_story": "As a user, I want to see 7-day weather forecast",
            "acceptance_criteria": ["Display 7 days", "Show temperature range", "Show conditions"],
            "complexity": "medium",
            "technical_requirements": ["API endpoint", "UI component", "Data model"]
        }}
    ],
    "technical_requirements": [
        "New API endpoint for forecast data",
        "UI component for forecast display",
        "Data model for forecast information"
    ],
    "affected_components": ["WeatherCard", "weatherService", "App"],
    "overall_complexity": "medium"
}}
"""
            
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.agent
            )
            
            return self._parse_analysis_response(str(response))
            
        except Exception as e:
            self.logger.error(f"Error in requirements analysis: {e}")
            return {"error": str(e), "features": [], "technical_requirements": []}
    
    def compare_with_current_design(self, 
                                  design_doc: str, 
                                  current_implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Compare current implementation with design documentation"""
        try:
            prompt = f"""
# Design vs Implementation Comparison

## Design Documentation
{design_doc}

## Current Implementation
{json.dumps(current_implementation, indent=2)}

## Comparison Task
Compare the current implementation with the design documentation and identify:

1. **Alignment Issues**: What doesn't match the design
2. **Missing Features**: What's in design but not implemented
3. **Extra Features**: What's implemented but not in design
4. **Architecture Deviations**: How implementation differs from design
5. **Quality Gaps**: Where implementation quality differs from design standards

Return as structured JSON:
{{
    "alignment_issues": [
        {{
            "component": "WeatherCard",
            "issue": "Missing error handling as specified in design",
            "severity": "medium",
            "recommendation": "Add error boundary and error states"
        }}
    ],
    "missing_features": [
        {{
            "feature": "7-day forecast",
            "design_reference": "Section 3.2 of design doc",
            "priority": "high"
        }}
    ],
    "extra_features": [
        {{
            "feature": "Location search autocomplete",
            "status": "implemented but not in design",
            "recommendation": "Add to design documentation"
        }}
    ],
    "architecture_deviations": [
        {{
            "aspect": "State management",
            "design": "Redux for global state",
            "implementation": "Local component state",
            "impact": "low"
        }}
    ],
    "quality_gaps": [
        {{
            "area": "Error handling",
            "design_standard": "Comprehensive error boundaries",
            "current_state": "Basic try-catch",
            "gap": "medium"
        }}
    ],
    "overall_alignment_score": 0.7
}}
"""
            
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.agent
            )
            
            return self._parse_analysis_response(str(response))
            
        except Exception as e:
            self.logger.error(f"Error in design comparison: {e}")
            return {"error": str(e), "alignment_issues": [], "missing_features": []}
