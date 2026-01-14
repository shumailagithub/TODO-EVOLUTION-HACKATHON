# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `/specs/1-in-memory-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-commands.md

**Tests**: Tests are NOT included - tests were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan (src/, src/models/, src/services/, src/cli/)
- [X] T002 Create pyproject.toml for Python 3.13+ configuration
- [X] T003 [P] Create __init__.py files in src/, src/models/, src/services/, src/cli/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Task model class in src/models/task.py with id, title, status attributes (per data-model.md)
- [X] T005 [P] Create TaskStatus enum in src/models/task.py with "pending", "in_progress", "completed" values
- [X] T006 Implement title validation in src/models/task.py (1-200 chars, non-empty, not only whitespace)
- [X] T007 Implement status validation in src/models/task.py (enum values only)
- [X] T008 Create ValidationError exception class in src/models/task.py
- [X] T009 Create TaskService class in src/services/task_service.py with in-memory dictionary storage
- [X] T010 [P] Implement add_task(title) method in TaskService (per FR-001, FR-002, FR-003)
- [X] T011 [P] Implement get_task(id) method in TaskService with ID validation (per FR-010)
- [X] T012 [P] Implement get_all_tasks() method in TaskService returning tasks sorted by ID (per FR-004)
- [X] T013 [P] Implement update_task(id, title) method in TaskService with title validation (per FR-007, FR-009)
- [X] T014 [P] Implement set_task_status(id, status) method in TaskService (per FR-005, FR-006)
- [X] T015 [P] Implement delete_task(id) method in TaskService (per FR-008, FR-010)
- [X] T016 Implement task_count() method in TaskService
- [X] T017 Initialize in-memory storage dictionary and ID counter in TaskService __init__

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with titles that get unique IDs and "pending" status.

**Independent Test**: Add task with title "Buy groceries", then view list to verify task appears with unique ID and status "pending".

- [X] T018 Create CLI argument parser using argparse in src/cli/main.py (per research.md)
- [X] T019 [P] Implement add command argument parser in src/cli/main.py (add <title>)
- [X] T020 Implement add command handler in src/cli/main.py calling TaskService.add_task()
- [X] T021 Add success output for add command: "Task added: [ID] [title]" (per cli-commands.md)
- [X] T022 Add error handling for empty title in add command (per FR-009)
- [X] T023 Add error handling for whitespace-only title in add command (per cli-commands.md)
- [X] T024 Add error handling for title length >200 characters in add command (per cli-commands.md)
- [X] T025 Create command prompt "> " in src/cli/main.py

**Checkpoint**: At this point, users can add tasks. MVP is partially functional.

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to see all tasks with IDs, titles, and status indicators.

**Independent Test**: Add multiple tasks, then use list command to verify all tasks appear with correct IDs, titles, and statuses.

- [X] T026 [P] Implement list command argument parser in src/cli/main.py (list)
- [X] T027 Implement list command handler in src/cli/main.py calling TaskService.get_all_tasks()
- [X] T028 Format task display with status indicators: [P] pending, [IP] in_progress, [C] completed (per cli-commands.md)
- [X] T029 Display "No tasks found." message when no tasks exist (per FR-012, cli-commands.md)
- [X] T030 Sort tasks by ID in ascending order for display (per data-model.md)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. MVP is COMPLETE!

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P2)

**Goal**: Enable users to change task status to "completed", "in_progress", or "pending".

**Independent Test**: Add task, mark it as complete using its ID, then view list to verify status changed to "completed".

- [X] T031 [P] Implement complete command argument parser in src/cli/main.py (complete <id>)
- [X] T032 [P] Implement in_progress command argument parser in src/cli/main.py (in_progress <id>)
- [X] T033 [P] Implement pending command argument parser in src/cli/main.py (pending <id>)
- [X] T034 Implement complete command handler calling TaskService.set_task_status(id, "completed")
- [X] T035 Implement in_progress command handler calling TaskService.set_task_status(id, "in_progress")
- [X] T036 Implement pending command handler calling TaskService.set_task_status(id, "pending")
- [X] T037 Add success output for complete command: "Task [ID] marked as completed" (per cli-commands.md)
- [X] T038 Add success output for in_progress command: "Task [ID] marked as in progress" (per cli-commands.md)
- [X] T039 Add success output for pending command: "Task [ID] marked as pending" (per cli-commands.md)
- [X] T040 Add error handling for invalid task ID (non-integer) in status commands (per cli-commands.md)
- [X] T041 Add error handling for non-existent task ID in status commands (per FR-010, cli-commands.md)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently.

---

## Phase 6: User Story 4 - Update a Task (Priority: P2)

**Goal**: Enable users to change task titles by referencing task ID.

**Independent Test**: Add task, update its title using task ID, then view list to verify title changed while ID and status remain unchanged.

- [X] T042 [P] Implement update command argument parser in src/cli/main.py (update <id> <new_title>)
- [X] T043 Implement update command handler calling TaskService.update_task(id, title)
- [X] T044 Add success output for update command: "Task [ID] updated: [new_title]" (per cli-commands.md)
- [X] T045 Add error handling for empty new title in update command (per cli-commands.md)
- [X] T046 Add error handling for whitespace-only new title in update command (per cli-commands.md)
- [X] T047 Add error handling for invalid task ID in update command (per cli-commands.md)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently.

---

## Phase 7: User Story 5 - Delete a Task (Priority: P3)

**Goal**: Enable users to remove tasks permanently from the list.

**Independent Test**: Add multiple tasks, delete one using its ID, then view list to verify deleted task no longer appears and remaining tasks are intact.

- [X] T048 [P] Implement delete command argument parser in src/cli/main.py (delete <id>)
- [X] T049 Implement delete command handler calling TaskService.delete_task(id)
- [X] T050 Add success output for delete command: "Task [ID] deleted" (per cli-commands.md)
- [X] T051 Add error handling for invalid task ID in delete command (per cli-commands.md)

**Checkpoint**: At this point, ALL user stories should be independently functional.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T052 [P] Implement help command argument parser in src/cli/main.py (help)
- [X] T053 [P] Implement help command handler displaying all commands (per FR-014, cli-commands.md)
- [X] T054 [P] Implement exit command argument parser in src/cli/main.py (exit)
- [X] T055 [P] Implement exit command handler displaying "Goodbye!" and terminating application (per FR-015, cli-commands.md)
- [X] T056 Create main CLI read-eval-print loop (REPL) in src/cli/main.py (per research.md, quickstart.md)
- [X] T057 Add usage information to error messages for commands with missing arguments (per cli-commands.md)
- [X] T058 Add type hints to all public interfaces (per constitution quality standards)
- [X] T059 Add docstrings to all functions and classes (per constitution quality standards)
- [X] T060 Add graceful error handling - application continues after errors (per research.md, NFR-003)
- [X] T061 Verify all error messages are clear and human-readable (per NFR-003, NFR-004)
- [X] T062 [P] Validate performance: Create 1000 tasks and verify command response time < 100ms (per NFR-001)
- [X] T063 [P] Validate usability: Test that new users can learn add, list, complete commands within 5 minutes (per NFR-002)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed sequentially in priority order (P1 → P2 → P2 → P3)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (Add Task - P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (View Tasks - P1)**: Can start after Foundational (Phase 2) - Depends on US1 for data, but independently testable
- **User Story 3 (Mark Complete - P2)**: Depends on US1 (tasks exist) and US2 (view to verify) - Can be tested independently
- **User Story 4 (Update Task - P2)**: Depends on US1 (tasks exist) and US2 (view to verify) - Can be tested independently
- **User Story 5 (Delete Task - P3)**: Depends on US1 (tasks exist) and US2 (view to verify) - Can be tested independently

### Within Each Phase

- **Setup**: Tasks T002 and T003 can run in parallel (different files)
- **Foundational**: Tasks T005, T010, T011, T012, T013, T014, T015 can run in parallel (different methods)
- **User Story 1**: Tasks T018, T019, T025 are file structure tasks that can be parallelized
- **User Story 2**: Task T026 can run in parallel with later US1 tasks
- **User Story 3**: Tasks T031, T032, T033 can run in parallel (different command parsers)
- **User Story 4**: Task T042 can run in parallel with earlier US3 tasks
- **User Story 5**: Task T048 can run in parallel with earlier US4 tasks
- **Polish**: Tasks T052, T053, T054, T055 can all run in parallel (different command handlers)

### Parallel Opportunities

- All Setup tasks marked [P] (T002, T003) can run in parallel
- Foundational tasks marked [P] (T005, T010-T015) can run in parallel within Phase 2
- User Story 3 tasks marked [P] (T031-T033) can run in parallel within Phase 5
- User Story 4 tasks marked [P] (T042) can run in parallel with Phase 5 tasks
- User Story 5 tasks marked [P] (T048) can run in parallel with Phase 6 tasks
- Polish tasks marked [P] (T052-T055) can all run in parallel within Phase 8

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T017) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T018-T025)
4. Complete Phase 4: User Story 2 (T026-T030)
5. **STOP and VALIDATE**: Test add and list commands independently - MVP is complete!
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Add Task) → Test independently → Add task works (Partial MVP)
3. Add User Story 2 (View Tasks) → Test independently → MVP is COMPLETE!
4. Add User Story 3 (Mark Complete) → Test independently → Task lifecycle management
5. Add User Story 4 (Update Task) → Test independently → Task editing capability
6. Add User Story 5 (Delete Task) → Test independently → Full CRUD complete
7. Add Phase 8 (Polish) → Test all commands → Production-ready Phase I

Each story adds value without breaking previous stories.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included as they were not requested in the spec
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All commands must follow cli-commands.md specifications
- Task model must follow data-model.md specifications
- Error messages must match cli-commands.md exactly

---

## Task Count Summary

- **Phase 1 (Setup)**: 3 tasks (T001-T003)
- **Phase 2 (Foundational)**: 14 tasks (T004-T017)
- **Phase 3 (US1 - Add Task)**: 8 tasks (T018-T025)
- **Phase 4 (US2 - View Tasks)**: 5 tasks (T026-T030)
- **Phase 5 (US3 - Mark Complete)**: 11 tasks (T031-T041)
- **Phase 6 (US4 - Update Task)**: 6 tasks (T042-T047)
- **Phase 7 (US5 - Delete Task)**: 4 tasks (T048-T051)
- **Phase 8 (Polish & Validation)**: 12 tasks (T052-T063)

**Total**: 63 tasks
