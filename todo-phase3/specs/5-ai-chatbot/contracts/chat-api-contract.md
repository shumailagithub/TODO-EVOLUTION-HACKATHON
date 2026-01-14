# API Contract: Chat Endpoint

## Endpoint
```
POST /api/{user_id}/chat
```

## Description
Processes natural language messages through an AI agent and performs appropriate task operations based on user intent. Maintains conversation context and returns friendly responses.

## Parameters
- `user_id` (path): String identifier for the authenticated user

## Request Body
```json
{
  "conversation_id": 123,
  "message": "Add buy groceries to my list"
}
```

### Fields
- `conversation_id` (optional): Integer ID of existing conversation. If not provided, a new conversation is created.
- `message` (required): Natural language message from the user

## Response
```json
{
  "conversation_id": 123,
  "response": "✅ Added task: Buy groceries",
  "tool_calls": ["add_task"]
}
```

### Response Fields
- `conversation_id`: Integer ID of the conversation (newly created or existing)
- `response`: Friendly, conversational response from the AI agent
- `tool_calls`: Array of MCP tools that were invoked during processing

## Error Responses

### 401 Unauthorized
- **Condition**: Invalid or missing authentication
- **Body**: `{"detail": "Unauthorized"}`

### 404 Not Found
- **Condition**: User does not exist
- **Body**: `{"detail": "User not found"}`

### 500 Internal Server Error
- **Condition**: Server error during processing
- **Body**: `{"detail": "Internal server error"}`

## Security
- All requests must include valid authentication
- User isolation enforced: users can only access their own conversations
- MCP tools validate user_id parameter for all operations

## Examples

### Starting a New Conversation
```
POST /api/user123/chat
```
```json
{
  "message": "Add buy milk to my tasks"
}
```

### Continuing an Existing Conversation
```
POST /api/user123/chat
```
```json
{
  "conversation_id": 456,
  "message": "Show me what I have to do"
}
```

## Rate Limits
- TBD: Implementation-dependent (likely based on OpenAI API limits)

## Headers
- `Content-Type: application/json`
- Authentication headers as required by the system