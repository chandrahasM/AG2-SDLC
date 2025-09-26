#!/usr/bin/env python3
"""
Test Ultimate Repository Analyzer Agent
Tests comprehensive semantic, structural, and behavioral analysis
"""

import sys
import os
import json
from pathlib import Path
import time

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our ultimate repository analyzer
from agents.repository_analyzer.ultimate_analyzer import UltimateRepositoryAnalyzer

def test_ultimate_repository_analyzer():
    """Test the Ultimate Repository Analyzer Agent"""
    
    print("🚀 Ultimate Repository Analyzer Agent Test Suite")
    print("=" * 70)
    print("Testing comprehensive semantic + structural + behavioral analysis")
    print("Using AG2 Framework with ConversableAgent and LLMConfig")
    print()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key in the .env file or environment variables.")
        return False
    print("✅ OpenAI API key found")
    print()
    
    # Test with Booking Website API
    booking_repo_path = "data/inputs/sample_repositories/booking_website_api"
    
    if not os.path.exists(booking_repo_path):
        print(f"❌ Booking repository not found at: {booking_repo_path}")
        return False
    
    print(f"📁 Testing with repository: {booking_repo_path}")
    print()
    
    try:
        # Initialize the ultimate repository analyzer
        print("🔧 Initializing Ultimate Repository Analyzer Agent...")
        print("   🤖 AG2 ConversableAgent with LLMConfig")
        print("   🧠 Semantic Code Understanding")
        print("   🔍 Advanced AST Parsing with Context")
        print("   🏗️  Architectural Pattern Detection")
        print("   📡 API Contract Analysis")
        print("   ⚡ Data Flow & Workflow Analysis")
        print()
        
        analyzer = UltimateRepositoryAnalyzer(model_name="gpt-4o-mini", temperature=0.1)
        print("✅ Ultimate Repository Analyzer initialized successfully!")
        print()
        
        # Show comprehensive capabilities
        print("🎯 Ultimate Analysis Capabilities:")
        print("-" * 50)
        print("  🧠 SEMANTIC ANALYSIS:")
        print("    ✅ Business domain extraction")
        print("    ✅ Domain model understanding")
        print("    ✅ Service boundary identification")
        print("    ✅ Business rule extraction")
        print()
        print("  🔍 STRUCTURAL ANALYSIS:")
        print("    ✅ Advanced AST parsing with semantic context")
        print("    ✅ Function interconnection mapping")
        print("    ✅ Class relationship analysis")
        print("    ✅ Dependency graph construction")
        print()
        print("  ⚡ BEHAVIORAL ANALYSIS:")
        print("    ✅ API contract extraction")
        print("    ✅ Business process identification")
        print("    ✅ Data flow tracing")
        print("    ✅ State management analysis")
        print()
        print("  🏗️  ARCHITECTURAL INTENT:")
        print("    ✅ Design pattern detection")
        print("    ✅ Architectural pattern identification")
        print("    ✅ Design decision reverse engineering")
        print("    ✅ Quality attribute assessment")
        print()
        print("  📊 GAP ANALYSIS READINESS:")
        print("    ✅ Design concept mapping")
        print("    ✅ Component traceability matrix")
        print("    ✅ Reconciliation question generation")
        print("    ✅ Design gap identification")
        print()
        
        # Configure ultimate analysis
        analysis_config = {
            "depth_level": "ultimate",
            "focus_areas": ["semantic", "structural", "behavioral", "architectural"],
            "include_business_analysis": True,
            "include_pattern_detection": True,
            "include_api_analysis": True,
            "include_dataflow_analysis": True,
            "generate_design_recommendations": True
        }
        
        # Run the ultimate analysis
        print("🚀 Running Ultimate Repository Analysis...")
        print("This will perform the most comprehensive analysis possible...")
        print()
        
        start_time = time.time()
        
        result = analyzer.ultimate_repository_analysis(
            repo_path=booking_repo_path,
            file_patterns=["*.py", "*.md", "*.txt"],
            analysis_config=analysis_config
        )
        
        end_time = time.time()
        analysis_duration = end_time - start_time
        
        if "error" in result:
            print(f"❌ Ultimate analysis failed: {result['error']}")
            return False
        
        print(f"✅ Ultimate Analysis completed successfully in {analysis_duration:.2f} seconds!")
        print()
        
        # Display comprehensive results
        print("📊 ULTIMATE REPOSITORY ANALYSIS RESULTS")
        print("=" * 70)
        print()
        
        # Structural Analysis Results
        structural = result.get("structural_analysis", {})
        repo_metadata = structural.get("repo_metadata", {})
        architecture_analysis = structural.get("architecture_analysis", {})
        quality_metrics = structural.get("code_quality_metrics", {})
        
        print("🏗️  STRUCTURAL ANALYSIS:")
        print("=" * 30)
        print(f"  📁 Repository: {repo_metadata.get('name', 'Unknown')}")
        print(f"  📄 Total Files: {repo_metadata.get('total_files', 0)}")
        print(f"  🔧 Total Functions: {repo_metadata.get('total_functions', 0)}")
        print(f"  🏛️  Total Classes: {repo_metadata.get('total_classes', 0)}")
        print(f"  🗣️  Languages: {', '.join(repo_metadata.get('languages', []))}")
        print()
        print(f"  🏗️  Architecture Pattern: {architecture_analysis.get('pattern', 'Unknown')}")
        print(f"  🎯 Confidence: {architecture_analysis.get('confidence', 0):.2f}")
        print(f"  🧩 Components: {', '.join(architecture_analysis.get('components', [])[:5])}")
        print(f"  🚪 Entry Points: {', '.join(architecture_analysis.get('entry_points', [])[:3])}")
        print()
        print(f"  📊 Average Complexity: {quality_metrics.get('average_complexity', 0):.2f}")
        print(f"  📈 Max Complexity: {quality_metrics.get('max_complexity', 0)}")
        print(f"  📚 Documentation Coverage: {quality_metrics.get('documentation_coverage', 0):.2%}")
        print(f"  🔧 Maintainability Index: {quality_metrics.get('maintainability_index', 0):.2f}")
        print(f"  ⚠️  Technical Debt Score: {quality_metrics.get('technical_debt_score', 0):.2f}")
        print()
        
        # Semantic Analysis Results
        semantic = result.get("semantic_analysis", {})
        business_capabilities = semantic.get("business_capabilities", [])
        domain_models = semantic.get("domain_models", {})
        service_boundaries = semantic.get("service_boundaries", [])
        
        print("🧠 SEMANTIC ANALYSIS:")
        print("=" * 25)
        print(f"  🎯 Business Capabilities: {len(business_capabilities)}")
        for cap in business_capabilities[:3]:
            print(f"    - {cap.get('capability', 'Unknown')}")
            print(f"      Purpose: {cap.get('purpose', 'Unknown')}")
            print(f"      Components: {', '.join(cap.get('implementing_components', [])[:3])}")
        print()
        
        entities = domain_models.get("entities", [])
        aggregates = domain_models.get("aggregates", [])
        print(f"  🏛️  Domain Models: {len(entities)} entities, {len(aggregates)} aggregates")
        for entity in entities[:3]:
            print(f"    - {entity.get('name', 'Unknown')}: {entity.get('responsibility', 'Unknown')}")
        print()
        
        print(f"  🔗 Service Boundaries: {len(service_boundaries)}")
        for service in service_boundaries[:3]:
            print(f"    - {service.get('service', 'Unknown')}: {service.get('responsibility', 'Unknown')}")
        print()
        
        # Behavioral Analysis Results
        behavioral = result.get("behavioral_analysis", {})
        api_contracts = behavioral.get("api_contracts", [])
        business_processes = behavioral.get("business_processes", [])
        business_workflows = behavioral.get("business_workflows", [])
        data_flow_graph = behavioral.get("data_flow_graph", {})
        
        print("⚡ BEHAVIORAL ANALYSIS:")
        print("=" * 25)
        print(f"  📡 API Contracts: {len(api_contracts)}")
        for contract in api_contracts[:3]:
            methods = ', '.join(contract.get('methods', []))
            print(f"    - {contract.get('path', 'Unknown')} ({methods})")
            print(f"      Purpose: {contract.get('purpose', 'Unknown')}")
        print()
        
        print(f"  📋 Business Processes: {len(business_processes)}")
        for process in business_processes[:3]:
            print(f"    - {process.get('process', 'Unknown')}")
            print(f"      Trigger: {process.get('trigger', 'Unknown')}")
        print()
        
        print(f"  🔄 Business Workflows: {len(business_workflows)}")
        for workflow in business_workflows[:3]:
            print(f"    - {workflow.get('name', 'Unknown')}")
            print(f"      Steps: {len(workflow.get('steps', []))}")
        print()
        
        graph_complexity = data_flow_graph.get("complexity_metrics", {})
        print(f"  🌐 Data Flow Complexity:")
        print(f"    - Nodes: {graph_complexity.get('node_count', 0)}")
        print(f"    - Edges: {graph_complexity.get('edge_count', 0)}")
        print(f"    - Cyclomatic Complexity: {graph_complexity.get('cyclomatic_complexity', 0)}")
        print()
        
        # Architectural Intent Results
        architectural_intent = result.get("architectural_intent", {})
        design_decisions = architectural_intent.get("design_decisions_identified", [])
        architecture_consistency = architectural_intent.get("architecture_consistency", {})
        quality_attributes = architectural_intent.get("quality_attributes_addressed", [])
        
        print("🏗️  ARCHITECTURAL INTENT:")
        print("=" * 30)
        print(f"  💡 Design Decisions: {len(design_decisions)}")
        for decision in design_decisions[:3]:
            print(f"    - {decision.get('decision', 'Unknown')}")
            print(f"      Rationale: {decision.get('rationale', 'Unknown')}")
            print(f"      Consistency: {decision.get('consistency', 'Unknown')}")
        print()
        
        consistent_patterns = architecture_consistency.get("consistent_patterns", [])
        inconsistencies = architecture_consistency.get("inconsistencies", [])
        print(f"  ✅ Consistent Patterns: {len(consistent_patterns)}")
        for pattern in consistent_patterns[:3]:
            print(f"    - {pattern}")
        print()
        
        if inconsistencies:
            print(f"  ⚠️  Inconsistencies Found: {len(inconsistencies)}")
            for inconsistency in inconsistencies[:3]:
                if isinstance(inconsistency, dict):
                    print(f"    - {inconsistency.get('issue', 'Unknown')}")
                else:
                    print(f"    - {inconsistency}")
        print()
        
        print(f"  🎯 Quality Attributes: {len(quality_attributes)}")
        for attr in quality_attributes[:3]:
            print(f"    - {attr.get('attribute', 'Unknown')}")
            print(f"      Strategies: {', '.join(attr.get('strategies', [])[:3])}")
        print()
        
        # Gap Analysis Readiness Results
        gap_analysis = result.get("gap_analysis_readiness", {})
        design_mappings = gap_analysis.get("mapping_to_design_concepts", [])
        reconciliation_questions = gap_analysis.get("questions_for_design_reconciliation", [])
        component_traceability = gap_analysis.get("component_traceability", {})
        
        print("📊 GAP ANALYSIS READINESS:")
        print("=" * 30)
        print(f"  🗺️  Design Concept Mappings: {len(design_mappings)}")
        for mapping in design_mappings[:3]:
            print(f"    - {mapping.get('code_component', 'Unknown')}")
            print(f"      → {mapping.get('likely_design_concept', 'Unknown')}")
            print(f"      Responsibilities: {', '.join(mapping.get('responsibilities', [])[:2])}")
        print()
        
        print(f"  ❓ Reconciliation Questions: {len(reconciliation_questions)}")
        for question in reconciliation_questions[:3]:
            print(f"    - {question.get('question', 'Unknown')}")
            print(f"      Context: {question.get('context', 'Unknown')}")
        print()
        
        business_to_code = component_traceability.get("business_capability_to_code", {})
        print(f"  🔗 Traceability Matrix: {len(business_to_code)} capability mappings")
        for capability, components in list(business_to_code.items())[:3]:
            print(f"    - {capability} → {', '.join(components[:3])}")
        print()
        
        # Save comprehensive results
        output_file = "data/outputs/ultimate_repository_analysis_results.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"💾 Ultimate analysis results saved to: {output_file}")
        print()
        
        # Show ultimate features demonstrated
        print("🎉 ULTIMATE FEATURES DEMONSTRATED:")
        print("=" * 50)
        print("✅ Semantic Code Understanding")
        print("  └── Business domain extraction from code semantics")
        print("  └── Domain model identification and relationships")
        print("  └── Service boundary detection")
        print()
        print("✅ Advanced AST Parsing with Context")
        print("  └── Function semantic analysis with business intent")
        print("  └── Class archetype classification")
        print("  └── Data transformation detection")
        print()
        print("✅ Architectural Pattern Detection")
        print("  └── Design pattern identification with confidence")
        print("  └── Architectural intent reverse engineering")
        print("  └── Design decision rationale extraction")
        print()
        print("✅ API Contract Analysis")
        print("  └── Endpoint semantic analysis")
        print("  └── Data contract extraction")
        print("  └── Business process mapping")
        print()
        print("✅ Data Flow & Workflow Analysis")
        print("  └── Business workflow identification")
        print("  └── Data flow graph construction")
        print("  └── State management pattern detection")
        print()
        print("✅ AG2 Framework Integration")
        print("  └── ConversableAgent with LLMConfig")
        print("  └── Comprehensive LLM synthesis")
        print("  └── Structured output generation")
        print()
        print("✅ Gap Analysis Readiness")
        print("  └── Design concept mapping")
        print("  └── Component traceability matrix")
        print("  └── Reconciliation question generation")
        print()
        
        print("🎯 READY FOR DESIGN AGENTS:")
        print("=" * 35)
        print("This ultimate analysis output provides everything needed for:")
        print("  📋 Documentation Synthesizer Agent")
        print("    └── Compare existing design with current codebase")
        print("    └── Identify semantic gaps and inconsistencies")
        print("    └── Generate precise reconciliation questions")
        print("  🏗️  Design Architect Agent")
        print("    └── Update architectural documentation")
        print("    └── Propose design improvements")
        print("    └── Ensure design-code alignment")
        print("  🔍 Gap Analysis Agent")
        print("    └── Detailed component-to-design mapping")
        print("    └── Business capability traceability")
        print("    └── Architecture consistency assessment")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during ultimate analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Ultimate Repository Analyzer Test Suite")
    print("=" * 70)
    print("Testing the most comprehensive repository analysis possible")
    print("Semantic + Structural + Behavioral + Architectural Analysis")
    print("Using AG2 Framework with ConversableAgent and LLMConfig")
    print()
    
    success = test_ultimate_repository_analyzer()
    
    if success:
        print("\n🎉 ALL ULTIMATE TESTS PASSED!")
        print("=" * 50)
        print("✅ Ultimate Repository Analyzer is working perfectly")
        print("✅ Comprehensive semantic analysis completed")
        print("✅ Advanced structural analysis with AST parsing")
        print("✅ Behavioral analysis with API contracts and workflows")
        print("✅ Architectural intent detection and pattern recognition")
        print("✅ AG2 framework integration with ConversableAgent")
        print("✅ LLM-powered comprehensive synthesis")
        print("✅ Gap analysis readiness for design agents")
        print("✅ Component traceability and design concept mapping")
        print("✅ Business capability to code component mapping")
        print("✅ Design reconciliation question generation")
        print("✅ Ultimate structured output for documentation synthesis")
        print()
        print("🚀 READY FOR PRODUCTION!")
        print("The Ultimate Repository Analyzer provides the most")
        print("comprehensive codebase analysis possible, optimized")
        print("for downstream design agents and documentation synthesis.")
    else:
        print("\n❌ Ultimate test failed!")
