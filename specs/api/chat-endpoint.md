# API Specification: Chat Endpoint

**Endpoint**: POST /api/{user_id}/chat
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The chat endpoint provides a single, stateless conversational interface for all task management operations across text, voice, and image modalities.

**Constitutional Requirement**: Per constitution.md section 3.2, "One conversational endpoint only: POST /api/{user_id}/chat"

## Endpoint Details

**Method**: POST
**Path**: `/api/{user_id}/chat`
**Authentication**: JWT Bearer token required
**Content-Type**: `application/json`

## Request Specification

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID making the request |

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer {JWT_TOKEN} |
| Content-Type | Yes | application/json |

### Request Body

```json
{
  "conversation_id": "number (optional, null for new conversation)",
  "message": "string (required, user's input)",
  "modality": "string (required, enum: text|voice|image)",
  "metadata": {
    "voice_confidence": "number (optional, for voice)",
    "image_data": "string (optional, base64 for image)",
    "client_type": "string (optional: web|cli|mobile)"
  }
}
```

### Request Examples

**New Text Conversation**:
```json
{
  "conversation_id": null,
  "message": "Add meeting with client tomorrow at 3pm",
  "modality": "text",
  "metadata": {
    "client_type": "web"
  }
}
```

**Continue Existing Conversation**:
```json
{
  "conversation_id": 123,
  "message": "Mark task 42 as complete",
  "modality": "text"
}
```

**Voice Input**:
```json
{
  "conversation_id": 123,
  "message": "Show me my tasks for this week",
  "modality": "voice",
  "metadata": {
    "voice_confidence": 0.92,
    "client_type": "mobile"
  }
}
```

**Image Input**:
```json
{
  "conversation_id": null,
  "message": "",
  "modality": "image",
  "metadata": {
    "image_data": "data:image/png;base64,iVBORw0KGgo...",
    "client_type": "mobile"
  }
}
```

## Response Specification

### Response Body

```json
{
  "conversation_id": "number",
  "response": "string (agent's response message)",
  "tool_calls": [
    {
      "tool": "string (MCP tool name)",
      "arguments": "object",
      "result": "object"
    }
  ],
  "tasks_affected": ["number (task IDs created/updated)"],
  "metadata": {
    "agents_invoked": ["string"],
    "execution_time_ms": "number"
  }
}
```

### Response Examples

**Task Created**:
```json
{
  "conversation_id": 124,
  "response": "I've added 'Meeting with client' to your task list for tomorrow at 3:00 PM.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "user_id": "user_123",
        "title": "Meeting with client",
        "due_date": "2025-12-28",
        "due_time": "15:00"
      },
      "result": {
        "task_id": 42,
        "status": "created"
      }
    }
  ],
  "tasks_affected": [42],
  "metadata": {
    "agents_invoked": ["InterfaceOrchestrator", "Orchestrator", "TaskReasoning", "Validation", "ResponseFormatter"],
    "execution_time_ms": 250
  }
}
```

**Task List Retrieved**:
```json
{
  "conversation_id": 124,
  "response": "You have 3 tasks due this week:\n1. Review architecture spec (Due: Dec 28)\n2. Write tests (Due: Dec 29)\n3. Deploy to staging (Due: Dec 30)",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "arguments": {
        "user_id": "user_123",
        "filters": {
          "due_after": "2025-12-27",
          "due_before": "2026-01-02"
        }
      },
      "result": {
        "tasks": [
          {"task_id": 42, "title": "Review architecture spec", "due_date": "2025-12-28"},
          {"task_id": 43, "title": "Write tests", "due_date": "2025-12-29"},
          {"task_id": 44, "title": "Deploy to staging", "due_date": "2025-12-30"}
        ],
        "count": 3
      }
    }
  ],
  "tasks_affected": [],
  "metadata": {
    "agents_invoked": ["InterfaceOrchestrator", "Orchestrator", "TaskReasoning", "ResponseFormatter"],
    "execution_time_ms": 180
  }
}
```

## Stateless Request Cycle

### Flow

```
1. Request arrives at endpoint
   ↓
2. Validate JWT token
   - Extract user_id from token
   - Verify user_id matches path parameter
   - Reject if invalid/expired
   ↓
3. Load conversation context (if conversation_id provided)
   - Query messages table for last N messages
   - Reconstruct conversation history
   - If conversation_id not provided: create new conversation
   ↓
4. Invoke agent chain
   - Pass request to Interface Orchestrator Agent
   - Interface Orchestrator → Orchestrator → Specialized Agents
   - Agents invoke skills → MCP tools → Database
   ↓
5. Store conversation messages
   - Save user message (role="user")
   - Save agent response (role="assistant")
   - Update conversation timestamp
   ↓
6. Format and return response
   - Include conversation_id
   - Include agent's message
   - Include tool_calls metadata
   ↓
7. No session state retained in memory
```

### Stateless Guarantees

1. **No server-side session**: All context loaded from database
2. **Conversation resumable**: After server restart, conversation continues seamlessly
3. **Request independence**: Each request is self-contained
4. **Database as truth**: All state persisted in database (conversations, messages, tasks)

## JWT Enforcement

### Token Validation

```
1. Extract Bearer token from Authorization header
2. Verify JWT signature with secret key
3. Check token expiration (exp claim)
4. Extract user_id from token claims
5. Verify user_id matches path parameter
6. If any check fails: Return 401 Unauthorized
```

### JWT Claims Required

```json
{
  "user_id": "string (must match path parameter)",
  "email": "string",
  "iat": "number (issued at)",
  "exp": "number (expiration)"
}
```

### Token Errors

| Error | Status | Message |
|-------|--------|---------|
| Missing token | 401 | "Authorization header required" |
| Invalid signature | 401 | "Invalid token" |
| Expired token | 401 | "Token expired" |
| user_id mismatch | 403 | "Forbidden: user_id mismatch" |

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "string",
    "message": "string (user-friendly)",
    "details": "object (optional, for debugging)",
    "timestamp": "ISO 8601"
  }
}
```

### Error Codes

| Code | Status | Description | Example |
|------|--------|-------------|---------|
| UNAUTHORIZED | 401 | Invalid/missing JWT | Missing Authorization header |
| FORBIDDEN | 403 | user_id mismatch | Token user_id ≠ path user_id |
| VALIDATION_ERROR | 400 | Invalid request body | Missing required field |
| AGENT_ERROR | 500 | Agent processing failed | Agent crashed |
| DATABASE_ERROR | 500 | Database unavailable | Connection timeout |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | >60 requests/minute |

### Error Examples

**Validation Error**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Message is required",
    "details": {
      "field": "message",
      "received": null
    },
    "timestamp": "2025-12-27T10:30:00Z"
  }
}
```

**Agent Error**:
```json
{
  "error": {
    "code": "AGENT_ERROR",
    "message": "Unable to process request at this time. Please try again.",
    "timestamp": "2025-12-27T10:31:00Z"
  }
}
```

## Rate Limiting

**Limit**: 60 requests per minute per user
**Response**: 429 Too Many Requests
**Headers**:
- `X-RateLimit-Limit: 60`
- `X-RateLimit-Remaining: 0`
- `X-RateLimit-Reset: <unix_timestamp>`

## Performance Targets

- **Response Time**: <2 seconds for text/voice (p95)
- **Response Time**: <5 seconds for image (p95)
- **Throughput**: 1000 concurrent users
- **Database Queries**: <3 queries per request average

## Security Measures

1. **JWT Validation**: All requests
2. **User Isolation**: Enforced at API, agent, and MCP layers
3. **Input Sanitization**: Via Validation Agent
4. **Rate Limiting**: Prevent abuse
5. **HTTPS Only**: No plain HTTP
6. **CORS Configuration**: Allowed domains only

## Testing Requirements

### Unit Tests

1. JWT validation accepts valid tokens
2. JWT validation rejects invalid tokens
3. user_id mismatch rejected
4. Request validation (required fields)

### Integration Tests

1. End-to-end: Request → Agents → MCP → Response
2. Conversation persistence across requests
3. Stateless recovery after server restart
4. Multi-modality handling

### Load Tests

1. 1000 concurrent users
2. Response times within targets
3. No memory leaks over time
4. Database connection pool stable

## Acceptance Criteria

1. ✅ Single endpoint handles all modalities
2. ✅ JWT authentication enforced
3. ✅ Stateless request cycle verified
4. ✅ Conversation persists in database
5. ✅ Error responses standardized
6. ✅ Rate limiting functional
7. ✅ Performance targets met
8. ✅ Security tests pass
