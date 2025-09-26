"""
File utilities for Workflow 1
"""

import os
import hashlib
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import fnmatch


class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def scan_directory(
        directory_path: str,
        include_patterns: List[str] = None,
        exclude_patterns: List[str] = None,
        max_depth: int = 10,
        max_file_size_mb: int = 10
    ) -> Dict[str, Any]:
        """
        Scan directory and return file information
        
        Args:
            directory_path: Path to scan
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
            max_depth: Maximum directory depth
            max_file_size_mb: Maximum file size in MB
            
        Returns:
            Dictionary with file information
        """
        if include_patterns is None:
            include_patterns = ["*"]
        if exclude_patterns is None:
            exclude_patterns = []
        
        directory = Path(directory_path)
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        files_info = {
            "total_files": 0,
            "total_size_bytes": 0,
            "files_by_extension": {},
            "files_by_size": {"small": 0, "medium": 0, "large": 0},
            "files": [],
            "directories": [],
            "excluded_files": 0
        }
        
        max_file_size_bytes = max_file_size_mb * 1024 * 1024
        
        for root, dirs, files in os.walk(directory):
            # Calculate current depth
            current_depth = len(Path(root).relative_to(directory).parts)
            if current_depth > max_depth:
                continue
            
            # Add directory info
            rel_dir = os.path.relpath(root, directory_path)
            if rel_dir != ".":
                files_info["directories"].append({
                    "path": rel_dir,
                    "depth": current_depth
                })
            
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(directory)
                
                # Check if file should be excluded
                if FileUtils._should_exclude_file(str(rel_path), exclude_patterns):
                    files_info["excluded_files"] += 1
                    continue
                
                # Check if file matches include patterns
                if not FileUtils._matches_patterns(str(rel_path), include_patterns):
                    continue
                
                try:
                    file_stat = file_path.stat()
                    file_size = file_stat.st_size
                    
                    # Skip files that are too large
                    if file_size > max_file_size_bytes:
                        files_info["excluded_files"] += 1
                        continue
                    
                    # Get file extension
                    extension = file_path.suffix.lower()
                    if extension not in files_info["files_by_extension"]:
                        files_info["files_by_extension"][extension] = 0
                    files_info["files_by_extension"][extension] += 1
                    
                    # Categorize by size
                    if file_size < 1024:  # < 1KB
                        files_info["files_by_size"]["small"] += 1
                    elif file_size < 1024 * 1024:  # < 1MB
                        files_info["files_by_size"]["medium"] += 1
                    else:
                        files_info["files_by_size"]["large"] += 1
                    
                    # Add file info
                    file_info = {
                        "path": str(rel_path),
                        "size_bytes": file_size,
                        "extension": extension,
                        "mime_type": mimetypes.guess_type(str(file_path))[0],
                        "modified_time": file_stat.st_mtime,
                        "depth": current_depth
                    }
                    
                    files_info["files"].append(file_info)
                    files_info["total_files"] += 1
                    files_info["total_size_bytes"] += file_size
                    
                except (OSError, PermissionError):
                    # Skip files we can't access
                    continue
        
        return files_info
    
    @staticmethod
    def _should_exclude_file(file_path: str, exclude_patterns: List[str]) -> bool:
        """Check if file should be excluded based on patterns"""
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
            # Also check if any parent directory matches
            path_parts = Path(file_path).parts
            for i in range(len(path_parts)):
                partial_path = str(Path(*path_parts[:i+1]))
                if fnmatch.fnmatch(partial_path, pattern):
                    return True
        return False
    
    @staticmethod
    def _matches_patterns(file_path: str, include_patterns: List[str]) -> bool:
        """Check if file matches any include patterns"""
        for pattern in include_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False
    
    @staticmethod
    def read_file_content(file_path: str, max_size_mb: int = 10) -> Optional[str]:
        """
        Read file content with size limit
        
        Args:
            file_path: Path to file
            max_size_mb: Maximum file size in MB
            
        Returns:
            File content as string or None if file is too large
        """
        max_size_bytes = max_size_mb * 1024 * 1024
        
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return None
            
            file_size = file_path_obj.stat().st_size
            if file_size > max_size_bytes:
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
                
        except (OSError, UnicodeDecodeError, PermissionError):
            return None
    
    @staticmethod
    def get_file_hash(file_path: str) -> Optional[str]:
        """Get SHA256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except (OSError, PermissionError):
            return None
    
    @staticmethod
    def find_files_by_pattern(
        directory: str,
        pattern: str,
        recursive: bool = True
    ) -> List[str]:
        """
        Find files matching pattern
        
        Args:
            directory: Directory to search
            pattern: File pattern (e.g., "*.py", "test_*.js")
            recursive: Whether to search recursively
            
        Returns:
            List of matching file paths
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            return []
        
        matches = []
        
        if recursive:
            for file_path in directory_path.rglob(pattern):
                if file_path.is_file():
                    matches.append(str(file_path))
        else:
            for file_path in directory_path.glob(pattern):
                if file_path.is_file():
                    matches.append(str(file_path))
        
        return matches
    
    @staticmethod
    def get_project_structure(directory: str, max_depth: int = 5) -> Dict[str, Any]:
        """
        Get project structure as nested dictionary
        
        Args:
            directory: Project directory
            max_depth: Maximum depth to traverse
            
        Returns:
            Nested dictionary representing project structure
        """
        def build_tree(path: Path, current_depth: int = 0) -> Dict[str, Any]:
            if current_depth > max_depth:
                return {}
            
            tree = {}
            
            try:
                for item in path.iterdir():
                    if item.is_dir():
                        # Skip common directories to ignore
                        if item.name in {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env'}:
                            continue
                        tree[item.name] = build_tree(item, current_depth + 1)
                    elif item.is_file():
                        tree[item.name] = {
                            "type": "file",
                            "size": item.stat().st_size,
                            "extension": item.suffix
                        }
            except (PermissionError, OSError):
                pass
            
            return tree
        
        project_path = Path(directory)
        if not project_path.exists():
            return {}
        
        return {
            "root": project_path.name,
            "structure": build_tree(project_path)
        }