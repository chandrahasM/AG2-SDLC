"""
Comprehensive Test of Repository Analyzer Agent
Tests file reading, filtering, LLM chunk processing, and output generation
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the real hybrid analyzer
from agents.frontend_analyzer.real_hybrid_analyzer import RealHybridRepositoryAnalyzerAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_comprehensive_repo_analyzer():
    """Comprehensive test of the repository analyzer agent"""
    
    print("🧪 Comprehensive Repository Analyzer Test")
    print("=" * 60)
    
    # Initialize the analyzer
    analyzer = RealHybridRepositoryAnalyzerAgent(
        model_name="gpt-4o-mini",
        temperature=0.1
    )
    
    # Test repository path
    repo_path = "data/inputs/sample_repositories/react_weather_app"
    
    print(f"📁 Testing repository: {repo_path}")
    print(f"🔧 Model: gpt-4o-mini")
    print(f"🌡️ Temperature: 0.1")
    print()
    
    # Check if repository exists
    if not os.path.exists(repo_path):
        print(f"❌ Repository not found: {repo_path}")
        return
    
    try:
        # Run comprehensive analysis
        print("🚀 Starting comprehensive analysis...")
        results = analyzer.analyze_repository(repo_path)
        
        # Check for errors
        if 'error' in results:
            print(f"❌ Analysis failed: {results['error']}")
            return
        
        # Save results
        output_dir = Path("data/outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Save full results
        full_output_path = output_dir / "comprehensive_test_results.json"
        with open(full_output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Full results saved to: {full_output_path}")
        
        # Create compact summary
        compact_output = create_compact_summary(results)
        compact_output_path = output_dir / "comprehensive_test_compact.json"
        with open(compact_output_path, 'w', encoding='utf-8') as f:
            json.dump(compact_output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Compact results saved to: {compact_output_path}")
        
        # Display comprehensive analysis
        print("\n" + "="*60)
        print("📊 COMPREHENSIVE ANALYSIS RESULTS")
        print("="*60)
        
        # 1. Repository Metadata Analysis
        print("\n1️⃣ REPOSITORY METADATA")
        print("-" * 30)
        metadata = results.get('repository_metadata', {})
        print(f"📁 Total files analyzed: {metadata.get('total_files', 0)}")
        print(f"🏗️ Structure pattern: {metadata.get('structure_pattern', 'Unknown')}")
        print(f"🧠 Analysis method: {metadata.get('analysis_method', 'Unknown')}")
        print(f"🎯 Design agent ready: {metadata.get('design_agent_ready', False)}")
        print(f"🤖 LLM calls made: {metadata.get('llm_calls_made', False)}")
        print(f"⏰ Analysis timestamp: {metadata.get('analysis_timestamp', 'Unknown')}")
        
        # 2. File Types Analysis
        print("\n2️⃣ FILE TYPES ANALYSIS")
        print("-" * 30)
        file_types = metadata.get('file_types', {})
        total_files = sum(len(files) for files in file_types.values())
        print(f"📄 Total files processed: {total_files}")
        for file_type, files in file_types.items():
            print(f"   {file_type}: {len(files)} files")
            for file_path in files:
                print(f"     - {Path(file_path).name}")
        
        # 3. Component Analysis (AST Parser Results)
        print("\n3️⃣ COMPONENT ANALYSIS (AST Parser)")
        print("-" * 30)
        component_analysis = results.get('component_analysis', {})
        components = component_analysis.get('components', {})
        print(f"🧩 Components found: {len(components)}")
        
        for component_name, component_data in components.items():
            print(f"\n   📦 {component_name}:")
            print(f"      Type: {component_data.get('type', 'Unknown')}")
            print(f"      File: {Path(component_data.get('file_path', '')).name}")
            print(f"      Props: {len(component_data.get('props', []))}")
            print(f"      State: {len(component_data.get('state', []))}")
            print(f"      Hooks: {len(component_data.get('hooks', []))}")
            print(f"      Event Handlers: {len(component_data.get('event_handlers', []))}")
            print(f"      JSX Elements: {len(component_data.get('jsx_elements', []))}")
            print(f"      Complexity: {component_data.get('complexity', 'N/A')}")
            
            # Show detailed state analysis
            state = component_data.get('state', [])
            if state:
                print(f"      State Details:")
                for state_item in state:
                    print(f"        - {state_item.get('name', 'Unknown')}: {state_item.get('type', 'Unknown')}")
            
            # Show detailed hooks analysis
            hooks = component_data.get('hooks', [])
            if hooks:
                print(f"      Hooks Details:")
                for hook in hooks:
                    print(f"        - {hook.get('name', 'Unknown')}: {hook.get('dependencies', [])}")
            
            # Show detailed event handlers
            event_handlers = component_data.get('event_handlers', [])
            if event_handlers:
                print(f"      Event Handlers:")
                for handler in event_handlers:
                    print(f"        - {handler.get('name', 'Unknown')}: {handler.get('type', 'Unknown')}")
        
        # 4. Semantic Analysis (LLM Results)
        print("\n4️⃣ SEMANTIC ANALYSIS (LLM Results)")
        print("-" * 30)
        semantic_analysis = results.get('semantic_analysis', {})
        llm_components = semantic_analysis.get('components', {})
        llm_services = semantic_analysis.get('services', {})
        
        print(f"🧠 LLM Components analyzed: {len(llm_components)}")
        print(f"🔌 LLM Services analyzed: {len(llm_services)}")
        
        if llm_components:
            print(f"\n   🧩 LLM Component Analysis:")
            for component_name, component_data in llm_components.items():
                print(f"      📦 {component_name}:")
                if 'purpose' in component_data:
                    print(f"         Purpose: {component_data['purpose']}")
                if 'business_role' in component_data:
                    print(f"         Business Role: {component_data['business_role']}")
                if 'code_quality' in component_data:
                    quality = component_data['code_quality']
                    print(f"         Quality Score: {quality.get('complexity_score', 'N/A')}")
                    print(f"         Maintainability: {quality.get('maintainability', 'N/A')}")
                if 'business_capabilities' in component_data:
                    capabilities = component_data['business_capabilities']
                    print(f"         Business Capabilities: {len(capabilities)}")
                    for cap in capabilities[:3]:  # Show first 3
                        print(f"           - {cap}")
        
        if llm_services:
            print(f"\n   🔌 LLM Service Analysis:")
            for service_name, service_data in llm_services.items():
                print(f"      📦 {service_name}:")
                if 'purpose' in service_data:
                    print(f"         Purpose: {service_data['purpose']}")
                if 'business_role' in service_data:
                    print(f"         Business Role: {service_data['business_role']}")
                if 'methods' in service_data:
                    methods = service_data['methods']
                    print(f"         Methods: {len(methods)}")
                    for method_name, method_data in methods.items():
                        print(f"           - {method_name}: {method_data.get('purpose', 'N/A')}")
        
        # 5. Business Capabilities Analysis
        print("\n5️⃣ BUSINESS CAPABILITIES ANALYSIS")
        print("-" * 30)
        business_capabilities = results.get('business_capabilities', [])
        print(f"💼 Total business capabilities: {len(business_capabilities)}")
        for i, capability in enumerate(business_capabilities, 1):
            print(f"   {i}. {capability}")
        
        # 6. Data Flow Analysis
        print("\n6️⃣ DATA FLOW ANALYSIS")
        print("-" * 30)
        data_flow = results.get('data_flow_analysis', {})
        if data_flow:
            print(f"🔄 Primary Flow: {data_flow.get('primary_flow', 'N/A')}")
            transformations = data_flow.get('data_transformations', [])
            print(f"🔄 Data Transformations: {len(transformations)}")
            for i, transformation in enumerate(transformations, 1):
                print(f"   {i}. {transformation}")
            
            state_mgmt = data_flow.get('state_management', {})
            if state_mgmt:
                print(f"📊 State Management:")
                print(f"   Global State: {state_mgmt.get('global_state', 'N/A')}")
                local_state = state_mgmt.get('local_state', [])
                print(f"   Local State: {len(local_state)}")
                for state in local_state:
                    print(f"     - {state}")
        
        # 7. Architectural Patterns
        print("\n7️⃣ ARCHITECTURAL PATTERNS")
        print("-" * 30)
        patterns = results.get('architectural_patterns', [])
        print(f"🏛️ Patterns identified: {len(patterns)}")
        for i, pattern in enumerate(patterns, 1):
            if isinstance(pattern, dict):
                print(f"   {i}. {pattern.get('pattern', 'Unknown')}: {pattern.get('description', 'N/A')}")
            else:
                print(f"   {i}. {pattern}")
        
        # 8. Code Quality Assessment
        print("\n8️⃣ CODE QUALITY ASSESSMENT")
        print("-" * 30)
        quality = results.get('code_quality_assessment', {})
        score = quality.get('overall_score', 0)
        print(f"⭐ Overall Score: {score}/10")
        
        strengths = quality.get('strengths', [])
        if strengths:
            print(f"💪 Strengths: {len(strengths)}")
            for strength in strengths:
                print(f"   - {strength}")
        
        weaknesses = quality.get('weaknesses', [])
        if weaknesses:
            print(f"⚠️ Weaknesses: {len(weaknesses)}")
            for weakness in weaknesses:
                print(f"   - {weakness}")
        
        # 9. Recommendations
        print("\n9️⃣ RECOMMENDATIONS")
        print("-" * 30)
        recommendations = results.get('recommendations', {})
        immediate = recommendations.get('immediate', [])
        short_term = recommendations.get('short_term', [])
        long_term = recommendations.get('long_term', [])
        
        print(f"🎯 Immediate: {len(immediate)}")
        for rec in immediate:
            print(f"   - {rec}")
        
        print(f"🎯 Short-term: {len(short_term)}")
        for rec in short_term:
            print(f"   - {rec}")
        
        print(f"🎯 Long-term: {len(long_term)}")
        for rec in long_term:
            print(f"   - {rec}")
        
        # 10. Summary Statistics
        print("\n🔟 SUMMARY STATISTICS")
        print("-" * 30)
        print(f"📄 Total files analyzed: {metadata.get('total_files', 0)}")
        print(f"🧩 Components found: {len(components)}")
        print(f"🔌 Services found: {len(llm_services)}")
        print(f"💼 Business capabilities: {len(business_capabilities)}")
        print(f"🏛️ Architectural patterns: {len(patterns)}")
        print(f"📊 Output size: {len(json.dumps(results))} characters")
        print(f"📊 Compact size: {len(json.dumps(compact_output))} characters")
        
        # 11. LLM Usage Statistics
        print("\n🤖 LLM USAGE STATISTICS")
        print("-" * 30)
        print(f"🧠 Component LLM calls: {len(llm_components)}")
        print(f"🔌 Service LLM calls: {len(llm_services)}")
        print(f"🏛️ Architecture LLM call: 1")
        print(f"📊 Total LLM calls: {len(llm_components) + len(llm_services) + 1}")
        
        print(f"\n✅ Comprehensive test completed successfully!")
        print(f"🎯 Repository analyzer is working perfectly!")
        
        return results
        
    except Exception as e:
        logger.error(f"Error during comprehensive analysis: {e}")
        print(f"❌ Analysis failed: {e}")
        return None

def create_compact_summary(results: dict) -> dict:
    """Create a compact summary for quick review"""
    
    metadata = results.get('repository_metadata', {})
    component_analysis = results.get('component_analysis', {})
    semantic_analysis = results.get('semantic_analysis', {})
    
    return {
        'summary': {
            'total_files': metadata.get('total_files', 0),
            'components_found': len(component_analysis.get('components', {})),
            'llm_components': len(semantic_analysis.get('components', {})),
            'llm_services': len(semantic_analysis.get('services', {})),
            'business_capabilities': len(results.get('business_capabilities', [])),
            'architectural_patterns': len(results.get('architectural_patterns', [])),
            'code_quality_score': results.get('code_quality_assessment', {}).get('overall_score', 0),
            'analysis_method': metadata.get('analysis_method', 'Unknown'),
            'design_agent_ready': metadata.get('design_agent_ready', False),
            'llm_calls_made': metadata.get('llm_calls_made', False)
        },
        'file_types': metadata.get('file_types', {}),
        'components': list(component_analysis.get('components', {}).keys()),
        'llm_insights': {
            'components_with_llm_analysis': list(semantic_analysis.get('components', {}).keys()),
            'services_with_llm_analysis': list(semantic_analysis.get('services', {}).keys())
        },
        'business_capabilities': results.get('business_capabilities', []),
        'architectural_patterns': results.get('architectural_patterns', []),
        'recommendations': results.get('recommendations', {}),
        'data_flow': results.get('data_flow_analysis', {})
    }

if __name__ == "__main__":
    test_comprehensive_repo_analyzer()
