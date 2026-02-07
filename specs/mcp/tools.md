# MCP Tools Specification

**Component**: MCP (Model Context Protocol) Server Tools
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Overview

The MCP server provides 5 tools that serve as the exclusive data access layer for the Todo Intelligence Platform. All task-related database operations must flow through these tools to enforce user isolation, validation, and security.

**Constitutional Requirement**: Per constitution.md section 5, "Agents may only interact with tasks via MCP tools."

**Tools Provided**:
1. add_task
2. list_tasks
3. update_task
4. complete_task
5. delete_task

---

## Tool 1: add_task

### Purpose
Create a new task for a specific user in the database.

### Parameters

| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| user_id | string | Yes | Non-empty | User creating the task |
| title | string | Yes | 1-200 chars | Task title |
| description | string | No | Max 2000 chars | Task description |
| due_date | string | No | ISO 8601 YYYY-MM-DD | Due date |
| due_time | string | No | HH:MM (24hr) | Due time |
| priority | string | No | Enum: low\|medium\|high | Task priority (default: medium) |
| status | string | No | Enum: pending\|in_progress\|completed | Task status (default: pending) |

### Validation Rules

1. **user_id**: Required, non-empty string
2. **title**: Required, 1-200 characters, trimmed of whitespace
3. **description**: Optional, max 2000 characters if provided
4. **due_date**: Optional, must be valid ISO 8601 date if provided
5. **due_time**: Optional, must be HH:MM format if provided
6. **priority**: Optional, must be one of: low, medium, high (default: medium)
7. **status**: Optional, for new tasks should be "pending" (default: pending)

### Database Effects

```sql
INSERT INTO tasks (
  user_id, title, description, due_date, due_time,
  priority, status, created_at, updated_at
) VALUES (
  $1, $2, $3, $4, $5, $6, $7, NOW(), NOW()
) RETURNING *;
```

**Effects**:
- Creates new row in tasks table
- Auto-generates task_id (serial/auto-increment)
- Sets created_at and updated_at to current timestamp
- Returns complete task object

### Example I/O

**Input**:
```json
{
  "user_id": "user_123",
  "title": "Review architecture spec",
  "description": "Complete review by EOD",
  "due_date": "2025-12-28",
  "priority": "high",
  "status": "pending"
}
```

**Output (Success)**:
```json
{
  "success": true,
  "task": {
    "task_id": 42,
    "user_id": "user_123",
    "title": "Review architecture spec",
    "description": "Complete review by EOD",
    "due_date": "2025-12-28",
    "due_time": null,
    "priority": "high",
    "status": "pending",
    "completed_at": null,
    "created_at": "2025-12-27T10:30:00Z",
    "updated_at": "2025-12-27T10:30:00Z"
  }
}
```

**Output (Error)**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "field": "title"
  }
}
```

---

## Tool 2: list_tasks

### Purpose
Query and retrieve tasks for a specific user with optional filtering, sorting, and pagination.

### Parameters

| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| user_id | string | Yes | Non-empty | User whose tasks to retrieve |
| filters | object | No | See filter rules | Filter criteria |
| filters.status | string | No | Enum: pending\|in_progress\|completed\|deleted | Filter by status |
| filters.priority | string | No | Enum: low\|medium\|high | Filter by priority |
| filters.due_before | string | No | ISO 8601 date | Tasks due before this date |
| filters.due_after | string | No | ISO 8601 date | Tasks due after this date |
| filters.search | string | No | Max 100 chars | Search in title/description |
| sort | string | No | See sort options | Sort order (default: created_at_desc) |
| limit | number | No | 1-100 | Max results (default: 20) |
| offset | number | No | ≥0 | Pagination offset (default: 0) |

### Sort Options

- `created_at_asc`: Oldest first
- `created_at_desc`: Newest first (default)
- `due_date_asc`: Earliest due date first
- `due_date_desc`: Latest due date first
- `priority_asc`: Low to high
- `priority_desc`: High to low
- `title_asc`: Alphabetical
- `title_desc`: Reverse alphabetical

### Validation Rules

1. **user_id**: Required
2. **limit**: 1-100 (default: 20)
3. **offset**: ≥0 (default: 0)
4. **filters.status**: Must be valid enum if provided
5. **filters.priority**: Must be valid enum if provided
6. **filters.due_before/due_after**: Must be valid ISO dates if provided
7. **sort**: Must be valid sort option if provided

### Database Effects

```sql
SELECT * FROM tasks
WHERE user_id = $1
  AND ($2 IS NULL OR status = $2)
  AND ($3 IS NULL OR priority = $3)
  AND ($4 IS NULL OR due_date < $4)
  AND ($5 IS NULL OR due_date > $5)
  AND ($6 IS NULL OR (title ILIKE $6 OR description ILIKE $6))
ORDER BY <sort_field> <sort_direction>
LIMIT $7 OFFSET $8;

-- Also get total count:
SELECT COUNT(*) FROM tasks WHERE <same conditions>;
```

**Effects**:
- Queries tasks table with user_id filter
- Applies optional filters
- Applies sorting
- Returns paginated results
- Never returns other users' tasks

### Example I/O

**Input**:
```json
{
  "user_id": "user_123",
  "filters": {
    "status": "pending",
    "priority": "high"
  },
  "sort": "due_date_asc",
  "limit": 10,
  "offset": 0
}
```

**Output**:
```json
{
  "success": true,
  "tasks": [
    {
      "task_id": 42,
      "title": "Review architecture spec",
      "due_date": "2025-12-28",
      "priority": "high",
      "status": "pending",
      "created_at": "2025-12-27T10:30:00Z"
    },
    {
      "task_id": 45,
      "title": "Prepare presentation",
      "due_date": "2025-12-29",
      "priority": "high",
      "status": "pending",
      "created_at": "2025-12-27T11:00:00Z"
    }
  ],
  "count": 2,
  "has_more": false
}
```

---

## Tool 3: update_task

### Purpose
Update specific fields of an existing task, with ownership verification.

### Parameters

| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| user_id | string | Yes | Non-empty | User updating the task |
| task_id | number | Yes | Positive integer | Task to update |
| updates | object | Yes | At least one field | Fields to update |
| updates.title | string | No | 1-200 chars | New title |
| updates.description | string | No | Max 2000 chars | New description |
| updates.due_date | string | No | ISO 8601 date | New due date |
| updates.due_time | string | No | HH:MM | New due time |
| updates.priority | string | No | Enum | New priority |
| updates.status | string | No | Enum | New status |

### Validation Rules

1. **Ownership**: Task must belong to user_id
2. **Existence**: Task must exist
3. **Updates**: At least one field must be provided
4. **Field values**: Same validation as add_task

### Database Effects

```sql
-- First verify ownership:
SELECT * FROM tasks WHERE task_id = $1 AND user_id = $2;

-- If owned by user:
UPDATE tasks
SET
  title = COALESCE($3, title),
  description = COALESCE($4, description),
  due_date = COALESCE($5, due_date),
  due_time = COALESCE($6, due_time),
  priority = COALESCE($7, priority),
  status = COALESCE($8, status),
  updated_at = NOW()
WHERE task_id = $1 AND user_id = $2
RETURNING *;
```

**Effects**:
- Updates specified fields only
- Preserves other fields
- Updates updated_at timestamp
- Returns updated task

### Example I/O

**Input**:
```json
{
  "user_id": "user_123",
  "task_id": 42,
  "updates": {
    "priority": "high",
    "status": "in_progress"
  }
}
```

**Output (Success)**:
```json
{
  "success": true,
  "task": {
    "task_id": 42,
    "title": "Review architecture spec",
    "priority": "high",
    "status": "in_progress",
    "updated_at": "2025-12-27T15:00:00Z"
  },
  "updated_fields": ["priority", "status"]
}
```

**Output (Unauthorized)**:
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Task does not belong to this user"
  }
}
```

---

## Tool 4: complete_task

### Purpose
Mark a task as completed with ownership verification.

### Parameters

| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| user_id | string | Yes | Non-empty | User completing the task |
| task_id | number | Yes | Positive integer | Task to complete |

### Validation Rules

1. **Ownership**: Task must belong to user_id
2. **Existence**: Task must exist

### Database Effects

```sql
-- Verify ownership:
SELECT * FROM tasks WHERE task_id = $1 AND user_id = $2;

-- Update task:
UPDATE tasks
SET
  status = 'completed',
  completed_at = NOW(),
  updated_at = NOW()
WHERE task_id = $1 AND user_id = $2
RETURNING *;
```

**Effects**:
- Sets status to "completed"
- Sets completed_at to current timestamp
- Updates updated_at timestamp
- Returns completed task

### Example I/O

**Input**:
```json
{
  "user_id": "user_123",
  "task_id": 42
}
```

**Output**:
```json
{
  "success": true,
  "task": {
    "task_id": 42,
    "title": "Review architecture spec",
    "status": "completed",
    "completed_at": "2025-12-27T16:00:00Z",
    "updated_at": "2025-12-27T16:00:00Z"
  }
}
```

---

## Tool 5: delete_task

### Purpose
Delete a task from the database with ownership verification.

### Parameters

| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| user_id | string | Yes | Non-empty | User deleting the task |
| task_id | number | Yes | Positive integer | Task to delete |

### Validation Rules

1. **Ownership**: Task must belong to user_id
2. **Existence**: Task must exist (or idempotent if already deleted)

### Database Effects

```sql
-- Verify ownership:
SELECT * FROM tasks WHERE task_id = $1 AND user_id = $2;

-- Delete task:
DELETE FROM tasks
WHERE task_id = $1 AND user_id = $2
RETURNING task_id;
```

**Effects**:
- Deletes task row from database
- No soft delete (permanent deletion)
- Returns confirmation

### Example I/O

**Input**:
```json
{
  "user_id": "user_123",
  "task_id": 42
}
```

**Output**:
```json
{
  "success": true,
  "task_id": 42,
  "message": "Task deleted successfully"
}
```

---

## Common Error Codes

| Code | Description | HTTP Status | Example |
|------|-------------|-------------|---------|
| VALIDATION_ERROR | Invalid input parameters | 400 | Missing required field |
| UNAUTHORIZED | User doesn't own the task | 403 | Attempting to update another user's task |
| NOT_FOUND | Task doesn't exist | 404 | Task ID not in database |
| DATABASE_ERROR | Database operation failed | 500 | Connection timeout |
| CONSTRAINT_VIOLATION | Database constraint failed | 400 | Invalid foreign key |

## Security Measures

### User Isolation

**Critical**: Every tool MUST include `user_id` in the WHERE clause of all queries.

```sql
-- CORRECT:
SELECT * FROM tasks WHERE task_id = $1 AND user_id = $2;

-- WRONG (security vulnerability):
SELECT * FROM tasks WHERE task_id = $1;
```

### SQL Injection Prevention

All tools use **parameterized queries**:
- Never concatenate user input into SQL strings
- Always use parameter placeholders ($1, $2, etc.)
- Database driver handles escaping

### Input Sanitization

- Trim whitespace from strings
- Validate types before database call
- Reject null bytes and control characters
- Limit string lengths

## Performance Considerations

### Indexes Required

```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

### Connection Pooling

- Maintain pool of database connections
- Reuse connections across requests
- Configure pool size based on load

### Query Optimization

- Use EXPLAIN to verify index usage
- Limit result sets (max 100 per query)
- Avoid N+1 queries (use JOINs if needed)

## Testing Requirements

### Unit Tests

1. Each tool with valid input → success
2. Each tool with invalid input → validation error
3. Each tool with wrong user_id → unauthorized error
4. Each tool with non-existent task → not found error

### Integration Tests

1. add_task → task created in database
2. list_tasks → only user's tasks returned
3. update_task → only specified fields updated
4. complete_task → status and timestamp set correctly
5. delete_task → task removed from database

### Security Tests

1. User A cannot list User B's tasks
2. User A cannot update User B's tasks
3. User A cannot complete User B's tasks
4. User A cannot delete User B's tasks
5. SQL injection attempts blocked

## Acceptance Criteria

An MCP tools implementation is considered compliant if:

1. ✅ All 5 tools implemented and functional
2. ✅ User isolation enforced for all tools
3. ✅ Parameterized queries prevent SQL injection
4. ✅ All validation rules enforced
5. ✅ Error responses standardized
6. ✅ Database indexes present for performance
7. ✅ All security tests pass (no cross-user access)
8. ✅ All integration tests pass
