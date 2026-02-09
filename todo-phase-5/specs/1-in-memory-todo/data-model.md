# Data Model: Task Entity

**Feature**: In-Memory Todo Console Application
**Date**: 2026-01-05

## Overview

The Task entity represents a single todo item with three core attributes. This structure is designed to be future-proof and backward-compatible across all phases.

## Task Entity

### Attributes

| Attribute | Type | Description | Constraints |
|------------|-------|-------------|--------------|
| `id` | `int` | Unique identifier for the task | Auto-incrementing, starts from 1, unique across all tasks |
| `title` | `str` | Human-readable task description | 1-200 characters, non-empty, cannot be only whitespace |
| `status` | `enum` | Current state of the task | One of: "pending", "in_progress", "completed" |

### Status Enum

The TaskStatus enum defines three valid states:

| Value | Display Indicator | Description |
|-------|-----------------|-------------|
| `pending` | `[P]` | Task is not yet started |
| `in_progress` | `[IP]` | Task is currently being worked on |
| `completed` | `[C]` | Task has been finished |

### Default Values

- `id`: Auto-assigned by TaskService on creation (incrementing counter)
- `title`: User-provided, validated during Task creation
- `status`: Defaults to `pending` on creation

## Validation Rules

### Title Validation

A title is valid if:
- Not empty or None
- Not only whitespace (after stripping)
- Length is between 1 and 200 characters (inclusive)
- Contains any printable ASCII or Unicode characters

### ID Validation

A task ID is valid if:
- Is a positive integer (1, 2, 3, ...)
- Exists in the task storage

### Status Validation

A status is valid if:
- Is one of the three enum values: "pending", "in_progress", "completed"

## State Transitions

Valid status transitions:

| From | To | Allowed? | Reason |
|------|-----|-----------|---------|
| `pending` | `in_progress` | ✅ Yes | User started working on task |
| `pending` | `completed` | ✅ Yes | User finished task without tracking progress |
| `in_progress` | `pending` | ✅ Yes | User postponed task |
| `in_progress` | `completed` | ✅ Yes | User finished task |
| `completed` | `pending` | ✅ Yes | User re-opened task |
| `completed` | `in_progress` | ✅ Yes | User re-opened and resumed task |

All transitions are allowed. The system does not restrict task flow to support flexible task management.

## Immutability

### Immutable After Creation

Once a Task object is created:
- `id` cannot be changed (immutable)
- `title` can be changed via update operation (replaces Task with new Task object)
- `status` can be changed via status update operation (replaces Task with new Task object)

**Rationale**: In-memory storage is a dictionary. When `id` changes, the key changes. When `title` or `status` changes, the value is replaced. This ensures TaskService maintains a single source of truth.

## Storage Representation

In TaskService, tasks are stored as:

```text
{
    id: Task(id=1, title="Buy groceries", status="pending"),
    id: Task(id=2, title="Call mom", status="in_progress"),
    id: Task(id=3, title="Write report", status="completed")
}
```

Where:
- Dictionary key = task ID (integer)
- Dictionary value = Task object (with id, title, status)

## Future-Proofing

### Phase I (Current)

Only core attributes are used: `id`, `title`, `status`.

### Phase II (Web Application)

Core attributes remain. Additional attributes MAY be added:
- `created_at`: timestamp of task creation
- `updated_at`: timestamp of last modification
- `user_id`: identifier for multi-user support
- `due_date`: optional deadline

### Phase III (AI-Enhanced)

Core attributes remain. Additional attributes MAY be added:
- `category`: AI-assigned category
- `priority`: AI-suggested priority level
- `estimated_time`: AI-predicted duration

### Phase IV (Kubernetes)

Core attributes remain unchanged. All previous attributes preserved.

**Invariant**: The core structure (`id`, `title`, `status`) is never removed or modified, ensuring backward compatibility across all phases.

## Example Task Objects

```text
Task(id=1, title="Buy groceries", status="pending")
Task(id=2, title="Call mom", status="in_progress")
Task(id=3, title="Write report", status="completed")
```
