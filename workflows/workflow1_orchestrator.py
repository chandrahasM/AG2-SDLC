"""
Main Workflow 1 Orchestrator
Entry point for executing the Code-to-Design workflow
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.orchestrator import WorkflowOrchestrator
from core.schemas import WorkflowInput, RepositoryConfig, AnalysisConfig, DocumentationConfig
from core.config.settings import load_config, load_environment_config
from agents.repository_analyzer import RepositoryAnalyzerAgent


class Workflow1Orchestrator:
    """
    Main orchestrator for Workflow 1: Code to Design
    
    This class provides the main entry point for executing the workflow
    and coordinates all agents in the proper sequence.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.config = load_config(config_path)
        self.env_config = load_environment_config()
        
        # Initialize orchestrator
        self.orchestrator = WorkflowOrchestrator(self.config.orchestrator)
        
        # Register agents
        self._register_agents()
        
        self.logger.info("Workflow 1 Orchestrator initialized")
    
    def _register_agents(self):
        """Register all agents with the orchestrator"""
        
        # Register Repository Analyzer Agent
        self.orchestrator.register_agent("repository_analyzer", RepositoryAnalyzerAgent)
        
        # TODO: Register other agents as they are implemented
        # self.orchestrator.register_agent("documentation_synthesizer", DocumentationSynthesizerAgent)
        # self.orchestrator.register_agent("design_architect", DesignArchitectAgent)
        # self.orchestrator.register_agent("test_analyst", TestAnalystAgent)
        # self.orchestrator.register_agent("devops_designer", DevOpsDesignerAgent)
        # self.orchestrator.register_agent("qa_validator", QAValidatorAgent)
        
        self.logger.info("All agents registered successfully")
    
    async def execute_workflow(
        self,
        repo_path: str,
        execution_id: Optional[str] = None,
        output_format: str = "markdown",
        include_diagrams: bool = True
    ):
        """
        Execute the complete Workflow 1: Code to Design
        
        Args:
            repo_path: Path to the repository to analyze
            execution_id: Optional execution ID (generated if not provided)
            output_format: Output format for generated documents
            include_diagrams: Whether to include diagrams in output
            
        Returns:
            WorkflowOutput with complete analysis results
        """
        if not execution_id:
            from datetime import datetime
            execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info(f"Starting Workflow 1 execution: {execution_id}")
        self.logger.info(f"Repository path: {repo_path}")
        
        # Create workflow input
        workflow_input = WorkflowInput(
            workflow_name="code-to-design",
            execution_id=execution_id,
            repository=RepositoryConfig(
                local_path=repo_path,
                file_patterns=self.config.repository_analyzer.parameters.get("file_patterns", [
                    "*.py", "*.java", "*.js", "*.ts", "*.md", "*.json", "*.yaml", "*.yml"
                ]),
                exclude_patterns=self.config.repository_analyzer.parameters.get("exclude_patterns", [
                    "**/node_modules/**", "**/__pycache__/**", "**/.git/**", "**/venv/**", "**/env/**"
                ]),
                max_file_size_mb=self.config.repository_analyzer.max_file_size_mb,
                depth_level=10
            ),
            analysis=AnalysisConfig(
                focus_areas=["architecture", "dependencies", "patterns", "quality", "testing"],
                include_comments=self.config.repository_analyzer.include_comments,
                include_docstrings=self.config.repository_analyzer.include_docstrings,
                analyze_test_files=self.config.repository_analyzer.analyze_test_files,
                generate_metrics=self.config.repository_analyzer.generate_metrics,
                language_specific=self.config.repository_analyzer.language_specific
            ),
            documentation=DocumentationConfig(
                design_docs_path=None,  # Will be set if provided
                requirements_docs_path=None,  # Will be set if provided
                include_markdown=True,
                include_confluence=False,
                include_notion=False
            ),
            output_format=output_format,
            include_diagrams=include_diagrams,
            parallel_execution=self.config.orchestrator.max_parallel_agents > 1
        )
        
        # Execute workflow
        try:
            workflow_output = await self.orchestrator.execute_workflow(workflow_input)
            
            # Save results
            await self._save_results(workflow_output)
            
            self.logger.info(f"Workflow 1 completed successfully: {execution_id}")
            return workflow_output
            
        except Exception as e:
            self.logger.error(f"Workflow 1 failed: {str(e)}", exc_info=True)
            raise
    
    async def _save_results(self, workflow_output):
        """Save workflow results to output directory"""
        output_dir = Path(self.config.orchestrator.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save final output
        final_output_path = output_dir / "final" / f"{workflow_output.execution_id}_final_output.json"
        final_output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(final_output_path, 'w', encoding='utf-8') as f:
            f.write(workflow_output.model_dump_json(indent=2))
        
        self.logger.info(f"Results saved to: {final_output_path}")
    
    def run_sync(
        self,
        repo_path: str,
        execution_id: Optional[str] = None,
        output_format: str = "markdown",
        include_diagrams: bool = True
    ):
        """
        Synchronous wrapper for execute_workflow
        
        Args:
            repo_path: Path to the repository to analyze
            execution_id: Optional execution ID (generated if not provided)
            output_format: Output format for generated documents
            include_diagrams: Whether to include diagrams in output
            
        Returns:
            WorkflowOutput with complete analysis results
        """
        return asyncio.run(self.execute_workflow(
            repo_path=repo_path,
            execution_id=execution_id,
            output_format=output_format,
            include_diagrams=include_diagrams
        ))


async def main():
    """Main entry point for command-line execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Workflow 1: Code to Design")
    parser.add_argument("repo_path", help="Path to the repository to analyze")
    parser.add_argument("--execution-id", help="Execution ID (optional)")
    parser.add_argument("--output-format", default="markdown", choices=["markdown", "json", "html"],
                       help="Output format for generated documents")
    parser.add_argument("--no-diagrams", action="store_true", help="Exclude diagrams from output")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize and run orchestrator
    orchestrator = Workflow1Orchestrator(args.config)
    
    try:
        result = await orchestrator.execute_workflow(
            repo_path=args.repo_path,
            execution_id=args.execution_id,
            output_format=args.output_format,
            include_diagrams=not args.no_diagrams
        )
        
        print(f"Workflow completed successfully!")
        print(f"Execution ID: {result.execution_id}")
        print(f"Status: {result.status}")
        print(f"Execution time: {result.total_execution_time:.2f} seconds")
        
        if result.final_design_document:
            print(f"Final document ID: {result.final_design_document.document_id}")
            print(f"Confidence score: {result.final_design_document.confidence_score:.2f}")
        
        return result
        
    except Exception as e:
        print(f"Workflow failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())