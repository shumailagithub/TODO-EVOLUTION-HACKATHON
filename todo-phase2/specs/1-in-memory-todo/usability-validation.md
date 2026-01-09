# NFR-002 Usability Validation Guide

**Requirement**: The system MUST be simple enough for a non-technical user to learn within 5 minutes.

**Measurement Method**: Provide a new user with only the `help` command output. Time how long it takes them to successfully: (1) add a task, (2) view all tasks, (3) mark a task as complete.

## Test Protocol

### Prerequisites
- Python 3.13+ installed
- Terminal/command prompt available
- Timer ready

### Test Steps

1. **Launch the application**:
   ```bash
   cd src
   python cli/main.py
   ```

2. **Provide only this instruction to the test user**:
   > "Type 'help' to see available commands. Your goal is to:
   > 1. Add a task called 'Test task'
   > 2. View all your tasks
   > 3. Mark the task as complete
   >
   > Start the timer now."

3. **Observe the user** (do not provide assistance)

4. **Stop the timer when**:
   - User successfully adds a task
   - User successfully views the task list
   - User successfully marks the task as complete

### Success Criteria

- **PASS**: User completes all three operations within 5 minutes
- **FAIL**: User takes longer than 5 minutes OR cannot complete without assistance

### Expected User Flow

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

> add Test task
Task added: 1 Test task

> list
Tasks:
1 [P] Test task

> complete 1
Task 1 marked as completed

> list
Tasks:
1 [C] Test task
```

### Validation Results

**Test Date**: 2026-01-07

**Manual Testing Required**: This validation requires actual user testing with 3 non-technical users.

**Automated Validation**: The help command output is clear and follows standard CLI patterns. Commands are intuitive and follow common conventions (add, list, complete, delete).

**Design Assessment**:
- ✅ Help command provides clear usage information
- ✅ Commands follow standard CLI patterns (similar to git, npm, etc.)
- ✅ Error messages are human-readable
- ✅ Command syntax is simple (verb + arguments)
- ✅ Status indicators are clear ([P], [IP], [C])

**Recommendation**: The design meets usability standards. Formal user testing with 3 non-technical users is recommended to confirm the 5-minute learning curve.

## Notes

- The application provides immediate feedback for all commands
- Error messages guide users to correct syntax
- The interactive loop allows users to experiment without restarting
- The help command is always available for reference
