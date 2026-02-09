# Backend API Specification

## Overview

The backend provides a RESTful API for authentication and task management. All endpoints return JSON responses and use standard HTTP status codes.

**Base URL:** `http://localhost:8000` (development)

**Authentication:** Bearer token in `Authorization` header for protected endpoints.

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/register

Register a new user account.

**Authentication:** None required

**Request:**
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string (3-50 chars)",
  "password": "string (min 8 chars)"
}
```

**Validation Rules:**
- `username`: Required, 3-50 characters, alphanumeric and underscores only
- `password`: Required, minimum 8 characters

**Success Response (201):**
```json
{
  "access_token": "string (JWT)",
  "refresh_token": "string (JWT)",
  "user_id": "string (UUID)",
  "username": "string"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input format
  ```json
  {
    "error": "validation_error",
    "message": "Password must be at least 8 characters"
  }
  ```
- `409 Conflict` - Username already exists
  ```json
  {
    "error": "username_exists",
    "message": "Username is already taken"
  }
  ```

---

#### POST /api/auth/login

Authenticate existing user and receive tokens.

**Authentication:** None required

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Success Response (200):**
```json
{
  "access_token": "string (JWT)",
  "refresh_token": "string (JWT)",
  "user_id": "string (UUID)",
  "username": "string"
}
```

**Error Responses:**
- `400 Bad Request` - Missing fields
  ```json
  {
    "error": "validation_error",
    "message": "Username and password are required"
  }
  ```
- `401 Unauthorized` - Invalid credentials
  ```json
  {
    "error": "invalid_credentials",
    "message": "Invalid username or password"
  }
  ```

---

#### POST /api/auth/refresh

Refresh access token using refresh token.

**Authentication:** None required (refresh token in body)

**Request:**
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "string (JWT)"
}
```

**Success Response (200):**
```json
{
  "access_token": "string (JWT)",
  "refresh_token": "string (JWT)"
}
```

**Error Responses:**
- `400 Bad Request` - Missing refresh token
  ```json
  {
    "error": "validation_error",
    "message": "Refresh token is required"
  }
  ```
- `401 Unauthorized` - Invalid or expired refresh token
  ```json
  {
    "error": "invalid_token",
    "message": "Refresh token is invalid or expired"
  }
  ```
- `401 Unauthorized` - Refresh token revoked
  ```json
  {
    "error": "token_revoked",
    "message": "Refresh token has been revoked"
  }
  ```

---

#### POST /api/auth/logout

Invalidate refresh token and end session.

**Authentication:** Required (access token)

**Request:**
```http
POST /api/auth/logout
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh_token": "string (JWT)"
}
```

**Success Response (204):**
- No content

**Error Responses:**
- `400 Bad Request` - Missing refresh token
  ```json
  {
    "error": "validation_error",
    "message": "Refresh token is required"
  }
  ```
- `401 Unauthorized` - Invalid or expired access token
  ```json
  {
    "error": "invalid_token",
    "message": "Access token is invalid or expired"
  }
  ```

---

### Task Endpoints

#### GET /api/tasks

Retrieve all tasks for the authenticated user.

**Authentication:** Required

**Request:**
```http
GET /api/tasks
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `completed` (optional): Filter by completion status
  - `true` - Only completed tasks
  - `false` - Only incomplete tasks
  - (not provided) - All tasks

**Success Response (200):**
```json
{
  "tasks": [
    {
      "id": "string (UUID)",
      "user_id": "string (UUID)",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "created_at": "string (ISO 8601 datetime)",
      "updated_at": "string (ISO 8601 datetime)"
    }
  ],
  "count": "integer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
  ```json
  {
    "error": "authentication_required",
    "message": "Authorization header is required"
  }
  ```

---

#### GET /api/tasks/{task_id}

Retrieve a specific task by ID.

**Authentication:** Required

**Request:**
```http
GET /api/tasks/{task_id}
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `task_id`: UUID of the task

**Success Response (200):**
```json
{
  "task": {
    "id": "string (UUID)",
    "user_id": "string (UUID)",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime)"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
  ```json
  {
    "error": "authentication_required",
    "message": "Authorization header is required"
  }
  ```
- `403 Forbidden` - Task belongs to another user
  ```json
  {
    "error": "access_denied",
    "message": "You do not have permission to access this task"
  }
  ```
- `404 Not Found` - Task does not exist
  ```json
  {
    "error": "not_found",
    "message": "Task not found"
  }
  ```

---

#### POST /api/tasks

Create a new task for the authenticated user.

**Authentication:** Required

**Request:**
```http
POST /api/tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "string (1-200 chars)",
  "description": "string (optional, max 1000 chars) or null"
}
```

**Validation Rules:**
- `title`: Required, 1-200 characters
- `description`: Optional, maximum 1000 characters

**Success Response (201):**
```json
{
  "task": {
    "id": "string (UUID)",
    "user_id": "string (UUID)",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime)"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input
  ```json
  {
    "error": "validation_error",
    "message": "Title is required and must be between 1 and 200 characters"
  }
  ```
- `401 Unauthorized` - Invalid or missing token
  ```json
  {
    "error": "authentication_required",
    "message": "Authorization header is required"
  }
  ```

---

#### PUT /api/tasks/{task_id}

Update an existing task.

**Authentication:** Required

**Request:**
```http
PUT /api/tasks/{task_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "string (1-200 chars, optional)",
  "description": "string (max 1000 chars, optional) or null",
  "completed": "boolean (optional)"
}
```

**Validation Rules:**
- At least one field must be provided
- Same validation as POST for fields that are provided

**Success Response (200):**
```json
{
  "task": {
    "id": "string (UUID)",
    "user_id": "string (UUID)",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime)"
  }
}
```

**Error Responses:**
- `400 Bad Request` - No fields provided or invalid input
  ```json
  {
    "error": "validation_error",
    "message": "At least one field must be provided"
  }
  ```
- `401 Unauthorized` - Invalid or missing token
  ```json
  {
    "error": "authentication_required",
    "message": "Authorization header is required"
  }
  ```
- `403 Forbidden` - Task belongs to another user
  ```json
  {
    "error": "access_denied",
    "message": "You do not have permission to modify this task"
  }
  ```
- `404 Not Found` - Task does not exist
  ```json
  {
    "error": "not_found",
    "message": "Task not found"
  }
  ```

---

#### PATCH /api/tasks/{task_id}/toggle

Toggle task completion status.

**Authentication:** Required

**Request:**
```http
PATCH /api/tasks/{task_id}/toggle
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `task_id`: UUID of the task

**Request Body:** None

**Success Response (200):**
```json
{
  "task": {
    "id": "string (UUID)",
    "user_id": "string (UUID)",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime)"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
  ```json
  {
    "error": "authentication_required",
    "message": "Authorization header is required"
  }
  ```
- `403 Forbidden` - Task belongs to another user
  ```json
  {
    "error": "access_denied",
    "message": "You do not have permission to modify this task"
  }
  ```
- `404 Not Found` - Task does not exist
  ```json
  {
    "error": "not_found",
    "message": "Task not found"
  }
  ```

---

#### DELETE /api/tasks/{task_id}

Delete a task.

**Authentication:** Required

**Request:**
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `task_id`: UUID of the task

**Success Response (204):**
- No content

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
  ```json
  {
    "error": "authentication_required",
    "message": "Authorization header is required"
  }
  ```
- `403 Forbidden` - Task belongs to another user
  ```json
  {
    "error": "access_denied",
    "message": "You do not have permission to delete this task"
  }
  ```
- `404 Not Found` - Task does not exist
  ```json
  {
    "error": "not_found",
    "message": "Task not found"
  }
  ```

---

## Standard HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE or logout |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists (e.g., username) |
| 422 | Unprocessable Entity | Validation errors |
| 500 | Internal Server Error | Unexpected server error |

## Error Response Format

All error responses follow this format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": "Optional additional information"
}
```

## CORS Configuration

**Allowed Origins:** `http://localhost:3000` (frontend)

**Allowed Methods:** GET, POST, PUT, PATCH, DELETE, OPTIONS

**Allowed Headers:**
- Content-Type
- Authorization

**Expose Headers:** None

**Allow Credentials:** true

## Rate Limiting

**Note:** Rate limiting is out of scope for Phase-2 (see `non-goals.md`)

## Request/Response Examples

### Complete Task Lifecycle

**1. Register:**
```http
POST /api/auth/register
{
  "username": "john_doe",
  "password": "secure_password_123"
}

Response: 201
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe"
}
```

**2. Create Task:**
```http
POST /api/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

Response: 201
{
  "task": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T10:00:00Z"
  }
}
```

**3. Get All Tasks:**
```http
GET /api/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Response: 200
{
  "tasks": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-05T10:00:00Z",
      "updated_at": "2026-01-05T10:00:00Z"
    }
  ],
  "count": 1
}
```

**4. Toggle Task:**
```http
PATCH /api/tasks/660e8400-e29b-41d4-a716-446655440001/toggle
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Response: 200
{
  "task": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T10:05:00Z"
  }
}
```

**5. Delete Task:**
```http
DELETE /api/tasks/660e8400-e29b-41d4-a716-446655440001
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Response: 204
(No content)
```

**6. Logout:**
```http
POST /api/auth/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response: 204
(No content)
```
