# Skill Specification: Task Completion

**Skill Name**: task_completion
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The task_completion skill provides a reusable capability for marking tasks as completed. It wraps the MCP complete_task tool and handles the completion workflow.

## Responsibilities

1. Accept task completion request from agents
2. Invoke the complete_task MCP tool
3. Handle ownership verification
4. Return completed task with timestamp

## Inputs

### Input Schema

```json
{
  "user_id": "string (required)",
  "task_id": "number (required)"
}
```

### Input Examples

```json
{
  "user_id": "user_123",
  "task_id": 42
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
    "status": "completed",
    "completed_at": "ISO 8601 timestamp",
    "updated_at": "ISO 8601 timestamp"
  },
  "error": null | object
}
```

## Triggers

### Text Modality
- CLI: `todo complete 42`
- Natural language: "Mark task 42 as done"
- Chat: "Complete the architecture review task"

### Voice Modality
- "Mark task forty-two as complete"
- "I finished the review task"

### Image Modality
- Image with checkbox marked (UI affordance)

## Execution Flow

```
1. Receive user_id and task_id
2. Validate inputs present
3. Invoke complete_task MCP tool
4. MCP tool:
   - Verifies ownership
   - Sets status = "completed"
   - Sets completed_at = current timestamp
5. Return updated task
```

## MCP Tool Invocation

**Tool Called**: complete_task

**Parameters**: user_id, task_id

**Response**: Task with status="completed" and completed_at timestamp

## Error Handling

- Task not found → TASK_NOT_FOUND
- Unauthorized → UNAUTHORIZED
- Already completed → Success (idempotent)

## Failure Modes

| Scenario | Response | Impact |
|----------|----------|--------|
| Task already completed | Success (idempotent) | Agent informs "Task already complete" |
| Task doesn't exist | TASK_NOT_FOUND | Agent informs task not found |
| Wrong user | UNAUTHORIZED | Agent informs can't complete others' tasks |

## Acceptance Criteria

1. ✅ Marks task as completed
2. ✅ Sets completed_at timestamp
3. ✅ Verifies ownership
4. ✅ Idempotent (completing twice is safe)
5. ✅ Returns completed task object
