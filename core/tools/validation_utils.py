"""
Validation utilities for Workflow 1
"""

import re
from typing import Dict, Any, List, Optional, Union
from pathlib import Path


class ValidationUtils:
    """Utility class for validation operations"""
    
    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Validate if file path exists and is accessible"""
        try:
            path = Path(file_path)
            return path.exists() and path.is_file()
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def validate_directory_path(directory_path: str) -> bool:
        """Validate if directory path exists and is accessible"""
        try:
            path = Path(directory_path)
            return path.exists() and path.is_dir()
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def validate_execution_id(execution_id: str) -> bool:
        """Validate execution ID format"""
        if not execution_id or not isinstance(execution_id, str):
            return False
        
        # Allow alphanumeric characters, underscores, and hyphens
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, execution_id))
    
    @staticmethod
    def validate_file_patterns(patterns: List[str]) -> bool:
        """Validate file patterns format"""
        if not isinstance(patterns, list):
            return False
        
        for pattern in patterns:
            if not isinstance(pattern, str) or not pattern.strip():
                return False
            
            # Check for basic glob pattern validity
            if '*' in pattern and not any(c in pattern for c in ['*', '?', '[', ']']):
                # If contains *, should be a valid glob pattern
                continue
        
        return True
    
    @staticmethod
    def validate_confidence_score(score: Union[float, int]) -> bool:
        """Validate confidence score is between 0 and 1"""
        try:
            score_float = float(score)
            return 0.0 <= score_float <= 1.0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_agent_output(output: Dict[str, Any]) -> List[str]:
        """
        Validate agent output structure
        
        Args:
            output: Agent output dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Required fields
        required_fields = ['agent_name', 'execution_id', 'status']
        for field in required_fields:
            if field not in output:
                errors.append(f"Missing required field: {field}")
        
        # Validate status
        if 'status' in output:
            valid_statuses = ['pending', 'running', 'completed', 'failed', 'cancelled']
            if output['status'] not in valid_statuses:
                errors.append(f"Invalid status: {output['status']}")
        
        # Validate execution_id
        if 'execution_id' in output:
            if not ValidationUtils.validate_execution_id(output['execution_id']):
                errors.append("Invalid execution_id format")
        
        return errors
    
    @staticmethod
    def validate_workflow_input(input_data: Dict[str, Any]) -> List[str]:
        """
        Validate workflow input structure
        
        Args:
            input_data: Workflow input dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Required fields
        required_fields = ['execution_id', 'repository']
        for field in required_fields:
            if field not in input_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate execution_id
        if 'execution_id' in input_data:
            if not ValidationUtils.validate_execution_id(input_data['execution_id']):
                errors.append("Invalid execution_id format")
        
        # Validate repository config
        if 'repository' in input_data:
            repo_config = input_data['repository']
            if not isinstance(repo_config, dict):
                errors.append("Repository config must be a dictionary")
            else:
                if 'local_path' not in repo_config:
                    errors.append("Repository config missing local_path")
                elif not ValidationUtils.validate_directory_path(repo_config['local_path']):
                    errors.append("Repository local_path is invalid or inaccessible")
                
                if 'file_patterns' in repo_config:
                    if not ValidationUtils.validate_file_patterns(repo_config['file_patterns']):
                        errors.append("Invalid file_patterns in repository config")
        
        return errors
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe file system usage
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = "unnamed_file"
        
        # Limit length
        if len(sanitized) > 255:
            name, ext = Path(sanitized).stem, Path(sanitized).suffix
            max_name_length = 255 - len(ext)
            sanitized = name[:max_name_length] + ext
        
        return sanitized
    
    @staticmethod
    def validate_json_structure(data: Any, expected_structure: Dict[str, Any]) -> List[str]:
        """
        Validate JSON data structure against expected schema
        
        Args:
            data: Data to validate
            expected_structure: Expected structure definition
            
        Returns:
            List of validation errors
        """
        errors = []
        
        if not isinstance(data, dict):
            errors.append("Data must be a dictionary")
            return errors
        
        # Check required fields
        for field, field_type in expected_structure.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
            else:
                if not isinstance(data[field], field_type):
                    errors.append(f"Field '{field}' must be of type {field_type.__name__}")
        
        return errors
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))
    
    @staticmethod
    def check_data_consistency(
        data1: Dict[str, Any],
        data2: Dict[str, Any],
        key_mappings: Optional[Dict[str, str]] = None
    ) -> List[str]:
        """
        Check consistency between two data structures
        
        Args:
            data1: First data structure
            data2: Second data structure
            key_mappings: Optional mapping between keys in data1 and data2
            
        Returns:
            List of consistency issues
        """
        issues = []
        
        if key_mappings is None:
            key_mappings = {}
        
        # Check for common keys
        for key1, value1 in data1.items():
            key2 = key_mappings.get(key1, key1)
            
            if key2 in data2:
                value2 = data2[key2]
                
                # Check if values are consistent
                if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
                    if abs(value1 - value2) > 0.01:  # Allow small floating point differences
                        issues.append(f"Inconsistent values for key '{key1}': {value1} vs {value2}")
                elif value1 != value2:
                    issues.append(f"Inconsistent values for key '{key1}': {value1} vs {value2}")
            else:
                issues.append(f"Key '{key1}' missing in second data structure")
        
        return issues