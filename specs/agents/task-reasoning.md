# Agent Specification: Task Reasoning

**Agent Name**: Task Reasoning Agent
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The Task Reasoning Agent contains all business logic for task management. It interprets user intents related to tasks, enriches task data with intelligent defaults, invokes appropriate task management skills, and handles task-specific workflows.

## Responsibilities

### Primary Responsibilities

1. **Task Intent Interpretation**: Understand what the user wants to do with tasks
2. **Data Enrichment**: Add intelligent defaults (priority, due dates, status)
3. **Skill Invocation**: Call appropriate task management skills
4. **Natural Language Processing**: Convert conversational requests to structured task data
5. **Task Lifecycle Management**: Handle state transitions (pending → in_progress → completed)

### Secondary Responsibilities

1. **Date/Time Parsing**: Convert "tomorrow", "next week", "3pm" to absolute date/times
2. **Priority Inference**: Suggest priority based on keywords (urgent, ASAP, when possible)
3. **Duplicate Detection**: Identify potential duplicate tasks before creation
4. **Task Relationships**: Recognize dependencies (blocked by, related to) - future phases
5. **Smart Defaults**: Apply user preferences and historical patterns - future phases

## Allowed Actions

### Intent Interpretation
- Analyze user intent for task-related actions
- Extract task title, description, due dates from natural language
- Identify create vs update vs list vs complete vs delete operations
- Recognize ambiguous requests requiring clarification

### Data Enrichment
- Parse relative dates ("tomorrow", "next Monday") to ISO dates
- Parse times ("3pm", "EOD", "morning") to specific times
- Infer priority from keywords (urgent → high, someday → low)
- Set default status (new tasks → pending)
- Generate task IDs (delegated to MCP tools)

### Skill Invocation
- Call `task_creation` skill for new tasks
- Call `task_update` skill for modifications
- Call `task_listing` skill for queries
- Call `task_completion` skill for marking done
- Call `task_deletion` skill for removals
- Call `intent_disambiguation` skill when request unclear

### Result Interpretation
- Process skill results
- Extract task IDs, statuses, counts
- Identify success vs failure conditions
- Pass results to Response Formatter Agent

## Skills Used

### Direct Skill Invocations

1. **task_creation**
   - When: User wants to create new task
   - Input: { user_id, title, description, due_date, priority, status }
   - Output: { task_id, status: "created" }

2. **task_update**
   - When: User modifies existing task
   - Input: { user_id, task_id, fields_to_update }
   - Output: { task_id, updated_fields, status: "updated" }

3. **task_listing**
   - When: User queries tasks
   - Input: { user_id, filters, sort, limit }
   - Output: { tasks: [...], count, has_more }

4. **task_completion**
   - When: User marks task done
   - Input: { user_id, task_id }
   - Output: { task_id, status: "completed", completed_at }

5. **task_deletion**
   - When: User deletes task
   - Input: { user_id, task_id }
   - Output: { task_id, status: "deleted" }

6. **intent_disambiguation**
   - When: Request is ambiguous (multiple interpretations possible)
   - Input: { user_input, possible_intents }
   - Output: { clarification_question, options }

## Disallowed Behavior

### Absolutely Prohibited

1. **Direct MCP Tool Calls**: NEVER call MCP tools directly; only via skills
2. **User Data Validation**: NO validation logic (delegate to Validation Agent)
3. **Response Formatting**: NO user-facing response formatting (delegate to Response Formatter)
4. **Authentication**: NO user authentication or authorization checks
5. **Cross-User Operations**: NEVER access tasks for different user_id

### Specific Restrictions

- **NO database queries**: All data access via skills → MCP tools
- **NO state storage**: Every request processed independently
- **NO user preferences caching**: Load from database if needed (future phase)
- **NO hardcoded business rules**: Rules derived from specs, not code
- **NO assumption of skill success**: Always check skill return values

## Input Specification

### Expected Input Format

```json
{
  "user_id": "string (required)",
  "action": "create_task|update_task|list_tasks|complete_task|delete_task",
  "parameters": {
    // Action-specific parameters
  },
  "modality": "text|voice|image",
  "context": {
    "conversation_id": "string (optional)",
    "previous_messages": [] // optional, for conversational context
  }
}
```

### Example Inputs

#### Create Task (Natural Language)
```json
{
  "user_id": "user_123",
  "action": "create_task",
  "parameters": {
    "raw_input": "Add urgent meeting with client tomorrow at 3pm"
  },
  "modality": "text"
}
```

#### Update Task (Structured)
```json
{
  "user_id": "user_456",
  "action": "update_task",
  "parameters": {
    "task_id": 42,
    "title": "Quarterly review meeting",
    "priority": "high"
  },
  "modality": "text"
}
```

#### List Tasks (Filtered)
```json
{
  "user_id": "user_789",
  "action": "list_tasks",
  "parameters": {
    "status": "pending",
    "due_before": "2025-12-31",
    "sort": "due_date_asc",
    "limit": 20
  },
  "modality": "voice"
}
```

## Output Specification

### Expected Output Format

```json
{
  "success": "boolean",
  "skill_invoked": "string (skill name)",
  "result": {
    // Skill-specific result data
  },
  "enrichments": {
    // Data added by Task Reasoning Agent
    "parsed_date": "ISO 8601",
    "inferred_priority": "low|medium|high",
    "defaults_applied": ["status", "priority"]
  },
  "errors": [
    {
      "code": "string",
      "message": "string"
    }
  ]
}
```

### Example Outputs

#### Successful Task Creation
```json
{
  "success": true,
  "skill_invoked": "task_creation",
  "result": {
    "task_id": 42,
    "title": "Urgent meeting with client",
    "due_date": "2025-12-28",
    "due_time": "15:00",
    "priority": "high",
    "status": "pending",
    "created_at": "2025-12-27T10:30:00Z"
  },
  "enrichments": {
    "parsed_date": "tomorrow → 2025-12-28",
    "parsed_time": "3pm → 15:00",
    "inferred_priority": "urgent keyword → high",
    "defaults_applied": ["status: pending"]
  },
  "errors": []
}
```

#### Ambiguous Request Requiring Clarification
```json
{
  "success": false,
  "skill_invoked": "intent_disambiguation",
  "result": {
    "clarification_question": "Which task did you want to update?",
    "options": [
      { "task_id": 10, "title": "Review document" },
      { "task_id": 15, "title": "Review presentation" }
    ]
  },
  "enrichments": {},
  "errors": [
    {
      "code": "AMBIGUOUS_REQUEST",
      "message": "Multiple tasks match 'review'"
    }
  ]
}
```

## Natural Language Processing Logic

### Date/Time Parsing

| User Input | Parsed Output | Logic |
|------------|---------------|-------|
| "tomorrow" | `current_date + 1 day` | Relative date calculation |
| "next Monday" | `next occurrence of Monday` | Weekday calculation |
| "in 3 days" | `current_date + 3 days` | Duration addition |
| "2025-12-28" | `2025-12-28` | ISO date passthrough |
| "3pm" | `15:00` | 12hr → 24hr conversion |
| "EOD" | `17:00` | End of day default |
| "morning" | `09:00` | Morning default |

### Priority Inference

| Keywords | Inferred Priority | Confidence |
|----------|-------------------|------------|
| urgent, ASAP, critical, emergency | high | high |
| important, priority, soon | high | medium |
| when possible, someday, eventually | low | high |
| (no keywords) | medium | default |

### Status Defaults

| Action | Default Status |
|--------|----------------|
| create_task | pending |
| update_task | (preserve current) |
| complete_task | completed |
| delete_task | deleted |

## Execution Flow

### Create Task Flow

```
1. Receive intent with raw user input
   ↓
2. Parse natural language:
   - Extract title (required)
   - Extract description (optional)
   - Parse due date/time (optional)
   - Infer priority (default: medium)
   ↓
3. Apply defaults:
   - status: pending
   - priority: medium (if not inferred)
   - due_date: null (if not specified)
   ↓
4. Construct skill parameters:
   {
     user_id, title, description,
     due_date, due_time, priority, status
   }
   ↓
5. Invoke task_creation skill
   ↓
6. Receive skill result:
   - If success: { task_id, status: "created" }
   - If failure: { error_code, message }
   ↓
7. Return result with enrichments to Orchestrator
```

### Update Task Flow

```
1. Receive intent with task_id + fields to update
   ↓
2. Parse updates:
   - If title changed: extract new title
   - If due_date changed: parse new date
   - If priority changed: validate priority value
   ↓
3. Construct skill parameters:
   { user_id, task_id, fields_to_update }
   ↓
4. Invoke task_update skill
   ↓
5. Receive skill result:
   - If success: { task_id, updated_fields }
   - If failure: { error_code, message }
   ↓
6. Return result to Orchestrator
```

### List Tasks Flow

```
1. Receive intent with filters (status, due_before, search, etc.)
   ↓
2. Parse filters:
   - Convert date filters to ISO format
   - Validate sort options
   - Apply default limit (20) if not specified
   ↓
3. Construct skill parameters:
   { user_id, filters, sort, limit, offset }
   ↓
4. Invoke task_listing skill
   ↓
5. Receive skill result:
   { tasks: [...], count, has_more }
   ↓
6. Return task list to Orchestrator
```

## Error Handling

### Error Categories

1. **Parsing Errors**: Cannot extract title or required fields
2. **Ambiguity Errors**: Multiple interpretations possible
3. **Skill Errors**: task_creation/update/etc. fails
4. **Data Errors**: Invalid dates, priorities, statuses

### Error Response Strategy

```
If user input is ambiguous:
  → Invoke intent_disambiguation skill
  → Return clarification question to user
  → Do NOT guess

If required field missing:
  → Return error: "Cannot create task without title"
  → Do NOT create partial task

If skill fails:
  → Pass skill error to Orchestrator
  → Do NOT retry automatically
  → Let user decide next action

If date parsing fails:
  → Use null for due_date
  → Log parsing failure
  → Proceed with task creation
```

## State Management

### Request-Scoped State Only

```python
# Conceptual example
class TaskReasoningAgent:
    def process_task_intent(self, intent):
        # Temporary state during request processing
        parsed_data = self.parse_natural_language(intent.parameters)
        enriched_data = self.apply_defaults(parsed_data)

        skill_result = self.invoke_skill(
            skill_name="task_creation",
            parameters=enriched_data
        )

        return {
            "success": skill_result.success,
            "result": skill_result.data,
            "enrichments": {
                "parsed_date": parsed_data.due_date,
                "inferred_priority": parsed_data.priority
            }
        }

    # After return, all state is discarded
```

### Prohibited State

- **NO task caching**: Load from database every request
- **NO user preferences**: Load from database if needed (future)
- **NO request history**: No memory of previous tasks created
- **NO learning**: No ML model updates based on user patterns (future)

## Testing Requirements

### Unit Tests

1. Date parsing (tomorrow, next Monday, in 3 days, ISO dates)
2. Time parsing (3pm, EOD, morning, 24hr format)
3. Priority inference (urgent, ASAP, someday, no keywords)
4. Default application (status, priority when missing)
5. Skill parameter construction (all required fields present)

### Integration Tests

1. End-to-end task creation from natural language
2. Task update with partial field changes
3. Task listing with multiple filters
4. Task completion and deletion flows
5. Ambiguous request disambiguation

### Edge Cases

1. Empty title → error
2. Invalid date format → null due_date
3. Unknown priority value → default to medium
4. Task ID not found → skill error propagated
5. Multiple matches for "review" → disambiguation invoked

## Failure Modes

| Failure Scenario | Detection | Response | User Impact |
|------------------|-----------|----------|-------------|
| Cannot parse title | Title extraction returns null | Return error: "Please provide task title" | Request rejected |
| Invalid date format | Date parsing fails | Set due_date = null, proceed | Task created without due date |
| Skill invocation fails | skill_result.success = false | Propagate skill error | Request fails with specific error |
| Ambiguous request | Multiple tasks match user input | Invoke disambiguation | User presented with options |
| Missing user_id | Input validation | Return error: "Unauthorized" | Request rejected |

## Dependencies

### Required Components

- **task_creation skill**: For creating new tasks
- **task_update skill**: For modifying tasks
- **task_listing skill**: For querying tasks
- **task_completion skill**: For marking tasks done
- **task_deletion skill**: For removing tasks
- **intent_disambiguation skill**: For ambiguous requests

### Optional Components

- **Natural Language Understanding**: For advanced parsing (Phase 4+)
- **User Preferences**: For personalized defaults (future)
- **Task Relationships**: For dependency tracking (future)

## Versioning and Evolution

### Phase 1 (CLI)
- Basic CRUD operations
- Simple date parsing (ISO format only)
- Manual priority specification

### Phase 2-3 (Web + Voice)
- Natural language date parsing
- Priority inference from keywords
- Conversational task creation

### Phase 4 (AI Chatbot)
- Advanced NLU (spaCy, transformers)
- Context-aware task enrichment
- Multi-turn task building

### Phase 5 (Multimodal)
- Image-extracted text integration
- Visual context enrichment
- Cross-modal task creation

## Acceptance Criteria

A Task Reasoning Agent implementation is considered compliant if:

1. ✅ Parses natural language dates correctly (tomorrow, next week, etc.)
2. ✅ Infers priority from keywords accurately
3. ✅ Invokes correct skill for each action type
4. ✅ Applies defaults for missing fields
5. ✅ Handles ambiguous requests via disambiguation
6. ✅ Never calls MCP tools directly
7. ✅ Returns structured results with enrichments
8. ✅ Passes all unit and integration tests
