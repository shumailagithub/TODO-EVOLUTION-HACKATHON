# Tasks: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Branch**: `5-ai-chatbot`
**Created**: 2026-01-12
**Input**: Specification from `specs/5-ai-chatbot/spec.md`

## Overview

This task breakdown implements the AI-Powered Todo Chatbot that allows users to manage their todo list using natural language commands. The system includes MCP tools for task operations, OpenAI integration for natural language processing, and conversation persistence in the database.

## Dependencies

- Existing Phase I & II functionality must remain unchanged
- Better Auth for authentication
- PostgreSQL with Neon for database
- OpenAI API for AI processing

---

## Phase 1: Setup

**Goal**: Initialize project structure and dependencies for the AI chatbot feature

- [X] T001 Install required dependencies: `pip install openai`
- [X] T002 Add OPENAI_API_KEY to environment variables in `.env` and `.env.example`
- [X] T003 Create backend directory structure: `mcp/`, `services/`, `models/`, `db/`
- [X] T004 Create frontend directory structure: `pages/` (if not exists)
- [X] T005 Verify existing database connection is working

---

## Phase 2: Foundational Components

**Goal**: Implement core database models and operations that all user stories depend on

- [X] T006 [P] Create Conversation model in `backend/models/conversation.py`
- [X] T007 [P] Create Message model in `backend/models/message.py`
- [X] T008 Create database operations for conversations in `backend/db/conversation_operations.py`
- [X] T009 Create MCP server structure in `backend/mcp/server.py`
- [X] T010 Create agent service structure in `backend/services/agent_service.py`
- [X] T011 Create chat API structure in `backend/api/chat.py`

---

## Phase 3: Natural Language Task Management (User Story 1 - P1)

**Goal**: Enable users to manage their todo list using natural language commands

**Independent Test**: User can send natural language commands like "Add buy groceries" and the system creates appropriate tasks

### Implementation Tasks

- [X] T012 [P] [US1] Implement add_task MCP tool in `backend/mcp/server.py`
- [X] T013 [P] [US1] Implement list_tasks MCP tool in `backend/mcp/server.py`
- [X] T014 [P] [US1] Implement complete_task MCP tool in `backend/mcp/server.py`
- [X] T015 [P] [US1] Implement delete_task MCP tool in `backend/mcp/server.py`
- [X] T016 [P] [US1] Implement update_task MCP tool in `backend/mcp/server.py`
- [X] T017 [US1] Create OpenAI agent configuration in `backend/services/agent_service.py`
- [X] T018 [US1] Implement agent runner function with tool calling in `backend/services/agent_service.py`
- [X] T019 [US1] Implement chat endpoint logic in `backend/api/chat.py`
- [X] T020 [US1] Create frontend chat interface in `frontend/pages/chat.js`
- [X] T021 [US1] Test complete natural language flow: "Add groceries" → AI → MCP → Task created

---

## Phase 4: MCP Tool Integration (User Story 2 - P2)

**Goal**: Expose all task operations as MCP tools that the AI agent can call to perform operations on the user's behalf

**Independent Test**: MCP tools can be called directly and perform correct CRUD operations with proper user validation

### Implementation Tasks

- [X] T022 [P] [US2] Add user_id validation to all MCP tools in `backend/mcp/server.py`
- [X] T023 [P] [US2] Test each MCP tool individually with valid parameters in `backend/mcp/server.py`
- [X] T024 [P] [US2] Test MCP tools with invalid user_id to ensure security in `backend/mcp/server.py`
- [X] T025 [US2] Create MCP tool registration and discovery in `backend/mcp/server.py`
- [X] T026 [US2] Test tool calling from OpenAI agent in `backend/services/agent_service.py`
- [X] T027 [US2] Verify consistent input/output schema across all MCP tools in `backend/mcp/server.py`

---

## Phase 5: Conversation Context Management (User Story 3 - P3)

**Goal**: Maintain conversation context and store conversation history in the database to provide continuity across sessions

**Independent Test**: Conversation history is preserved across server restarts and context is maintained during multi-turn conversations

### Implementation Tasks

- [X] T028 [P] [US3] Implement conversation creation function in `backend/db/conversation_operations.py`
- [X] T029 [P] [US3] Implement conversation history retrieval function in `backend/db/conversation_operations.py`
- [X] T030 [P] [US3] Implement message storage function in `backend/db/conversation_operations.py`
- [X] T031 [US3] Integrate conversation management into chat endpoint in `backend/api/chat.py`
- [X] T032 [US3] Test conversation context preservation after server restart
- [X] T033 [US3] Test multi-turn conversations maintain context properly

---

## Phase 6: Frontend Integration & Polish

**Goal**: Complete the frontend experience and ensure seamless integration with existing application

### Implementation Tasks

- [X] T034 [P] Style chat interface to match existing design in `frontend/pages/chat.js`
- [X] T035 [P] Add loading indicators during AI processing in `frontend/pages/chat.js`
- [X] T036 [P] Add error handling for frontend in `frontend/pages/chat.js`
- [X] T037 Add "Chat" link to navigation in `frontend/components/Navbar.tsx`
- [X] T038 Register chat router in main application in `backend/main.py`
- [X] T039 Update root endpoint to include chat API documentation in `backend/main.py`
- [X] T040 Test frontend authentication flow with chat page in `frontend/pages/chat.js`

---

## Phase 7: Testing & Validation

**Goal**: Validate complete system functionality and ensure no regression in existing features

### Implementation Tasks

- [X] T041 Test natural language commands: "Add groceries", "Show tasks", "Mark 1 done"
- [X] T042 Test conversation history persistence across sessions
- [X] T043 Test error handling: invalid task IDs, malformed commands
- [X] T044 Test user isolation: ensure users can't access other users' tasks
- [X] T045 Verify Phase II functionality unchanged: REST API, web UI still work
- [X] T046 Test multi-user scenarios with proper data isolation
- [X] T047 Performance test: ensure responses under 2 seconds
- [X] T048 Security test: verify authentication and authorization work correctly

---

## Phase 8: Documentation & Deployment

**Goal**: Complete documentation and prepare for deployment

### Implementation Tasks

- [X] T049 Update README with Phase III setup instructions
- [X] T050 Document environment variables needed for chatbot
- [X] T051 Create usage examples for natural language commands
- [X] T052 Document MCP tools API contracts
- [X] T053 Clean up console logs and debug code
- [X] T054 Run code formatter and linter
- [X] T055 Create git tag: `v3.0-phase3`
- [X] T056 Final integration test of complete system

---

## Task Dependencies

### User Story Dependencies
- US2 (MCP Tool Integration) depends on US1 (Natural Language Task Management) for basic tool structure
- US3 (Conversation Context Management) depends on US1 (Natural Language Task Management) for basic functionality

### Implementation Dependencies
- T006-T007 (Models) must be completed before T008 (DB Operations)
- T008 (DB Operations) must be completed before T019 (Chat Endpoint)
- T012-T016 (MCP Tools) must be completed before T017 (Agent Service)
- T017 (Agent Service) must be completed before T019 (Chat Endpoint)

---

## Parallel Execution Opportunities

### Phase 2 (Foundational Components)
- T006, T007 can run in parallel (different model files)
- T009, T010, T011 can run in parallel (different service files)

### Phase 3 (User Story 1)
- T012-T016 can run in parallel (different MCP tools)
- T017, T018 can run in parallel (agent service components)

### Phase 7 (Testing & Validation)
- T041-T044 can run in parallel (different test scenarios)
- T045-T047 can run in parallel (different validation tests)

---

## Implementation Strategy

**MVP Scope**: Implement User Story 1 (Natural Language Task Management) as minimum viable product with basic add/list/complete functionality.

**Incremental Delivery**:
1. Complete Phase 1-2 (Setup & Foundation)
2. Complete Phase 3 (Core US1 functionality)
3. Complete Phase 4 (US2 MCP integration)
4. Complete Phase 5 (US3 context management)
5. Complete Phase 6-8 (Polish, testing, documentation)