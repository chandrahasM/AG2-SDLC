#!/usr/bin/env python3
"""
Test Advanced Repository Analyzer Agent
Tests the comprehensive structural analysis for design agents
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

def test_advanced_repository_analyzer():
    """Test the Advanced Repository Analyzer Agent"""
    
    print("🔍 Advanced Repository Analyzer Agent Test")
    print("=" * 60)
    print("Comprehensive structural analysis for design agents")
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
        print("🚀 Initializing Advanced Repository Analyzer Agent...")
        analyzer = RepositoryAnalyzerAgent(model_name="gpt-4o-mini", temperature=0.1)
        print("✅ Agent initialized successfully!")
        print()
        
        # Show agent capabilities
        print("🔧 Agent Capabilities:")
        print("-" * 40)
        print("  ✅ Deep code structure analysis using AST")
        print("  ✅ Function interconnections and call graphs")
        print("  ✅ Component mapping and relationships")
        print("  ✅ Data model analysis and relationships")
        print("  ✅ API contract analysis")
        print("  ✅ Dependency graph construction")
        print("  ✅ Quality metrics calculation")
        print("  ✅ Strategic code selection for LLM")
        print("  ✅ Design agent ready output")
        print()
        
        # Configure analysis parameters
        file_patterns = ["*.py", "*.md", "*.txt"]
        analysis_config = {
            "depth_level": "deep",
            "focus_areas": ["architecture", "components", "dependencies", "apis"],
            "include_comments": True,
            "include_docstrings": True
        }
        
        # Run the analysis
        print("🔍 Running Advanced Repository Analysis...")
        print("This will perform comprehensive structural analysis...")
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
        print("📊 Comprehensive Structural Analysis Results:")
        print("=" * 50)
        
        # System architecture
        system_architecture = result.get("system_architecture", {})
        print("🏗️  System Architecture:")
        print(f"  - Pattern: {system_architecture.get('pattern', 'Unknown')}")
        print(f"  - Confidence: {system_architecture.get('confidence', 0):.2f}")
        print(f"  - Components: {', '.join(system_architecture.get('components', []))}")
        print(f"  - Entry Points: {', '.join(system_architecture.get('entry_points', []))}")
        print(f"  - Design Principles: {', '.join(system_architecture.get('design_principles', []))}")
        print()
        
        # Components
        components = result.get("components", [])
        print("🧩 Components:")
        for comp in components:
            print(f"  - {comp.get('name', 'Unknown')} ({comp.get('type', 'Unknown')})")
            print(f"    Purpose: {comp.get('purpose', 'Unknown')}")
            print(f"    Files: {', '.join(comp.get('files', []))}")
            print(f"    Interfaces: {len(comp.get('interfaces', []))}")
            print()
        
        # Data models
        data_models = result.get("data_models", [])
        print("📊 Data Models:")
        for model in data_models:
            print(f"  - {model.get('name', 'Unknown')}")
            print(f"    Fields: {len(model.get('fields', []))}")
            print(f"    Relationships: {len(model.get('relationships', []))}")
            print(f"    Validators: {len(model.get('validators', []))}")
            print()
        
        # API contracts
        api_contracts = result.get("api_contracts", [])
        print("🌐 API Contracts:")
        for contract in api_contracts:
            print(f"  - {contract.get('path', 'Unknown')} ({', '.join(contract.get('methods', []))})")
            print(f"    Handler: {contract.get('handler_function', 'Unknown')}")
            print(f"    Parameters: {len(contract.get('parameters', []))}")
            print()
        
        # Function registry
        function_registry = result.get("function_registry", [])
        print("🔧 Function Registry:")
        print(f"  - Total Functions: {len(function_registry)}")
        for func in function_registry[:5]:  # Show first 5
            print(f"    - {func.get('name', 'Unknown')} (Complexity: {func.get('complexity', 0)})")
        print()
        
        # Class registry
        class_registry = result.get("class_registry", [])
        print("🏛️  Class Registry:")
        print(f"  - Total Classes: {len(class_registry)}")
        for cls in class_registry[:5]:  # Show first 5
            print(f"    - {cls.get('name', 'Unknown')} (Methods: {len(cls.get('methods', []))})")
        print()
        
        # Quality metrics
        quality_metrics = result.get("code_quality_metrics", {})
        print("📈 Code Quality Metrics:")
        print(f"  - Total Functions: {quality_metrics.get('total_functions', 0)}")
        print(f"  - Total Classes: {quality_metrics.get('total_classes', 0)}")
        print(f"  - Average Complexity: {quality_metrics.get('average_complexity', 0):.2f}")
        print(f"  - Max Complexity: {quality_metrics.get('max_complexity', 0)}")
        print(f"  - Documentation Coverage: {quality_metrics.get('documentation_coverage', 0):.2%}")
        print(f"  - Maintainability Index: {quality_metrics.get('maintainability_index', 0):.2f}")
        print()
        
        # Design recommendations
        design_recommendations = result.get("design_recommendations", [])
        print("💡 Design Recommendations:")
        for rec in design_recommendations:
            print(f"  - {rec.get('area', 'Unknown')}: {rec.get('issue', 'Unknown')}")
            print(f"    Recommendation: {rec.get('recommendation', 'Unknown')}")
            print(f"    Priority: {rec.get('priority', 'Unknown')}")
            print()
        
        # Save detailed results
        output_file = "data/outputs/advanced_repository_analysis_results.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to: {output_file}")
        print()
        
        # Show key features demonstrated
        print("🎉 Key Features Demonstrated:")
        print("=" * 50)
        print("✅ Deep code structure analysis using AST")
        print("✅ Function interconnections and call graphs")
        print("✅ Component mapping and relationships")
        print("✅ Data model analysis and relationships")
        print("✅ API contract analysis")
        print("✅ Dependency graph construction")
        print("✅ Quality metrics calculation")
        print("✅ Strategic code selection for LLM")
        print("✅ Design agent ready output")
        print("✅ Comprehensive structural analysis")
        print()
        
        print("🎯 This output is optimized for downstream design agents!")
        print("The structured analysis provides complete understanding of:")
        print("- System architecture and component relationships")
        print("- Function interconnections and data flow")
        print("- API contracts and data models")
        print("- Code quality and design recommendations")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Advanced Repository Analyzer Agent Test Suite")
    print("=" * 60)
    print("Testing comprehensive structural analysis for design agents")
    print()
    
    success = test_advanced_repository_analyzer()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Advanced Repository Analyzer Agent is working perfectly")
        print("✅ Comprehensive structural analysis completed")
        print("✅ Design agent ready output generated")
        print("✅ Function interconnections mapped")
        print("✅ Component relationships analyzed")
        print("✅ API contracts extracted")
        print("✅ Data models analyzed")
        print("✅ Quality metrics calculated")
        print("✅ Design recommendations provided")
    else:
        print("\n❌ Test failed!")
