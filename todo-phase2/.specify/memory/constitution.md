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

**Version**: 1.0.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-07
