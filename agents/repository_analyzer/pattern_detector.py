"""
Advanced Pattern Detector for Architectural Intent
Detects not just patterns, but architectural INTENT and design decisions
"""

import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class DesignDecision:
    decision: str
    rationale: str
    implementation: str
    consistency: str

@dataclass
class ArchitecturalViolation:
    issue: str
    violation: str
    impact: str
    files: List[str]

@dataclass
class QualityAttribute:
    attribute: str
    strategies: List[str]
    evidence: str

class AdvancedPatternDetector:
    """Detects architectural patterns and design intent"""
    
    def __init__(self):
        # Pattern signatures for detection
        self.pattern_signatures = {
            'repository': {
                'class_suffixes': ['Repository', 'Repo'],
                'method_patterns': [r'find_\w+', r'get_\w+', r'save_\w+', r'delete_\w+'],
                'interface_indicators': ['abstract', 'ABC', 'Protocol'],
                'dependency_patterns': ['database', 'session', 'connection']
            },
            'service': {
                'class_suffixes': ['Service', 'Manager', 'Handler'],
                'method_patterns': [r'process_\w+', r'handle_\w+', r'execute_\w+'],
                'dependency_patterns': ['repository', 'client', 'gateway'],
                'business_logic_indicators': ['calculate', 'validate', 'transform']
            },
            'factory': {
                'class_suffixes': ['Factory', 'Builder', 'Creator'],
                'method_patterns': [r'create_\w+', r'build_\w+', r'make_\w+'],
                'return_patterns': ['new instance', 'object creation'],
                'conditional_creation': True
            },
            'observer': {
                'method_patterns': [r'notify_\w+', r'subscribe_\w+', r'unsubscribe_\w+'],
                'event_patterns': ['event', 'listener', 'callback'],
                'collection_patterns': ['listeners', 'observers', 'subscribers']
            },
            'strategy': {
                'class_suffixes': ['Strategy', 'Policy', 'Algorithm'],
                'interface_indicators': ['abstract', 'ABC', 'Protocol'],
                'method_patterns': [r'execute', r'apply', r'process'],
                'context_patterns': ['context', 'executor']
            },
            'decorator': {
                'method_patterns': [r'@\w+', r'decorator'],
                'wrapper_patterns': ['wrapper', 'decorated'],
                'enhancement_indicators': ['before', 'after', 'around']
            },
            'adapter': {
                'class_suffixes': ['Adapter', 'Wrapper'],
                'method_patterns': [r'adapt_\w+', r'convert_\w+'],
                'interface_mapping': True,
                'external_integration': True
            },
            'facade': {
                'class_suffixes': ['Facade', 'Gateway', 'Interface'],
                'method_patterns': [r'simple_\w+', r'unified_\w+'],
                'subsystem_coordination': True,
                'complexity_hiding': True
            }
        }
        
        # Architectural patterns
        self.architectural_patterns = {
            'layered': {
                'layer_indicators': ['controller', 'service', 'repository', 'model'],
                'separation_patterns': ['presentation', 'business', 'data', 'persistence'],
                'dependency_direction': 'downward'
            },
            'hexagonal': {
                'port_indicators': ['port', 'interface', 'contract'],
                'adapter_indicators': ['adapter', 'implementation'],
                'core_isolation': True,
                'dependency_inversion': True
            },
            'microservices': {
                'service_boundaries': ['service', 'api', 'gateway'],
                'communication_patterns': ['rest', 'http', 'message', 'event'],
                'data_isolation': True,
                'independent_deployment': True
            },
            'event_driven': {
                'event_indicators': ['event', 'message', 'notification'],
                'handler_patterns': ['handler', 'listener', 'subscriber'],
                'async_patterns': ['async', 'queue', 'publish', 'subscribe']
            },
            'cqrs': {
                'command_patterns': ['command', 'create', 'update', 'delete'],
                'query_patterns': ['query', 'get', 'find', 'search'],
                'separation_indicators': ['read', 'write', 'command', 'query']
            }
        }
        
        # Quality attribute patterns
        self.quality_patterns = {
            'maintainability': [
                'single responsibility', 'separation of concerns', 'modular design',
                'low coupling', 'high cohesion', 'consistent patterns'
            ],
            'testability': [
                'dependency injection', 'interface segregation', 'mockable components',
                'pure functions', 'isolated units', 'test doubles'
            ],
            'scalability': [
                'stateless design', 'horizontal scaling', 'load balancing',
                'caching strategies', 'async processing', 'resource pooling'
            ],
            'security': [
                'authentication', 'authorization', 'input validation',
                'secure communication', 'data encryption', 'access control'
            ],
            'performance': [
                'caching', 'lazy loading', 'connection pooling',
                'async operations', 'batch processing', 'optimization'
            ]
        }

    def detect_architectural_intent(self, analysis_data: Dict) -> Dict:
        """Detects architectural intent and design decisions"""
        logger.info("Detecting architectural intent and design decisions...")
        
        try:
            semantic_analysis = analysis_data.get('semantic_analysis', {})
            structural_analysis = analysis_data.get('structural_analysis', {})
            
            # Detect design patterns
            design_patterns = self._detect_design_patterns(analysis_data)
            
            # Detect architectural patterns
            architectural_patterns = self._detect_architectural_patterns(analysis_data)
            
            # Reverse engineer design decisions
            design_decisions = self._reverse_engineer_design_decisions(analysis_data)
            
            # Assess architecture consistency
            consistency_analysis = self._assess_architecture_consistency(analysis_data)
            
            # Identify quality attributes addressed
            quality_attributes = self._identify_quality_attributes(analysis_data)
            
            # Detect architectural violations
            violations = self._detect_architectural_violations(analysis_data)
            
            return {
                "design_patterns_detected": design_patterns,
                "architectural_patterns": architectural_patterns,
                "design_decisions_identified": design_decisions,
                "architecture_consistency": consistency_analysis,
                "quality_attributes_addressed": quality_attributes,
                "architectural_violations": violations,
                "design_principles_applied": self._identify_design_principles(analysis_data),
                "architecture_evolution_indicators": self._detect_evolution_indicators(analysis_data)
            }
            
        except Exception as e:
            logger.error(f"Error detecting architectural intent: {e}")
            return {
                "design_patterns_detected": [],
                "architectural_patterns": [],
                "design_decisions_identified": [],
                "architecture_consistency": {"consistent_patterns": [], "inconsistencies": []},
                "quality_attributes_addressed": [],
                "architectural_violations": [],
                "design_principles_applied": [],
                "architecture_evolution_indicators": []
            }

    def _detect_design_patterns(self, analysis_data: Dict) -> List[Dict]:
        """Detect design patterns in the codebase"""
        patterns_found = []
        
        functions = analysis_data.get('functions', [])
        classes = analysis_data.get('classes', [])
        
        # Detect patterns from class structures
        for pattern_name, signature in self.pattern_signatures.items():
            pattern_instances = self._find_pattern_instances(pattern_name, signature, classes, functions)
            patterns_found.extend(pattern_instances)
        
        return patterns_found

    def _find_pattern_instances(self, pattern_name: str, signature: Dict, classes: List[Dict], functions: List[Dict]) -> List[Dict]:
        """Find instances of a specific pattern"""
        instances = []
        
        for cls in classes:
            confidence = self._calculate_pattern_confidence(cls, signature, classes, functions)
            
            if confidence > 0.6:  # Threshold for pattern detection
                instance = {
                    "name": f"{pattern_name.title()} Pattern",
                    "type": "design_pattern",
                    "confidence": confidence,
                    "location": f"{cls.get('file_path', 'unknown')}::{cls.get('name', 'unknown')}",
                    "description": self._generate_pattern_description(pattern_name, cls),
                    "implementation_quality": self._assess_pattern_implementation_quality(pattern_name, cls, classes),
                    "participants": self._identify_pattern_participants(pattern_name, cls, classes),
                    "intent": self._get_pattern_intent(pattern_name),
                    "consequences": self._get_pattern_consequences(pattern_name)
                }
                instances.append(instance)
        
        return instances

    def _calculate_pattern_confidence(self, cls: Dict, signature: Dict, classes: List[Dict], functions: List[Dict]) -> float:
        """Calculate confidence score for pattern match"""
        confidence = 0.0
        total_checks = 0
        
        class_name = cls.get('name', '').lower()
        methods = cls.get('methods', [])
        
        # Check class name suffixes
        if 'class_suffixes' in signature:
            total_checks += 1
            for suffix in signature['class_suffixes']:
                if class_name.endswith(suffix.lower()):
                    confidence += 0.3
                    break
        
        # Check method patterns
        if 'method_patterns' in signature:
            total_checks += 1
            method_names = [m.get('name', '') for m in methods]
            pattern_matches = 0
            
            for pattern in signature['method_patterns']:
                for method_name in method_names:
                    if re.search(pattern, method_name, re.IGNORECASE):
                        pattern_matches += 1
                        break
            
            if pattern_matches > 0:
                confidence += 0.4 * (pattern_matches / len(signature['method_patterns']))
        
        # Check interface indicators
        if 'interface_indicators' in signature:
            total_checks += 1
            base_classes = cls.get('base_classes', [])
            for indicator in signature['interface_indicators']:
                if any(indicator.lower() in base.lower() for base in base_classes):
                    confidence += 0.2
                    break
        
        # Check dependency patterns
        if 'dependency_patterns' in signature:
            total_checks += 1
            # This would require analysis of method calls and dependencies
            # Simplified check for now
            all_calls = []
            for method in methods:
                all_calls.extend(method.get('calls', []))
            
            dependency_matches = 0
            for pattern in signature['dependency_patterns']:
                if any(pattern.lower() in call.lower() for call in all_calls):
                    dependency_matches += 1
            
            if dependency_matches > 0:
                confidence += 0.3 * (dependency_matches / len(signature['dependency_patterns']))
        
        return min(confidence, 1.0)  # Cap at 1.0

    def _detect_architectural_patterns(self, analysis_data: Dict) -> List[Dict]:
        """Detect architectural patterns"""
        patterns_found = []
        
        for pattern_name, pattern_def in self.architectural_patterns.items():
            confidence = self._assess_architectural_pattern(pattern_name, pattern_def, analysis_data)
            
            if confidence > 0.5:
                pattern_info = {
                    "pattern": pattern_name,
                    "confidence": confidence,
                    "evidence": self._collect_architectural_evidence(pattern_name, pattern_def, analysis_data),
                    "implementation_details": self._extract_architectural_implementation(pattern_name, analysis_data),
                    "benefits": self._get_architectural_benefits(pattern_name),
                    "trade_offs": self._get_architectural_tradeoffs(pattern_name)
                }
                patterns_found.append(pattern_info)
        
        return patterns_found

    def _assess_architectural_pattern(self, pattern_name: str, pattern_def: Dict, analysis_data: Dict) -> float:
        """Assess confidence for architectural pattern"""
        confidence = 0.0
        
        classes = analysis_data.get('classes', [])
        functions = analysis_data.get('functions', [])
        
        # Check for layer indicators (for layered architecture)
        if 'layer_indicators' in pattern_def:
            layer_count = 0
            for indicator in pattern_def['layer_indicators']:
                if any(indicator.lower() in cls.get('name', '').lower() or 
                      indicator.lower() in cls.get('file_path', '').lower() 
                      for cls in classes):
                    layer_count += 1
            
            if layer_count >= 3:  # At least 3 layers
                confidence += 0.4
        
        # Check for service boundaries (for microservices)
        if 'service_boundaries' in pattern_def:
            service_count = 0
            for indicator in pattern_def['service_boundaries']:
                if any(indicator.lower() in cls.get('name', '').lower() 
                      for cls in classes):
                    service_count += 1
            
            if service_count >= 2:
                confidence += 0.3
        
        # Check for communication patterns
        if 'communication_patterns' in pattern_def:
            comm_patterns = 0
            all_calls = []
            for func in functions:
                all_calls.extend(func.get('calls', []))
            
            for pattern in pattern_def['communication_patterns']:
                if any(pattern.lower() in call.lower() for call in all_calls):
                    comm_patterns += 1
            
            if comm_patterns > 0:
                confidence += 0.3
        
        return min(confidence, 1.0)

    def _reverse_engineer_design_decisions(self, analysis_data: Dict) -> List[Dict]:
        """Reverse engineer design decisions from code"""
        decisions = []
        
        classes = analysis_data.get('classes', [])
        functions = analysis_data.get('functions', [])
        
        # Detect repository pattern usage
        repo_classes = [cls for cls in classes if 'repository' in cls.get('name', '').lower()]
        if repo_classes:
            decision = {
                "decision": "Use Repository Pattern for data access",
                "rationale": "Abstract database implementation, ease testing",
                "implementation": f"{len(repo_classes)} repository classes with interface abstraction",
                "consistency": "Applied consistently" if len(repo_classes) > 1 else "Single implementation",
                "evidence": [cls.get('name', '') for cls in repo_classes]
            }
            decisions.append(decision)
        
        # Detect service layer pattern
        service_classes = [cls for cls in classes if 'service' in cls.get('name', '').lower()]
        if service_classes:
            decision = {
                "decision": "Implement Service Layer pattern",
                "rationale": "Separate business logic from presentation and data layers",
                "implementation": f"{len(service_classes)} service classes handling business operations",
                "consistency": "Consistently applied across business domains",
                "evidence": [cls.get('name', '') for cls in service_classes]
            }
            decisions.append(decision)
        
        # Detect validation strategy
        validation_functions = [func for func in functions if 'validate' in func.get('name', '').lower()]
        if validation_functions:
            decision = {
                "decision": "Separate validation layers",
                "rationale": "Input validation vs business rule validation",
                "implementation": f"{len(validation_functions)} validation functions across layers",
                "consistency": "Mixed - some validation in controllers, some in services",
                "evidence": [func.get('name', '') for func in validation_functions[:5]]
            }
            decisions.append(decision)
        
        # Detect error handling strategy
        error_handling_decision = self._analyze_error_handling_strategy(functions)
        if error_handling_decision:
            decisions.append(error_handling_decision)
        
        # Detect dependency injection usage
        di_decision = self._analyze_dependency_injection_usage(classes, functions)
        if di_decision:
            decisions.append(di_decision)
        
        return decisions

    def _assess_architecture_consistency(self, analysis_data: Dict) -> Dict:
        """Assess consistency of architectural patterns"""
        consistency = {
            "consistent_patterns": [],
            "inconsistencies": []
        }
        
        classes = analysis_data.get('classes', [])
        functions = analysis_data.get('functions', [])
        
        # Check controller consistency
        controllers = [cls for cls in classes if 'controller' in cls.get('name', '').lower()]
        if controllers:
            controller_consistency = self._check_controller_consistency(controllers)
            if controller_consistency['is_consistent']:
                consistency['consistent_patterns'].append("All controllers follow same structure")
            else:
                consistency['inconsistencies'].extend(controller_consistency['violations'])
        
        # Check service layer consistency
        services = [cls for cls in classes if 'service' in cls.get('name', '').lower()]
        if services:
            service_consistency = self._check_service_consistency(services)
            if service_consistency['is_consistent']:
                consistency['consistent_patterns'].append("Service layer handles business logic consistently")
            else:
                consistency['inconsistencies'].extend(service_consistency['violations'])
        
        # Check error handling consistency
        error_consistency = self._check_error_handling_consistency(functions)
        if error_consistency['is_consistent']:
            consistency['consistent_patterns'].append("Error handling follows unified strategy")
        else:
            consistency['inconsistencies'].extend(error_consistency['violations'])
        
        return consistency

    def _identify_quality_attributes(self, analysis_data: Dict) -> List[Dict]:
        """Identify quality attributes addressed by the architecture"""
        attributes = []
        
        classes = analysis_data.get('classes', [])
        functions = analysis_data.get('functions', [])
        
        for attr_name, indicators in self.quality_patterns.items():
            evidence = self._collect_quality_evidence(attr_name, indicators, classes, functions)
            
            if evidence['strategies']:
                attribute = {
                    "attribute": attr_name.title(),
                    "strategies": evidence['strategies'],
                    "evidence": evidence['evidence'],
                    "implementation_score": evidence['score']
                }
                attributes.append(attribute)
        
        return attributes

    def _detect_architectural_violations(self, analysis_data: Dict) -> List[Dict]:
        """Detect architectural violations"""
        violations = []
        
        classes = analysis_data.get('classes', [])
        functions = analysis_data.get('functions', [])
        
        # Check for repository pattern violations
        repo_violations = self._check_repository_violations(classes, functions)
        violations.extend(repo_violations)
        
        # Check for service layer violations
        service_violations = self._check_service_violations(classes, functions)
        violations.extend(service_violations)
        
        # Check for separation of concerns violations
        soc_violations = self._check_separation_concerns_violations(classes, functions)
        violations.extend(soc_violations)
        
        return violations

    def _identify_design_principles(self, analysis_data: Dict) -> List[str]:
        """Identify design principles applied"""
        principles = []
        
        classes = analysis_data.get('classes', [])
        functions = analysis_data.get('functions', [])
        
        # Single Responsibility Principle
        if self._check_single_responsibility(classes):
            principles.append("Single Responsibility Principle")
        
        # Open/Closed Principle
        if self._check_open_closed(classes):
            principles.append("Open/Closed Principle")
        
        # Dependency Inversion Principle
        if self._check_dependency_inversion(classes):
            principles.append("Dependency Inversion Principle")
        
        # Interface Segregation Principle
        if self._check_interface_segregation(classes):
            principles.append("Interface Segregation Principle")
        
        return principles

    def _detect_evolution_indicators(self, analysis_data: Dict) -> List[Dict]:
        """Detect indicators of architecture evolution"""
        indicators = []
        
        classes = analysis_data.get('classes', [])
        functions = analysis_data.get('functions', [])
        
        # Check for legacy patterns
        legacy_indicators = self._identify_legacy_patterns(classes, functions)
        if legacy_indicators:
            indicators.extend(legacy_indicators)
        
        # Check for modern patterns
        modern_indicators = self._identify_modern_patterns(classes, functions)
        if modern_indicators:
            indicators.extend(modern_indicators)
        
        # Check for migration patterns
        migration_indicators = self._identify_migration_patterns(classes, functions)
        if migration_indicators:
            indicators.extend(migration_indicators)
        
        return indicators

    # Helper methods
    def _generate_pattern_description(self, pattern_name: str, cls: Dict) -> str:
        """Generate description for detected pattern"""
        descriptions = {
            'repository': f"Data access abstraction implemented in {cls.get('name', 'unknown')} class",
            'service': f"Business logic orchestration in {cls.get('name', 'unknown')} service",
            'factory': f"Object creation abstraction in {cls.get('name', 'unknown')} factory",
            'observer': f"Event notification pattern in {cls.get('name', 'unknown')}",
            'strategy': f"Algorithm encapsulation in {cls.get('name', 'unknown')} strategy",
            'decorator': f"Behavior enhancement pattern in {cls.get('name', 'unknown')}",
            'adapter': f"Interface adaptation in {cls.get('name', 'unknown')} adapter",
            'facade': f"Simplified interface in {cls.get('name', 'unknown')} facade"
        }
        
        return descriptions.get(pattern_name, f"{pattern_name.title()} pattern implementation")

    def _assess_pattern_implementation_quality(self, pattern_name: str, cls: Dict, classes: List[Dict]) -> float:
        """Assess quality of pattern implementation"""
        # Simplified quality assessment
        methods = cls.get('methods', [])
        
        quality_score = 0.5  # Base score
        
        # Check for proper interface usage
        base_classes = cls.get('base_classes', [])
        if any('interface' in base.lower() or 'abstract' in base.lower() for base in base_classes):
            quality_score += 0.2
        
        # Check for proper method naming
        method_names = [m.get('name', '') for m in methods]
        if pattern_name == 'repository':
            expected_methods = ['find', 'save', 'delete', 'get']
            if any(any(expected in method.lower() for expected in expected_methods) for method in method_names):
                quality_score += 0.2
        
        # Check for error handling
        if any(method.get('error_handling', {}) for method in methods):
            quality_score += 0.1
        
        return min(quality_score, 1.0)

    def _identify_pattern_participants(self, pattern_name: str, cls: Dict, classes: List[Dict]) -> List[str]:
        """Identify participants in the pattern"""
        participants = [cls.get('name', 'unknown')]
        
        if pattern_name == 'repository':
            # Look for related entity classes
            class_name = cls.get('name', '').replace('Repository', '').replace('Repo', '')
            for other_cls in classes:
                if class_name.lower() in other_cls.get('name', '').lower() and other_cls != cls:
                    participants.append(other_cls.get('name', ''))
        
        return participants

    def _get_pattern_intent(self, pattern_name: str) -> str:
        """Get the intent of the pattern"""
        intents = {
            'repository': "Encapsulate data access logic and provide a uniform interface to data",
            'service': "Encapsulate business logic and coordinate application operations",
            'factory': "Create objects without specifying their concrete classes",
            'observer': "Define one-to-many dependency between objects for notifications",
            'strategy': "Define family of algorithms and make them interchangeable",
            'decorator': "Add new functionality to objects dynamically",
            'adapter': "Allow incompatible interfaces to work together",
            'facade': "Provide simplified interface to complex subsystem"
        }
        
        return intents.get(pattern_name, f"Implement {pattern_name} pattern")

    def _get_pattern_consequences(self, pattern_name: str) -> List[str]:
        """Get consequences of using the pattern"""
        consequences = {
            'repository': ["Improved testability", "Database abstraction", "Centralized query logic"],
            'service': ["Business logic centralization", "Transaction management", "Improved maintainability"],
            'factory': ["Flexible object creation", "Reduced coupling", "Easier testing"],
            'observer': ["Loose coupling", "Dynamic relationships", "Broadcast communication"],
            'strategy': ["Algorithm flexibility", "Runtime selection", "Easier maintenance"],
            'decorator': ["Flexible enhancement", "Single responsibility", "Runtime composition"],
            'adapter': ["Legacy integration", "Interface compatibility", "Third-party integration"],
            'facade': ["Simplified interface", "Reduced complexity", "Improved usability"]
        }
        
        return consequences.get(pattern_name, ["Pattern-specific benefits"])

    def _collect_architectural_evidence(self, pattern_name: str, pattern_def: Dict, analysis_data: Dict) -> List[str]:
        """Collect evidence for architectural pattern"""
        evidence = []
        
        classes = analysis_data.get('classes', [])
        
        if 'layer_indicators' in pattern_def:
            for indicator in pattern_def['layer_indicators']:
                matching_classes = [cls.get('name', '') for cls in classes 
                                  if indicator.lower() in cls.get('name', '').lower()]
                if matching_classes:
                    evidence.append(f"{indicator.title()} layer: {', '.join(matching_classes[:3])}")
        
        return evidence

    def _extract_architectural_implementation(self, pattern_name: str, analysis_data: Dict) -> Dict:
        """Extract implementation details of architectural pattern"""
        implementation = {
            "components": [],
            "relationships": [],
            "communication_mechanisms": []
        }
        
        classes = analysis_data.get('classes', [])
        
        # Group classes by architectural role
        if pattern_name == 'layered':
            layers = {
                'presentation': [cls for cls in classes if any(word in cls.get('name', '').lower() 
                                                             for word in ['controller', 'view', 'api'])],
                'business': [cls for cls in classes if any(word in cls.get('name', '').lower() 
                                                          for word in ['service', 'manager', 'handler'])],
                'data': [cls for cls in classes if any(word in cls.get('name', '').lower() 
                                                      for word in ['repository', 'dao', 'model'])]
            }
            
            for layer_name, layer_classes in layers.items():
                if layer_classes:
                    implementation['components'].append({
                        'layer': layer_name,
                        'classes': [cls.get('name', '') for cls in layer_classes]
                    })
        
        return implementation

    def _get_architectural_benefits(self, pattern_name: str) -> List[str]:
        """Get benefits of architectural pattern"""
        benefits = {
            'layered': ["Clear separation of concerns", "Easy to maintain", "Testable layers"],
            'hexagonal': ["Business logic isolation", "Easy to test", "Flexible adapters"],
            'microservices': ["Independent deployment", "Technology diversity", "Scalability"],
            'event_driven': ["Loose coupling", "Scalability", "Responsiveness"],
            'cqrs': ["Optimized read/write", "Scalability", "Complex query support"]
        }
        
        return benefits.get(pattern_name, ["Pattern-specific benefits"])

    def _get_architectural_tradeoffs(self, pattern_name: str) -> List[str]:
        """Get trade-offs of architectural pattern"""
        tradeoffs = {
            'layered': ["Performance overhead", "Rigid structure", "Potential for god objects"],
            'hexagonal': ["Initial complexity", "More abstractions", "Learning curve"],
            'microservices': ["Distributed complexity", "Network overhead", "Data consistency"],
            'event_driven': ["Eventual consistency", "Complex debugging", "Event ordering"],
            'cqrs': ["Increased complexity", "Data synchronization", "Learning curve"]
        }
        
        return tradeoffs.get(pattern_name, ["Pattern-specific trade-offs"])

    def _analyze_error_handling_strategy(self, functions: List[Dict]) -> Optional[Dict]:
        """Analyze error handling strategy"""
        error_patterns = []
        
        for func in functions:
            if 'error_handling' in func:
                error_info = func['error_handling']
                if error_info.get('try_blocks', 0) > 0:
                    error_patterns.append('try_catch')
                if error_info.get('exception_types'):
                    error_patterns.append('specific_exceptions')
        
        if error_patterns:
            return {
                "decision": "Implement structured error handling",
                "rationale": "Provide consistent error management across application",
                "implementation": f"Error handling patterns: {', '.join(set(error_patterns))}",
                "consistency": "Applied across multiple functions",
                "evidence": [f"{len([f for f in functions if 'error_handling' in f])} functions with error handling"]
            }
        
        return None

    def _analyze_dependency_injection_usage(self, classes: List[Dict], functions: List[Dict]) -> Optional[Dict]:
        """Analyze dependency injection usage"""
        di_indicators = 0
        
        for cls in classes:
            methods = cls.get('methods', [])
            for method in methods:
                if method.get('name') == '__init__':
                    parameters = method.get('parameters', [])
                    # Check for dependency injection patterns
                    if len(parameters) > 1:  # More than just 'self'
                        di_indicators += 1
        
        if di_indicators > 0:
            return {
                "decision": "Use Dependency Injection pattern",
                "rationale": "Improve testability and reduce coupling",
                "implementation": f"Constructor injection in {di_indicators} classes",
                "consistency": "Applied in service and repository classes",
                "evidence": [f"{di_indicators} classes with injected dependencies"]
            }
        
        return None

    def _collect_quality_evidence(self, attr_name: str, indicators: List[str], classes: List[Dict], functions: List[Dict]) -> Dict:
        """Collect evidence for quality attributes"""
        evidence = {
            'strategies': [],
            'evidence': '',
            'score': 0.0
        }
        
        found_indicators = []
        
        # Check class and function names for quality indicators
        all_names = [cls.get('name', '').lower() for cls in classes] + [func.get('name', '').lower() for func in functions]
        
        for indicator in indicators:
            if any(indicator.replace(' ', '_') in name for name in all_names):
                found_indicators.append(indicator)
        
        # Check for specific patterns
        if attr_name == 'maintainability':
            # Check for separation of concerns
            if any('service' in name for name in all_names) and any('repository' in name for name in all_names):
                found_indicators.append('separation of concerns')
            
            # Check for modular design
            file_paths = set(cls.get('file_path', '') for cls in classes)
            if len(file_paths) > 3:
                found_indicators.append('modular design')
        
        elif attr_name == 'testability':
            # Check for dependency injection
            if any('inject' in name or '__init__' in [m.get('name', '') for m in cls.get('methods', [])] for cls in classes):
                found_indicators.append('dependency injection')
        
        if found_indicators:
            evidence['strategies'] = found_indicators
            evidence['evidence'] = f"Evidence found in {len(found_indicators)} components"
            evidence['score'] = min(len(found_indicators) / len(indicators), 1.0)
        
        return evidence

    def _check_repository_violations(self, classes: List[Dict], functions: List[Dict]) -> List[Dict]:
        """Check for repository pattern violations"""
        violations = []
        
        # Find repository classes
        repo_classes = [cls for cls in classes if 'repository' in cls.get('name', '').lower()]
        
        # Find classes that access data directly (violation)
        for cls in classes:
            if 'service' in cls.get('name', '').lower():
                methods = cls.get('methods', [])
                for method in methods:
                    calls = method.get('calls', [])
                    # Check if service directly accesses database
                    if any('database' in call.lower() or 'session' in call.lower() for call in calls):
                        violations.append({
                            "issue": f"{cls.get('name', 'Unknown')} directly accesses database",
                            "violation": "Repository pattern not followed",
                            "impact": "Medium - testing difficulty",
                            "files": [cls.get('file_path', 'unknown')]
                        })
        
        return violations

    def _check_service_violations(self, classes: List[Dict], functions: List[Dict]) -> List[Dict]:
        """Check for service layer violations"""
        violations = []
        
        # Check if controllers contain business logic
        for cls in classes:
            if 'controller' in cls.get('name', '').lower():
                methods = cls.get('methods', [])
                for method in methods:
                    # Check for business logic in controllers
                    if method.get('semantic_complexity', {}).get('business_rules', 0) > 2:
                        violations.append({
                            "issue": f"{cls.get('name', 'Unknown')} contains complex business logic",
                            "violation": "Business logic should be in service layer",
                            "impact": "Medium - maintainability issue",
                            "files": [cls.get('file_path', 'unknown')]
                        })
        
        return violations

    def _check_separation_concerns_violations(self, classes: List[Dict], functions: List[Dict]) -> List[Dict]:
        """Check for separation of concerns violations"""
        violations = []
        
        # Check for mixed responsibilities
        for cls in classes:
            class_name = cls.get('name', '').lower()
            methods = cls.get('methods', [])
            method_names = [m.get('name', '').lower() for m in methods]
            
            # Check if class has mixed responsibilities
            has_data_access = any('save' in name or 'find' in name for name in method_names)
            has_business_logic = any('calculate' in name or 'process' in name for name in method_names)
            has_presentation = any('render' in name or 'format' in name for name in method_names)
            
            mixed_count = sum([has_data_access, has_business_logic, has_presentation])
            
            if mixed_count > 1:
                violations.append({
                    "issue": f"{cls.get('name', 'Unknown')} has mixed responsibilities",
                    "violation": "Single Responsibility Principle violated",
                    "impact": "High - maintainability and testability issues",
                    "files": [cls.get('file_path', 'unknown')]
                })
        
        return violations

    def _check_controller_consistency(self, controllers: List[Dict]) -> Dict:
        """Check consistency across controllers"""
        if not controllers:
            return {"is_consistent": True, "violations": []}
        
        # Check method naming patterns
        all_method_patterns = []
        for controller in controllers:
            methods = controller.get('methods', [])
            method_names = [m.get('name', '') for m in methods]
            all_method_patterns.extend(method_names)
        
        # Simple consistency check - all controllers should have similar patterns
        common_patterns = ['get', 'post', 'put', 'delete']
        consistent = all(any(pattern in method.lower() for method in all_method_patterns) 
                        for pattern in common_patterns)
        
        return {
            "is_consistent": consistent,
            "violations": [] if consistent else ["Inconsistent HTTP method patterns across controllers"]
        }

    def _check_service_consistency(self, services: List[Dict]) -> Dict:
        """Check consistency across services"""
        if not services:
            return {"is_consistent": True, "violations": []}
        
        # Check if all services follow similar patterns
        violations = []
        
        # Check for constructor injection consistency
        injection_count = 0
        for service in services:
            methods = service.get('methods', [])
            init_method = next((m for m in methods if m.get('name') == '__init__'), None)
            if init_method and len(init_method.get('parameters', [])) > 1:
                injection_count += 1
        
        if injection_count > 0 and injection_count < len(services):
            violations.append("Inconsistent dependency injection across services")
        
        return {
            "is_consistent": len(violations) == 0,
            "violations": violations
        }

    def _check_error_handling_consistency(self, functions: List[Dict]) -> Dict:
        """Check error handling consistency"""
        functions_with_error_handling = [f for f in functions if 'error_handling' in f]
        
        if not functions_with_error_handling:
            return {"is_consistent": True, "violations": []}
        
        # Check for consistent error handling patterns
        error_patterns = set()
        for func in functions_with_error_handling:
            error_info = func.get('error_handling', {})
            if error_info.get('try_blocks', 0) > 0:
                error_patterns.add('try_catch')
            if error_info.get('exception_types'):
                error_patterns.add('specific_exceptions')
        
        # If we have multiple patterns, it might be consistent
        consistent = len(error_patterns) > 0
        
        return {
            "is_consistent": consistent,
            "violations": [] if consistent else ["No consistent error handling strategy"]
        }

    def _check_single_responsibility(self, classes: List[Dict]) -> bool:
        """Check if Single Responsibility Principle is followed"""
        # Simple check - classes with focused names and limited methods
        focused_classes = 0
        
        for cls in classes:
            methods = cls.get('methods', [])
            # Classes with specific names and reasonable method count
            if (('service' in cls.get('name', '').lower() or 
                 'repository' in cls.get('name', '').lower() or
                 'controller' in cls.get('name', '').lower()) and 
                len(methods) <= 10):
                focused_classes += 1
        
        return focused_classes > len(classes) * 0.7  # 70% of classes are focused

    def _check_open_closed(self, classes: List[Dict]) -> bool:
        """Check if Open/Closed Principle is followed"""
        # Check for interfaces and abstract classes
        abstract_classes = 0
        
        for cls in classes:
            base_classes = cls.get('base_classes', [])
            if any('abstract' in base.lower() or 'interface' in base.lower() or 'abc' in base.lower() 
                  for base in base_classes):
                abstract_classes += 1
        
        return abstract_classes > 0

    def _check_dependency_inversion(self, classes: List[Dict]) -> bool:
        """Check if Dependency Inversion Principle is followed"""
        # Check for dependency injection patterns
        di_classes = 0
        
        for cls in classes:
            methods = cls.get('methods', [])
            init_method = next((m for m in methods if m.get('name') == '__init__'), None)
            if init_method:
                parameters = init_method.get('parameters', [])
                # Check for injected dependencies (more than just 'self')
                if len(parameters) > 1:
                    di_classes += 1
        
        return di_classes > len(classes) * 0.3  # 30% use dependency injection

    def _check_interface_segregation(self, classes: List[Dict]) -> bool:
        """Check if Interface Segregation Principle is followed"""
        # Check for small, focused interfaces
        small_interfaces = 0
        
        for cls in classes:
            base_classes = cls.get('base_classes', [])
            methods = cls.get('methods', [])
            
            # If it's an interface-like class with few methods
            if (any('interface' in base.lower() or 'abstract' in base.lower() 
                   for base in base_classes) and len(methods) <= 5):
                small_interfaces += 1
        
        return small_interfaces > 0

    def _identify_legacy_patterns(self, classes: List[Dict], functions: List[Dict]) -> List[Dict]:
        """Identify legacy patterns"""
        legacy_indicators = []
        
        # Check for god classes
        for cls in classes:
            methods = cls.get('methods', [])
            if len(methods) > 20:
                legacy_indicators.append({
                    "type": "legacy_pattern",
                    "pattern": "God Class",
                    "location": cls.get('name', 'unknown'),
                    "description": "Large class with too many responsibilities"
                })
        
        return legacy_indicators

    def _identify_modern_patterns(self, classes: List[Dict], functions: List[Dict]) -> List[Dict]:
        """Identify modern patterns"""
        modern_indicators = []
        
        # Check for async patterns
        async_functions = [f for f in functions if f.get('is_async', False)]
        if async_functions:
            modern_indicators.append({
                "type": "modern_pattern",
                "pattern": "Async/Await",
                "location": f"{len(async_functions)} functions",
                "description": "Modern asynchronous programming patterns"
            })
        
        return modern_indicators

    def _identify_migration_patterns(self, classes: List[Dict], functions: List[Dict]) -> List[Dict]:
        """Identify migration patterns"""
        migration_indicators = []
        
        # Check for adapter patterns (might indicate migration)
        adapters = [cls for cls in classes if 'adapter' in cls.get('name', '').lower()]
        if adapters:
            migration_indicators.append({
                "type": "migration_pattern",
                "pattern": "Legacy Integration",
                "location": ', '.join([cls.get('name', '') for cls in adapters]),
                "description": "Adapter pattern suggests integration with legacy systems"
            })
        
        return migration_indicators
