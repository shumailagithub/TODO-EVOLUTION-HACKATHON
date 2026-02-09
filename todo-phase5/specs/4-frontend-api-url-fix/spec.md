# Feature Specification: Frontend API Base URL Configuration Fix

**Feature Branch**: `4-frontend-api-url-fix`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "Fix frontend API base URL configuration to use correct backend port."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Successful API Communication (Priority: P1)

A user needs to interact with the backend API without connection errors. The frontend should communicate with the backend on the correct port (8001) instead of the incorrect port (8000).

**Why this priority**: This is critical for all functionality - if the frontend cannot communicate with the backend, no features will work. This addresses the immediate communication failure.

**Independent Test**: Can be fully tested by performing any API operation (register, login, task operations) and verifying successful communication with the backend. Delivers core value by enabling all frontend-backend communication.

**Acceptance Scenarios**:

1. **Given** user performs any API operation, **When** request is made from frontend, **Then** request is sent to backend on port 8001
2. **Given** user attempts registration, **When** registration request is made, **Then** request is sent to http://localhost:8001/api/auth/register
3. **Given** user attempts login, **When** login request is made, **Then** request is sent to http://localhost:8001/api/auth/login
4. **Given** user manages tasks, **When** task API requests are made, **Then** requests are sent to http://localhost:8001/api/tasks

---

### User Story 2 - Environment Configuration (Priority: P1)

The application needs to use the correct API base URL through proper environment configuration. The system should read the API URL from environment variables.

**Why this priority**: This ensures proper configuration management and allows for different environments (development, staging, production) without code changes.

**Independent Test**: Can be fully tested by verifying the NEXT_PUBLIC_API_URL environment variable is properly configured and used by the application. Delivers core value by enabling proper environment configuration.

**Acceptance Scenarios**:

1. **Given** frontend application starts, **When** API calls are made, **Then** NEXT_PUBLIC_API_URL from .env.local is used as base URL
2. **Given** NEXT_PUBLIC_API_URL is set to http://localhost:8001, **When** API requests are made, **Then** all requests use this base URL
3. **Given** environment configuration exists, **When** application runs, **Then** no hardcoded URLs are used
4. **Given** different environment, **When** configuration changes, **Then** API calls use the updated base URL

---

### User Story 3 - API Route Consistency (Priority: P2)

The frontend API routes need to consistently use the configured base URL. All proxy routes should forward to the correct backend.

**Why this priority**: This ensures all API routes work consistently and prevents partial functionality due to inconsistent URL configuration.

**Independent Test**: Can be fully tested by verifying all frontend API routes forward to the correct backend URL. Delivers value by ensuring complete API functionality.

**Acceptance Scenarios**:

1. **Given** frontend API route /api/auth/register, **When** request is forwarded, **Then** it goes to http://localhost:8001/api/auth/register
2. **Given** frontend API route /api/auth/login, **When** request is forwarded, **Then** it goes to http://localhost:8001/api/auth/login
3. **Given** frontend API route /api/tasks, **When** request is forwarded, **Then** it goes to http://localhost:8001/api/tasks
4. **Given** frontend API route /api/tasks/[id], **When** request is forwarded, **Then** it goes to http://localhost:8001/api/tasks/[id]

### User Story 4 - Specific API Route Updates (Priority: P1)

Specific frontend API routes need to be updated to use the correct backend port. The system should replace hardcoded URLs with the correct port.

**Why this priority**: This directly addresses the immediate issue where specific API routes are using the wrong port, causing connection failures.

**Independent Test**: Can be fully tested by verifying the specific files mentioned have their URLs updated to use port 8001. Delivers value by fixing the immediate connection issues.

**Acceptance Scenarios**:

1. **Given** file frontend/pages/api/auth/register.js, **When** the file is updated, **Then** it contains fetch URL pointing to port 8001
2. **Given** file frontend/pages/api/auth/login.js, **When** the file is updated, **Then** it contains fetch URL pointing to port 8001
3. **Given** file frontend/pages/api/tasks/index.js, **When** the file is updated, **Then** all fetch URLs point to port 8001
4. **Given** registration process, **When** user registers successfully, **Then** user is redirected to login page without "Internal Server Error"

---

### User Story 5 - Error Handling for Connection Issues (Priority: P2)

The application needs to handle connection errors gracefully when the backend is unavailable. The system should provide meaningful error messages.

**Why this priority**: This improves user experience by providing clear feedback when the backend is unavailable rather than generic errors.

**Independent Test**: Can be fully tested by attempting API calls when the backend is not running and verifying appropriate error messages. Delivers value by providing better error handling.

**Acceptance Scenarios**:

1. **Given** backend is not running, **When** user makes API request, **Then** appropriate connection error message is displayed
2. **Given** wrong backend URL is configured, **When** API request is made, **Then** clear error message indicates connection failure
3. **Given** network issues occur, **When** API request fails, **Then** user receives helpful error message
4. **Given** API call fails, **When** error occurs, **Then** error message indicates to check backend availability

---

### Edge Cases

- What happens when the environment variable is not set?
- How does the system handle malformed URLs in environment variables?
- What happens when the backend is running on a different port than expected?
- How does the system handle network timeouts during API calls?
- What happens when the backend URL is unreachable?
- How does the system handle SSL/TLS configuration differences?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The frontend MUST use NEXT_PUBLIC_API_URL environment variable as the base URL for all backend API calls
- **FR-002**: The .env.local file MUST contain NEXT_PUBLIC_API_URL=http://localhost:8001
- **FR-003**: All frontend API routes MUST forward requests to the configured backend URL
- **FR-004**: The application MUST NOT use hardcoded backend URLs
- **FR-005**: All authentication API calls MUST go to the correct backend port (8001)
- **FR-006**: All task management API calls MUST go to the correct backend port (8001)
- **FR-007**: Frontend API proxy routes MUST use the configured base URL
- **FR-008**: Error messages MUST indicate correct backend URL when connection fails
- **FR-009**: File frontend/pages/api/auth/register.js MUST have fetch URL pointing to port 8001
- **FR-010**: File frontend/pages/api/auth/login.js MUST have fetch URL pointing to port 8001
- **FR-011**: File frontend/pages/api/tasks/index.js MUST have all fetch URLs pointing to port 8001
- **FR-012**: Registration process MUST redirect to login page after successful registration without "Internal Server Error"

### Non-Functional Requirements

- **NFR-001**: The system MUST handle environment configuration changes without requiring code changes
  - **Measurement Method**: Verify that changing NEXT_PUBLIC_API_URL in .env.local updates all API calls without code modifications.
  - **Acceptance Criteria**: All API calls use the updated URL after environment variable change and application restart.

- **NFR-002**: The system MUST provide consistent API communication across all endpoints
  - **Measurement Method**: Test all API endpoints (auth, tasks) and verify they use the same base URL.
  - **Acceptance Criteria**: All API endpoints use the configured base URL consistently.

- **NFR-003**: The system MUST provide clear error messages for connection failures
  - **Measurement Method**: Test API calls when backend is unavailable and verify error message content.
  - **Acceptance Criteria**: Error messages clearly indicate connection issues and suggest checking backend availability.

- **NFR-004**: The system MUST support different environments through configuration
- **NFR-005**: The system MUST maintain performance during API calls
- **NFR-006**: The system MUST handle connection timeouts gracefully
- **NFR-007**: The system MUST validate the configured API URL format

### Key Entities

- **API Base URL**: Configuration value that determines the backend endpoint for all API calls
- **Environment Variable**: NEXT_PUBLIC_API_URL that stores the backend URL configuration
- **Frontend API Routes**: Proxy routes that forward requests to the configured backend

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API calls are made to port 8001 instead of 8000
- **SC-002**: The NEXT_PUBLIC_API_URL environment variable is properly configured
- **SC-003**: No hardcoded backend URLs exist in the frontend code
- **SC-004**: All authentication flows work without connection errors
- **SC-005**: All task management functions work without connection errors
- **SC-006**: Frontend API proxy routes correctly forward to backend
- **SC-007**: Error messages indicate correct backend URL when connection fails
- **SC-008**: Environment configuration is used consistently across all API calls
- **SC-009**: File frontend/pages/api/auth/register.js has fetch URL pointing to port 8001
- **SC-010**: File frontend/pages/api/auth/login.js has fetch URL pointing to port 8001
- **SC-011**: File frontend/pages/api/tasks/index.js has all fetch URLs pointing to port 8001
- **SC-012**: Registration completes successfully and redirects to login without "Internal Server Error"

## Constraints

### Phase II Constraints (Non-Negotiable)

- Must use NEXT_PUBLIC_API_URL environment variable for API base URL
- Must configure .env.local with correct backend URL
- Must remove any hardcoded backend URLs
- Must maintain existing API contract compatibility
- Must preserve all existing functionality
- Must follow Next.js environment variable conventions

### Assumptions

- Backend is running on port 8001
- NEXT_PUBLIC_API_URL environment variable is available in Next.js
- Frontend API routes can access environment variables
- Backend API endpoints remain unchanged
- Network connectivity exists between frontend and backend

### Scope (In-Scope vs Out-of-Scope)

**In-Scope**:
- Configure NEXT_PUBLIC_API_URL in .env.local
- Update frontend API routes to use environment variable
- Remove hardcoded backend URLs
- Ensure all API calls use correct port (8001)
- Update error handling for connection issues
- Verify API route forwarding consistency

**Out-of-Scope**:
- Backend configuration changes
- API endpoint modifications
- Database connection changes
- Authentication protocol changes
- Deployment configuration
- SSL/TLS setup