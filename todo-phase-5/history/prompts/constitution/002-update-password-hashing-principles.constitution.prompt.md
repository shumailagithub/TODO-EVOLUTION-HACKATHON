---
id: 002
title: Update Password Hashing Principles
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
  - security
  - authentication
  - password-hashing

links:
  spec: null
  ticket: null
  adr: null
  pr: null

files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/002-update-password-hashing-principles.constitution.prompt.md"

tests_yaml: []

outcome: Updated constitution to include password hashing security principles
evaluation: Successfully added IX. Password Hashing Security Principles section addressing bcrypt issues
---

# Update Password Hashing Principles

## User Input
```
Update constitution to handle bcrypt password hashing issues and authentication flow:

**Critical Issues to Address:**
- Backend bcrypt library compatibility error causing 500 Internal Server Error
- Password hashing failing due to bcrypt version mismatch with passlib
- Registration endpoint crashes when trying to hash passwords
- Password length must be truncated to 72 bytes for bcrypt

**Technology Stack Updates:**
- Backend: FastAPI with bcrypt 4.x (not passlib's bcrypt wrapper)
- Use bcrypt directly instead of passlib for password hashing
- Frontend: Next.js on port 3000
- Backend: FastAPI on port 8001 (not 8000)

**Security Principles:**
- Passwords must be UTF-8 encoded and truncated to 72 bytes before hashing
- Use bcrypt directly with proper error handling
- Salt rounds: 12 for bcrypt
- Store only hashed passwords, never plain text

**Authentication Flow:**
1. Register → Hash password with bcrypt → Save user → Redirect to /login (no token)
2. Login → Verify password → Generate JWT → Return token → Frontend stores → Redirect to /
3. Protected routes → Verify JWT → Allow access OR return 401
```

## Response
Updated the constitution file to include a new principle section:

### IX. Password Hashing Security Principles (NON-NEGOTIABLE)
The application MUST handle password security with the following requirements:
- Passwords MUST be UTF-8 encoded and truncated to 72 bytes before bcrypt hashing
- Use bcrypt directly with 12 rounds of salt for password hashing (not passlib's bcrypt wrapper)
- Store only hashed passwords, never plain text passwords
- Handle bcrypt version compatibility issues gracefully to prevent 500 Internal Server Errors
- Registration endpoint MUST NOT crash when hashing passwords with proper error handling
- Password length validation MUST occur before hashing to prevent bcrypt limitations from causing failures

Version updated from 1.1.0 to 1.2.0 with amendment date updated to 2026-01-09.