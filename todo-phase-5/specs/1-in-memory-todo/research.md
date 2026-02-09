# Phase 0 Research: In-Memory Todo CLI Application

**Feature**: In-Memory Todo Console Application
**Date**: 2026-01-05

## CLI Framework Selection

### Decision: argparse (Python Standard Library)

**Rationale**:
- Included in Python 3.13+ standard library - no external dependency
- Well-documented and widely understood
- Supports subcommands, arguments, and flags naturally
- Generates help messages automatically
- Mature, stable, and battle-tested

**Alternatives Considered**:
- **click**: More features, but requires external dependency. Adds complexity for simple CLI.
- **docopt**: Human-readable syntax, but external dependency and less control.
- **Custom parsing**: More flexibility, but reinvents the wheel and increases maintenance burden.

**Conclusion**: argparse provides sufficient functionality without external dependencies.

## Task ID Generation Strategy

### Decision: Sequential Integers Starting from 1

**Rationale**:
- Simple and human-readable
- Easy to reference in CLI commands
- No external dependencies or libraries required
- O(1) complexity for ID assignment
- Naturally ordered for list display

**Alternatives Considered**:
- **UUIDs**: Universally unique but not human-readable. Overkill for single-user CLI.
- **Random strings**: Unnecessary complexity, difficult for users to reference.
- **Timestamps**: Technically unique but not user-friendly for CLI interaction.

**Conclusion**: Sequential integers provide optimal balance of simplicity and usability.

## In-Memory Storage Structure

### Decision: Python Dictionary with ID as Key

**Rationale**:
- O(1) lookup complexity by task ID
- Simple and idiomatic Python
- Easy to implement and maintain
- Naturally supports delete operations
- No external libraries required

**Alternatives Considered**:
- **List**: O(n) lookup complexity. Acceptable for small datasets but inefficient.
- **Custom index structures**: Overengineering for Phase I scope.

**Conclusion**: Dictionary provides optimal performance for ID-based operations.

## Command Pattern

### Decision: Subcommand-Based (add, list, update, delete, complete)

**Rationale**:
- Intuitive and discoverable
- Follows common CLI patterns (e.g., git add, git commit)
- Maps directly to user stories
- argparse handles subcommands natively
- Easy to extend with new commands in future phases

**Alternatives Considered**:
- **Positional arguments with flags**: More compact but less discoverable.
- **Menu-driven interface**: Too complex, not typical CLI pattern.

**Conclusion**: Subcommands align with user mental model and best practices.

## Status Display Format

### Decision: Short bracketed indicators (`[P]` pending, `[IP] in_progress`, `[C] completed`)

**Rationale**:
- Universally readable across terminals
- Concise and visually distinct
- Easy to parse for users
- No special character encoding issues

**Alternatives Considered**:
- **Full text**: "Task (pending): Buy groceries" - Too verbose, reduces readability.
- **Color codes**: Not portable across all terminals, adds complexity.
- **Icons/Emojis**: Not universally supported across terminals, encoding issues.

**Conclusion**: Short bracketed indicators are universally readable and concise.

## Command Input Loop

### Decision: Interactive prompt with read-eval-print loop (REPL)

**Rationale**:
- Familiar to CLI users
- Enables multiple operations without restarting
- Allows incremental task management
- Simple to implement with standard library

**Alternatives Considered**:
- **Single-command mode**: Users must restart application for each operation. Poor user experience.
- **File-based input**: Overkill for interactive CLI, violates typical CLI patterns.

**Conclusion**: Interactive REPL provides best user experience for task management.

## Error Handling Strategy

### Decision: Explicit error messages with graceful continuation

**Rationale**:
- Users can self-correct without assistance
- Application continues after errors
- Clear, actionable error messages
- No application crashes on invalid input

**Alternatives Considered**:
- **Exceptions with stack traces**: Too technical for end users. Violates NFR-003.
- **Silent failures**: Users don't know what went wrong. Unacceptable.

**Conclusion**: Explicit, human-readable error messages support NFR-003 and enable user self-correction.

## Summary

All technology choices align with:
- Phase I constraints (in-memory, CLI-only, no external dependencies)
- Non-functional requirements (simplicity, clarity, performance)
- Constitution principles (minimal complexity, no premature optimization)

No dependencies outside Python 3.13+ standard library are required.
