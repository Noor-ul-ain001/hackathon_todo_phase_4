# Skill Specification: Task Update

**Skill Name**: task_update
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The task_update skill provides a reusable capability for updating existing tasks. It wraps the MCP update_task tool and handles partial updates to task fields.

## Responsibilities

1. Accept task update parameters from agents
2. Validate input structure
3. Invoke the update_task MCP tool
4. Handle ownership verification (task belongs to user)
5. Return updated task to calling agent

## Inputs

### Input Schema

```json
{
  "user_id": "string (required)",
  "task_id": "number (required)",
  "updates": {
    "title": "string (optional, 1-200 characters)",
    "description": "string (optional, max 2000 characters)",
    "due_date": "string (optional, ISO 8601 format)",
    "due_time": "string (optional, HH:MM format)",
    "priority": "string (optional, enum: low|medium|high)",
    "status": "string (optional, enum: pending|in_progress|completed)"
  }
}
```

### Input Examples

**Update Title Only**:
```json
{
  "user_id": "user_123",
  "task_id": 42,
  "updates": {
    "title": "Review updated architecture spec"
  }
}
```

**Update Multiple Fields**:
```json
{
  "user_id": "user_456",
  "task_id": 43,
  "updates": {
    "due_date": "2025-12-30",
    "priority": "high",
    "status": "in_progress"
  }
}
```

## Outputs

### Output Schema

```json
{
  "success": "boolean",
  "task": {
    "task_id": "number",
    "title": "string",
    "description": "string | null",
    "due_date": "string | null",
    "due_time": "string | null",
    "priority": "string",
    "status": "string",
    "created_at": "ISO 8601 timestamp",
    "updated_at": "ISO 8601 timestamp"
  },
  "updated_fields": ["string"],
  "error": null | object
}
```

## Triggers

### Text Modality
- CLI: `todo update 42 --title "New title" --priority high`
- Natural language: "Change task 42 to high priority"
- Chat: "Update the meeting task to tomorrow"

### Voice Modality
- "Set task 42 to high priority"
- "Move the meeting to tomorrow"

### Image Modality
- Image with updated task info (rare use case)

## Execution Flow

```
1. Receive update parameters (user_id, task_id, updates object)
2. Validate required fields present
3. Invoke update_task MCP tool
4. MCP tool verifies ownership
5. If success: Return updated task
6. If failure: Return error (not found, unauthorized, etc.)
```

## MCP Tool Invocation

**Tool Called**: update_task

**Parameters**: user_id, task_id, updates

**Response**: Updated task object or error

## Error Handling

- Missing task_id → INVALID_INPUT
- Task not found → TASK_NOT_FOUND (from MCP)
- Unauthorized (wrong user) → UNAUTHORIZED (from MCP)
- Empty updates object → INVALID_INPUT

## Failure Modes

| Scenario | Response | Impact |
|----------|----------|--------|
| Task doesn't exist | TASK_NOT_FOUND error | Agent informs user task not found |
| User doesn't own task | UNAUTHORIZED error | Agent informs user can't update others' tasks |
| No updates provided | INVALID_INPUT error | Agent requests at least one field to update |

## Acceptance Criteria

1. ✅ Updates specified fields only
2. ✅ Verifies task ownership
3. ✅ Returns updated task with new values
4. ✅ Preserves unmodified fields
5. ✅ Handles partial updates correctly
6. ✅ Rejects updates to non-existent tasks
7. ✅ Rejects cross-user updates
