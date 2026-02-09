# API Contract: MCP Tools

## Overview
The system exposes 5 MCP (Model Context Protocol) tools for AI agent integration. These tools are called by the OpenAI agent based on natural language interpretation.

## Tool: add_task
### Description
Creates a new task in the user's todo list.

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "The user's ID"},
    "title": {"type": "string", "description": "The task title"},
    "description": {"type": "string", "description": "Optional task description"}
  },
  "required": ["user_id", "title"]
}
```

### Output
```json
{
  "task_id": 123,
  "status": "created",
  "title": "Buy groceries"
}
```

## Tool: list_tasks
### Description
Lists tasks from the user's todo list with optional filtering.

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "The user's ID"},
    "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status"}
  },
  "required": ["user_id"]
}
```

### Output
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "completed": false,
      "created_at": "2023-01-01T00:00:00"
    }
  ]
}
```

## Tool: complete_task
### Description
Marks a task as completed.

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "The user's ID"},
    "task_id": {"type": "integer", "description": "The ID of the task to complete"}
  },
  "required": ["user_id", "task_id"]
}
```

### Output
```json
{
  "task_id": 123,
  "status": "completed",
  "title": "Buy groceries"
}
```

## Tool: delete_task
### Description
Deletes a task from the user's list.

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "The user's ID"},
    "task_id": {"type": "integer", "description": "The ID of the task to delete"}
  },
  "required": ["user_id", "task_id"]
}
```

### Output
```json
{
  "task_id": 123,
  "status": "deleted",
  "title": "Buy groceries"
}
```

## Tool: update_task
### Description
Updates task fields in the user's list.

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "string", "description": "The user's ID"},
    "task_id": {"type": "integer", "description": "The ID of the task to update"},
    "title": {"type": "string", "description": "New title for the task"},
    "description": {"type": "string", "description": "New description for the task"}
  },
  "required": ["user_id", "task_id"]
}
```

### Output
```json
{
  "task_id": 123,
  "status": "updated",
  "title": "Buy groceries"
}
```

## Security
- All tools validate that the user_id matches the authenticated user
- Tools only operate on data belonging to the specified user
- No cross-user data access is permitted

## Error Handling
- Invalid user_id: Returns error indicating user not found
- Invalid task_id: Returns error indicating task not found
- Permission denied: Returns error if user doesn't own the resource