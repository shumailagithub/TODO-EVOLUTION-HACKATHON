# Quickstart Guide: Todo Chatbot with NLP + NeonDB

## Architecture Overview

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌─────────────┐
│   User    │───▶│  Chat API   │───▶│  Service Layer │───▶│  NeonDB    │
│             │    │             │    │                 │    │             │
│ "add task"  │    │ NLP Parser  │    │ Intent Handler  │    │ tasks table │
└─────────────┘    │ Intent →    │    │ Verification    │    │ tasks_with_ │
                   │ Params      │    │ SELECT after    │    │ serial VIEW │
                   └──────────────┘    │ each operation  │    └─────────────┘
                                     └─────────────────┘
```

## NLP Flow Process

```
User Input ──► Intent Recognition ──► Parameter Extraction ──► API Call ──► DB Operation ──► Verification ──► Response
  "add buy      (ADD_TASK)           (description: "buy      (POST /api/    (INSERT INTO    (SELECT WHERE    "✅ Added task:
  milk"                              milk")                  tasks)         tasks ...)      uuid=new_uuid)    buy milk (#3)"
```

## Core Components

### 1. NLP Engine
- **Input**: Natural language command
- **Processing**: Intent classification and parameter extraction
- **Output**: Structured operation request

### 2. Verification Layer
- **CREATE**: Verify insertion with SELECT by UUID
- **UPDATE**: Verify modification with SELECT by UUID
- **DELETE**: Verify removal with SELECT (expect 0 results)
- **COMPLETE**: Verify status change with SELECT by UUID

### 3. Serial Number Management
- **Read**: Use `tasks_with_serial` VIEW for all queries
- **Mapping**: Serial numbers automatically renumbered after deletions
- **Consistency**: Serial numbers always reflect current database state

## Error Handling Flow

```
Error Type ──► Detection ──► Verification ──► User Message
Validation    Input check   ❌              "Please provide task description"
Database      Query fail    ❌              "Temporary issue, please try again"
Not Found     SELECT 0      ❌              "Task #999 not found"
Success       All checks    ✅              "✅ Operation completed"
```

## Key Verification Points

### After CREATE (Add Task)
```python
# 1. Insert task
new_task_uuid = insert_task(user_id, description)

# 2. Verify insertion
verification_query = "SELECT * FROM tasks WHERE id = ? AND description = ?"
result = execute_query(verification_query, [new_task_uuid, description])

# 3. Confirm success before responding
if len(result) == 1:
    # Safe to respond to user
    return success_response(new_task_uuid, get_serial_number(new_task_uuid))
else:
    # Rollback and report error
    return error_response("Task was not properly saved")
```

### After UPDATE (Complete Task)
```python
# 1. Map serial to UUID
target_uuid = get_uuid_by_serial_and_user(user_id, serial_number)

# 2. Update task
update_query = "UPDATE tasks SET completed = true WHERE id = ?"
execute_query(update_query, [target_uuid])

# 3. Verify completion
verification_query = "SELECT completed FROM tasks WHERE id = ?"
result = execute_query(verification_query, [target_uuid])

# 4. Confirm status before responding
if result and result[0]['completed'] == True:
    return success_response(target_uuid, serial_number)
else:
    return error_response("Task completion failed to save")
```

### After DELETE (Remove Task)
```python
# 1. Map serial to UUID
target_uuid = get_uuid_by_serial_and_user(user_id, serial_number)

# 2. Delete task
delete_query = "DELETE FROM tasks WHERE id = ?"
rows_affected = execute_query(delete_query, [target_uuid])

# 3. Verify deletion
verification_query = "SELECT COUNT(*) FROM tasks WHERE id = ?"
result = execute_query(verification_query, [target_uuid])

# 4. Confirm removal before responding
if result[0]['count'] == 0:
    return success_response(target_uuid, serial_number)
else:
    return error_response("Task deletion failed to save")
```

## Testing Approach

1. **Unit Tests**: Verify each component in isolation
2. **Integration Tests**: Test the full flow from NLP to DB verification
3. **End-to-End Tests**: Simulate user interactions and verify database state
4. **Edge Case Tests**: Test error conditions and boundary scenarios