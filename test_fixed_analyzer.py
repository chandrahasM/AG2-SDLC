"""
Test the fixed repository analyzer with the React weather app
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the fixed analyzer
from agents.frontend_analyzer.real_hybrid_analyzer import RealHybridRepositoryAnalyzerAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fixed_analyzer():
    """Test the fixed repository analyzer"""
    
    print("🔧 Testing Fixed Repository Analyzer")
    print("=" * 50)
    
    # Initialize the analyzer
    analyzer = RealHybridRepositoryAnalyzerAgent(
        model_name="gpt-4o-mini",
        temperature=0.1
    )
    
    # Test repository path
    repo_path = "data/inputs/sample_repositories/react_weather_app"
    
    print(f"📁 Analyzing repository: {repo_path}")
    
    # Check if repository exists
    if not os.path.exists(repo_path):
        print(f"❌ Repository not found: {repo_path}")
        return
    
    try:
        # Run analysis
        results = analyzer.analyze_repository(repo_path)
        
        # Check for errors
        if 'error' in results:
            print(f"❌ Analysis failed: {results['error']}")
            return
        
        # Save results
        output_dir = Path("data/outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Save full results
        full_output_path = output_dir / "fixed_analyzer_results.json"
        with open(full_output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Full results saved to: {full_output_path}")
        
        # Display summary
        print("\n📊 Fixed Analyzer Results:")
        print("=" * 40)
        
        metadata = results.get('repository_metadata', {})
        print(f"📁 Total files analyzed: {metadata.get('total_files', 0)}")
        print(f"🏗️ Structure pattern: {metadata.get('structure_pattern', 'Unknown')}")
        print(f"🧠 Analysis method: {metadata.get('analysis_method', 'Unknown')}")
        print(f"🎯 Design agent ready: {metadata.get('design_agent_ready', False)}")
        print(f"🤖 LLM calls made: {metadata.get('llm_calls_made', False)}")
        
        # Display file types
        file_types = metadata.get('file_types', {})
        print(f"\n📄 File types analyzed:")
        for file_type, files in file_types.items():
            print(f"   {file_type}: {len(files)} files")
            for file_path in files[:3]:  # Show first 3 files
                print(f"     - {Path(file_path).name}")
        
        # Display components
        semantic_analysis = results.get('semantic_analysis', {})
        components = semantic_analysis.get('components', {})
        print(f"\n🧩 Components found: {len(components)}")
        for component_name, component_data in components.items():
            print(f"   - {component_name}")
            if 'purpose' in component_data:
                print(f"     Purpose: {component_data['purpose']}")
            if 'business_role' in component_data:
                print(f"     Business role: {component_data['business_role']}")
        
        # Display services
        services = semantic_analysis.get('services', {})
        print(f"\n🔌 Services found: {len(services)}")
        for service_name, service_data in services.items():
            print(f"   - {service_name}")
            if 'purpose' in service_data:
                print(f"     Purpose: {service_data['purpose']}")
            if 'business_role' in service_data:
                print(f"     Business role: {service_data['business_role']}")
        
        # Display business capabilities
        business_capabilities = results.get('business_capabilities', [])
        print(f"\n💼 Business capabilities: {len(business_capabilities)}")
        for capability in business_capabilities[:5]:  # Show first 5
            print(f"   - {capability}")
        
        # Display architectural patterns
        patterns = results.get('architectural_patterns', [])
        print(f"\n🏛️ Architectural patterns: {len(patterns)}")
        for pattern in patterns:
            if isinstance(pattern, dict):
                print(f"   - {pattern.get('pattern', 'Unknown')}")
            else:
                print(f"   - {pattern}")
        
        # Display code quality score
        quality = results.get('code_quality_assessment', {})
        score = quality.get('overall_score', 0)
        print(f"\n⭐ Code quality score: {score}/10")
        
        # Display recommendations
        recommendations = results.get('recommendations', {})
        immediate = recommendations.get('immediate', [])
        print(f"\n🎯 Immediate recommendations: {len(immediate)}")
        for rec in immediate[:3]:  # Show first 3
            print(f"   - {rec}")
        
        print(f"\n✅ Fixed analyzer test completed successfully!")
        print(f"📄 Output size: {len(json.dumps(results))} characters")
        
        return results
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        print(f"❌ Analysis failed: {e}")
        return None

if __name__ == "__main__":
    test_fixed_analyzer()
