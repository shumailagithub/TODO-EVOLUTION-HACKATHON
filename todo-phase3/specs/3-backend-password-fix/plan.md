# Implementation Plan: Backend Password Hashing Fix

**Feature**: 3-backend-password-fix
**Created**: 2026-01-09
**Status**: Draft

## Architecture Overview

### Tech Stack
- **Backend**: FastAPI with Python 3.13+
- **Password Hashing**: bcrypt 4.x (direct usage, not passlib wrapper)
- **Database**: PostgreSQL (Neon) with SQLModel
- **Authentication**: JWT tokens with bcrypt password hashing

### File Structure
```
backend/
├── auth/
│   └── password.py          # Password hashing utilities (to be updated)
├── api/
│   └── auth.py              # Authentication endpoints
├── models/
│   └── user.py              # User model
└── requirements.txt         # Dependencies (to be updated)
```

## Implementation Approach

### Phase 1: Password Utility Update
1. Replace passlib CryptContext with direct bcrypt usage
2. Update hash_password function with proper 72-byte truncation
3. Update verify_password function with proper 72-byte handling
4. Ensure UTF-8 encoding for password handling

### Phase 2: Dependency Management
1. Update requirements.txt to use bcrypt 4.x directly
2. Remove passlib bcrypt wrapper if present
3. Ensure compatibility with existing codebase

### Phase 3: Testing and Validation
1. Test password hashing functionality
2. Verify login still works with new implementation
3. Test edge cases with long passwords
4. Validate UTF-8 character handling

## Technical Decisions

### Decision 1: Bcrypt Implementation Strategy
**Problem**: How to implement bcrypt without passlib wrapper?
**Options**:
- Direct bcrypt import and usage
- Create custom wrapper around bcrypt
- Use alternative library
**Decision**: Use direct bcrypt import and usage
**Rationale**: Provides maximum control and avoids compatibility issues with passlib

### Decision 2: Password Truncation Strategy
**Problem**: How to handle bcrypt's 72-byte limit?
**Options**:
- Pre-truncate at 72 bytes before hashing
- Let bcrypt handle truncation internally
- Reject passwords longer than 72 bytes
**Decision**: Pre-truncate at 72 bytes before hashing
**Rationale**: Most compatible approach that maintains security

### Decision 3: UTF-8 Encoding Strategy
**Problem**: How to handle non-ASCII characters in passwords?
**Options**:
- Encode to UTF-8 before truncation
- Reject non-ASCII characters
- Use different encoding
**Decision**: Encode to UTF-8 before truncation
**Rationale**: Supports international characters while maintaining compatibility

## Security Considerations

### Password Hashing Security
- Use bcrypt with 12 salt rounds for appropriate security
- Properly truncate passwords to 72 bytes before hashing
- Handle UTF-8 encoding consistently
- Never store plain text passwords

### Compatibility
- Ensure existing user accounts remain functional
- Maintain API contract compatibility
- Preserve authentication flow

## Dependencies

### Current Dependencies
- passlib (to be reduced for bcrypt)
- bcrypt (to be used directly)
- python-jose (for JWT)
- argon2-cffi (if present)

### Updated Dependencies
- bcrypt==4.2.1 (direct usage)
- Remove passlib bcrypt wrapper if causing issues

## API Contract

### Authentication Endpoints
- POST /api/auth/register - User registration with new password hashing
- POST /api/auth/login - User authentication with new verification
- All endpoints should continue working with same request/response format

## Deployment Considerations

### Backward Compatibility
- Existing users should still be able to login
- Password migration strategy if needed
- Zero-downtime deployment possible

## Risk Analysis

### High Risk Items
- Breaking existing user authentication
- Introducing security vulnerabilities
- Incompatibility with existing password hashes

### Mitigation Strategies
- Thorough testing of login functionality
- Maintain support for existing password formats if needed
- Gradual rollout if possible

## Rollout Strategy

### Phase 1: Local Testing
- Implement changes locally
- Test with various password types
- Verify registration and login work

### Phase 2: Integration Testing
- Test with frontend integration
- Verify all authentication flows
- Security review

## Monitoring and Observability

### Server-Side Logging
- Password hashing events
- Authentication success/failure rates
- Error occurrences during hashing

### Success Metrics
- Successful registration rate
- Successful login rate
- Password hashing performance