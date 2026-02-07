# Todo AI Chatbot - Agent Architecture

## Overview
This document defines the multi-agent architecture for the Todo AI Chatbot project, following the Agentic Dev Stack workflow with Claude Code.

---

## Agent Ecosystem

### 1. MCP Server Agent
**Purpose**: Build and manage the Model Context Protocol server with all tool implementations

**Skills**:
- `mcp_tool_generator` - Generates MCP tool definitions from specifications
- `mcp_server_builder` - Creates FastAPI server with MCP integration
- `tool_validator` - Validates tool inputs/outputs against MCP spec

**Responsibilities**:
- Create MCP server with Official MCP SDK
- Implement all 5 tools: add_task, list_tasks, complete_task, delete_task, update_task
- Ensure stateless design with database persistence
- Handle tool registration and discovery

**Input**: Tool specifications, database schema
**Output**: Complete MCP server implementation

---

### 2. Database Schema Agent
**Purpose**: Design and manage database models and migrations

**Skills**:
- `sqlmodel_generator` - Creates SQLModel models from spec
- `migration_builder` - Generates Alembic migration scripts
- `relationship_mapper` - Defines database relationships

**Responsibilities**:
- Create Task, Conversation, and Message models
- Set up foreign key relationships
- Generate migration scripts
- Ensure proper indexing for user_id queries

**Input**: Database specification from requirements
**Output**: SQLModel models, migration scripts

---

### 3. API Backend Agent
**Purpose**: Build FastAPI backend with chat endpoint and business logic

**Skills**:
- `fastapi_endpoint_builder` - Creates REST API endpoints
- `stateless_handler` - Implements stateless request handling
- `error_handler` - Generates error handling middleware

**Responsibilities**:
- Implement POST /api/{user_id}/chat endpoint
- Handle conversation state from database
- Integrate with OpenAI Agents SDK
- Return responses with tool call metadata

**Input**: API specification, MCP tools
**Output**: FastAPI application with chat endpoint

---

### 4. AI Agent Manager
**Purpose**: Configure and orchestrate OpenAI Agents SDK with MCP tools

**Skills**:
- `agent_config_builder` - Creates agent configurations
- `tool_integrator` - Integrates MCP tools with AI agent
- `prompt_engineer` - Designs system prompts for agent behavior

**Responsibilities**:
- Initialize OpenAI Agents SDK
- Configure agent with MCP tools
- Design system prompts for natural language understanding
- Implement conversation context management
- Handle agent behavior specifications (task creation, listing, etc.)

**Input**: MCP tool definitions, behavior specifications
**Output**: Configured AI agent with proper prompts

---

### 5. UI Agent (Image-to-UI Conversion)
**Purpose**: Analyze UI mockup images and generate ChatKit-based frontend code

**Skills**:
- `image_analyzer` - Analyzes UI mockups using vision capabilities
- `chatkit_generator` - Generates OpenAI ChatKit configurations
- `component_builder` - Creates React components from designs
- `style_extractor` - Extracts colors, layouts, and styling from images

**Responsibilities**:
- Accept UI mockup images as input
- Analyze layout, components, and design elements
- Generate ChatKit configuration for chat interface
- Create custom styling to match mockup
- Generate responsive design code
- Ensure domain allowlist configuration

**Input**: UI mockup images (PNG, JPG, Figma exports)
**Output**:
- ChatKit configuration files
- Custom CSS/styling
- React component code
- Deployment configuration

**Example Workflow**:
1. Receive mockup image of chat interface
2. Identify chat bubble styles, colors, layouts
3. Extract header design, input field styling
4. Generate ChatKit config with custom theme
5. Create additional React components for custom elements
6. Output complete frontend codebase

---

### 6. Testing Agent
**Purpose**: Generate comprehensive test suites for all components

**Skills**:
- `pytest_generator` - Creates pytest test cases
- `integration_tester` - Builds integration tests
- `mock_generator` - Creates test mocks and fixtures

**Responsibilities**:
- Generate unit tests for MCP tools
- Create integration tests for API endpoints
- Test agent behavior with various inputs
- Mock database and external services
- Ensure >80% code coverage

**Input**: Implementation code
**Output**: Pytest test suites, fixtures, mocks

---

### 7. Documentation Agent
**Purpose**: Generate comprehensive documentation

**Skills**:
- `readme_generator` - Creates README files
- `api_doc_builder` - Generates API documentation
- `setup_guide_creator` - Writes setup instructions

**Responsibilities**:
- Generate README with setup instructions
- Document API endpoints (OpenAPI/Swagger)
- Create MCP tool documentation
- Write deployment guides
- Document environment variables

**Input**: All implementation code
**Output**: Complete documentation suite

---

### 8. Deployment Agent
**Purpose**: Handle deployment and infrastructure setup

**Skills**:
- `vercel_deployer` - Configures Vercel deployment
- `docker_builder` - Creates Dockerfiles and compose files
- `env_manager` - Manages environment configuration

**Responsibilities**:
- Create deployment configurations
- Set up environment variables
- Configure OpenAI domain allowlist
- Generate Docker files for backend
- Create Vercel config for frontend
- Document deployment steps

**Input**: Complete application code
**Output**: Deployment configurations, Docker files

---

## Agent Orchestration Flow

```
User Requirement
    ↓
[Database Schema Agent] → Creates models and migrations
    ↓
[MCP Server Agent] → Builds MCP tools using DB models
    ↓
[AI Agent Manager] → Configures OpenAI agent with MCP tools
    ↓
[API Backend Agent] → Creates FastAPI endpoint integrating agent
    ↓
[UI Agent] → Analyzes mockup and generates ChatKit frontend
    ↓
[Testing Agent] → Generates test suites for all components
    ↓
[Documentation Agent] → Creates comprehensive docs
    ↓
[Deployment Agent] → Configures deployment
    ↓
Complete Application
```

---

## UI Agent - Detailed Specification

### Image Analysis Capabilities
The UI Agent uses Claude's vision capabilities to:
1. Identify chat interface layout (header, message list, input area)
2. Extract color schemes and branding
3. Detect component hierarchy
4. Recognize interaction patterns
5. Identify responsive breakpoints

### Generation Process
1. **Image Input**: Accept PNG, JPG, or Figma export
2. **Analysis**: Use vision model to identify:
   - Chat bubble styles (rounded corners, shadows, colors)
   - Message alignment (left/right for user/assistant)
   - Input field design (border, placeholder, button)
   - Header elements (title, user info, actions)
   - Color palette and typography
3. **ChatKit Configuration**: Generate:
   - Theme configuration (colors, fonts, spacing)
   - Custom CSS for non-standard elements
   - Component overrides for ChatKit defaults
4. **Custom Components**: Create React components for:
   - Custom headers
   - Special message types
   - Action buttons
   - Loading states
5. **Responsive Design**: Ensure mobile/desktop compatibility

### Example UI Agent Prompt
```
Analyze this chat interface mockup and generate a complete ChatKit implementation:

1. Identify all visual elements (colors, spacing, fonts)
2. Generate ChatKit theme configuration
3. Create custom CSS for unique elements
4. Build React components for custom features
5. Ensure responsive design
6. Include domain allowlist setup instructions
```

---

## Agent Communication Protocol

Agents communicate through:
1. **Shared Spec Files**: Common specification documents
2. **File Outputs**: Agents read each other's generated files
3. **Metadata Files**: JSON/YAML configs for cross-agent data
4. **Claude Code Context**: All agents run in same conversation context

---

## Implementation Strategy

### Phase 1: Foundation
1. Database Schema Agent creates models
2. MCP Server Agent builds tool infrastructure

### Phase 2: Intelligence
3. AI Agent Manager configures OpenAI agent
4. API Backend Agent builds endpoint

### Phase 3: Interface
5. UI Agent generates frontend from mockup
6. Integrate frontend with backend

### Phase 4: Quality
7. Testing Agent generates test suites
8. Run tests and fix issues

### Phase 5: Delivery
9. Documentation Agent creates docs
10. Deployment Agent sets up deployment

---

## Success Criteria

- All agents complete their tasks without manual coding
- Generated code follows specifications exactly
- MCP tools work with OpenAI Agents SDK
- UI matches mockup design (if provided)
- All tests pass
- Application deploys successfully
- Documentation is complete and accurate

---

## Technology Stack Per Agent

| Agent | Primary Technologies |
|-------|---------------------|
| MCP Server Agent | Python, FastAPI, Official MCP SDK |
| Database Schema Agent | SQLModel, Alembic, PostgreSQL/SQLite |
| API Backend Agent | FastAPI, Pydantic, Python typing |
| AI Agent Manager | OpenAI Agents SDK, OpenAI API |
| UI Agent | React, OpenAI ChatKit, CSS-in-JS |
| Testing Agent | Pytest, pytest-asyncio, httpx |
| Documentation Agent | Markdown, OpenAPI/Swagger |
| Deployment Agent | Docker, Vercel, environment configs |

---

## Notes

- All agents should be stateless where possible
- Each agent should validate its inputs
- Agents should log their activities
- Error handling should be comprehensive
- Code should be production-ready, not prototype quality
