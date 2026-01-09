# Implementation Plan: In-Memory Todo Console Application

**Branch**: `1-in-memory-todo` | **Date**: 2026-01-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-in-memory-todo/spec.md`

## Summary

Phase I is an in-memory CLI todo application that provides basic CRUD operations on tasks. Users can add, view, update, complete, and delete tasks through a command-line interface. All data is stored in-memory and lost when the application exits. This serves as the foundation for future phases that will add persistence, web UI, AI features, and Kubernetes deployment.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: argparse (standard library) - no external dependencies required
**Storage**: In-memory using Python dictionary/list structures
**Testing**: pytest (optional - tests not requested in spec)
**Target Platform**: Command-line interface (CLI) - cross-platform
**Project Type**: Single project (CLI application)
**Performance Goals**: Command response within 100ms for up to 1000 tasks
**Constraints**: In-memory only, no persistence, no external services, single process, single user
**Scale/Scope**: Up to 1000 tasks, single user session, no concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Constraints Compliance

✅ **Python 3.13+**: Planning for Python 3.13+ - COMPLIANT
✅ **CLI Application Only**: Design uses argparse for CLI interface - COMPLIANT
✅ **In-Memory Storage**: Uses Python dict/list structures - COMPLIANT
✅ **No Database**: No external database - COMPLIANT
✅ **No Web Framework**: No HTTP server or web framework - COMPLIANT
✅ **No AI Features**: No AI or external APIs - COMPLIANT
✅ **Single Process/Single User**: Interactive CLI loop - COMPLIANT
✅ **Data Lost on Exit**: In-memory storage ensures this - COMPLIANT

### SDD Compliance

✅ **Spec-Driven**: Implementation will follow spec.md - COMPLIANT
✅ **No Manual Coding**: All code via `/sp.implement` command - COMPLIANT
✅ **Task Entity Invariance**: Core structure (id, title, status) preserved - COMPLIANT

**RESULT**: All gates pass. No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/1-in-memory-todo/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Technology research (Phase 0 output)
├── data-model.md        # Task entity definition (Phase 1 output)
├── quickstart.md        # CLI usage guide (Phase 1 output)
└── contracts/           # Command contracts (Phase 1 output)
    └── cli-commands.md  # CLI command specifications
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task entity and validation
├── services/
│   └── task_service.py  # Business logic for task operations
└── cli/
    └── main.py          # CLI entry point and command handling
```

**Structure Decision**: Single project structure chosen because Phase I is a CLI application without backend/frontend separation. The models/ directory holds the Task entity, services/ contains business logic, and cli/ handles user interaction. This separation enables easy extraction to microservices in Phase IV.

## Phase 0: Research

Research completed and documented in [research.md](./research.md).

Key decisions:
- CLI framework: argparse (standard library)
- Task ID generation: Sequential integers starting from 1
- Command pattern: Subcommand-based (add, list, update, delete, complete)
- Status display: Short indicators (P for pending, IP for in_progress, C for completed)

## Phase 1: Design

### Data Model

Task entity definition in [data-model.md](./data-model.md):

```text
Task
├── id: int (sequential, auto-incrementing, unique)
├── title: str (1-200 characters, non-empty)
└── status: enum ("pending" | "in_progress" | "completed")
```

### CLI Commands

Command specifications in [contracts/cli-commands.md](./contracts/cli-commands.md):

Available commands:
- `add <title>` - Create a new task
- `list` - Display all tasks
- `update <id> <new_title>` - Update task title
- `complete <id>` - Mark task as completed
- `pending <id>` - Mark task as pending
- `in_progress <id>` - Mark task as in_progress
- `delete <id>` - Delete a task
- `help` - Display help information
- `exit` - Exit the application

### CLI Loop Behavior

The application runs an interactive command loop:

1. Display command prompt (`> `)
2. Wait for user input
3. Parse command and arguments
4. Validate input
5. Execute corresponding command
6. Display result or error message
7. Loop back to step 1 (unless `exit` command)

### In-Memory Storage Implementation

Tasks are stored in a Python dictionary for O(1) lookups by ID:

```text
storage = {
    1: Task(id=1, title="Buy groceries", status="pending"),
    2: Task(id=2, title="Call mom", status="in_progress"),
    ...
}
```

- Dictionary key = task ID
- Dictionary value = Task object
- Sequential ID counter tracks next available ID
- All operations modify this dictionary
- Dictionary discarded on application exit

### Quick Start Guide

Usage instructions in [quickstart.md](./quickstart.md):

1. Run the application
2. Use `add <title>` to create tasks
3. Use `list` to view tasks
4. Use `complete <id>` to mark tasks complete
5. Use `exit` to quit

## Module Responsibilities

### models/task.py

**Responsibility**: Define the Task entity and enforce validation rules.

**Exports**:
- `Task` class: Immutable data structure with id, title, status
- `TaskStatus` enum: pending, in_progress, completed
- `ValidationError`: Custom exception for validation failures

**Key operations**:
- Task creation with validation
- Status transitions with validation
- String representation for display

### services/task_service.py

**Responsibility**: Implement all business logic for task operations.

**Exports**:
- `TaskService` class: Manages in-memory task storage

**Key operations**:
- `add_task(title)` → Create task with new ID
- `get_task(id)` → Retrieve task by ID
- `get_all_tasks()` → Retrieve all tasks sorted by ID
- `update_task(id, title)` → Update task title
- `set_task_status(id, status)` → Change task status
- `delete_task(id)` → Remove task
- `task_count()` → Return total number of tasks

**State**: In-memory dictionary holding all tasks, ID counter

### cli/main.py

**Responsibility**: Handle user interaction and coordinate application flow.

**Exports**:
- `main()` function: Application entry point

**Key operations**:
- Parse command-line arguments using argparse
- Display command prompt and read user input
- Route commands to TaskService
- Format and display task list
- Display error messages
- Handle graceful exit

**Dependencies**: models (Task), services (TaskService)

## Testing Approach

Given that tests were not explicitly requested in the spec, testing is OPTIONAL and will be handled via manual testing during validation.

If tests were to be added:

**Test Framework**: pytest

**Test Structure**:
- `tests/unit/test_task.py` - Task model validation
- `tests/unit/test_task_service.py` - Service logic
- `tests/integration/test_cli.py` - End-to-end CLI flows

**Test Coverage Goals**:
- All user story acceptance scenarios
- Edge cases (empty inputs, invalid IDs, etc.)
- Error handling paths

## Constitution Re-Check (Post-Design)

### Phase I Constraints Compliance

✅ **Python 3.13+**: Design uses standard library - COMPLIANT
✅ **CLI Application Only**: argparse-based CLI - COMPLIANT
✅ **In-Memory Storage**: Dictionary-based storage - COMPLIANT
✅ **No Database**: No external database - COMPLIANT
✅ **No Web Framework**: No HTTP server - COMPLIANT
✅ **No AI Features**: No AI or external APIs - COMPLIANT
✅ **Single Process/Single User**: Interactive loop - COMPLIANT
✅ **Data Lost on Exit**: In-memory only - COMPLIANT

### Task Entity Invariance

✅ **id**: Integer (can be string in future phases) - COMPLIANT
✅ **title**: String - COMPLIANT
✅ **status**: Enum with required values - COMPLIANT

**RESULT**: All gates pass. Design fully complies with constitution.

## Next Steps

1. Review and approve this plan
2. Run `/sp.tasks` to generate actionable task list
3. Run `/sp.implement` to execute tasks and generate code
4. Validate against spec acceptance criteria
