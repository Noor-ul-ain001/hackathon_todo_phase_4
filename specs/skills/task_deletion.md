# Skill Specification: Task Deletion

**Skill Name**: task_deletion
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The task_deletion skill provides a reusable capability for deleting tasks from the system. It wraps the MCP delete_task tool and handles the deletion workflow.

## Responsibilities

1. Accept task deletion request from agents
2. Invoke the delete_task MCP tool
3. Handle ownership verification
4. Return deletion confirmation

## Inputs

### Input Schema

```json
{
  "user_id": "string (required)",
  "task_id": "number (required)",
  "confirmation": "boolean (optional, default: true)"
}
```

### Input Examples

```json
{
  "user_id": "user_123",
  "task_id": 42
}
```

**With Explicit Confirmation**:
```json
{
  "user_id": "user_456",
  "task_id": 43,
  "confirmation": true
}
```

## Outputs

### Output Schema

```json
{
  "success": "boolean",
  "task_id": "number",
  "message": "string",
  "error": null | object
}
```

### Output Example

```json
{
  "success": true,
  "task_id": 42,
  "message": "Task deleted successfully",
  "error": null
}
```

## Triggers

### Text Modality
- CLI: `todo delete 42`
- Natural language: "Delete task 42"
- Chat: "Remove the architecture review task"

### Voice Modality
- "Delete task forty-two"
- "Remove the meeting task"

### Image Modality
- Image with delete button clicked (UI affordance)

## Execution Flow

```
1. Receive user_id and task_id
2. Validate inputs
3. Invoke delete_task MCP tool
4. MCP tool:
   - Verifies ownership
   - Deletes task from database
5. Return success confirmation
```

## MCP Tool Invocation

**Tool Called**: delete_task

**Parameters**: user_id, task_id

**Response**: Success confirmation or error

## Error Handling

- Task not found → TASK_NOT_FOUND (or success if idempotent)
- Unauthorized → UNAUTHORIZED
- Already deleted → Success (idempotent)

## Failure Modes

| Scenario | Response | Impact |
|----------|----------|--------|
| Task doesn't exist | TASK_NOT_FOUND or success | Agent informs task already deleted |
| Wrong user | UNAUTHORIZED | Agent informs can't delete others' tasks |
| Database error | MCP_TOOL_ERROR | Agent can retry |

## Acceptance Criteria

1. ✅ Deletes task from database
2. ✅ Verifies ownership before deletion
3. ✅ Returns confirmation message
4. ✅ Idempotent (deleting twice is safe)
5. ✅ Rejects unauthorized deletion attempts
