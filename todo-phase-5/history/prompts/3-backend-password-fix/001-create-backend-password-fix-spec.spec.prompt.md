---
id: 001
title: Create Backend Password Fix Spec
stage: spec
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 3-backend-password-fix
branch: main
user: user
command: /sp.specify
labels:
  - authentication
  - security
  - backend
  - password-hashing

links:
  spec: ./spec.md
  ticket: null
  adr: null
  pr: null

files_yaml:
  - "specs/3-backend-password-fix/spec.md"
  - "history/prompts/3-backend-password-fix/001-create-backend-password-fix-spec.spec.prompt.md"

tests_yaml: []

outcome: Created specification for backend password hashing fixes
evaluation: Successfully created detailed specification covering bcrypt compatibility issues and password handling requirements
---

# Create Backend Password Fix Spec

## User Input
```
Specification: Fix Backend Password Hashing and Registration

**Problem:**
Backend crashes with "ValueError: password cannot be longer than 72 bytes" and bcrypt version compatibility issues when registering users.

**Root Cause:**
- passlib's bcrypt wrapper has compatibility issues with bcrypt 4.x
- Password not being truncated before hashing
- Error: "module 'bcrypt' has no attribute '__about__'"

**Files to Fix:**

**1. backend/auth/password.py**
Current issue: Using passlib's CryptContext which has bcrypt compatibility problems

Required changes:
- Remove passlib dependency for password hashing
- Import bcrypt directly: `import bcrypt`
- Update hash_password function:
```python
  def hash_password(password: str) -> str:
      # Encode to UTF-8 and truncate to 72 bytes
      password_bytes = password.encode('utf-8')[:72]
      # Generate salt and hash
      salt = bcrypt.gensalt(rounds=12)
      hashed = bcrypt.hashpw(password_bytes, salt)
      return hashed.decode('utf-8')
```
- Update verify_password function:
```python
  def verify_password(plain_password: str, hashed_password: str) -> bool:
      password_bytes = plain_password.encode('utf-8')[:72]
      hashed_bytes = hashed_password.encode('utf-8')
      return bcrypt.checkpw(password_bytes, hashed_bytes)
```

**2. backend/pyproject.toml or requirements.txt**
- Ensure bcrypt>=4.0.0 is installed
- Remove passlib[bcrypt] if present
- Add: bcrypt==4.2.1

**Expected Behavior After Fix:**
- Registration works without 500 errors
- Passwords are properly hashed and stored
- Login can verify passwords correctly
- Backend runs on port 8001 without crashes
```

## Response
Created a comprehensive specification document covering the backend password hashing fixes with detailed user stories, requirements, and success criteria. The spec includes:

- User Story 1: Successful Registration - Ensures registration works without bcrypt errors
- User Story 2: Successful Login - Verifies password verification works correctly
- User Story 3: Password Security - Implements secure password hashing practices
- User Story 4: Error Handling - Prevents server crashes during password operations

The specification addresses all the critical issues:
- Bcrypt compatibility problems with version 4.x
- Password truncation to 72 bytes for bcrypt limitations
- UTF-8 encoding for proper character handling
- Direct bcrypt usage instead of passlib wrapper
- Proper error handling to prevent 500 errors