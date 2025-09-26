"""
Workflow Orchestrator for Workflow 1: Code to Design
Coordinates the execution of all agents in the proper sequence
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Type
from datetime import datetime
from pathlib import Path

from .schemas import (
    WorkflowInput, WorkflowOutput, BaseAgentOutput,
    FinalDesignDocument
)
from .tools.llm_client import AG2LLMClient
from .config.settings import OrchestratorConfig

# Import agent output types
from agents.repository_analyzer.schemas import RepositoryAnalysisOutput

# Placeholder imports for agents not yet implemented
# from agents.documentation_synthesizer.schemas import DocumentationSynthesisOutput
# from agents.design_architect.schemas import DesignArchitectOutput
# from agents.test_analyst.schemas import TestAnalysisOutput
# from agents.devops_designer.schemas import DevOpsDesignOutput
# from agents.qa_validator.schemas import QAValidationOutput

# For now, use BaseAgentOutput as placeholder
DocumentationSynthesisOutput = BaseAgentOutput
DesignArchitectOutput = BaseAgentOutput
TestAnalysisOutput = BaseAgentOutput
DevOpsDesignOutput = BaseAgentOutput
QAValidationOutput = BaseAgentOutput


class WorkflowOrchestrator:
    """
    Orchestrates the execution of Workflow 1: Code to Design
    Manages agent execution, data flow, and error handling
    """
    
    def __init__(self, config: Optional[OrchestratorConfig] = None):
        self.config = config or OrchestratorConfig()
        self.logger = logging.getLogger(__name__)
        self.llm_client = AG2LLMClient()
        
        # Agent registry - will be populated by agent imports
        self.agents: Dict[str, Type] = {}
        self.agent_instances: Dict[str, Any] = {}
        
        # Execution state
        self.current_execution_id: Optional[str] = None
        self.execution_start_time: Optional[datetime] = None
        
    def register_agent(self, agent_name: str, agent_class: Type):
        """Register an agent class for execution"""
        self.agents[agent_name] = agent_class
        self.logger.info(f"Registered agent: {agent_name}")
    
    async def execute_workflow(self, workflow_input: WorkflowInput) -> WorkflowOutput:
        """
        Execute the complete Workflow 1: Code to Design
        
        Phase 1: Parallel Analysis (Repository Analyzer, Documentation Synthesizer, Test Analyst, DevOps Designer)
        Phase 2: Design Synthesis (Design Architect)
        Phase 3: Validation & Question Generation (QA Validator)
        """
        self.current_execution_id = workflow_input.execution_id
        self.execution_start_time = datetime.now()
        
        self.logger.info(f"Starting Workflow 1 execution: {workflow_input.execution_id}")
        
        workflow_output = WorkflowOutput(
            workflow_name=workflow_input.workflow_name,
            execution_id=workflow_input.execution_id,
            status="running",
            started_at=self.execution_start_time,
            summary={}
        )
        
        try:
            # Phase 1: Parallel Analysis
            self.logger.info("Phase 1: Starting parallel analysis")
            phase1_outputs = await self._execute_phase1_parallel_analysis(workflow_input)
            
            # Update workflow output with phase 1 results
            workflow_output.repository_analysis = phase1_outputs.get('repository_analyzer')
            workflow_output.documentation_synthesis = phase1_outputs.get('documentation_synthesizer')
            workflow_output.test_analysis = phase1_outputs.get('test_analyst')
            workflow_output.devops_design = phase1_outputs.get('devops_designer')
            
            # Phase 2: Design Synthesis
            self.logger.info("Phase 2: Starting design synthesis")
            design_output = await self._execute_phase2_design_synthesis(
                workflow_input, phase1_outputs
            )
            workflow_output.design_architect = design_output
            
            # Phase 3: Validation & Question Generation
            self.logger.info("Phase 3: Starting validation and question generation")
            validation_output = await self._execute_phase3_validation(
                workflow_input, phase1_outputs, design_output
            )
            workflow_output.qa_validation = validation_output
            
            # Generate final design document
            self.logger.info("Generating final design document")
            final_document = await self._generate_final_document(
                workflow_input, workflow_output
            )
            workflow_output.final_design_document = final_document
            
            # Complete workflow
            workflow_output.status = "completed"
            workflow_output.completed_at = datetime.now()
            workflow_output.total_execution_time = (
                workflow_output.completed_at - workflow_output.started_at
            ).total_seconds()
            
            self.logger.info(f"Workflow 1 completed successfully: {workflow_input.execution_id}")
            
        except Exception as e:
            self.logger.error(f"Workflow 1 failed: {str(e)}", exc_info=True)
            workflow_output.status = "failed"
            workflow_output.errors.append(str(e))
            workflow_output.completed_at = datetime.now()
            if workflow_output.started_at:
                workflow_output.total_execution_time = (
                    workflow_output.completed_at - workflow_output.started_at
                ).total_seconds()
        
        return workflow_output
    
    async def _execute_phase1_parallel_analysis(self, workflow_input: WorkflowInput) -> Dict[str, BaseAgentOutput]:
        """Execute Phase 1: Parallel analysis by all analysis agents"""
        phase1_agents = [
            'repository_analyzer',
            'documentation_synthesizer', 
            'test_analyst',
            'devops_designer'
        ]
        
        # Create tasks for parallel execution
        tasks = []
        for agent_name in phase1_agents:
            if agent_name in self.agents:
                task = self._execute_agent(agent_name, workflow_input)
                tasks.append((agent_name, task))
            else:
                self.logger.warning(f"Agent {agent_name} not registered, skipping")
        
        # Execute all tasks in parallel
        results = {}
        if tasks:
            task_results = await asyncio.gather(
                *[task for _, task in tasks],
                return_exceptions=True
            )
            
            for (agent_name, _), result in zip(tasks, task_results):
                if isinstance(result, Exception):
                    self.logger.error(f"Agent {agent_name} failed: {str(result)}")
                    results[agent_name] = None
                else:
                    results[agent_name] = result
        
        return results
    
    async def _execute_phase2_design_synthesis(
        self, 
        workflow_input: WorkflowInput, 
        phase1_outputs: Dict[str, BaseAgentOutput]
    ) -> DesignArchitectOutput:
        """Execute Phase 2: Design synthesis by Design Architect agent"""
        if 'design_architect' not in self.agents:
            raise ValueError("Design Architect agent not registered")
        
        # Prepare inputs for design architect
        design_input = {
            'workflow_input': workflow_input,
            'repository_analysis': phase1_outputs.get('repository_analyzer'),
            'documentation_synthesis': phase1_outputs.get('documentation_synthesizer'),
            'test_analysis': phase1_outputs.get('test_analyst'),
            'devops_design': phase1_outputs.get('devops_designer')
        }
        
        return await self._execute_agent('design_architect', design_input)
    
    async def _execute_phase3_validation(
        self,
        workflow_input: WorkflowInput,
        phase1_outputs: Dict[str, BaseAgentOutput],
        design_output: DesignArchitectOutput
    ) -> QAValidationOutput:
        """Execute Phase 3: Validation and question generation by QA Validator agent"""
        if 'qa_validator' not in self.agents:
            raise ValueError("QA Validator agent not registered")
        
        # Prepare inputs for QA validator
        validation_input = {
            'workflow_input': workflow_input,
            'repository_analysis': phase1_outputs.get('repository_analyzer'),
            'documentation_synthesis': phase1_outputs.get('documentation_synthesizer'),
            'test_analysis': phase1_outputs.get('test_analyst'),
            'devops_design': phase1_outputs.get('devops_designer'),
            'design_architect': design_output
        }
        
        return await self._execute_agent('qa_validator', validation_input)
    
    async def _execute_agent(self, agent_name: str, input_data: Any) -> BaseAgentOutput:
        """Execute a single agent with the given input data"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not registered")
        
        agent_class = self.agents[agent_name]
        
        # Create agent instance if not exists
        if agent_name not in self.agent_instances:
            self.agent_instances[agent_name] = agent_class()
        
        agent_instance = self.agent_instances[agent_name]
        
        self.logger.info(f"Executing agent: {agent_name}")
        start_time = datetime.now()
        
        try:
            # Execute agent
            result = await agent_instance.execute(input_data)
            
            # Add execution metadata
            if hasattr(result, 'execution_time_seconds'):
                result.execution_time_seconds = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"Agent {agent_name} completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Agent {agent_name} failed: {str(e)}", exc_info=True)
            # Create error output
            error_output = BaseAgentOutput(
                agent_name=agent_name,
                execution_id=self.current_execution_id,
                status="failed",
                error_message=str(e),
                execution_time_seconds=(datetime.now() - start_time).total_seconds()
            )
            return error_output
    
    async def _generate_final_document(
        self,
        workflow_input: WorkflowInput,
        workflow_output: WorkflowOutput
    ) -> FinalDesignDocument:
        """Generate the final comprehensive design document"""
        
        # Calculate overall confidence score
        confidence_scores = []
        if workflow_output.qa_validation and hasattr(workflow_output.qa_validation, 'confidence_scores'):
            confidence_scores.extend(workflow_output.qa_validation.confidence_scores.values())
        
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        # Collect agent outputs
        agent_outputs = {}
        for field_name, output in [
            ('repository_analysis', workflow_output.repository_analysis),
            ('documentation_synthesis', workflow_output.documentation_synthesis),
            ('design_architect', workflow_output.design_architect),
            ('test_analysis', workflow_output.test_analysis),
            ('devops_design', workflow_output.devops_design),
            ('qa_validation', workflow_output.qa_validation)
        ]:
            if output:
                agent_outputs[field_name] = output
        
        # Generate document ID
        document_id = f"design_doc_{workflow_input.execution_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return FinalDesignDocument(
            document_id=document_id,
            workflow_execution_id=workflow_input.execution_id,
            executive_summary=self._generate_executive_summary(workflow_output),
            system_overview=workflow_output.design_architect.system_overview if workflow_output.design_architect else "",
            architecture_diagram=workflow_output.design_architect.architecture_diagram if workflow_output.design_architect else "",
            component_specifications=workflow_output.design_architect.component_specifications if workflow_output.design_architect else [],
            api_documentation=workflow_output.design_architect.api_documentation if workflow_output.design_architect else {},
            data_flow_diagrams=workflow_output.design_architect.data_flow_diagrams if workflow_output.design_architect else [],
            code_quality_metrics=workflow_output.repository_analysis.code_quality_metrics if workflow_output.repository_analysis else {},
            test_strategy=workflow_output.test_analysis.proposed_test_strategy if workflow_output.test_analysis else {},
            deployment_architecture=workflow_output.devops_design.deployment_architecture if workflow_output.devops_design else "",
            operational_requirements=workflow_output.devops_design.operational_requirements if workflow_output.devops_design else [],
            documentation_gaps=workflow_output.documentation_synthesis.major_discrepancies if workflow_output.documentation_synthesis else [],
            validation_questions=workflow_output.qa_validation.clarification_questions if workflow_output.qa_validation else [],
            confidence_score=overall_confidence,
            agent_outputs=agent_outputs
        )
    
    def _generate_executive_summary(self, workflow_output: WorkflowOutput) -> str:
        """Generate executive summary from workflow outputs"""
        summary_parts = []
        
        if workflow_output.repository_analysis:
            summary_parts.append("Repository analysis completed successfully.")
        
        if workflow_output.documentation_synthesis:
            accuracy = workflow_output.documentation_synthesis.documentation_accuracy_score
            summary_parts.append(f"Documentation accuracy score: {accuracy:.2f}")
        
        if workflow_output.design_architect:
            summary_parts.append("Comprehensive design documentation generated.")
        
        if workflow_output.qa_validation:
            question_count = len(workflow_output.qa_validation.clarification_questions)
            summary_parts.append(f"Generated {question_count} clarification questions for validation.")
        
        return " ".join(summary_parts) if summary_parts else "Workflow execution completed."