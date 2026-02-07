# Todo Intelligence Platform - Quick Start Guide

## Overview

Complete guide to running the full Todo Intelligence Platform stack with all components.

## Architecture Stack

```
┌─────────────────────────────────────────────────────┐
│  Frontend (Next.js)                                 │
│  http://localhost:3000                              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Backend API (FastAPI)                              │
│  http://localhost:8000                              │
│  • Chat endpoint                                    │
│  • Conversation service                             │
│  • Agent client                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Agent System (6 Agents)                            │
│  • Interface Orchestrator                           │
│  • Main Orchestrator                                │
│  • Task Reasoning                                   │
│  • Validation & Safety                              │
│  • Response Formatter                               │
│  • Visual Context                                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Skills Layer (7 Skills)                            │
│  • Task Creation                                    │
│  • Task Listing                                     │
│  • Task Update                                      │
│  • Task Completion                                  │
│  • Task Deletion                                    │
│  • Intent Disambiguation                            │
│  • UI Intent Normalization                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  MCP Server (5 Tools)                               │
│  http://localhost:8001                              │
│  • add_task                                         │
│  • list_tasks                                       │
│  • update_task                                      │
│  • complete_task                                    │
│  • delete_task                                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Neon PostgreSQL Database                           │
│  • Tasks                                            │
│  • Conversations                                    │
│  • Messages                                         │
│  • Users                                            │
└─────────────────────────────────────────────────────┘
```

---

## Prerequisites

### 1. Python Environment
```bash
python --version  # Should be 3.11+
```

### 2. Node.js Environment
```bash
node --version    # Should be 18+
npm --version     # Should be 8+
```

### 3. Neon PostgreSQL Database

Create a `.env` file in `backend/` with:
```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

---

## Installation

### 1. Backend Setup
```bash
cd C:\Users\user\Desktop\todo\phase3\backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. MCP Server Setup
```bash
cd C:\Users\user\Desktop\todo\phase3\mcp-server
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Agents Setup
```bash
cd C:\Users\user\Desktop\todo\phase3\agents
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 4. Skills Setup
```bash
cd C:\Users\user\Desktop\todo\phase3\skills
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 5. Frontend Setup
```bash
cd C:\Users\user\Desktop\todo\phase3\frontend
npm install
```

---

## Running the System

**IMPORTANT**: Start services in this order!

### Terminal 1: MCP Server (Start FIRST)
```bash
cd C:\Users\user\Desktop\todo\phase3\mcp-server
.\venv\Scripts\activate
python -m src.server
```

**Wait for**: "MCP Server running on http://localhost:8001"

### Terminal 2: Backend API (Start SECOND)
```bash
cd C:\Users\user\Desktop\todo\phase3\backend
.\venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

**Wait for**: "Uvicorn running on http://127.0.0.1:8000"

### Terminal 3: Frontend (Start LAST)
```bash
cd C:\Users\user\Desktop\todo\phase3\frontend
npm run dev
```

**Wait for**: "ready - started server on 0.0.0.0:3000"

---

## Testing

### 1. Open Browser
Navigate to: `http://localhost:3000`

### 2. Try CLI Commands
```
todo add 'Review architecture spec' --due tomorrow --priority high
todo add 'Buy groceries' --priority medium
todo list --status pending
todo complete 1
todo update 2 --priority high
todo delete 1
```

### 3. Try Natural Language
```
Add a task to call mom tomorrow
Show me my pending tasks
Mark task 1 as complete
Change task 2 to high priority
What tasks do I have?
```

### 4. Expected Flow

**User Input**: "todo add 'Test task' --due tomorrow"

1. **Frontend** sends POST to backend
2. **Backend** calls Interface Orchestrator agent
3. **Interface Orchestrator** normalizes CLI command
4. **Main Orchestrator** routes to Task Reasoning
5. **Validation Agent** validates inputs
6. **Task Reasoning** invokes Task Creation skill
7. **Task Creation skill** calls add_task MCP tool
8. **MCP tool** saves to Neon PostgreSQL
9. **Response Formatter** generates user-friendly message
10. **Backend** saves conversation to database
11. **Frontend** displays response

**Response**: "✓ Task created: Test task (Due: Dec 28)"

---

## Verification Checklist

### MCP Server
- [ ] Running on port 8001
- [ ] No connection errors in logs
- [ ] Database connection successful

### Backend API
- [ ] Running on port 8000
- [ ] No import errors
- [ ] Can access http://localhost:8000/docs (FastAPI docs)

### Frontend
- [ ] Running on port 3000
- [ ] No compilation errors
- [ ] UI loads correctly in browser

### End-to-End
- [ ] Can send message from UI
- [ ] Loading indicator appears
- [ ] Response appears in chat
- [ ] No console errors in browser
- [ ] Backend logs show agent invocations
- [ ] MCP server logs show tool calls
- [ ] Messages persist in database

---

## Common Issues

### Issue: "Connection refused to localhost:8000"
**Solution**: Ensure backend is running before starting frontend

### Issue: "MCP server not responding"
**Solution**:
1. Check MCP server is running on port 8001
2. Check no firewall blocking port
3. Restart MCP server

### Issue: "Database connection error"
**Solution**:
1. Verify `.env` file in backend/ has correct DATABASE_URL
2. Test Neon database is accessible
3. Run migrations: `alembic upgrade head`

### Issue: "Frontend shows error 500"
**Solution**:
1. Check backend logs for Python errors
2. Verify all Python dependencies installed
3. Check agent system can import all modules

### Issue: "Tasks not persisting"
**Solution**:
1. Verify MCP server is connected to database
2. Check MCP server logs for SQL errors
3. Verify user_id is being passed correctly

---

## Stopping the System

1. **Frontend**: Press `Ctrl+C` in Terminal 3
2. **Backend**: Press `Ctrl+C` in Terminal 2
3. **MCP Server**: Press `Ctrl+C` in Terminal 1

---

## Production Deployment

See individual deployment guides:
- Backend: `backend/README.md`
- MCP Server: `mcp-server/README.md`
- Frontend: `frontend/README.md`

**Recommended Stack**:
- Frontend: Vercel or Netlify
- Backend: Railway, Render, or AWS ECS
- MCP Server: Railway or Render
- Database: Neon (already using)

---

## Monitoring

### Backend Logs
```bash
# In backend terminal
tail -f logs/backend.log
```

### MCP Server Logs
```bash
# In MCP server terminal
tail -f logs/mcp.log
```

### Frontend Console
Open browser DevTools → Console tab

---

## Next Steps

- [ ] Add authentication (Better Auth + JWT)
- [ ] Add rate limiting
- [ ] Set up monitoring (Sentry)
- [ ] Configure CI/CD (GitHub Actions)
- [ ] Add Docker containers
- [ ] Deploy to production

---

## Support

For issues:
1. Check logs in each terminal
2. Verify all services running
3. Check database connectivity
4. Review error messages in browser console

Documentation:
- `IMPLEMENTATION_SUMMARY.md` - Complete architecture
- `frontend/FRONTEND_SETUP.md` - Frontend details
- `backend/README.md` - Backend details
- `mcp-server/README.md` - MCP server details

---

## Success Indicators

You'll know the system is working when:
- ✅ All 3 terminals show "running" messages
- ✅ Browser loads chat interface
- ✅ You can send a message and get a response
- ✅ Response includes task ID
- ✅ Subsequent messages remember conversation context
- ✅ Tasks appear in database

**Congratulations!** You now have a fully functional AI-powered task management system with:
- 6 coordinated agents
- 7 specialized skills
- 5 MCP tools
- Stateless architecture
- Multi-user isolation
- Conversational interface
- Real-time web UI
