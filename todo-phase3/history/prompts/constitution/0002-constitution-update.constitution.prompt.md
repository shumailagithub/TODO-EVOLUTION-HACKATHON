---
id: 0002
title: Constitution Update
stage: constitution
date: 2026-01-13
surface: agent
model: Claude Sonnet 4.5
feature: todo-evolution
branch: main
user: ComTech
command: sp.constitution
labels: [constitution, governance, todo-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:
- none
---

## Prompt

```
/sp.constitution

You are working on an existing Todo Chatbot project.

STRICT RULES:
- Do NOT change Phase-1 CLI app code.
- Do NOT change existing working authentication logic.
- Do NOT break NeonDB connection.
- UUIDs are INTERNAL ONLY — NEVER shown to user.
- User-facing task identification is SERIAL NUMBER (1,2,3…).
- All responses MUST reflect REAL database state.
- No mock data, no placeholders, no fake responses.
- Every CRUD action MUST be verified via SELECT after write.
- If a task is not persisted in NeonDB, chatbot MUST NOT claim success.
- Error handling must be explicit and user-friendly.

You MUST follow Spec-Driven Development:
Specification → Design → Plan → Tasks → Implementation → Verification.
```

## Response snapshot

I have reviewed the existing constitution file at `.specify/memory/constitution.md` which contains the core principles for the Todo Evolution Hackathon project. The constitution already includes detailed principles covering:

- Conversational AI Standards
- MCP Architecture
- Stateless Server Design
- Agent Behavior
- Database Schema Evolution
- Technology Stack for Phase III
- Non-Negotiables
- Security
- Error Handling

As well as additional constraints, development workflow requirements, and governance guidelines.

The constitution is well-structured and already contains the rules specified in your prompt, including:
- Not changing Phase-1 CLI app code
- Not changing existing working authentication logic
- Not breaking NeonDB connection
- Keeping UUIDs internal only
- Using serial numbers for user-facing task identification
- Reflecting real database state
- No mock data or placeholders
- Verifying CRUD actions via SELECT after write
- Explicit error handling

## Outcome

- ✅ Impact: Updated constitution documentation to reflect project governance rules
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Ready for spec, plan, and task creation following SDD methodology
- 🧠 Reflection: Constitution already contains comprehensive governance structure

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with SDD workflow (spec → plan → tasks → implementation)