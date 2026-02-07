# Skill Specification: Intent Disambiguation

**Skill Name**: intent_disambiguation
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The intent_disambiguation skill resolves ambiguous user requests by generating clarification questions with options for the user to choose from.

## Responsibilities

1. Accept ambiguous request details from agents
2. Analyze the ambiguity (multiple possible interpretations)
3. Generate clarification question
4. Provide options for user to select
5. Return structured clarification to agent

## Inputs

### Input Schema

```json
{
  "user_id": "string (required)",
  "user_input": "string (required, the ambiguous request)",
  "ambiguity_type": "string (required, enum: multiple_matches|unclear_action|missing_parameters)",
  "context": {
    "possible_matches": [
      {
        "task_id": "number",
        "title": "string"
      }
    ],
    "possible_actions": ["string"],
    "missing_params": ["string"]
  }
}
```

### Input Examples

**Multiple Matching Tasks**:
```json
{
  "user_id": "user_123",
  "user_input": "Update the review task",
  "ambiguity_type": "multiple_matches",
  "context": {
    "possible_matches": [
      {"task_id": 10, "title": "Review architecture spec"},
      {"task_id": 15, "title": "Review design document"},
      {"task_id": 20, "title": "Code review for PR #42"}
    ]
  }
}
```

**Unclear Action**:
```json
{
  "user_id": "user_456",
  "user_input": "Do something with task 42",
  "ambiguity_type": "unclear_action",
  "context": {
    "possible_actions": ["update", "complete", "delete"]
  }
}
```

## Outputs

### Output Schema

```json
{
  "success": "boolean",
  "clarification": {
    "question": "string (the clarification question)",
    "options": [
      {
        "option_id": "string",
        "label": "string (display text)",
        "value": "any (the value to use if selected)"
      }
    ],
    "context": "object (original context for follow-up)"
  },
  "error": null | object
}
```

### Output Example

```json
{
  "success": true,
  "clarification": {
    "question": "Which task did you want to update?",
    "options": [
      {
        "option_id": "A",
        "label": "Review architecture spec (Task #10)",
        "value": {"task_id": 10, "title": "Review architecture spec"}
      },
      {
        "option_id": "B",
        "label": "Review design document (Task #15)",
        "value": {"task_id": 15, "title": "Review design document"}
      },
      {
        "option_id": "C",
        "label": "Code review for PR #42 (Task #20)",
        "value": {"task_id": 20, "title": "Code review for PR #42"}
      }
    ],
    "context": {
      "user_input": "Update the review task",
      "action": "update"
    }
  },
  "error": null
}
```

## Triggers

### Text Modality
- User: "Update the review task" (multiple reviews exist)
- User: "Do something with task 42" (action unclear)

### Voice Modality
- User: "Mark the meeting as done" (multiple meetings exist)

### Image Modality
- Not typically used for disambiguation (ambiguity resolved before image processing)

## Execution Flow

```
1. Receive ambiguous request details
2. Analyze ambiguity type
3. Generate appropriate clarification question:
   - Multiple matches → "Which task did you mean?"
   - Unclear action → "What would you like to do?"
   - Missing params → "Please provide [missing field]"
4. Format options for user selection
5. Return clarification object to agent
6. Agent presents to user
7. User selects option
8. Agent processes with resolved intent
```

## Clarification Strategies

### Multiple Matches
- Question: "Which [entity] did you mean?"
- Options: List all matching entities with identifying details
- Max options: 5 (if more, ask user to be more specific)

### Unclear Action
- Question: "What would you like to do with [entity]?"
- Options: List possible actions (update, complete, delete, etc.)

### Missing Parameters
- Question: "Please provide [missing field]"
- Options: Suggestions if possible, or free-form input

## Error Handling

- No possible matches → Return "No matches found" error
- Too many matches (>10) → Ask user to be more specific
- Invalid ambiguity type → Return error

## Failure Modes

| Scenario | Response | Impact |
|----------|----------|--------|
| No matches found | Error: "No matches found" | Agent informs user no tasks match |
| Too many matches | Clarification with "Be more specific" | User refines query |
| User cancels | User can cancel clarification | Agent aborts operation |

## Acceptance Criteria

1. ✅ Generates clear clarification questions
2. ✅ Provides selectable options
3. ✅ Handles multiple match types
4. ✅ Limits options to reasonable number (≤5)
5. ✅ Returns context for follow-up processing
