# Implementation Tasks: Frontend API URL Configuration Fix

**Feature**: 4-frontend-api-url-fix
**Created**: 2026-01-09
**Status**: In Progress

## Task Categories
- **SETUP**: Project configuration and preparation
- **CORE**: Core functionality implementation
- **TEST**: Testing and validation
- **POLISH**: Documentation and final touches

---

## Phase 1: Setup [SETUP]

### Task 1.1: Verify current environment configuration
- **Description**: Check current state of .env.local and environment variables
- **File**: .env.local
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: None

### Task 1.2: Backup original API route files
- **Description**: Create backups of current API route files before modification
- **File**: frontend/pages/api/auth/register.js.backup, frontend/pages/api/auth/login.js.backup, frontend/pages/api/tasks/index.js.backup
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: None

---

## Phase 2: Environment Configuration [SETUP]

### Task 2.1: Create/update .env.local with NEXT_PUBLIC_API_URL
- **Description**: Update environment file to use correct backend port
- **File**: .env.local
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 1.1

---

## Phase 3: API Route Updates [CORE]

### Task 3.1: Update register API route to use environment variable
- **Description**: Update frontend/pages/api/auth/register.js to use NEXT_PUBLIC_API_URL
- **File**: frontend/pages/api/auth/register.js
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 2.1

### Task 3.2: Update login API route to use environment variable
- **Description**: Update frontend/pages/api/auth/login.js to use NEXT_PUBLIC_API_URL
- **File**: frontend/pages/api/auth/login.js
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 3.1

### Task 3.3: Update tasks API route to use environment variable
- **Description**: Update frontend/pages/api/tasks/index.js to use NEXT_PUBLIC_API_URL
- **File**: frontend/pages/api/tasks/index.js
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 3.2

### Task 3.4: Update other API routes as needed
- **Description**: Update any additional API routes that reference backend URLs
- **File**: frontend/pages/api/tasks/[id]/index.js, frontend/pages/api/tasks/[id]/toggle.js
- **Priority**: P2
- **Status**: Pending
- **Dependencies**: Task 3.3

---

## Phase 4: Frontend Page Updates [CORE]

### Task 4.1: Update registration page to not store token
- **Description**: Ensure registration page redirects to login without storing token
- **File**: frontend/pages/register.js
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 3.4

### Task 4.2: Update login page to properly handle tokens
- **Description**: Ensure login page stores token and redirects to home page
- **File**: frontend/pages/login.js
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 4.1

---

## Phase 5: Testing and Validation [TEST]

### Task 5.1: Test API communication with backend
- **Description**: Verify API routes can communicate with backend on port 8001
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 4.2

### Task 5.2: Verify registration and login flows work correctly
- **Description**: Test complete registration and login flows with new configuration
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 5.1

### Task 5.3: Test task management functions
- **Description**: Verify task creation, retrieval, and update functions work correctly
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 5.2

---

## Phase 6: Final Validation [POLISH]

### Task 6.1: Code review and cleanup
- **Description**: Review all changes for consistency and best practices
- **Priority**: P2
- **Status**: Pending
- **Dependencies**: Task 5.3

### Task 6.2: Final testing
- **Description**: Complete end-to-end testing of all functionality
- **Priority**: P1
- **Status**: Pending
- **Dependencies**: Task 6.1

---

## Success Criteria
- [ ] Environment variable NEXT_PUBLIC_API_URL is set to http://localhost:8001
- [ ] All API routes use the environment variable for backend communication
- [ ] Registration flow works correctly without storing token
- [ ] Login flow works correctly and stores token
- [ ] Task management functions work correctly
- [ ] No hardcoded port 8000 references remain in frontend code
- [ ] All existing functionality remains intact