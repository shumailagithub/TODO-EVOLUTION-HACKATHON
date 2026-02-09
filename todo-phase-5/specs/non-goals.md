# Non-Goals (Out of Scope)

## Overview

This document explicitly lists features and functionality that are **NOT** part of Phase-2. These items are intentionally excluded to maintain focus on core functionality within hackathon constraints.

## Authentication-Related Non-Goals

### Social Authentication
- ❌ OAuth2 providers (Google, GitHub, Facebook, etc.)
- ❌ Third-party login (Apple ID, Microsoft, etc.)
- ❌ Magic link authentication
- ❌ Phone number authentication
- ❌ Multi-factor authentication (MFA/2FA)
- ❌ Email verification for registration

### Account Management
- ❌ Email change functionality
- ❌ Password reset via email
- ❌ Password change (requires old password)
- ❌ Account deletion
- ❌ Profile management
- ❌ User avatar upload
- ❌ Email notifications

### Session Management
- ❌ Multi-device session management
- ❌ Session list (view active sessions)
- ❌ Revoke specific session
- ❌ Remember me functionality
- ❌ Session timeout warnings
- ❌ Concurrent login prevention
- ❌ Last login tracking

## Task-Related Non-Goals

### Advanced Task Features
- ❌ Task categories or tags
- ❌ Task priorities (high, medium, low)
- ❌ Task due dates and deadlines
- ❌ Task reminders or notifications
- ❌ Subtasks or nested tasks
- ❌ Task dependencies (blocking tasks)
- ❌ Task attachments (files, images)
- ❌ Task comments or notes
- ❌ Task sharing between users
- ❌ Task templates
- ❌ Recurring tasks

### Task Organization
- ❌ Task folders or projects
- ❌ Task lists or groups
- ❌ Search functionality
- ❌ Advanced filtering (by date, priority, etc.)
- ❌ Sorting options (by date, title, etc.)
- ❌ Drag-and-drop task reordering
- ❌ Kanban board view
- ❌ Calendar view
- ❌ Task statistics or analytics

## User Interface Non-Goals

### Advanced UI Features
- ❌ Dark mode theme toggle
- ❌ Responsive mobile app (basic responsive required)
- ❌ Native mobile app (iOS/Android)
- ❌ Progressive Web App (PWA)
- ❌ Offline functionality
- ❌ Real-time updates (WebSockets)
- ❌ Drag-and-drop task management
- ❌ Keyboard shortcuts
- ❌ Accessibility compliance (WCAG)
- ❌ Internationalization (i18n) and localization (l10n)
- ❌ Customizable themes
- ❌ Widget or dashboard analytics

### User Experience
- ❌ Onboarding tutorial or walkthrough
- ❌ Empty state illustrations
- ❌ Loading animations beyond basic spinners
- ❌ Success notifications (toasts)
- ❌ Confirmation dialogs for destructive actions
- ❌ Undo/redo functionality
- ❌ Bulk operations (select multiple tasks)
- ❌ Task history/audit trail

## Backend Non-Goals

### Advanced API Features
- ❌ GraphQL API
- ❌ WebSocket endpoints
- ❌ File upload/download endpoints
- ❌ Background jobs or task queues
- ❌ Email sending (SMTP)
- ❌ Push notifications
- ❌ Webhook support
- ❌ API versioning
- ❌ OpenAPI/Swagger UI beyond basic FastAPI auto-docs
- ❌ Rate limiting
- ❌ Request throttling
- ❌ API key authentication (in addition to JWT)

### Performance Optimizations
- ❌ Caching layer (Redis, Memcached)
- ❌ Database query optimization beyond basic indexing
- ❌ Connection pooling optimization
- ❌ Lazy loading or pagination for tasks
- ❌ Database sharding or replication
- ❌ CDN for static assets
- ❌ Image optimization

## Database Non-Goals

### Advanced Database Features
- ❌ Database migrations framework (Alembic)
- ❌ Database backup automation
- ❌ Database restore procedures
- ❌ Data archiving
- ❌ Soft deletes (tasks are permanently deleted)
- ❌ Audit logging tables
- ❌ Database performance monitoring
- ❌ Query analytics

### Data Management
- ❌ Data export (CSV, JSON)
- ❌ Data import
- ❌ Bulk operations on database
- ❌ Data validation beyond model constraints
- ❌ Database triggers or stored procedures
- ❌ Full-text search
- ❌ Database views

## Security Non-Goals

### Advanced Security Features
- ❌ Rate limiting on auth endpoints
- ❌ IP-based blocking
- ❌ CAPTCHA for login/registration
- ❌ Account lockout after failed attempts
- ❌ Security question recovery
- ❌ Device fingerprinting
- ❌ Anomaly detection
- ❌ Web Application Firewall (WAF)
- ❌ DDoS protection
- ❌ Content Security Policy (CSP) headers
- ❌ HTTP Strict Transport Security (HSTS)
- ❌ X-Frame-Options headers
- ❌ CSRF tokens (stateless JWT provides protection)

### Audit and Compliance
- ❌ Full audit logging
- ❌ Session activity logs
- ❌ Data access logs
- ❌ GDPR compliance features (data export, deletion)
- ❌ Privacy policy implementation
- ❌ Terms of service
- ❌ Cookie consent management
- ❌ Anonymization of user data
- ❌ Data retention policies

## Testing Non-Goals

### Test Coverage
- ❌ Unit tests for all functions
- ❌ Integration tests for API endpoints
- ❌ End-to-end (E2E) tests (Cypress, Playwright)
- ❌ Load testing
- ❌ Performance testing
- ❌ Security testing (penetration testing)
- ❌ Accessibility testing
- ❌ Cross-browser testing beyond Chrome/Firefox
- ❌ Mobile device testing
- ❌ Test coverage reporting

### Test Automation
- ❌ Continuous integration (CI) pipeline
- ❌ Automated test runners
- ❌ Test data fixtures
- ❌ Mock servers for API testing
- ❌ Visual regression testing

## DevOps and Deployment Non-Goals

### Deployment Automation
- ❌ CI/CD pipeline (GitHub Actions, GitLab CI, etc.)
- ❌ Automated deployment scripts
- ❌ Infrastructure as Code (Terraform, CloudFormation)
- ❌ Containerization (Docker)
- ❌ Container orchestration (Kubernetes)
- ❌ Blue/green deployments
- ❌ Rolling updates
- ❌ Automated rollback procedures

### Infrastructure
- ❌ Load balancers
- ❌ Auto-scaling groups
- ❌ Multi-region deployment
- ❌ Disaster recovery procedures
- ❌ Backup and restore automation
- ❌ Monitoring dashboards (Grafana, Datadog)
- ❌ Alerting systems
- ❌ Log aggregation (ELK stack, Splunk)
- ❌ Error tracking (Sentry, Rollbar)

### Environment Management
- ❌ Multiple environments (dev, staging, production)
- ❌ Environment-specific configurations
- ❌ Feature flags
- ❌ A/B testing infrastructure
- ❌ Canary deployments

## Documentation Non-Goals

### Developer Documentation
- ❌ API documentation beyond auto-generated docs
- ❌ Architecture diagrams
- ❌ Database schema diagrams
- ❌ Contribution guidelines
- ❌ Code comments beyond inline explanations
- ❌ README with detailed setup instructions

### User Documentation
- ❌ User manual
- ❌ FAQ
- ❌ Troubleshooting guide
- ❌ Video tutorials
- ❌ Changelog or release notes

## Collaboration Non-Goals

### Team Features
- ❌ Team or workspace management
- ❌ Team member invitations
- ❌ Role-based access control (RBAC)
- ❌ Permissions management
- ❌ Shared task lists
- ❌ Task assignment to other users
- ❌ Comments or mentions (@username)
- ❌ Activity feed or notifications
- ❌ Real-time collaboration
- ❌ Conflict resolution

### Integrations
- ❌ Third-party integrations (Slack, Microsoft Teams, etc.)
- ❌ Calendar integration (Google Calendar, Outlook)
- ❌ Email task creation
- ❌ Webhooks for external services
- ❌ Public API for third-party developers

## Analytics Non-Goals

### User Analytics
- ❌ User behavior tracking
- ❌ Usage metrics
- ❌ Feature adoption tracking
- ❌ Funnel analysis
- ❌ A/B testing framework
- ❌ User segmentation

### Application Analytics
- ❌ Task completion rate statistics
- ❌ User engagement metrics
- ❌ Performance monitoring (APM)
- ❌ Error rate tracking
- ❌ Response time monitoring

## Future Phase Considerations

**Note:** These non-goals may be considered for future phases (Phase-3 and beyond), but are explicitly excluded from Phase-2.

### Potential Phase-3 Features
- Task categories and tags
- Task priorities and due dates
- Advanced filtering and search
- Email verification
- Password reset
- Rate limiting
- Basic unit tests

### Potential Phase-4 Features
- Social authentication
- Email notifications
- Task sharing and collaboration
- Mobile app
- PWA functionality
- Offline support

## Rationale for Non-Goals

### Hackathon Constraints
- Limited time for development
- Focus on core functionality
- Demonstrating technical competence over feature completeness
- Simplicity over complexity

### Learning Priorities
- Understanding authentication fundamentals
- Learning REST API design
- Database integration
- Multi-user data isolation
- Frontend-backend integration

### Scope Management
- Avoid scope creep
- Maintain quality over quantity
- Ensure core features work well
- Minimize technical debt

## Exceptions

**Only add features outside this list if:**
1. They are absolutely required for the application to function
2. They take less than 30 minutes to implement
3. They do not increase complexity significantly
4. They are approved by the project lead

## Summary

**Phase-2 Focus:**
- ✅ Multi-user todo management
- ✅ JWT authentication
- ✅ Per-user task isolation
- ✅ Basic CRUD operations
- ✅ Persistent PostgreSQL storage
- ✅ Modern web UI

**Phase-2 Does NOT Include:**
- ❌ Any feature listed above
- ❌ "Nice to have" additions
- ❌ Production-grade enhancements
- ❌ Advanced features beyond basic requirements

**Rule of Thumb:** If it's not in the core specs (`overview.md`, `auth.md`, `backend-api.md`, `database.md`, `frontend.md`), it's out of scope for Phase-2.
