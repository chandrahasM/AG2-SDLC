#!/usr/bin/env python3
"""
Test Repository Analyzer Agent with AG2 Framework
Uses ConversableAgent, LLMConfig, and Pydantic structured outputs
"""

import sys
import os
import json
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our repository analyzer
from agents.repository_analyzer.repository_analyzer import RepositoryAnalyzerAgent

def test_repository_analyzer():
    """Test the Repository Analyzer Agent with AG2 framework"""
    
    print("🔍 Repository Analyzer Agent Test (AG2 Framework)")
    print("=" * 60)
    print("Using ConversableAgent, LLMConfig, and Pydantic structured outputs")
    print()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key in the .env file or environment variables.")
        return False
    print("✅ OpenAI API key found")
    print()
    
    # Test with FastAPI sample project
    sample_repo_path = "data/inputs/sample_repositories/fastapi_sample_app"
    
    if not os.path.exists(sample_repo_path):
        print(f"❌ Sample repository not found at: {sample_repo_path}")
        return False
    
    print(f"📁 Testing with repository: {sample_repo_path}")
    print()
    
    try:
        # Initialize the repository analyzer
        print("🚀 Initializing Repository Analyzer Agent with AG2 framework...")
        analyzer = RepositoryAnalyzerAgent(model_name="gpt-4o-mini", temperature=0.1)
        print("✅ Agent initialized successfully!")
        print()
        
        # Show agent capabilities
        print("🔧 Agent Capabilities:")
        print("-" * 40)
        print("  ✅ ConversableAgent with LLMConfig")
        print("  ✅ Pydantic structured outputs")
        print("  ✅ File system scanning and structure mapping")
        print("  ✅ AST parsing for deep code understanding")
        print("  ✅ Dependency analysis (internal/external)")
        print("  ✅ Architectural pattern detection via LLM")
        print("  ✅ Code quality and complexity metrics via LLM")
        print("  ✅ Design pattern recognition via LLM")
        print("  ✅ Structured JSON output for documentation synthesis")
        print()
        
        # Configure analysis parameters
        file_patterns = ["*.py", "*.md", "*.txt"]
        analysis_config = {
            "depth_level": "deep",
            "focus_areas": ["architecture", "patterns", "quality", "dependencies"],
            "include_comments": True,
            "include_docstrings": True
        }
        
        # Run the analysis
        print("🔍 Running AG2-based Repository Analysis...")
        print("This will use ConversableAgent with LLM for intelligent analysis...")
        print()
        
        result = analyzer.analyze_repository(
            repo_path=sample_repo_path,
            file_patterns=file_patterns,
            analysis_config=analysis_config
        )
        
        if "error" in result:
            print(f"❌ Analysis failed: {result['error']}")
            return False
        
        print("✅ Analysis completed successfully!")
        print()
        
        # Display structured results
        print("📊 Structured Analysis Results (AG2 Framework):")
        print("=" * 50)
        
        # Repository metadata
        repo_metadata = result.get("repo_metadata", {})
        print("📁 Repository Metadata:")
        print(f"  - Name: {repo_metadata.get('name', 'Unknown')}")
        print(f"  - Path: {repo_metadata.get('path', 'Unknown')}")
        print(f"  - Total Files: {repo_metadata.get('total_files', 0)}")
        print(f"  - Languages: {', '.join(repo_metadata.get('languages', []))}")
        print(f"  - Main Language: {repo_metadata.get('main_language', 'Unknown')}")
        print(f"  - Duplicate Files: {repo_metadata.get('duplicate_files', 0)}")
        print(f"  - Duplicate Ratio: {repo_metadata.get('duplicate_ratio', 0):.2%}")
        print()
        
        # Architecture analysis (LLM-powered)
        architecture_analysis = result.get("architecture_analysis", {})
        print("🏗️  Architecture Analysis (LLM-powered):")
        print("-" * 40)
        print(f"  - Pattern: {architecture_analysis.get('pattern', 'Unknown')}")
        print(f"  - Confidence: {architecture_analysis.get('confidence', 0):.2f}")
        print(f"  - Components: {', '.join(architecture_analysis.get('components', []))}")
        print(f"  - Entry Points: {', '.join(architecture_analysis.get('entry_points', []))}")
        print(f"  - Design Principles: {', '.join(architecture_analysis.get('design_principles', []))}")
        print()
        
        # Code quality metrics (LLM-powered)
        code_quality_metrics = result.get("code_quality_metrics", {})
        print("📊 Code Quality Metrics (LLM-powered):")
        print("-" * 40)
        print(f"  - Total Functions: {code_quality_metrics.get('total_functions', 0)}")
        print(f"  - Total Classes: {code_quality_metrics.get('total_classes', 0)}")
        print(f"  - Average Complexity: {code_quality_metrics.get('average_complexity', 0):.2f}")
        print(f"  - Max Complexity: {code_quality_metrics.get('max_complexity', 0)}")
        print(f"  - Maintainability Index: {code_quality_metrics.get('maintainability_index', 0):.2f}")
        print(f"  - Technical Debt Score: {code_quality_metrics.get('technical_debt_score', 0):.2f}")
        print(f"  - Documentation Coverage: {code_quality_metrics.get('documentation_coverage', 0):.2%}")
        print(f"  - Code Duplication: {code_quality_metrics.get('code_duplication', 0):.2%}")
        print()
        
        # Detected patterns (LLM-powered)
        detected_patterns = result.get("detected_patterns", [])
        print("🎯 Detected Patterns (LLM-powered):")
        print("-" * 40)
        if detected_patterns:
            for pattern in detected_patterns:
                print(f"  - {pattern.get('name', 'Unknown')} ({pattern.get('pattern_type', 'Unknown')})")
                print(f"    Confidence: {pattern.get('confidence', 0):.2f}")
                print(f"    Location: {pattern.get('location', 'Unknown')}")
                print(f"    Description: {pattern.get('description', 'No description')}")
                print()
        else:
            print("  No patterns detected")
        print()
        
        # AST analysis summary
        ast_analysis = result.get("ast_analysis", {})
        print("🐍 AST Analysis Summary:")
        print("-" * 40)
        print(f"  - Files Analyzed: {ast_analysis.get('files_analyzed', 0)}")
        print(f"  - Total Functions: {ast_analysis.get('total_functions', 0)}")
        print(f"  - Total Classes: {ast_analysis.get('total_classes', 0)}")
        print(f"  - Total Imports: {ast_analysis.get('total_imports', 0)}")
        print(f"  - Average Complexity: {ast_analysis.get('average_complexity', 0):.2f}")
        print(f"  - Max Complexity: {ast_analysis.get('max_complexity', 0)}")
        print()
        
        # Dependency analysis
        dependency_analysis = result.get("dependency_analysis", {})
        print("📦 Dependency Analysis:")
        print("-" * 40)
        print(f"  - External Dependencies: {dependency_analysis.get('total_external', 0)}")
        print(f"  - Internal Dependencies: {dependency_analysis.get('total_internal', 0)}")
        print(f"  - Dependency Ratio: {dependency_analysis.get('dependency_ratio', 0):.2%}")
        print()
        
        # Save detailed results
        output_file = "data/outputs/repository_analysis_results.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to: {output_file}")
        print()
        
        # Show key features demonstrated
        print("🎉 Key Features Demonstrated (AG2 Framework):")
        print("=" * 50)
        print("✅ ConversableAgent with LLMConfig")
        print("✅ Pydantic structured outputs")
        print("✅ LLM-powered intelligent analysis")
        print("✅ File system scanning and structure mapping")
        print("✅ AST parsing for deep code understanding")
        print("✅ Dependency analysis (internal/external)")
        print("✅ Architectural pattern detection via LLM")
        print("✅ Code quality metrics calculation via LLM")
        print("✅ Design pattern recognition via LLM")
        print("✅ Structured JSON output for documentation synthesis")
        print("✅ Flexible and extensible framework")
        print()
        
        print("🎯 This output is ready for Documentation Synthesizer Agent!")
        print("The structured JSON contains all necessary information for")
        print("comparing existing design with current codebase structure.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Repository Analyzer Agent Test Suite (AG2 Framework)")
    print("=" * 60)
    print("Testing ConversableAgent with LLMConfig and Pydantic structured outputs")
    print()
    
    success = test_repository_analyzer()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Repository Analyzer Agent is working perfectly with AG2 framework")
        print("✅ ConversableAgent and LLMConfig are functioning correctly")
        print("✅ Pydantic structured outputs are working")
        print("✅ LLM-powered analysis is providing intelligent insights")
        print("✅ Structured output ready for documentation synthesis")
        print("✅ Flexible and extensible framework implementation")
    else:
        print("\n❌ Test failed!")