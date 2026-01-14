---
id: 1
title: Update Phase3 Constitution
stage: constitution
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: $ARGUMENTS
labels: [constitution, phase3, ai-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
---

## Prompt

```
$ARGUMENTS
```

Update the existing constitution to include Phase III: AI-Powered Todo Chatbot

**Phase III Principles:**

**Conversational AI Standards:**
- AI must understand natural language commands for all task operations
- Responses must be friendly, conversational, and confirm actions
- Agent must gracefully handle ambiguity and errors
- Never lose conversation context (store in database)

**MCP Architecture:**
- All task operations exposed as MCP tools (5 tools: add, list, complete, delete, update)
- MCP server is stateless - all state persists to database
- Tools follow consistent input/output schema
- Each tool must validate user_id for security

**Stateless Server Design:**
- Chat endpoint receives message, fetches history, processes, stores, returns
- Server holds NO conversation state in memory
- Each request is independent and reproducible
- Conversation resumes correctly after server restart

**Agent Behavior:**
- Use OpenAI Agents SDK for AI logic
- Agent decides which MCP tool(s) to call based on user intent
- Agent can chain multiple tools in one turn if needed
- Always confirm actions: "✅ Added task: Buy groceries"

**Database Schema Evolution:**
- Add `conversations` table (user_id, id, created_at, updated_at)
- Add `messages` table (user_id, id, conversation_id, role, content, created_at)
- Existing `tasks` table remains unchanged
- All tables indexed by user_id for multi-user support

**Technology Stack for Phase III:**
- Frontend: OpenAI ChatKit
- Backend: FastAPI (existing) + OpenAI Agents SDK + Official MCP SDK
- Database: Neon PostgreSQL (existing)
- Authentication: Better Auth (existing)

**Non-Negotiables:**
- DO NOT modify Phase 1 or Phase 2 functionality
- DO NOT change existing task CRUD operations
- DO NOT alter existing database tables
- Only ADD new chatbot interface and MCP layer
- Existing REST API endpoints must continue working

**Security:**
- All MCP tools require user_id parameter
- Validate user_id matches authenticated user
- No user can access another user's tasks via chatbot
- Conversation history isolated per user

**Error Handling:**
- Handle "task not found" gracefully
- Handle malformed natural language inputs
- Provide helpful error messages to user
- Log errors for debugging but don't expose internals
```

## Response snapshot

Updated the constitution file to include all the Phase III principles for the AI-Powered Todo Chatbot, incorporating all the specified requirements including Conversational AI Standards, MCP Architecture, Stateless Server Design, Agent Behavior, Database Schema Evolution, Technology Stack, Non-Negotiables, Security, and Error Handling.

## Outcome

- ✅ Impact: Updated constitution to include Phase III AI-powered todo chatbot principles
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Implement MCP tools for the AI chatbot
- 🧠 Reflection: The constitution now properly defines the architectural principles for Phase III

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing MCP tools as per constitution