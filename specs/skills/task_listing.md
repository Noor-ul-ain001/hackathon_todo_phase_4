# Skill Specification: Task Listing

**Skill Name**: task_listing
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The task_listing skill provides a reusable capability for querying and retrieving tasks from the system. It wraps the MCP list_tasks tool and handles filtering, sorting, and pagination parameters.

## Responsibilities

1. Accept task query parameters from agents
2. Validate parameter format
3. Invoke the list_tasks MCP tool
4. Handle MCP tool responses
5. Return formatted task list to calling agent

## Inputs

### Input Schema

```json
{
  "user_id": "string (required)",
  "filters": {
    "status": "string (optional, enum: pending|in_progress|completed|deleted)",
    "priority": "string (optional, enum: low|medium|high)",
    "due_before": "string (optional, ISO 8601 date)",
    "due_after": "string (optional, ISO 8601 date)",
    "search": "string (optional, search in title/description)"
  },
  "sort": "string (optional, default: created_at_desc)",
  "limit": "number (optional, default: 20, max: 100)",
  "offset": "number (optional, default: 0)"
}
```

### Input Examples

**All Tasks**:
```json
{
  "user_id": "user_123"
}
```

**Pending Tasks**:
```json
{
  "user_id": "user_456",
  "filters": {
    "status": "pending"
  }
}
```

**Urgent Tasks Due This Week**:
```json
{
  "user_id": "user_789",
  "filters": {
    "priority": "high",
    "due_before": "2026-01-03"
  },
  "sort": "due_date_asc",
  "limit": 10
}
```

## Outputs

### Output Schema

```json
{
  "success": "boolean",
  "tasks": [
    {
      "task_id": "number",
      "title": "string",
      "description": "string | null",
      "due_date": "string | null",
      "due_time": "string | null",
      "priority": "string",
      "status": "string",
      "created_at": "ISO 8601 timestamp",
      "updated_at": "ISO 8601 timestamp"
    }
  ],
  "count": "number (total matching tasks)",
  "has_more": "boolean (true if more results beyond limit)",
  "error": {
    "code": "string",
    "message": "string"
  } | null
}
```

### Output Examples

**Success with Results**:
```json
{
  "success": true,
  "tasks": [
    {
      "task_id": 42,
      "title": "Review architecture spec",
      "description": "Complete review by EOD",
      "due_date": "2025-12-28",
      "due_time": null,
      "priority": "high",
      "status": "pending",
      "created_at": "2025-12-27T10:30:00Z",
      "updated_at": "2025-12-27T10:30:00Z"
    },
    {
      "task_id": 43,
      "title": "Write tests",
      "description": null,
      "due_date": "2025-12-29",
      "due_time": "15:00",
      "priority": "medium",
      "status": "pending",
      "created_at": "2025-12-27T11:00:00Z",
      "updated_at": "2025-12-27T11:00:00Z"
    }
  ],
  "count": 2,
  "has_more": false,
  "error": null
}
```

**Success with No Results**:
```json
{
  "success": true,
  "tasks": [],
  "count": 0,
  "has_more": false,
  "error": null
}
```

## Triggers

### Text Modality
- CLI: `todo list --status pending`
- Natural language: "Show me my pending tasks"
- Chat: "What tasks do I have due this week?"

### Voice Modality
- "List my urgent tasks"
- "Show me tasks due tomorrow"

### Image Modality
- Not applicable for listing (output only)

## Execution Flow

```
1. Receive query parameters from calling agent
2. Validate input structure
3. Prepare MCP tool parameters (filters, sort, limit, offset)
4. Invoke list_tasks MCP tool
5. Receive MCP tool response
6. If success: Format task list and return
7. If failure: Format error and return
```

## MCP Tool Invocation

**Tool Called**: list_tasks

**Parameters**: All input parameters passed through

**Response Handling**:
- Success: Returns tasks array + metadata
- Failure: Returns error object

## Error Handling

- Missing user_id → INVALID_INPUT error
- MCP tool failure → MCP_TOOL_ERROR with details
- Empty results → Success with empty array (not an error)

## Failure Modes

| Scenario | Response | Agent Impact |
|----------|----------|--------------|
| No tasks found | Success with empty array | Agent formats "No tasks found" message |
| Invalid filter | MCP tool validates, returns error | Agent receives error, can correct filter |
| Database timeout | MCP_TOOL_ERROR | Agent can retry |

## Acceptance Criteria

1. ✅ Returns user's tasks with correct filtering
2. ✅ Never returns other users' tasks
3. ✅ Supports all filter options
4. ✅ Supports sorting
5. ✅ Supports pagination (limit, offset)
6. ✅ Handles empty results gracefully
7. ✅ Stateless operation
