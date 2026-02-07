# Frontend Setup Guide

## Overview

Next.js frontend for the Todo Intelligence Platform with real backend API integration.

## Configuration Files

✅ **Created/Configured:**
- `pages/_app.js` - Global app wrapper with CSS imports
- `pages/index.js` - Main chat interface (connected to real API)
- `styles/globals.css` - Tailwind CSS directives and global styles
- `tailwind.config.js` - Tailwind configuration
- `postcss.config.js` - PostCSS configuration
- `next.config.js` - Next.js configuration
- `.env.local` - Environment variables (API URL)
- `package.json` - Dependencies and scripts

## Prerequisites

1. **Backend Running**: The backend API must be running on `http://localhost:8000`
2. **MCP Server Running**: The MCP server must be running on `http://localhost:8001`
3. **Neon PostgreSQL**: Database must be configured and accessible

## Installation

```bash
cd C:\Users\user\Desktop\todo\phase3\frontend
npm install
```

## Running the Frontend

### Development Mode
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

### Production Build
```bash
npm run build
npm start
```

## Environment Variables

File: `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Integration

The frontend connects to the backend via:
- **Endpoint**: `POST http://localhost:8000/api/{user_id}/chat`
- **Request**:
  ```json
  {
    "message": "Add task: Review architecture",
    "modality": "text",
    "conversation_id": null,
    "metadata": {}
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": 1,
    "response": "✓ Task created: Review architecture",
    "tool_calls": [...],
    "tasks_affected": [42],
    "metadata": {...}
  }
  ```

## Features

- ✅ Real-time chat interface
- ✅ Conversational task management
- ✅ Natural language processing
- ✅ CLI command support
- ✅ Error handling
- ✅ Loading states
- ✅ Conversation persistence
- ✅ Responsive design (Tailwind CSS)

## Testing the Flow

### 1. Start Backend Services

Terminal 1 - Backend API:
```bash
cd C:\Users\user\Desktop\todo\phase3\backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload --port 8000
```

Terminal 2 - MCP Server:
```bash
cd C:\Users\user\Desktop\todo\phase3\mcp-server
source venv/bin/activate
python -m src.server
```

### 2. Start Frontend

Terminal 3 - Frontend:
```bash
cd C:\Users\user\Desktop\todo\phase3\frontend
npm run dev
```

### 3. Test Commands

Open `http://localhost:3000` in your browser and try:

**CLI Commands:**
- `todo add 'Review architecture spec' --due tomorrow --priority high`
- `todo list --status pending`
- `todo complete 1`
- `todo update 1 --priority low`
- `todo delete 1`

**Natural Language:**
- "Add a task to buy groceries tomorrow"
- "Show me my pending tasks"
- "Mark task 1 as complete"
- "Change task 2 to high priority"

### 4. Expected Behavior

- User message appears immediately
- Loading indicator shows while processing
- Agent response appears with formatted message
- Errors are displayed in red with helpful messages
- Conversation persists across page refreshes (stored in Neon DB)

## Architecture

```
User Input (Browser)
    ↓
Next.js Frontend (localhost:3000)
    ↓
POST /api/{user_id}/chat
    ↓
FastAPI Backend (localhost:8000)
    ↓
Agent System (6 Agents)
    ↓
Skills Layer (7 Skills)
    ↓
MCP Tools (5 Tools via localhost:8001)
    ↓
Neon PostgreSQL Database
```

## Troubleshooting

### Frontend won't start
- Run `npm install` to ensure all dependencies are installed
- Check for port conflicts on 3000

### API connection errors
- Verify backend is running on port 8000
- Check `.env.local` has correct API URL
- Look for CORS errors in browser console

### No response from backend
- Verify MCP server is running on port 8001
- Check backend logs for errors
- Verify Neon PostgreSQL connection in backend `.env`

### Styling issues
- Run `npm install` to ensure Tailwind CSS is installed
- Verify `tailwind.config.js` exists
- Check browser console for CSS errors

## Next Steps (Optional Enhancements)

- Add voice input support (Whisper STT)
- Add image upload support (OCR)
- Add authentication (Better Auth + JWT)
- Add task list sidebar
- Add conversation history panel
- Add markdown rendering for responses
- Add copy-to-clipboard for code blocks
- Add dark mode toggle
