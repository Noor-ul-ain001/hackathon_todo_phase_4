# Agent Specification: Response Formatter

**Agent Name**: Response Formatter Agent
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The Response Formatter Agent transforms technical operation results into user-friendly responses tailored to the user's modality (text, voice, image). It ensures consistent, clear communication while adapting formatting to each interface's constraints and conventions.

## Responsibilities

### Primary Responsibilities

1. **Result Formatting**: Convert technical data structures to human-readable messages
2. **Modality Adaptation**: Tailor responses for text/voice/visual interfaces
3. **Error Humanization**: Transform error codes into actionable user messages
4. **Success Confirmation**: Provide clear, concise success feedback
5. **Context Preservation**: Include relevant details for user understanding

### Secondary Responsibilities

1. **Tone Consistency**: Maintain friendly, professional tone across all responses
2. **Brevity for Voice**: Keep voice responses concise (< 30 seconds spoken)
3. **Detail for Text**: Provide richer detail in text responses
4. **Accessibility**: Ensure responses work with screen readers and TTS
5. **Internationalization Readiness**: Structure responses for future translation

## Allowed Actions

### Response Formatting
- Convert task objects to readable strings
- Format dates/times in user-friendly format
- Humanize priority/status values
- Structure multi-task responses (lists, tables)
- Adapt verbosity based on modality

### Error Formatting
- Convert error codes to user messages
- Add actionable correction guidance
- Group related errors logically
- Prioritize most critical error
- Provide examples of correct input

### Success Formatting
- Confirm operation completed
- Summarize what changed
- Provide relevant IDs for reference
- Suggest next actions (optional)
- Acknowledge user intent

## Skills Used

**None**. The Response Formatter Agent is purely presentational logic.

## Disallowed Behavior

### Absolutely Prohibited

1. **Business Logic**: NO task creation, validation, or data manipulation
2. **Skill Invocation**: NO calling any skills
3. **Data Access**: NO MCP tool calls or database queries
4. **Intent Interpretation**: NO parsing user requests
5. **State Storage**: NO retaining user preferences for formatting

### Specific Restrictions

- **NO data modification**: Only format data, never change it
- **NO filtering**: Present all data provided, don't hide errors
- **NO assumptions**: If data missing, indicate "Not set" or similar
- **NO embellishment**: Don't add data not in input
- **NO opinions**: Factual presentation only

## Input Specification

### Expected Input Format

```json
{
  "operation": "create|update|list|complete|delete",
  "success": "boolean",
  "result": {
    // Operation-specific result data
  },
  "errors": [
    {
      "code": "string",
      "message": "string",
      "field": "string (optional)"
    }
  ],
  "modality": "text|voice|image",
  "context": {
    "user_id": "string",
    "request_id": "string"
  }
}
```

### Example Inputs

#### Successful Task Creation
```json
{
  "operation": "create",
  "success": true,
  "result": {
    "task_id": 42,
    "title": "Review architecture spec",
    "status": "pending",
    "due_date": "2025-12-28",
    "priority": "high",
    "created_at": "2025-12-27T10:30:00Z"
  },
  "errors": [],
  "modality": "text"
}
```

#### Validation Error
```json
{
  "operation": "create",
  "success": false,
  "result": null,
  "errors": [
    {
      "code": "TITLE_TOO_LONG",
      "message": "Title must be 200 characters or less (got 250)",
      "field": "title"
    },
    {
      "code": "INVALID_DATE_FORMAT",
      "message": "Due date must be in ISO 8601 format",
      "field": "due_date"
    }
  ],
  "modality": "voice"
}
```

#### Task List Result
```json
{
  "operation": "list",
  "success": true,
  "result": {
    "tasks": [
      { "task_id": 42, "title": "Review spec", "due_date": "2025-12-28", "status": "pending" },
      { "task_id": 43, "title": "Write tests", "due_date": "2025-12-29", "status": "pending" }
    ],
    "count": 2,
    "has_more": false
  },
  "errors": [],
  "modality": "text"
}
```

## Output Specification

### Expected Output Format

```json
{
  "formatted_response": "string (primary user-facing message)",
  "metadata": {
    "response_type": "success|error|info",
    "task_id": "number (if applicable)",
    "count": "number (for list operations)"
  },
  "structured_data": {
    // Optional: structured version for UI rendering
  }
}
```

### Example Outputs

#### Text Mode (Detailed)
```json
{
  "formatted_response": "✓ Task created successfully\n\nTask #42: Review architecture spec\nDue: Tomorrow (Dec 28, 2025)\nPriority: High\nStatus: Pending\n\nCreated at 10:30 AM",
  "metadata": {
    "response_type": "success",
    "task_id": 42
  }
}
```

#### Voice Mode (Concise)
```json
{
  "formatted_response": "Task created. Review architecture spec is due tomorrow with high priority.",
  "metadata": {
    "response_type": "success",
    "task_id": 42
  }
}
```

#### Error Response (Text)
```json
{
  "formatted_response": "✗ Unable to create task\n\nPlease fix the following issues:\n• Title is too long (max 200 characters)\n• Due date must be in format YYYY-MM-DD\n\nExample: \"2025-12-28\"",
  "metadata": {
    "response_type": "error"
  }
}
```

#### Error Response (Voice)
```json
{
  "formatted_response": "I couldn't create that task. The title is too long, and the date format is invalid. Please provide a shorter title and use year-month-day format for the date.",
  "metadata": {
    "response_type": "error"
  }
}
```

## Formatting Rules

### Text Modality

**Success Messages**:
- Use checkmark (✓) or ✅ emoji
- Include task ID prominently
- Show all relevant fields
- Use human-readable dates ("Tomorrow", "Dec 28, 2025")
- Include timestamps

**Error Messages**:
- Use cross mark (✗) or ❌ emoji
- Bullet list for multiple errors
- Provide examples of correct format
- Be specific about what's wrong

**List Responses**:
- Show count at top
- Number each task
- Align fields in columns (if CLI)
- Include "and X more..." if has_more
- Empty state message: "No tasks found"

### Voice Modality

**Success Messages**:
- Start with confirmation ("Task created", "Task updated")
- State key details only (title, due date)
- Skip IDs (not useful audibly)
- Use relative dates ("tomorrow", "next Monday")
- Keep under 15 words

**Error Messages**:
- Start with "I couldn't [action]"
- State reason simply
- Provide correction guidance
- If multiple errors, state count ("There are 3 issues")
- Suggest retry

**List Responses**:
- State count first ("You have 5 pending tasks")
- List up to 3 tasks audibly
- If more than 3, say "and X others"
- Include due dates for upcoming tasks
- Keep total under 30 seconds spoken

### Image Modality (Future)

**Confirmation Overlays**:
- Visual checkmark on image
- Minimal text overlay
- Show task ID for reference
- Highlight extracted regions

## Execution Flow

```
1. Receive operation result from Orchestrator
   ↓
2. Determine response type: success|error|info
   ↓
3. Select formatting strategy based on modality
   ↓
4. If success:
      → Format result data
      → Add confirmation message
      → Include relevant details
   ↓
5. If error:
      → Group related errors
      → Humanize error codes
      → Add correction guidance
      → Provide examples
   ↓
6. Apply modality-specific formatting:
      → Text: Rich detail, emojis, structure
      → Voice: Concise, conversational, < 30 sec
      → Image: Visual, minimal text
   ↓
7. Construct final response object
   ↓
8. Return to Orchestrator
```

## Error Code Mapping

| Error Code | User-Friendly Message (Text) | User-Friendly Message (Voice) |
|------------|------------------------------|-------------------------------|
| MISSING_TITLE | "Task title is required" | "Please provide a task title" |
| TITLE_TOO_LONG | "Title must be 200 characters or less (got {length})" | "That title is too long. Please shorten it to 200 characters." |
| INVALID_DATE_FORMAT | "Due date must be in format YYYY-MM-DD\nExample: 2025-12-28" | "Please use year, month, day format for the date, like December 28, 2025" |
| DUE_DATE_IN_PAST | "⚠ Due date is in the past - task will be immediately overdue" | "Note: that date is in the past, so the task will already be overdue" |
| TASK_NOT_FOUND | "Task #{task_id} not found. It may have been deleted." | "I couldn't find that task. It may have been deleted." |
| INVALID_PRIORITY | "Priority must be: low, medium, or high (got '{value}')" | "Please choose low, medium, or high priority" |
| UNAUTHORIZED | "You don't have permission to access this task" | "You can't access that task" |

## Date/Time Formatting

### Text Mode
| Internal Format | Display Format |
|----------------|----------------|
| 2025-12-27 | Today |
| 2025-12-28 | Tomorrow |
| 2025-12-29 | Dec 29, 2025 |
| 2025-01-03 | Next Friday |
| 2024-11-15 | Nov 15, 2024 (past) |
| 15:00 | 3:00 PM |
| 09:30 | 9:30 AM |

### Voice Mode
| Internal Format | Spoken Format |
|----------------|---------------|
| 2025-12-27 | today |
| 2025-12-28 | tomorrow |
| 2025-12-29 | the day after tomorrow |
| 2025-01-03 | next Friday |
| 15:00 | three P M |
| 09:30 | nine thirty A M |

## Success Message Templates

### Task Creation
- Text: "✓ Task created successfully\n\nTask #{id}: {title}\nDue: {due_date}\nPriority: {priority}"
- Voice: "Task created. {title} is due {due_date} with {priority} priority."

### Task Update
- Text: "✓ Task updated\n\nTask #{id}: {title}\nUpdated: {fields_changed}"
- Voice: "Task updated. {fields_changed_summary}"

### Task Completion
- Text: "✓ Task completed\n\nTask #{id}: {title}\nCompleted at {time}"
- Voice: "{title} marked as complete"

### Task Deletion
- Text: "✓ Task deleted\n\nTask #{id}: {title}"
- Voice: "Task deleted"

### Task List (Empty)
- Text: "No tasks found matching your filters.\n\nTry adjusting your search or create a new task."
- Voice: "You have no matching tasks"

### Task List (Results)
- Text: "Found {count} task(s)\n\n1. [#{id}] {title} - Due: {due_date}\n2. ..."
- Voice: "You have {count} tasks. {first_task_title} is due {due_date}. {second_task_title} is due {due_date}. And {remaining_count} others."

## Testing Requirements

### Unit Tests

1. Success message formatting for each operation type
2. Error message humanization for all error codes
3. Modality-specific formatting (text vs voice)
4. Date/time formatting (today, tomorrow, past, future)
5. List formatting (0 tasks, 1 task, many tasks)
6. Empty state messages

### Integration Tests

1. End-to-end formatting of task creation success
2. End-to-end formatting of validation errors
3. Task list with various filter results
4. Multi-error aggregation and formatting

### Edge Cases

1. No tasks found → empty state message
2. Task with no due date → "No due date set"
3. Task with no description → omit description from output
4. Very long task list (100+ tasks) → pagination message
5. Multiple errors (5+) → group by category

## State Management

### Stateless Formatting

```python
# Conceptual example
class ResponseFormatterAgent:
    def format_response(self, input_data):
        modality = input_data["modality"]
        success = input_data["success"]

        if success:
            formatted = self.format_success(
                input_data["operation"],
                input_data["result"],
                modality
            )
        else:
            formatted = self.format_error(
                input_data["errors"],
                modality
            )

        return {
            "formatted_response": formatted,
            "metadata": {
                "response_type": "success" if success else "error"
            }
        }

    # No state retained across requests
```

### Prohibited State

- **NO user preferences**: Don't remember if user prefers concise responses
- **NO formatting history**: Every response formatted independently
- **NO learned patterns**: No ML-based style adaptation
- **NO caching**: Every response generated fresh

## Failure Modes

| Failure Scenario | Detection | Response | User Impact |
|------------------|-----------|----------|-------------|
| Missing result data | result = null but success = true | Return generic success | User sees confirmation but missing details |
| Unknown error code | Error code not in mapping | Use generic error message | User sees "An error occurred" |
| Invalid modality | modality not in [text, voice, image] | Default to text | Response formatted as text |

## Dependencies

### Required Components

None - Response Formatter is self-contained presentational logic.

## Versioning and Evolution

### Phase 1 (CLI)
- Text-only formatting
- Simple success/error messages
- Basic list formatting

### Phase 2-3 (Web + Voice)
- Voice-specific formatting
- Richer text formatting (Markdown)
- Adaptive verbosity

### Phase 4 (AI Chatbot)
- Conversational responses
- Context-aware tone
- Follow-up suggestions

### Phase 5 (Multimodal)
- Image overlay formatting
- Visual confirmation indicators
- Cross-modal consistency

## Acceptance Criteria

A Response Formatter Agent implementation is considered compliant if:

1. ✅ Formats all success responses clearly and consistently
2. ✅ Humanizes all error codes with actionable messages
3. ✅ Adapts formatting to modality (text vs voice)
4. ✅ Handles empty states gracefully
5. ✅ Formats dates in user-friendly format
6. ✅ Never modifies input data
7. ✅ Maintains consistent tone across all responses
8. ✅ Passes all unit and integration tests
