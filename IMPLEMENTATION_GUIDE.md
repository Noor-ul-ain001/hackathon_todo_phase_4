# Todo AI Chatbot - Implementation Guide with Claude Code

## Overview
This guide shows you how to use Claude Code and the Agentic Dev Stack to build the entire Todo AI Chatbot application using specialized agents.

---

## Prerequisites

1. **Claude Code CLI** installed and configured
2. **Spec-Kit Plus** for specification management
3. **OpenAI API Key** for Agents SDK
4. **Git** repository initialized
5. **Node.js** and **Python 3.10+** installed

---

## Phase 1: Foundation - Database & MCP Server

### Step 1: Initialize Project with Claude Code

```bash
# Create project directory
mkdir todo-ai-chatbot
cd todo-ai-chatbot

# Initialize git
git init

# Start Claude Code session
claude-code
```

### Step 2: Database Schema Agent

**Prompt for Claude Code:**
```
I'm building a Todo AI Chatbot following the Agentic Dev Stack workflow.

Please act as the Database Schema Agent and create:

1. SQLModel models for three tables:
   - Task: user_id, id, title, description, completed, created_at, updated_at
   - Conversation: user_id, id, created_at, updated_at
   - Message: user_id, id, conversation_id, role (user/assistant), content, created_at

2. Database connection management with async SQLAlchemy
3. Alembic migration setup and initial migration
4. Query utility functions
5. Seed data for development testing

Use these specifications: [paste DATABASE_SCHEMA_AGENT_SPEC.md]

Create a backend/database/ directory with all necessary files.
```

**Expected Output:**
- `backend/database/models.py`
- `backend/database/connection.py`
- `backend/database/queries.py`
- `backend/database/seed.py`
- `alembic/versions/001_initial_schema.py`
- `alembic/env.py`
- `alembic.ini`

### Step 3: MCP Server Agent

**Prompt for Claude Code:**
```
Please act as the MCP Server Agent.

Using the database models just created, implement an MCP server with these 5 tools:

1. add_task - Create new task
2. list_tasks - Retrieve tasks with status filter
3. complete_task - Mark task as complete
4. delete_task - Remove task
5. update_task - Modify task

Requirements:
- Use Official MCP SDK
- All tools must be stateless
- Validate all inputs
- Include user_id in all operations
- Return standardized output formats

Reference: [paste MCP_SERVER_AGENT_SPEC.md]

Create mcp_server/ directory with FastAPI integration.
```

**Expected Output:**
- `mcp_server/main.py`
- `mcp_server/server.py`
- `mcp_server/tools/add_task.py`
- `mcp_server/tools/list_tasks.py`
- `mcp_server/tools/complete_task.py`
- `mcp_server/tools/delete_task.py`
- `mcp_server/tools/update_task.py`
- `mcp_server/validation.py`

### Step 4: Test Foundation

**Prompt for Claude Code:**
```
Create pytest tests for:
1. All database models
2. Database queries
3. All 5 MCP tools
4. Input validation

Run the tests and fix any issues.
```

---

## Phase 2: Intelligence - AI Agent & API

### Step 5: AI Agent Manager

**Prompt for Claude Code:**
```
Please act as the AI Agent Manager.

Create an OpenAI Agents SDK integration that:

1. Configures an assistant with all 5 MCP tools
2. Implements conversation management with database persistence
3. Handles tool call execution via MCP server
4. Provides natural language understanding for task intents
5. Includes comprehensive error handling

Behavior requirements:
- Friendly, conversational tone
- Always confirm actions
- Handle ambiguous requests gracefully
- Extract clear task titles from user messages

Reference: [paste AI_AGENT_MANAGER_SPEC.md]

Create backend/agent/ directory with all components.
```

**Expected Output:**
- `backend/agent/config.py`
- `backend/agent/conversation.py`
- `backend/agent/tool_executor.py`
- `backend/agent/prompts.py`
- `backend/agent/error_handlers.py`

### Step 6: API Backend Agent

**Prompt for Claude Code:**
```
Create a FastAPI backend with a stateless chat endpoint:

POST /api/{user_id}/chat

Request:
- conversation_id (optional, creates new if not provided)
- message (required)

Response:
- conversation_id
- response (assistant message)
- tool_calls (array of tools invoked)

Requirements:
- Fetch conversation history from database
- Store user message in database
- Run OpenAI agent with MCP tools
- Store assistant response in database
- Return stateless response

Create backend/api/ directory with chat endpoint and dependencies.
```

**Expected Output:**
- `backend/api/chat.py`
- `backend/api/dependencies.py`
- `backend/main.py` (FastAPI app)

---

## Phase 3: Interface - UI Agent with Image Analysis

### Step 7: Prepare UI Mockup (Optional)

If you have a UI mockup:
- Save as `ui-mockup.png` or similar
- Can be a screenshot, Figma export, or hand-drawn sketch

If you don't have a mockup, Claude Code can use default ChatKit styling.

### Step 8: UI Agent - Image to UI Conversion

**Prompt for Claude Code with Mockup:**
```
Please act as the UI Agent with image analysis capabilities.

I'm attaching a mockup of my desired chat interface [attach ui-mockup.png].

Analyze this image and generate a complete ChatKit-based frontend that matches the design:

1. Use your vision capabilities to identify:
   - Color scheme
   - Layout structure (header, messages, input)
   - Component styles (chat bubbles, buttons, inputs)
   - Typography (fonts, sizes)
   - Spacing and padding
   - Animation hints (if any)

2. Generate:
   - Next.js project with ChatKit
   - Custom theme configuration matching the mockup
   - Custom CSS for unique elements
   - React components for custom features
   - API integration with backend
   - Responsive design (mobile/tablet/desktop)

3. Include:
   - Environment configuration
   - OpenAI domain allowlist setup instructions
   - Deployment configuration for Vercel

Reference: [paste UI_AGENT_SPEC.md]

Backend API URL: http://localhost:8000

Create frontend/ directory with complete implementation.
```

**Prompt for Claude Code without Mockup:**
```
Please act as the UI Agent.

Create a ChatKit-based frontend for the Todo AI Chatbot with a modern, clean design:

1. Generate Next.js project with OpenAI ChatKit
2. Create a professional theme:
   - Primary color: Blue (#3B82F6)
   - Clean, modern chat bubbles
   - Clear visual distinction between user/assistant messages
   - Professional header with title
   - Smooth animations

3. Features:
   - Message history display
   - Input field with send button
   - Loading states
   - Error handling
   - Responsive design

4. Integration:
   - Connect to backend API at http://localhost:8000
   - Handle conversation state
   - Display tool calls (optional debugging info)

Reference: [paste UI_AGENT_SPEC.md]

Create frontend/ directory with complete implementation.
```

**Expected Output:**
- `frontend/package.json`
- `frontend/pages/_app.tsx`
- `frontend/pages/index.tsx`
- `frontend/components/CustomHeader.tsx`
- `frontend/components/MessageBubble.tsx`
- `frontend/styles/theme.css`
- `frontend/styles/variables.css`
- `frontend/lib/api.ts`
- `frontend/.env.local.example`
- `frontend/README.md`

---

## Phase 4: Quality - Testing & Documentation

### Step 9: Testing Agent

**Prompt for Claude Code:**
```
Please act as the Testing Agent.

Create comprehensive test suites for all components:

1. Frontend tests (Jest + React Testing Library):
   - Component rendering
   - User interactions
   - API integration
   - Error states

2. Backend tests (Pytest):
   - Database operations
   - MCP tools
   - Agent conversation flow
   - API endpoints
   - Error handling

3. Integration tests:
   - Full chat flow
   - Tool execution
   - State persistence

Generate all test files and ensure >80% coverage.
Run tests and fix any failures.
```

### Step 10: Documentation Agent

**Prompt for Claude Code:**
```
Please act as the Documentation Agent.

Create comprehensive documentation:

1. Main README.md with:
   - Project overview
   - Architecture diagram
   - Setup instructions
   - Environment variables
   - Running the application
   - Development workflow

2. API documentation (OpenAPI/Swagger)

3. MCP Tools documentation

4. Frontend component documentation

5. Deployment guide:
   - Backend deployment options
   - Frontend deployment to Vercel
   - OpenAI domain allowlist setup
   - Environment configuration

6. Development guide:
   - Adding new tools
   - Modifying agent behavior
   - Customizing UI theme

Generate all documentation files.
```

---

## Phase 5: Deployment

### Step 11: Deployment Agent

**Prompt for Claude Code:**
```
Please act as the Deployment Agent.

Create deployment configurations:

1. Docker setup:
   - Dockerfile for backend
   - docker-compose.yml for local development
   - Include database, MCP server, and API

2. Vercel configuration for frontend:
   - vercel.json
   - Build configuration
   - Environment variable setup

3. Environment management:
   - .env.example files
   - Configuration validation
   - Secrets management guide

4. OpenAI domain allowlist setup:
   - Instructions for adding domain
   - Getting domain key
   - Configuring ChatKit

5. CI/CD setup (optional):
   - GitHub Actions workflow
   - Automated testing
   - Deployment pipeline

Generate all deployment files and instructions.
```

---

## Complete Implementation Workflow

### Timeline

```
Day 1: Foundation
├─ Initialize project
├─ Database Schema Agent → Models & migrations
├─ MCP Server Agent → Tools implementation
└─ Test foundation

Day 2: Intelligence
├─ AI Agent Manager → Agent configuration
├─ API Backend Agent → Chat endpoint
└─ Integration testing

Day 3: Interface
├─ Prepare UI mockup (optional)
├─ UI Agent → Frontend generation
└─ Frontend-backend integration

Day 4: Quality
├─ Testing Agent → Test suites
├─ Documentation Agent → Docs
└─ Fix issues

Day 5: Deployment
├─ Deployment Agent → Configs
├─ Deploy backend
├─ Deploy frontend
└─ Configure OpenAI allowlist
```

---

## Example Agent Interactions

### Database Schema Agent
```
Input: "Create SQLModel models for Task, Conversation, Message tables"

Process:
1. Parse specifications
2. Generate models.py with proper types
3. Add indexes for user_id
4. Create relationships
5. Generate migrations
6. Add query utilities

Output: Complete database layer ready for use
```

### UI Agent (with Image)
```
Input: [Image of modern chat interface with dark theme]

Process:
1. Analyze image with vision model
2. Extract color palette: Dark background (#1A1A1A), accent blue (#00D4FF)
3. Identify components: Rounded chat bubbles, gradient header
4. Generate ChatKit theme matching design
5. Create custom CSS for unique elements
6. Build responsive layout
7. Add smooth animations

Output: Pixel-perfect frontend matching mockup
```

### MCP Server Agent
```
Input: "Implement add_task tool"

Process:
1. Create Pydantic input/output models
2. Add input validation
3. Implement database operation
4. Add error handling
5. Register with MCP server
6. Generate tests

Output: Fully functional add_task tool
```

---

## Validation Checkpoints

After each phase, validate:

### Phase 1 Validation
```bash
# Test database
python -m pytest tests/test_database.py

# Test MCP server
python -m pytest tests/test_mcp_tools.py

# Run MCP server
cd mcp_server && uvicorn main:app --reload
# Visit http://localhost:8000/docs
```

### Phase 2 Validation
```bash
# Test agent
python -m pytest tests/test_agent.py

# Test API
python -m pytest tests/test_api.py

# Run full backend
python -m backend.main
# Test endpoint: POST http://localhost:8000/api/test_user/chat
```

### Phase 3 Validation
```bash
# Install frontend deps
cd frontend && npm install

# Run frontend
npm run dev

# Visit http://localhost:3000
# Test chat functionality
```

---

## Troubleshooting

### Database Issues
```
Problem: Migration fails
Solution: Check alembic.ini database URL, verify models import correctly

Problem: Connection errors
Solution: Ensure DATABASE_URL is set, check async engine configuration
```

### MCP Server Issues
```
Problem: Tools not found
Solution: Verify tool registration in server.py

Problem: Validation errors
Solution: Check Pydantic schemas match input data
```

### Agent Issues
```
Problem: Agent doesn't call tools
Solution: Verify tool schemas in OpenAI format, check system prompt

Problem: Tool execution fails
Solution: Check MCP server is running, verify user_id is passed
```

### Frontend Issues
```
Problem: ChatKit not loading
Solution: Check NEXT_PUBLIC_OPENAI_DOMAIN_KEY is set

Problem: API calls fail
Solution: Verify NEXT_PUBLIC_API_URL, check CORS configuration
```

---

## Success Metrics

- All agents complete their tasks autonomously
- No manual coding required
- Generated code passes all tests
- UI matches mockup (if provided)
- Application deploys successfully
- Documentation is comprehensive
- User can chat and manage tasks naturally

---

## Next Steps After Implementation

1. **User Testing**: Gather feedback on conversation flow
2. **Performance Optimization**: Profile and optimize slow queries
3. **Feature Additions**: Add due dates, priorities, tags
4. **Enhanced NLP**: Improve intent recognition
5. **Multi-modal**: Add voice input support
6. **Analytics**: Track usage metrics
7. **Scaling**: Set up load balancing and caching

---

## Resources

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [OpenAI ChatKit](https://github.com/openai/chatkit)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Vercel Deployment](https://vercel.com/docs)

---

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review agent specifications in agents/ directory
3. Consult individual component README files
4. Check generated test files for examples
