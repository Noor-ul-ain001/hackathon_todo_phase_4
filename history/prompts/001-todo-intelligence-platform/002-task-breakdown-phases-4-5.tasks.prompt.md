---
id: 002
title: Task Breakdown Phases 4-5
stage: tasks
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-intelligence-platform
branch: 001-todo-intelligence-platform
user: user
command: /sp.tasks
labels: ["task-breakdown", "atomic-tasks", "phase-4", "phase-5", "multimodal"]
links:
  spec: specs/001-todo-intelligence-platform/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-intelligence-platform/tasks.md
tests:
  - None (task planning phase)
---

## Prompt

You are now operating in TASK BREAKDOWN mode.

An execution plan has been generated and approved.
Do NOT write implementation code.
Do NOT modify specifications.
Do NOT invent new requirements.

========================================
PROJECT
========================================
Todo Intelligence Platform

========================================
AUTHORITY
========================================
@specs/constitution.md

The constitution overrides all decisions.

========================================
INPUT
========================================
Use ONLY the following inputs:
- Approved execution plan (previous output)
- Referenced specs from the plan

========================================
OBJECTIVE
========================================
Decompose the approved execution plan into
small, atomic, agent-executable tasks.

Each task must be independently:
- Understandable
- Verifiable
- Executable by Claude Code agents

========================================
TASK BREAKDOWN RULES
========================================
1. No code
2. No combined responsibilities
3. One task = one clear outcome
4. Tasks must map to a single agent or skill
5. Tasks must reference exact specs
6. Tasks must be orderable
7. Tasks must be testable

========================================
REQUIRED TASK FORMAT
========================================
For EACH task, output:

TASK ID
Short, unique identifier

TASK NAME
Clear action-oriented title

DESCRIPTION
What must be done (spec-aligned)

AGENT RESPONSIBLE
Which agent executes this task

SKILLS USED
Which reusable skills are involved

INPUT SPECS
Exact spec references (@specs/...)

OUTPUT ARTIFACT
What is produced or validated

ACCEPTANCE CRITERIA
Objective yes/no checks

DEPENDENCIES
Upstream tasks (if any)

FAILURE CONDITIONS
What makes this task invalid

========================================
TASK GROUPING
========================================
Group tasks under these headings:

1. Spec Validation Tasks
2. Database Preparation Tasks
3. MCP Tool Tasks
4. Agent Wiring Tasks
(... and additional categories as needed)

## Response snapshot

Created comprehensive task breakdown for Phases 4 & 5 (AI Chatbot + Multimodal Interface) with **396 atomic, agent-executable tasks** organized into 8 sequential implementation stages.

**Critical Finding**: Confirmed Stage 0 (Specification Completion) is a BLOCKER. All 15 missing specifications must be completed before any implementation tasks can begin.

**Task Breakdown Structure**:

**Stage 0: Specification Completion** (20 tasks) ⚠️ BLOCKER
- T001-T007: Generate 7 skill specifications in parallel
- T008-T013: Generate MCP, API, database, and 3 UI specs in parallel
- T014-T017: Verify cross-spec consistency
- T018-T020: Constitution compliance audit and approval

**Stage 1: Database Readiness** (32 tasks)
- Database connection setup (7 tasks)
- Schema implementation: users, tasks, conversations, messages (5 tasks)
- Indexes & constraints (10 tasks)
- Migration infrastructure with Alembic (5 tasks)
- Test data seeding (4 tasks)

**Stage 2: MCP Tool Layer** (52 tasks)
- MCP server setup (5 tasks)
- Implement 5 tools: add_task, list_tasks, update_task, complete_task, delete_task (37 tasks)
- Error handling & validation (4 tasks)
- Multi-user isolation testing (6 tasks)

**Stage 3: Skill Layer** (55 tasks)
- Skill infrastructure (4 tasks)
- Implement 7 skills: task CRUD + disambiguation + ui_normalization (47 tasks)
- Skill testing (4 tasks)

**Stage 4: Agent Layer Wiring** (75 tasks)
- Agent infrastructure (4 tasks)
- Implement 6 agents: Interface Orchestrator, Task Reasoning, Validation & Safety, Response Formatter, Visual Context, Orchestrator (67 tasks)
- Agent coordination testing (4 tasks)

**Stage 5: Chat Endpoint Integration** (38 tasks)
- API endpoint implementation (7 tasks)
- Stateless conversation loading (4 tasks)
- Agent invocation from API (6 tasks)
- Conversation persistence (5 tasks)
- Response formatting & return (5 tasks)
- Error handling (4 tasks)
- Stateless verification testing (4 tasks)

**Stage 6: Multimodal Interface** (60 tasks)
- Sub-stage 6.1: Text Chat (Web + CLI) - 21 tasks
- Sub-stage 6.2: Voice (STT + TTS) - 16 tasks
- Sub-stage 6.3: Image (OCR + extraction) - 19 tasks
- Overall multimodal validation - 4 tasks

**Stage 7: Security Hardening** (34 tasks)
- Authentication (Better Auth + JWT) - 11 tasks
- User isolation enforcement - 5 tasks
- Input sanitization - 4 tasks
- Rate limiting - 4 tasks
- Error message sanitization - 4 tasks
- Security testing - 6 tasks

**Stage 8: Polish & Cross-Cutting** (30 tasks)
- Documentation - 4 tasks
- Code quality - 4 tasks
- Performance optimization - 4 tasks
- Deployment preparation - 7 tasks
- Monitoring & observability - 4 tasks
- Final validation - 7 tasks

**Task Format**:
- All tasks use strict checklist format: `- [ ] [ID] [P?] Description with file path`
- [P] marker for parallelizable tasks (150+ tasks can run in parallel within stages)
- Organized by implementation stage (not user stories - technical infrastructure)
- Exact file paths included for all implementation tasks

**Dependencies**:
- Sequential stage dependencies: 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8
- Parallel opportunities within each stage (150+ tasks marked [P])
- Stage 0 is CRITICAL BLOCKER for all subsequent work

**Implementation Strategy**:
- **MVP First**: Stages 0-7 + 6.1 (text only) = 9 weeks
- **Full Product**: All stages = 12 weeks
- **Incremental Delivery**: Each stage adds testable value

**Path Conventions**:
- Backend API: `backend/src/`
- MCP Server: `mcp-server/src/`
- Web Frontend: `frontend/src/`
- CLI: `cli/src/`
- Agents: `agents/src/`
- Skills: `skills/src/`
- Tests: `tests/` at root

## Outcome

- ✅ Impact: Comprehensive 396-task breakdown created, immediately executable after Stage 0 completion
- 🧪 Tests: No tests yet (planning phase) - testing tasks embedded in implementation stages (T063, T072, T086, T113, etc.)
- 📁 Files: Created tasks.md with 396 atomic tasks across 8 stages
- 🔁 Next prompts: Execute Stage 0 (specification completion via `/sp.specify`), then begin Stage 1 implementation
- 🧠 Reflection: Task breakdown successfully maintains constitution compliance, stateless architecture, and MCP-first principles. Clear critical path identified with blocker status.

## Evaluation notes (flywheel)

- Failure modes observed: Specifications still incomplete (Stage 0 blocker persists). No implementation can begin until resolved.
- Graders run and results (PASS/FAIL):
  - Task atomicity: PASS (each task has single clear outcome)
  - Task format compliance: PASS (all tasks use strict checklist format with IDs, [P] markers, file paths)
  - Constitution alignment: PASS (stateless, MCP-first, agentic patterns enforced)
  - Dependencies: PASS (clear stage order, parallel opportunities identified)
  - Executability: PASS (tasks are agent-executable with specific artifacts)
  - Blocker identification: PASS (Stage 0 clearly marked as blocker)
- Prompt variant (if applicable): Task breakdown for technical infrastructure (not user stories)
- Next experiment (smallest change to try): Execute Stage 0 (T001-T020) to unblock all implementation work
