# Todo Intelligence Platform - System Architecture

**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## High-Level Architecture

The Todo Intelligence Platform follows a strict layered architecture where intelligence resides in agents, data access flows through MCP tools, and application code serves only as infrastructure orchestration.

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   CLI    │  │ Web Chat │  │  Voice   │  │  Image   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Intent Normalization Layer                      │
│         (Convert UI-specific input → Structured Intent)     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Agent Orchestration Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Orchestrator │──│Task Reasoning│──│  Validation  │     │
│  │    Agent     │  │    Agent     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │   Response   │  │    Visual    │                        │
│  │   Formatter  │  │   Context    │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Skills Layer                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  Task   │  │  Task   │  │  Task   │  │  Task   │       │
│  │Creation │  │ Listing │  │ Update  │  │Complete │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │  Task   │  │  Intent │  │   UI    │                    │
│  │Deletion │  │Disambig │  │  Norm   │                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              MCP (Model Context Protocol) Layer              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │add_task │  │list_    │  │update_  │  │complete_│       │
│  │         │  │tasks    │  │task     │  │task     │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                              │
│  ┌─────────┐                                                │
│  │delete_  │                                                │
│  │task     │                                                │
│  └─────────┘                                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Database Layer                          │
│  ┌──────┐  ┌──────┐  ┌──────────────┐  ┌──────────┐       │
│  │users │  │tasks │  │conversations │  │ messages │       │
│  └──────┘  └──────┘  └──────────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## Stateless Request Flow

Every user interaction follows this invariant pattern:

```
1. User Input (any modality: text/voice/image)
        ↓
2. Intent Normalization
   → Extract: user_id, action, parameters, context
   → Output: Structured intent object
        ↓
3. JWT Validation (Phases 2+)
   → Verify token
   → Extract user_id claim
   → Reject if invalid
        ↓
4. Agent Orchestration
   → Orchestrator receives intent
   → Selects appropriate agents
   → Agents invoke skills
   → Skills call MCP tools
        ↓
5. MCP Tool Execution
   → Validate parameters
   → Execute database operation
   → Return results
        ↓
6. Response Formation
   → Response Formatter agent structures output
   → Format adapted to user's modality
        ↓
7. Return to User
   → Conversation stored (if chat mode)
   → No session state retained in memory
```

### Critical Invariants

1. **No Session State**: Each request is completely independent
2. **Context Derivation**: All context rebuilt from:
   - JWT claims (user_id, permissions)
   - Database state (tasks, conversations, messages)
   - Request parameters (intent, filters, search)
3. **Agent Statelessness**: Agents execute and terminate; no persistent memory
4. **Database as Truth**: Single source of truth for all persistent state

## MCP Integration

### MCP Server Architecture

The MCP server provides the exclusive interface for data operations:

```
┌─────────────────────────────────────────────────────────────┐
│                        MCP Server                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Tool Registry                          │    │
│  │  - add_task                                         │    │
│  │  - list_tasks                                       │    │
│  │  - update_task                                      │    │
│  │  - complete_task                                    │    │
│  │  - delete_task                                      │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Parameter Validation                       │    │
│  │  - Type checking                                    │    │
│  │  - Required field validation                        │    │
│  │  - User ID verification                             │    │
│  │  - Input sanitization                               │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Database Connector                         │    │
│  │  - Parameterized queries                            │    │
│  │  - Transaction management                           │    │
│  │  - Connection pooling                               │    │
│  │  - User isolation enforcement                       │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Tool Interaction Pattern

Skills invoke MCP tools using this pattern:

```python
# Conceptual example (implementation-agnostic)
intent = {
    "user_id": "user_123",
    "action": "create_task",
    "parameters": {
        "title": "Review architecture spec",
        "description": "Complete review by EOD"
    }
}

# Skill invokes MCP tool
result = mcp.call_tool(
    tool="add_task",
    arguments={
        "user_id": intent["user_id"],
        "title": intent["parameters"]["title"],
        "description": intent["parameters"]["description"]
    }
)

# MCP tool executes database operation
# Returns: { "task_id": 42, "status": "created" }
```

### MCP Security Model

1. **User Isolation**: Every tool requires `user_id` parameter
2. **Query Parameterization**: No string concatenation in SQL
3. **Input Validation**: Type and format checks before database access
4. **Error Sanitization**: Database errors never leak to user responses

## Agent Orchestration Flow

### Request Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                   Request Arrives                            │
│              (text/voice/image input)                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│          Interface Orchestrator Agent                        │
│  - Determines modality (text/voice/image)                   │
│  - Invokes ui_intent_normalization skill                    │
│  - Produces structured intent                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               Orchestrator Agent                             │
│  - Receives normalized intent                               │
│  - Routes to appropriate specialized agent                  │
│  - Coordinates multi-agent workflows if needed              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Task      │    │ Validation  │    │   Visual    │
│  Reasoning  │    │   Safety    │    │  Context    │
│   Agent     │    │   Agent     │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│          Skills Invoked with Intent Parameters              │
│  - task_creation, task_update, task_listing, etc.          │
│  - Skills call MCP tools with validated parameters          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                MCP Tools Execute                             │
│  - Database operations performed                            │
│  - Results returned to skills                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│            Response Formatter Agent                          │
│  - Receives operation results                               │
│  - Formats for user's modality                              │
│  - Adds context-appropriate details                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Response Returned to User                       │
│  - Text response (CLI/chat)                                 │
│  - Voice output (TTS)                                       │
│  - Visual confirmation (UI update)                          │
└─────────────────────────────────────────────────────────────┘
```

### Agent Collaboration Example

Example: User says "Add meeting tomorrow at 3pm"

```
1. Interface Orchestrator Agent
   Input: "Add meeting tomorrow at 3pm"
   Output: {
     "intent": "create_task",
     "parameters": {
       "title": "meeting",
       "due_date": "2025-12-28",
       "due_time": "15:00"
     }
   }

2. Orchestrator Agent
   Routes to: Task Reasoning Agent + Validation Agent

3. Task Reasoning Agent
   - Interprets "tomorrow" → calculates date
   - Interprets "3pm" → converts to 24hr time
   - Enriches task with defaults (priority, status)

4. Validation Agent
   - Checks date is valid (not in past)
   - Validates time format
   - Ensures title is non-empty
   - Approves or rejects

5. If approved, invokes task_creation skill
   Skill calls: mcp.add_task(user_id, title, due_date, due_time)

6. Response Formatter Agent
   MCP result: { "task_id": 42, "status": "created" }
   Formatted: "Created task 'meeting' for tomorrow at 3:00 PM (Task #42)"

7. Return to user
```

## Data Flow Architecture

### Phase 1: CLI (Single User)

```
CLI Command → MCP Tool → SQLite Database
```

No authentication required; single hardcoded user_id.

### Phase 2-5: Multi-User Web/Multimodal

```
User Request
    ↓
[JWT Validation]
    ↓
Extract user_id from token
    ↓
Intent Normalization
    ↓
Agent Orchestration
    ↓
Skill Invocation (with user_id)
    ↓
MCP Tool (enforces user_id isolation)
    ↓
Database (user_id in WHERE clauses)
    ↓
Results filtered by user_id
    ↓
Response to user
```

### Conversation Storage (Phases 4-5)

For chat-based interactions:

```
User message → stored in messages table (user_id, conversation_id, role="user")
Agent response → stored in messages table (user_id, conversation_id, role="assistant")

Next request includes conversation_id → Agent loads recent messages for context
```

**Stateless Context Reconstruction**:
- Agent receives conversation_id in request
- Queries messages table for last N messages
- Reconstructs context from database (not from memory)
- Processes new message with this context
- Stores new exchange in database
- Terminates (no state persisted)

## Security Architecture

### Authentication Flow (Phase 2+)

```
1. User logs in → Auth provider issues JWT
2. JWT contains: { "user_id": "...", "email": "...", "exp": ... }
3. Every API request includes: Authorization: Bearer <JWT>
4. API validates JWT signature and expiration
5. Extracts user_id claim
6. Passes user_id to agents and MCP tools
7. All database operations filtered by user_id
```

### Multi-User Isolation

**Database Level**:
```sql
-- Every query includes user_id in WHERE clause
SELECT * FROM tasks WHERE user_id = ? AND task_id = ?
UPDATE tasks SET status = ? WHERE user_id = ? AND task_id = ?
DELETE FROM tasks WHERE user_id = ? AND task_id = ?
```

**MCP Tool Level**:
```
Every MCP tool:
1. Requires user_id parameter
2. Validates user_id matches JWT claim
3. Includes user_id in all database queries
4. Returns only user's own data
```

**Agent Level**:
```
Agents receive user_id in intent:
- Never process requests without user_id
- Never access data without user context
- Never return data for wrong user
```

### Input Validation Layers

1. **UI Layer**: Basic format validation (length, characters)
2. **Intent Normalization**: Type validation (string, number, date)
3. **Validation Agent**: Semantic validation (logic, constraints)
4. **MCP Tools**: Final validation before database (SQL injection prevention)

## Scalability Considerations

### Stateless Benefits

- **Horizontal Scaling**: Any server can handle any request
- **No Session Affinity**: Load balancer free to route anywhere
- **Crash Recovery**: Failed requests simply retried; no state loss
- **Database as Bottleneck**: Scale database (read replicas, sharding) not app servers

### Performance Optimization Points

1. **Database Indexing**: user_id, task_id, conversation_id, created_at
2. **Connection Pooling**: Reuse database connections
3. **Query Optimization**: Limit result sets, use pagination
4. **Agent Caching**: None (agents are stateless and terminate)
5. **MCP Tool Efficiency**: Batch operations where possible

## Failure Modes and Recovery

### Request Failure

```
1. User request arrives
2. Error occurs at any layer
3. Transaction rolled back (if in progress)
4. Error captured and sanitized
5. User-friendly error returned
6. No state corrupted (stateless architecture)
7. User retries → fresh request processed
```

### Database Failures

- **Connection Lost**: MCP tool returns error, user notified to retry
- **Transaction Failure**: Rollback automatic, no partial state
- **Data Corruption**: Database backups, point-in-time recovery

### Agent Failures

- **Agent Error**: Caught by orchestrator, error response formatted
- **Skill Error**: Returned to agent, agent handles gracefully
- **MCP Tool Error**: Returned to skill, skill returns error to agent

**No cascading failures**: Each layer isolates errors and returns structured responses.

## Technology-Agnostic Principles

This architecture can be implemented with:
- **Any web framework** (Next.js, Django, Rails, etc.)
- **Any database** (PostgreSQL, MySQL, SQLite, MongoDB)
- **Any auth provider** (Auth0, Clerk, Firebase, custom JWT)
- **Any MCP implementation** (TypeScript, Python, Go)
- **Any agent runtime** (Claude API, local LLM, agent framework)

**Critical invariants** (must be preserved regardless of technology):
1. Agents contain business logic, not application code
2. All data operations via MCP tools
3. Stateless request processing
4. User isolation enforced at every layer
5. Intent normalization for multimodal consistency

## Next Steps

1. Review and approve this architecture
2. Review agent specifications (agents/*.md)
3. Review skill specifications (skills/*.md)
4. Review MCP tool specifications (mcp/tools.md)
5. Review database schema (database/schema.md)
6. Begin implementation with Phase 1 (CLI)
