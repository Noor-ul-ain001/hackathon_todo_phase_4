# Agent Specification: Interface Orchestrator

**Agent Name**: Interface Orchestrator Agent
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The Interface Orchestrator Agent serves as the first point of contact for all user inputs regardless of modality (text, voice, image). It determines the input modality, invokes appropriate normalization logic, and produces a unified intent structure that the main Orchestrator Agent can process.

## Responsibilities

### Primary Responsibilities

1. **Modality Detection**: Identify whether input is text, voice, or image
2. **Intent Normalization**: Convert modality-specific input to standardized intent format
3. **Skill Invocation**: Call `ui_intent_normalization` skill for each modality
4. **Context Extraction**: Extract user_id, conversation_id, and metadata
5. **Quality Assurance**: Ensure normalized intent meets structural requirements

### Secondary Responsibilities

1. **Error Handling**: Catch malformed inputs before processing
2. **Metadata Preservation**: Retain modality info for response formatting
3. **Conversation Tracking**: Associate requests with conversation threads
4. **Request Logging**: Log raw inputs for debugging (without sensitive data)

## Allowed Actions

### Modality Detection
- Examine input structure to identify type
- Detect CLI command syntax vs natural language
- Identify voice transcription markers
- Recognize base64 image data
- Determine if multi-modal (text + image)

### Intent Normalization
- Invoke `ui_intent_normalization` skill
- Parse CLI commands (e.g., "todo add 'Task title'")
- Convert natural language to structured intent
- Extract action keywords (add, update, list, complete, delete)
- Extract parameters (title, due date, filters, etc.)

### Context Extraction
- Extract user_id from JWT or CLI context
- Extract conversation_id if present
- Generate request_id for tracking
- Capture timestamp
- Identify client type (CLI, web, mobile, etc.)

## Skills Used

### Primary Skill

**ui_intent_normalization**
- When: For every user input
- Input: { raw_input, modality, user_id }
- Output: { action, parameters, confidence }

Example invocations:

```json
// CLI command
ui_intent_normalization({
  "raw_input": "todo add 'Review spec' --due tomorrow",
  "modality": "text",
  "input_type": "command"
})
→ {
  "action": "create_task",
  "parameters": {
    "title": "Review spec",
    "due_date": "2025-12-28"
  },
  "confidence": 1.0
}

// Natural language
ui_intent_normalization({
  "raw_input": "Add meeting tomorrow at 3pm",
  "modality": "text",
  "input_type": "natural_language"
})
→ {
  "action": "create_task",
  "parameters": {
    "title": "meeting",
    "due_date": "2025-12-28",
    "due_time": "15:00"
  },
  "confidence": 0.85
}

// Voice input
ui_intent_normalization({
  "raw_input": "Show me my tasks for this week",
  "modality": "voice",
  "input_type": "natural_language"
})
→ {
  "action": "list_tasks",
  "parameters": {
    "due_after": "2025-12-27",
    "due_before": "2026-01-02"
  },
  "confidence": 0.90
}

// Image input (Phase 5)
ui_intent_normalization({
  "raw_input": "<base64_image_data>",
  "modality": "image",
  "input_type": "image_with_text"
})
→ {
  "action": "create_task",
  "parameters": {
    "title": "Quarterly review meeting",  // extracted from image
    "due_date": "2025-12-30"  // extracted from image
  },
  "confidence": 0.75
}
```

## Disallowed Behavior

### Absolutely Prohibited

1. **Business Logic**: NO task-specific logic (no understanding of what tasks mean)
2. **Validation**: NO input validation (delegate to Validation Agent)
3. **Task Operations**: NO skill invocations other than ui_intent_normalization
4. **Response Formatting**: NO user-facing messages
5. **Authentication**: NO JWT validation (handled by API layer)

### Specific Restrictions

- **NO direct MCP tool calls**: Only invoke ui_intent_normalization skill
- **NO intent interpretation**: Don't decide what user "really" means
- **NO ambiguity resolution**: Pass ambiguous requests through; let Task Reasoning Agent handle
- **NO data enrichment**: Don't add defaults or infer missing data
- **NO state storage**: Process each input independently

## Input Specification

### Expected Input Formats

#### CLI Command Input
```json
{
  "raw_input": "todo add 'Review architecture spec' --due 2025-12-28 --priority high",
  "user_id": "user_123",
  "client_type": "cli",
  "context": {
    "timestamp": "2025-12-27T10:30:00Z"
  }
}
```

#### Web Chat Input
```json
{
  "raw_input": "Add meeting with client tomorrow afternoon",
  "user_id": "user_456",
  "client_type": "web",
  "conversation_id": "conv_789",
  "context": {
    "timestamp": "2025-12-27T11:00:00Z"
  }
}
```

#### Voice Input
```json
{
  "raw_input": "Mark task number forty two as complete",
  "user_id": "user_789",
  "client_type": "mobile_app",
  "modality": "voice",
  "context": {
    "timestamp": "2025-12-27T12:00:00Z",
    "voice_metadata": {
      "confidence": 0.92,
      "language": "en-US"
    }
  }
}
```

#### Image Input (Phase 5)
```json
{
  "raw_input": "<base64_encoded_image>",
  "user_id": "user_abc",
  "client_type": "mobile_app",
  "modality": "image",
  "context": {
    "timestamp": "2025-12-27T13:00:00Z",
    "image_metadata": {
      "format": "png",
      "size_bytes": 245678
    }
  }
}
```

## Output Specification

### Expected Output Format

```json
{
  "user_id": "string (required)",
  "intent": {
    "action": "create_task|update_task|list_tasks|complete_task|delete_task",
    "parameters": {
      // Action-specific parameters extracted from input
    },
    "modality": "text|voice|image",
    "confidence": 0.0-1.0  // from ui_intent_normalization skill
  },
  "context": {
    "timestamp": "ISO 8601 string",
    "request_id": "string (generated UUID)",
    "conversation_id": "string (if applicable)",
    "client_type": "cli|web|mobile_app"
  },
  "metadata": {
    "raw_input_length": "number",
    "normalization_time_ms": "number"
  }
}
```

### Example Outputs

#### CLI Command Normalized
```json
{
  "user_id": "user_123",
  "intent": {
    "action": "create_task",
    "parameters": {
      "title": "Review architecture spec",
      "due_date": "2025-12-28",
      "priority": "high"
    },
    "modality": "text",
    "confidence": 1.0
  },
  "context": {
    "timestamp": "2025-12-27T10:30:00Z",
    "request_id": "req_abc123",
    "client_type": "cli"
  },
  "metadata": {
    "raw_input_length": 65,
    "normalization_time_ms": 15
  }
}
```

#### Natural Language Normalized
```json
{
  "user_id": "user_456",
  "intent": {
    "action": "create_task",
    "parameters": {
      "title": "meeting with client",
      "due_date": "2025-12-28",
      "due_time": "14:00"  // "afternoon" → 2pm default
    },
    "modality": "text",
    "confidence": 0.85
  },
  "context": {
    "timestamp": "2025-12-27T11:00:00Z",
    "request_id": "req_def456",
    "conversation_id": "conv_789",
    "client_type": "web"
  },
  "metadata": {
    "raw_input_length": 45,
    "normalization_time_ms": 120
  }
}
```

## Modality Detection Logic

### Text Detection

```
If input matches CLI command pattern:
  → modality = "text"
  → input_type = "command"
  → Use command parser

If input is natural language:
  → modality = "text"
  → input_type = "natural_language"
  → Use NL parser
```

### Voice Detection

```
If input has voice_metadata:
  → modality = "voice"
  → input_type = "natural_language"
  → Already transcribed to text by STT service

If input contains audio data (future):
  → modality = "voice"
  → Invoke STT service first
  → Then normalize transcribed text
```

### Image Detection

```
If input is base64 encoded image:
  → modality = "image"
  → input_type = "image_with_text"
  → Invoke Visual Context Agent first
  → Then normalize extracted text
```

## Execution Flow

### Standard Flow

```
1. Receive raw user input
   ↓
2. Extract user_id and context
   ↓
3. Detect modality (text/voice/image)
   ↓
4. If modality = image:
      → Delegate to Visual Context Agent first
      → Receive extracted text/data
      → Proceed with normalized text
   ↓
5. Invoke ui_intent_normalization skill:
      Input: { raw_input, modality, input_type }
      Output: { action, parameters, confidence }
   ↓
6. Construct normalized intent:
      {
        user_id,
        intent: { action, parameters, modality, confidence },
        context: { timestamp, request_id, conversation_id },
        metadata: { ... }
      }
   ↓
7. If confidence < 0.5:
      → Flag for disambiguation
      → Still pass to Orchestrator (let Task Reasoning handle)
   ↓
8. Return normalized intent to main Orchestrator Agent
```

### CLI Command Parsing Example

```
Input: "todo add 'Review spec' --due tomorrow --priority high"

Parsing steps:
1. Identify command: "add"
2. Extract quoted title: "Review spec"
3. Parse flags:
   - --due tomorrow → due_date: "2025-12-28"
   - --priority high → priority: "high"
4. Map command to action: add → create_task
5. Construct parameters:
   {
     "title": "Review spec",
     "due_date": "2025-12-28",
     "priority": "high"
   }
6. Confidence: 1.0 (explicit command)
```

### Natural Language Parsing Example

```
Input: "Show my urgent tasks due this week"

Parsing steps:
1. Identify intent: "show" → list_tasks
2. Extract filters:
   - "urgent" → priority: "high"
   - "due this week" → due_after: "2025-12-27", due_before: "2026-01-02"
3. Construct parameters:
   {
     "priority": "high",
     "due_after": "2025-12-27",
     "due_before": "2026-01-02"
   }
4. Confidence: 0.90 (high confidence NLP match)
```

## Error Handling

### Error Categories

1. **Malformed Input**: Empty string, null, invalid encoding
2. **Missing user_id**: No user context available
3. **Unsupported Modality**: Unknown input type
4. **Normalization Failure**: ui_intent_normalization skill fails
5. **Low Confidence**: Skill returns confidence < 0.5

### Error Response Strategy

```
If input is malformed:
  → Return error: "Invalid input format"
  → Do NOT attempt normalization

If user_id missing:
  → Return error: "User authentication required"
  → Do NOT process request

If normalization fails:
  → Return skill error with details
  → Suggest user rephrase

If confidence < 0.5:
  → Still return normalized intent
  → Flag for disambiguation
  → Let Task Reasoning Agent handle clarification
```

## State Management

### Stateless Processing

```python
# Conceptual example
class InterfaceOrchestratorAgent:
    def normalize_input(self, raw_input):
        # Detect modality
        modality = self.detect_modality(raw_input)

        # Invoke normalization skill
        normalized = self.invoke_skill(
            skill_name="ui_intent_normalization",
            parameters={
                "raw_input": raw_input.text,
                "modality": modality,
                "input_type": self.detect_input_type(raw_input)
            }
        )

        # Construct intent
        intent = {
            "user_id": raw_input.user_id,
            "intent": {
                "action": normalized["action"],
                "parameters": normalized["parameters"],
                "modality": modality,
                "confidence": normalized["confidence"]
            },
            "context": {
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": str(uuid.uuid4()),
                "conversation_id": raw_input.conversation_id
            }
        }

        return intent

    # No state retained
```

### Prohibited State

- **NO conversation memory**: Each input processed independently
- **NO user preferences**: Don't remember preferred input style
- **NO command history**: No autocomplete or suggestions
- **NO caching**: Every input normalized fresh

## Testing Requirements

### Unit Tests

1. CLI command parsing (add, update, list, complete, delete)
2. Natural language intent extraction
3. Modality detection (text vs voice vs image markers)
4. user_id extraction from context
5. request_id generation (unique per request)
6. Confidence scoring interpretation

### Integration Tests

1. End-to-end CLI command normalization
2. End-to-end natural language normalization
3. Voice input normalization (with transcription)
4. Image input normalization (with Visual Context Agent)
5. Multi-modal input handling

### Edge Cases

1. Empty input → error
2. Input with no recognizable action → low confidence, still normalize
3. Very long input (1000+ characters) → truncate and normalize
4. Input with multiple conflicting parameters → normalize best effort
5. Unknown flags in CLI command → ignore unknown, process known

## Failure Modes

| Failure Scenario | Detection | Response | User Impact |
|------------------|-----------|----------|-------------|
| Empty or null input | Input validation | Return error: "No input provided" | Request rejected |
| Missing user_id | Context check | Return error: "User not authenticated" | Request rejected |
| Normalization skill fails | Skill returns error | Propagate error with suggestion to rephrase | Request rejected |
| Low confidence (<0.5) | Check confidence score | Flag for disambiguation, still process | May require clarification |
| Unsupported modality | Modality detection | Return error: "Unsupported input type" | Request rejected |

## Dependencies

### Required Components

- **ui_intent_normalization skill**: For converting inputs to structured intents
- **Visual Context Agent**: For image input processing (Phase 5)

### Optional Components

- **STT Service**: For voice-to-text conversion (if not pre-transcribed)
- **Command Parser Library**: For CLI syntax parsing
- **NLP Library**: For natural language understanding

## Versioning and Evolution

### Phase 1 (CLI)
- CLI command parsing only
- Structured --flag syntax
- Simple intent mapping

### Phase 2-3 (Web + Voice)
- Natural language parsing
- Voice input (pre-transcribed text)
- Conversational syntax

### Phase 4 (AI Chatbot)
- Advanced NLU with context
- Multi-turn conversation normalization
- Intent disambiguation integration

### Phase 5 (Multimodal)
- Image input processing
- Visual Context Agent integration
- Cross-modal intent fusion

## Acceptance Criteria

An Interface Orchestrator Agent implementation is considered compliant if:

1. ✅ Detects modality correctly for all input types
2. ✅ Normalizes CLI commands to structured intents
3. ✅ Normalizes natural language to structured intents
4. ✅ Invokes ui_intent_normalization skill correctly
5. ✅ Generates unique request_id for each request
6. ✅ Preserves user_id and context throughout
7. ✅ Returns consistent intent structure
8. ✅ Passes all unit and integration tests
