# Database Specification

## Overview

Phase-2 uses PostgreSQL database via Neon cloud service, managed through SQLModel ORM. The database supports multi-user todo management with proper data isolation and referential integrity.

## Database Provider

**Provider:** Neon (Serverless PostgreSQL)
**Version:** PostgreSQL 15+
**Connection:** Managed via connection string from environment variable

**Environment Variable:**
```bash
DATABASE_URL="postgresql://username:password@hostname/database"
```

## Schema

### ER Diagram

```
┌─────────────────┐          ┌──────────────────┐
│      users      │          │  refresh_tokens  │
├─────────────────┤          ├──────────────────┤
│ id (PK)         │          │ id (PK)          │
│ username        │◄─────────┤ user_id (FK)     │
│ password_hash   │          │ token_id         │
│ created_at      │          │ expires_at       │
│ updated_at      │          │ created_at       │
└─────────────────┘          └──────────────────┘
         │
         │
         │
         ▼
┌─────────────────┐
│     tasks       │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ title           │
│ description     │
│ completed       │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## SQLModel Models

### 1. User Model

**Table:** `users`

**Purpose:** Store user account information

**Model Definition (Python/SQLModel):**
```python
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table_name = "users"
```

**Columns:**
- `id` (UUID, PRIMARY KEY): Unique identifier for user
- `username` (VARCHAR(50), UNIQUE, INDEXED): User's unique username
- `password_hash` (VARCHAR(255)): Bcrypt-hashed password
- `created_at` (TIMESTAMP, DEFAULT NOW()): Account creation timestamp
- `updated_at` (TIMESTAMP, DEFAULT NOW()): Last update timestamp

**Constraints:**
- `username` must be unique
- `username` length: 3-50 characters
- `password_hash` always required (bcrypt hashed)
- `created_at` and `updated_at` automatically set

**Indexes:**
- `idx_users_username` on `username` column (for login queries)

---

### 2. Refresh Token Model

**Table:** `refresh_tokens`

**Purpose:** Store active refresh tokens for token revocation

**Model Definition:**
```python
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class RefreshToken(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    token_id: str = Field(max_length=255, unique=True, index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table_name = "refresh_tokens"
```

**Columns:**
- `id` (UUID, PRIMARY KEY): Unique identifier for token record
- `user_id` (UUID, FOREIGN KEY): Reference to `users.id`
- `token_id` (VARCHAR(255), UNIQUE, INDEXED): The `jti` claim from JWT
- `expires_at` (TIMESTAMP): Token expiration datetime
- `created_at` (TIMESTAMP, DEFAULT NOW()): Token creation timestamp

**Constraints:**
- `user_id` must reference valid user
- `token_id` must be unique
- `expires_at` must be in future when created

**Indexes:**
- `idx_refresh_tokens_token_id` on `token_id` (for fast token validation)
- `idx_refresh_tokens_user_id` on `user_id` (for user token cleanup)

**Relationships:**
- Many refresh tokens per user (for multiple devices)
- Cascade delete: When user is deleted, all their refresh tokens are deleted

---

### 3. Task Model

**Table:** `tasks`

**Purpose:** Store user tasks

**Model Definition:**
```python
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table_name = "tasks"
```

**Columns:**
- `id` (UUID, PRIMARY KEY): Unique identifier for task
- `user_id` (UUID, FOREIGN KEY): Owner of the task (references `users.id`)
- `title` (VARCHAR(200)): Task title
- `description` (VARCHAR(1000), NULLABLE): Optional detailed description
- `completed` (BOOLEAN): Task completion status (default: false)
- `created_at` (TIMESTAMP, DEFAULT NOW()): Task creation timestamp
- `updated_at` (TIMESTAMP, DEFAULT NOW()): Last update timestamp

**Constraints:**
- `user_id` must reference valid user
- `title` must be provided (1-200 characters)
- `description` optional, max 1000 characters
- `completed` defaults to false

**Indexes:**
- `idx_tasks_user_id` on `user_id` (for user task queries)
- `idx_tasks_user_completed` on (`user_id`, `completed`) (for filtering by completion status)

**Relationships:**
- Many tasks per user
- Cascade delete: When user is deleted, all their tasks are deleted

---

## Relationships

### Users → Tasks (One-to-Many)
- One user can have many tasks
- Each task belongs to exactly one user
- Enforced via `tasks.user_id` foreign key

### Users → Refresh Tokens (One-to-Many)
- One user can have many refresh tokens (for multiple devices)
- Each refresh token belongs to exactly one user
- Enforced via `refresh_tokens.user_id` foreign key

## Database Initialization

### Migration Strategy

**Approach:** Simple table creation via SQLModel

**Order of Table Creation:**
1. `users` (no dependencies)
2. `refresh_tokens` (depends on `users`)
3. `tasks` (depends on `users`)

**Schema Versioning:** Not required for Phase-2 (simple initial setup)

### Initial Setup Script

```python
from sqlmodel import create_engine, SQLModel
from backend.models.user import User
from backend.models.refresh_token import RefreshToken
from backend.models.task import Task

def init_db():
    engine = create_engine(DATABASE_URL)

    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully")
```

## Queries

### Common Query Patterns

#### 1. Create User
```python
user = User(username="john_doe", password_hash="$2b$12$hashed_password")
session.add(user)
session.commit()
session.refresh(user)
```

#### 2. Find User by Username
```python
user = session.exec(
    select(User).where(User.username == "john_doe")
).first()
```

#### 3. Create Task for User
```python
task = Task(
    user_id=user.id,
    title="Buy groceries",
    description="Milk, eggs, bread"
)
session.add(task)
session.commit()
session.refresh(task)
```

#### 4. Get All Tasks for User
```python
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()
```

#### 5. Get Completed Tasks for User
```python
tasks = session.exec(
    select(Task)
    .where(Task.user_id == user_id)
    .where(Task.completed == True)
).all()
```

#### 6. Get Single Task with Ownership Check
```python
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == current_user_id)
).first()
```

#### 7. Create Refresh Token
```python
refresh_token = RefreshToken(
    user_id=user.id,
    token_id="unique_jti_value",
    expires_at=datetime.utcnow() + timedelta(days=7)
)
session.add(refresh_token)
session.commit()
```

#### 8. Validate Refresh Token
```python
token_record = session.exec(
    select(RefreshToken)
    .where(RefreshToken.token_id == jti)
    .where(RefreshToken.expires_at > datetime.utcnow())
).first()
```

#### 9. Revoke Refresh Token
```python
session.exec(
    delete(RefreshToken).where(RefreshToken.token_id == jti)
)
session.commit()
```

## Data Integrity Rules

### 1. User Isolation
- All task queries MUST include `user_id` filter
- Backend API enforces ownership check before task operations
- Users cannot query tasks without their `user_id` in WHERE clause

### 2. Cascade Deletion
- Deleting a user automatically deletes their refresh tokens
- Deleting a user automatically deletes their tasks

### 3. Unique Constraints
- `username` must be unique across all users
- `refresh_tokens.token_id` must be unique

### 4. Not Null Constraints
- `users.username`
- `users.password_hash`
- `tasks.user_id`
- `tasks.title`

## Performance Considerations

### Index Usage

**Critical Indexes:**
1. `users.username` - Required for login lookup
2. `refresh_tokens.token_id` - Required for token validation
3. `tasks.user_id` - Required for all task queries
4. `tasks.user_id + tasks.completed` - Optimizes filtering

### Connection Pooling

**SQLAlchemy Engine Configuration:**
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)
```

**Configuration:**
- Pool size: 5 connections
- Max overflow: 10 connections
- Pre-ping: Test connections before use (detect stale connections)

## Backup and Recovery

**Managed by Neon:**
- Automatic backups
- Point-in-time recovery
- Database snapshots

**No manual backup configuration required for Phase-2**

## Database Connection

### Environment Configuration

**Development (.env):**
```bash
DATABASE_URL="postgresql://user:pass@localhost:5432/todo_phase2"
```

**Production (Neon):**
```bash
DATABASE_URL="postgresql://neon-user:password@ep-xxx.aws.neon.tech/neondb?sslmode=require"
```

### Connection Lifecycle

**Session Management:**
- Create new session per request
- Commit or rollback at end of request
- Close session to return to pool

**Example:**
```python
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session
```

## SQL for Reference

### Table Creation SQL

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_username ON users(username);

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_id VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_refresh_tokens_token_id ON refresh_tokens(token_id);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```
