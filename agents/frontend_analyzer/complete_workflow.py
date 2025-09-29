"""
Complete Multi-Agent Workflow
Orchestrates Repository Analyzer, Design Analyzer, and Architect agents
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from autogen import ConversableAgent, LLMConfig

from .enhanced_repository_analyzer import EnhancedRepositoryAnalyzerAgent
from .design_analyzer_agent import DesignAnalyzerAgent
from .architect_agent import ArchitectAgent

logger = logging.getLogger(__name__)

class CompleteWorkflowOrchestrator:
    """Orchestrates the complete multi-agent workflow for frontend analysis and design"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.llm_config = llm_config
        
        # Initialize all agents
        self.repo_analyzer = EnhancedRepositoryAnalyzerAgent(llm_config)
        self.design_analyzer = DesignAnalyzerAgent(llm_config)
        self.architect = ArchitectAgent(llm_config)
        
        self.logger.info("Complete Workflow Orchestrator initialized")
    
    def run_complete_workflow(self, 
                            repo_path: str, 
                            design_doc_path: str, 
                            requirements: str) -> Dict[str, Any]:
        """Run the complete multi-agent workflow"""
        try:
            self.logger.info("Starting complete multi-agent workflow...")
            
            # Phase 1: Repository Analysis
            self.logger.info("Phase 1: Repository Analysis...")
            repo_analysis = self.repo_analyzer.analyze_repository(repo_path)
            
            # Phase 2: Design Analysis
            self.logger.info("Phase 2: Design Analysis...")
            design_analysis = self.design_analyzer.analyze_design_gaps(
                design_doc_path, requirements, repo_analysis
            )
            
            # Phase 3: Requirements Analysis
            self.logger.info("Phase 3: Requirements Analysis...")
            requirements_analysis = self.design_analyzer.generate_requirements_analysis(requirements)
            
            # Phase 4: Implementation Planning
            self.logger.info("Phase 4: Implementation Planning...")
            implementation_plan = self.architect.create_implementation_plan(
                design_analysis, repo_analysis
            )
            
            # Phase 5: Technical Specifications
            self.logger.info("Phase 5: Technical Specifications...")
            technical_specs = self.architect.generate_technical_specifications(
                requirements_analysis.get('features', []),
                repo_analysis
            )
            
            # Phase 6: Generate Final Output
            self.logger.info("Phase 6: Generating final output...")
            final_output = self._generate_final_output(
                repo_analysis, design_analysis, requirements_analysis, 
                implementation_plan, technical_specs
            )
            
            self.logger.info("Complete workflow finished successfully!")
            return final_output
            
        except Exception as e:
            self.logger.error(f"Error in complete workflow: {e}")
            return {"error": str(e)}
    
    def _generate_final_output(self, 
                             repo_analysis: Dict[str, Any], 
                             design_analysis: Dict[str, Any], 
                             requirements_analysis: Dict[str, Any], 
                             implementation_plan: Dict[str, Any], 
                             technical_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final comprehensive output"""
        
        return {
            "workflow_metadata": {
                "timestamp": self._get_timestamp(),
                "workflow_version": "1.0",
                "agents_used": ["Repository Analyzer", "Design Analyzer", "Architect"],
                "status": "completed"
            },
            "repository_analysis": repo_analysis,
            "design_analysis": design_analysis,
            "requirements_analysis": requirements_analysis,
            "implementation_plan": implementation_plan,
            "technical_specifications": technical_specs,
            "summary": {
                "total_gaps_identified": len(design_analysis.get('gaps', [])),
                "critical_gaps": len([g for g in design_analysis.get('gaps', []) if g.get('priority') == 'high']),
                "files_to_modify": len(implementation_plan.get('files_to_modify', [])),
                "files_to_create": len(implementation_plan.get('files_to_create', [])),
                "estimated_effort": self._calculate_estimated_effort(implementation_plan),
                "recommendation": self._generate_recommendation(design_analysis, implementation_plan)
            }
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _calculate_estimated_effort(self, implementation_plan: Dict[str, Any]) -> str:
        """Calculate estimated effort from implementation plan"""
        phases = implementation_plan.get('implementation_phases', [])
        total_effort = 0
        
        for phase in phases:
            effort_str = phase.get('effort', '0 days')
            if 'day' in effort_str:
                try:
                    days = int(effort_str.split()[0])
                    total_effort += days
                except:
                    pass
        
        if total_effort == 0:
            return "Unknown"
        elif total_effort <= 3:
            return f"{total_effort} days (Low)"
        elif total_effort <= 7:
            return f"{total_effort} days (Medium)"
        else:
            return f"{total_effort} days (High)"
    
    def _generate_recommendation(self, 
                               design_analysis: Dict[str, Any], 
                               implementation_plan: Dict[str, Any]) -> str:
        """Generate overall recommendation"""
        critical_gaps = len([g for g in design_analysis.get('gaps', []) if g.get('priority') == 'high'])
        total_gaps = len(design_analysis.get('gaps', []))
        
        if critical_gaps == 0:
            return "No critical gaps identified. Implementation can proceed with normal priority."
        elif critical_gaps <= 2:
            return f"Found {critical_gaps} critical gaps. Address these first before proceeding with other changes."
        else:
            return f"Found {critical_gaps} critical gaps out of {total_gaps} total gaps. Consider breaking down the implementation into smaller phases."
    
    def run_repository_analysis_only(self, repo_path: str) -> Dict[str, Any]:
        """Run only repository analysis (for testing)"""
        try:
            self.logger.info("Running repository analysis only...")
            return self.repo_analyzer.analyze_repository(repo_path)
        except Exception as e:
            self.logger.error(f"Error in repository analysis: {e}")
            return {"error": str(e)}
    
    def run_design_analysis_only(self, 
                               repo_path: str, 
                               design_doc_path: str, 
                               requirements: str) -> Dict[str, Any]:
        """Run only design analysis (for testing)"""
        try:
            self.logger.info("Running design analysis only...")
            
            # First get repository analysis
            repo_analysis = self.repo_analyzer.analyze_repository(repo_path)
            
            # Then run design analysis
            design_analysis = self.design_analyzer.analyze_design_gaps(
                design_doc_path, requirements, repo_analysis
            )
            
            return {
                "repository_analysis": repo_analysis,
                "design_analysis": design_analysis
            }
        except Exception as e:
            self.logger.error(f"Error in design analysis: {e}")
            return {"error": str(e)}
    
    def run_implementation_planning_only(self, 
                                      repo_path: str, 
                                      design_doc_path: str, 
                                      requirements: str) -> Dict[str, Any]:
        """Run only implementation planning (for testing)"""
        try:
            self.logger.info("Running implementation planning only...")
            
            # Get repository analysis
            repo_analysis = self.repo_analyzer.analyze_repository(repo_path)
            
            # Get design analysis
            design_analysis = self.design_analyzer.analyze_design_gaps(
                design_doc_path, requirements, repo_analysis
            )
            
            # Get implementation plan
            implementation_plan = self.architect.create_implementation_plan(
                design_analysis, repo_analysis
            )
            
            return {
                "repository_analysis": repo_analysis,
                "design_analysis": design_analysis,
                "implementation_plan": implementation_plan
            }
        except Exception as e:
            self.logger.error(f"Error in implementation planning: {e}")
            return {"error": str(e)}
