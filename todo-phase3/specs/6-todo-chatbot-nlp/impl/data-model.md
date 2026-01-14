# Data Model: Todo Chatbot with NLP + NeonDB

## Current Database Schema

### tasks table
- **id**: UUID (Primary Key) - Internal identifier
- **user_id**: UUID - Owner of the task
- **description**: TEXT - Task description
- **completed**: BOOLEAN - Completion status
- **created_at**: TIMESTAMP - Creation time
- **updated_at**: TIMESTAMP - Last update time

### tasks_with_serial VIEW
- **serial_number**: INTEGER - Sequential numbering (ROW_NUMBER)
- **id**: UUID - Original task UUID
- **user_id**: UUID - Owner of the task
- **description**: TEXT - Task description
- **completed**: BOOLEAN - Completion status
- **created_at**: TIMESTAMP - Creation time
- **updated_at**: TIMESTAMP - Last update time

## Data Flow Patterns

### Read Operations
1. User requests tasks by serial number
2. Application queries `tasks_with_serial` VIEW
3. Returns serial_number mapped to actual task data
4. Serial numbers automatically renumbered after deletions

### Write Operations
1. User performs operation (add, update, delete, complete)
2. Operation executed on `tasks` table using UUID
3. Verification SELECT confirms operation success
4. Response reflects actual database state

## Entity Relationships

### Task Entity
- **Identity**: UUID (internal), serial_number (user-facing)
- **Ownership**: Linked to user via user_id
- **State**: Active/Completed (via completed boolean)
- **Lifecycle**: Created → Updated → Completed/Deleted

### User-Task Relationship
- **One-to-Many**: One user to many tasks
- **Isolation**: Tasks isolated by user_id
- **Access Control**: Only owner can modify tasks

## Validation Rules

### Task Creation
- Description must not be empty
- User_id must match authenticated user
- Completed status defaults to false

### Task Updates
- UUID must exist and belong to user
- Serial number resolution happens at query time
- Updates must be verified in database

### Task Deletion
- UUID must exist and belong to user
- Deletion triggers serial number renumbering
- Verification confirms record no longer exists

## State Transition Patterns

### Task Lifecycle
```
CREATED (completed: false)
    ↓
COMPLETED (completed: true)
    ↑ ↓
UPDATED (any field change)
    ↓
DELETED (record removed)
```

### Serial Number Management
- **On INSERT**: New task gets next available serial number
- **On DELETE**: All subsequent serial numbers decrease by 1
- **On UPDATE**: Serial numbers remain unchanged unless deletion occurs
- **Consistency**: VIEW always reflects current serial number assignments