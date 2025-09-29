"""
Architect Agent
Takes design analysis and repository analysis to create detailed implementation plans
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from autogen import ConversableAgent, LLMConfig

logger = logging.getLogger(__name__)

class ArchitectAgent:
    """Creates detailed implementation plans based on design and repository analysis"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.llm_config = llm_config
        
        # Create the architect agent
        self.agent = ConversableAgent(
            name="architect",
            system_message=self._get_architect_system_message(),
            llm_config=llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5
        )
        
        self.logger.info("Architect Agent initialized")
    
    def _get_architect_system_message(self) -> str:
        """Get the system message for the architect agent"""
        return """You are an Architect Agent specialized in creating detailed implementation plans.

Your role is to:
1. Analyze design gaps and requirements
2. Review current codebase structure and capabilities
3. Create detailed technical implementation plans
4. Specify which files need to be modified/created
5. Provide step-by-step implementation guidance
6. Identify dependencies and implementation order
7. Estimate effort and complexity for each task

You should focus on:
- Technical feasibility of proposed changes
- Code structure and architecture decisions
- File-by-file implementation plan
- Dependencies between changes
- Testing and validation requirements
- Risk assessment and mitigation

Always provide actionable, detailed implementation plans that developers can follow.
"""
    
    def create_implementation_plan(self, 
                                 design_analysis: Dict[str, Any], 
                                 repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed implementation plan based on design and repo analysis"""
        try:
            # Create implementation planning prompt
            prompt = self._create_implementation_prompt(design_analysis, repo_analysis)
            
            # Get LLM analysis
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.agent
            )
            
            # Parse response
            plan = self._parse_implementation_response(str(response))
            
            return plan
            
        except Exception as e:
            self.logger.error(f"Error creating implementation plan: {e}")
            return {
                "error": str(e),
                "phases": [],
                "files_to_modify": [],
                "files_to_create": [],
                "implementation_order": []
            }
    
    def _create_implementation_prompt(self, 
                                    design_analysis: Dict[str, Any], 
                                    repo_analysis: Dict[str, Any]) -> str:
        """Create implementation planning prompt for LLM"""
        return f"""
# Implementation Planning

## Design Analysis Results
{json.dumps(design_analysis, indent=2)}

## Current Repository Analysis
{json.dumps(repo_analysis, indent=2)}

## Implementation Planning Task
Based on the design gaps and current codebase, create a detailed implementation plan that includes:

1. **Implementation Phases**: Break down work into logical phases
2. **File Modifications**: Which existing files need changes
3. **New Files**: What new files need to be created
4. **Code Changes**: Specific code changes needed
5. **Dependencies**: What depends on what
6. **Testing Strategy**: How to test the changes
7. **Risk Assessment**: Potential risks and mitigation

Return as structured JSON:
{{
    "implementation_phases": [
        {{
            "phase": "Phase 1: Service Layer Enhancement",
            "description": "Add forecast functionality to weather service",
            "effort": "2-3 days",
            "priority": "high",
            "dependencies": []
        }}
    ],
    "files_to_modify": [
        {{
            "file": "src/services/weatherService.ts",
            "changes": [
                "Add getForecast method",
                "Add ForecastData interface",
                "Update error handling"
            ],
            "effort": "1 day",
            "complexity": "medium"
        }}
    ],
    "files_to_create": [
        {{
            "file": "src/components/ForecastCard.tsx",
            "purpose": "Display 7-day weather forecast",
            "dependencies": ["weatherService", "WeatherData interface"],
            "effort": "2 days",
            "complexity": "medium"
        }}
    ],
    "implementation_order": [
        "1. Update weatherService.ts with forecast methods",
        "2. Create ForecastCard component",
        "3. Update App.tsx to include forecast",
        "4. Add error handling and loading states",
        "5. Test integration"
    ],
    "testing_strategy": [
        "Unit tests for new service methods",
        "Component tests for ForecastCard",
        "Integration tests for forecast flow",
        "E2E tests for complete user journey"
    ],
    "risk_assessment": [
        {{
            "risk": "API rate limiting",
            "probability": "medium",
            "impact": "high",
            "mitigation": "Implement caching and request throttling"
        }}
    ],
    "success_criteria": [
        "7-day forecast displays correctly",
        "Error states handled gracefully",
        "Performance remains acceptable",
        "All tests pass"
    ]
}}
"""
    
    def _parse_implementation_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured implementation plan"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                # Fallback to structured response
                return {
                    "implementation_phases": [{"phase": "Parse Error", "description": response}],
                    "files_to_modify": [],
                    "files_to_create": [],
                    "implementation_order": []
                }
        except Exception as e:
            self.logger.error(f"Error parsing implementation response: {e}")
            return {
                "implementation_phases": [{"phase": "Parse Error", "description": str(e)}],
                "files_to_modify": [],
                "files_to_create": [],
                "implementation_order": []
            }
    
    def generate_technical_specifications(self, 
                                        requirements: List[str], 
                                        current_architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed technical specifications for implementation"""
        try:
            prompt = f"""
# Technical Specifications Generation

## Requirements
{json.dumps(requirements, indent=2)}

## Current Architecture
{json.dumps(current_architecture, indent=2)}

## Technical Specifications Task
Generate detailed technical specifications including:

1. **API Specifications**: New endpoints and data models
2. **Component Specifications**: New components and their interfaces
3. **State Management**: How state will be managed
4. **Data Flow**: How data flows through the system
5. **Error Handling**: Error handling strategy
6. **Performance Requirements**: Performance considerations
7. **Security Considerations**: Security requirements

Return as structured JSON:
{{
    "api_specifications": [
        {{
            "endpoint": "GET /api/forecast",
            "parameters": ["location", "days"],
            "response": "ForecastData[]",
            "error_codes": ["400", "404", "500"],
            "rate_limit": "100 requests/hour"
        }}
    ],
    "component_specifications": [
        {{
            "name": "ForecastCard",
            "props": ["forecastData", "onError", "loading"],
            "state": ["isLoading", "error"],
            "methods": ["handleRefresh", "handleError"],
            "dependencies": ["weatherService", "ErrorBoundary"]
        }}
    ],
    "state_management": {{
        "global_state": "None - using local component state",
        "local_state": ["forecastData", "loading", "error"],
        "state_updates": "Via weatherService calls and component state"
    }},
    "data_flow": [
        "User requests forecast -> App component -> weatherService.getForecast() -> API call -> ForecastCard display"
    ],
    "error_handling": {{
        "strategy": "Error boundaries + try-catch in service calls",
        "user_feedback": "Error messages in UI",
        "logging": "Console errors for debugging"
    }},
    "performance_requirements": {{
        "load_time": "< 2 seconds for forecast data",
        "caching": "Cache forecast data for 1 hour",
        "optimization": "Lazy load forecast component"
    }},
    "security_considerations": [
        "Validate location input",
        "Sanitize API responses",
        "Rate limit API calls"
    ]
}}
"""
            
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.agent
            )
            
            return self._parse_implementation_response(str(response))
            
        except Exception as e:
            self.logger.error(f"Error generating technical specifications: {e}")
            return {"error": str(e), "api_specifications": [], "component_specifications": []}
    
    def create_code_change_specifications(self, 
                                        file_path: str, 
                                        current_code: str, 
                                        required_changes: List[str]) -> Dict[str, Any]:
        """Create detailed specifications for code changes to a specific file"""
        try:
            prompt = f"""
# Code Change Specifications

## File: {file_path}

## Current Code
```typescript
{current_code}
```

## Required Changes
{json.dumps(required_changes, indent=2)}

## Code Change Task
Create detailed specifications for implementing these changes:

1. **Exact Code Changes**: Show exactly what to add/modify/remove
2. **Line Numbers**: Where to make changes
3. **Dependencies**: What imports or dependencies are needed
4. **Testing**: How to test the changes
5. **Validation**: How to validate the changes work

Return as structured JSON:
{{
    "file_path": "{file_path}",
    "changes": [
        {{
            "type": "add",
            "line_number": 15,
            "code": "async getForecast(location: string, days: number = 7): Promise<ForecastData[]> {{",
            "description": "Add getForecast method to WeatherService class"
        }},
        {{
            "type": "modify",
            "line_number": 5,
            "old_code": "import {{ WeatherData }} from '../types/weather';",
            "new_code": "import {{ WeatherData, ForecastData }} from '../types/weather';",
            "description": "Add ForecastData import"
        }}
    ],
    "imports_to_add": [
        "import {{ ForecastData }} from '../types/weather';"
    ],
    "dependencies": [
        "ForecastData interface must be defined in types/weather.ts"
    ],
    "testing_instructions": [
        "Test getForecast method with valid location",
        "Test error handling with invalid location",
        "Test with different day counts"
    ],
    "validation_criteria": [
        "Method returns Promise<ForecastData[]>",
        "Handles errors gracefully",
        "Validates input parameters"
    ]
}}
"""
            
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}],
                sender=self.agent
            )
            
            return self._parse_implementation_response(str(response))
            
        except Exception as e:
            self.logger.error(f"Error creating code change specifications: {e}")
            return {"error": str(e), "changes": [], "imports_to_add": []}
