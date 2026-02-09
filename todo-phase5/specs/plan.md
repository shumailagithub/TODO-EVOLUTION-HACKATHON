# Implementation Plan - Phase-2

## Overview

This plan defines the step-by-step implementation order for Phase-2 of the Todo Application. The plan follows the backend-first approach, with authentication implemented before task CRUD operations.

**Principles:**
1. Backend before frontend
2. Database before business logic
3. Authentication before task operations
4. Incremental testing at each step
5. No Phase-1 code modification

---

## Phase 1: Backend Setup

### Step 1.1: Initialize Backend Project

**Goal:** Set up FastAPI project structure and dependencies

**Tasks:**
1. Create `backend/` directory
2. Initialize Python project with `pyproject.toml`
3. Install dependencies:
   - `fastapi`
   - `uvicorn` (ASGI server)
   - `sqlmodel`
   - `psycopg2-binary` (PostgreSQL adapter)
   - `pydantic` (built into FastAPI)
   - `python-jose[cryptography]` (JWT handling)
   - `passlib[bcrypt]` (password hashing)
   - `python-multipart` (form data)
   - `python-dotenv` (environment variables)
4. Create directory structure:
   ```
   backend/
   ├── main.py
   ├── models/
   ├── auth/
   ├── api/
   ├── db/
   └── config/
   ```
5. Create `.env.example` with required environment variables
6. Create `.gitignore` to exclude `.env` and Python cache

**Verification:**
- `pip list` shows all installed packages
- Directory structure matches spec

---

### Step 1.2: Database Configuration

**Goal:** Set up database connection and session management

**Tasks:**
1. Create `backend/config.py` with environment variable loading
2. Create `backend/db/connection.py` with:
   - Database engine setup (SQLAlchemy)
   - Connection pooling configuration
   - Session factory
3. Create `.env` file (not committed) with:
   - `DATABASE_URL` (Neon PostgreSQL connection string)
   - `JWT_SECRET` (generate secure random string)
   - `ACCESS_TOKEN_EXPIRE_MINUTES=15`
   - `REFRESH_TOKEN_EXPIRE_DAYS=7`
   - `BCRYPT_ROUNDS=12`
4. Test database connection in `backend/main.py` with simple health check

**Verification:**
- Can connect to Neon PostgreSQL
- Database connection is established without errors

---

### Step 1.3: Create SQLModel Models

**Goal:** Define database models for users, refresh tokens, and tasks

**Tasks:**
1. Create `backend/models/user.py`:
   - User model with id, username, password_hash, timestamps
   - Proper field types and constraints
2. Create `backend/models/refresh_token.py`:
   - RefreshToken model with user_id, token_id, expires_at
   - Foreign key to User
3. Create `backend/models/task.py`:
   - Task model with id, user_id, title, description, completed, timestamps
   - Foreign key to User
4. Create `backend/models/__init__.py` to export all models
5. Create `backend/db/init.py` with `create_tables()` function

**Verification:**
- All models follow database.md specification
- Models can be imported without errors
- Fields have correct types and constraints

---

### Step 1.4: Initialize Database Tables

**Goal:** Create tables in PostgreSQL database

**Tasks:**
1. Create script `backend/db/init_db.py` that:
   - Imports all models
   - Creates all tables using `SQLModel.metadata.create_all()`
   - Prints success message
2. Run the script to initialize database
3. Verify tables created in Neon dashboard or via SQL client

**Verification:**
- `users`, `refresh_tokens`, `tasks` tables exist in database
- Table structure matches models (columns, types, constraints, indexes)

---

## Phase 2: Authentication Implementation

### Step 2.1: Password Hashing Utilities

**Goal:** Implement password hashing and verification functions

**Tasks:**
1. Create `backend/auth/password.py` with:
   - `hash_password(password: str) -> str` function
   - `verify_password(plain: str, hashed: str) -> bool` function
   - Use bcrypt with 12 rounds
2. Write simple test script to verify hashing works

**Verification:**
- Password hashing produces different hash each time (due to salt)
- Password verification correctly matches valid passwords
- Password verification rejects invalid passwords

---

### Step 2.2: JWT Token Utilities

**Goal:** Implement JWT token generation and validation

**Tasks:**
1. Create `backend/auth/tokens.py` with:
   - `generate_access_token(user_id: str) -> str`
   - `generate_refresh_token(user_id: str) -> str`
   - `decode_token(token: str) -> dict`
2. Include proper claims:
   - `sub`: user_id
   - `exp`: expiration timestamp
   - `iat`: issued at timestamp
   - `type`: "access" or "refresh"
   - `jti`: unique ID for refresh tokens
3. Use environment `JWT_SECRET` for signing

**Verification:**
- Access tokens expire after 15 minutes
- Refresh tokens expire after 7 days
- Tokens can be decoded and claims validated
- Invalid tokens raise exceptions

---

### Step 2.3: Authentication Dependencies

**Goal:** Create FastAPI dependencies for protected routes

**Tasks:**
1. Create `backend/auth/dependencies.py` with:
   - `get_access_token()` - extracts token from Authorization header
   - `validate_access_token()` - validates and decodes token
   - `get_current_user()` - returns authenticated User object
2. Handle error cases:
   - Missing token → 401 Unauthorized
   - Invalid token → 401 Unauthorized
   - Expired token → 401 Unauthorized
   - Wrong token type → 401 Unauthorized

**Verification:**
- Protected routes reject requests without token
- Valid tokens grant access
- Invalid tokens are rejected with proper error messages

---

### Step 2.4: User Database Operations

**Goal:** Implement CRUD operations for users

**Tasks:**
1. Create `backend/db/user_operations.py` with:
   - `create_user(username: str, password_hash: str) -> User`
   - `get_user_by_username(username: str) -> User | None`
   - `get_user_by_id(user_id: str) -> User | None`
2. Include proper error handling and session management

**Verification:**
- Can create user and retrieve by username
- Duplicate username raises appropriate error
- Can retrieve user by ID

---

### Step 2.5: Refresh Token Database Operations

**Goal:** Implement CRUD operations for refresh tokens

**Tasks:**
1. Create `backend/db/token_operations.py` with:
   - `create_refresh_token(user_id: str, token_id: str, expires_at: datetime) -> RefreshToken`
   - `get_refresh_token(token_id: str) -> RefreshToken | None`
   - `delete_refresh_token(token_id: str) -> None`
   - `delete_all_user_tokens(user_id: str) -> None`
2. Include validation (token not expired)

**Verification:**
- Can create and retrieve refresh tokens
- Can delete specific token
- Can delete all tokens for a user

---

### Step 2.6: Authentication API Endpoints

**Goal:** Implement auth endpoints (register, login, refresh, logout)

**Tasks:**
1. Create `backend/api/auth.py` with endpoints:
   - `POST /api/auth/register`
   - `POST /api/auth/login`
   - `POST /api/auth/refresh`
   - `POST /api/auth/logout`
2. Follow `backend-api.md` specification
3. Implement request validation using Pydantic models
4. Return proper HTTP status codes and error messages
5. Register routes in `backend/main.py`

**Verification:**
- Register creates user, returns tokens
- Login with valid credentials returns tokens
- Login with invalid credentials returns 401
- Refresh with valid token returns new tokens
- Logout revokes refresh token
- All error messages match specification

---

## Phase 3: Task CRUD Implementation

### Step 3.1: Task Database Operations

**Goal:** Implement CRUD operations for tasks

**Tasks:**
1. Create `backend/db/task_operations.py` with:
   - `create_task(user_id: str, title: str, description: str | None) -> Task`
   - `get_tasks(user_id: str, completed: bool | None) -> list[Task]`
   - `get_task_by_id(task_id: str, user_id: str) -> Task | None`
   - `update_task(task_id: str, user_id: str, data: dict) -> Task | None`
   - `toggle_task(task_id: str, user_id: str) -> Task | None`
   - `delete_task(task_id: str, user_id: str) -> bool`
2. **CRITICAL:** All operations MUST include user_id for data isolation
3. Return None if task not found or doesn't belong to user

**Verification:**
- Can create task for specific user
- Can retrieve only user's own tasks
- Cannot access other users' tasks (returns None)
- Can update only own tasks
- Can delete only own tasks
- Toggle updates completed status

---

### Step 3.2: Task API Endpoints

**Goal:** Implement task API endpoints

**Tasks:**
1. Create `backend/api/tasks.py` with endpoints:
   - `GET /api/tasks`
   - `GET /api/tasks/{task_id}`
   - `POST /api/tasks`
   - `PUT /api/tasks/{task_id}`
   - `PATCH /api/tasks/{task_id}/toggle`
   - `DELETE /api/tasks/{task_id}`
2. Follow `backend-api.md` specification
3. Apply `get_current_user()` dependency to all endpoints
4. Implement ownership checks before operations
5. Return 404 for non-existent tasks
6. Return 403 for cross-user access attempts
7. Register routes in `backend/main.py`

**Verification:**
- All endpoints require authentication
- Users can only access their own tasks
- Cross-user access returns 403
- All CRUD operations work correctly
- Error responses match specification
- GET /api/tasks with filter works

---

### Step 3.3: CORS Configuration

**Goal:** Enable cross-origin requests from frontend

**Tasks:**
1. Add CORSMiddleware to `backend/main.py`
2. Configure:
   - Allow origin: `http://localhost:3000`
   - Allow credentials: true
   - Allow methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
   - Allow headers: Content-Type, Authorization

**Verification:**
- Frontend can make requests to backend
- Preflight OPTIONS requests succeed
- Authorization headers are allowed

---

### Step 3.4: Backend Testing and Verification

**Goal:** Manual testing of all backend functionality

**Tasks:**
1. Start backend server: `uvicorn backend.main:app --reload`
2. Test authentication flow:
   - Register user → get tokens
   - Login user → get tokens
   - Refresh token → get new tokens
   - Logout → revoke token
3. Test task operations:
   - Create task
   - Get all tasks
   - Get specific task
   - Update task
   - Toggle task completion
   - Delete task
4. Test security:
   - Attempt access without token → 401
   - Attempt access with expired token → 401
   - Create second user
   - Attempt to access other user's tasks → 404 (not found) or 403
5. Use Postman, curl, or browser DevTools for testing

**Verification:**
- All authentication endpoints work
- All task endpoints work
- Security checks work correctly
- Error messages match specification

---

## Phase 4: Frontend Setup

### Step 4.1: Initialize Next.js Project

**Goal:** Set up Next.js frontend project

**Tasks:**
1. Create `frontend/` directory
2. Initialize Next.js project:
   - `npx create-next-app@latest frontend`
   - Select: TypeScript, App Router, ESLint, Tailwind (optional)
3. Install additional dependencies (if needed):
   - Axios (optional, can use fetch API)
4. Create directory structure:
   ```
   frontend/
   ├── app/
   │   ├── layout.tsx
   │   ├── page.tsx
   │   ├── login/
   │   │   └── page.tsx
   │   ├── register/
   │   │   └── page.tsx
   │   └── dashboard/
   │       └── page.tsx
   ├── components/
   ├── lib/
   └── public/
   ```
5. Create `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`
6. Create `.gitignore` to exclude `.env.local` and build artifacts

**Verification:**
- Next.js development server starts: `npm run dev`
- Access `http://localhost:3000` shows default page
- TypeScript compiles without errors

---

### Step 4.2: Create TypeScript Types

**Goal:** Define TypeScript interfaces matching backend API

**Tasks:**
1. Create `frontend/lib/types.ts` with all interfaces from `frontend.md`:
   - User, Task, AuthResponse
   - Request types (LoginRequest, RegisterRequest, etc.)
   - Response types (TasksResponse, TaskResponse)
   - ErrorResponse
2. Ensure types match backend Pydantic models exactly

**Verification:**
- All types can be imported
- TypeScript compiler accepts types without errors

---

### Step 4.3: Create API Client

**Goal:** Implement API client functions

**Tasks:**
1. Create `frontend/lib/api.ts` with:
   - `fetchAPI()` helper function
   - Auth functions: `register()`, `login()`, `refreshToken()`, `logout()`
   - Task functions: `getTasks()`, `getTask()`, `createTask()`, `updateTask()`, `toggleTask()`, `deleteTask()`
2. Implement automatic token refresh logic
3. Handle errors and throw appropriate exceptions
4. Follow `frontend.md` specification exactly

**Verification:**
- Can import and use all API functions
- Functions call correct backend endpoints
- Authorization header is included
- Token refresh works on 401 responses

---

### Step 4.4: Create Auth Utilities

**Goal:** Implement authentication state management utilities

**Tasks:**
1. Create `frontend/lib/auth.ts` with:
   - `isAuthenticated()` - check if user is logged in
   - `getAuth()` - get stored auth data
   - `setAuth()` - store auth data in localStorage
   - `clearAuth()` - clear auth data from localStorage
   - `isTokenValid()` - check if token is expired
   - `getCurrentUser()` - get current user info

**Verification:**
- Functions correctly interact with localStorage
- Token validation works correctly
- Can store and retrieve auth data

---

### Step 4.5: Create Protected Route Component

**Goal:** Implement route protection wrapper

**Tasks:**
1. Create `frontend/components/ProtectedRoute.tsx` with:
   - Check authentication status
   - Redirect to `/login` if not authenticated
   - Render children if authenticated
2. Follow implementation from `frontend.md`

**Verification:**
- Unauthenticated users are redirected to login
- Authenticated users can access protected content

---

### Step 4.6: Create Auth Form Component

**Goal:** Implement reusable authentication form

**Tasks:**
1. Create `frontend/components/AuthForm.tsx` with:
   - Props: `mode: 'login' | 'register'`
   - Form fields: username, password, confirmPassword (register only)
   - Client-side validation
   - Loading state
   - Error display
   - Call appropriate API function
   - Redirect to dashboard on success
2. Follow `frontend.md` specification

**Verification:**
- Login form accepts credentials and calls API
- Register form accepts credentials and calls API
- Validation prevents invalid submissions
- Error messages display correctly
- Success redirects to dashboard

---

## Phase 5: Frontend Pages Implementation

### Step 5.1: Create Landing Page

**Goal:** Implement root page with smart redirect

**Tasks:**
1. Update `frontend/app/page.tsx`:
   - Check authentication status on mount
   - Redirect to `/dashboard` if authenticated
   - Redirect to `/login` if not authenticated
2. Show loading state during redirect

**Verification:**
- Authenticated users redirected to `/dashboard`
- Non-authenticated users redirected to `/login`

---

### Step 5.2: Create Login Page

**Goal:** Implement login interface

**Tasks:**
1. Create `frontend/app/login/page.tsx`:
   - Use `AuthForm` component with mode="login"
   - Link to registration page
   - Redirect to `/dashboard` if already authenticated
2. Ensure proper error handling

**Verification:**
- Login form displays correctly
- Successful login redirects to dashboard
- Login with invalid credentials shows error
- Link to registration page works

---

### Step 5.3: Create Registration Page

**Goal:** Implement registration interface

**Tasks:**
1. Create `frontend/app/register/page.tsx`:
   - Use `AuthForm` component with mode="register"
   - Link to login page
   - Redirect to `/dashboard` if already authenticated
2. Ensure proper error handling

**Verification:**
- Registration form displays correctly
- Password confirmation validation works
- Successful registration redirects to dashboard
- Registration with existing username shows error
- Link to login page works

---

### Step 5.4: Create Navbar Component

**Goal:** Implement navigation bar

**Tasks:**
1. Create `frontend/components/Navbar.tsx`:
   - Display application title
   - Display current username
   - Logout button (calls `logout()`, redirects to `/login`)
   - Responsive layout (basic)

**Verification:**
- Navbar displays correctly on dashboard
- Username shows correctly
- Logout button works and redirects

---

### Step 5.5: Create Task Item Component

**Goal:** Implement individual task display

**Tasks:**
1. Create `frontend/components/TaskItem.tsx`:
   - Display task title
   - Display description (if present)
   - Checkbox for toggle completion
   - Delete button
   - Style completed tasks differently (strikethrough, gray)
   - Accept props: `task`, `onToggle`, `onDelete`

**Verification:**
- Task displays correctly
- Completed tasks have visual distinction
- Toggle checkbox works
- Delete button works

---

### Step 5.6: Create Task List Component

**Goal:** Implement task list container

**Tasks:**
1. Create `frontend/components/TaskList.tsx`:
   - Accept tasks array
   - Render TaskItem components
   - Display empty state message if no tasks
   - Show loading spinner if loading
   - Handle toggle and delete callbacks

**Verification:**
- Tasks render correctly
- Empty state shows when no tasks
- Loading state shows during operations
- Task callbacks work correctly

---

### Step 5.7: Create Task Form Component

**Goal:** Implement add task form

**Tasks:**
1. Create `frontend/components/TaskForm.tsx`:
   - Title input (required, max 200 chars)
   - Description textarea (optional, max 1000 chars)
   - Submit button
   - Client-side validation
   - Loading state during submission
   - Call `createTask()` API
   - Clear form on success
   - Accept prop: `onSubmit`

**Verification:**
- Form accepts title and optional description
- Validation prevents empty submissions
- Submission creates task via API
- Form clears after successful submission
- Loading state shows during API call

---

### Step 5.8: Create Dashboard Page

**Goal:** Implement main todo list interface

**Tasks:**
1. Create `frontend/app/dashboard/page.tsx`:
   - Wrap with `ProtectedRoute`
   - Use `Navbar` component
   - Use `TaskForm` component
   - Use `TaskList` component
   - Implement state: `tasks`, `filter`, `loading`, `error`
   - Fetch tasks on mount and filter change
   - Handle task operations: create, toggle, delete
   - Display error messages
   - Implement filter tabs (All/Active/Completed)
2. Ensure proper error handling

**Verification:**
- Dashboard displays correctly for authenticated users
- Tasks load from API
- Filter tabs work (All/Active/Completed)
- Add task creates new task
- Toggle task updates completion status
- Delete task removes task
- Logout button works
- Error messages display correctly
- Loading states show during operations

---

### Step 5.9: Create Loading State

**Goal:** Implement loading indicator for dashboard

**Tasks:**
1. Create `frontend/app/dashboard/loading.tsx`:
   - Display loading spinner or message
   - Match dashboard styling

**Verification:**
- Loading state displays before dashboard loads
- Transitions smoothly to dashboard

---

## Phase 6: Integration and Testing

### Step 6.1: Start Both Applications

**Goal:** Run backend and frontend simultaneously

**Tasks:**
1. Start backend: Terminal 1
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
2. Start frontend: Terminal 2
   ```bash
   cd frontend
   npm run dev
   ```
3. Access frontend at `http://localhost:3000`

**Verification:**
- Both applications start successfully
- No errors in console logs
- Frontend can access backend API

---

### Step 6.2: End-to-End Authentication Flow

**Goal:** Test complete authentication flow

**Tasks:**
1. Register new user:
   - Navigate to `/register`
   - Enter username and password
   - Submit
   - Verify redirect to `/dashboard`
   - Verify tokens stored in localStorage
2. Login with existing user:
   - Logout (if logged in)
   - Navigate to `/login`
   - Enter credentials
   - Submit
   - Verify redirect to `/dashboard`
3. Test token refresh:
   - Wait for access token to expire (or simulate)
   - Perform API call
   - Verify automatic token refresh happens
   - Verify request succeeds with new token
4. Test logout:
   - Click logout button
   - Verify redirect to `/login`
   - Verify localStorage cleared

**Verification:**
- Registration works
- Login works
- Token refresh works transparently
- Logout works
- Auth state persists across page refresh

---

### Step 6.3: End-to-End Task Management

**Goal:** Test complete task lifecycle

**Tasks:**
1. Create task:
   - Add task with title only
   - Add task with title and description
   - Verify task appears in list
2. View tasks:
   - Switch between All/Active/Completed filters
   - Verify correct tasks shown
3. Complete task:
   - Toggle task checkbox
   - Verify task moves to Completed filter
4. Update task (if implemented):
   - Edit task title/description
   - Verify updates persist
5. Delete task:
   - Delete task
   - Verify task removed from list
6. Test multiple tasks:
   - Create several tasks
   - Complete some
   - Delete some
   - Verify all operations work correctly

**Verification:**
- Create, read, update, delete operations work
- Filters work correctly
- Task state persists across page refresh
- All tasks belong to correct user

---

### Step 6.4: Multi-User Data Isolation Test

**Goal:** Verify users cannot access each other's data

**Tasks:**
1. Create two user accounts:
   - User A: "alice"
   - User B: "bob"
2. Login as User A:
   - Create 3 tasks
   - Note task IDs
3. Logout User A
4. Login as User B:
   - Attempt to access User A's task IDs via direct API calls
   - Verify 404 or 403 responses
   - Verify User B sees only their own tasks
   - Create 3 tasks
5. Logout User B
6. Login as User A:
   - Verify User A's tasks are still there
   - Verify User A cannot see User B's tasks

**Verification:**
- Users can only see their own tasks
- Cross-user access is blocked (404/403)
- Data isolation is enforced
- Users' task collections are independent

---

### Step 6.5: Error Handling Verification

**Goal:** Test error scenarios and user feedback

**Tasks:**
1. Test authentication errors:
   - Login with wrong password
   - Register with existing username
   - Access protected route without token
   - Use expired token
2. Test task errors:
   - Create task without title
   - Create task with title > 200 chars
   - Access non-existent task
   - Access other user's task
3. Test network errors:
   - Stop backend server
   - Try to make API calls
   - Verify error messages display

**Verification:**
- All error scenarios show user-friendly messages
- Error messages match specification
- Application handles errors gracefully
- No crashes or unhandled exceptions

---

### Step 6.6: Cross-Browser Testing (Optional)

**Goal:** Verify compatibility across browsers

**Tasks:**
1. Test in Chrome
2. Test in Firefox
3. Test in Edge (if available)
4. Verify basic functionality works in all browsers

**Verification:**
- Core features work in all tested browsers
- Styling renders correctly
- No browser-specific issues

---

## Phase 7: Final Verification

### Step 7.1: Specification Compliance Check

**Goal:** Verify all specifications are met

**Tasks:**
1. Review `overview.md`: All goals achieved
2. Review `auth.md`: JWT flow implemented correctly
3. Review `backend-api.md`: All endpoints match specification
4. Review `database.md`: Models and queries match specification
5. Review `frontend.md`: All pages and components implemented
6. Review `security.md`: All security rules followed
7. Review `non-goals.md`: No out-of-scope features added

**Verification:**
- All spec requirements met
- No features added from non-goals
- API contracts match exactly
- Security rules enforced

---

### Step 7.2: Code Quality Check

**Goal:** Ensure code is clean and maintainable

**Tasks:**
1. Review backend code:
   - Proper error handling
   - Clean code structure
   - Clear variable/function names
   - Comments where necessary
2. Review frontend code:
   - Proper TypeScript types
   - Clean component structure
   - Proper state management
   - No obvious bugs

**Verification:**
- Code follows Python and TypeScript best practices
- No obvious bugs or issues
- Code is readable and maintainable

---

### Step 7.3: Documentation Check

**Goal:** Ensure environment setup is clear

**Tasks:**
1. Verify `backend/.env.example` has all required variables
2. Verify `frontend/.env.local.example` exists (if used)
3. Verify README instructions (if created)

**Verification:**
- Environment variables documented
- Setup instructions clear

---

### Step 7.4: Final Integration Test

**Goal:** Complete end-to-end test of entire application

**Tasks:**
1. Fresh start:
   - Clear browser localStorage
   - Stop and restart both servers
2. Complete user journey:
   - Register new user
   - Login
   - Create multiple tasks
   - Complete some tasks
   - Filter tasks
   - Logout
   - Login again
   - Verify all tasks persist
   - Logout
3. Second user journey:
   - Register second user
   - Create tasks
   - Verify data isolation
   - Logout

**Verification:**
- Entire user journey works smoothly
- No errors in console
- All functionality works as expected
- Application is ready for demonstration

---

## Summary

**Total Phases:** 7
**Estimated Implementation Order:** Sequential, no parallel tasks

**Critical Dependencies:**
1. Backend must be fully functional before frontend integration
2. Database must be initialized before auth implementation
3. Auth must work before task operations
4. API client must work before page implementation

**Success Criteria:**
- ✅ Two users can register and login independently
- ✅ Each user can create, view, complete, and delete their own tasks
- ✅ Users cannot access each other's data
- ✅ All data persists across sessions
- ✅ All endpoints match `backend-api.md` specification
- ✅ All security rules from `security.md` are enforced
- ✅ No Phase-1 code is modified

**Ready for:** Demonstration, code review, and Phase-3 planning (if applicable)
