# Agent Specification: Orchestrator

**Agent Name**: Orchestrator Agent
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The Orchestrator Agent serves as the primary entry point for all normalized user intents. It coordinates the execution of multi-agent workflows, routes intents to appropriate specialized agents, and ensures consistent request processing across all modalities.

## Responsibilities

### Primary Responsibilities

1. **Intent Routing**: Receive normalized intents and route to appropriate specialized agents
2. **Agent Coordination**: Orchestrate multi-agent workflows when multiple agents needed
3. **Execution Sequencing**: Ensure agents execute in correct order with proper dependencies
4. **Error Aggregation**: Collect errors from sub-agents and coordinate error responses
5. **Result Assembly**: Combine results from multiple agents into cohesive outcomes

### Secondary Responsibilities

1. **Validation Trigger**: Invoke Validation Agent before destructive operations
2. **Context Passing**: Pass user_id and intent parameters to all sub-agents
3. **Workflow State**: Track which agents have completed (within single request only)
4. **Fallback Handling**: Provide default responses when agents unavailable

## Allowed Actions

### Intent Analysis
- Parse intent object structure
- Extract action type (create, update, list, delete, complete)
- Identify required parameters
- Determine which agents needed

### Agent Invocation
- Call Task Reasoning Agent for task-related logic
- Call Validation Agent for input validation and safety checks
- Call Visual Context Agent for image-based intents
- Call Response Formatter Agent for output formatting
- Pass complete intent context to each agent

### Workflow Coordination
- Execute agents sequentially when dependencies exist
- Execute agents in parallel when independent (implementation-specific)
- Collect and merge results from multiple agents
- Handle partial failures gracefully

### Error Handling
- Catch errors from any sub-agent
- Determine if workflow can continue or must abort
- Coordinate error responses with Response Formatter
- Log errors for debugging (without exposing to user)

## Skills Used

The Orchestrator Agent does NOT directly invoke skills. It delegates skill invocation to specialized agents:

- **Task Reasoning Agent** → invokes task management skills
- **Validation Agent** → invokes validation-related logic
- **Visual Context Agent** → invokes image processing skills
- **Response Formatter Agent** → formats outputs (no skill invocation)

The Orchestrator's role is coordination, not execution.

## Disallowed Behavior

### Absolutely Prohibited

1. **Direct Skill Invocation**: NEVER call skills directly; always via specialized agents
2. **Business Logic**: NO task-specific logic (due dates, priorities, status changes)
3. **Data Access**: NO direct MCP tool calls; only via sub-agents
4. **State Storage**: NO persistent state across requests
5. **User Authentication**: NO JWT validation (handled by API layer)
6. **Response Formatting**: NO direct response formatting (delegate to Response Formatter Agent)

### Specific Restrictions

- **NO hardcoded routing rules**: Routing logic based on intent structure, not hardcoded actions
- **NO assumption of success**: Always check sub-agent return values
- **NO user data manipulation**: Only pass data between agents
- **NO caching**: Every request processed fresh from intent
- **NO session memory**: Each request is independent

## Input Specification

### Expected Input Format

```json
{
  "user_id": "string (required)",
  "intent": {
    "action": "string (required: create_task|update_task|list_tasks|complete_task|delete_task)",
    "parameters": {
      // Action-specific parameters
    },
    "modality": "string (required: text|voice|image)",
    "conversation_id": "string (optional, for chat-based interactions)"
  },
  "context": {
    "timestamp": "ISO 8601 string",
    "request_id": "string (for logging)"
  }
}
```

### Example Inputs

#### Create Task Intent
```json
{
  "user_id": "user_123",
  "intent": {
    "action": "create_task",
    "parameters": {
      "title": "Review architecture spec",
      "description": "Complete review by EOD",
      "due_date": "2025-12-28"
    },
    "modality": "text"
  },
  "context": {
    "timestamp": "2025-12-27T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

#### List Tasks Intent
```json
{
  "user_id": "user_456",
  "intent": {
    "action": "list_tasks",
    "parameters": {
      "status": "pending",
      "limit": 10
    },
    "modality": "voice"
  },
  "context": {
    "timestamp": "2025-12-27T11:00:00Z",
    "request_id": "req_def456"
  }
}
```

## Output Specification

### Expected Output Format

```json
{
  "success": "boolean",
  "result": {
    // Action-specific result data
  },
  "errors": [
    {
      "code": "string",
      "message": "string",
      "field": "string (optional)"
    }
  ],
  "metadata": {
    "agents_invoked": ["agent_name_1", "agent_name_2"],
    "execution_time_ms": "number",
    "request_id": "string"
  }
}
```

### Example Outputs

#### Successful Task Creation
```json
{
  "success": true,
  "result": {
    "task_id": 42,
    "title": "Review architecture spec",
    "status": "pending",
    "created_at": "2025-12-27T10:30:05Z"
  },
  "errors": [],
  "metadata": {
    "agents_invoked": ["TaskReasoningAgent", "ValidationAgent", "ResponseFormatterAgent"],
    "execution_time_ms": 250,
    "request_id": "req_abc123"
  }
}
```

#### Validation Error
```json
{
  "success": false,
  "result": null,
  "errors": [
    {
      "code": "INVALID_DATE",
      "message": "Due date cannot be in the past",
      "field": "due_date"
    }
  ],
  "metadata": {
    "agents_invoked": ["TaskReasoningAgent", "ValidationAgent"],
    "execution_time_ms": 120,
    "request_id": "req_xyz789"
  }
}
```

## Execution Flow

### Standard Request Flow

```
1. Receive normalized intent
   ↓
2. Validate intent structure (action, parameters present)
   ↓
3. Determine required agents based on action
   ↓
4. Invoke specialized agents in sequence:
   a. Task Reasoning Agent (for task logic)
   b. Validation Agent (for safety checks)
   c. Visual Context Agent (if modality = image)
   ↓
5. Collect results from all agents
   ↓
6. If any agent failed with blocking error:
      → Abort workflow
      → Invoke Response Formatter with error
      → Return error response
   ↓
7. If all agents succeeded:
      → Merge results
      → Invoke Response Formatter with success
      → Return success response
   ↓
8. Terminate (no state retained)
```

### Multi-Agent Coordination Example

User intent: "Add meeting tomorrow with image attachment"

```
Orchestrator receives intent:
{
  "action": "create_task",
  "parameters": {
    "title": "meeting",
    "due_date": "2025-12-28",
    "image_data": "<base64>"
  },
  "modality": "image"
}

Execution sequence:
1. Invoke Visual Context Agent
   Input: image_data
   Output: { "extracted_text": "Quarterly review meeting", "confidence": 0.95 }

2. Invoke Task Reasoning Agent
   Input: { "title": "meeting", "extracted_text": "Quarterly review meeting" }
   Output: { "enriched_title": "Quarterly review meeting", "suggested_priority": "high" }

3. Invoke Validation Agent
   Input: { "title": "Quarterly review meeting", "due_date": "2025-12-28" }
   Output: { "valid": true, "warnings": [] }

4. Task Reasoning Agent invokes task_creation skill
   Result: { "task_id": 42, "status": "created" }

5. Invoke Response Formatter Agent
   Input: { "task_id": 42, "title": "Quarterly review meeting", "modality": "image" }
   Output: "Task created: Quarterly review meeting (Task #42)"

6. Return formatted response to user
```

## Error Handling

### Error Categories

1. **Intent Structure Errors**: Missing required fields (action, user_id)
2. **Agent Invocation Errors**: Sub-agent unavailable or crashed
3. **Validation Errors**: Validation Agent rejected input
4. **Execution Errors**: Skill or MCP tool failure
5. **Unknown Errors**: Unexpected exceptions

### Error Response Strategy

```
If error is recoverable:
  → Retry with fallback logic
  → Return partial success if applicable

If error is blocking:
  → Abort workflow immediately
  → Return structured error to user
  → Do NOT expose internal details

If error is unknown:
  → Log full details internally
  → Return generic error to user
  → Include request_id for support
```

## State Management

### Request-Scoped State Only

The Orchestrator maintains state ONLY within a single request execution:

```python
# Conceptual example (implementation-agnostic)
class OrchestratorAgent:
    def process_intent(self, intent):
        # State exists only during this function execution
        workflow_state = {
            "agents_invoked": [],
            "results": [],
            "errors": []
        }

        # Execute agents...
        # Update workflow_state...

        # Return final result
        return self.format_response(workflow_state)

    # After return, workflow_state is garbage collected
    # Next request starts fresh
```

### Prohibited State

- **NO session storage**: No user-specific state across requests
- **NO caching**: No cached agent results
- **NO request history**: No memory of previous requests
- **NO user preferences**: Preferences loaded from database per request

## Testing Requirements

### Unit Tests

1. Intent routing to correct agents
2. Error aggregation from multiple agents
3. Partial failure handling
4. Invalid intent structure rejection
5. Agent coordination sequencing

### Integration Tests

1. End-to-end task creation via multiple agents
2. Multi-agent workflows (e.g., image + task creation)
3. Error propagation from sub-agents
4. Response formatting coordination

### Edge Cases

1. All agents fail → coherent error response
2. Missing user_id → request rejected
3. Unknown action → appropriate error
4. Agent timeout → fallback behavior
5. Empty parameters → validation error

## Failure Modes

| Failure Scenario | Detection | Response | User Impact |
|------------------|-----------|----------|-------------|
| Invalid intent structure | Intent parsing | Return error: "Invalid request format" | Request rejected, retry with valid format |
| Sub-agent unavailable | Agent invocation fails | Return error: "Service temporarily unavailable" | Request fails, retry later |
| Validation Agent rejects input | validation_result.valid = false | Return validation errors | Request rejected with specific field errors |
| Task Reasoning Agent error | Exception caught | Return error: "Unable to process request" | Request fails, retry or contact support |
| All agents succeed but MCP fails | Skill returns error | Return error: "Operation failed" | Request fails, retry |

## Monitoring and Observability

### Metrics to Track

1. **Request throughput**: Requests/second processed
2. **Agent invocation counts**: Which agents used most frequently
3. **Error rates**: Percentage of failed workflows
4. **Execution time**: p50, p95, p99 latency
5. **Agent coordination patterns**: Common multi-agent sequences

### Logging Requirements

Log at INFO level:
- Request received (user_id, action, request_id)
- Agents invoked (agent names, sequence)
- Workflow completed (success/failure, duration)

Log at ERROR level:
- Agent invocation failures
- Unexpected exceptions
- Validation failures (if frequent)

Do NOT log:
- User task data (titles, descriptions)
- JWT tokens
- Internal agent communication details

## Dependencies

### Required Components

- **Task Reasoning Agent**: For task-specific logic
- **Validation Agent**: For input validation
- **Response Formatter Agent**: For output formatting
- **Visual Context Agent**: For image-based intents (Phase 5)

### Optional Components

- **Intent Disambiguation Skill**: For ambiguous requests (via Task Reasoning Agent)

## Versioning and Evolution

### Phase 1 (CLI)
- Basic intent routing
- Single-agent workflows (Task Reasoning → Validation → Response)

### Phase 2-3 (Web + Voice)
- Multi-user support (user_id routing)
- Conversation context handling

### Phase 4 (AI Chatbot)
- Intent disambiguation coordination
- Multi-turn conversation orchestration

### Phase 5 (Multimodal)
- Visual Context Agent integration
- Cross-modal result merging

## Acceptance Criteria

An Orchestrator Agent implementation is considered compliant if:

1. ✅ Routes all valid intents to appropriate agents
2. ✅ Coordinates multi-agent workflows without state retention
3. ✅ Returns structured responses in expected format
4. ✅ Handles all error categories gracefully
5. ✅ Never invokes skills directly
6. ✅ Never stores state across requests
7. ✅ Passes all unit and integration tests
8. ✅ Logs requests without exposing sensitive data
