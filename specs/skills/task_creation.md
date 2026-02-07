# Skill Specification: Task Creation

**Skill Name**: task_creation
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The task_creation skill provides a reusable capability for creating new tasks in the system. It wraps the MCP add_task tool and handles the skill-level concerns of parameter preparation, error handling, and result formatting.

## Responsibilities

1. Accept task creation parameters from agents
2. Validate parameter format (basic structure check)
3. Invoke the add_task MCP tool
4. Handle MCP tool responses (success and errors)
5. Return formatted result to calling agent

## Inputs

### Input Schema

```json
{
  "user_id": "string (required)",
  "title": "string (required, 1-200 characters)",
  "description": "string (optional, max 2000 characters)",
  "due_date": "string (optional, ISO 8601 format YYYY-MM-DD)",
  "due_time": "string (optional, HH:MM 24-hour format)",
  "priority": "string (optional, enum: low|medium|high)",
  "status": "string (optional, default: pending)"
}
```

### Input Examples

**Basic Task**:
```json
{
  "user_id": "user_123",
  "title": "Review architecture spec"
}
```

**Complete Task**:
```json
{
  "user_id": "user_456",
  "title": "Quarterly review meeting",
  "description": "Review Q4 results and plan Q1 objectives",
  "due_date": "2025-12-30",
  "due_time": "14:00",
  "priority": "high",
  "status": "pending"
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
  "error": {
    "code": "string",
    "message": "string"
  } | null
}
```

### Output Examples

**Success**:
```json
{
  "success": true,
  "task": {
    "task_id": 42,
    "title": "Review architecture spec",
    "description": null,
    "due_date": null,
    "due_time": null,
    "priority": "medium",
    "status": "pending",
    "created_at": "2025-12-27T10:30:00Z",
    "updated_at": "2025-12-27T10:30:00Z"
  },
  "error": null
}
```

**Error**:
```json
{
  "success": false,
  "task": null,
  "error": {
    "code": "MCP_TOOL_ERROR",
    "message": "Failed to create task: database connection timeout"
  }
}
```

## Triggers

### Text Modality
- CLI command: `todo add "Task title" --due 2025-12-28`
- Natural language: "Add task to review the architecture spec"
- Chat input: "Create a new task for the meeting tomorrow"

### Voice Modality
- Voice command: "Add meeting with client tomorrow at 3pm"
- Transcribed to text, then normalized to intent

### Image Modality
- Image with text extracted: "Quarterly Review Meeting Dec 30"
- Visual Context Agent extracts data, passes to this skill

## Execution Flow

```
1. Receive task parameters from calling agent
   ↓
2. Validate input structure
   - user_id present and non-empty
   - title present and non-empty
   - Optional fields have correct types
   ↓
3. Prepare MCP tool parameters
   - Map skill inputs to MCP tool format
   - Set defaults (status = "pending" if not provided)
   ↓
4. Invoke add_task MCP tool
   - Pass: user_id, title, description, due_date, due_time, priority, status
   ↓
5. Receive MCP tool response
   ↓
6. If MCP tool succeeds:
      → Extract task data from response
      → Format success response
      → Return to calling agent
   ↓
7. If MCP tool fails:
      → Extract error details
      → Format error response
      → Return to calling agent
```

## MCP Tool Invocation

### Tool Called
**add_task** (from MCP tool layer)

### Parameters Passed
```json
{
  "user_id": "<from input>",
  "title": "<from input>",
  "description": "<from input or null>",
  "due_date": "<from input or null>",
  "due_time": "<from input or null>",
  "priority": "<from input or 'medium'>",
  "status": "<from input or 'pending'>"
}
```

### Response Handling
- **Success**: MCP tool returns `{ "task_id": 42, "created_at": "...", ... }`
- **Failure**: MCP tool returns `{ "error": { "code": "...", "message": "..." } }`

## Error Handling

### Error Categories

1. **Input Validation Errors**
   - Missing user_id: Return error "user_id is required"
   - Missing title: Return error "title is required"
   - Invalid types: Return error with specific field

2. **MCP Tool Errors**
   - Database connection failure
   - Constraint violation (e.g., duplicate task)
   - Timeout
   - Unknown errors

### Error Response Strategy

```
If input validation fails:
  → Return error immediately (don't call MCP tool)
  → Error code: "INVALID_INPUT"

If MCP tool fails:
  → Capture MCP error
  → Wrap in skill error response
  → Error code: "MCP_TOOL_ERROR"
  → Include original MCP error message

All errors include:
  - success: false
  - task: null
  - error: { code, message }
```

## Failure Modes

| Failure Scenario | Detection | Response | Calling Agent Impact |
|------------------|-----------|----------|----------------------|
| Missing user_id | Input validation | Error: "user_id required" | Agent receives error, can retry with user_id |
| Missing title | Input validation | Error: "title required" | Agent receives error, can extract title from user input |
| MCP tool timeout | MCP tool call fails | Error: "Database timeout" | Agent receives error, can retry |
| Database constraint violation | MCP tool returns error | Error: "Task creation failed" | Agent receives error, can inform user |
| Unknown error | Exception during execution | Error: "Unexpected error occurred" | Agent receives error, can log and inform user |

## Validation Rules

### Skill-Level Validation (Before MCP Call)

The skill performs basic structure validation:
- user_id is present and is a string
- title is present and is a string
- If due_date provided: is a string (format validation done by Validation Agent)
- If priority provided: is a string (enum validation done by Validation Agent)

**Note**: Detailed validation (length limits, enum values, date formats) is handled by the Validation Agent before the skill is invoked.

## State Management

### Stateless Operation

The task_creation skill is completely stateless:
- No cached data
- No session memory
- Each invocation is independent
- All context comes from input parameters

```python
# Conceptual example
def task_creation_skill(input_params):
    # 1. Validate input structure
    if not input_params.get("user_id"):
        return {"success": False, "error": {"code": "INVALID_INPUT", "message": "user_id required"}}

    if not input_params.get("title"):
        return {"success": False, "error": {"code": "INVALID_INPUT", "message": "title required"}}

    # 2. Call MCP tool
    mcp_result = mcp_client.call_tool(
        tool="add_task",
        parameters=input_params
    )

    # 3. Handle response
    if mcp_result.success:
        return {
            "success": True,
            "task": mcp_result.task,
            "error": None
        }
    else:
        return {
            "success": False,
            "task": None,
            "error": mcp_result.error
        }

    # No state retained after return
```

## Testing Requirements

### Unit Tests

1. Valid input → MCP tool called correctly
2. Missing user_id → error returned, MCP tool not called
3. Missing title → error returned, MCP tool not called
4. MCP tool success → success response formatted correctly
5. MCP tool failure → error response formatted correctly

### Integration Tests

1. End-to-end: skill → MCP tool → database → task created
2. Error propagation: MCP tool error → skill error → agent receives error
3. All input variations: minimal, complete, optional fields

### Edge Cases

1. Empty title string → validation error
2. Very long title (201 characters) → passed to MCP tool, which validates
3. Invalid priority value → passed to MCP tool, which validates
4. Null optional fields → handled gracefully

## Dependencies

### Required Components

- **MCP add_task tool**: For creating tasks in database
- **MCP client library**: For invoking MCP tools

### Optional Components

None - skill is self-contained

## Versioning and Evolution

### Version 1.0 (Current)
- Basic task creation
- Supports all standard task fields
- Error handling for MCP tool failures

### Future Enhancements (Potential)
- Batch task creation (create multiple tasks at once)
- Template-based task creation
- Task duplication from existing task
- Subtask creation (if hierarchy added)

## Acceptance Criteria

A task_creation skill implementation is considered compliant if:

1. ✅ Accepts all required input parameters (user_id, title)
2. ✅ Accepts all optional input parameters (description, due_date, due_time, priority, status)
3. ✅ Validates input structure before MCP call
4. ✅ Invokes add_task MCP tool with correct parameters
5. ✅ Returns success response when MCP tool succeeds
6. ✅ Returns error response when MCP tool fails
7. ✅ Returns error response when input validation fails
8. ✅ Is completely stateless (no retained state)
9. ✅ Passes all unit and integration tests
