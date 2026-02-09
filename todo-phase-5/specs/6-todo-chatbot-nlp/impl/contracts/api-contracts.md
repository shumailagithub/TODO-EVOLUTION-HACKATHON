# API Contracts: Todo Chatbot with NLP + NeonDB

## Overview
All endpoints must follow the verification protocol:
1. Validate input
2. Execute DB operation
3. Verify with SELECT
4. Respond to chatbot only after verification

## Endpoint Specifications

### POST /api/{user_id}/chat
**Purpose**: Process natural language input and return structured response

#### Request
```json
{
  "message": "Natural language command (e.g., 'add buy milk')"
}
```

#### Response
```json
{
  "response": "Structured response for user",
  "operation_result": {
    "success": true,
    "operation": "add|complete|delete|update|list",
    "details": {
      "task_uuid": "string",
      "serial_number": "integer",
      "description": "string",
      "status": "completed|pending|deleted|added|updated"
    }
  }
}
```

#### Error Response
```json
{
  "response": "User-friendly error message",
  "error_code": "VALIDATION_ERROR|DATABASE_ERROR|NOT_FOUND|UNAUTHORIZED",
  "details": "Specific error details for debugging"
}
```

## Verified Operation Endpoints

### CREATE: Add Task
**Intent**: "add buy milk", "create task walk dog"

**Process**:
1. Parse intent → ADD_TASK
2. Extract parameters → description: "buy milk"
3. Validate input → ensure description not empty
4. Execute: INSERT into tasks table
5. Verify: SELECT WHERE uuid = new_uuid AND description = "buy milk"
6. Return: Confirmation with serial number from VIEW

**Success Response**:
```json
{
  "response": "✅ Added task: buy milk (serial #3)",
  "operation_result": {
    "success": true,
    "operation": "add",
    "details": {
      "task_uuid": "uuid-string",
      "serial_number": 3,
      "description": "buy milk",
      "status": "added"
    }
  }
}
```

### READ: List Tasks
**Intent**: "list tasks", "show all", "what do I have to do?"

**Process**:
1. Parse intent → LIST_TASKS
2. Execute: SELECT from tasks_with_serial VIEW
3. Format: Prepare response with serial numbers
4. Verify: Check result count matches expectation
5. Return: Formatted task list

**Success Response**:
```json
{
  "response": "1. buy milk [pending]\n2. walk dog [completed]\n3. call mom [pending]",
  "operation_result": {
    "success": true,
    "operation": "list",
    "details": {
      "task_count": 3,
      "tasks": [
        {"serial_number": 1, "description": "buy milk", "completed": false},
        {"serial_number": 2, "description": "walk dog", "completed": true},
        {"serial_number": 3, "description": "call mom", "completed": false}
      ]
    }
  }
}
```

### UPDATE: Complete Task
**Intent**: "complete task 1", "mark #2 as done", "finish task 3"

**Process**:
1. Parse intent → COMPLETE_TASK
2. Extract parameters → serial_number: 1
3. Map serial to UUID via VIEW
4. Validate: Ensure task belongs to user
5. Execute: UPDATE SET completed = true WHERE uuid = mapped_uuid
6. Verify: SELECT WHERE uuid = mapped_uuid AND completed = true
7. Return: Confirmation

**Success Response**:
```json
{
  "response": "✅ Completed task: buy milk (serial #1)",
  "operation_result": {
    "success": true,
    "operation": "complete",
    "details": {
      "task_uuid": "uuid-string",
      "serial_number": 1,
      "description": "buy milk",
      "status": "completed"
    }
  }
}
```

### DELETE: Remove Task
**Intent**: "delete task 1", "remove #2", "cancel task 3"

**Process**:
1. Parse intent → DELETE_TASK
2. Extract parameters → serial_number: 1
3. Map serial to UUID via VIEW
4. Validate: Ensure task belongs to user
5. Execute: DELETE FROM tasks WHERE uuid = mapped_uuid
6. Verify: SELECT COUNT WHERE uuid = mapped_uuid should equal 0
7. Return: Confirmation (serial numbers automatically renumbered)

**Success Response**:
```json
{
  "response": "✅ Deleted task: buy milk (serial #1)",
  "operation_result": {
    "success": true,
    "operation": "delete",
    "details": {
      "task_uuid": "uuid-string",
      "serial_number": 1,
      "description": "buy milk",
      "status": "deleted"
    }
  }
}
```

## Verification Requirements

### CREATE Verification
- **Action**: After INSERT, execute SELECT WHERE uuid = new_uuid AND description = provided_desc
- **Expected**: Single record matching inserted data
- **Failure**: Rollback if verification fails, return error

### UPDATE Verification
- **Action**: After UPDATE, execute SELECT WHERE uuid = target_uuid AND field = expected_new_value
- **Expected**: Record with updated values
- **Failure**: Return error without claiming success

### DELETE Verification
- **Action**: After DELETE, execute SELECT WHERE uuid = target_uuid
- **Expected**: Zero records returned
- **Failure**: Return error without claiming success

### Error Propagation Strategy
- **Validation Errors**: Invalid input → User-friendly message explaining what's wrong
- **Database Errors**: Connection/query issues → "Temporary issue, please try again"
- **Not Found**: Referenced task doesn't exist → "Task not found" with suggestion
- **Unauthorized**: Attempt to access others' tasks → "Access denied" message