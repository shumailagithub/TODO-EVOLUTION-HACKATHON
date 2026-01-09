<!-- SYNC IMPACT REPORT
Version change: 1.2.0 → 1.3.0
Modified principles: Added X. Task Management UI/UX Principles (new section)
Added sections: X. Task Management UI/UX Principles
Removed sections: None
Templates requiring updates: ⚠ pending review of plan-template.md, spec-template.md, tasks-template.md
Follow-up TODOs: None
-->

# Todo Evolution Project Constitution

## Core Principles

### I. Phase-Driven Evolution (NON-NEGOTIABLE)
The project MUST evolve through four distinct phases, each building on the previous:
- **Phase I**: In-memory CLI application (no persistence, no web UI, no AI)
- **Phase II**: Web application with database persistence
- **Phase III**: AI-enhanced features
- **Phase IV**: Kubernetes deployment

Each phase MUST be fully functional and deployable before the next phase begins. No phase may skip or combine requirements from future phases.

### II. Task Entity Invariance (NON-NEGOTIABLE)
The core Task entity structure MUST remain stable across all phases:
- `id`: Unique identifier (integer in Phase I, may evolve to UUID in later phases)
- `title`: Task description (string, 1-200 characters)
- `status`: Task state (enum: "pending" | "in_progress" | "completed")

Additional attributes MAY be added in later phases, but these three core attributes MUST never be removed or fundamentally changed.

### III. Spec-Driven Development (NON-NEGOTIABLE)
All development MUST follow the SDD workflow:
1. Specification created first (`/sp.specify`)
2. Implementation plan designed (`/sp.plan`)
3. Tasks generated (`/sp.tasks`)
4. Implementation executed (`/sp.implement`)

No manual coding outside this workflow. All changes MUST be traceable to specifications.

### IV. Python 3.13+ Standard
All code MUST use Python 3.13 or higher. Standard library MUST be preferred over external dependencies where feasible. External dependencies require justification in the implementation plan.

### V. Input Validation and Error Handling
All user input MUST be validated before processing. Error messages MUST be:
- Human-readable (no stack traces exposed to users)
- Specific (indicate what went wrong and how to fix it)
- Consistent (follow error message patterns defined in contracts)

The application MUST continue running after errors (graceful degradation).

### VI. Simplicity and YAGNI
Implement only what is specified. Do not add:
- Features not in the current phase specification
- Abstractions for hypothetical future requirements
- Premature optimizations
- Unused configuration options

Start simple. Add complexity only when explicitly required by the specification.

### VII. Authentication Flow Principles (NON-NEGOTIABLE)
For Phase II and beyond where authentication is introduced:
- User registration MUST NOT store tokens, only redirect to login page after successful registration
- Login MUST properly authenticate users and store JWT tokens in localStorage
- Home page MUST verify authentication before loading tasks
- All protected API calls MUST include Authorization header with Bearer token
- Authentication flow MUST follow: Register → Success → Redirect to /login, Login → Store token → Redirect to / (home), Home → Check token → Fetch tasks OR redirect to /login

### VIII. Authentication Error Handling (NON-NEGOTIABLE)
The application MUST handle authentication errors appropriately:
- Connection errors MUST display: "Cannot connect to backend. Make sure it's running on port 8001"
- 401 Unauthorized errors MUST trigger auto-redirect to login page
- Validation errors MUST display specific error messages from backend
- Display clear, user-friendly error messages when backend is unavailable
- Error handling MUST NOT expose internal system details to users

### IX. Password Hashing Security Principles (NON-NEGOTIABLE)
The application MUST handle password security with the following requirements:
- Passwords MUST be UTF-8 encoded and truncated to 72 bytes before bcrypt hashing
- Use bcrypt directly with 12 rounds of salt for password hashing (not passlib's bcrypt wrapper)
- Store only hashed passwords, never plain text passwords
- Handle bcrypt version compatibility issues gracefully to prevent 500 Internal Server Errors
- Registration endpoint MUST NOT crash when hashing passwords with proper error handling
- Password length validation MUST occur before hashing to prevent bcrypt limitations from causing failures

### X. Task Management UI/UX Principles (NON-NEGOTIABLE)
For Phase II and beyond where task management UI is enhanced:
- Each task MUST have an Edit button to update title and description
- Each task MUST have a Delete button to remove from database with confirmation
- Edit functionality MUST provide inline editing capability with Save/Cancel buttons
- Delete functionality MUST show confirmation dialog before permanent removal
- Both Edit and Delete buttons MUST be positioned next to each task in the UI
- All CRUD operations (Create, Read, Update, Delete) MUST sync with NeonDB
- Existing functionality (add, list, complete tasks) MUST NOT be modified when adding Edit/Delete
- UI MUST maintain current design style and animations when adding new functionality
- Loading and error states MUST be properly handled for all Edit/Delete operations
- Backend endpoints MUST follow REST conventions: PUT for updates, DELETE for removals

## Phase I Constraints (Current Phase)

### Technology Stack
- **Language**: Python 3.13+
- **CLI Framework**: argparse (standard library)
- **Storage**: In-memory only (Python dict/list)
- **Testing**: Manual validation (automated tests optional)
- **Platform**: Cross-platform CLI

### Prohibited in Phase I
- ❌ No database (PostgreSQL, SQLite, etc.)
- ❌ No web framework (FastAPI, Flask, Django)
- ❌ No web UI (React, Next.js, HTML)
- ❌ No external APIs or services
- ❌ No file persistence
- ❌ No AI features
- ❌ No authentication/authorization
- ❌ No multi-user support

### Required in Phase I
- ✅ Command-line interface only
- ✅ In-memory storage (data lost on exit)
- ✅ Single process, single user
- ✅ Interactive command loop
- ✅ Basic CRUD operations on tasks
- ✅ Input validation and error handling

## Quality Standards

### Code Quality
- Type hints required for all public interfaces
- Docstrings required for all classes and functions
- Clear variable and function names (no abbreviations unless standard)
- Maximum function length: 50 lines (excluding docstrings)
- Maximum file length: 500 lines

### Performance Standards
- Command response time: < 100ms for up to 1000 tasks
- Memory usage: Reasonable for in-memory storage (no memory leaks)
- Startup time: < 1 second

### Usability Standards
- New users can learn basic commands (add, list, complete) within 5 minutes
- Help command provides clear usage information
- Error messages enable self-correction without external help

## Development Workflow

### Artifact Requirements
Every feature MUST have:
1. **spec.md**: Feature specification with user stories and requirements
2. **plan.md**: Implementation plan with architecture decisions
3. **tasks.md**: Actionable task list with dependencies
4. **contracts/**: API/CLI contracts (where applicable)
5. **data-model.md**: Entity definitions (where applicable)

### Prompt History Records (PHR)
Every user interaction MUST be recorded as a PHR in `history/prompts/`:
- Constitution changes → `history/prompts/constitution/`
- Feature work → `history/prompts/<feature-name>/`
- General work → `history/prompts/general/`

### Architecture Decision Records (ADR)
Significant architectural decisions MUST be documented as ADRs in `history/adr/`:
- Technology stack choices
- Data model design
- API contract design
- Security patterns
- Performance optimization strategies

ADRs require user approval before creation.

## Governance

### Constitution Authority
This constitution supersedes all other practices and preferences. Any deviation requires explicit amendment to this document.

### Amendment Process
1. Identify need for constitutional change
2. Document proposed change with rationale
3. Update constitution with new version number
4. Update Last Amended date
5. Communicate change to all stakeholders

### Compliance Verification
All implementation work MUST verify compliance with:
- Phase constraints (current phase only)
- Task entity invariance
- Spec-driven workflow
- Quality standards
- Technology constraints

**Version**: 1.3.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-09
