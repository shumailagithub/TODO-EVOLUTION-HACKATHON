# Phase-2 Overview

## What is Phase-2?

Phase-2 transforms the single-user, in-memory console todo application (Phase-1) into a multi-user, persistent web application with JWT-based authentication.

### Key Changes from Phase-1

| Aspect | Phase-1 | Phase-2 |
|--------|---------|---------|
| **Platform** | Console (CLI) | Web (Browser) |
| **Users** | Single-user | Multi-user |
| **Persistence** | In-memory | PostgreSQL database |
| **Authentication** | None | JWT-based (Better Auth) |
| **Architecture** | Monolithic script | Client-server (REST API) |
| **Data Access** | Direct memory | API calls |

## Goals

### Primary Goals

1. **Multi-User Support**
   - Multiple users can register accounts
   - Each user has their own isolated task collection
   - Users cannot see or modify other users' tasks

2. **Persistent Storage**
   - All user data stored in PostgreSQL
   - Tasks persist across sessions
   - Database survives application restarts

3. **Secure Authentication**
   - JWT-based authentication using Better Auth
   - Secure token lifecycle (issue, validate, refresh)
   - Protected endpoints require valid tokens

4. **Web Interface**
   - Responsive web UI using Next.js (App Router)
   - Modern, clean interface
   - Real-time task management (add, complete, delete)

5. **RESTful API**
   - Clear, documented API endpoints
   - Proper HTTP methods and status codes
   - Consistent request/response formats

## Scope

### In Scope

- User registration and login
- JWT authentication (access and refresh tokens)
- Task CRUD operations (Create, Read, Update, Delete)
- Task completion toggle
- Per-user task filtering
- PostgreSQL database with SQLModel
- FastAPI backend
- Next.js frontend (App Router)
- Protected routes on frontend
- Basic error handling and validation

### Technology Stack

- **Backend:** FastAPI
- **Frontend:** Next.js (App Router)
- **ORM:** SQLModel
- **Database:** Neon PostgreSQL
- **Authentication:** Better Auth (JWT)
- **API Style:** REST

## Success Criteria

1. A user can register an account and receive JWT tokens
2. A logged-in user can create, view, complete, and delete their own tasks
3. Users cannot access or modify tasks belonging to other users
4. All data persists across browser refresh and application restarts
5. Protected routes redirect unauthenticated users to login
6. API endpoints return proper HTTP status codes and error messages

## Constraints

- Phase-1 code must NOT be modified or reused
- Phase-2 must be implemented in new directories: `frontend/`, `backend/`, `specs/`
- No features beyond core todo functionality
- Prioritize correctness and clarity over extra features
