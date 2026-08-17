# HouseHoldHub MVP - Implementation Plan

**Date:** August 16, 2026  
**Status:** Proposed (awaiting review before GitHub issue creation)  
**Plan Scope:** 7 milestones across 5 repositories

---

## Implementation Overview

### Repositories & Responsibilities

| Repository | Responsibility | Involved in Milestones |
|------------|-----------------|----------------------|
| **Documentation** | PRD, architecture, API specs, guides | 1, 7 |
| **Backend** | Django API, database models, authentication | 1-6 |
| **Frontend** | React UI, API client, authentication flows | 1, 3, 4, 5, 6, 7 |
| **Infrastructure** | Docker, database, deployment config | 1 |
| **Automation** | CI/CD pipelines, testing, deployment | 1 |

### Timeline Estimate

- Phase 1 (Foundation): 1 week (parallel across all repos)
- Phase 2 (Authentication): 2 weeks (backend 1.5w, frontend 2w, parallel)
- Phase 3 (Households): 2 weeks (backend 1.5w, frontend 2w, parallel)
- Phase 4 (Tasks): 2 weeks (backend 1w, frontend 1.5w, parallel)
- Phase 5 (Secondary): 2 weeks (shopping, expenses, inventory; can parallelize)
- Phase 6 (Testing): 1.5 weeks (integration, security, performance)
- Phase 7 (Launch): 0.5 weeks (deployment, verification, launch)

**Total: ~11 weeks (MVP ready)**

---

## Milestone 1: Project Foundation & Infrastructure

**Objective:** Establish development environment, CI/CD pipelines, database infrastructure, and initial codebase scaffold.

**Scope:** Repository setup, Docker, PostgreSQL, Django scaffold, React scaffold, CI/CD, initial documentation.

**Repositories Involved:**
- Documentation
- Backend
- Frontend
- Infrastructure
- Automation

**Prerequisites:**
- GitHub organizations/teams created
- Team access configured
- Domain and hosting provider selected (post-MVP)

**Deliverables:**
1. Backend Django project scaffold (apps, settings, models stub)
2. Frontend React + Vite scaffold (project structure, types)
3. Docker Compose for full-stack development (PostgreSQL, Django, React)
4. GitHub Actions CI/CD pipelines (backend lint/test, frontend lint/test)
5. Initial project documentation (README, setup guide, contribution guide)
6. Database environment (PostgreSQL configuration, initial schema structure)
7. Shared API contract (OpenAPI YAML in documentation repo)

**Acceptance Criteria:**
- [ ] Backend: `python manage.py runserver` starts dev server on localhost:8000
- [ ] Frontend: `npm run dev` starts dev server on localhost:3000
- [ ] Docker Compose: `docker-compose up` brings up PostgreSQL + Django + React
- [ ] CI/CD: GitHub Actions runs on PR (backend tests, frontend tests, linting)
- [ ] Documentation: README has setup instructions for all repos
- [ ] OpenAPI: YAML specification published in docs repo; accessible to both teams

**Dependencies:**
- None (this is the foundation for all other milestones)

**Risks:**
- Team unfamiliar with Django/React: Mitigate with initial spike/training
- Docker environment issues: Mitigate with team setup testing early
- CI/CD misconfiguration: Mitigate with detailed GitHub Actions docs

**Cross-Repository Concerns:**
- Backend Django settings must match Frontend API base URL (localhost:8000/api/v1)
- Docker Compose must coordinate ports (8000 for Django, 3000 for React, 5432 for PostgreSQL)
- OpenAPI spec must be version-controlled and accessible to both Backend and Frontend teams

---

## Milestone 2: Authentication & Session Management

**Objective:** Implement user signup, login, password reset, Google OAuth, and session-based authentication.

**Scope:** 
- Backend: User model, Django auth, session management, Google OAuth integration, password reset endpoints
- Frontend: Signup/login UI, password reset flow, Google OAuth integration, session validation
- Infrastructure: Email configuration (SendGrid/SES connection)

**Repositories Involved:**
- Backend (primary)
- Frontend (dependent on Backend API)
- Infrastructure (email service)

**Prerequisites:**
- Milestone 1 complete (project scaffold)
- Database infrastructure ready
- OpenAPI spec available

**Deliverables:**
1. User model (email, password_hash, name, google_id, timestamps)
2. Django auth endpoints (signup, login, logout, password reset, OAuth callback)
3. Session management (HTTP-only cookies, CSRF protection)
4. Email service integration (SendGrid/SES for password reset, OAuth emails)
5. Frontend authentication context (useAuth hook, ProtectedRoute component)
6. Frontend auth UI (signup form, login form, password reset form, Google button)
7. Integration tests (auth flows, session validation, cross-household prevention)
8. Backend API documentation (auth endpoints in OpenAPI)

**Acceptance Criteria:**
- [ ] Backend: POST /auth/signup creates user + session; returns 201 with user data
- [ ] Backend: POST /auth/login validates email/password; returns 200 with session cookie
- [ ] Backend: POST /auth/logout deletes session; returns 200
- [ ] Backend: POST /auth/forgot-password sends reset email; returns 200
- [ ] Backend: POST /auth/reset-password validates token; resets password; returns 200
- [ ] Backend: GET /auth/me returns current user if authenticated; 401 if not
- [ ] Frontend: Signup page creates account and redirects to household selection
- [ ] Frontend: Login page authenticates and shows households
- [ ] Frontend: Google OAuth redirect completes authentication
- [ ] Frontend: Password reset email link works; allows password change
- [ ] Sessions: HTTP-only cookie set on login; cleared on logout
- [ ] Sessions: Unauthenticated requests return 401
- [ ] Database: User table has email (unique), password_hash, deleted_at fields
- [ ] Tests: 100% coverage of auth endpoints; at least 5 auth integration tests

**Dependencies:**
- Milestone 1 must be complete (Backend API running, Frontend can call it)
- OpenAPI spec must define auth endpoints
- Email service (SendGrid/SES) must be configured

**Risks:**
- Google OAuth configuration errors: Mitigate with detailed setup guide
- Session cookie misconfiguration (missing HttpOnly/Secure flags): Mitigate with security tests
- Password reset token handling bugs: Mitigate with security-focused integration tests

**Cross-Repository Concerns:**
- Frontend must use Backend API base URL from environment variables (REACT_APP_API_URL)
- Frontend must handle 401 responses and redirect to login
- Backend must set CSRF tokens in responses for Frontend to include in requests
- Both teams must agree on session cookie name (default: sessionid)
- Email service credentials must be in environment (never committed)

---

## Milestone 3: Household Management & Membership Model

**Objective:** Implement household CRUD, membership management, and invitation system.

**Scope:**
- Backend: Household model, Membership model, Invitation model, household endpoints, member invitation endpoints
- Frontend: Household selection UI, household creation, member list, invitation UI, join by code
- Database: Household, Membership, Invitation tables with proper FKs

**Repositories Involved:**
- Backend (primary)
- Frontend (dependent)
- Documentation (update API spec)

**Prerequisites:**
- Milestone 2 complete (authentication working)
- User model complete
- OpenAPI spec updated with household endpoints

**Deliverables:**
1. Household model (name, description, code, owner_id, soft-delete via deleted_at)
2. Membership model (user_id, household_id, role: owner|member, joined_at)
3. Invitation model (household_id, email, token_hash, state, expires_at)
4. Backend endpoints:
   - GET/POST /households (list user's households, create)
   - GET/PATCH/DELETE /households/{id} (get, update, soft-delete)
   - GET/POST /households/{id}/code (get code, regenerate)
   - GET/POST /households/{id}/members (list members, invite)
   - DELETE /households/{id}/members/{user_id} (remove member)
   - POST /households/{id}/join (join by code)
   - POST /households/{id}/invitations/{token}/accept (accept invitation)
   - DELETE /households/{id}/invitations/{token} (revoke invitation)
5. Frontend components:
   - Household selection/switcher
   - Create household form
   - Household settings page
   - Member list with removal option
   - Invite member form
   - Join household by code
   - Accept invitation from email link
6. Email templates (household invitation, invitation accepted)
7. Authorization middleware (verify household membership on all subsequent requests)
8. Tests: Authorization tests (owner vs. member permissions), cross-household isolation

**Acceptance Criteria:**
- [ ] Backend: Household CRUD works; creates with owner=current_user
- [ ] Backend: Household code generation returns unique 8-char code
- [ ] Backend: Regenerating code invalidates old code immediately
- [ ] Backend: Member invitation sends email with unique token link
- [ ] Backend: Accepting invitation link creates Membership; sets state=accepted
- [ ] Backend: Revoking invitation prevents acceptance (state=revoked)
- [ ] Backend: Removing member deletes Membership; user loses access
- [ ] Backend: Owner can delete household (soft-delete via deleted_at)
- [ ] Backend: Non-owner cannot create household (returns 403 on wrong user)
- [ ] Backend: Non-member cannot access household data (returns 403)
- [ ] Backend: Email invitations expire after TBD days (30 default)
- [ ] Frontend: Household selector visible after login; shows user's households
- [ ] Frontend: Create household form submits to API; updates local list
- [ ] Frontend: Member list shows all members; owner can remove
- [ ] Frontend: Invite form sends invitation; shows status
- [ ] Frontend: Join by code form validates and adds user to household
- [ ] Frontend: Accepting invitation email link validates token; logs user in; shows household
- [ ] Database: Household soft-delete sets deleted_at; doesn't cascade-delete children
- [ ] Database: Membership is unique(household_id, user_id)
- [ ] Tests: 100+ authorization tests (owner-only, member-only, cross-household)

**Dependencies:**
- Milestone 2 (authentication)
- OpenAPI spec updated with household/membership/invitation endpoints
- Email service configured (for invitations)
- Database schema for Household, Membership, Invitation tables

**Risks:**
- Invitation token security bugs: Mitigate with security review + hashing tests
- Soft-delete cascading incorrectly: Mitigate with explicit tests for data preservation
- Cross-household access possible: Mitigate with comprehensive isolation tests
- Email invitation link breakage: Mitigate with e2e tests for email acceptance flow

**Cross-Repository Concerns:**
- Frontend must parse invitation token from email link (format: /invitation/accept?token=X)
- Backend must hash tokens before storage (SHA-256)
- Frontend must detect when user joins household; update household list
- Both teams must agree on household code format (8 alphanumeric)
- Frontend needs way to switch between user's multiple households

---

## Milestone 4: Task Management

**Objective:** Implement task CRUD, assignment to household members, completion tracking.

**Scope:**
- Backend: Task model, TaskAssignment to Membership, task endpoints, completion logic
- Frontend: Task list, task creation, task editing, assignment dropdown, completion toggle
- Database: Task table with foreign keys to Household, Membership, User

**Repositories Involved:**
- Backend (primary)
- Frontend (dependent)
- Documentation (update API spec)

**Prerequisites:**
- Milestone 3 complete (household & membership working)
- Task model defined in System Design
- OpenAPI spec updated with task endpoints

**Deliverables:**
1. Task model (title, description, due_date, household_id, created_by_id, assigned_to_id→Membership, completed, completed_at)
2. Backend endpoints:
   - GET /households/{id}/tasks (list tasks, filterable by completed/assignee/due_date)
   - POST /households/{id}/tasks (create task)
   - GET /households/{id}/tasks/{task_id} (get task details)
   - PATCH /households/{id}/tasks/{task_id} (edit task)
   - DELETE /households/{id}/tasks/{task_id} (delete task, creator/owner only)
   - PATCH /households/{id}/tasks/{task_id}/complete (mark complete)
3. Frontend components:
   - Task list (with filtering by status, assignee, due date)
   - Task creation form
   - Task detail view
   - Task edit form
   - Assignment dropdown (shows household members)
   - Completion toggle
4. Authorization: Creator/owner can reassign/delete; assigned member can mark complete
5. Tests: Task CRUD, authorization (creator/owner/assigned), assignment validation

**Acceptance Criteria:**
- [ ] Backend: POST /tasks creates task with created_by=current_user
- [ ] Backend: GET /tasks returns paginated list; filters work (completed, assigned_to_id, due_date)
- [ ] Backend: PATCH /tasks/{id} edits task; only creator/owner can edit
- [ ] Backend: DELETE /tasks/{id} deletes task; only creator/owner can delete
- [ ] Backend: Assignment to Membership validates same household
- [ ] Backend: PATCH /tasks/{id}/complete marks task complete; only assigned member or owner can complete
- [ ] Backend: If assigned member is removed from household, task becomes unassigned (assigned_to_id=NULL)
- [ ] Frontend: Task list shows open tasks and completed tasks in separate sections
- [ ] Frontend: Create task form: title (required), description, due_date, assigned_to_id (optional)
- [ ] Frontend: Assignment dropdown shows only household members
- [ ] Frontend: Completing task requires confirmation; shows completion timestamp
- [ ] Frontend: Task list auto-refreshes after edit/completion (TanStack Query invalidation)
- [ ] Database: Task.assigned_to_id is nullable FK to Membership
- [ ] Database: Task.completed_by_id tracks who completed (nullable)
- [ ] Tests: Creator cannot reassign to member from different household (validated in FK)

**Dependencies:**
- Milestone 3 (household & membership)
- OpenAPI spec updated with task endpoints
- Database schema for Task table

**Risks:**
- Assignment to wrong household possible: Mitigate with FK constraint + tests
- Completion by non-assigned member possible: Mitigate with permission check tests
- Task list slow with many tasks: Mitigate with pagination + indexes (documented in ERD)

**Cross-Repository Concerns:**
- Frontend assignment dropdown must query backend for household members
- Frontend must use TanStack Query to invalidate task list after mutations
- Backend must return assigned member name in task response (for display without extra query)
- Frontend filtering must send filter params to Backend pagination

---

## Milestone 5: Secondary Features (Shopping, Expenses, Inventory)

**Objective:** Implement shopping list, expense tracking, and inventory management features.

**Scope:**
- Backend: ShoppingItem, Expense, InventoryItem models and endpoints
- Frontend: UI for shopping list, expense tracking, inventory management
- Database: ShoppingItem, Expense, InventoryItem tables

**Repositories Involved:**
- Backend (primary)
- Frontend (dependent)
- Documentation

**Prerequisites:**
- Milestone 4 complete (task model and endpoints established)
- OpenAPI spec updated with new endpoints

**Deliverables:**

### Shopping List (5A)

1. **Backend:**
   - ShoppingItem model (name, quantity, purchased, purchased_by_id, household_id)
   - GET /households/{id}/shopping (list items, filter by purchased)
   - POST /households/{id}/shopping (add item)
   - PATCH /households/{id}/shopping/{item_id} (update name/quantity/purchased status)
   - DELETE /households/{id}/shopping/{item_id} (delete, creator/owner only)

2. **Frontend:**
   - Shopping list view (pending and purchased sections)
   - Add item form
   - Update item form
   - Toggle purchased checkbox
   - Delete item button

### Expenses (5B)

1. **Backend:**
   - Expense model (amount_cents, category enum, payer_id, description, created_by_id)
   - GET /households/{id}/expenses (list expenses, filter by category/payer, sorted by date)
   - POST /households/{id}/expenses (log expense, defaults payer to creator)
   - PATCH /households/{id}/expenses/{expense_id} (edit expense, creator/owner only)
   - DELETE /households/{id}/expenses/{expense_id} (delete, creator/owner only)

2. **Frontend:**
   - Expense list view (sorted by date, newest first)
   - Expense creation form (amount, category, payer, description)
   - Expense editing form
   - Category breakdown (pie chart or stats)
   - Delete expense button

### Inventory (5C)

1. **Backend:**
   - InventoryItem model (name, quantity, category, location, created_by_id)
   - GET /households/{id}/inventory (list items, filter by category)
   - POST /households/{id}/inventory (add item)
   - PATCH /households/{id}/inventory/{item_id} (update quantity/details)
   - DELETE /households/{id}/inventory/{item_id} (delete, creator/owner only)

2. **Frontend:**
   - Inventory list view (filterable by category)
   - Add inventory form (name, quantity, category, location)
   - Edit inventory form
   - Delete item button

**Acceptance Criteria (Shopping):**
- [ ] Backend: GET /shopping returns list; filters by purchased status
- [ ] Backend: POST /shopping creates item with purchased=false
- [ ] Backend: PATCH /shopping/{id} toggles purchased status; sets purchased_by_id
- [ ] Frontend: Shopping list shows pending items and purchased items separately
- [ ] Frontend: Toggle checkbox marks item purchased/unpurchased

**Acceptance Criteria (Expenses):**
- [ ] Backend: POST /expenses creates with amount_cents (no decimals); defaults payer to creator
- [ ] Backend: GET /expenses returns sorted by date (newest first); filters work
- [ ] Backend: PATCH /expenses/{id} edits (creator/owner only)
- [ ] Backend: DELETE /expenses/{id} deletes (creator/owner only)
- [ ] Frontend: Expense form has amount (in dollars, converted to cents), category dropdown, payer dropdown, description
- [ ] Frontend: Expense list shows all expenses with total and per-category breakdown

**Acceptance Criteria (Inventory):**
- [ ] Backend: GET /inventory returns list; filters by category
- [ ] Backend: POST /inventory creates item with quantity
- [ ] Backend: PATCH /inventory/{id} updates quantity and details
- [ ] Frontend: Inventory list shows all items; can filter by category
- [ ] Frontend: Add/edit forms for quantity, category, location

**Dependencies:**
- Milestone 4 (task model pattern established; follow same authorization model)
- OpenAPI spec updated for shopping, expense, inventory endpoints

**Risks:**
- Feature scope creep: Mitigate by deferring post-MVP enhancements (splitting, settlement, low-stock alerts)
- Duplicate authorization logic: Mitigate by creating reusable permission mixins/classes

**Cross-Repository Concerns:**
- All three features follow same CRUD pattern as tasks; reuse authorization checks
- Frontend can parallelize shopping/expense/inventory UI development
- Backend can parallelize model implementation (independent domain models)

---

## Milestone 6: Testing, Security, Performance

**Objective:** Comprehensive testing, security hardening, and performance optimization.

**Scope:**
- Integration testing (E2E workflows)
- Security testing (authorization, rate limiting, input validation)
- Performance testing (query optimization, caching)
- Documentation finalization

**Repositories Involved:**
- Backend
- Frontend
- Automation
- Documentation

**Prerequisites:**
- Milestone 5 complete (all features implemented)
- All endpoints implemented and documented

**Deliverables:**
1. Backend integration tests:
   - Full signup → create household → invite member → create task workflow
   - Cross-household isolation tests (non-member cannot access)
   - Authorization tests (owner vs. member, creator vs. others)
   - Rate limiting tests (login, password reset, API endpoints)
   - Input validation tests (invalid emails, negative amounts, etc.)
   - Concurrent edit tests (last-write-wins behavior)

2. Frontend integration tests:
   - Login → create household → invite member
   - Create task → assign → complete workflow
   - Task list filtering
   - Member management

3. Security hardening:
   - CSRF token validation in all POST/PATCH/DELETE requests
   - Password hashing verification (bcrypt cost=12 or Argon2)
   - Session expiration testing (30-day TTL)
   - SQL injection prevention (parameterized queries verified)
   - Rate limiting implemented (login 5/min, password reset 3/hour, API 100/15min)

4. Performance optimization:
   - Database indexes verified (18+ indexes per ERD)
   - Query optimization (N+1 prevention, select_related/prefetch_related)
   - Caching strategy (TanStack Query cache invalidation)
   - Load testing (1000 concurrent users on household/task endpoints)

5. Documentation:
   - API documentation (OpenAPI rendered)
   - Deployment guide
   - Development setup guide
   - Security considerations document
   - Testing guide

**Acceptance Criteria:**
- [ ] Backend: 90%+ code coverage (unit + integration tests)
- [ ] Backend: Authorization tests: 100+ test cases for permission matrix
- [ ] Backend: All 40+ API endpoints have integration tests
- [ ] Backend: Rate limiting configured and tested
- [ ] Backend: SQL injection prevention verified (parameterized queries only)
- [ ] Backend: CSRF tokens generated and validated
- [ ] Frontend: 70%+ component coverage
- [ ] Frontend: E2E tests cover full user workflows
- [ ] Security: Password reset token validated (hashed, one-time use, 1-hour expiration)
- [ ] Security: Session cookie flags set (HttpOnly, Secure, SameSite=Strict)
- [ ] Performance: GET /households/{id}/tasks with 1000 tasks returns <200ms
- [ ] Performance: No N+1 queries in API responses
- [ ] Documentation: Deployment guide tested (can deploy MVP with guide)

**Dependencies:**
- Milestone 5 (all features implemented)
- Performance targets defined (from non-functional requirements in PRD)

**Risks:**
- Finding critical security bugs late: Mitigate with security review early (not waiting for M6)
- Performance issues requiring major refactoring: Mitigate with early load testing during M4/M5
- Low test coverage hiding bugs: Mitigate with test coverage requirements and review

**Cross-Repository Concerns:**
- Backend and Frontend must both have tests run in CI/CD
- Test data seeding scripts (fixtures) for integration tests
- Both teams must agree on test coverage minimums

---

## Milestone 7: Launch Preparation & Go-Live

**Objective:** Final verification, deployment, and launch of MVP.

**Scope:**
- Deployment infrastructure setup
- Pre-launch verification
- Monitoring setup
- Documentation publication
- Launch

**Repositories Involved:**
- Infrastructure (primary)
- Backend
- Frontend
- Documentation
- Automation

**Prerequisites:**
- Milestone 6 complete (all testing done)
- Deployment platform chosen (Heroku/AWS/DigitalOcean)
- DNS/domain configured

**Deliverables:**
1. Deployment:
   - Docker images built and pushed to registry
   - Environment variables configured (production secrets)
   - Database seeded and migrated
   - Static assets built (Frontend)
   - Load balancer/reverse proxy configured (if needed)

2. Monitoring:
   - Logging configured (structured JSON logs to stdout)
   - Error tracking setup (Sentry free tier or similar)
   - Health check endpoint implemented
   - Basic metrics/dashboards (post-MVP, or simple logs)

3. Pre-launch verification:
   - Smoke tests on production environment
   - Database backup/restore tested
   - Rollback procedure documented and tested
   - Performance baseline measured
   - Security scan completed (dependency vulnerabilities)

4. Documentation:
   - User guide (how to use HouseHoldHub)
   - Admin guide (if needed)
   - API documentation published
   - Architecture documentation published
   - Deployment runbook

5. Launch:
   - Feature flag for MVP features (if post-MVP features already exist)
   - Announcement/marketing (if applicable)
   - Monitor for issues first 24 hours

**Acceptance Criteria:**
- [ ] Deployment: Infrastructure as Code (Dockerfile, docker-compose, deployment config)
- [ ] Deployment: Production secrets in environment variables (not committed)
- [ ] Deployment: Database migrations run automatically on deployment
- [ ] Monitoring: Errors logged to Sentry or similar with context
- [ ] Monitoring: Application health check endpoint responds 200
- [ ] Verification: Smoke tests pass (signup, create household, create task)
- [ ] Verification: Database backup tested (can restore to point-in-time)
- [ ] Verification: Load test shows <500ms response time at 100 concurrent users
- [ ] Documentation: Setup guide tested with new developer
- [ ] Documentation: Deployment runbook tested (someone new can deploy)
- [ ] Security: Dependency scan shows no critical vulnerabilities
- [ ] Launch: MVP accessible at production URL
- [ ] Launch: 99%+ uptime in first 24 hours

**Dependencies:**
- Milestone 6 (all testing complete)
- Infrastructure platform selected and configured
- Domain/DNS configured

**Risks:**
- Deployment day surprises: Mitigate by testing deployment in staging environment first
- Production secrets leaked: Mitigate by never committing secrets, using secrets manager
- Database migration failures in production: Mitigate by testing migrations on prod-like DB first
- Performance degradation in production: Mitigate by load testing before launch

**Cross-Repository Concerns:**
- All repos must have Docker images that work together
- CI/CD must automatically build and push images on main branch
- Deployment orchestration (database → backend → frontend, in order)
- Post-deployment smoke tests across all services

---

## Dependency Graph

```
Milestone 1: Foundation
  ↓ (all depend on M1)
Milestone 2: Authentication
  ↓ (M3-M5 depend on M2)
Milestone 3: Household & Membership
  ↓ (M4-M5 depend on M3)
Milestone 4: Tasks
  ↓ (M5 depends on M4)
Milestone 5: Shopping, Expenses, Inventory
  ↓ (M6 depends on M5)
Milestone 6: Testing & Security
  ↓ (M7 depends on M6)
Milestone 7: Launch
```

**Critical Path:** M1 → M2 → M3 → M4 → M5 → M6 → M7 (linear; cannot parallelize)

**Parallelization Opportunities:**
- Within M1: All repos can work in parallel (frontend, backend, infra, docs)
- Within M2: Backend auth endpoints (1.5w) can be parallelized with Frontend UI (2w) if both work to OpenAPI spec
- Within M3: Similar parallel opportunity (backend 1.5w, frontend 2w)
- Within M4: Task backend can be done in parallel with Frontend (backend 1w, frontend 1.5w)
- Within M5: Shopping/Expenses/Inventory can all be developed in parallel (backend), with Frontend following

**Estimated Parallelized Timeline:**
- M1: 1 week (parallel)
- M2: 2 weeks (parallel backend 1.5w + frontend 2w)
- M3: 2 weeks (parallel backend 1.5w + frontend 2w)
- M4: 1.5 weeks (parallel backend 1w + frontend 1.5w)
- M5: 2 weeks (parallel shopping/expense/inventory + UI development)
- M6: 1.5 weeks (testing + security)
- M7: 0.5 weeks (launch)

**Total: ~10.5 weeks (with parallelization)**

---

## Critical Cross-Repository Dependencies

### Backend → Frontend Contract
- **OpenAPI Specification** is the contract; any deviation is a breaking change
- Frontend must never call undocumented endpoints
- Backend must never change response format without updating OpenAPI spec
- Both teams must review OpenAPI spec changes before implementing

### Database → Backend
- Django ORM models must match ERD exactly
- FK constraints must match deletion behavior specified in ERD
- Indexes must be created for performance (18+ per ERD)
- Soft-delete via `deleted_at` must be implemented consistently

### Authentication → All Features
- Every endpoint after M2 must validate session (via middleware)
- Household membership check must be on every endpoint that accesses household data
- Cross-household isolation must be tested on every feature (M3-M5)

### Household/Membership → Task/Shopping/Expense/Inventory
- Task assignment must reference Membership (not User) to enforce household scoping
- Authorization checks must follow: creator/owner for delete; any member for create
- Soft-delete of household must NOT cascade-delete tasks/shopping/expenses/inventory (data preservation)

### Frontend → Backend API Availability
- Frontend can only proceed with UI development once Backend API is specified (OpenAPI)
- Frontend can mock API responses while Backend is implemented, using OpenAPI spec as contract
- Frontend must point to correct Backend URL (environment variable: REACT_APP_API_URL)

### Automation → All Repositories
- CI/CD must run tests on every PR (backend tests, frontend tests)
- CI/CD must prevent merge if tests fail
- Deployment pipeline must be tested before M7

---

## Next Section: Proposed GitHub Issues

[Issues organized by milestone and repository follow below...]

---

