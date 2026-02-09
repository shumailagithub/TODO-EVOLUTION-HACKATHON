# Testing Plan: AI-Powered Todo Chatbot (Phase III)

## Overview
This document outlines the comprehensive testing plan for the AI-Powered Todo Chatbot implementation. The testing ensures all new functionality works correctly while preserving existing Phase I and II functionality.

## Test Categories

### 1. MCP Tools Testing

#### 1.1 add_task Tool
- **Test Case**: Call `add_task` with valid parameters
- **Input**: `{user_id: "test_user", title: "Buy groceries", description: "Milk, bread, eggs"}`
- **Expected**: Returns `{task_id: int, status: "created", title: "Buy groceries"}`
- **Validation**: Task appears in user's task list

#### 1.2 list_tasks Tool
- **Test Case**: Call `list_tasks` with different status filters
- **Input**: `{user_id: "test_user", status: "all" | "pending" | "completed"}`
- **Expected**: Returns array of tasks matching filter
- **Validation**: Correct tasks returned based on status

#### 1.3 complete_task Tool
- **Test Case**: Call `complete_task` with valid task ID
- **Input**: `{user_id: "test_user", task_id: 123}`
- **Expected**: Returns `{task_id: 123, status: "completed", title: "Original title"}`
- **Validation**: Task is marked as completed in database

#### 1.4 delete_task Tool
- **Test Case**: Call `delete_task` with valid task ID
- **Input**: `{user_id: "test_user", task_id: 123}`
- **Expected**: Returns `{task_id: 123, status: "deleted", title: "Original title"}`
- **Validation**: Task is removed from database

#### 1.5 update_task Tool
- **Test Case**: Call `update_task` with valid parameters
- **Input**: `{user_id: "test_user", task_id: 123, title: "Updated title"}`
- **Expected**: Returns `{task_id: 123, status: "updated", title: "Updated title"}`
- **Validation**: Task fields are updated in database

### 2. Chat Endpoint Testing

#### 2.1 Basic Chat Functionality
- **Test Case**: Send message to `/api/{user_id}/chat`
- **Input**: `{conversation_id: null, message: "Add buy milk"}`
- **Expected**: Response with new conversation_id, assistant response, and tool_calls
- **Validation**: New conversation created, message stored, task added

#### 2.2 Existing Conversation
- **Test Case**: Continue existing conversation
- **Input**: `{conversation_id: 123, message: "Show my tasks"}`
- **Expected**: Response continues conversation context
- **Validation**: Conversation history maintained

#### 2.3 Authentication
- **Test Case**: Attempt to access without valid user
- **Input**: Invalid or missing user_id
- **Expected**: Proper error response
- **Validation**: Unauthorized access prevented

### 3. Conversation Persistence Testing

#### 3.1 Conversation Creation
- **Test Case**: Start new conversation
- **Action**: Send first message without conversation_id
- **Expected**: New conversation created in DB with user_id
- **Validation**: Conversation record exists with correct user_id

#### 3.2 Message Storage
- **Test Case**: Send multiple messages
- **Action**: Multiple chat requests in sequence
- **Expected**: All messages stored in DB with correct roles
- **Validation**: Message records exist with conversation_id and user_id

#### 3.3 Context Recovery
- **Test Case**: Restart server and resume conversation
- **Action**: Retrieve conversation history after server restart
- **Expected**: Previous messages available to AI agent
- **Validation**: Conversation context preserved

### 4. Natural Language Understanding Testing

#### 4.1 Add Task Commands
- **Test Case**: Various ways to add tasks
- **Inputs**:
  - "Add buy groceries"
  - "Create task: call dentist"
  - "Add 'walk the dog' to my list"
- **Expected**: Tasks created via add_task tool
- **Validation**: Tasks appear in user's list

#### 4.2 List Task Commands
- **Test Case**: Various ways to list tasks
- **Inputs**:
  - "Show me my tasks"
  - "What do I need to do?"
  - "Show pending tasks"
  - "What's completed?"
- **Expected**: list_tasks tool called with appropriate filters
- **Validation**: Correct tasks returned to user

#### 4.3 Complete Task Commands
- **Test Case**: Various ways to complete tasks
- **Inputs**:
  - "Mark task 1 as done"
  - "Complete the first task"
  - "Finish 'buy groceries'"
- **Expected**: complete_task tool called
- **Validation**: Tasks marked as completed

#### 4.4 Delete Task Commands
- **Test Case**: Various ways to delete tasks
- **Inputs**:
  - "Delete task 2"
  - "Remove 'call dentist'"
  - "Cancel the third task"
- **Expected**: delete_task tool called
- **Validation**: Tasks removed from list

#### 4.5 Update Task Commands
- **Test Case**: Various ways to update tasks
- **Inputs**:
  - "Change task 1 to 'buy milk'"
  - "Update 'groceries' to 'buy essentials'"
- **Expected**: update_task tool called
- **Validation**: Task titles updated

### 5. Error Handling Testing

#### 5.1 Invalid Task IDs
- **Test Case**: Reference non-existent task IDs
- **Input**: "Complete task 999999"
- **Expected**: Graceful error handling with user-friendly message
- **Validation**: No system crashes, proper error response

#### 5.2 Malformed Natural Language
- **Test Case**: Ambiguous or unclear commands
- **Input**: "Um, maybe do something?"
- **Expected**: AI asks for clarification or provides helpful response
- **Validation**: System doesn't crash, user gets helpful feedback

#### 5.3 Unauthorized Access
- **Test Case**: User attempts to access another user's tasks
- **Input**: AI tool called with mismatched user_id
- **Expected**: Security validation prevents access
- **Validation**: Proper user isolation maintained

### 6. Existing Functionality Verification

#### 6.1 Phase II API Endpoints
- **Test Case**: Access existing task endpoints
- **Endpoints**: `/api/{user_id}/tasks`, `/api/{user_id}/tasks/{id}`, etc.
- **Expected**: All existing endpoints continue to work
- **Validation**: No regression in Phase II functionality

#### 6.2 Authentication Flow
- **Test Case**: Login, register, and auth endpoints
- **Endpoints**: `/api/auth/login`, `/api/auth/register`, etc.
- **Expected**: All auth endpoints continue to work
- **Validation**: No regression in authentication

#### 6.3 Frontend Pages
- **Test Case**: Access existing pages (index.js, login.js, register.js)
- **Pages**: Home page, login, registration
- **Expected**: All pages continue to work as before
- **Validation**: No regression in existing UI

### 7. Performance Testing

#### 7.1 Response Time
- **Test Case**: Measure chat response time
- **Target**: Under 2 seconds for 90% of responses
- **Validation**: AI responses within acceptable timeframe

#### 7.2 Concurrent Users
- **Test Case**: Multiple users chatting simultaneously
- **Scenario**: 10+ users using chat concurrently
- **Expected**: No data leakage between users
- **Validation**: Proper user isolation maintained

### 8. Security Testing

#### 8.1 User Isolation
- **Test Case**: Verify user data isolation
- **Method**: Cross-user data access attempts
- **Expected**: Users cannot access other users' tasks or conversations
- **Validation**: Foreign key constraints and user_id validation effective

#### 8.2 Database Integrity
- **Test Case**: Verify referential integrity
- **Method**: Check conversation-message relationships
- **Expected**: Proper foreign key relationships maintained
- **Validation**: No orphaned records

## Testing Execution Steps

### Pre-Test Setup
1. Ensure database is clean or seeded with test data
2. Verify environment variables are set correctly
3. Start backend and frontend services
4. Create test user accounts

### Test Execution Order
1. Run MCP tools tests (foundational)
2. Run chat endpoint tests (integration)
3. Run conversation persistence tests (state management)
4. Run natural language tests (AI functionality)
5. Run error handling tests (resilience)
6. Run existing functionality tests (regression)
7. Run performance tests (optimization)
8. Run security tests (protection)

### Post-Test Actions
1. Clean up test data from database
2. Document any issues found
3. Verify all tests pass before production deployment
4. Update documentation if needed

## Success Criteria
- All MCP tools function correctly
- Chat interface responds appropriately to natural language
- Conversation history persists correctly
- Existing functionality remains unaffected
- Error handling is graceful and user-friendly
- Security measures prevent unauthorized access
- Performance meets target requirements