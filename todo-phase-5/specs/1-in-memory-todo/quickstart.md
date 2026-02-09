# Quick Start Guide

**Feature**: In-Memory Todo Console Application
**Phase**: I - CLI Application
**Date**: 2026-01-05

## Running the Application

### Prerequisites

- Python 3.13 or higher installed
- Command-line terminal or shell

### Launch the Application

```bash
python src/cli/main.py
```

You will see the command prompt:
```
>
```

## Basic Usage

### Step 1: Add Your First Task

Create a task by typing `add` followed by your task title:

```
> add Buy groceries
Task added: 1 Buy groceries
```

### Step 2: View All Tasks

See all your tasks with the `list` command:

```
> list
Tasks:
1 [P] Buy groceries
```

### Step 3: Mark a Task as Complete

When you finish a task, mark it as complete using the task ID:

```
> complete 1
Task 1 marked as completed
```

### Step 4: View Updated Tasks

Check your tasks again to see the status change:

```
> list
Tasks:
1 [C] Buy groceries
```

## All Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <title>` | Create a new task | `add Call mom` |
| `list` | Display all tasks | `list` |
| `update <id> <title>` | Change a task title | `update 1 Call dad` |
| `complete <id>` | Mark task as done | `complete 1` |
| `in_progress <id>` | Mark task as started | `in_progress 1` |
| `pending <id>` | Reset task to pending | `pending 1` |
| `delete <id>` | Remove a task | `delete 1` |
| `help` | Show command list | `help` |
| `exit` | Quit the app | `exit` |

## Status Indicators

Tasks display their status with short codes:

- `[P]` - Pending (not started)
- `[IP]` - In Progress (working on it)
- `[C]` - Completed (finished)

## Example Session

Here's a complete example of using the application:

```
> add Buy groceries
Task added: 1 Buy groceries

> add Call mom
Task added: 2 Call mom

> add Write report
Task added: 3 Write report

> list
Tasks:
1 [P] Buy groceries
2 [P] Call mom
3 [P] Write report

> in_progress 1
Task 1 marked as in progress

> list
Tasks:
1 [IP] Buy groceries
2 [P] Call mom
3 [P] Write report

> complete 1
Task 1 marked as completed

> delete 3
Task 3 deleted

> list
Tasks:
1 [C] Buy groceries
2 [P] Call mom

> update 2 Call dad
Task 2 updated: Call dad

> list
Tasks:
1 [C] Buy groceries
2 [P] Call dad

> exit
Goodbye!
```

## Common Tasks

### Create Multiple Tasks Quickly

```
> add Buy groceries
Task added: 1 Buy groceries
> add Call mom
Task added: 2 Call mom
> add Write report
Task added: 3 Write report
```

### Track Task Progress

```
> in_progress 1
Task 1 marked as in progress
> complete 1
Task 1 marked as completed
```

### Fix a Mistake

```
> update 1 Buy milk
Task 1 updated: Buy milk
```

### Remove Unwanted Tasks

```
> delete 5
Task 5 deleted
```

## Tips

- Task IDs are sequential numbers (1, 2, 3...)
- Use `list` frequently to see task IDs
- Task titles can contain spaces and special characters
- All data is lost when you exit the application (in-memory only)
- Type `help` anytime to see all commands

## Important Notes

⚠️ **Data Persistence**: This application stores tasks in memory only. When you close the application or type `exit`, **all tasks are lost**. This is intentional for Phase I.

⚠️ **Case Sensitivity**: Commands are case-sensitive. Use lowercase: `add`, `list`, `complete`, etc.

⚠️ **Task IDs**: If you delete a task, its ID is **not reused**. The next task gets the next sequential ID.

## Getting Help

If you forget a command, type `help`:

```
> help
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

## Error Recovery

If you see an error message:

1. Read the error to understand what went wrong
2. Correct your command based on the error message
3. The application continues; you don't need to restart

Example error recovery:
```
> complete
Error: Missing task ID. Usage: complete <id>
> complete 1
Task 1 marked as completed
```

## What's Next?

After you complete Phase I, future phases will add:
- **Phase II**: Web interface and persistent database storage
- **Phase III**: AI-powered task recommendations
- **Phase IV**: Kubernetes deployment for production use

For more details, see the [Project Constitution](../../.specify/memory/constitution.md).
