# Data Model: AI-Powered Todo Chatbot

## Entities

### Conversation
**Purpose**: Tracks individual chat sessions for each user

**Fields**:
- `id` (int, primary key, auto-increment) - Unique identifier for the conversation
- `user_id` (str, indexed) - Foreign key linking to user (enforces user isolation)
- `created_at` (datetime) - Timestamp when conversation was created
- `updated_at` (datetime) - Timestamp when conversation was last updated

**Relationships**:
- One-to-many with Message (one conversation can have many messages)

**Validation**:
- `user_id` must exist in users table
- `created_at` and `updated_at` automatically managed

### Message
**Purpose**: Stores individual messages within a conversation

**Fields**:
- `id` (int, primary key, auto-increment) - Unique identifier for the message
- `conversation_id` (int, indexed, foreign key) - Links to parent conversation
- `user_id` (str, indexed) - Links to user who sent the message
- `role` (str) - Message role ("user" or "assistant")
- `content` (str) - The actual message content
- `created_at` (datetime) - Timestamp when message was created

**Relationships**:
- Many-to-one with Conversation (many messages belong to one conversation)

**Validation**:
- `role` must be either "user" or "assistant"
- `conversation_id` must exist in conversations table
- `user_id` must match the conversation owner
- `content` cannot be empty

### Task (Existing - Unchanged)
**Purpose**: Represents todo items (from Phase I & II, preserved unchanged)

**Fields**:
- `id` (int, primary key, auto-increment)
- `user_id` (str, indexed) - Owner of the task
- `title` (str) - Task description
- `description` (str, optional) - Extended task details
- `completed` (bool) - Completion status
- `created_at` (datetime) - When task was created
- `updated_at` (datetime) - When task was last updated

**Validation**:
- `user_id` enforces ownership
- `title` cannot be empty
- `completed` defaults to False

## State Transitions

### Task State Transitions
- `pending` → `completed`: When user marks task as done
- `completed` → `pending`: When user unmarks completed task (if supported)

### Conversation Lifecycle
- Created when user starts first chat session
- Updated when new messages are added
- Remains until cleanup policy is applied (future enhancement)

## Indexes
- `conversations.user_id`: Enables fast user-based queries
- `messages.conversation_id`: Enables fast conversation history retrieval
- `messages.user_id`: Enables security validation
- Composite indexes may be added based on query patterns