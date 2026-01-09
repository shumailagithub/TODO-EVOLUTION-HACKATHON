# CLI Command Contracts

**Feature**: In-Memory Todo Console Application
**Date**: 2026-01-05

## Overview

This document defines all CLI commands available in the in-memory todo application. Each command specifies its syntax, behavior, input validation, and output format.

## Command Syntax

All commands follow this pattern:

```
<command> [arguments]
```

Where `<command>` is the action verb and `[arguments]` are optional or required parameters.

## Available Commands

### 1. Add Task

**Command**: `add <title>`

**Description**: Create a new task with the specified title.

**Arguments**:
- `title` (required): The task description. Can contain spaces and special characters.

**Input Validation**:
- Title must not be empty (error: "Error: Task title cannot be empty")
- Title must not be only whitespace (error: "Error: Task title cannot be only whitespace")
- Title length must be 1-200 characters (error: "Error: Task title must be between 1 and 200 characters")

**Success Output**:
```
Task added: [ID] [title]
```

**Examples**:
- `add Buy groceries` → `Task added: 1 Buy groceries`
- `add Call mom` → `Task added: 2 Call mom`

**Error Output**:
- `add` → `Error: Missing task title. Usage: add <title>`
- `add ` (whitespace) → `Error: Task title cannot be only whitespace`

---

### 2. List Tasks

**Command**: `list`

**Description**: Display all tasks in the system, sorted by ID in ascending order.

**Arguments**: None

**Input Validation**: None

**Success Output**:

When tasks exist:
```
Tasks:
1 [P] Buy groceries
2 [IP] Call mom
3 [C] Write report
```

When no tasks exist:
```
No tasks found.
```

**Status Indicators**:
- `[P]` - pending
- `[IP]` - in_progress
- `[C]` - completed

**Examples**:
- `list` (with tasks) → Displays list with ID, status, and title
- `list` (no tasks) → `No tasks found.`

---

### 3. Update Task

**Command**: `update <id> <new_title>`

**Description**: Change the title of an existing task.

**Arguments**:
- `id` (required): The task ID (positive integer)
- `new_title` (required): The new task description. Can contain spaces.

**Input Validation**:
- Task ID must be a positive integer (error: "Error: Invalid task ID. Must be a positive integer.")
- Task ID must exist (error: "Error: Task with ID X not found.")
- New title must not be empty (error: "Error: Task title cannot be empty")
- New title must not be only whitespace (error: "Error: Task title cannot be only whitespace")
- New title length must be 1-200 characters (error: "Error: Task title must be between 1 and 200 characters")

**Success Output**:
```
Task [ID] updated: [new_title]
```

**Examples**:
- `update 1 Buy milk` → `Task 1 updated: Buy milk`
- `update 2 Call dad` → `Task 2 updated: Call dad`

**Error Output**:
- `update` → `Error: Missing task ID and title. Usage: update <id> <new_title>`
- `update 1` → `Error: Missing new title. Usage: update <id> <new_title>`
- `update abc Buy milk` → `Error: Invalid task ID. Must be a positive integer.`
- `update 999 Buy milk` → `Error: Task with ID 999 not found.`

---

### 4. Mark Task as Complete

**Command**: `complete <id>`

**Description**: Set a task's status to "completed".

**Arguments**:
- `id` (required): The task ID (positive integer)

**Input Validation**:
- Task ID must be a positive integer (error: "Error: Invalid task ID. Must be a positive integer.")
- Task ID must exist (error: "Error: Task with ID X not found.")

**Success Output**:
```
Task [ID] marked as completed
```

**Examples**:
- `complete 1` → `Task 1 marked as completed`

**Error Output**:
- `complete` → `Error: Missing task ID. Usage: complete <id>`
- `complete abc` → `Error: Invalid task ID. Must be a positive integer.`
- `complete 999` → `Error: Task with ID 999 not found.`

---

### 5. Mark Task as In Progress

**Command**: `in_progress <id>`

**Description**: Set a task's status to "in_progress".

**Arguments**:
- `id` (required): The task ID (positive integer)

**Input Validation**:
- Task ID must be a positive integer (error: "Error: Invalid task ID. Must be a positive integer.")
- Task ID must exist (error: "Error: Task with ID X not found.")

**Success Output**:
```
Task [ID] marked as in progress
```

**Examples**:
- `in_progress 1` → `Task 1 marked as in progress`

**Error Output**:
- `in_progress` → `Error: Missing task ID. Usage: in_progress <id>`
- `in_progress abc` → `Error: Invalid task ID. Must be a positive integer.`
- `in_progress 999` → `Error: Task with ID 999 not found.`

---

### 6. Mark Task as Pending

**Command**: `pending <id>`

**Description**: Set a task's status to "pending".

**Arguments**:
- `id` (required): The task ID (positive integer)

**Input Validation**:
- Task ID must be a positive integer (error: "Error: Invalid task ID. Must be a positive integer.")
- Task ID must exist (error: "Error: Task with ID X not found.")

**Success Output**:
```
Task [ID] marked as pending
```

**Examples**:
- `pending 1` → `Task 1 marked as pending`

**Error Output**:
- `pending` → `Error: Missing task ID. Usage: pending <id>`
- `pending abc` → `Error: Invalid task ID. Must be a positive integer.`
- `pending 999` → `Error: Task with ID 999 not found.`

---

### 7. Delete Task

**Command**: `delete <id>`

**Description**: Remove a task from the system permanently.

**Arguments**:
- `id` (required): The task ID (positive integer)

**Input Validation**:
- Task ID must be a positive integer (error: "Error: Invalid task ID. Must be a positive integer.")
- Task ID must exist (error: "Error: Task with ID X not found.")

**Success Output**:
```
Task [ID] deleted
```

**Examples**:
- `delete 1` → `Task 1 deleted`

**Error Output**:
- `delete` → `Error: Missing task ID. Usage: delete <id>`
- `delete abc` → `Error: Invalid task ID. Must be a positive integer.`
- `delete 999` → `Error: Task with ID 999 not found.`

---

### 8. Help

**Command**: `help`

**Description**: Display usage information for all commands.

**Arguments**: None

**Success Output**:
```
Available commands:
  add <title>          Add a new task
  list                  List all tasks
  update <id> <title>   Update a task title
  complete <id>         Mark task as completed
  in_progress <id>       Mark task as in progress
  pending <id>           Mark task as pending
  delete <id>            Delete a task
  help                  Show this help message
  exit                  Exit the application
```

---

### 9. Exit

**Command**: `exit`

**Description**: Terminate the application. All data is lost (in-memory only).

**Arguments**: None

**Success Output**:
```
Goodbye!
```

**Note**: After this command, the application terminates and all tasks are lost.

---

## Interactive Loop

The application displays a prompt (`> `) and waits for user input. After each command completes (or fails), the prompt is displayed again. This continues until the `exit` command is entered.

```
> add Buy groceries
Task added: 1 Buy groceries
> list
Tasks:
1 [P] Buy groceries
> complete 1
Task 1 marked as completed
> exit
Goodbye!
```

## Error Handling Principles

1. **Specific Error Messages**: Each error case has a unique, descriptive message.
2. **Usage Information**: Errors include command usage when arguments are missing.
3. **Graceful Continuation**: Errors do not crash the application; the prompt reappears.
4. **No Stack Traces**: Users never see technical exception details.
