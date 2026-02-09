# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `5-ai-chatbot` | **Date**: 2026-01-12 | **Spec**: [link to spec](./spec.md)
**Input**: Feature specification from `/specs/[5-ai-chatbot]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an AI-Powered Todo Chatbot that allows users to manage their todo list using natural language commands. The system includes MCP tools for task operations, OpenAI integration for natural language processing, and conversation persistence in the database. The implementation follows a bottom-up approach: Database → MCP Tools → Agent → API → Frontend, ensuring each layer is solid before building on top.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript, FastAPI, Next.js
**Primary Dependencies**: OpenAI SDK, SQLModel, FastAPI, Next.js, ChatKit
**Storage**: PostgreSQL with Neon (existing), new conversation/messages tables
**Testing**: Manual testing with comprehensive test plan (80+ test cases)
**Target Platform**: Web application (Linux/Mac/Windows server)
**Project Type**: Web (frontend + backend)
**Performance Goals**: <2 seconds response time for 90% of AI interactions
**Constraints**: User isolation, conversation context preservation, stateless server design
**Scale/Scope**: Multi-user support with proper user_id validation and isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Conversational AI Standards: AI understands natural language commands for all task operations
- ✅ MCP Architecture: All task operations exposed as MCP tools with consistent schema
- ✅ Stateless Server Design: All state persists to database, no conversation state in memory
- ✅ Agent Behavior: OpenAI Agent decides which tools to call based on user intent
- ✅ Database Schema Evolution: Added conversations and messages tables, preserved tasks table
- ✅ Non-Negotiables: Existing Phase I & II functionality preserved, no changes to existing CRUD
- ✅ Security: All tools validate user_id, conversation history isolated per user
- ✅ Error Handling: Graceful handling of "task not found" and malformed inputs

## Project Structure

### Documentation (this feature)

```text
specs/5-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── api/
│   └── chat.py          # Chat API endpoint
├── services/
│   └── agent_service.py # OpenAI Agent integration
├── mcp/
│   └── server.py        # MCP tools server with 5 tools
├── models/
│   ├── conversation.py  # Conversation model
│   └── message.py       # Message model
├── db/
│   ├── conversation_operations.py  # Conversation DB ops
│   └── task_operations.py          # Existing task ops (unchanged)
└── main.py              # Updated to include chat router

frontend/
├── pages/
│   └── chat.js          # Chat interface
└── components/
    └── Navbar.tsx       # Updated with Chat link
```

**Structure Decision**: Selected Web application structure with separate backend and frontend. Backend handles AI integration and MCP tools, while frontend provides user-friendly chat interface. This maintains separation of concerns while enabling rich user interactions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | | |