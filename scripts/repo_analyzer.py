"""
Working Demo of Real Hybrid Repository Analyzer
Shows actual LLM calls and tool usage with proper integration
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the real hybrid analyzer
from agents.frontend_analyzer.real_hybrid_analyzer import RealHybridRepositoryAnalyzerAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demonstrate_real_hybrid_approach():
    """Demonstrate the real hybrid approach with actual LLM calls"""
    
    print("🚀 Real Hybrid Repository Analyzer - Working Demo")
    print("=" * 60)
    
    # Initialize the real hybrid analyzer
    analyzer = RealHybridRepositoryAnalyzerAgent(
        model_name="gpt-4o-mini",
        temperature=0.1
    )
    
    # Test repository path
    repo_path = "data/inputs/sample_repositories/react_weather_app"
    
    print(f"📁 Analyzing repository: {repo_path}")
    print("🔧 Using real LLM calls and tools")
    print()
    
    try:
        # Run real hybrid analysis
        results = analyzer.analyze_repository(repo_path)
        
        # Check for errors
        if 'error' in results:
            print(f"❌ Analysis failed: {results['error']}")
            return
        
        # Save results
        output_dir = Path("data/outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Save full results
        full_output_path = output_dir / "real_hybrid_demo_results.json"
        with open(full_output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Full results saved to: {full_output_path}")
        
        # Display summary
        print("\n📊 Real Hybrid Analysis Summary:")
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
        
        # Display components from component_analysis (AST parser results)
        component_analysis = results.get('component_analysis', {})
        components = component_analysis.get('components', {})
        print(f"\n🧩 Components found by AST parser: {len(components)}")
        for component_name, component_data in components.items():
            print(f"   - {component_name}:")
            print(f"     • Type: {component_data.get('type', 'Unknown')}")
            print(f"     • Props: {len(component_data.get('props', []))}")
            print(f"     • State: {len(component_data.get('state', []))}")
            print(f"     • Hooks: {len(component_data.get('hooks', []))}")
            print(f"     • Event handlers: {len(component_data.get('event_handlers', []))}")
            print(f"     • Complexity: {component_data.get('complexity', 'N/A')}")
        
        # Display semantic analysis (LLM results)
        semantic_analysis = results.get('semantic_analysis', {})
        llm_components = semantic_analysis.get('components', {})
        llm_services = semantic_analysis.get('services', {})
        
        print(f"\n🧠 LLM Analysis Results:")
        print(f"   - Components analyzed by LLM: {len(llm_components)}")
        print(f"   - Services analyzed by LLM: {len(llm_services)}")
        
        if llm_components:
            print(f"\n   Component LLM Analysis:")
            for component_name, component_data in llm_components.items():
                print(f"     - {component_name}:")
                if 'purpose' in component_data:
                    print(f"       Purpose: {component_data['purpose']}")
                if 'business_role' in component_data:
                    print(f"       Business role: {component_data['business_role']}")
                if 'code_quality' in component_data:
                    quality = component_data['code_quality']
                    print(f"       Quality score: {quality.get('complexity_score', 'N/A')}")
                    print(f"       Maintainability: {quality.get('maintainability', 'N/A')}")
        
        if llm_services:
            print(f"\n   Service LLM Analysis:")
            for service_name, service_data in llm_services.items():
                print(f"     - {service_name}:")
                if 'purpose' in service_data:
                    print(f"       Purpose: {service_data['purpose']}")
                if 'business_role' in service_data:
                    print(f"       Business role: {service_data['business_role']}")
                if 'code_quality' in service_data:
                    quality = service_data['code_quality']
                    print(f"       Quality score: {quality.get('complexity_score', 'N/A')}")
                    print(f"       Maintainability: {quality.get('maintainability', 'N/A')}")
        
        # Display business capabilities
        business_capabilities = results.get('business_capabilities', [])
        print(f"\n💼 Business capabilities: {len(business_capabilities)}")
        for capability in business_capabilities[:3]:  # Show first 3
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
        
        print(f"\n✅ Real hybrid analysis completed successfully!")
        print(f"📄 Full output: {len(json.dumps(results))} characters")
        
        # Show LLM usage statistics
        print(f"\n🤖 LLM Usage Statistics:")
        print(f"   - Components analyzed: {len(llm_components)}")
        print(f"   - Services analyzed: {len(llm_services)}")
        print(f"   - Architecture analysis: 1")
        print(f"   - Total LLM calls: {len(llm_components) + len(llm_services) + 1}")
        
        # Show specific LLM insights
        print(f"\n🧠 LLM-Generated Insights:")
        for component_name, component_data in llm_components.items():
            if 'llm_response' in component_data:
                print(f"   - {component_name}: LLM generated detailed analysis")
            elif 'purpose' in component_data:
                print(f"   - {component_name}: {component_data['purpose']}")
        
        # Show the difference between AST and LLM analysis
        print(f"\n📊 AST Parser vs LLM Analysis Comparison:")
        print(f"   AST Parser (Fast, Structural):")
        print(f"     - Found {len(components)} components")
        print(f"     - Extracted props, state, hooks, event handlers")
        print(f"     - Calculated complexity scores")
        print(f"     - Mapped component relationships")
        
        print(f"   LLM Analysis (Semantic, Business Context):")
        print(f"     - Analyzed {len(llm_components)} components semantically")
        print(f"     - Generated business purpose and role")
        print(f"     - Extracted business capabilities")
        print(f"     - Provided code quality insights")
        print(f"     - Generated architectural patterns")
        
        # Show the hybrid approach benefits
        print(f"\n🎯 Hybrid Approach Benefits:")
        print(f"   ✅ Fast structural analysis (AST parser)")
        print(f"   ✅ Deep semantic understanding (LLM)")
        print(f"   ✅ Business context extraction (LLM)")
        print(f"   ✅ Code quality assessment (LLM)")
        print(f"   ✅ Architectural pattern detection (LLM)")
        print(f"   ✅ Actionable recommendations (LLM)")
        print(f"   ✅ Design agent ready output")
        
        return results
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        print(f"❌ Analysis failed: {e}")
        return None

if __name__ == "__main__":
    demonstrate_real_hybrid_approach()
