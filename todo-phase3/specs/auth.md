# Authentication

## Overview

Phase-2 uses JWT (JSON Web Token) based authentication powered by Better Auth. This provides secure, stateless authentication for multi-user scenarios.

## Token Types

### 1. Access Token
- **Purpose:** Short-lived token for API requests
- **Lifetime:** 15 minutes
- **Format:** JWT signed with HS256
- **Claims:**
  - `sub`: User ID (UUID)
  - `exp`: Expiration timestamp
  - `iat`: Issued at timestamp
  - `type`: "access"

### 2. Refresh Token
- **Purpose:** Long-lived token for obtaining new access tokens
- **Lifetime:** 7 days
- **Format:** JWT signed with HS256
- **Claims:**
  - `sub`: User ID (UUID)
  - `exp`: Expiration timestamp
  - `iat`: Issued at timestamp
  - `type`: "refresh"
  - `jti`: Unique token ID (for revocation)

## Authentication Flow

### Registration Flow

```
┌──────────────┐
│   User       │
└──────┬───────┘
       │
       │ 1. Submit: username, password
       ▼
┌──────────────────┐
│  Frontend        │
│  (Next.js)       │
└──────┬───────────┘
       │
       │ 2. POST /api/auth/register
       │    {username, password}
       ▼
┌──────────────────┐
│  Backend         │
│  (FastAPI)       │
└──────┬───────────┘
       │
       │ 3. Validate:
       │    - Username uniqueness
       │    - Password strength
       ▼
       │
       │ 4. Hash password (bcrypt)
       │ 5. Create user in DB
       ▼
       │
       │ 6. Generate tokens:
       │    - Access token (15 min)
       │    - Refresh token (7 days)
       ▼
       │
       │ 7. Store refresh token in DB
       ▼
┌──────┴───────────┐
│  Response: 201   │
│  {              │
│    access_token, │
│    refresh_token,│
│    user_id,      │
│    username      │
│  }               │
└──────────────────┘
       │
       │ 8. Store tokens in localStorage
       ▼
┌──────┴───────────┐
│  Redirect to     │
│  dashboard       │
└──────────────────┘
```

### Login Flow

```
┌──────────────┐
│   User       │
└──────┬───────┘
       │
       │ 1. Submit: username, password
       ▼
┌──────────────────┐
│  Frontend        │
│  (Next.js)       │
└──────┬───────────┘
       │
       │ 2. POST /api/auth/login
       │    {username, password}
       ▼
┌──────────────────┐
│  Backend         │
│  (FastAPI)       │
└──────┬───────────┘
       │
       │ 3. Find user by username
       │ 4. Verify password (bcrypt)
       ▼
       │
       │ 5. Generate tokens:
       │    - Access token (15 min)
       │    - Refresh token (7 days)
       ▼
       │
       │ 6. Store refresh token in DB
       ▼
┌──────┴───────────┐
│  Response: 200    │
│  {              │
│    access_token, │
│    refresh_token,│
│    user_id,      │
│    username      │
│  }               │
└──────────────────┘
       │
       │ 7. Store tokens in localStorage
       ▼
┌──────┴───────────┐
│  Redirect to     │
│  dashboard       │
└──────────────────┘
```

### Token Refresh Flow

```
┌──────────────────┐
│  Frontend        │
│  (Next.js)       │
└──────┬───────────┘
       │
       │ 1. Detect expired access token
       │    (or approaching expiry)
       ▼
       │
       │ 2. POST /api/auth/refresh
       │    {refresh_token}
       ▼
┌──────────────────┐
│  Backend         │
│  (FastAPI)       │
└──────┬───────────┘
       │
       │ 3. Validate refresh token signature
       │ 4. Check token not revoked
       │    (lookup jti in DB)
       ▼
       │
       │ 5. Generate new access token
       │ 6. Generate new refresh token
       ▼
       │
       │ 7. Revoke old refresh token
       │    (delete from DB)
       ▼
       │
       │ 8. Store new refresh token
       ▼
┌──────┴───────────┐
│  Response: 200    │
│  {              │
│    access_token, │
│    refresh_token │
│  }               │
└──────────────────┘
       │
       │ 9. Update localStorage
       ▼
┌──────┴───────────┐
│  Retry original  │
│  request with    │
│  new token       │
└──────────────────┘
```

### Logout Flow

```
┌──────────────────┐
│  Frontend        │
│  (Next.js)       │
└──────┬───────────┘
       │
       │ 1. POST /api/auth/logout
       │    Authorization: Bearer <access>
       │    {refresh_token}
       ▼
┌──────────────────┐
│  Backend         │
│  (FastAPI)       │
└──────┬───────────┘
       │
       │ 2. Validate access token
       │ 3. Extract user_id
       ▼
       │
       │ 4. Revoke refresh token
       │    (delete from DB)
       ▼
┌──────┴───────────┐
│  Response: 204    │
│  (No Content)    │
└──────────────────┘
       │
       │ 5. Clear localStorage
       ▼
┌──────┴───────────┐
│  Redirect to     │
│  login page      │
└──────────────────┘
```

## Token Validation Rules

### Access Token Validation

For every protected API request:

1. **Presence Check:**
   - `Authorization` header must exist
   - Must start with `Bearer ` prefix

2. **Format Check:**
   - Must be valid JWT format
   - Must decode successfully

3. **Signature Check:**
   - Must verify with secret key
   - Invalid signatures → 401 Unauthorized

4. **Expiration Check:**
   - `exp` claim must be in future
   - Expired tokens → 401 Unauthorized

5. **Type Check:**
   - `type` claim must be "access"
   - Wrong type → 401 Unauthorized

### Refresh Token Validation

For token refresh requests:

1. **All access token validation rules apply**
2. **Token ID Check:**
   - `jti` claim must exist
   - Must be present in database
   - Missing → 401 Unauthorized (token revoked)
3. **Type Check:**
   - `type` claim must be "refresh"

## Token Storage

### Client-Side (Frontend)

**Location:** `localStorage`

**Keys:**
```javascript
{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "user_id": "<UUID>",
  "username": "<string>"
}
```

**Security Considerations:**
- Tokens stored in localStorage are vulnerable to XSS
- In production, consider HttpOnly cookies for refresh tokens
- Access tokens in localStorage is acceptable for this hackathon

### Server-Side (Backend)

**Refresh Tokens:**
- Stored in PostgreSQL `refresh_tokens` table
- Includes: `jti`, `user_id`, `expires_at`, `created_at`
- Allows revocation on logout

**User Credentials:**
- Passwords hashed with bcrypt (salt rounds: 12)
- Stored in PostgreSQL `users` table

## Better Auth Configuration

### Environment Variables Required

```bash
# JWT Secret (minimum 32 characters)
JWT_SECRET="your-super-secret-jwt-key-here"

# JWT Token Lifetimes
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Hashing
BCRYPT_ROUNDS=12
```

### Better Auth Integration Points

1. **Token Generation:** `/backend/auth/tokens.py`
   - `generate_access_token(user_id)`
   - `generate_refresh_token(user_id)`

2. **Token Validation:** `/backend/auth/validator.py`
   - `validate_access_token(token_str)`
   - `validate_refresh_token(token_str)`

3. **Middleware:** `/backend/auth/middleware.py`
   - Dependency: `get_current_user(token: str) -> User`
   - Applied to all protected endpoints

4. **Password Handling:** `/backend/auth/password.py`
   - `hash_password(password: str) -> str`
   - `verify_password(plain: str, hashed: str) -> bool`

## Error Responses

### Authentication Errors

**401 Unauthorized - Missing Token**
```json
{
  "error": "authentication_required",
  "message": "Authorization header is required"
}
```

**401 Unauthorized - Invalid Token**
```json
{
  "error": "invalid_token",
  "message": "Token is invalid or expired"
}
```

**401 Unauthorized - Wrong Token Type**
```json
{
  "error": "invalid_token_type",
  "message": "Expected access token, got refresh token"
}
```

**409 Conflict - Username Exists**
```json
{
  "error": "username_exists",
  "message": "Username is already taken"
}
```

**401 Unauthorized - Invalid Credentials**
```json
{
  "error": "invalid_credentials",
  "message": "Invalid username or password"
}
```

## Security Best Practices

1. **Never transmit tokens in URL parameters**
2. **Always use HTTPS in production**
3. **Rotate JWT secrets regularly**
4. **Implement token refresh before expiry**
5. **Set secure cookie flags if using cookies**
6. **Log authentication failures for security monitoring**
7. **Implement rate limiting on auth endpoints**
