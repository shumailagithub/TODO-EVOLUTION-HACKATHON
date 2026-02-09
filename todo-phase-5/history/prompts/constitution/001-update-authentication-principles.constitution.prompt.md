---
id: 001
title: Update Authentication Principles in Constitution
stage: constitution
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: null
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - authentication
  - error-handling
  - phase2

links:
  spec: null
  ticket: null
  adr: null
  pr: null

files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/001-update-authentication-principles.constitution.prompt.md"

tests_yaml: []

outcome: Updated constitution to include authentication flow and error handling principles
evaluation: Successfully added authentication-specific principles to guide development in Phase II
---

# Update Authentication Principles in Constitution

## User Input
```
Update the existing constitution to include authentication flow fixes:

**Additional Principles for Authentication:**
- User registration should NOT store tokens, only redirect to login page
- Login must properly authenticate and store JWT tokens in localStorage
- Home page must verify authentication before loading tasks
- All protected API calls must include Authorization header with Bearer token
- Display clear, user-friendly error messages when backend is unavailable
- Handle 401 Unauthorized errors by redirecting to login page

**Authentication Flow:**
1. Register → Success → Redirect to /login (no token stored)
2. Login → Store token → Redirect to / (home)
3. Home → Check token → Fetch tasks OR redirect to /login

**Error Handling:**
- Connection errors: "Cannot connect to backend. Make sure it's running on port 8000"
- 401 errors: Auto-redirect to login page
- Validation errors: Display specific error from backend
```

## Response
Updated the constitution file to include two new principles:

### VII. Authentication Flow Principles (NON-NEGOTIABLE)
For Phase II and beyond where authentication is introduced:
- User registration MUST NOT store tokens, only redirect to login page after successful registration
- Login MUST properly authenticate users and store JWT tokens in localStorage
- Home page MUST verify authentication before loading tasks
- All protected API calls MUST include Authorization header with Bearer token
- Authentication flow MUST follow: Register → Success → Redirect to /login, Login → Store token → Redirect to / (home), Home → Check token → Fetch tasks OR redirect to /login

### VIII. Authentication Error Handling (NON-NEGOTIABLE)
The application MUST handle authentication errors appropriately:
- Connection errors MUST display: "Cannot connect to backend. Make sure it's running on port 8001"
- 401 Unauthorized errors MUST trigger auto-redirect to login page
- Validation errors MUST display specific error messages from backend
- Display clear, user-friendly error messages when backend is unavailable
- Error handling MUST NOT expose internal system details to users

Version updated from 1.0.0 to 1.1.0 with amendment date updated to 2026-01-09.