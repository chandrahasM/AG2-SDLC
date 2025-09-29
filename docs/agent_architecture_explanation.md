# Multi-Agent Architecture: Repository Analyzer & Design Agents

## 🏗️ **Overview**

The multi-agent system consists of **4 specialized agents** that work together to analyze code repositories, understand requirements, and propose design changes. Here's how they coordinate:

## 🤖 **Agent 1: Repository Analyzer Agent**

### **Purpose**
The **Repository Analyzer Agent** is the foundation of the system. It analyzes existing codebases to create a comprehensive understanding of the current system.

### **How It Works**

#### **Phase 1: Fast Python Analysis**
```python
# Uses AST parsing and regex patterns for structural analysis
file_analyses = self._analyze_files(repo_path, file_patterns)
```
- **Input**: Repository path, file patterns (`.tsx`, `.ts`, `.jsx`, `.js`)
- **Process**: 
  - Scans files using `ReactASTParser`
  - Extracts components, services, hooks, state, props
  - Filters out `node_modules`, test files, config files
  - Focuses only on business logic files
- **Output**: Structured file analysis with components, services, dependencies

#### **Phase 2: Component Relationship Analysis**
```python
component_analysis = self.component_analyzer.analyze_components(file_analyses)
```
- **Process**: Maps component dependencies and relationships
- **Output**: Component interaction matrix, data flow patterns

#### **Phase 3: LLM Semantic Analysis**
```python
semantic_analysis = self._run_comprehensive_llm_analysis(file_analyses, component_analysis)
```
- **Process**: Uses specialized LLM agents for deep semantic understanding
- **Agents Used**:
  - `component_analyzer_agent`: Analyzes React components
  - `business_logic_agent`: Extracts business rules and workflows
  - `architecture_agent`: Identifies patterns and design decisions
  - `api_analyzer_agent`: Analyzes API contracts and service integration
  - `performance_analyzer_agent`: Assesses performance characteristics

#### **Phase 4-8: Comprehensive Analysis**
- **API Contract Analysis**: Extracts API endpoints, schemas, authentication
- **State Flow Analysis**: Maps state variables, mutations, side effects
- **Error Handling Strategy**: Identifies error boundaries, propagation patterns
- **Performance Analysis**: Bundle size, render optimization, memory usage
- **Testing Strategy**: Unit, integration, E2E test recommendations

### **Key Outputs for Design Agents**

```json
{
  "repository_metadata": { "design_agent_ready": true },
  "semantic_analysis": {
    "components": { "App": { "purpose": "...", "business_role": "..." } },
    "services": { "weatherService": { "methods": {...} } }
  },
  "component_interactions": {
    "App": {
      "renders": ["SearchForm", "WeatherCard"],
      "passes_data_to": { "WeatherCard": { "location": "string" } },
      "receives_from": { "SearchForm": ["search_query"] }
    }
  },
  "api_contracts": { "weather_service": { "endpoints": {...} } },
  "state_flow_analysis": { "state_variables": {...} },
  "business_capabilities": [{ "name": "Weather Data Display", "business_value": "..." }],
  "architectural_patterns": [{ "pattern": "Component-based Architecture" }],
  "code_quality_assessment": { "overall_score": 7.5 },
  "recommendations": { "immediate": [...], "short_term": [...], "long_term": [...] }
}
```

---

## 🎯 **Agent 2: Design Analyzer Agent**

### **Purpose**
The **Design Analyzer Agent** compares existing design documents with new requirements to identify gaps and conflicts.

### **How It Works**

#### **Phase 1: Parse Existing Design**
```python
design_components = self._parse_existing_design(existing_design)
```
- **Input**: Current design document (features, components, user stories, APIs)
- **Process**: Extracts structured design elements
- **Output**: Parsed design components

#### **Phase 2: Parse New Requirements**
```python
requirement_components = self._parse_new_requirements(new_requirements)
```
- **Input**: New requirements (features, components, user stories, APIs)
- **Process**: Structures new requirements for comparison
- **Output**: Parsed requirement components

#### **Phase 3: Compare and Identify Gaps**
```python
gap_analysis = self._compare_designs(design_components, requirement_components)
```
- **Process**: 
  - Compares features, components, APIs, data models
  - Identifies missing, modified, and removed features
  - Detects conflicts and inconsistencies
- **Output**: Comprehensive gap analysis

#### **Phase 4: Analyze Impact**
```python
impact_analysis = self._analyze_impact(gap_analysis, code_analysis)
```
- **Process**:
  - Maps gaps to affected components and files
  - Identifies breaking changes
  - Assesses migration effort
  - Generates testing requirements
- **Output**: Impact analysis with affected files and breaking changes

### **Key Outputs**

```json
{
  "gap_analysis": {
    "missing_features": [{ "name": "7-day forecast", "priority": "high" }],
    "new_components_needed": [{ "name": "ForecastCard", "type": "component" }],
    "existing_components_to_modify": [{ "name": "WeatherCard", "changes": [...] }],
    "api_changes": [{ "type": "new", "endpoint": "/api/forecast" }]
  },
  "impact_analysis": {
    "affected_components": [...],
    "breaking_changes": [...],
    "migration_effort": "medium"
  }
}
```

---

## 🏛️ **Agent 3: Design Architect Agent**

### **Purpose**
The **Design Architect Agent** takes gap analysis results and creates detailed design specifications for implementation.

### **How It Works**

#### **Phase 1: Analyze Design Structure**
```python
design_structure = self._analyze_design_structure(existing_design)
```
- **Process**: Analyzes current design document structure
- **Output**: Design structure analysis

#### **Phase 2: Plan Design Updates**
```python
update_plan = self._plan_design_updates(gap_analysis, impact_analysis)
```
- **Process**: 
  - Plans new features, components, APIs
  - Identifies components to modify
  - Creates priority order and implementation phases
- **Output**: Comprehensive update plan

#### **Phase 3: Design New Components**
```python
new_component_designs = self._design_new_components(gap_analysis)
```
- **Process**: Creates detailed component specifications including:
  - Props interfaces with types and validation
  - State interfaces with business purpose
  - Lifecycle methods and event handlers
  - Business logic and styling requirements
  - Accessibility requirements
- **Output**: Detailed component designs

#### **Phase 4: Update Existing Components**
```python
updated_component_designs = self._update_existing_components(gap_analysis)
```
- **Process**: 
  - Identifies required changes to existing components
  - Creates migration guides
  - Assesses backward compatibility
- **Output**: Component update specifications

#### **Phase 5: Design API Changes**
```python
api_designs = self._design_api_changes(gap_analysis)
```
- **Process**: 
  - Designs new API endpoints with parameters and responses
  - Plans API modifications with versioning strategy
  - Creates error handling specifications
- **Output**: API design specifications

#### **Phase 6: Create Implementation Plan**
```python
implementation_plan = self._create_implementation_plan(update_plan, impact_analysis)
```
- **Process**: 
  - Creates phased implementation plan
  - Estimates resources and timeline
  - Assesses risks and defines success metrics
- **Output**: Detailed implementation plan

### **Key Outputs**

```json
{
  "updated_design": {
    "version": "2.0",
    "features": [...],
    "components": [...],
    "api_endpoints": [...],
    "implementation_plan": {...}
  },
  "new_components": [{
    "name": "ForecastCard",
    "props_interface": { "properties": [...] },
    "state_interface": { "properties": [...] },
    "business_logic": [...],
    "styling_requirements": {...}
  }],
  "implementation_plan": {
    "phases": [...],
    "timeline": "6-8 weeks",
    "resource_requirements": {...}
  }
}
```

---

## 🔄 **Agent 4: Code Generation Agent**

### **Purpose**
The **Code Generation Agent** takes the updated design specifications and generates actual code implementations.

### **How It Works**

#### **Phase 1: Parse Design Specifications**
```python
specifications = self._parse_design_specifications(updated_design)
```
- **Input**: Updated design document with component specifications
- **Process**: Extracts implementation details
- **Output**: Parsed specifications

#### **Phase 2: Generate Component Code**
```python
component_code = self._generate_component_code(component_spec)
```
- **Process**: 
  - Generates TypeScript interfaces
  - Creates React component structure
  - Implements business logic
  - Adds event handlers and lifecycle methods
- **Output**: Complete component code

#### **Phase 3: Generate Service Code**
```python
service_code = self._generate_service_code(api_spec)
```
- **Process**: 
  - Generates API service functions
  - Implements error handling
  - Creates data transformation logic
- **Output**: Service layer code

#### **Phase 4: Generate Test Code**
```python
test_code = self._generate_test_code(component_spec, test_strategy)
```
- **Process**: 
  - Generates unit tests for components
  - Creates integration tests
  - Implements E2E test scenarios
- **Output**: Comprehensive test suite

---

## 🔄 **Agent Coordination Flow**

### **1. Repository Analysis → Design Analysis**
```
Repository Analyzer Output → Design Analyzer Input
```
- **Data Flow**: Code analysis results feed into gap analysis
- **Purpose**: Design analyzer uses current code state to identify what needs to change

### **2. Design Analysis → Design Architecture**
```
Gap Analysis → Design Architect Input
```
- **Data Flow**: Gap analysis results drive design updates
- **Purpose**: Design architect creates detailed specifications based on identified gaps

### **3. Design Architecture → Code Generation**
```
Updated Design → Code Generation Input
```
- **Data Flow**: Design specifications become code generation requirements
- **Purpose**: Code generator implements the designed specifications

### **4. Feedback Loop**
```
Code Generation → Repository Analysis (for validation)
```
- **Data Flow**: Generated code can be re-analyzed to validate implementation
- **Purpose**: Ensures generated code matches design specifications

---

## 🎯 **Key AG2 Concepts Used**

### **1. ConversableAgent**
- **Purpose**: Each agent is a `ConversableAgent` with specialized system messages
- **Benefits**: Enables natural language communication between agents
- **Usage**: Agents can ask questions, provide feedback, and coordinate tasks

### **2. LLMConfig**
- **Purpose**: Centralized LLM configuration for all agents
- **Benefits**: Consistent model usage across the system
- **Usage**: Each agent uses the same LLM configuration for consistency

### **3. System Messages**
- **Purpose**: Define each agent's role and capabilities
- **Benefits**: Clear specialization and focused responsibilities
- **Usage**: Each agent has a detailed system message explaining its purpose

### **4. Tool Calling**
- **Purpose**: Agents can call specialized tools for analysis
- **Benefits**: Combines LLM intelligence with structured analysis
- **Usage**: Repository analyzer uses AST parsing tools, component analysis tools

### **5. Structured Outputs**
- **Purpose**: Agents produce structured JSON outputs
- **Benefits**: Enables programmatic processing by other agents
- **Usage**: Each agent's output is designed for consumption by the next agent

---

## 🚀 **Example: Adding 7-Day Forecast Feature**

### **Step 1: Repository Analysis**
```python
# Repository Analyzer analyzes current weather app
repo_analysis = repository_analyzer.analyze_repository("weather-app/")
# Output: Current components (App, WeatherCard, SearchForm), services, APIs
```

### **Step 2: Design Analysis**
```python
# Design Analyzer compares current design with new requirement
gap_analysis = design_analyzer.analyze_design_gaps(
    existing_design=current_design,
    new_requirements={"features": [{"name": "7-day forecast"}]},
    code_analysis=repo_analysis
)
# Output: Missing forecast feature, need ForecastCard component, need /api/forecast API
```

### **Step 3: Design Architecture**
```python
# Design Architect creates detailed specifications
updated_design = design_architect.update_design_document(
    existing_design=current_design,
    gap_analysis=gap_analysis,
    impact_analysis=impact_analysis
)
# Output: Detailed ForecastCard component spec, API design, implementation plan
```

### **Step 4: Code Generation**
```python
# Code Generator creates actual code
generated_code = code_generator.generate_code(updated_design)
# Output: ForecastCard.tsx, forecastService.ts, tests, updated App.tsx
```

---

## 🎯 **Benefits of This Architecture**

### **1. Separation of Concerns**
- Each agent has a clear, focused responsibility
- Easy to modify or replace individual agents
- Clear data flow between agents

### **2. Scalability**
- Can add new agents for specific tasks
- Agents can be run in parallel where possible
- Easy to extend functionality

### **3. Maintainability**
- Each agent is independently testable
- Clear interfaces between agents
- Easy to debug and troubleshoot

### **4. Flexibility**
- Can work with different types of repositories
- Adaptable to different design methodologies
- Supports various code generation approaches

### **5. Intelligence**
- LLM-powered semantic understanding
- Context-aware decision making
- Natural language communication between agents

This architecture provides a robust, intelligent system for analyzing codebases, understanding requirements, and generating design changes with minimal human intervention! 🚀
