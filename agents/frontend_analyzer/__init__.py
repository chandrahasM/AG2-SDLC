"""
Frontend Multi-Agent Architecture for React/TypeScript Analysis
"""

from .real_hybrid_analyzer import RealHybridRepositoryAnalyzerAgent
from .design_analyzer_agent import DesignAnalyzerAgent
from .architect_agent import ArchitectAgent
from .smart_code_generation_agent import SmartCodeGenerationAgent
from .streamlined_workflow import StreamlinedWorkflow

__all__ = [
    'RealHybridRepositoryAnalyzerAgent',
    'DesignAnalyzerAgent', 
    'ArchitectAgent',
    'SmartCodeGenerationAgent',
    'StreamlinedWorkflow'
]
