"""
Unit tests for Repository Analyzer Agent
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from agents.repository_analyzer.agent import RepositoryAnalyzerAgent
from agents.repository_analyzer.analyzers.file_analyzer import FileAnalyzer
from core.schemas import WorkflowInput, RepositoryConfig, AnalysisConfig, DocumentationConfig


class TestFileAnalyzer:
    """Test cases for FileAnalyzer"""
    
    def test_init(self):
        """Test FileAnalyzer initialization"""
        analyzer = FileAnalyzer(max_file_size_mb=5)
        assert analyzer.max_file_size_mb == 5
        assert analyzer.max_file_size_bytes == 5 * 1024 * 1024
    
    def test_detect_language(self):
        """Test language detection"""
        analyzer = FileAnalyzer()
        
        assert analyzer._detect_language("test.py") == "python"
        assert analyzer._detect_language("app.js") == "javascript"
        assert analyzer._detect_language("Main.java") == "java"
        assert analyzer._detect_language("server.go") == "go"
        assert analyzer._detect_language("unknown.xyz") is None
    
    def test_categorize_file(self):
        """Test file categorization"""
        analyzer = FileAnalyzer()
        
        assert analyzer._categorize_file("config.json", "json") == "configuration"
        assert analyzer._categorize_file("test_app.py", "python") == "test"
        assert analyzer._categorize_file("README.md", "markdown") == "documentation"
        assert analyzer._categorize_file("Dockerfile", None) == "build"
        assert analyzer._categorize_file("app.py", "python") == "source"
        assert analyzer._categorize_file("unknown.txt", None) == "other"
    
    def test_should_skip_directory(self):
        """Test directory skipping logic"""
        analyzer = FileAnalyzer()
        
        assert analyzer._should_skip_directory(".git") is True
        assert analyzer._should_skip_directory("__pycache__") is True
        assert analyzer._should_skip_directory("node_modules") is True
        assert analyzer._should_skip_directory("src") is False
        assert analyzer._should_skip_directory(".hidden") is True
    
    def test_should_skip_file(self):
        """Test file skipping logic"""
        analyzer = FileAnalyzer()
        
        assert analyzer._should_skip_file(".DS_Store") is True
        assert analyzer._should_skip_file(".gitignore") is True
        assert analyzer._should_skip_file("app.py") is False
        assert analyzer._should_skip_file(".hidden_file") is True
    
    def test_analyze_repository_structure(self):
        """Test repository structure analysis"""
        analyzer = FileAnalyzer()
        
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            (temp_path / "app.py").write_text("print('Hello, World!')")
            (temp_path / "test_app.py").write_text("def test_hello(): pass")
            (temp_path / "README.md").write_text("# Test Project")
            (temp_path / "config.json").write_text('{"name": "test"}')
            
            # Create subdirectory
            (temp_path / "src").mkdir()
            (temp_path / "src" / "main.py").write_text("def main(): pass")
            
            # Analyze structure
            result = analyzer.analyze_repository_structure(str(temp_path))
            
            # Verify results
            assert result["total_files"] >= 5
            assert "python" in result["languages_detected"]
            assert "markdown" in result["languages_detected"]
            assert "json" in result["languages_detected"]
            assert result["file_types"]["source"] >= 2
            assert result["file_types"]["test"] >= 1
            assert result["file_types"]["documentation"] >= 1
            assert result["file_types"]["configuration"] >= 1
    
    def test_analyze_file_content(self):
        """Test file content analysis"""
        analyzer = FileAnalyzer()
        
        # Create a temporary Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
# This is a test file
import os
from pathlib import Path

def hello_world():
    \"\"\"Print hello world\"\"\"
    print("Hello, World!")

class TestClass:
    def __init__(self):
        self.name = "test"
""")
            temp_file = f.name
        
        try:
            result = analyzer.analyze_file_content(temp_file)
            
            # Verify results
            assert result["language"] == "python"
            assert result["line_count"] > 10
            assert "imports" in result
            assert "functions" in result
            assert "classes" in result
            assert result["comments_ratio"] > 0
            
            # Check Python-specific analysis
            assert "import os" in result["imports"]
            assert "hello_world" in result["functions"]
            assert "TestClass" in result["classes"]
            
        finally:
            os.unlink(temp_file)


class TestRepositoryAnalyzerAgent:
    """Test cases for RepositoryAnalyzerAgent"""
    
    def test_init(self):
        """Test agent initialization"""
        agent = RepositoryAnalyzerAgent()
        assert agent.agent_name == "repository_analyzer"
        assert agent.version == "1.0.0"
        assert agent.llm_client is not None
        assert agent.prompt_manager is not None
        assert agent.file_analyzer is not None
    
    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test successful agent execution"""
        agent = RepositoryAnalyzerAgent()
        
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            (temp_path / "app.py").write_text("print('Hello, World!')")
            (temp_path / "README.md").write_text("# Test Project")
            
            # Create workflow input
            workflow_input = WorkflowInput(
                execution_id="test_exec_001",
                repository=RepositoryConfig(
                    local_path=str(temp_path),
                    file_patterns=["*.py", "*.md"],
                    exclude_patterns=[],
                    max_file_size_mb=10,
                    depth_level=5
                ),
                analysis=AnalysisConfig(),
                documentation=DocumentationConfig()
            )
            
            # Mock LLM client to avoid actual API calls
            with patch.object(agent.llm_client, 'generate_text') as mock_llm:
                mock_llm.return_value = "Microservices architecture detected"
                
                # Execute agent
                result = await agent.execute(workflow_input)
                
                # Verify results
                assert result.agent_name == "repository_analyzer"
                assert result.execution_id == "test_exec_001"
                assert result.status == "completed"
                assert result.repo_metadata is not None
                assert result.architecture_analysis is not None
                assert result.code_quality_metrics is not None
                assert result.detected_patterns is not None
                assert result.file_structure is not None
                assert result.dependencies is not None
    
    @pytest.mark.asyncio
    async def test_execute_invalid_path(self):
        """Test agent execution with invalid repository path"""
        agent = RepositoryAnalyzerAgent()
        
        # Create workflow input with invalid path
        workflow_input = WorkflowInput(
            execution_id="test_exec_002",
            repository=RepositoryConfig(
                local_path="/invalid/path/that/does/not/exist",
                file_patterns=["*.py"],
                exclude_patterns=[],
                max_file_size_mb=10,
                depth_level=5
            ),
            analysis=AnalysisConfig(),
            documentation=DocumentationConfig()
        )
        
        # Execute agent
        result = await agent.execute(workflow_input)
        
        # Verify error handling
        assert result.agent_name == "repository_analyzer"
        assert result.execution_id == "test_exec_002"
        assert result.status == "failed"
        assert result.error_message is not None
    
    def test_extract_architecture_pattern(self):
        """Test architecture pattern extraction"""
        agent = RepositoryAnalyzerAgent()
        
        # Test microservices detection
        result = agent._extract_architecture_pattern("This is a microservices architecture")
        assert result == "Microservices"
        
        # Test default case
        result = agent._extract_architecture_pattern("Some other text")
        assert result == "Monolithic"
    
    def test_extract_components(self):
        """Test component extraction"""
        agent = RepositoryAnalyzerAgent()
        
        structure_analysis = {
            "file_types": {
                "source": 10,
                "test": 5,
                "configuration": 3
            }
        }
        
        components = agent._extract_components(structure_analysis)
        
        assert len(components) == 3
        assert any(comp["name"] == "source" for comp in components)
        assert any(comp["name"] == "test" for comp in components)
        assert any(comp["name"] == "configuration" for comp in components)
    
    def test_extract_entry_points(self):
        """Test entry point extraction"""
        agent = RepositoryAnalyzerAgent()
        
        structure_analysis = {
            "largest_files": [
                {"path": "src/main.py", "size_bytes": 1000, "language": "python"},
                {"path": "app.py", "size_bytes": 2000, "language": "python"},
                {"path": "server.js", "size_bytes": 1500, "language": "javascript"},
                {"path": "config.json", "size_bytes": 500, "language": "json"}
            ]
        }
        
        entry_points = agent._extract_entry_points(structure_analysis)
        
        assert len(entry_points) >= 2  # main.py and app.py should be detected
        assert "src/main.py" in entry_points
        assert "app.py" in entry_points


if __name__ == "__main__":
    pytest.main([__file__])
