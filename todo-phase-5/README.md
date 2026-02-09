# In-Memory Todo Console Application - Phase I

Phase I of "The Evolution of Todo" project - a command-line interface todo application with in-memory storage.

## Overview

This is a minimal viable product (MVP) that provides basic CRUD operations on tasks through a command-line interface. All data is stored in-memory and lost when the application exits.

## Features

- **Add tasks**: Create new tasks with titles
- **List tasks**: View all tasks with IDs, titles, and status indicators
- **Update tasks**: Modify task titles
- **Complete tasks**: Mark tasks as completed, in progress, or pending
- **Delete tasks**: Remove tasks from the list
- **Help command**: Display all available commands
- **Exit**: Gracefully terminate the application

## Requirements

- Python 3.13 or higher
- No external dependencies (uses standard library only)

## Quick Start

### Running the Application

```bash
python src/cli/main.py
```

### Basic Usage

```bash
# Add a task
> add Buy groceries
Task added: 1 Buy groceries

# List all tasks
> list
Tasks:
1 [P] Buy groceries

# Mark task as complete
> complete 1
Task 1 marked as completed

# List again
> list
Tasks:
1 [C] Buy groceries

# Exit
> exit
Goodbye!
```

## Commands

| Command | Description |
|---------|-------------|
| `add <title>` | Add a new task |
| `list` | Display all tasks |
| `update <id> <title>` | Update a task title |
| `complete <id>` | Mark task as completed |
| `in_progress <id>` | Mark task as in progress |
| `pending <id>` | Mark task as pending |
| `delete <id>` | Delete a task |
| `help` | Show command list |
| `exit` | Exit the application |

## Task Status Indicators

- `[P]` - Pending (not started)
- `[IP]` - In Progress (working on it)
- `[C]` - Completed (finished)

## Important Notes

⚠️ **Data Persistence**: This is Phase I - data is stored in-memory only. When you close the application or type `exit`, **all tasks are lost**. This is intentional and will be addressed in Phase II.

⚠️ **Single User**: This is a single-user, single-process application.

## Project Structure

```
src/
├── models/
│   └── task.py          # Task entity and validation
├── services/
│   └── task_service.py  # Business logic and in-memory storage
└── cli/
    └── main.py          # CLI entry point and command handling

specs/1-in-memory-todo/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan
├── tasks.md             # Task breakdown
├── data-model.md        # Task entity definition
├── contracts/cli-commands.md  # CLI command specifications
├── research.md          # Technology decisions
└── quickstart.md        # User guide

.specify/memory/
└── constitution.md        # Project governance
```

## Roadmap

- **Phase I (Current)**: CLI-only in-memory application
- **Phase II**: Web Application with persistent database
- **Phase III**: AI-Enhanced Application
- **Phase IV**: Kubernetes Deployment

## Development

This project follows Spec-Driven Development (SDD) as defined in the [Project Constitution](.specify/memory/constitution.md).

### Workflow

1. `/sp.specify` - Create feature specification
2. `/sp.plan` - Generate architectural design
3. `/sp.tasks` - Create actionable task list
4. `/sp.implement` - Execute implementation

## License

See LICENSE file for details.
