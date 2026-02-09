# Quickstart Guide: AI-Powered Todo Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (NeonDB configured)
- OpenAI API key
- Better Auth configured

## Setup Instructions

### 1. Environment Configuration

Add the following to your `.env` file in the backend directory:

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Database Setup

The AI chatbot requires two new database tables:

**conversations** table:
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
```

**messages** table:
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

### 3. Backend Services

Start the backend API server:

```bash
cd backend
pip install -r requirements.txt  # if needed
uvicorn main:app --reload --port 8001
```

The chat endpoint will be available at:
- POST `/api/{user_id}/chat`

### 4. Frontend Setup

Start the frontend development server:

```bash
cd frontend
npm install  # if needed
npm run dev
```

Access the chat interface at:
- Navigate to `/chat` page in the application
- Or click the "Chat" link in the navbar

## Usage Examples

Once the system is running, users can interact with the AI chatbot using natural language:

### Adding Tasks
- "Add buy groceries to my list"
- "Create a task to call the doctor"
- "Add 'finish report' to my tasks"

### Listing Tasks
- "Show me my tasks"
- "What do I need to do?"
- "Show pending tasks"
- "What's completed?"

### Managing Tasks
- "Mark task 1 as done"
- "Complete the first task"
- "Delete task 2"
- "Change task 1 to 'buy milk'"

## API Contract

### Chat Endpoint
```
POST /api/{user_id}/chat
```

**Request Body:**
```json
{
  "conversation_id": 123,    // optional, creates new if not provided
  "message": "Add task to buy groceries"
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "✅ Added task: Buy groceries",
  "tool_calls": ["add_task"]
}
```

## MCP Tools

The system exposes 5 MCP tools for the AI agent:

1. **add_task**: `{user_id, title, description?}` → `{task_id, status, title}`
2. **list_tasks**: `{user_id, status?}` → `{tasks: [{id, title, completed, created_at}]}`
3. **complete_task**: `{user_id, task_id}` → `{task_id, status, title}`
4. **delete_task**: `{user_id, task_id}` → `{task_id, status, title}`
5. **update_task**: `{user_id, task_id, title?, description?}` → `{task_id, status, title}`

## Troubleshooting

### Common Issues
- **API Key Error**: Ensure OPENAI_API_KEY is set correctly in environment
- **Database Connection**: Verify PostgreSQL connection string is correct
- **Authentication**: Ensure user is logged in before accessing chat
- **CORS Issues**: Check that frontend origin is allowed in backend CORS settings

### Debugging Tips
- Check server logs for detailed error messages
- Verify database tables were created successfully
- Test individual MCP tools separately if AI integration fails
- Confirm user authentication is working properly