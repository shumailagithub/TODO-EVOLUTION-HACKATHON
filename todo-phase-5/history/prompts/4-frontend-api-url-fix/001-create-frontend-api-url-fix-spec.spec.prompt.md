---
id: 001
title: Create Frontend API URL Fix Spec
stage: spec
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 4-frontend-api-url-fix
branch: main
user: user
command: /sp.specify
labels:
  - frontend
  - configuration
  - api
  - environment

links:
  spec: ./spec.md
  ticket: null
  adr: null
  pr: null

files_yaml:
  - "specs/4-frontend-api-url-fix/spec.md"
  - "history/prompts/4-frontend-api-url-fix/001-create-frontend-api-url-fix-spec.spec.prompt.md"

tests_yaml: []

outcome: Created specification for frontend API URL configuration fix
evaluation: Successfully created detailed specification covering API base URL configuration and environment variable usage
---

# Create Frontend API URL Fix Spec

## User Input
```
Specification: Update Frontend API Base URL

**Problem:**
Frontend is calling backend on wrong port - backend runs on 8001 but frontend might be using 8000

**Files to Check/Fix:**

**1. frontend/.env.local (create if doesn't exist)**
Add: NEXT_PUBLIC_API_URL=http://localhost:8001

**2. frontend/pages/api/auth/register.js**
Update backend URL to use port 8001:
```javascript
const response = await fetch('http://localhost:8001/api/auth/register', {
```

**3. frontend/pages/api/auth/login.js**
Update backend URL:
```javascript
const response = await fetch('http://localhost:8001/api/auth/login', {
```

**4. frontend/pages/api/tasks/index.js**
Update all backend URLs to port 8001

**Success Criteria:**
- Frontend successfully calls backend on port 8001
- Registration completes without "Internal Server Error"
- User is redirected to login page after successful registration
```

## Response
Created a comprehensive specification document covering the frontend API base URL configuration fix with detailed user stories, requirements, and success criteria. The spec includes:

- User Story 1: Successful API Communication - Ensures frontend communicates on correct port
- User Story 2: Environment Configuration - Uses proper environment variable configuration
- User Story 3: API Route Consistency - Ensures all routes use correct base URL
- User Story 4: Specific API Route Updates - Updates specific files with correct port
- User Story 5: Error Handling - Provides clear feedback for connection issues

The specification addresses all the critical issues:
- Configuring NEXT_PUBLIC_API_URL environment variable
- Using http://localhost:8001 as the backend URL
- Updating specific API route files (register.js, login.js, tasks/index.js)
- Removing hardcoded backend URLs
- Ensuring consistent API communication
- Proper error handling for connection issues
- Ensuring registration completes successfully without errors