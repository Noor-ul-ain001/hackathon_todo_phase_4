# Implementation Plan: AI Chatbot with MCP + Multimodal Interface

**Feature**: Todo Intelligence Platform - Phases 4 & 5
**Branch**: 001-todo-intelligence-platform
**Created**: 2025-12-27
**Status**: BLOCKED - Missing Prerequisite Specifications

---

## ⚠️ CRITICAL PREREQUISITES

**This plan CANNOT be executed until the following specifications are completed:**

### Missing Required Specifications

1. **specs/skills/** (7 skills required):
   - task_creation.md
   - task_listing.md
   - task_update.md
   - task_completion.md
   - task_deletion.md
   - intent_disambiguation.md
   - ui_intent_normalization.md

2. **specs/mcp/tools.md** (5 MCP tools required):
   - add_task
   - list_tasks
   - update_task
   - complete_task
   - delete_task

3. **specs/api/chat-endpoint.md**:
   - POST /api/{user_id}/chat specification

4. **specs/database/schema.md**:
   - users, tasks, conversations, messages tables

5. **specs/ui/** (3 UI specs required):
   - chat.md
   - voice.md
   - image-interface.md

### Action Required

**Before proceeding with this plan:**
1. Run `/sp.specify` to complete all missing specifications
2. Return to this plan after specifications are approved
3. Verify all specs comply with constitution

---

## PHASE OVERVIEW

### High-Level Goal

Implement a conversational AI chatbot with full multimodal support (text, voice, image) that:
- Understands natural language task management commands
- Processes voice inputs via speech-to-text
- Extracts task information from images
- Maintains stateless conversation state in database
- Routes all data operations through MCP tools
- Provides consistent user experience across all modalities

### Key Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Missing skill specifications | BLOCKER | Complete `/sp.specify` first |
| Stateless conversation management complexity | HIGH | Strict adherence to architecture.md patterns |
| Multi-agent coordination bugs | HIGH | Comprehensive integration testing per stage |
| MCP tool isolation failures | CRITICAL | Security validation at each layer |
| Image processing quality issues | MEDIUM | Quality thresholds in Visual Context Agent |
| Voice transcription accuracy | MEDIUM | Confidence scoring and clarification flow |
| Cross-modality intent consistency | HIGH | Rigorous ui_intent_normalization testing |

### Success Criteria

**Technical:**
- [ ] All agents deployed and coordinating correctly
- [ ] All MCP tools functional with user isolation
- [ ] Stateless request cycle verified (no session state)
- [ ] Conversation persistence working (survives restarts)
- [ ] All three modalities (text/voice/image) operational

**Functional:**
- [ ] Users can create tasks via natural language
- [ ] Users can create tasks via voice commands
- [ ] Users can create tasks from images
- [ ] All modalities produce equivalent results
- [ ] Conversation context maintained across requests

**Quality:**
- [ ] >90% intent recognition accuracy for text
- [ ] >85% intent recognition accuracy for voice
- [ ] >75% data extraction accuracy from images
- [ ] <2 second response time for text/voice
- [ ] <5 second response time for image processing

---

## AGENT RESPONSIBILITY MAP

### Orchestrator Agent
**Responsibilities:**
- Route all incoming intents to specialized agents
- Coordinate multi-agent workflows
- Aggregate results from sub-agents
- Pass control to Response Formatter

**Skills Used:** None (delegates to specialized agents)

### Interface Orchestrator Agent
**Responsibilities:**
- Detect input modality (text/voice/image)
- Normalize all inputs to structured intents
- Extract user_id and conversation context

**Skills Used:**
- ui_intent_normalization (for all modalities)

### Task Reasoning Agent
**Responsibilities:**
- Parse natural language for task operations
- Extract task parameters (title, description, dates, priority)
- Handle date/time parsing (relative and absolute)
- Invoke appropriate task management skills

**Skills Used:**
- task_creation
- task_update
- task_listing
- task_completion
- task_deletion
- intent_disambiguation

### Validation & Safety Agent
**Responsibilities:**
- Validate all input parameters
- Enforce business rules (date ranges, string lengths)
- Check user authorization
- Sanitize inputs for security

**Skills Used:** None (pure validation logic)

### Visual Context Agent (Phase 5)
**Responsibilities:**
- Extract text from images via OCR
- Parse dates, priorities, and task info from extracted text
- Assess image quality
- Structure visual data for task creation

**Skills Used:** None (uses OCR/Vision APIs)

### Response Formatter Agent
**Responsibilities:**
- Convert technical results to user-friendly messages
- Adapt responses to modality (concise for voice, detailed for text)
- Humanize error messages
- Format success confirmations

**Skills Used:** None (pure formatting logic)

---

## EXECUTION STAGES

### Stage 0: Specification Completion & Validation

**Purpose:** Ensure all prerequisite specifications exist and are consistent

**Prerequisites:** None

**Input Specs Referenced:**
- constitution.md
- overview.md
- architecture.md
- agents/*.md (all 6 agents)

**Tasks:**

1. **Complete Missing Specifications**
   - Action: Run `/sp.specify` to generate:
     - skills/*.md (7 files)
     - mcp/tools.md
     - api/chat-endpoint.md
     - database/schema.md
     - ui/*.md (3 files)
   - Validation: All spec files exist and follow template structure

2. **Cross-Spec Consistency Check**
   - Verify agent specs reference correct skills
   - Verify skill specs define correct MCP tool invocations
   - Verify API spec matches architecture.md patterns
   - Verify database schema includes all required tables from constitution
   - Validation: No contradictions between specs

3. **Constitution Compliance Audit**
   - Verify stateless architecture preserved
   - Verify MCP-first rule followed
   - Verify agentic development pattern maintained
   - Verify multi-user isolation enforced
   - Validation: All specs comply with constitution.md

**Output Artifacts:**
- Complete specification set (15 new files)
- Consistency validation report
- Constitution compliance checklist

**Agents Involved:**
- None (human/Claude review process)

**Validation Checkpoints:**
- [ ] All 15 specification files created
- [ ] No spec contradictions exist
- [ ] Constitution compliance verified
- [ ] Specs approved for implementation

**Estimated Duration:** BLOCKED - specifications must be completed first

---

### Stage 1: Database Readiness

**Purpose:** Implement database schema with all required tables for multi-user, conversational, multimodal system

**Prerequisites:**
- database/schema.md specification completed
- Constitution section 11 (Database Constitution) reviewed

**Input Specs Referenced:**
- database/schema.md
- constitution.md (sections 11, 7.2)

**Tasks:**

1. **Database Connection Setup**
   - Configure Neon PostgreSQL connection
   - Set up async SQLAlchemy with SQLModel
   - Configure connection pooling
   - Environment variables for DB credentials
   - Validation: Connection successful, no errors

2. **Schema Implementation**
   - Create `users` table (managed by Better Auth)
   - Create `tasks` table with user_id isolation
   - Create `conversations` table with user_id isolation
   - Create `messages` table with user_id + conversation_id
   - Validation: All tables created with correct columns

3. **Indexes & Constraints**
   - Add indexes on user_id for all tables
   - Add indexes on conversation_id for messages
   - Add foreign key constraints (tasks→users, conversations→users, messages→users+conversations)
   - Add cascade delete rules
   - Validation: EXPLAIN queries show index usage

4. **Migration Infrastructure**
   - Set up Alembic for database migrations
   - Create initial migration
   - Test migration rollback
   - Validation: Migrations apply cleanly

5. **Test Data Seeding**
   - Create fixture for test users
   - Create fixture for test tasks
   - Create fixture for test conversations
   - Validation: Test data queryable

**Output Artifacts:**
- Database tables (users, tasks, conversations, messages)
- Alembic migration files
- Database connection module
- Test fixtures

**Agents Involved:**
- None (direct database setup, not agent work)

**Validation Checkpoints:**
- [ ] All tables exist with correct schema
- [ ] Indexes created on user_id fields
- [ ] Foreign keys enforce referential integrity
- [ ] Migrations apply and rollback successfully
- [ ] Test fixtures load without errors

---

### Stage 2: MCP Tool Layer Implementation

**Purpose:** Implement all 5 MCP tools as the exclusive data access layer

**Prerequisites:**
- Stage 1 (Database Readiness) completed
- mcp/tools.md specification completed

**Input Specs Referenced:**
- mcp/tools.md
- constitution.md (sections 5, 6.1)
- architecture.md (MCP Integration section)

**Tasks:**

1. **MCP Server Setup**
   - Initialize MCP server project structure
   - Configure tool registry
   - Set up database connection for MCP server
   - Validation: MCP server starts without errors

2. **Implement add_task Tool**
   - Accept parameters: user_id, title, description, due_date, due_time, priority, status
   - Validate all required fields present
   - Insert task into database with user_id isolation
   - Return task_id and created timestamp
   - Validation: Task created and queryable with correct user_id

3. **Implement list_tasks Tool**
   - Accept parameters: user_id, filters (status, due_before, due_after), sort, limit, offset
   - Query tasks with user_id WHERE clause
   - Apply filters and sorting
   - Return array of tasks + count + has_more flag
   - Validation: Only user's tasks returned, never other users'

4. **Implement update_task Tool**
   - Accept parameters: user_id, task_id, fields_to_update
   - Verify task belongs to user_id (ownership check)
   - Update specified fields only
   - Return updated task object
   - Validation: Cannot update other users' tasks (authorization test)

5. **Implement complete_task Tool**
   - Accept parameters: user_id, task_id
   - Verify task ownership
   - Set status=completed, completed_at=now()
   - Return updated task
   - Validation: Task marked complete with timestamp

6. **Implement delete_task Tool**
   - Accept parameters: user_id, task_id
   - Verify task ownership
   - Delete task from database
   - Return success confirmation
   - Validation: Task deleted, not accessible afterward

7. **Error Handling & Validation**
   - Implement parameter validation for all tools
   - Implement SQL injection prevention (parameterized queries)
   - Implement error response standardization
   - Validation: Invalid inputs rejected with clear errors

8. **Multi-User Isolation Testing**
   - Create tasks for user A and user B
   - Verify user A cannot access user B's tasks via any tool
   - Test all 5 tools with cross-user attempts
   - Validation: All cross-user access attempts fail

**Output Artifacts:**
- MCP server with 5 tools (add_task, list_tasks, update_task, complete_task, delete_task)
- Tool parameter validation logic
- Error handling standardization
- Multi-user isolation tests

**Agents Involved:**
- None (MCP tools are infrastructure, not agent-driven)

**Validation Checkpoints:**
- [ ] All 5 MCP tools functional
- [ ] User isolation enforced for all tools
- [ ] Parameter validation working
- [ ] Error responses standardized
- [ ] Cross-user access tests passing (all rejections)

---

### Stage 3: Skill Layer Implementation

**Purpose:** Implement all 7 skills that agents use to invoke MCP tools

**Prerequisites:**
- Stage 2 (MCP Tool Layer) completed
- skills/*.md specifications completed (all 7 files)

**Input Specs Referenced:**
- skills/task_creation.md
- skills/task_listing.md
- skills/task_update.md
- skills/task_completion.md
- skills/task_deletion.md
- skills/intent_disambiguation.md
- skills/ui_intent_normalization.md
- constitution.md (section 4.2)

**Tasks:**

1. **Implement task_creation Skill**
   - Accept: user_id, title, description, due_date, priority, status
   - Invoke: add_task MCP tool
   - Handle: MCP tool errors and return formatted result
   - Validation: Skill correctly wraps MCP tool

2. **Implement task_listing Skill**
   - Accept: user_id, filters, sort, limit
   - Invoke: list_tasks MCP tool
   - Handle: Empty results, pagination
   - Validation: Skill returns formatted task list

3. **Implement task_update Skill**
   - Accept: user_id, task_id, updates object
   - Invoke: update_task MCP tool
   - Handle: Ownership errors, not found errors
   - Validation: Skill correctly updates and handles errors

4. **Implement task_completion Skill**
   - Accept: user_id, task_id
   - Invoke: complete_task MCP tool
   - Handle: Already completed, not found
   - Validation: Skill marks task complete

5. **Implement task_deletion Skill**
   - Accept: user_id, task_id
   - Invoke: delete_task MCP tool
   - Handle: Not found, already deleted
   - Validation: Skill deletes task

6. **Implement intent_disambiguation Skill**
   - Accept: user_input, possible_intents
   - Analyze ambiguity (multiple tasks match, unclear action)
   - Return: Clarification question with options
   - Validation: Skill generates useful clarification

7. **Implement ui_intent_normalization Skill**
   - Accept: raw_input, modality (text/voice/image), input_type
   - Parse: CLI commands, natural language, voice transcripts, image data
   - Extract: Action (create/update/list/complete/delete) + parameters
   - Return: Structured intent object with confidence score
   - Validation: Skill normalizes all input types correctly

8. **Skill Testing**
   - Unit test each skill independently
   - Integration test skill → MCP tool flow
   - Test error propagation
   - Validation: All skills pass tests

**Output Artifacts:**
- 7 skill implementations
- Skill unit tests
- Skill integration tests
- Error handling patterns

**Agents Involved:**
- None (skills are infrastructure for agents to use)

**Validation Checkpoints:**
- [ ] All 7 skills implemented
- [ ] Skills correctly invoke MCP tools
- [ ] Error handling working for all skills
- [ ] Unit tests passing for all skills
- [ ] Integration tests passing (skill → MCP → DB)

---

### Stage 4: Agent Layer Wiring

**Purpose:** Implement all 6 agents with correct skill invocations and coordination

**Prerequisites:**
- Stage 3 (Skill Layer) completed
- agents/*.md specifications completed (all 6 files)

**Input Specs Referenced:**
- agents/orchestrator.md
- agents/task-reasoning.md
- agents/validation-safety.md
- agents/response-formatter.md
- agents/interface-orchestrator.md
- agents/visual-context.md
- constitution.md (section 4.1)
- architecture.md (Agent Orchestration Flow)

**Tasks:**

1. **Implement Interface Orchestrator Agent**
   - Detect modality (text/voice/image)
   - Invoke ui_intent_normalization skill
   - Extract user_id from context
   - Return normalized intent to main Orchestrator
   - Validation: Agent correctly normalizes all input types

2. **Implement Task Reasoning Agent**
   - Parse natural language for task operations
   - Extract dates, times, priorities from text
   - Invoke appropriate skill (task_creation, task_update, etc.)
   - Handle ambiguous requests via intent_disambiguation skill
   - Validation: Agent extracts task data and invokes skills correctly

3. **Implement Validation & Safety Agent**
   - Validate all input parameters (types, lengths, formats)
   - Enforce business rules (date ranges, enum values)
   - Check user ownership for updates/deletes
   - Return validation errors or success
   - Validation: Agent blocks invalid inputs, allows valid ones

4. **Implement Response Formatter Agent**
   - Convert technical results to user messages
   - Adapt to modality (concise for voice, detailed for text)
   - Humanize error codes
   - Format success confirmations
   - Validation: Agent produces appropriate responses for each modality

5. **Implement Visual Context Agent (Phase 5)**
   - Accept image data (base64 or URL)
   - Perform OCR to extract text
   - Parse extracted text for task info (title, dates, priorities)
   - Assess image quality and return confidence scores
   - Return structured extraction results
   - Validation: Agent extracts task data from images with acceptable accuracy

6. **Implement Orchestrator Agent**
   - Receive normalized intent from Interface Orchestrator
   - Route to appropriate agents (Task Reasoning, Validation, Visual Context)
   - Coordinate multi-agent workflows
   - Collect results and pass to Response Formatter
   - Return final response
   - Validation: Agent coordinates all sub-agents correctly

7. **Agent Coordination Testing**
   - Test full flow: Input → Interface Orchestrator → Orchestrator → Task Reasoning → Validation → Response Formatter
   - Test error handling at each agent
   - Test multi-agent workflows (e.g., image + task creation)
   - Validation: End-to-end agent coordination working

**Output Artifacts:**
- 6 agent implementations
- Agent unit tests
- Agent integration tests
- Agent coordination tests

**Agents Involved:**
- All 6 agents (this is their implementation stage)

**Validation Checkpoints:**
- [ ] All 6 agents implemented
- [ ] Agents correctly invoke skills
- [ ] Agent coordination working (Orchestrator → specialized agents)
- [ ] Error handling working at all agent levels
- [ ] End-to-end tests passing (input → agents → skills → MCP → DB → response)

---

### Stage 5: Chat Endpoint Integration

**Purpose:** Implement the stateless conversational API endpoint

**Prerequisites:**
- Stage 4 (Agent Layer) completed
- api/chat-endpoint.md specification completed

**Input Specs Referenced:**
- api/chat-endpoint.md
- constitution.md (sections 3.2, 12.1)
- architecture.md (Stateless Request Flow)

**Tasks:**

1. **API Endpoint Implementation**
   - Create POST /api/{user_id}/chat endpoint
   - Accept: conversation_id (optional), message, modality, metadata
   - Extract user_id from URL path
   - Validate JWT token (user authentication)
   - Validation: Endpoint accepts requests

2. **Stateless Conversation Loading**
   - If conversation_id provided: load last N messages from database
   - If conversation_id not provided: create new conversation
   - Reconstruct conversation context from messages table
   - Validation: Conversation state loaded from DB, not memory

3. **Agent Invocation from API**
   - Pass request to Interface Orchestrator Agent
   - Interface Orchestrator → Orchestrator → Specialized Agents
   - Agents invoke skills → MCP tools → Database operations
   - Validation: API successfully invokes agent chain

4. **Conversation Persistence**
   - Store user message in messages table (role="user")
   - Store agent response in messages table (role="assistant")
   - Update conversation updated_at timestamp
   - Validation: Messages persisted to DB

5. **Response Formatting & Return**
   - Format response according to modality
   - Include conversation_id in response
   - Include tool_calls metadata (which MCP tools were invoked)
   - Return JSON response
   - Validation: Response structure matches spec

6. **Error Handling**
   - Catch agent errors and return formatted error responses
   - Catch MCP tool errors and return user-friendly messages
   - Log errors for debugging
   - Validation: All error types handled gracefully

7. **Stateless Verification Testing**
   - Test: Server restart between requests → conversation resumes correctly
   - Test: No in-memory state → all context from database
   - Test: Concurrent requests → no state collision
   - Validation: System is truly stateless

**Output Artifacts:**
- POST /api/{user_id}/chat endpoint
- Conversation loading/saving logic
- Stateless request cycle implementation
- Error handling for API layer

**Agents Involved:**
- All 6 agents (invoked by API endpoint)

**Validation Checkpoints:**
- [ ] Chat endpoint functional
- [ ] Conversation loaded from database (stateless)
- [ ] Messages persisted after each request
- [ ] Agents invoked correctly from API
- [ ] Response format matches specification
- [ ] Stateless verification tests passing

---

### Stage 6: Multimodal Interface Implementation

**Purpose:** Implement text, voice, and image input processing

**Prerequisites:**
- Stage 5 (Chat Endpoint) completed
- ui/chat.md, ui/voice.md, ui/image-interface.md specifications completed

**Input Specs Referenced:**
- ui/chat.md
- ui/voice.md
- ui/image-interface.md
- constitution.md (sections 6, 13, 14, 15)
- architecture.md (Intent Normalization Layer)

---

#### Sub-Stage 6.1: Text Chat Interface

**Tasks:**

1. **Web Chat UI Setup**
   - Set up Next.js project with OpenAI ChatKit
   - Configure domain allowlist
   - Environment variables (API endpoint, auth tokens)
   - Validation: Chat UI renders

2. **Text Input Integration**
   - User types message → send to POST /api/{user_id}/chat with modality="text"
   - Display agent response in chat
   - Maintain conversation_id across messages
   - Validation: Text messages processed correctly

3. **Conversation History Display**
   - Load conversation messages on page load
   - Display user and assistant messages
   - Format task operation results (created, updated, deleted)
   - Validation: Conversation history displays correctly

4. **CLI Text Interface**
   - Implement CLI command parser
   - Parse commands like "todo add 'Task title' --due tomorrow"
   - Send structured intent to chat endpoint
   - Display formatted responses
   - Validation: CLI commands work

**Output Artifacts:**
- Web chat UI (Next.js + ChatKit)
- CLI text interface
- Text intent normalization

**Validation Checkpoints:**
- [ ] Web chat UI functional
- [ ] CLI commands functional
- [ ] Conversation history loads correctly
- [ ] Text modality end-to-end working

---

#### Sub-Stage 6.2: Voice Interface

**Tasks:**

1. **Speech-to-Text Integration**
   - Integrate OpenAI Whisper API
   - Record user audio in browser/CLI
   - Send audio to Whisper for transcription
   - Receive text transcription
   - Validation: Audio transcribed to text

2. **Voice Intent Processing**
   - Send transcribed text to POST /api/{user_id}/chat with modality="voice"
   - Interface Orchestrator detects voice modality
   - ui_intent_normalization skill processes voice input
   - Validation: Voice commands understood

3. **Text-to-Speech Integration**
   - Integrate OpenAI TTS API
   - Convert agent text response to speech
   - Play audio response to user
   - Validation: Responses spoken back to user

4. **Voice-Optimized Response Formatting**
   - Response Formatter generates concise responses for voice
   - Remove visual elements (checkmarks, emojis)
   - Keep responses under 30 seconds spoken
   - Validation: Voice responses appropriately formatted

**Output Artifacts:**
- Speech-to-text integration (Whisper)
- Text-to-speech integration (OpenAI TTS)
- Voice-optimized response formatting

**Validation Checkpoints:**
- [ ] Voice input transcribed correctly
- [ ] Voice intents processed like text
- [ ] Responses spoken back to user
- [ ] Voice responses concise and clear

---

#### Sub-Stage 6.3: Image Interface

**Tasks:**

1. **Image Upload Integration**
   - Allow users to upload images (screenshots, photos)
   - Support formats: PNG, JPG, WebP
   - Validate image size (< 10MB)
   - Validation: Images upload successfully

2. **Visual Context Agent Integration**
   - Send image to Visual Context Agent
   - Agent performs OCR to extract text
   - Agent parses dates, priorities, task info
   - Agent returns structured extraction results
   - Validation: Task data extracted from images

3. **Image Intent Processing**
   - Send extracted data to POST /api/{user_id}/chat with modality="image"
   - Task Reasoning Agent uses extracted data for task creation
   - Validation Agent validates extracted data
   - Validation: Tasks created from image data

4. **Image Quality Handling**
   - Detect low-quality images (Visual Context Agent)
   - Return error with guidance ("Please capture clearer image")
   - Validation: Poor quality images rejected with clear message

5. **Image Privacy Handling**
   - Discard image data after OCR extraction
   - Do not store images long-term (privacy)
   - Validation: Images not persisted after processing

**Output Artifacts:**
- Image upload UI
- Visual Context Agent integration
- Image-to-task workflow
- Image quality error handling

**Validation Checkpoints:**
- [ ] Images upload and process successfully
- [ ] Text extracted from images via OCR
- [ ] Tasks created from image data
- [ ] Low-quality images rejected appropriately
- [ ] Images discarded after processing (privacy)

---

**Overall Stage 6 Validation:**
- [ ] All three modalities (text, voice, image) functional
- [ ] Consistent results across modalities for same intent
- [ ] Response formatting adapts to modality
- [ ] End-to-end tests passing for all modalities

---

### Stage 7: Security Hardening

**Purpose:** Implement authentication, authorization, and security measures

**Prerequisites:**
- Stage 6 (Multimodal Interface) completed
- All prior stages operational

**Input Specs Referenced:**
- constitution.md (sections 8, 16)
- architecture.md (Security Architecture)

**Tasks:**

1. **Authentication Setup (Better Auth)**
   - Integrate Better Auth library
   - Configure JWT signing and validation
   - Set up user registration and login endpoints
   - Validation: Users can register and log in

2. **JWT Validation Middleware**
   - Create middleware to validate JWT on all API requests
   - Extract user_id from JWT claims
   - Reject requests with invalid/expired tokens
   - Validation: Unauthenticated requests rejected

3. **User Isolation Enforcement**
   - Verify user_id from JWT matches user_id in request path
   - MCP tools enforce user_id in all database queries
   - Test: User A cannot access User B's tasks
   - Validation: Cross-user access blocked at all layers

4. **Input Sanitization**
   - Validation Agent sanitizes all inputs
   - Remove SQL injection vectors
   - Remove XSS vectors (for web interface)
   - Validation: Injection attacks blocked

5. **Rate Limiting**
   - Implement rate limiting on chat endpoint
   - Limit: 60 requests/minute per user
   - Return 429 error when exceeded
   - Validation: Rate limiting working

6. **Error Message Sanitization**
   - Never expose internal errors to users
   - Sanitize database errors
   - Log full errors internally, return generic messages to users
   - Validation: Internal details not leaked in errors

7. **Security Testing**
   - Test SQL injection attempts → blocked
   - Test XSS attempts → sanitized
   - Test unauthorized access → rejected (401/403)
   - Test rate limiting → enforced
   - Validation: All security tests passing

**Output Artifacts:**
- Better Auth integration
- JWT validation middleware
- User isolation enforcement tests
- Input sanitization logic
- Rate limiting
- Security test suite

**Agents Involved:**
- Validation & Safety Agent (input sanitization)

**Validation Checkpoints:**
- [ ] Authentication working (Better Auth)
- [ ] JWT validation enforcing authorization
- [ ] User isolation working (cross-user tests fail)
- [ ] Input sanitization blocking injection attacks
- [ ] Rate limiting enforced
- [ ] Security tests all passing

---

## CONSTITUTION COMPLIANCE CHECKLIST

### ✅ Spec-Driven Development (Section 2.1)
- [ ] All features have specifications before implementation
- [ ] Implementation follows specs exactly
- [ ] No code written without corresponding spec

### ✅ Agentic Development Only (Section 2.2)
- [ ] All implementation via Claude Code agents
- [ ] No manual coding
- [ ] Human only authors specs and reviews

### ✅ Stateless Architecture (Section 2.3)
- [ ] No server session state
- [ ] All state in database (tasks, conversations, messages)
- [ ] Conversation resumes after restart
- [ ] Every request independently reproducible

### ✅ MCP-First Rule (Section 2.4)
- [ ] All data operations via MCP tools (add_task, list_tasks, etc.)
- [ ] Agents invoke skills → skills invoke MCP tools → MCP tools access DB
- [ ] No direct database access by agents

### ✅ Architecture Compliance (Section 3)
- [ ] Layers not bypassed: UI → API → Agents → Skills → MCP → DB
- [ ] Single conversational endpoint: POST /api/{user_id}/chat
- [ ] No additional endpoints without justification

### ✅ Agent & Skill Requirements (Section 4)
- [ ] All 6 required agents implemented
- [ ] All 7 required skills implemented
- [ ] Skills reusable across modalities

### ✅ MCP Tool Requirements (Section 5)
- [ ] All 5 MCP tools implemented (add_task, list_tasks, update_task, complete_task, delete_task)
- [ ] Tools enforce user_id isolation
- [ ] Tools are stateless

### ✅ Multimodal Support (Section 6)
- [ ] Text modality working
- [ ] Voice modality working (STT → intent → TTS)
- [ ] Image modality working (OCR → task extraction)
- [ ] All modalities converge to same agent intents

### ✅ Conversation Management (Section 7)
- [ ] Stateless request cycle enforced
- [ ] Conversations persist in database
- [ ] Messages table stores all exchanges
- [ ] No in-memory conversation state

### ✅ Authentication & Security (Section 8)
- [ ] Better Auth implemented
- [ ] JWT validation on all endpoints
- [ ] User isolation enforced at API, agent, and MCP layers

### ✅ Database Compliance (Section 11)
- [ ] Neon PostgreSQL used
- [ ] Async SQLAlchemy with SQLModel
- [ ] Alembic migrations
- [ ] All tables have user_id for isolation

### ✅ API Compliance (Section 12)
- [ ] POST /api/{user_id}/chat implemented
- [ ] Request/response formats match spec
- [ ] Consistent error handling

### ✅ Testing Requirements (Section 17)
- [ ] Unit tests > 80% coverage
- [ ] Integration tests for all endpoints
- [ ] MCP tool tests
- [ ] Agent behavior tests

---

## RISKS & MITIGATION STRATEGIES

### High-Priority Risks

1. **Risk: Specifications Incomplete**
   - **Impact:** BLOCKER - Cannot implement without specs
   - **Mitigation:** Complete `/sp.specify` immediately before proceeding
   - **Status:** ACTIVE BLOCKER

2. **Risk: Stateless Conversation Complexity**
   - **Impact:** HIGH - Core architectural requirement
   - **Mitigation:**
     - Strict adherence to architecture.md patterns
     - Rebuild conversation context from messages table on every request
     - Test: Server restart → conversation resumes correctly
   - **Testing:** Restart tests in Stage 5

3. **Risk: Multi-Agent Coordination Bugs**
   - **Impact:** HIGH - Agents must coordinate correctly
   - **Mitigation:**
     - Comprehensive integration tests per stage
     - Clear agent responsibility boundaries
     - Orchestrator Agent handles all routing
   - **Testing:** Agent coordination tests in Stage 4

4. **Risk: MCP Tool User Isolation Failures**
   - **Impact:** CRITICAL - Security vulnerability
   - **Mitigation:**
     - Every MCP tool enforces user_id in WHERE clauses
     - Cross-user access tests in Stage 2
     - Security audit in Stage 7
   - **Testing:** Multi-user isolation tests mandatory

5. **Risk: Image Processing Quality Issues**
   - **Impact:** MEDIUM - Affects Phase 5 functionality
   - **Mitigation:**
     - Quality thresholds in Visual Context Agent
     - Clear error messages for poor quality images
     - Confidence scoring for extracted data
   - **Testing:** Image quality tests in Stage 6.3

6. **Risk: Voice Transcription Accuracy**
   - **Impact:** MEDIUM - Affects Phase 4 functionality
   - **Mitigation:**
     - Use OpenAI Whisper (high accuracy)
     - Confidence scoring from STT
     - Clarification flow for low-confidence results
   - **Testing:** Voice accuracy tests in Stage 6.2

---

## DEPENDENCIES & PREREQUISITES

### External Services Required
- Neon PostgreSQL (database)
- Better Auth (authentication)
- OpenAI Whisper (speech-to-text)
- OpenAI TTS (text-to-speech)
- Claude API or GPT-4 Vision (image OCR/understanding)

### Internal Dependencies (Execution Order)
1. Specifications must be complete BEFORE Stage 1
2. Database (Stage 1) BEFORE MCP tools (Stage 2)
3. MCP tools (Stage 2) BEFORE Skills (Stage 3)
4. Skills (Stage 3) BEFORE Agents (Stage 4)
5. Agents (Stage 4) BEFORE API Endpoint (Stage 5)
6. API Endpoint (Stage 5) BEFORE Multimodal UI (Stage 6)
7. All functional stages (1-6) BEFORE Security (Stage 7)

---

## NEXT STEPS

### Immediate Actions Required

1. **BLOCKER: Complete Specifications**
   - Run `/sp.specify` to generate missing spec files:
     - 7 skill specs (specs/skills/*.md)
     - MCP tools spec (specs/mcp/tools.md)
     - API endpoint spec (specs/api/chat-endpoint.md)
     - Database schema spec (specs/database/schema.md)
     - 3 UI specs (specs/ui/*.md)
   - Review and approve all specifications
   - Verify constitution compliance

2. **After Specs Complete: Begin Stage 1**
   - Database setup (Neon PostgreSQL)
   - Schema implementation
   - Migration infrastructure

3. **Progress Through Stages Sequentially**
   - Do NOT skip stages
   - Complete validation checkpoints before moving forward
   - Document any deviations from plan (with justification)

---

## PLAN APPROVAL REQUIREMENTS

This plan cannot be executed until:

- [ ] All missing specifications completed
- [ ] Specifications reviewed and approved
- [ ] Constitution compliance verified
- [ ] External service accounts created (Neon, Better Auth, OpenAI)
- [ ] Development environment ready (Node.js, Python, Docker)

**Status:** ⚠️ PENDING SPECIFICATION COMPLETION

**Estimated Total Duration:** 8-12 weeks (after specs completed)

**Phases Covered:** 4 (AI Chatbot) + 5 (Multimodal Interface)

---

## SUMMARY

This plan provides a comprehensive, stage-by-stage implementation roadmap for Phases 4 & 5 of the Todo Intelligence Platform. It strictly adheres to the constitution's requirements for spec-driven, agentic, stateless, MCP-first development.

**Critical Path:**
1. Complete specifications (BLOCKER)
2. Database → MCP Tools → Skills → Agents → API → Multimodal UI → Security
3. Validate constitution compliance at each stage
4. Execute via Claude Code agents only

**Success Criteria:** A fully functional, conversational AI chatbot with text, voice, and image support, maintaining stateless architecture and MCP-first data access patterns.
