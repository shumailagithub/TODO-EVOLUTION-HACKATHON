# Architecture

## High-Level System Architecture

```
┌─────────────────┐         HTTP/HTTPS          ┌─────────────────┐
│   Frontend      │ ──────────────────────────> │   Backend       │
│   (Next.js)     │                             │   (FastAPI)     │
│                 │ <──────────────────────────  │                 │
└─────────────────┘         JSON Responses       └─────────────────┘
                                                              │
                                                              │ SQLModel
                                                              │
                                                              ▼
                                                    ┌─────────────────┐
                                                    │   PostgreSQL    │
                                                    │   (Neon)        │
                                                    └─────────────────┘
```

## Components

### 1. Frontend (Next.js App Router)

**Location:** `frontend/`

**Responsibilities:**
- Render UI pages
- Manage authentication state
- Handle user interactions
- Make API calls to backend
- Store JWT tokens (localStorage)
- Handle route protection

**Key Pages:**
- `/login` - User login page
- `/register` - User registration page
- `/dashboard` - Main todo list page (protected)
- `/` - Landing page (redirects to login or dashboard)

### 2. Backend (FastAPI)

**Location:** `backend/`

**Responsibilities:**
- Serve REST API endpoints
- Authenticate and authorize requests
- Validate JWT tokens
- Execute business logic
- Interact with database via SQLModel
- Return JSON responses

**Key Modules:**
- `auth/` - Authentication logic (Better Auth)
- `api/` - API route handlers
- `models/` - SQLModel database models
- `db/` - Database connection and session management
- `config/` - Configuration and environment variables

### 3. Database (PostgreSQL via Neon)

**Location:** Remote cloud database

**Responsibilities:**
- Persist user accounts
- Persist tasks with user associations
- Enforce referential integrity
- Support SQLModel ORM operations

## Data Flow

### Authentication Flow

```
┌──────────┐                    ┌──────────┐
│ Browser  │                    │ Backend  │
└──────────┘                    └──────────┘
     │                               │
     │ 1. POST /auth/register        │
     │    {username, password}       │
     │──────────────────────────────>│
     │                               │
     │                               │ 2. Create user in DB
     │                               │ 3. Generate JWT tokens
     │                               │    (access, refresh)
     │                               │
     │ 4. Response: {access_token,   │
     │    refresh_token, user_id}    │
     │<──────────────────────────────│
     │                               │
     │ 5. Store tokens in localStorage│
     │                               │
```

### Protected API Request Flow

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│ Browser  │                    │ Backend  │                    │ Database │
└──────────┘                    └──────────┘                    └──────────┘
     │                               │                               │
     │ 1. GET /api/tasks              │                               │
     │    Authorization: Bearer <JWT> │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                               │ 2. Validate JWT               │
     │                               │    Extract user_id            │
     │                               │                               │
     │                               │ 3. Query DB:                  │
     │                               │    SELECT * FROM tasks        │
     │                               │    WHERE user_id = ?          │
     │                               │─────────────────────────────> │
     │                               │                               │
     │                               │ 4. Return tasks               │
     │                               │<─────────────────────────────│
     │                               │                               │
     │ 5. Response: {tasks: [...]}    │                               │
     │<──────────────────────────────│                               │
```

### Task Creation Flow

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│ Browser  │                    │ Backend  │                    │ Database │
└──────────┘                    └──────────┘                    └──────────┘
     │                               │                               │
     │ 1. POST /api/tasks             │                               │
     │    Authorization: Bearer <JWT> │                               │
     │    {title, description}        │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                               │ 2. Validate JWT               │
     │                               │    Extract user_id            │
     │                               │                               │
     │                               │ 3. Validate request data      │
     │                               │                               │
     │                               │ 4. INSERT INTO tasks          │
     │                               │    (user_id, title,           │
     │                               │     description,              │
     │                               │     completed)                │
     │                               │─────────────────────────────> │
     │                               │                               │
     │                               │ 5. Return created task        │
     │                               │<─────────────────────────────│
     │                               │                               │
     │ 6. Response: {task: {...}}     │                               │
     │<──────────────────────────────│                               │
```

## Directory Structure

```
todo-phase2/
├── frontend/                 # Next.js application
│   ├── app/                 # App Router pages
│   │   ├── page.tsx        # Landing page
│   │   ├── login/          # Login page
│   │   ├── register/       # Registration page
│   │   └── dashboard/      # Todo list (protected)
│   ├── components/         # React components
│   ├── lib/               # API client, auth utilities
│   └── public/            # Static assets
│
├── backend/                # FastAPI application
│   ├── main.py            # Application entry point
│   ├── auth/              # Authentication logic
│   ├── api/               # API route handlers
│   │   ├── auth.py       # Auth endpoints
│   │   └── tasks.py      # Task endpoints
│   ├── models/            # SQLModel models
│   ├── db/                # Database setup
│   └── config/            # Configuration
│
└── specs/                 # Specifications and plans
    ├── overview.md
    ├── architecture.md
    ├── auth.md
    ├── backend-api.md
    ├── database.md
    ├── frontend.md
    ├── security.md
    ├── non-goals.md
    └── plan.md
```

## Communication Protocol

### Frontend → Backend

- **Protocol:** HTTP/HTTPS
- **Data Format:** JSON
- **Authentication:** Bearer token in Authorization header
- **Content-Type:** application/json

### Backend → Database

- **Protocol:** PostgreSQL wire protocol
- **ORM:** SQLModel (built on SQLAlchemy + Pydantic)
- **Connection Pooling:** Managed by SQLAlchemy

## Separation of Concerns

### Frontend Concerns
- UI rendering and user interaction
- Client-side authentication state
- HTTP request/response handling
- Route protection and navigation

### Backend Concerns
- API endpoint implementation
- Authentication and authorization
- Business logic validation
- Database operations
- Security (CORS, rate limiting, etc.)

### Database Concerns
- Data persistence
- Referential integrity
- Transaction management
- Query execution
