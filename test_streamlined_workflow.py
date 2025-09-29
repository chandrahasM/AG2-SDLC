"""
Test script for Working Streamlined Multi-Agent Workflow
Uses real analyzers and provides actual functionality
"""

import os
import json
import logging
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_working_streamlined_workflow():
    """Test the working streamlined multi-agent workflow"""
    try:
        # Import the working streamlined workflow
        from agents.frontend_analyzer.streamlined_workflow import StreamlinedWorkflow
        
        # Set up LLM configuration
        llm_config = {
            "config_list": [{
                "model": "gpt-4o-mini",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "temperature": 0.1
            }],
            "timeout": 300
        }
        
        # Initialize streamlined workflow
        workflow = StreamlinedWorkflow(llm_config)
        
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
        
        logger.info("🚀 Starting Streamlined Multi-Agent Workflow Test")
        logger.info(f"📁 Repository: {repo_path}")
        logger.info(f"📄 Design Doc: {design_doc_path}")
        logger.info(f"📋 Requirements: {requirements[:100]}...")
        
        # Record start time
        start_time = time.time()
        
        # Run the complete working streamlined workflow
        result = workflow.run_complete_workflow(
            repo_path=repo_path,
            design_doc_path=design_doc_path,
            requirements=requirements
        )
        
        # Record end time
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"✅ Streamlined workflow completed in {duration:.2f} seconds")
        
        # Check for errors
        if "error" in result:
            logger.error(f"❌ Workflow failed: {result['error']}")
            return result
        
        # Print detailed results
        print_detailed_results(result)
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return {"error": f"Test failed: {str(e)}"}

def print_detailed_results(result: dict):
    """Print detailed results from the working streamlined workflow"""
    
    print("\n" + "="*80)
    print("🎯 WORKING STREAMLINED WORKFLOW DETAILED RESULTS")
    print("="*80)
    
    # Workflow metadata
    metadata = result.get("workflow_metadata", {})
    print(f"\n📊 WORKFLOW METADATA:")
    print(f"  Status: {metadata.get('status', 'Unknown')}")
    print(f"  Duration: {metadata.get('total_duration_seconds', 0):.2f} seconds")
    print(f"  Agents Used: {', '.join(metadata.get('agents_used', []))}")
    print(f"  Repository: {metadata.get('repo_path', 'Unknown')}")
    print(f"  Design Doc: {metadata.get('design_doc_path', 'Unknown')}")
    
    # Agent outputs
    agent_outputs = result.get("agent_outputs", {})
    
    # Repository Analyzer Results
    print(f"\n🔍 REPOSITORY ANALYZER RESULTS:")
    repo_analysis = agent_outputs.get("repository_analyzer", {})
    repo_meta = repo_analysis.get("repository_metadata", {})
    print(f"  Files Analyzed: {repo_meta.get('total_files', 0)}")
    print(f"  Components Found: {len(repo_analysis.get('components', {}))}")
    print(f"  Services Found: {len(repo_analysis.get('business_logic', {}))}")
    print(f"  Business Capabilities: {len(repo_analysis.get('business_capabilities', []))}")
    print(f"  Architectural Patterns: {len(repo_analysis.get('architectural_patterns', []))}")
    
    # Show component details
    components = repo_analysis.get("components", {})
    if components:
        print(f"  Component Details:")
        for comp_name, comp_data in list(components.items())[:3]:  # Show first 3
            print(f"    - {comp_name}: {comp_data.get('type', 'Unknown')} component")
    
    # Design Analyzer Results
    print(f"\n📋 DESIGN ANALYZER RESULTS:")
    design_analysis = agent_outputs.get("design_analyzer", {})
    gaps = design_analysis.get("gaps", [])
    print(f"  Gaps Identified: {len(gaps)}")
    print(f"  Critical Gaps: {len([g for g in gaps if g.get('priority') == 'high'])}")
    print(f"  Medium Gaps: {len([g for g in gaps if g.get('priority') == 'medium'])}")
    print(f"  Low Gaps: {len([g for g in gaps if g.get('priority') == 'low'])}")
    
    if gaps:
        print(f"  Top Gaps:")
        for i, gap in enumerate(gaps[:3], 1):
            print(f"    {i}. {gap.get('description', 'No description')} (Priority: {gap.get('priority', 'Unknown')})")
    
    # Architect Results
    print(f"\n🏗️ ARCHITECT RESULTS:")
    architect_analysis = agent_outputs.get("architect", {})
    impl_plan = architect_analysis.get("implementation_plan", {})
    print(f"  Files to Modify: {len(impl_plan.get('files_to_modify', []))}")
    print(f"  Files to Create: {len(impl_plan.get('files_to_create', []))}")
    print(f"  Implementation Phases: {len(impl_plan.get('implementation_phases', []))}")
    print(f"  Risks Identified: {len(architect_analysis.get('risk_assessment', []))}")
    print(f"  Success Criteria: {len(impl_plan.get('success_criteria', []))}")
    
    if impl_plan.get('files_to_modify'):
        print(f"  Files to Modify:")
        for file_info in impl_plan['files_to_modify'][:5]:  # Show first 5
            file_path = file_info.get('file', file_info.get('file_path', 'Unknown'))
            print(f"    - {file_path}")
    
    if impl_plan.get('files_to_create'):
        print(f"  Files to Create:")
        for file_info in impl_plan['files_to_create'][:5]:  # Show first 5
            file_path = file_info.get('file', file_info.get('file_path', 'Unknown'))
            print(f"    - {file_path}")
    
    # Code Generator Results
    print(f"\n💻 CODE GENERATOR RESULTS:")
    code_generation = agent_outputs.get("code_generator", {})
    print(f"  Changes Applied: {code_generation.get('changes_applied', 0)}")
    print(f"  Errors Fixed: {code_generation.get('errors_fixed', 0)}")
    print(f"  Files Modified: {len(code_generation.get('files_modified', []))}")
    print(f"  Files Created: {len(code_generation.get('files_created', []))}")
    print(f"  Build Status: {code_generation.get('build_status', 'Unknown')}")
    print(f"  Lint Status: {code_generation.get('lint_status', 'Unknown')}")
    
    if code_generation.get('files_modified'):
        print(f"  Modified Files:")
        for file_path in code_generation['files_modified'][:5]:  # Show first 5
            print(f"    - {file_path}")
    
    if code_generation.get('files_created'):
        print(f"  Created Files:")
        for file_path in code_generation['files_created'][:5]:  # Show first 5
            print(f"    - {file_path}")
    
    # Summary
    print(f"\n📈 SUMMARY:")
    summary = result.get("summary", {})
    print(f"  Total Files Analyzed: {summary.get('total_files_analyzed', 0)}")
    print(f"  Gaps Identified: {summary.get('gaps_identified', 0)}")
    print(f"  Files to Modify: {summary.get('files_to_modify', 0)}")
    print(f"  Files to Create: {summary.get('files_to_create', 0)}")
    print(f"  Code Changes Applied: {summary.get('code_changes_applied', 0)}")
    print(f"  Errors Fixed: {summary.get('errors_fixed', 0)}")
    
    # Output files
    print(f"\n📁 OUTPUT FILES:")
    print(f"  Repository Analyzer: data/outputs/streamlined_workflow/repository_analyzer_output.json")
    print(f"  Design Analyzer: data/outputs/streamlined_workflow/design_analyzer_output.json")
    print(f"  Architect: data/outputs/streamlined_workflow/architect_output.json")
    print(f"  Code Generator: data/outputs/streamlined_workflow/code_generator_output.json")
    print(f"  Complete Workflow: data/outputs/streamlined_workflow/complete_workflow_output.json")
    print(f"  Compact Summary: data/outputs/streamlined_workflow/compact_workflow_output.json")
    
    print("="*80)

if __name__ == "__main__":
    print("🚀 Testing Streamlined Multi-Agent Workflow")
    print("This will run all four agents in sequence using REAL analyzers")
    print("Each agent will perform actual analysis and output JSON files")
    
    # Run the main test
    result = test_working_streamlined_workflow()
    
    if result and "error" not in result:
        print("\n✅ Streamlined workflow test completed successfully!")
        print("📁 Check the data/outputs/streamlined_workflow/ directory for all JSON outputs")
        print("🔍 Each agent's output is saved separately for detailed review")
    else:
        print(f"\n❌ Test failed: {result.get('error', 'Unknown error') if result else 'No result returned'}")
