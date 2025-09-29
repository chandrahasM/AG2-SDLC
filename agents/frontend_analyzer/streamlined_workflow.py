"""
Working Streamlined Multi-Agent Workflow
Integrates with existing real analyzers and provides actual functionality
"""

import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List
from autogen import ConversableAgent, LLMConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamlinedWorkflow:
    """
    Working streamlined workflow that integrates with existing real analyzers
    """
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.llm_config = llm_config
        self.output_dir = Path("data/outputs/streamlined_workflow")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Streamlined Workflow initialized")
    
    def run_complete_workflow(self, repo_path: str, design_doc_path: str, requirements: str) -> Dict[str, Any]:
        """Run the complete streamlined workflow with real analyzers"""
        
        self.logger.info("🚀 Starting Streamlined Multi-Agent Workflow")
        self.logger.info(f"📁 Repository: {repo_path}")
        self.logger.info(f"📄 Design Doc: {design_doc_path}")
        self.logger.info(f"📋 Requirements: {requirements[:100]}...")
        
        workflow_start_time = time.time()
        
        try:
            # Phase 1: Repository Analysis (using real analyzer)
            self.logger.info("\n" + "="*60)
            self.logger.info("🔍 PHASE 1: REPOSITORY ANALYSIS")
            self.logger.info("="*60)
            
            repo_analysis = self._run_real_repository_analysis(repo_path)
            self._save_agent_output("repository_analyzer", repo_analysis)
            
            # Phase 2: Design Analysis (using real analyzer)
            self.logger.info("\n" + "="*60)
            self.logger.info("📋 PHASE 2: DESIGN ANALYSIS")
            self.logger.info("="*60)
            
            design_analysis = self._run_real_design_analysis(design_doc_path, requirements, repo_analysis)
            self._save_agent_output("design_analyzer", design_analysis)
            
            # Phase 3: Architect Planning (using real analyzer)
            self.logger.info("\n" + "="*60)
            self.logger.info("🏗️ PHASE 3: ARCHITECT PLANNING")
            self.logger.info("="*60)
            
            architect_analysis = self._run_real_architect_analysis(repo_analysis, design_analysis)
            self._save_agent_output("architect", architect_analysis)
            
            # Phase 4: Code Generation (using real analyzer)
            self.logger.info("\n" + "="*60)
            self.logger.info("💻 PHASE 4: CODE GENERATION")
            self.logger.info("="*60)
            
            code_generation = self._run_real_code_generation(repo_path, architect_analysis)
            self._save_agent_output("code_generator", code_generation)
            
            # Generate final workflow summary
            workflow_end_time = time.time()
            total_duration = workflow_end_time - workflow_start_time
            
            final_output = {
                "workflow_metadata": {
                    "status": "completed",
                    "total_duration_seconds": total_duration,
                    "agents_used": ["repository_analyzer", "design_analyzer", "architect", "code_generator"],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "repo_path": repo_path,
                    "design_doc_path": design_doc_path
                },
                "agent_outputs": {
                    "repository_analyzer": repo_analysis,
                    "design_analyzer": design_analysis,
                    "architect": architect_analysis,
                    "code_generator": code_generation
                },
                "summary": {
                    "total_files_analyzed": repo_analysis.get("repository_metadata", {}).get("total_files", 0),
                    "gaps_identified": len(design_analysis.get("gaps", [])),
                    "files_to_modify": len(architect_analysis.get("files_to_modify", [])),
                    "files_to_create": len(architect_analysis.get("files_to_create", [])),
                    "code_changes_applied": code_generation.get("changes_applied", 0),
                    "errors_fixed": code_generation.get("errors_fixed", 0)
                }
            }
            
            # Save final workflow output
            self._save_workflow_output(final_output)
            
            self.logger.info(f"\n✅ Streamlined workflow completed in {total_duration:.2f} seconds")
            self._print_workflow_summary(final_output)
            
            return final_output
            
        except Exception as e:
            self.logger.error(f"❌ Workflow failed: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def _run_real_repository_analysis(self, repo_path: str) -> Dict[str, Any]:
        """Run real repository analysis using existing analyzer"""
        
        self.logger.info("🔍 Running real repository analysis...")
        
        try:
            # Import and use the real hybrid analyzer
            from agents.frontend_analyzer.real_hybrid_analyzer import RealHybridRepositoryAnalyzerAgent
            
            # Initialize the real analyzer
            analyzer = RealHybridRepositoryAnalyzerAgent(
                model_name="gpt-4o-mini",
                temperature=0.1
            )
            
            # Run the analysis
            result = analyzer.analyze_repository(repo_path)
            
            # Add metadata
            result["agent_metadata"] = {
                "agent_name": "repository_analyzer",
                "phase": "repository_analysis",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "repo_path": repo_path,
                "analyzer_type": "real_hybrid_analyzer"
            }
            
            files_analyzed = result.get("repository_metadata", {}).get("total_files", 0)
            self.logger.info(f"✅ Repository analysis completed - {files_analyzed} files analyzed")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Repository analysis failed: {str(e)}")
            return {
                "error": str(e),
                "agent_metadata": {
                    "agent_name": "repository_analyzer",
                    "phase": "repository_analysis",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "repo_path": repo_path,
                    "analyzer_type": "real_hybrid_analyzer"
                }
            }
    
    def _run_real_design_analysis(self, design_doc_path: str, requirements: str, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run real design analysis using existing analyzer"""
        
        self.logger.info("📋 Running real design analysis...")
        
        try:
            # Import and use the real design analyzer
            from agents.frontend_analyzer.design_analyzer_agent import DesignAnalyzerAgent
            
            # Initialize the real analyzer
            analyzer = DesignAnalyzerAgent(self.llm_config)
            
            # Run the analysis
            result = analyzer.analyze_design_gaps(
                design_doc_path=design_doc_path,
                requirements=requirements,
                current_implementation=repo_analysis
            )
            
            # Add metadata
            result["agent_metadata"] = {
                "agent_name": "design_analyzer",
                "phase": "design_analysis",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "design_doc_path": design_doc_path,
                "analyzer_type": "real_design_analyzer"
            }
            
            gaps_count = len(result.get("gaps", []))
            self.logger.info(f"✅ Design analysis completed - {gaps_count} gaps identified")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Design analysis failed: {str(e)}")
            return {
                "error": str(e),
                "gaps": [],
                "agent_metadata": {
                    "agent_name": "design_analyzer",
                    "phase": "design_analysis",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "design_doc_path": design_doc_path,
                    "analyzer_type": "real_design_analyzer"
                }
            }
    
    def _run_real_architect_analysis(self, repo_analysis: Dict[str, Any], design_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run real architect analysis using existing analyzer"""
        
        self.logger.info("🏗️ Running real architect analysis...")
        
        try:
            # Import and use the real architect agent
            from agents.frontend_analyzer.architect_agent import ArchitectAgent
            
            # Initialize the real analyzer
            analyzer = ArchitectAgent(self.llm_config)
            
            # Run the analysis
            result = analyzer.create_implementation_plan(
                design_analysis=design_analysis,
                repo_analysis=repo_analysis
            )
            
            # Add metadata
            result["agent_metadata"] = {
                "agent_name": "architect",
                "phase": "architect_planning",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "analyzer_type": "real_architect_agent"
            }
            
            files_to_modify = len(result.get("files_to_modify", []))
            files_to_create = len(result.get("files_to_create", []))
            self.logger.info(f"✅ Architect planning completed - {files_to_modify} files to modify, {files_to_create} files to create")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Architect analysis failed: {str(e)}")
            return {
                "error": str(e),
                "implementation_plan": {"files_to_modify": [], "files_to_create": []},
                "agent_metadata": {
                    "agent_name": "architect",
                    "phase": "architect_planning",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "analyzer_type": "real_architect_agent"
                }
            }
    
    def _run_real_code_generation(self, repo_path: str, architect_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run real code generation using existing analyzer"""
        
        self.logger.info("💻 Running real code generation...")
        
        try:
            # Import and use the real code generation agent
            from agents.frontend_analyzer.smart_code_generation_agent import SmartCodeGenerationAgent
            
            # Initialize the real analyzer
            analyzer = SmartCodeGenerationAgent(self.llm_config, repo_path)
            
            # Create workflow results for the code generator
            workflow_results = {
                "architect_agent_output": architect_analysis,
                "supporting_analysis": {
                    "repository_analysis": {},
                    "design_analysis": {}
                }
            }
            
            # Run the analysis
            result = analyzer.generate_code_changes(workflow_results)
            
            # Add metadata
            result["agent_metadata"] = {
                "agent_name": "code_generator",
                "phase": "code_generation",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "repo_path": repo_path,
                "analyzer_type": "real_code_generation_agent"
            }
            
            changes_applied = result.get("changes_applied", 0)
            errors_fixed = result.get("errors_fixed", 0)
            self.logger.info(f"✅ Code generation completed - {changes_applied} changes applied, {errors_fixed} errors fixed")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Code generation failed: {str(e)}")
            return {
                "error": str(e),
                "changes_applied": 0,
                "errors_fixed": 0,
                "agent_metadata": {
                    "agent_name": "code_generator",
                    "phase": "code_generation",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "repo_path": repo_path,
                    "analyzer_type": "real_code_generation_agent"
                }
            }
    
    def _save_agent_output(self, agent_name: str, output: Dict[str, Any]):
        """Save individual agent output to JSON file"""
        
        output_file = self.output_dir / f"{agent_name}_output.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"💾 {agent_name} output saved to: {output_file}")
    
    def _save_workflow_output(self, workflow_output: Dict[str, Any]):
        """Save complete workflow output"""
        
        # Save full output
        full_output_file = self.output_dir / "complete_workflow_output.json"
        with open(full_output_file, 'w', encoding='utf-8') as f:
            json.dump(workflow_output, f, indent=2, ensure_ascii=False)
        
        # Save compact output for LLM consumption
        compact_output = self._create_compact_output(workflow_output)
        compact_output_file = self.output_dir / "compact_workflow_output.json"
        with open(compact_output_file, 'w', encoding='utf-8') as f:
            json.dump(compact_output, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"💾 Complete workflow output saved to: {full_output_file}")
        self.logger.info(f"💾 Compact workflow output saved to: {compact_output_file}")
    
    def _create_compact_output(self, workflow_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create compact output for LLM consumption"""
        
        agent_outputs = workflow_output.get("agent_outputs", {})
        summary = workflow_output.get("summary", {})
        
        return {
            "workflow_summary": {
                "status": workflow_output.get("workflow_metadata", {}).get("status", "unknown"),
                "duration_seconds": workflow_output.get("workflow_metadata", {}).get("total_duration_seconds", 0),
                "agents_used": workflow_output.get("workflow_metadata", {}).get("agents_used", [])
            },
            "repository_analysis_summary": {
                "total_files": summary.get("total_files_analyzed", 0),
                "components_found": len(agent_outputs.get("repository_analyzer", {}).get("components", {})),
                "services_found": len(agent_outputs.get("repository_analyzer", {}).get("business_logic", {})),
                "business_capabilities": len(agent_outputs.get("repository_analyzer", {}).get("business_capabilities", []))
            },
            "design_analysis_summary": {
                "gaps_identified": summary.get("gaps_identified", 0),
                "critical_gaps": len([g for g in agent_outputs.get("design_analyzer", {}).get("gaps", []) if g.get("priority") == "high"]),
                "gaps": agent_outputs.get("design_analyzer", {}).get("gaps", [])[:5]
            },
            "architect_plan_summary": {
                "files_to_modify": summary.get("files_to_modify", 0),
                "files_to_create": summary.get("files_to_create", 0),
                "implementation_phases": len(agent_outputs.get("architect", {}).get("implementation_plan", {}).get("implementation_phases", [])),
                "risks_identified": len(agent_outputs.get("architect", {}).get("risk_assessment", []))
            },
            "code_generation_summary": {
                "changes_applied": summary.get("code_changes_applied", 0),
                "errors_fixed": summary.get("errors_fixed", 0),
                "files_modified": len(agent_outputs.get("code_generator", {}).get("files_modified", [])),
                "files_created": len(agent_outputs.get("code_generator", {}).get("files_created", []))
            }
        }
    
    def _print_workflow_summary(self, workflow_output: Dict[str, Any]):
        """Print workflow summary"""
        
        print("\n" + "="*80)
        print("🎯 STREAMLINED WORKFLOW SUMMARY")
        print("="*80)
        
        metadata = workflow_output.get("workflow_metadata", {})
        summary = workflow_output.get("summary", {})
        
        print(f"Status: {metadata.get('status', 'Unknown')}")
        print(f"Duration: {metadata.get('total_duration_seconds', 0):.2f} seconds")
        print(f"Agents Used: {', '.join(metadata.get('agents_used', []))}")
        
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"  Files Analyzed: {summary.get('total_files_analyzed', 0)}")
        print(f"  Gaps Identified: {summary.get('gaps_identified', 0)}")
        print(f"  Files to Modify: {summary.get('files_to_modify', 0)}")
        print(f"  Files to Create: {summary.get('files_to_create', 0)}")
        print(f"  Changes Applied: {summary.get('code_changes_applied', 0)}")
        print(f"  Errors Fixed: {summary.get('errors_fixed', 0)}")
        
        print(f"\n📁 OUTPUT FILES:")
        print(f"  Repository Analyzer: {self.output_dir}/repository_analyzer_output.json")
        print(f"  Design Analyzer: {self.output_dir}/design_analyzer_output.json")
        print(f"  Architect: {self.output_dir}/architect_output.json")
        print(f"  Code Generator: {self.output_dir}/code_generator_output.json")
        print(f"  Complete Workflow: {self.output_dir}/complete_workflow_output.json")
        print(f"  Compact Summary: {self.output_dir}/compact_workflow_output.json")
        
        print("="*80)
