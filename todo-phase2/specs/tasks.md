# Implementation Tasks - Phase-2

## Overview

This document breaks down the implementation plan into small, atomic, executable tasks. Each task is independently implementable and follows the correct execution order.

**Task Format:**
- ID: Sequential within section
- Title: Clear, actionable description
- Acceptance Criteria: Specific conditions for task completion
- Dependencies: Tasks that must be completed first

---

## 1. Backend Tasks

### B1.1: Initialize Backend Project Structure

**Title:** Create backend directory structure and project configuration

**Acceptance Criteria:**
- `backend/` directory exists
- `pyproject.toml` exists with project metadata
- All required dependencies listed in `pyproject.toml`:
  - fastapi
  - uvicorn[standard]
  - sqlmodel
  - psycopg2-binary
  - pydantic
  - python-jose[cryptography]
  - passlib[bcrypt]
  - python-multipart
  - python-dotenv
- Subdirectories created: `models/`, `auth/`, `api/`, `db/`, `config/`
- `.env.example` exists with required variable placeholders
- `.gitignore` exists excluding `.env`, `__pycache__`, `.pytest_cache`, `*.pyc`

**Dependencies:** None

---

### B1.2: Configure Environment Variables

**Title:** Set up environment variable loading and configuration

**Acceptance Criteria:**
- `backend/config.py` exists
- Loads environment variables using `python-dotenv`
- Defines configuration variables with defaults:
  - `DATABASE_URL` (from env, required)
  - `JWT_SECRET` (from env, required)
  - `ACCESS_TOKEN_EXPIRE_MINUTES` (from env, default: 15)
  - `REFRESH_TOKEN_EXPIRE_DAYS` (from env, default: 7)
  - `BCRYPT_ROUNDS` (from env, default: 12)
- Validates required environment variables exist
- `.env` file exists (not in version control) with all required values

**Dependencies:** B1.1

---

### B1.3: Create Database Connection and Session Management

**Title:** Set up SQLAlchemy engine and session factory

**Acceptance Criteria:**
- `backend/db/connection.py` exists
- Creates SQLAlchemy engine with connection pooling:
  - Pool size: 5
  - Max overflow: 10
  - Pool pre-ping enabled
- `get_session()` dependency function returns generator yielding Session
- Engine uses `DATABASE_URL` from config
- Session is properly closed after use

**Dependencies:** B1.2

---

### B1.4: Create User SQLModel

**Title:** Define User database model

**Acceptance Criteria:**
- `backend/models/user.py` exists
- User model class extends SQLModel and table=True
- Fields defined exactly matching database.md:
  - `id`: UUID, primary_key=True, default_factory=uuid4
  - `username`: str, index=True, unique=True, max_length=50
  - `password_hash`: str, max_length=255
  - `created_at`: datetime, default_factory=datetime.utcnow
  - `updated_at`: datetime, default_factory=datetime.utcnow
- Table name: "users"
- Model can be imported without errors

**Dependencies:** B1.1

---

### B1.5: Create RefreshToken SQLModel

**Title:** Define RefreshToken database model

**Acceptance Criteria:**
- `backend/models/refresh_token.py` exists
- RefreshToken model class extends SQLModel and table=True
- Fields defined exactly matching database.md:
  - `id`: UUID, primary_key=True, default_factory=uuid4
  - `user_id`: UUID, foreign_key="users.id"
  - `token_id`: str, unique=True, index=True, max_length=255
  - `expires_at`: datetime
  - `created_at`: datetime, default_factory=datetime.utcnow
- Table name: "refresh_tokens"
- Model can be imported without errors

**Dependencies:** B1.4

---

### B1.6: Create Task SQLModel

**Title:** Define Task database model

**Acceptance Criteria:**
- `backend/models/task.py` exists
- Task model class extends SQLModel and table=True
- Fields defined exactly matching database.md:
  - `id`: UUID, primary_key=True, default_factory=uuid4
  - `user_id`: UUID, foreign_key="users.id"
  - `title`: str, max_length=200
  - `description`: Optional[str], default=None, max_length=1000
  - `completed`: bool, default=False
  - `created_at`: datetime, default_factory=datetime.utcnow
  - `updated_at`: datetime, default_factory=datetime.utcnow
- Table name: "tasks"
- Model can be imported without errors

**Dependencies:** B1.4

---

### B1.7: Create Models Package Export

**Title:** Create models __init__.py to export all models

**Acceptance Criteria:**
- `backend/models/__init__.py` exists
- Exports User, RefreshToken, Task models
- Can import all models from `backend.models` package

**Dependencies:** B1.4, B1.5, B1.6

---

### B1.8: Create Database Initialization Script

**Title:** Create script to initialize database tables

**Acceptance Criteria:**
- `backend/db/init_db.py` exists
- `create_tables()` function defined
- Function creates all tables using `SQLModel.metadata.create_all(engine)`
- Function can be run as standalone script
- Prints success message after table creation

**Dependencies:** B1.3, B1.7

---

### B1.9: Initialize Database Tables

**Title:** Run database initialization script to create tables in PostgreSQL

**Acceptance Criteria:**
- Database initialization script executed successfully
- Tables created in Neon PostgreSQL:
  - `users`
  - `refresh_tokens`
  - `tasks`
- Table structures verified in Neon dashboard or via SQL client
- All indexes created correctly

**Dependencies:** B1.8

---

### B2.1: Create Password Hashing Utilities

**Title:** Implement password hashing and verification functions

**Acceptance Criteria:**
- `backend/auth/password.py` exists
- `hash_password(password: str) -> str` function:
  - Uses bcrypt with configured rounds
  - Returns hashed password as string
  - Each call produces different hash (due to salt)
- `verify_password(plain: str, hashed: str) -> bool` function:
  - Returns True if password matches hash
  - Returns False for invalid password
- Functions work correctly with bcrypt

**Dependencies:** B1.2

---

### B2.2: Create JWT Token Utilities

**Title:** Implement JWT token generation and validation functions

**Acceptance Criteria:**
- `backend/auth/tokens.py` exists
- `generate_access_token(user_id: str) -> str`:
  - Returns JWT string
  - Contains claims: sub, exp, iat, type="access"
  - Expires after ACCESS_TOKEN_EXPIRE_MINUTES
- `generate_refresh_token(user_id: str) -> str`:
  - Returns JWT string
  - Contains claims: sub, exp, iat, type="refresh", jti (unique)
  - Expires after REFRESH_TOKEN_EXPIRE_DAYS
- `decode_token(token: str) -> dict`:
  - Decodes and validates token signature
  - Returns token payload
  - Raises exception for invalid tokens
- Tokens signed with JWT_SECRET from config

**Dependencies:** B1.2

---

### B2.3: Create Authentication Dependencies

**Title:** Implement FastAPI dependencies for protected routes

**Acceptance Criteria:**
- `backend/auth/dependencies.py` exists
- `get_access_token()` dependency:
  - Extracts token from Authorization header
  - Strips "Bearer " prefix
  - Raises 401 if header missing
- `validate_access_token()` dependency:
  - Validates token signature and expiration
  - Returns decoded token payload
  - Raises 401 for invalid or expired tokens
- `get_current_user()` dependency:
  - Validates access token
  - Queries database for user by user_id
  - Returns User object
  - Raises 401 for invalid or missing user

**Dependencies:** B2.1, B2.2, B1.3, B1.4

---

### B2.4: Create User Database Operations

**Title:** Implement CRUD operations for users

**Acceptance Criteria:**
- `backend/db/user_operations.py` exists
- `create_user(username: str, password_hash: str) -> User`:
  - Creates new user in database
  - Returns created User object
  - Raises error if username exists
- `get_user_by_username(username: str) -> User | None`:
  - Returns User if found
  - Returns None if not found
- `get_user_by_id(user_id: str) -> User | None`:
  - Returns User if found
  - Returns None if not found
- All operations use session from dependency

**Dependencies:** B1.3, B1.4

---

### B2.5: Create Refresh Token Database Operations

**Title:** Implement CRUD operations for refresh tokens

**Acceptance Criteria:**
- `backend/db/token_operations.py` exists
- `create_refresh_token(user_id: str, token_id: str, expires_at: datetime) -> RefreshToken`:
  - Creates new refresh token in database
  - Returns created RefreshToken object
- `get_refresh_token(token_id: str) -> RefreshToken | None`:
  - Returns RefreshToken if found
  - Returns None if not found
- `delete_refresh_token(token_id: str) -> None`:
  - Deletes refresh token from database
- `delete_all_user_tokens(user_id: str) -> None`:
  - Deletes all refresh tokens for user
- All operations use session from dependency

**Dependencies:** B1.3, B1.5

---

### B2.6: Create Authentication Request/Response Models

**Title:** Define Pydantic models for authentication endpoints

**Acceptance Criteria:**
- `backend/api/auth.py` exists
- `LoginRequest` Pydantic model:
  - username: str
  - password: str
- `RegisterRequest` Pydantic model:
  - username: str
  - password: str
- `AuthResponse` Pydantic model:
  - access_token: str
  - refresh_token: str
  - user_id: str
  - username: str
- `RefreshTokenRequest` Pydantic model:
  - refresh_token: str
- Models validate input correctly

**Dependencies:** None

---

### B2.7: Implement Register Endpoint

**Title:** Create POST /api/auth/register endpoint

**Acceptance Criteria:**
- Endpoint: `POST /api/auth/register`
- Accepts JSON body: {username, password}
- Validates:
  - Username: 3-50 chars, alphanumeric + underscores
  - Password: minimum 8 chars
- Checks if username already exists
- Hashes password using hash_password()
- Creates user in database
- Generates access and refresh tokens
- Stores refresh token in database
- Returns 201 with AuthResponse on success
- Returns 400 for invalid input
- Returns 409 for existing username

**Dependencies:** B2.1, B2.2, B2.4, B2.5, B2.6

---

### B2.8: Implement Login Endpoint

**Title:** Create POST /api/auth/login endpoint

**Acceptance Criteria:**
- Endpoint: `POST /api/auth/login`
- Accepts JSON body: {username, password}
- Validates required fields
- Finds user by username
- Verifies password using verify_password()
- Generates access and refresh tokens
- Stores refresh token in database
- Returns 200 with AuthResponse on success
- Returns 400 for missing fields
- Returns 401 for invalid credentials

**Dependencies:** B2.1, B2.2, B2.4, B2.5, B2.6

---

### B2.9: Implement Refresh Token Endpoint

**Title:** Create POST /api/auth/refresh endpoint

**Acceptance Criteria:**
- Endpoint: `POST /api/auth/refresh`
- Accepts JSON body: {refresh_token}
- Validates refresh token signature and expiration
- Checks token type is "refresh"
- Validates token exists in database and not expired
- Generates new access and refresh tokens
- Revokes old refresh token (deletes from database)
- Stores new refresh token in database
- Returns 200 with {access_token, refresh_token} on success
- Returns 400 for missing refresh_token
- Returns 401 for invalid, expired, or revoked token

**Dependencies:** B2.2, B2.5, B2.6

---

### B2.10: Implement Logout Endpoint

**Title:** Create POST /api/auth/logout endpoint

**Acceptance Criteria:**
- Endpoint: `POST /api/auth/logout`
- Requires authentication (uses get_current_user)
- Accepts JSON body: {refresh_token}
- Validates access token
- Deletes refresh token from database
- Returns 204 No Content on success
- Returns 400 for missing refresh_token
- Returns 401 for invalid access token

**Dependencies:** B2.3, B2.5, B2.6

---

### B2.11: Register Authentication Routes in FastAPI App

**Title:** Create main FastAPI app and register auth routes

**Acceptance Criteria:**
- `backend/main.py` exists
- Creates FastAPI application instance
- Registers auth router from `backend.api.auth`
- Includes all auth endpoints:
  - POST /api/auth/register
  - POST /api/auth/login
  - POST /api/auth/refresh
  - POST /api/auth/logout
- App can start with uvicorn
- Routes accessible at correct paths

**Dependencies:** B2.7, B2.8, B2.9, B2.10

---

### B3.1: Create Task Request/Response Models

**Title:** Define Pydantic models for task endpoints

**Acceptance Criteria:**
- `backend/api/tasks.py` exists
- `CreateTaskRequest` Pydantic model:
  - title: str (1-200 chars)
  - description: Optional[str] (max 1000 chars)
- `UpdateTaskRequest` Pydantic model:
  - title: Optional[str] (1-200 chars)
  - description: Optional[str] (max 1000 chars)
  - completed: Optional[bool]
- `TaskResponse` Pydantic model:
  - task: Task model with all fields
- `TasksResponse` Pydantic model:
  - tasks: list[Task model]
  - count: int
- Models validate input correctly

**Dependencies:** None

---

### B3.2: Create Task Database Operations

**Title:** Implement CRUD operations for tasks

**Acceptance Criteria:**
- `backend/db/task_operations.py` exists
- `create_task(user_id: str, title: str, description: str | None) -> Task`:
  - Creates task for user
  - Returns created Task object
- `get_tasks(user_id: str, completed: bool | None) -> list[Task]`:
  - Returns list of tasks for user
  - Filters by completed status if provided
  - All queries include user_id filter
- `get_task_by_id(task_id: str, user_id: str) -> Task | None`:
  - Returns task if exists and belongs to user
  - Returns None if not found or wrong user
- `update_task(task_id: str, user_id: str, data: dict) -> Task | None`:
  - Updates task if exists and belongs to user
  - Returns updated Task or None
- `toggle_task(task_id: str, user_id: str) -> Task | None`:
  - Toggles completed status
  - Returns updated Task or None
- `delete_task(task_id: str, user_id: str) -> bool`:
  - Deletes task if exists and belongs to user
  - Returns True if deleted, False otherwise
- All operations enforce user ownership

**Dependencies:** B1.3, B1.6

---

### B3.3: Implement GET /api/tasks Endpoint

**Title:** Create endpoint to get all tasks for authenticated user

**Acceptance Criteria:**
- Endpoint: `GET /api/tasks`
- Requires authentication (uses get_current_user)
- Accepts optional query parameter `completed` (true/false)
- Filters tasks by user_id from current user
- Applies completed filter if provided
- Returns 200 with TasksResponse
- Returns 401 for missing/invalid authentication

**Dependencies:** B2.3, B3.1, B3.2

---

### B3.4: Implement GET /api/tasks/{task_id} Endpoint

**Title:** Create endpoint to get specific task

**Acceptance Criteria:**
- Endpoint: `GET /api/tasks/{task_id}`
- Requires authentication
- Validates task_id is valid UUID
- Fetches task by ID and user_id
- Returns 200 with TaskResponse if task exists and belongs to user
- Returns 401 for missing/invalid authentication
- Returns 403 if task belongs to different user
- Returns 404 if task not found

**Dependencies:** B2.3, B3.1, B3.2

---

### B3.5: Implement POST /api/tasks Endpoint

**Title:** Create endpoint to create new task

**Acceptance Criteria:**
- Endpoint: `POST /api/tasks`
- Requires authentication
- Accepts JSON body: {title, description?}
- Validates title (1-200 chars) and description (max 1000 chars)
- Creates task for authenticated user
- Returns 201 with TaskResponse on success
- Returns 400 for invalid input
- Returns 401 for missing/invalid authentication

**Dependencies:** B2.3, B3.1, B3.2

---

### B3.6: Implement PUT /api/tasks/{task_id} Endpoint

**Title:** Create endpoint to update task

**Acceptance Criteria:**
- Endpoint: `PUT /api/tasks/{task_id}`
- Requires authentication
- Validates task_id is valid UUID
- Accepts JSON body with optional fields: title, description, completed
- At least one field must be provided
- Validates provided fields
- Updates task if exists and belongs to user
- Returns 200 with TaskResponse on success
- Returns 400 for no fields or invalid input
- Returns 401 for missing/invalid authentication
- Returns 403 if task belongs to different user
- Returns 404 if task not found

**Dependencies:** B2.3, B3.1, B3.2

---

### B3.7: Implement PATCH /api/tasks/{task_id}/toggle Endpoint

**Title:** Create endpoint to toggle task completion

**Acceptance Criteria:**
- Endpoint: `PATCH /api/tasks/{task_id}/toggle`
- Requires authentication
- Validates task_id is valid UUID
- Toggles completed status (true <-> false)
- Updates task if exists and belongs to user
- Returns 200 with TaskResponse on success
- Returns 401 for missing/invalid authentication
- Returns 403 if task belongs to different user
- Returns 404 if task not found

**Dependencies:** B2.3, B3.1, B3.2

---

### B3.8: Implement DELETE /api/tasks/{task_id} Endpoint

**Title:** Create endpoint to delete task

**Acceptance Criteria:**
- Endpoint: `DELETE /api/tasks/{task_id}`
- Requires authentication
- Validates task_id is valid UUID
- Deletes task if exists and belongs to user
- Returns 204 No Content on success
- Returns 401 for missing/invalid authentication
- Returns 403 if task belongs to different user
- Returns 404 if task not found

**Dependencies:** B2.3, B3.1, B3.2

---

### B3.9: Register Task Routes in FastAPI App

**Title:** Register task routes in main FastAPI app

**Acceptance Criteria:**
- Task router from `backend.api.tasks` registered in `backend/main.py`
- All task endpoints accessible:
  - GET /api/tasks
  - GET /api/tasks/{task_id}
  - POST /api/tasks
  - PUT /api/tasks/{task_id}
  - PATCH /api/tasks/{task_id}/toggle
  - DELETE /api/tasks/{task_id}
- Routes work correctly with authentication

**Dependencies:** B2.11, B3.3, B3.4, B3.5, B3.6, B3.7, B3.8

---

### B4.1: Configure CORS Middleware

**Title:** Enable CORS for frontend-backend communication

**Acceptance Criteria:**
- CORSMiddleware added to FastAPI app in `backend/main.py`
- Configuration:
  - allow_origins: ["http://localhost:3000"]
  - allow_credentials: true
  - allow_methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
  - allow_headers: ["Content-Type", "Authorization"]
- Preflight OPTIONS requests succeed
- Frontend can make requests to backend

**Dependencies:** B2.11, B3.9

---

### B4.2: Backend Manual Testing

**Title:** Test all backend functionality manually

**Acceptance Criteria:**
- Backend server starts successfully with uvicorn
- Test auth flow:
  - Register user returns tokens
  - Login returns tokens
  - Refresh token returns new tokens
  - Logout revokes token
- Test task operations:
  - Create task works
  - Get all tasks works
  - Get specific task works
  - Update task works
  - Toggle task works
  - Delete task works
- Test security:
  - No token returns 401
  - Invalid token returns 401
  - Cross-user access blocked
- All error responses match specification

**Dependencies:** B4.1

---

## 2. Frontend Tasks

### F1.1: Initialize Next.js Project

**Title:** Create Next.js frontend project structure

**Acceptance Criteria:**
- `frontend/` directory exists
- Next.js project initialized with App Router
- TypeScript enabled
- ESLint enabled
- Tailwind CSS enabled (optional)
- Directory structure created:
  - `app/` with layout.tsx and page.tsx
  - `app/login/` with page.tsx
  - `app/register/` with page.tsx
  - `app/dashboard/` with page.tsx
  - `components/` directory
  - `lib/` directory
- `.env.local` created with NEXT_PUBLIC_API_URL=http://localhost:8000
- `.gitignore` excludes .env.local and build artifacts
- Development server starts with npm run dev

**Dependencies:** B4.2 (backend ready)

---

### F1.2: Create TypeScript Type Definitions

**Title:** Define TypeScript interfaces matching backend API

**Acceptance Criteria:**
- `frontend/lib/types.ts` exists
- Defines all interfaces from frontend.md:
  - User, Task, AuthResponse
  - LoginRequest, RegisterRequest
  - CreateTaskRequest, UpdateTaskRequest
  - TasksResponse, TaskResponse
  - ErrorResponse
- Types match backend Pydantic models exactly
- All types can be imported without errors

**Dependencies:** F1.1

---

### F1.3: Create API Client Helper Function

**Title:** Implement fetchAPI helper with token handling

**Acceptance Criteria:**
- `frontend/lib/api.ts` exists
- `fetchAPI<T>()` function implemented:
  - Accepts endpoint and options
  - Reads access_token from localStorage
  - Adds Authorization header
  - Makes HTTP request to backend
  - Handles JSON responses
  - Handles 204 No Content
  - Throws error for non-OK responses
  - Includes error details in thrown errors
- API_BASE_URL configured from environment variable

**Dependencies:** F1.2

---

### F1.4: Create Auth API Functions

**Title:** Implement authentication API calls

**Acceptance Criteria:**
- `register()` function in `frontend/lib/api.ts`:
  - Calls POST /api/auth/register
  - Accepts username and password
  - Returns AuthResponse
- `login()` function in `frontend/lib/api.ts`:
  - Calls POST /api/auth/login
  - Accepts username and password
  - Returns AuthResponse
- `refreshToken()` function in `frontend/lib/api.ts`:
  - Calls POST /api/auth/refresh
  - Accepts refresh_token string
  - Returns {access_token, refresh_token}
- `logout()` function in `frontend/lib/api.ts`:
  - Calls POST /api/auth/logout
  - Accepts refresh_token string
  - Returns void
- All functions use fetchAPI helper

**Dependencies:** F1.3

---

### F1.5: Create Task API Functions

**Title:** Implement task API calls

**Acceptance Criteria:**
- `getTasks()` function in `frontend/lib/api.ts`:
  - Calls GET /api/tasks
  - Accepts optional filter object {completed?: boolean}
  - Returns TasksResponse
- `getTask()` function in `frontend/lib/api.ts`:
  - Calls GET /api/tasks/{task_id}
  - Returns TaskResponse
- `createTask()` function in `frontend/lib/api.ts`:
  - Calls POST /api/tasks
  - Accepts title and optional description
  - Returns TaskResponse
- `updateTask()` function in `frontend/lib/api.ts`:
  - Calls PUT /api/tasks/{task_id}
  - Accepts task_id and data object
  - Returns TaskResponse
- `toggleTask()` function in `frontend/lib/api.ts`:
  - Calls PATCH /api/tasks/{task_id}/toggle
  - Accepts task_id
  - Returns TaskResponse
- `deleteTask()` function in `frontend/lib/api.ts`:
  - Calls DELETE /api/tasks/{task_id}
  - Accepts task_id
  - Returns void
- All functions use fetchAPI helper

**Dependencies:** F1.3

---

### F1.6: Implement Token Refresh Logic

**Title:** Add automatic token refresh to fetchAPI

**Acceptance Criteria:**
- `fetchAPI()` updated to handle token refresh:
  - Checks if token expires within 5 minutes
  - Automatically refreshes if expiring soon
  - On 401 response, attempts token refresh
  - Retries original request with new token
  - If refresh fails, clears auth and redirects to /login
- `isTokenExpiringSoon()` helper function implemented
- `refreshAccessToken()` helper function implemented
- Updates localStorage with new tokens
- Token refresh is transparent to caller

**Dependencies:** F1.4, F1.5

---

### F1.7: Create Auth Utilities

**Title:** Implement authentication state management utilities

**Acceptance Criteria:**
- `frontend/lib/auth.ts` exists
- `isAuthenticated()` function:
  - Returns true if access_token exists and valid
  - Returns false otherwise
- `getAuth()` function:
  - Returns StoredAuth object or null
  - Reads from localStorage
- `setAuth()` function:
  - Stores auth data in localStorage
  - Accepts StoredAuth object
- `clearAuth()` function:
  - Removes all auth data from localStorage
- `isTokenValid()` function:
  - Decodes JWT and checks expiration
  - Returns true if not expired, false otherwise
- `getCurrentUser()` function:
  - Returns {user_id, username} or null
  - Reads from localStorage

**Dependencies:** F1.2

---

### F1.8: Create ProtectedRoute Component

**Title:** Implement route protection wrapper component

**Acceptance Criteria:**
- `frontend/components/ProtectedRoute.tsx` exists
- Client-side component ('use client')
- Props: {children: React.ReactNode}
- Uses useRouter from next/navigation
- On mount:
  - Checks isAuthenticated()
  - Redirects to /login if not authenticated
  - Renders children if authenticated
- Shows loading state during redirect check
- Exported as function component

**Dependencies:** F1.7

---

### F1.9: Create AuthForm Component

**Title:** Implement reusable authentication form

**Acceptance Criteria:**
- `frontend/components/AuthForm.tsx` exists
- Client-side component
- Props: {mode: 'login' | 'register', onSuccess?: () => void}
- State: username, password, confirmPassword, loading, error
- Form fields based on mode:
  - Login: username, password
  - Register: username, password, confirmPassword
- Client-side validation:
  - Username: 3-50 chars, alphanumeric + underscores
  - Password: minimum 8 chars
  - Confirm password: matches password (register only)
- Submit button disabled during loading
- Error message display
- Link between login and register pages
- Calls appropriate API function (login/register)
- On success:
  - Stores tokens in localStorage using setAuth()
  - Redirects to /dashboard
  - Calls onSuccess callback if provided
- On error: displays error message

**Dependencies:** F1.4, F1.7

---

### F2.1: Create Landing Page

**Title:** Implement root page with smart redirect

**Acceptance Criteria:**
- `frontend/app/page.tsx` updated
- Client-side component
- Uses useRouter from next/navigation
- On mount:
  - Checks isAuthenticated()
  - Redirects to /dashboard if authenticated
  - Redirects to /login if not authenticated
- Shows "Loading..." during redirect check

**Dependencies:** F1.7

---

### F2.2: Create Login Page

**Title:** Implement login interface

**Acceptance Criteria:**
- `frontend/app/login/page.tsx` exists
- Uses AuthForm component with mode="login"
- Redirects to /dashboard if already authenticated
- Link to registration page
- Page title: "Login"

**Dependencies:** F1.7, F1.9

---

### F2.3: Create Registration Page

**Title:** Implement registration interface

**Acceptance Criteria:**
- `frontend/app/register/page.tsx` exists
- Uses AuthForm component with mode="register"
- Redirects to /dashboard if already authenticated
- Link to login page
- Page title: "Register"

**Dependencies:** F1.7, F1.9

---

### F2.4: Create Navbar Component

**Title:** Implement navigation bar

**Acceptance Criteria:**
- `frontend/components/Navbar.tsx` exists
- Displays application title ("Todo App")
- Displays current username from localStorage
- Logout button:
  - Calls logout() API
  - Calls clearAuth()
  - Redirects to /login
- Responsive layout (basic flexbox)
- Styled with Tailwind CSS (or basic CSS)

**Dependencies:** F1.4, F1.7

---

### F2.5: Create TaskItem Component

**Title:** Implement individual task display component

**Acceptance Criteria:**
- `frontend/components/TaskItem.tsx` exists
- Props: {task: Task, onToggle: () => void, onDelete: () => void}
- Displays task title
- Displays description (if present)
- Checkbox for toggle completion
- Delete button
- Styling:
  - Completed tasks: strikethrough on title, gray color
  - Incomplete tasks: normal styling
- Calls onToggle when checkbox clicked
- Calls onDelete when delete button clicked

**Dependencies:** F1.2

---

### F2.6: Create TaskList Component

**Title:** Implement task list container component

**Acceptance Criteria:**
- `frontend/components/TaskList.tsx` exists
- Props: {tasks: Task[], onToggle: (id: string) => void, onDelete: (id: string) => void, loading?: boolean}
- Renders TaskItem component for each task
- Displays empty state message if tasks array is empty
- Displays loading spinner if loading prop is true
- Passes toggle and delete callbacks to TaskItem components
- Styled with Tailwind CSS (or basic CSS)

**Dependencies:** F2.5

---

### F2.7: Create TaskForm Component

**Title:** Implement add task form component

**Acceptance Criteria:**
- `frontend/components/TaskForm.tsx` exists
- Props: {onSubmit: (title: string, description?: string) => void, loading?: boolean}
- Form fields:
  - Title input (required, max 200 chars)
  - Description textarea (optional, max 1000 chars)
- Submit button
- Client-side validation:
  - Title required (1-200 chars)
  - Description optional (max 1000 chars if provided)
- Submit button disabled during loading
- On submit:
  - Calls onSubmit with title and description
  - Clears form fields

**Dependencies:** F1.2

---

### F2.8: Create Dashboard Page

**Title:** Implement main todo list interface

**Acceptance Criteria:**
- `frontend/app/dashboard/page.tsx` exists
- Wrapped with ProtectedRoute component
- Uses Navbar component
- Uses TaskForm component
- Uses TaskList component
- State:
  - tasks: Task[]
  - filter: 'all' | 'active' | 'completed'
  - loading: boolean
  - error: string | null
- Fetches tasks on mount and when filter changes
- Filters tasks based on selected filter:
  - All: all tasks
  - Active: only completed=false
  - Completed: only completed=true
- Functions:
  - handleCreateTask(): calls createTask() API, refreshes tasks
  - handleToggleTask(): calls toggleTask() API, refreshes tasks
  - handleDeleteTask(): calls deleteTask() API, refreshes tasks
  - fetchTasks(): calls getTasks() API, updates state
- Filter tabs: All, Active, Completed (buttons to switch filter)
- Displays error message if error state set
- Styled with Tailwind CSS (or basic CSS)

**Dependencies:** F1.5, F1.6, F1.8, F2.4, F2.6, F2.7

---

### F2.9: Create Dashboard Loading State

**Title:** Implement loading indicator for dashboard

**Acceptance Criteria:**
- `frontend/app/dashboard/loading.tsx` exists
- Displays loading spinner or "Loading..." message
- Simple, clean design matching dashboard styling

**Dependencies:** F2.8

---

## 3. Integration Tasks

### I1.1: Start Both Applications

**Title:** Run backend and frontend servers simultaneously

**Acceptance Criteria:**
- Backend server starts: `uvicorn backend.main:app --reload`
- Frontend server starts: `npm run dev`
- Frontend accessible at http://localhost:3000
- Backend accessible at http://localhost:8000
- No errors in console logs for either application

**Dependencies:** B4.2, F2.9

---

### I1.2: Test Authentication Flow End-to-End

**Title:** Test complete authentication flow in browser

**Acceptance Criteria:**
- Register new user:
  - Navigate to /register
  - Enter username and password
  - Submit successfully
  - Redirected to /dashboard
  - Tokens stored in localStorage
- Login with existing user:
  - Logout
  - Navigate to /login
  - Enter credentials
  - Submit successfully
  - Redirected to /dashboard
- Token refresh works transparently
- Logout works:
  - Click logout
  - Redirected to /login
  - localStorage cleared
- Auth persists across page refresh

**Dependencies:** I1.1

---

### I1.3: Test Task Management End-to-End

**Title:** Test complete task lifecycle in browser

**Acceptance Criteria:**
- Create task with title only
- Create task with title and description
- Verify tasks appear in list
- Filter tabs work (All/Active/Completed)
- Toggle task completion works
- Update task works (if implemented)
- Delete task works
- Multiple tasks can be managed
- Task state persists across page refresh

**Dependencies:** I1.2

---

### I1.4: Test Multi-User Data Isolation

**Title:** Verify users cannot access each other's data

**Acceptance Criteria:**
- Create User A, create 3 tasks
- Logout User A
- Create User B
- User B cannot see User A's tasks
- Create tasks for User B
- Logout User B
- Login User A
- User A's tasks still present
- User A cannot see User B's tasks
- Cross-user API access blocked (404/403)

**Dependencies:** I1.3

---

### I1.5: Test Error Handling

**Title:** Verify error scenarios and user feedback

**Acceptance Criteria:**
- Login with wrong password shows error
- Register with existing username shows error
- Access protected route without token shows error
- Create task without title shows error
- Access non-existent task shows error
- Access other user's task shows error
- Network errors show user-friendly messages
- No crashes or unhandled exceptions

**Dependencies:** I1.4

---

## 4. Verification Tasks

### V1.1: Specification Compliance Check

**Title:** Verify all specifications are met

**Acceptance Criteria:**
- Review overview.md: All goals achieved
- Review auth.md: JWT flow implemented correctly
- Review backend-api.md: All endpoints match specification
- Review database.md: Models and queries match specification
- Review frontend.md: All pages and components implemented
- Review security.md: All security rules followed
- Review non-goals.md: No out-of-scope features added

**Dependencies:** I1.5

---

### V1.2: Code Quality Review

**Title:** Review code for quality and maintainability

**Acceptance Criteria:**
- Backend code has proper error handling
- Frontend code has proper TypeScript types
- Code is readable and follows best practices
- No obvious bugs or issues
- Comments where necessary
- Clean code structure

**Dependencies:** V1.1

---

### V1.3: Final Integration Test

**Title:** Complete end-to-end test of entire application

**Acceptance Criteria:**
- Fresh browser localStorage
- Both servers restarted
- Complete user journey works:
  - Register → Login → Create tasks → Complete tasks → Logout
- Second user journey works
- Data isolation verified
- No errors in console
- Application ready for demonstration

**Dependencies:** V1.2
