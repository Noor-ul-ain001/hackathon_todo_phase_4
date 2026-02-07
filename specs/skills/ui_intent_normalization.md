# Skill Specification: UI Intent Normalization

**Skill Name**: ui_intent_normalization
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The ui_intent_normalization skill converts modality-specific user inputs (CLI commands, natural language, voice transcripts, image data) into a unified, structured intent format that agents can process consistently.

## Responsibilities

1. Accept raw input from any modality (text, voice, image)
2. Detect input type (command, natural language, voice, image)
3. Parse and extract action + parameters
4. Normalize to structured intent format
5. Return intent with confidence score

## Inputs

### Input Schema

```json
{
  "raw_input": "string | object (the user's input)",
  "modality": "string (required, enum: text|voice|image)",
  "input_type": "string (required, enum: command|natural_language|image_with_text)",
  "user_id": "string (required)",
  "context": {
    "conversation_id": "string (optional)",
    "previous_intent": "object (optional, for follow-up requests)"
  }
}
```

### Input Examples

**CLI Command**:
```json
{
  "raw_input": "todo add 'Review spec' --due tomorrow --priority high",
  "modality": "text",
  "input_type": "command",
  "user_id": "user_123"
}
```

**Natural Language (Text)**:
```json
{
  "raw_input": "Add meeting with client tomorrow at 3pm",
  "modality": "text",
  "input_type": "natural_language",
  "user_id": "user_456"
}
```

**Voice (Transcribed)**:
```json
{
  "raw_input": "Show me my tasks for this week",
  "modality": "voice",
  "input_type": "natural_language",
  "user_id": "user_789"
}
```

**Image (With Extracted Text)**:
```json
{
  "raw_input": {
    "extracted_text": "Quarterly Review Meeting\nDec 30, 2025 at 2:00 PM\nUrgent",
    "confidence": 0.92
  },
  "modality": "image",
  "input_type": "image_with_text",
  "user_id": "user_abc"
}
```

## Outputs

### Output Schema

```json
{
  "success": "boolean",
  "intent": {
    "action": "string (enum: create_task|update_task|list_tasks|complete_task|delete_task)",
    "parameters": {
      "title": "string (optional)",
      "description": "string (optional)",
      "due_date": "string (optional, ISO 8601)",
      "due_time": "string (optional, HH:MM)",
      "priority": "string (optional)",
      "status": "string (optional)",
      "task_id": "number (optional)",
      "filters": "object (optional, for list_tasks)",
      // ... action-specific parameters
    },
    "confidence": "number (0.0-1.0)",
    "modality": "string"
  },
  "error": null | object
}
```

### Output Examples

**CLI Command Normalized**:
```json
{
  "success": true,
  "intent": {
    "action": "create_task",
    "parameters": {
      "title": "Review spec",
      "due_date": "2025-12-28",
      "priority": "high"
    },
    "confidence": 1.0,
    "modality": "text"
  },
  "error": null
}
```

**Natural Language Normalized**:
```json
{
  "success": true,
  "intent": {
    "action": "create_task",
    "parameters": {
      "title": "meeting with client",
      "due_date": "2025-12-28",
      "due_time": "15:00"
    },
    "confidence": 0.85,
    "modality": "text"
  },
  "error": null
}
```

**Voice Normalized**:
```json
{
  "success": true,
  "intent": {
    "action": "list_tasks",
    "parameters": {
      "filters": {
        "due_after": "2025-12-27",
        "due_before": "2026-01-02"
      }
    },
    "confidence": 0.90,
    "modality": "voice"
  },
  "error": null
}
```

**Image Normalized**:
```json
{
  "success": true,
  "intent": {
    "action": "create_task",
    "parameters": {
      "title": "Quarterly Review Meeting",
      "due_date": "2025-12-30",
      "due_time": "14:00",
      "priority": "high"
    },
    "confidence": 0.75,
    "modality": "image"
  },
  "error": null
}
```

## Triggers

### Text Modality
- CLI commands: Structured syntax
- Natural language: Conversational requests

### Voice Modality
- Pre-transcribed text from STT service

### Image Modality
- Extracted text from Visual Context Agent

## Execution Flow

```
1. Receive raw input + modality + input_type
2. Route to appropriate parser:
   - command → CLI parser
   - natural_language (text/voice) → NLP parser
   - image_with_text → Image parser
3. Parser extracts:
   - Action (create, update, list, complete, delete)
   - Parameters (title, due_date, filters, etc.)
4. Calculate confidence score:
   - CLI commands: 1.0 (explicit)
   - Natural language: 0.7-0.95 (depends on clarity)
   - Image: 0.5-0.9 (depends on OCR quality)
5. Return normalized intent
```

## Parsing Logic

### CLI Command Parser

```
Pattern: "todo <action> <params>"

Actions:
- add → create_task
- list → list_tasks
- update → update_task
- complete/done → complete_task
- delete/remove → delete_task

Flags:
- --due <date> → due_date
- --priority <low|medium|high> → priority
- --status <status> → status
- --description <text> → description

Confidence: 1.0 (explicit commands)
```

### Natural Language Parser

```
Keywords for actions:
- create_task: "add", "create", "new task"
- list_tasks: "show", "list", "display", "what tasks"
- update_task: "update", "change", "modify", "set"
- complete_task: "complete", "done", "finish", "mark as done"
- delete_task: "delete", "remove", "cancel"

Date parsing:
- "tomorrow" → current_date + 1
- "next Monday" → next occurrence
- "in 3 days" → current_date + 3
- "2025-12-28" → literal date

Time parsing:
- "3pm" → 15:00
- "EOD" → 17:00
- "morning" → 09:00

Priority inference:
- "urgent", "ASAP" → high
- "when possible", "someday" → low
- (default) → medium

Confidence: 0.7-0.95 (based on clarity)
```

### Image Parser

```
Input: Extracted text from Visual Context Agent

1. Identify title (largest/topmost text)
2. Extract dates (look for date patterns)
3. Extract times (look for time patterns)
4. Detect priority keywords (URGENT, ASAP, etc.)
5. Extract description (body text)

Confidence: Based on OCR quality from Visual Context Agent (0.5-0.9)
```

## Confidence Scoring

| Input Type | Confidence Range | Rationale |
|------------|------------------|-----------|
| CLI command | 1.0 | Explicit, structured syntax |
| Natural language (clear) | 0.9-0.95 | High clarity, recognized patterns |
| Natural language (ambiguous) | 0.7-0.85 | Some ambiguity, reasonable interpretation |
| Voice (clear transcription) | 0.85-0.95 | Clear transcription, recognized patterns |
| Voice (unclear transcription) | 0.6-0.8 | Transcription uncertainty |
| Image (high quality) | 0.8-0.9 | Clear OCR, recognized patterns |
| Image (medium quality) | 0.6-0.75 | Some OCR errors, fuzzy patterns |
| Image (low quality) | 0.4-0.55 | Many OCR errors, low confidence |

**Threshold**: If confidence < 0.5, flag for disambiguation

## Error Handling

- Unrecognized command → Error: "Unknown command"
- Cannot extract action → Error: "Could not understand request"
- Empty input → Error: "No input provided"
- Invalid date format → Parse as null, proceed
- Low confidence (<0.5) → Flag for disambiguation

## Failure Modes

| Scenario | Response | Impact |
|----------|----------|--------|
| Completely unrecognizable input | Error: "Could not parse" | Agent asks user to rephrase |
| Very low confidence (<0.3) | Error: "Too ambiguous" | Agent requests clarification |
| Multiple valid interpretations | Success with lower confidence | Agent may invoke disambiguation |
| Image with no text | Error: "No text found in image" | Agent requests clearer image |

## State Management

**Stateless**: Each normalization is independent. No session memory, no cached patterns.

## Acceptance Criteria

1. ✅ Normalizes CLI commands correctly (confidence = 1.0)
2. ✅ Normalizes natural language (confidence 0.7-0.95)
3. ✅ Normalizes voice input (pre-transcribed)
4. ✅ Normalizes image-extracted text (confidence varies)
5. ✅ Returns consistent intent structure across all modalities
6. ✅ Calculates appropriate confidence scores
7. ✅ Flags low-confidence requests for disambiguation
8. ✅ Stateless operation
