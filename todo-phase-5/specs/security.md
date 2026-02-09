# Security Specification

## Overview

Phase-2 implements security best practices for multi-user authentication, data isolation, and secure API communication.

## Authentication Security

### Password Storage

**Hashing Algorithm:** Bcrypt

**Configuration:**
- Salt rounds: 12 (balance between security and performance)
- Never store plain-text passwords
- Hash before storage in database

**Implementation:**
```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
```

### JWT Security

**Signing Algorithm:** HS256 (HMAC-SHA256)

**Secret Key Requirements:**
- Minimum 32 characters
- Stored in environment variable (`JWT_SECRET`)
- Never committed to version control
- Generated using cryptographically secure random generator

**Token Lifetimes:**
- Access token: 15 minutes
- Refresh token: 7 days

**Security Measures:**
1. **Signature Validation:** All tokens validated against secret key
2. **Expiration Enforcement:** Expired tokens rejected immediately
3. **Token Type Check:** Access tokens used for API, refresh tokens only for refresh endpoint
4. **Token Revocation:** Refresh tokens stored in database, deleted on logout

**Never Include in JWT:**
- Plain-text passwords
- Personally identifiable information (PII) beyond what's necessary
- Session secrets
- Any data that shouldn't be visible to client

### Token Storage (Client-Side)

**Location:** `localStorage`

**Trade-offs for Hackathon:**
- **Pros:** Simple implementation, works across subdomains
- **Cons:** Vulnerable to XSS attacks

**Production Recommendation (not required for Phase-2):**
- Use HttpOnly, Secure, SameSite cookies for refresh tokens
- Keep access tokens in memory or short-lived localStorage

### Token Refresh Strategy

**Proactive Refresh:**
- Check token expiry on every API call
- Refresh access token if it expires within 5 minutes
- Transparent to user (no re-login required)

**Fallback:**
- If access token is expired during API call (401 response):
  - Attempt token refresh
  - Retry original request with new token
  - If refresh fails, redirect to login

## Authorization Rules

### User Ownership

**Core Principle:** Users can only access their own data.

**Implementation:**
1. **Database-Level:** All queries include `user_id` filter
2. **API-Level:** Ownership check before allowing operations
3. **Response-Level:** Never return data from other users

### Protected Endpoints

**Authentication Required:**
- All `/api/tasks/*` endpoints
- `/api/auth/logout`
- `/api/auth/refresh`

**Public Endpoints:**
- `/api/auth/register`
- `/api/auth/login`

### Ownership Enforcement

**For Task Operations:**

**GET /api/tasks:**
```python
# Backend MUST filter by user_id
SELECT * FROM tasks WHERE user_id = current_user_id
```

**GET /api/tasks/{task_id}:**
```python
# Backend MUST check ownership
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == current_user_id)  # Ownership check
).first()

if not task:
    raise HTTPException(404, "Task not found")
```

**PUT /api/tasks/{task_id}:**
```python
# Backend MUST verify ownership before update
if task.user_id != current_user_id:
    raise HTTPException(403, "Access denied")
```

**DELETE /api/tasks/{task_id}:**
```python
# Backend MUST verify ownership before delete
if task.user_id != current_user_id:
    raise HTTPException(403, "Access denied")
```

## Data Isolation

### Database-Level Isolation

**Every Query MUST Include:**
- `user_id` in WHERE clause
- Foreign key constraints (already enforced by SQL)
- Cascade delete (automatic on user deletion)

**Prohibited Query Patterns:**
```python
# BAD - Returns ALL tasks from ALL users
session.exec(select(Task)).all()

# BAD - No user_id filter
session.exec(select(Task).where(Task.id == task_id)).first()

# GOOD - Only returns user's tasks
session.exec(select(Task).where(Task.user_id == user_id)).all()

# GOOD - Ownership check
session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == user_id)
).first()
```

### API-Level Isolation

**Rules:**
1. Never return tasks without `user_id` filter
2. Never allow cross-user task access
3. Always return 403 for unauthorized access attempts
4. Never reveal existence of other users' tasks (use 404, not 403, when appropriate)

**Response Security:**
```json
// GOOD - Only user's own tasks
{
  "tasks": [
    {
      "id": "user-task-id",
      "user_id": "current-user-id",
      "title": "My Task",
      ...
    }
  ]
}

// NEVER DO THIS - Other users' tasks
{
  "tasks": [
    {
      "id": "other-user-task",
      "user_id": "different-user-id",  // Security violation
      ...
    }
  ]
}
```

## API Security

### CORS Configuration

**Allowed Origins:**
- Development: `http://localhost:3000`
- Production: Specific frontend domain (not wildcard)

**Allowed Methods:**
- GET, POST, PUT, PATCH, DELETE, OPTIONS

**Allowed Headers:**
- Content-Type
- Authorization

**Exposed Headers:**
- None required for Phase-2

**Allow Credentials:** true

**Implementation (FastAPI):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

### Input Validation

**Backend Validation:**
- Username: 3-50 characters, alphanumeric + underscores
- Password: Minimum 8 characters
- Task title: 1-200 characters
- Task description: Maximum 1000 characters
- UUID validation for all ID parameters

**Client-Side Validation:**
- Mirror backend validation rules
- Provide immediate user feedback
- Never rely solely on client validation

### SQL Injection Prevention

**ORM Protection:**
- Use SQLModel (parameterized queries)
- Never concatenate raw SQL strings
- Never interpolate user input into queries

**Protected:**
```python
# GOOD - Parameterized query via ORM
session.exec(select(Task).where(Task.id == task_id))

# BAD - Vulnerable to SQL injection
session.exec(f"SELECT * FROM tasks WHERE id = '{task_id}'")
```

### Error Messages

**Public Error Messages:**
- Be generic for security-sensitive operations
- Don't reveal system details
- Don't confirm/deny existence of resources

**Examples:**
```json
// GOOD - Generic error
{
  "error": "invalid_credentials",
  "message": "Invalid username or password"
}

// BAD - Reveals user existence
{
  "error": "user_not_found",
  "message": "Username 'john_doe' does not exist"
}
```

## Environment Variables

### Required Secrets

**File:** `.env` (backend root)

```bash
# Database Connection
DATABASE_URL="postgresql://..."

# JWT Secret (minimum 32 chars, cryptographically random)
JWT_SECRET="your-super-secret-jwt-key-here-change-in-production"

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Hashing
BCRYPT_ROUNDS=12
```

### Security Rules for Environment Variables

1. **Never commit `.env` files to version control**
2. **Use `.env.example` as template with placeholder values**
3. **Generate secure random values in production**
4. **Use different values for development and production**
5. **Rotate JWT secrets regularly (production)**

### .gitignore

**Must include:**
```
.env
.env.local
.env.production
```

## Transport Security

### HTTPS (Production)

**Requirement:** All API communication over HTTPS in production

**Development:** HTTP allowed (localhost only)

**Configuration:**
- Frontend: Configure API URL with `https://` in production
- Backend: Use TLS/SSL certificate
- Database: Neon provides secure PostgreSQL connections

### In-Transit Encryption

- TLS 1.2 or higher
- Database connections encrypted (PostgreSQL SSL mode)
- No plain-text credentials in URLs (use environment variables)

## Attack Mitigation

### Brute Force Protection

**Note:** Not required for Phase-2 (see `non-goals.md`)

**Recommended for Production:**
- Rate limiting on `/api/auth/login`
- Account lockout after failed attempts
- CAPTCHA after multiple failures

### Cross-Site Scripting (XSS)

**Frontend Protection:**
- React automatically escapes JSX
- Never use `dangerouslySetInnerHTML` with user input
- Validate and sanitize user input before display
- Use Content Security Policy (CSP) headers (production)

### Cross-Site Request Forgery (CSRF)

**Mitigation:**
- JWT tokens in localStorage (CSRF protection via CORS)
- Same-origin policy enforced by browsers
- CORS properly configured

### Session Hijacking

**Prevention:**
- Short access token lifetime (15 minutes)
- HTTPS in production
- Bind tokens to specific attributes (optional for Phase-2)

## Logging and Auditing

### Security Events to Log

**Backend (for production monitoring):**
- Failed login attempts
- Multiple consecutive failed attempts from same IP
- Successful logout
- Token refresh operations
- Unauthorized access attempts (403 errors)

**What NOT to Log:**
- Passwords (even hashed)
- Full JWT tokens
- Session secrets
- PII (unless necessary for compliance)

### Log Format

```python
logger.warning(
    "Failed login attempt",
    extra={
        "username": username,
        "ip_address": request.client.host,
        "timestamp": datetime.utcnow().isoformat()
    }
)
```

## Security Checklist

### Authentication
- [x] Passwords hashed with bcrypt (12 rounds)
- [x] JWT tokens signed with secure secret
- [x] Access tokens expire in 15 minutes
- [x] Refresh tokens expire in 7 days
- [x] Tokens validated on every request
- [x] Token revocation on logout

### Authorization
- [x] User ownership enforced on all task operations
- [x] Database queries include user_id filter
- [x] API returns 403 for cross-user access
- [x] Protected routes require authentication

### Data Security
- [x] Multi-user data isolation enforced
- [x] SQL injection prevented via ORM
- [x] CORS properly configured
- [x] Input validation on both client and server

### Secrets Management
- [x] Environment variables for secrets
- [x] .env in .gitignore
- [x] No secrets in version control
- [x] JWT secret minimum 32 characters

### Transport Security
- [x] Database connections encrypted
- [x] HTTPS in production (development: localhost)
- [x] CORS prevents cross-origin requests

## Security Best Practices

### Do's
1. Always validate and sanitize user input
2. Use parameterized queries (ORM)
3. Implement proper authentication and authorization
4. Log security-relevant events
5. Keep dependencies updated
6. Use HTTPS in production
7. Encrypt sensitive data at rest (database)
8. Implement proper error handling
9. Use environment variables for secrets
10. Follow principle of least privilege

### Don'ts
1. Never commit secrets to version control
2. Never store plain-text passwords
3. Never concatenate user input into SQL queries
4. Never reveal system details in error messages
5. Never trust client-side validation alone
6. Never use weak JWT secrets
7. Never expose user data without authorization
8. Never allow cross-user data access
9. Never ignore security warnings
10. Never disable security features for convenience

## Compliance Considerations

**Phase-2 is a hackathon project** - Full compliance (GDPR, SOC2, etc.) is out of scope.

**Implemented:**
- Data isolation (basic privacy)
- Secure authentication
- Encrypted database connections

**Not Implemented (see `non-goals.md`):**
- Full audit logging
- Data export/deletion workflows
- Consent management
- Privacy policy implementation
