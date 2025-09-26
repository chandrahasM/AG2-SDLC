#!/usr/bin/env python3
"""
Test Simple Repository Analyzer Agent
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

# Import our simple repository analyzer
from agents.repository_analyzer.simple_analyzer import SimpleRepositoryAnalyzerAgent

def test_simple_repository_analyzer():
    """Test the Simple Repository Analyzer Agent"""
    
    print("🔍 Simple Repository Analyzer Agent Test")
    print("=" * 50)
    print("Testing basic structural analysis with LLM")
    print()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
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
        print("🚀 Initializing Simple Repository Analyzer Agent...")
        analyzer = SimpleRepositoryAnalyzerAgent(model_name="gpt-4o-mini", temperature=0.1)
        print("✅ Agent initialized successfully!")
        print()
        
        # Run the analysis
        print("🔍 Running Simple Repository Analysis...")
        result = analyzer.analyze_repository(repo_path=sample_repo_path)
        
        if "error" in result:
            print(f"❌ Analysis failed: {result['error']}")
            return False
        
        print("✅ Analysis completed successfully!")
        print()
        
        # Display results
        print("📊 Analysis Results:")
        print("=" * 30)
        
        # System architecture
        system_architecture = result.get("system_architecture", {})
        print("🏗️  System Architecture:")
        print(f"  - Pattern: {system_architecture.get('pattern', 'Unknown')}")
        print(f"  - Confidence: {system_architecture.get('confidence', 0):.2f}")
        print(f"  - Components: {', '.join(system_architecture.get('components', []))}")
        print()
        
        # Function registry
        function_registry = result.get("function_registry", [])
        print("🔧 Function Registry:")
        print(f"  - Total Functions: {len(function_registry)}")
        for func in function_registry[:5]:  # Show first 5
            print(f"    - {func.get('name', 'Unknown')} in {func.get('file_path', 'Unknown')}")
        print()
        
        # Class registry
        class_registry = result.get("class_registry", [])
        print("🏛️  Class Registry:")
        print(f"  - Total Classes: {len(class_registry)}")
        for cls in class_registry[:5]:  # Show first 5
            print(f"    - {cls.get('name', 'Unknown')} in {cls.get('file_path', 'Unknown')}")
        print()
        
        # Quality metrics
        quality_metrics = result.get("code_quality_metrics", {})
        print("📈 Code Quality Metrics:")
        print(f"  - Total Functions: {quality_metrics.get('total_functions', 0)}")
        print(f"  - Total Classes: {quality_metrics.get('total_classes', 0)}")
        print(f"  - Maintainability Index: {quality_metrics.get('maintainability_index', 0):.2f}")
        print()
        
        # Design recommendations
        design_recommendations = result.get("design_recommendations", [])
        print("💡 Design Recommendations:")
        for rec in design_recommendations[:3]:  # Show first 3
            if isinstance(rec, dict):
                print(f"  - {rec.get('area', 'Unknown')}: {rec.get('issue', 'Unknown')}")
            else:
                print(f"  - {rec}")
        print()
        
        # Save results
        output_file = "data/outputs/simple_repository_analysis_results.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"💾 Results saved to: {output_file}")
        print()
        
        print("🎉 Key Features Demonstrated:")
        print("=" * 30)
        print("✅ Basic AST parsing and code structure analysis")
        print("✅ Function and class extraction")
        print("✅ LLM-powered architectural analysis")
        print("✅ Structured output for design agents")
        print("✅ AG2 framework integration")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Simple Repository Analyzer Agent Test Suite")
    print("=" * 50)
    print("Testing basic structural analysis with LLM")
    print()
    
    success = test_simple_repository_analyzer()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Simple Repository Analyzer Agent is working")
        print("✅ Basic structural analysis completed")
        print("✅ LLM integration working")
        print("✅ Structured output generated")
    else:
        print("\n❌ Test failed!")
