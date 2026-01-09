<!--
  Sync Impact Report
  ===================
  Version change: N/A → 1.0.0 (Initial constitution creation)
  Modified principles: N/A (new constitution)
  Added sections:
    - Core Principles (7 principles)
    - Phase Evolution Roadmap
    - Technical Constraints
    - Development Workflow
    - Governance
  Removed sections: N/A
  Templates requiring updates:
    - ✅ plan-template.md: Aligned with SDD and no manual coding principles
    - ✅ spec-template.md: Aligned with SDD requirements
    - ✅ tasks-template.md: Aligned with task-driven workflow
  Follow-up TODOs: None
-->

# The Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development (SDD) - NON-NEGOTIABLE

All development work MUST originate from an approved specification document.

No code shall be written without a corresponding feature specification that defines:
- User scenarios and acceptance criteria
- Functional requirements
- Success criteria
- Data entities and their relationships

Changes to implementation MUST be made by refining the specification, not by directly editing code.
The spec is the source of truth; code is a derivative artifact.

**Rationale**: Ensures alignment with business intent, enables traceability, prevents drift from requirements, and supports the phase-based evolution strategy.

### II. No Manual Coding Rule

Code generation is permitted ONLY after specifications are approved and complete.

Manual coding without a specification is PROHIBITED. All code changes MUST flow through this workflow:

1. User provides feature description
2. `/sp.specify` creates feature specification
3. `/sp.plan` generates architectural design
4. `/sp.tasks` creates actionable task list
5. `/sp.implement` executes tasks based on approved artifacts

Direct code editing bypassing this workflow violates this constitution.

**Rationale**: Enforces SDD discipline, prevents implementation-first thinking, ensures architectural alignment, and maintains artifact traceability.

### III. Phase-Based Evolution Strategy

The project evolves through distinct phases, each building on previous foundations:

- **Phase I (Current)**: CLI-only in-memory application
  - Command-line interface
  - In-memory storage only
  - No database, no web framework
  - Basic CRUD operations on todos

- **Phase II**: Web Application
  - Web UI interface
  - Persistent storage (database integration)
  - REST API endpoints
  - Multi-user support

- **Phase III**: AI-Enhanced Application
  - AI-powered features
  - Smart task recommendations
  - Natural language processing
  - Advanced categorization

- **Phase IV**: Kubernetes Deployment
  - Containerized deployment
  - Microservices architecture
  - Scalable infrastructure
  - Production-grade operations

Each phase MUST be complete and tested before proceeding to the next. Phase boundaries are immutable once crossed.

**Rationale**: Gradual complexity increase, validated foundations at each stage, reduces technical debt, enables learning and iteration.

### IV. Task Entity Invariance

All Task entities MUST maintain a future-proof structure across all phases:

Required attributes:
- `id`: Unique identifier (string or integer)
- `title`: Task description (string)
- `status`: Task state (enum: "pending" | "in_progress" | "completed")

Additional attributes MAY be added in future phases, but the core structure MUST remain backward-compatible.

Phase I (CLI) will use only the core attributes. Later phases (Web, AI, K8s) will extend, not replace, this structure.

**Rationale**: Ensures data portability across phases, prevents breaking changes, allows seamless migration as complexity grows.

### V. Code Generation Gateway

Implementation code MUST NOT be generated until ALL of the following are approved:

1. Feature specification (spec.md) exists and is complete
2. Implementation plan (plan.md) is generated and reviewed
3. Task list (tasks.md) is created and validated
4. All user stories have independent test plans
5. Constitution compliance check passes

The `/sp.implement` command is the ONLY authorized entry point for code generation.

**Rationale**: Ensures all design decisions are captured, prevents premature implementation, maintains architectural integrity, guarantees traceability.

### VI. Spec-Refinement Workflow for Changes

ALL changes to the system MUST be made through specification refinement:

For bugs:
1. Update spec.md to clarify the expected behavior
2. Update acceptance criteria if needed
3. Re-run `/sp.tasks` to update task list
4. `/sp.implement` to regenerate affected code

For new features:
1. Follow standard SDD workflow (spec → plan → tasks → implement)

For optimizations/refactoring:
1. Document the change in plan.md with rationale
2. Update tasks.md to reflect new tasks
3. `/sp.implement` to regenerate

Direct code editing to fix bugs or add features is PROHIBITED.

**Rationale**: Maintains spec as source of truth, prevents code-spec drift, enables full traceability of changes, supports reproducible builds.

### VII. Phase I Constraints (Non-Negotiable)

Phase I development MUST adhere strictly to these constraints:

- Python 3.13+ only
- CLI application exclusively
- In-memory storage (no database, no files)
- No web framework or HTTP server
- No AI features or external APIs
- Single process, single user
- Data lost on process termination

Violating these constraints in Phase I invalidates the evolutionary roadmap and requires restarting the phase.

**Rationale**: Establishes minimal viable foundation, focuses on core logic without complexity, validates basic user needs, ensures clean slate for future phases.

## Phase Evolution Roadmap

### Phase I: In-Memory CLI (Current)
**Objective**: Validate core todo functionality with minimal complexity

**Constraints**:
- CLI interface only
- In-memory storage
- Single user, single process
- Basic CRUD operations

**Exit Criteria**:
- All P1 user stories working
- CLI commands tested and documented
- Core data model validated

### Phase II: Web Application
**Objective**: Multi-user persistence and web interface

**Constraints**:
- Web UI framework
- Persistent database
- REST API
- Authentication

**Entry Criteria**:
- Phase I complete and validated
- Task model stable and frozen
- Technical design approved

### Phase III: AI-Enhanced
**Objective**: Intelligent task management

**Constraints**:
- AI service integration
- Natural language processing
- Smart recommendations

**Entry Criteria**:
- Phase II production-ready
- Data quality validated
- AI requirements specified

### Phase IV: Kubernetes Deployment
**Objective**: Production-grade infrastructure

**Constraints**:
- Microservices architecture
- Container orchestration
- Auto-scaling
- Monitoring/observability

**Entry Criteria**:
- Phase III feature-complete
- Performance benchmarks met
- Security review complete

## Technical Constraints

### Language & Framework
- **Language**: Python 3.13+
- **Package Management**: pip/pyproject.toml
- **CLI Framework**: argparse or click (to be decided in Phase I plan)
- **Testing**: pytest (if tests are requested in spec)

### Storage Architecture
- **Phase I**: In-memory only (dict/list structures)
- **Phase II+**: To be specified in respective phase plans
- No database migrations or persistence until Phase II

### Code Organization
- Follow implementation plan structure from plan.md
- Single module/project in Phase I
- Clear separation of models, services, CLI interface

### Quality Standards
- Type hints required on all public interfaces
- Docstrings on all functions/classes
- Error handling explicit and documented
- Logging via standard library (no external logging frameworks)

## Development Workflow

### Standard Feature Development Flow

1. **Feature Request**: User provides natural language description
2. **Specification**: `/sp.specify` creates spec.md with user stories, requirements, success criteria
3. **Clarification**: `/sp.clarify` identifies gaps and refines spec if needed
4. **Planning**: `/sp.plan` generates plan.md with architecture, data model, contracts
5. **Task Generation**: `/sp.tasks` creates tasks.md with actionable steps
6. **Implementation**: `/sp.implement` executes tasks sequentially
7. **Validation**: Verify against spec acceptance criteria
8. **PHR Recording**: `/sp.phr` documents the interaction

### Bug Fix Flow

1. Identify bug symptom and expected behavior
2. Update spec.md to clarify correct behavior
3. Update plan.md if architectural change needed
4. Regenerate tasks.md with `/sp.tasks`
5. Implement with `/sp.implement`
6. Validate fix against updated acceptance criteria

### Refactoring Flow

1. Document refactoring rationale in plan.md
2. Create or update tasks.md with refactoring tasks
3. Execute with `/sp.implement`
4. Validate no regression in acceptance criteria

## Governance

### Amendment Process

Constitution amendments require:

1. Clear rationale for change
2. Impact analysis on existing phases
3. Version update (semantic versioning)
4. Approval from project owner
5. Propagation to dependent templates

### Versioning Policy

- **MAJOR**: Breaking changes to core principles (e.g., removing SDD, adding manual coding)
- **MINOR**: New principles or significant expansion of existing ones
- **PATCH**: Clarifications, wording improvements, non-substantive changes

### Compliance Review

All artifacts must verify constitution compliance:

- **spec.md**: Must include user scenarios, acceptance criteria, entities
- **plan.md**: Must include Constitution Check section, must justify violations
- **tasks.md**: Must reference specific user stories, must be dependency-ordered
- **Implementation**: Must be generated via `/sp.implement`, never manual

### Phase Gate Enforcement

Each phase transition requires:

1. Exit criteria of current phase met
2. Entry criteria of next phase satisfied
3. Architecture decision records for new technologies
4. Updated constitution if phase requires new constraints

### Authority

This constitution supersedes all other practices and guidelines.

In case of conflict:
1. Constitution > Templates > Command docs > Ad-hoc decisions
2. User requirements override everything (via specification, not direct edits)

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05
