---
id: 6
title: AI Chatbot Tasks Creation
stage: tasks
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-chatbot
branch: 5-ai-chatbot
user: user
command: $ARGUMENTS
labels: [tasks, ai, chatbot, todo, mcp]
links:
  spec: ../specs/5-ai-chatbot/spec.md
  plan: ../specs/5-ai-chatbot/plan.md
  tasks: ../specs/5-ai-chatbot/tasks.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/5-ai-chatbot/tasks.md
tests:
---

## Prompt

```
$ARGUMENTS
```

Tasks Breakdown for Phase III Implementation

**TASK GROUP 1: Database Setup**

**T-301: Create Conversation Model**
- File: `/backend/models/conversation.py`
- Create SQLModel class with fields: id, user_id, created_at, updated_at
- Add table=True parameter
- Add indexes on user_id
- Export model

**T-302: Create Message Model**
- File: `/backend/models/message.py`
- Create SQLModel class with fields: id, conversation_id, user_id, role, content, created_at
- Add foreign key to conversations table
- Add indexes on conversation_id and user_id
- Validate role is "user" or "assistant"
- Export model

**T-303: Create Database Operations for Conversations**
- File: `/backend/db/conversation_operations.py`
- Implement `create_conversation(user_id: str) -> int`
- Implement `get_conversation_history(conversation_id: int, limit: int = 50) -> list`
- Implement `add_message(conversation_id: int, user_id: str, role: str, content: str) -> int`
- Add error handling for database failures
- Test all functions

**T-304: Database Migration**
- Create migration script to add conversations and messages tables
- Test migration on local database
- Verify existing tasks table unchanged

---

**TASK GROUP 2: MCP Server Implementation**

**T-305: Setup MCP Server Structure**
- File: `/backend/mcp/server.py`
- Install: `pip install mcp`
- Create MCP Server class
- Setup tool registry
- Add logging for debugging

**T-306: Implement add_task MCP Tool**
- Define input schema: {user_id: str, title: str, description?: str}
- Define output schema: {task_id: int, status: str, title: str, message: str}
- Connect to existing task creation logic from Phase II
- Validate user_id
- Return standardized response
- Test with sample inputs

**T-307: Implement list_tasks MCP Tool**
- Define input schema: {user_id: str, status?: "all"|"pending"|"completed"}
- Define output schema: Array of task objects
- Query existing tasks table with filters
- Sort by created_at descending
- Return formatted list
- Test with different status filters

**T-308: Implement complete_task MCP Tool**
- Define input schema: {user_id: str, task_id: int}
- Define output schema: {task_id: int, status: "completed", title: str, message: str}
- Validate task exists and belongs to user
- Update task.completed = True
- Return confirmation
- Test with valid and invalid task IDs

**T-309: Implement delete_task MCP Tool**
- Define input schema: {user_id: str, task_id: int}
- Define output schema: {task_id: int, status: "deleted", title: str, message: str}
- Validate task exists and belongs to user
- Delete from database
- Return confirmation
- Test deletion and verify task removed

**T-310: Implement update_task MCP Tool**
- Define input schema: {user_id: str, task_id: int, title?: str, description?: str}
- Define output schema: {task_id: int, status: "updated", title: str, message: str}
- Validate task exists and belongs to user
- Update provided fields only
- Return updated task
- Test partial updates (title only, description only, both)

**T-311: Register All Tools with MCP Server**
- Register all 5 tools in MCP server
- Test tool discovery
- Verify tool schemas are correct
- Test error handling for each tool

---

**TASK GROUP 3: OpenAI Agent Service**

**T-312: Setup OpenAI Agent**
- File: `/backend/services/agent_service.py`
- Install: `pip install openai`
- Create agent configuration with GPT-4
- Add system prompt for task management
- Configure tool calling

**T-313: Implement Agent Runner**
- Create `run_agent(messages: list, user_id: str)` function
- Build message history for agent
- Call OpenAI API with tools
- Handle tool calls from agent
- Execute requested tools
- Format agent response
- Test with sample conversations

**T-314: Add Agent Error Handling**
- Handle OpenAI API failures (rate limits, errors)
- Handle invalid tool calls
- Handle tool execution errors
- Provide fallback responses
- Log errors for debugging
- Test error scenarios

---

**TASK GROUP 4: Chat API Endpoint**

**T-315: Create Chat Router**
- File: `/backend/api/chat.py`
- Create FastAPI router
- Define request/response Pydantic models
- Add authentication dependency

**T-316: Implement Chat Endpoint Logic**
- Implement POST `/api/{user_id}/chat`
- Get or create conversation
- Fetch conversation history
- Store user message
- Build message array for agent
- Run agent
- Store assistant response
- Return formatted response
- Test with Postman/curl

**T-317: Register Chat Router in Main App**
- File: `/backend/main.py`
- Import chat router
- Register with app.include_router()
- Test endpoint is accessible
- Verify authentication works

---

**TASK GROUP 5: ChatKit Frontend**

**T-318: Setup ChatKit Page**
- File: `/frontend/pages/chat.js`
- Install: `npm install @openai/chatkit`
- Create chat page component
- Add authentication check
- Redirect to login if not authenticated

**T-319: Implement Chat Message Handler**
- Create `handleMessage` function
- Call POST `/api/{user_id}/chat` with message
- Handle response from backend
- Update conversation ID state
- Display assistant response in ChatKit
- Add loading indicator

**T-320: Style Chat Interface**
- Match existing app design (glassmorphism, dark mode support)
- Style message bubbles
- Add timestamp display
- Add user/assistant avatars
- Make responsive for mobile
- Test on different screen sizes

**T-321: Add Chat Link to Navigation (Optional)**
- File: `/frontend/components/Navbar.tsx`
- Add "Chat" navigation link
- Highlight active page
- Test navigation works

---

**TASK GROUP 6: OpenAI Domain Setup**

**T-322: Deploy Frontend and Configure Domain**
- Deploy frontend to Vercel
- Get production URL
- Add domain to OpenAI allowlist: https://platform.openai.com/settings/organization/security/domain-allowlist
- Get domain key
- Add to environment variables
- Redeploy and test ChatKit in production

---

**TASK GROUP 7: Integration Testing**

**T-323: Test Natural Language Commands**
- Test: "Add task to buy groceries"
- Test: "Show me all my tasks"
- Test: "What's pending?"
- Test: "Mark task 3 as complete"
- Test: "Delete task 2"
- Test: "Change task 1 to 'Call dentist at 3pm'"
- Test: "I need to remember to pay bills"
- Verify agent calls correct tools
- Verify responses are friendly and accurate

**T-324: Test Conversation History**
- Start conversation
- Send multiple messages
- Verify agent remembers context
- Restart backend server
- Resume conversation
- Verify history persisted correctly

**T-325: Test Error Scenarios**
- Test with invalid task ID
- Test with non-existent conversation ID
- Test with malformed messages
- Test with missing authentication
- Test with database connection failures
- Verify graceful error handling

**T-326: Verify Phase II Unchanged**
- Test existing REST API endpoints still work
- Test existing web UI (index.js) still works
- Test task CRUD operations unchanged
- Test login/registration still works
- Verify no regressions introduced

---

**TASK GROUP 8: Documentation & Deployment**

**T-327: Update Documentation**
- Update README with Phase III setup
- Document environment variables needed
- Add chatbot usage examples
- Document MCP tools
- Create Phase III spec files in `/specs/phase3/`

**T-328: Code Cleanup**
- Remove console.logs
- Remove debug code
- Format code consistently
- Add comments where needed
- Run linter/formatter

**T-329: Git Commit and Tag**
- Commit Phase III changes
- Create meaningful commit message
- Push to GitHub
- Create tag: `v3.0-phase3`
- Push tag: `git push origin v3.0-phase3`

---

**DEPENDENCIES:**