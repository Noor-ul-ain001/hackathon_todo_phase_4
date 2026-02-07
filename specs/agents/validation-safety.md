# Agent Specification: Validation and Safety

**Agent Name**: Validation and Safety Agent
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The Validation and Safety Agent enforces all input validation rules, business constraints, and safety checks before task operations execute. It acts as the final gatekeeper preventing invalid, dangerous, or nonsensical operations from reaching the database.

## Responsibilities

### Primary Responsibilities

1. **Input Validation**: Verify all required fields present and correctly formatted
2. **Business Rule Enforcement**: Apply business constraints (dates, priorities, status transitions)
3. **Safety Checks**: Prevent destructive operations without confirmation
4. **Data Integrity**: Ensure data consistency and referential integrity
5. **User Isolation**: Verify user can only access their own tasks

### Secondary Responsibilities

1. **Sanitization**: Clean inputs to prevent injection attacks
2. **Range Validation**: Check numeric and date ranges
3. **Enum Validation**: Verify status, priority values are valid
4. **Length Limits**: Enforce max lengths for titles, descriptions
5. **Warning Generation**: Provide non-blocking warnings for suspicious inputs

## Allowed Actions

### Validation Operations
- Check required fields present (user_id, task_id, title, etc.)
- Validate data types (string, number, date, enum)
- Verify string lengths within limits
- Validate date formats and ranges
- Check enum values (status, priority)
- Verify user_id matches task owner (for updates/deletes)

### Safety Checks
- Prevent past due dates (optional warning, not blocking)
- Detect potentially invalid status transitions
- Identify suspicious batch operations
- Check for destructive operations (delete without confirmation)
- Validate bulk operation limits

### Error Reporting
- Generate field-specific error messages
- Provide actionable correction guidance
- Distinguish blocking errors vs warnings
- Return validation summary (all errors at once, not fail-fast)

## Skills Used

**None directly**. The Validation Agent performs logic-based validation without invoking external skills.

However, it may need to query data via the Orchestrator if validation requires checking existing task state (e.g., "Can user delete this task?" → need to verify ownership).

## Disallowed Behavior

### Absolutely Prohibited

1. **Business Logic Execution**: NO task creation, updates, or deletions
2. **Skill Invocation**: NO calling task management skills
3. **Data Modification**: NO changes to database state
4. **Response Formatting**: NO user-facing response formatting
5. **Authentication**: NO user authentication (handled by API layer)

### Specific Restrictions

- **NO MCP tool calls**: Validation is logic-only (unless ownership check needed - TBD)
- **NO assuming valid**: Every field must be explicitly checked
- **NO silent failures**: All errors must be reported
- **NO auto-correction**: Report errors, don't guess user intent
- **NO state storage**: Validation rules stateless

## Input Specification

### Expected Input Format

```json
{
  "user_id": "string (required)",
  "action": "create_task|update_task|complete_task|delete_task",
  "parameters": {
    // Action-specific fields to validate
  },
  "context": {
    "is_destructive": "boolean (true for delete operations)"
  }
}
```

### Example Inputs

#### Validate Task Creation
```json
{
  "user_id": "user_123",
  "action": "create_task",
  "parameters": {
    "title": "Review architecture spec",
    "description": "Complete by EOD",
    "due_date": "2025-12-28",
    "priority": "high",
    "status": "pending"
  },
  "context": {
    "is_destructive": false
  }
}
```

#### Validate Task Deletion
```json
{
  "user_id": "user_456",
  "action": "delete_task",
  "parameters": {
    "task_id": 42
  },
  "context": {
    "is_destructive": true
  }
}
```

## Output Specification

### Expected Output Format

```json
{
  "valid": "boolean (true if all checks pass)",
  "errors": [
    {
      "field": "string (field name with error)",
      "code": "string (error code)",
      "message": "string (user-friendly message)",
      "severity": "error|warning"
    }
  ],
  "warnings": [
    {
      "field": "string",
      "code": "string",
      "message": "string"
    }
  ],
  "sanitized_data": {
    // Cleaned/normalized version of input parameters
  }
}
```

### Example Outputs

#### Valid Input
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "sanitized_data": {
    "title": "Review architecture spec",
    "description": "Complete by EOD",
    "due_date": "2025-12-28",
    "priority": "high",
    "status": "pending"
  }
}
```

#### Invalid Input (Multiple Errors)
```json
{
  "valid": false,
  "errors": [
    {
      "field": "title",
      "code": "TITLE_TOO_LONG",
      "message": "Title must be 200 characters or less (got 250)",
      "severity": "error"
    },
    {
      "field": "due_date",
      "code": "INVALID_DATE_FORMAT",
      "message": "Due date must be in ISO 8601 format (YYYY-MM-DD)",
      "severity": "error"
    },
    {
      "field": "priority",
      "code": "INVALID_ENUM_VALUE",
      "message": "Priority must be one of: low, medium, high (got 'urgent')",
      "severity": "error"
    }
  ],
  "warnings": [],
  "sanitized_data": null
}
```

#### Valid with Warnings
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "field": "due_date",
      "code": "DUE_DATE_IN_PAST",
      "message": "Due date is in the past - task will be immediately overdue"
    }
  ],
  "sanitized_data": {
    "title": "Complete last quarter report",
    "due_date": "2025-11-15",
    "priority": "medium",
    "status": "pending"
  }
}
```

## Validation Rules

### Universal Rules (All Actions)

| Field | Rule | Error Code | Error Message |
|-------|------|------------|---------------|
| user_id | Required, non-empty string | MISSING_USER_ID | "User ID is required" |
| user_id | UUID format (or app-specific format) | INVALID_USER_ID | "User ID format is invalid" |
| action | Required, valid enum | INVALID_ACTION | "Action must be one of: create_task, update_task, list_tasks, complete_task, delete_task" |

### Create Task Rules

| Field | Rule | Error Code | Error Message |
|-------|------|------------|---------------|
| title | Required | MISSING_TITLE | "Task title is required" |
| title | 1-200 characters | TITLE_TOO_SHORT / TITLE_TOO_LONG | "Title must be between 1 and 200 characters" |
| description | Optional, max 2000 characters | DESCRIPTION_TOO_LONG | "Description must be 2000 characters or less" |
| due_date | Optional, ISO 8601 format (YYYY-MM-DD) | INVALID_DATE_FORMAT | "Due date must be in format YYYY-MM-DD" |
| due_date | If present, not more than 10 years in future | DUE_DATE_TOO_FAR | "Due date cannot be more than 10 years in the future" |
| due_time | Optional, HH:MM format (24hr) | INVALID_TIME_FORMAT | "Time must be in format HH:MM (24-hour)" |
| priority | Optional, one of: low, medium, high | INVALID_PRIORITY | "Priority must be: low, medium, or high" |
| status | Optional, must be "pending" for new tasks | INVALID_STATUS_FOR_CREATE | "New tasks must have status 'pending'" |

### Update Task Rules

| Field | Rule | Error Code | Error Message |
|-------|------|------------|---------------|
| task_id | Required, positive integer | MISSING_TASK_ID / INVALID_TASK_ID | "Valid task ID is required" |
| title | If present, 1-200 characters | TITLE_TOO_SHORT / TITLE_TOO_LONG | "Title must be between 1 and 200 characters" |
| status | If present, valid transition allowed | INVALID_STATUS_TRANSITION | "Cannot transition from {current} to {new}" |

### Complete Task Rules

| Field | Rule | Error Code | Error Message |
|-------|------|------------|---------------|
| task_id | Required, positive integer | MISSING_TASK_ID | "Task ID is required to complete task" |

### Delete Task Rules

| Field | Rule | Error Code | Error Message |
|-------|------|------------|---------------|
| task_id | Required, positive integer | MISSING_TASK_ID | "Task ID is required to delete task" |
| confirmation | Optional, if present must be true | DESTRUCTIVE_OP_NOT_CONFIRMED | "Destructive operation requires confirmation" |

### List Tasks Rules

| Field | Rule | Error Code | Error Message |
|-------|------|------------|---------------|
| limit | Optional, 1-100 | INVALID_LIMIT | "Limit must be between 1 and 100" |
| offset | Optional, non-negative integer | INVALID_OFFSET | "Offset must be 0 or greater" |
| status | If present, valid enum | INVALID_STATUS_FILTER | "Status filter must be: pending, in_progress, completed, deleted" |
| sort | If present, valid field + direction | INVALID_SORT | "Sort must be: field_name_asc or field_name_desc" |

## Execution Flow

### Standard Validation Flow

```
1. Receive intent from Orchestrator
   ↓
2. Determine validation rules based on action
   ↓
3. Check universal rules (user_id, action)
   ↓
4. Check action-specific rules (create vs update vs delete)
   ↓
5. Collect ALL errors (don't stop at first error)
   ↓
6. Check for warnings (non-blocking issues)
   ↓
7. If errors exist:
      → Set valid = false
      → Return all errors
      → Set sanitized_data = null
   ↓
8. If no errors:
      → Set valid = true
      → Return sanitized/normalized data
      → Include warnings if any
   ↓
9. Return validation result to Orchestrator
```

### Sanitization Logic

```
1. Trim whitespace from strings (title, description)
2. Normalize dates to ISO 8601 format
3. Convert priority/status to lowercase
4. Remove null bytes and control characters
5. Escape special SQL characters (if not using parameterized queries - but we are)
6. Truncate descriptions at 2000 characters (with warning)
7. Return sanitized version
```

## Error Handling

### Error Collection Strategy

**Fail-Complete, not Fail-Fast**:
- Check ALL fields before returning
- Report ALL errors in a single response
- Allows user to fix all issues at once
- Better UX than iterative error discovery

### Warning Strategy

Warnings are non-blocking issues that don't prevent operation:
- Due date in the past (user might be logging historical tasks)
- Very long title (close to limit)
- Suspicious patterns (title = "test", "asdf", etc.)
- Unusual status transitions (completed → pending)

User sees warnings but operation proceeds if no errors.

## State Management

### Stateless Validation

```python
# Conceptual example
class ValidationAgent:
    VALIDATION_RULES = {
        "create_task": {
            "title": {"required": True, "min_length": 1, "max_length": 200},
            "description": {"required": False, "max_length": 2000},
            # ...
        },
        # ... other actions
    }

    def validate(self, intent):
        errors = []
        warnings = []

        rules = self.VALIDATION_RULES[intent.action]

        for field, field_rules in rules.items():
            value = intent.parameters.get(field)

            # Check each rule
            if field_rules.get("required") and not value:
                errors.append({"field": field, "code": "MISSING_FIELD", ...})

            if value and field_rules.get("max_length"):
                if len(value) > field_rules["max_length"]:
                    errors.append({"field": field, "code": "TOO_LONG", ...})

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    # No state stored across requests
```

### Prohibited State

- **NO validation history**: Every request validated fresh
- **NO user-specific rules**: All users subject to same rules (for now)
- **NO learning**: No ML-based validation (for now)
- **NO caching**: No cached validation results

## Testing Requirements

### Unit Tests

1. Required field validation (missing title, user_id, task_id)
2. Length validation (title, description limits)
3. Format validation (dates, times, UUIDs)
4. Enum validation (priority, status values)
5. Range validation (dates not too far future)
6. Sanitization (whitespace trimming, normalization)

### Integration Tests

1. End-to-end validation of valid task creation
2. End-to-end validation with multiple errors
3. Warning generation for edge cases
4. Sanitized data passed to skills correctly

### Edge Cases

1. Empty title → error
2. Title with only whitespace → error (after trim)
3. Description exactly 2000 characters → valid
4. Description 2001 characters → error
5. Due date in past → warning, not error
6. Invalid enum value → error with valid options listed
7. Multiple errors simultaneously → all reported

## Failure Modes

| Failure Scenario | Detection | Response | User Impact |
|------------------|-----------|----------|-------------|
| Missing required field | Field not in parameters | Return error with field name | Request rejected with specific error |
| Invalid data type | Type check fails | Return error: "Expected string, got number" | Request rejected |
| Exceeds length limit | len(value) > max | Return error with limit | Request rejected |
| Invalid enum value | Value not in allowed set | Return error with allowed values | Request rejected |
| Multiple errors | Multiple rules fail | Return all errors | User fixes all issues at once |

## Dependencies

### Required Components

None - Validation Agent is self-contained logic.

### Optional Components

- **Task Ownership Check**: May need to query database to verify user owns task (for updates/deletes)
  - If needed, would call via Orchestrator → skill → MCP tool
  - For Phase 1 (single user), ownership check not needed

## Versioning and Evolution

### Phase 1 (CLI)
- Basic field validation
- Type and length checks
- Simple sanitization

### Phase 2-3 (Web + Voice)
- Multi-user ownership checks
- Enhanced sanitization (XSS prevention)
- Rate limiting validation

### Phase 4 (AI Chatbot)
- Semantic validation (does task make sense?)
- Context-aware validation (based on conversation)
- ML-based anomaly detection

### Phase 5 (Multimodal)
- Image content validation
- Cross-modal consistency checks
- Visual context safety checks

## Acceptance Criteria

A Validation and Safety Agent implementation is considered compliant if:

1. ✅ Enforces all required field rules
2. ✅ Validates all length, format, and enum constraints
3. ✅ Returns ALL errors in a single response (fail-complete)
4. ✅ Distinguishes between blocking errors and warnings
5. ✅ Sanitizes inputs before returning
6. ✅ Never modifies database state
7. ✅ Provides actionable error messages
8. ✅ Passes all unit and integration tests
