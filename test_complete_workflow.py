"""
Test script for the complete multi-agent workflow
Tests Repository Analyzer, Design Analyzer, and Architect agents
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_complete_workflow():
    """Test the complete multi-agent workflow"""
    try:
        # Import the workflow orchestrator
        from agents.frontend_analyzer.complete_workflow import CompleteWorkflowOrchestrator
        
        # Set up LLM configuration
        llm_config = {
            "config_list": [{
                "model": "gpt-4o-mini",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "temperature": 0.1
            }],
            "timeout": 120
        }
        
        # Initialize workflow orchestrator
        orchestrator = CompleteWorkflowOrchestrator(llm_config)
        
        # Define test parameters
        repo_path = "data/inputs/sample_repositories/react_weather_app"
        design_doc_path = "data/inputs/sample_repositories/react_weather_app/design-document.md"
        requirements = """
        Add 7-day weather forecast functionality to the weather app:
        
        1. User should be able to see weather forecast for the next 7 days
        2. Each day should show: date, high/low temperature, weather condition, and icon
        3. Forecast should be displayed in a card format below the current weather
        4. User should be able to refresh the forecast data
        5. Error handling should be implemented for forecast API failures
        6. Loading states should be shown while fetching forecast data
        
        Technical Requirements:
        - Use the existing weather service architecture
        - Maintain consistent UI/UX with current design
        - Ensure mobile responsiveness
        - Implement proper error boundaries
        """
        
        logger.info("Starting complete workflow test...")
        logger.info(f"Repository: {repo_path}")
        logger.info(f"Design Doc: {design_doc_path}")
        logger.info(f"Requirements: {requirements[:100]}...")
        
        # Run the complete workflow
        result = orchestrator.run_complete_workflow(
            repo_path=repo_path,
            design_doc_path=design_doc_path,
            requirements=requirements
        )
        
        # Save results
        output_dir = Path("data/outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Save full results
        with open(output_dir / "complete_workflow_results.json", "w") as f:
            json.dump(result, f, indent=2)
        
        # Save compact results for LLM consumption
        compact_result = create_compact_output(result)
        with open(output_dir / "complete_workflow_compact.json", "w") as f:
            json.dump(compact_result, f, indent=2)
        
        logger.info("Complete workflow test completed!")
        logger.info(f"Full results saved to: {output_dir / 'complete_workflow_results.json'}")
        logger.info(f"Compact results saved to: {output_dir / 'complete_workflow_compact.json'}")
        
        # Print summary
        print_summary(result)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in complete workflow test: {e}")
        return {"error": str(e)}

def test_repository_analysis_only():
    """Test only the repository analysis"""
    try:
        from agents.frontend_analyzer.complete_workflow import CompleteWorkflowOrchestrator
        
        llm_config = {
            "config_list": [{
                "model": "gpt-4o-mini",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "temperature": 0.1
            }],
            "timeout": 120
        }
        
        orchestrator = CompleteWorkflowOrchestrator(llm_config)
        repo_path = "data/inputs/sample_repositories/react_weather_app"
        
        logger.info("Testing repository analysis only...")
        result = orchestrator.run_repository_analysis_only(repo_path)
        
        # Save results
        output_dir = Path("data/outputs")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "repo_analysis_only.json", "w") as f:
            json.dump(result, f, indent=2)
        
        logger.info("Repository analysis test completed!")
        return result
        
    except Exception as e:
        logger.error(f"Error in repository analysis test: {e}")
        return {"error": str(e)}

def create_compact_output(result: dict) -> dict:
    """Create a compact output for LLM consumption"""
    try:
        # Extract key information
        repo_analysis = result.get("repository_analysis", {})
        design_analysis = result.get("design_analysis", {})
        implementation_plan = result.get("implementation_plan", {})
        
        compact = {
            "workflow_summary": {
                "status": result.get("workflow_metadata", {}).get("status", "unknown"),
                "agents_used": result.get("workflow_metadata", {}).get("agents_used", []),
                "timestamp": result.get("workflow_metadata", {}).get("timestamp", "")
            },
            "repository_summary": {
                "total_files": repo_analysis.get("repository_metadata", {}).get("total_files", 0),
                "components": repo_analysis.get("components", {}),
                "services": repo_analysis.get("business_logic", {}),
                "dependencies": repo_analysis.get("dependencies", {})
            },
            "design_gaps": {
                "total_gaps": len(design_analysis.get("gaps", [])),
                "critical_gaps": len([g for g in design_analysis.get("gaps", []) if g.get("priority") == "high"]),
                "gaps": design_analysis.get("gaps", [])[:5]  # Top 5 gaps
            },
            "implementation_plan": {
                "phases": implementation_plan.get("implementation_phases", [])[:3],  # Top 3 phases
                "files_to_modify": implementation_plan.get("files_to_modify", [])[:5],  # Top 5 files
                "files_to_create": implementation_plan.get("files_to_create", [])[:3],  # Top 3 new files
                "implementation_order": implementation_plan.get("implementation_order", [])[:5]  # Top 5 steps
            },
            "summary": result.get("summary", {})
        }
        
        return compact
        
    except Exception as e:
        logger.error(f"Error creating compact output: {e}")
        return {"error": str(e)}

def print_summary(result: dict):
    """Print a summary of the results"""
    try:
        print("\n" + "="*80)
        print("COMPLETE WORKFLOW TEST RESULTS SUMMARY")
        print("="*80)
        
        # Workflow metadata
        workflow_meta = result.get("workflow_metadata", {})
        print(f"Status: {workflow_meta.get('status', 'Unknown')}")
        print(f"Agents Used: {', '.join(workflow_meta.get('agents_used', []))}")
        
        # Repository analysis
        repo_meta = result.get("repository_analysis", {}).get("repository_metadata", {})
        print(f"\nRepository Analysis:")
        print(f"  Total Files: {repo_meta.get('total_files', 0)}")
        print(f"  File Types: {repo_meta.get('file_types', {})}")
        
        # Design analysis
        design_analysis = result.get("design_analysis", {})
        gaps = design_analysis.get("gaps", [])
        print(f"\nDesign Analysis:")
        print(f"  Total Gaps: {len(gaps)}")
        print(f"  Critical Gaps: {len([g for g in gaps if g.get('priority') == 'high'])}")
        
        # Implementation plan
        impl_plan = result.get("implementation_plan", {})
        phases = impl_plan.get("implementation_phases", [])
        files_to_modify = impl_plan.get("files_to_modify", [])
        files_to_create = impl_plan.get("files_to_create", [])
        
        print(f"\nImplementation Plan:")
        print(f"  Phases: {len(phases)}")
        print(f"  Files to Modify: {len(files_to_modify)}")
        print(f"  Files to Create: {len(files_to_create)}")
        
        # Summary
        summary = result.get("summary", {})
        print(f"\nSummary:")
        print(f"  Estimated Effort: {summary.get('estimated_effort', 'Unknown')}")
        print(f"  Recommendation: {summary.get('recommendation', 'No recommendation')}")
        
        print("="*80)
        
    except Exception as e:
        logger.error(f"Error printing summary: {e}")

if __name__ == "__main__":
    # Test the complete workflow
    print("Testing complete multi-agent workflow...")
    result = test_complete_workflow()
    
    if "error" in result:
        print(f"Test failed with error: {result['error']}")
    else:
        print("Test completed successfully!")
