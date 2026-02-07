# Todo AI Chatbot - Quick Start Guide

Get your Todo AI Chatbot running in minutes using Claude Code and specialized agents.

---

## Prerequisites

```bash
# Required software
- Claude Code CLI (latest version)
- Python 3.10+
- Node.js 18+
- Git

# API Keys
- OpenAI API Key (for Agents SDK and ChatKit)
```

---

## 30-Minute Quick Start

### Step 1: Project Setup (2 minutes)

```bash
# Create and navigate to project directory
mkdir todo-ai-chatbot
cd todo-ai-chatbot

# Initialize git
git init

# Copy agent specifications
# Download AGENT_ARCHITECTURE.md and agent specs from this repository
```

### Step 2: Start Claude Code (1 minute)

```bash
# Start Claude Code session
claude-code

# Or if you prefer a specific model
claude-code --model sonnet
```

### Step 3: Run All Agents in Sequence (25 minutes)

Copy and paste these prompts to Claude Code one at a time:

#### Prompt 1: Database Setup (5 minutes)

```
I'm building a Todo AI Chatbot. Please act as the Database Schema Agent.

Create:
1. SQLModel models for Task, Conversation, and Message tables
2. Async database connection with SQLAlchemy
3. Alembic migrations
4. Query utilities

Use SQLite for development: sqlite+aiosqlite:///./todo.db

Reference the specifications in DATABASE_SCHEMA_AGENT_SPEC.md
```

#### Prompt 2: MCP Server (5 minutes)

```
Please act as the MCP Server Agent.

Create an MCP server with 5 tools:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task

Use FastAPI and the Official MCP SDK.
All tools should be stateless and use the database.

Reference: MCP_SERVER_AGENT_SPEC.md
```

#### Prompt 3: AI Agent (5 minutes)

```
Please act as the AI Agent Manager.

Create OpenAI Agents SDK integration:
1. Configure assistant with MCP tools
2. Conversation management
3. Tool execution via MCP server
4. Natural language understanding

Use environment variable: OPENAI_API_KEY

Reference: AI_AGENT_MANAGER_SPEC.md
```

#### Prompt 4: API Backend (3 minutes)

```
Create FastAPI chat endpoint:

POST /api/{user_id}/chat
- Request: conversation_id (optional), message (required)
- Response: conversation_id, response, tool_calls

Integrate with the AI agent and MCP server.
Use stateless design with database persistence.
```

#### Prompt 5: Frontend UI (5 minutes)

```
Please act as the UI Agent.

Create a ChatKit-based frontend with:
- Modern, clean design
- Blue theme (#3B82F6)
- Responsive layout
- API integration with backend

Backend API: http://localhost:8000

Reference: UI_AGENT_SPEC.md
```

#### Prompt 6: Testing (2 minutes)

```
Create pytest tests for:
- Database models
- MCP tools
- Agent conversation
- API endpoint

Run the tests and fix any issues.
```

### Step 4: Configuration (2 minutes)

Create `.env` file in project root:

```bash
# Backend .env
DATABASE_URL=sqlite+aiosqlite:///./todo.db
OPENAI_API_KEY=sk-your-key-here
MCP_SERVER_URL=http://localhost:8000
CORS_ORIGINS=["http://localhost:3000"]
```

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
```

---

## Running the Application

### Terminal 1: Backend + MCP Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start backend (includes MCP server)
uvicorn backend.main:app --reload --port 8000
```

### Terminal 2: Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Terminal 3: Test the Application

```bash
# Open browser
open http://localhost:3000

# Try these commands in the chat:
- "Add buy groceries to my list"
- "What tasks do I have?"
- "Mark task 1 as complete"
- "Delete the groceries task"
```

---

## Expected Project Structure

After running all agents, you should have:

```
todo-ai-chatbot/
├── backend/
│   ├── database/
│   │   ├── models.py
│   │   ├── connection.py
│   │   └── queries.py
│   ├── agent/
│   │   ├── config.py
│   │   ├── conversation.py
│   │   └── prompts.py
│   ├── api/
│   │   └── chat.py
│   └── main.py
├── mcp_server/
│   ├── main.py
│   ├── server.py
│   └── tools/
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── styles/
│   └── lib/
├── tests/
├── alembic/
├── .env
├── requirements.txt
└── README.md
```

---

## Troubleshooting Quick Fixes

### Backend won't start

```bash
# Check dependencies
pip install fastapi uvicorn sqlmodel openai mcp-sdk

# Check .env file exists
cat .env

# Check port is available
lsof -i :8000
```

### Frontend won't start

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check environment variables
cat frontend/.env.local
```

### Database errors

```bash
# Reset database
rm todo.db
alembic upgrade head

# Check migration files exist
ls alembic/versions/
```

### Agent not calling tools

```bash
# Verify OpenAI API key
echo $OPENAI_API_KEY

# Check MCP server is running
curl http://localhost:8000/tools

# Check tool schemas
curl http://localhost:8000/docs
```

---

## Verification Steps

### 1. Backend Health Check

```bash
curl http://localhost:8000/health

# Expected: {"status": "healthy", "version": "1.0.0"}
```

### 2. MCP Tools Available

```bash
curl http://localhost:8000/tools

# Expected: List of 5 tools
```

### 3. Chat Endpoint Works

```bash
curl -X POST http://localhost:8000/api/test_user/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy milk to my list"}'

# Expected: JSON with conversation_id, response, tool_calls
```

### 4. Frontend Loads

```
Open http://localhost:3000
- Should see chat interface
- Should be able to type messages
- Should receive responses
```

---

## Next Steps After Quick Start

1. **Customize UI**
   - Modify `frontend/styles/theme.css` for colors
   - Edit `frontend/components/` for custom components

2. **Enhance Agent Behavior**
   - Update `backend/agent/prompts.py` for different personality
   - Add more tools in `mcp_server/tools/`

3. **Add Features**
   - Task due dates
   - Task priorities
   - Task categories/tags
   - User authentication

4. **Deploy to Production**
   - Backend: Railway, Render, or AWS
   - Frontend: Vercel
   - Database: PostgreSQL on Supabase

---

## Common Use Cases

### Use Case 1: Add Task
```
User: "I need to call mom tomorrow"
Agent: [calls add_task]
Response: "I've added 'Call mom tomorrow' to your task list."
```

### Use Case 2: List Tasks
```
User: "What do I need to do?"
Agent: [calls list_tasks with status="pending"]
Response: "You have 3 pending tasks: 1) Call mom tomorrow, 2) Buy groceries, 3) Finish report"
```

### Use Case 3: Complete Task
```
User: "I called mom"
Agent: [calls complete_task]
Response: "Great! I've marked 'Call mom tomorrow' as complete."
```

### Use Case 4: Update Task
```
User: "Change the groceries task to buy milk and eggs"
Agent: [calls update_task]
Response: "I've updated the task to 'Buy milk and eggs'."
```

---

## Development Tips

### Hot Reload

Both backend and frontend have hot reload:
- Backend: Auto-reloads when Python files change
- Frontend: Auto-refreshes when React files change

### Testing Changes

```bash
# Test backend changes
pytest tests/

# Test frontend changes
cd frontend && npm test

# Test integration
# Use Postman or curl for API testing
```

### Debugging

```bash
# Backend logs
# Check terminal where uvicorn is running

# Frontend logs
# Check browser console (F12)

# Database inspection
sqlite3 todo.db
> SELECT * FROM tasks;
> SELECT * FROM conversations;
```

---

## Performance Tips

### Database Optimization

```python
# Add indexes for common queries
# Already included in migrations:
- user_id (all tables)
- conversation_id (messages)
- completed (tasks)
```

### Caching (Optional)

```python
# Add Redis caching for conversation history
# Reduces database queries
```

### Rate Limiting (Production)

```python
# Add to FastAPI
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/{user_id}/chat")
@limiter.limit("10/minute")
async def chat(...)
```

---

## Security Checklist

- [ ] Environment variables not committed to git
- [ ] CORS properly configured for production
- [ ] API rate limiting enabled
- [ ] User authentication implemented (if needed)
- [ ] SQL injection prevented (SQLModel handles this)
- [ ] XSS protection in frontend
- [ ] HTTPS enabled in production

---

## Resources

- **Documentation**: See README.md for detailed setup
- **Agent Specs**: See agents/ directory for detailed specifications
- **Examples**: See UI_AGENT_EXAMPLES.md for UI customization
- **Architecture**: See AGENT_ARCHITECTURE.md for system design

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the generated test files for examples
3. Consult the agent specification files
4. Check logs in both terminals

---

## Success Indicators

You'll know everything is working when:

- ✅ Backend starts without errors
- ✅ Frontend loads in browser
- ✅ You can send a message
- ✅ Agent responds appropriately
- ✅ Tasks are created/listed/updated/deleted
- ✅ Conversation history persists across messages
- ✅ All tests pass

Enjoy your AI-powered todo chatbot!
