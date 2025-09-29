"""
Debug LLM responses to see what's being returned
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

def debug_llm_responses():
    """Debug what the LLM is actually returning"""
    
    print("🔍 Debugging LLM Responses")
    print("=" * 40)
    
    # Initialize the analyzer
    analyzer = RealHybridRepositoryAnalyzerAgent(
        model_name="gpt-4o-mini",
        temperature=0.1
    )
    
    # Test with a simple component
    test_component = {
        'name': 'App',
        'type': 'function',
        'props': [],
        'state': [{'name': 'currentLocation', 'type': 'useState', 'initial_value': "useState('London')"}],
        'hooks': [{'name': 'useState', 'line_number': 2, 'dependencies': ['currentLocation', 'setCurrentLocation']}],
        'business_logic': []
    }
    
    test_file_analysis = {
        'file_path': 'src/App.tsx',
        'file_type': 'component',
        'imports': ['React', 'useState'],
        'exports': ['App']
    }
    
    print("🧪 Testing LLM response processing...")
    
    try:
        # Test the component analysis
        result = analyzer._analyze_component_with_real_llm(test_component, test_file_analysis)
        
        print(f"📊 LLM Analysis Result:")
        print(f"   Type: {type(result)}")
        print(f"   Content: {json.dumps(result, indent=2) if result else 'None'}")
        
        if result:
            print(f"✅ LLM analysis successful!")
            print(f"   Component: {result.get('name', 'Unknown')}")
            print(f"   Purpose: {result.get('purpose', 'N/A')}")
            print(f"   Business Role: {result.get('business_role', 'N/A')}")
        else:
            print(f"❌ LLM analysis returned None")
            
    except Exception as e:
        print(f"❌ Error during LLM analysis: {e}")
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    debug_llm_responses()
