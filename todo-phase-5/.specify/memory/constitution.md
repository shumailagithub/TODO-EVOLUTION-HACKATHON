<!-- SYNC IMPACT REPORT
Version change: N/A (Initial version) → 1.0.0
Modified principles: N/A
Added sections: All principles and sections for Todo Evolution Hackathon
Removed sections: None
Templates requiring updates: ⚠ pending (plan-template.md, spec-template.md, tasks-template.md, commands)
Follow-up TODOs: None
-->

# Todo Evolution Hackathon Constitution

## Core Principles

### I. Conversational AI Standards
AI must understand natural language commands for all task operations; Responses must be friendly, conversational, and confirm actions; Agent must gracefully handle ambiguity and errors; Never lose conversation context (store in database)

### II. MCP Architecture
All task operations exposed as MCP tools (5 tools: add, list, complete, delete, update); MCP server is stateless - all state persists to database; Tools follow consistent input/output schema; Each tool must validate user_id for security

### III. Stateless Server Design
Chat endpoint receives message, fetches history, processes, stores, returns; Server holds NO conversation state in memory; Each request is independent and reproducible; Conversation resumes correctly after server restart

### IV. Agent Behavior
Use OpenAI Agents SDK for AI logic; Agent decides which MCP tool(s) to call based on user intent; Agent can chain multiple tools in one turn if needed; Always confirm actions: "✅ Added task: Buy groceries"

### V. Database Schema Evolution
Add `conversations` table (user_id, id, created_at, updated_at); Add `messages` table (user_id, id, conversation_id, role, content, created_at); Existing `tasks` table remains unchanged; All tables indexed by user_id for multi-user support

### VI. Technology Stack for Phase III
Frontend: OpenAI ChatKit; Backend: FastAPI (existing) + OpenAI Agents SDK + Official MCP SDK; Database: Neon PostgreSQL (existing); Authentication: Better Auth (existing)

### VII. Non-Negotiables
DO NOT modify Phase 1 or Phase 2 functionality; DO NOT change existing task CRUD operations; DO NOT alter existing database tables; Only ADD new chatbot interface and MCP layer; Existing REST API endpoints must continue working

### VIII. Security
All MCP tools require user_id parameter; Validate user_id matches authenticated user; No user can access another user's tasks via chatbot; Conversation history isolated per user

### IX. Error Handling
Handle "task not found" gracefully; Handle malformed natural language inputs; Provide helpful error messages to user; Log errors for debugging but don't expose internals

## Additional Constraints

### Technology Stack Requirements
- Frontend: React with TypeScript
- Backend: FastAPI with Python 3.11+
- Database: PostgreSQL with Neon
- Authentication: Better Auth
- AI Framework: OpenAI Agents SDK
- MCP Framework: Official MCP SDK

### Performance Standards
- Response time under 2 seconds for all AI interactions
- Database queries optimized with proper indexing
- Conversation history retrieval efficient for long conversations
- Task operations should maintain existing performance levels

### Security Requirements
- All user data properly isolated by user_id
- Authentication required for all endpoints
- MCP tools validate user permissions
- Input sanitization for all natural language inputs

## Development Workflow

### Code Review Requirements
- All MCP tools must include user_id validation
- Database migrations must be backward compatible
- AI interactions must include proper error handling
- New features must not break existing functionality

### Testing Gates
- Unit tests for all MCP tools
- Integration tests for conversation flow
- End-to-end tests for AI interactions
- Database isolation tests for multi-user scenarios

### Quality Standards
- All new code follows existing project patterns
- Type safety maintained throughout
- Proper error handling and logging
- Documentation for all new public interfaces

## Governance

All development must comply with these principles. Any deviation requires explicit approval and documentation of the exception. Code reviews must verify compliance with all principles, especially security requirements and non-negotiable constraints. New features must enhance rather than replace existing functionality.

**Version**: 1.0.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-01-12