# HouseHoldHub MVP - Revised Implementation Plan

**Date:** August 16, 2026  
**Status:** Approved (ready for GitHub issue creation)  
**Revision Focus:** Parallelizable milestones, explicit testing per feature, Dashboard restoration, issue consolidation

---

## Executive Summary

**Major Changes from Original Plan:**

1. **Milestone Structure:** Shifted from 7 linear milestones to 10 parallelizable milestones (M0-M9) with explicit dependencies
2. **Parallelization:** After M2 (Household & Membership), Tasks, Shopping, Expenses, and Inventory can develop in parallel
3. **Dashboard Restoration:** Added M7 as explicit product feature (household overview, task summaries, quick actions)
4. **Testing Moved Upstream:** Each feature milestone includes its own unit/integration/authorization tests; M8 focuses on cross-domain E2E
5. **Issue Consolidation:** Reduced from 71 to 63 issues through:
   - Consolidating Documentation setup (3 issues → 1)
   - Moving test acceptance criteria into feature issues where appropriate
   - Removing "documentation-only" issues; documentation is part of feature DoD
6. **Repository Clarity:** Distinguished Infrastructure (runtime/deployment) from Automation (reusable dev automation)
7. **API Contract First:** Frontend can develop in parallel using OpenAPI spec + generated types; doesn't require Backend implementation

---

## Revised Milestone Dependency Graph (10 Milestones: M0-M9)

```
                      M0: Engineering Foundation
                              ↓
                    M1: Identity & Authentication
                              ↓
                    M2: Household & Membership
                    /        |         |         \
                   /         |         |          \
            M3: Tasks    M4: Shopping  M5: Expenses  M6: Inventory
        (may run in parallel; independently executable after M2)
                    \         |         |          /
                     \        |         |         /
                           M7: Dashboard
                              ↓
                    M8: Integration & Hardening
                              ↓
                        M9: Deployment Readiness
```

**Critical Path:** M0 → M1 → M2 → max(M3, M4, M5, M6) → M7 → M8 → M9

**Planning Estimate:** ~9-10 weeks (rough planning assumption only; not a calendar commitment; actual duration depends on team capacity and historical velocity data)

---

## Milestone Definitions

### M0: Engineering Foundation (Week 1)

**Objective:** Establish development environment, infrastructure, and baseline for all teams.

**Scope:**
- Backend: Django 6.x scaffold, database models stub, DRF configuration
- Frontend: React 19 + TypeScript scaffold, API client, type generation from OpenAPI
- Infrastructure: PostgreSQL, Docker Compose, environment templates
- Automation: GitHub Actions for Backend/Frontend/Docker
- Documentation: Repository structure, OpenAPI spec publication, developer setup guide

**Key Decisions:**
- Keep Foundation minimal: no production deployment infrastructure, no Redis, no monitoring platforms
- Docker Compose for local development only (not production)
- All configuration via environment variables (secrets management TBD for production)
- OpenAPI specification is the single source of truth for API contract

**Deliverables:**
1. Backend Django project (apps: api, users, households, tasks, shopping, expenses, inventory)
2. Frontend React + Vite project with TypeScript, React Router, TanStack Query
3. Database models skeleton (all 8 entities with stubs, matching ERD)
4. DRF serializers skeleton and permission classes (base classes, not fully implemented)
5. API client (Axios) with HTTP interceptors and error handling
6. **NEW:** TypeScript types generated from OpenAPI spec (via OpenAPI Generator or similar)
7. Docker Compose for local development (PostgreSQL 14+, Django, React)
8. GitHub Actions workflows for:
   - Backend: linting (flake8), type-check, unit tests, coverage
   - Frontend: linting (eslint), type-check (tsc), unit tests, build
   - Automation: Docker image build and push to registry on main branch push
9. Documentation repo with:
   - OpenAPI specification (YAML, rendered via Swagger UI or ReDoc)
   - Developer setup guide (tested with fresh developer; should take <30 min)
   - Architecture documentation index (links to ADRs, System Design, ERD)
   - Contribution guide and code standards

**Key Dependencies:**
- None (foundation)

**Acceptance Criteria:**
- [ ] `python manage.py runserver` on localhost:8000 (dev)
- [ ] `npm run dev` on localhost:3000 (dev)
- [ ] `docker-compose up` brings all services online
- [ ] Django migrations run successfully
- [ ] GitHub Actions runs on PR; enforces passing tests before merge
- [ ] TypeScript types generated from OpenAPI and imported successfully in Frontend
- [ ] Setup guide tested with new developer; completed in <30 minutes
- [ ] All repos have .env.example with documented variables

**Testing:**
- Unit tests for Django models (basic tests included in scaffold)
- Unit tests for utility functions (API client, interceptors, error handling)
- No integration tests yet (no business logic to test)

**Issue Count:** ~16-17 issues

---

### M1: Identity & Authentication (Weeks 2-3)

**Objective:** Implement user signup, login, password reset, session-based authentication.

**Scope:**
- User model, email/password signup, login, password reset
- Session-based authentication (HTTP-only cookies, database-backed sessions)
- Google OAuth 2.0 integration
- Email service integration (SendGrid/SES/Mailgun)
- Frontend auth UI and protected routes
- Comprehensive auth testing and security validation

**Key Decisions:**
- No JWT; database-backed Django sessions (no Redis)
- Session TTL: 14 days (configurable)
- Password reset token: 32-byte random, hashed before storage, 1-hour expiration
- Rate limiting: 5 login attempts per IP per minute; 3 password resets per email per hour

**Deliverables:**
1. User model (email, password_hash, name, google_id, deleted_at, timestamps)
2. Django auth backend (email-based, not username)
3. Session management (HTTP-only cookies, CSRF protection, SameSite=Strict)
4. Auth endpoints:
   - POST /auth/signup (create user + session)
   - POST /auth/login (validate + start session)
   - POST /auth/logout (clear session)
   - POST /auth/forgot-password (send reset email)
   - POST /auth/reset-password (validate token + reset)
   - GET /auth/me (current user)
5. Google OAuth flow (redirect → Google → callback → session)
6. Email service integration (password reset emails, OAuth confirmation emails)
7. Frontend components:
   - AuthContext and useAuth hook
   - Signup page, Login page, Password reset pages
   - ProtectedRoute wrapper for authenticated pages
   - Loading state during auth check
8. Integration tests:
   - Signup flow (valid, invalid email, duplicate, weak password)
   - Login flow (valid, invalid, rate limiting, session persistence)
   - Password reset (valid token, invalid token, expired token)
   - OAuth flow (new user, existing user, logout)
   - Session lifecycle (persistent, expires, CSRF validation)
   - Authorization (401 without session, 200 with session)

**Key Dependencies:**
- M0 complete (Backend API running, Frontend can call it, OpenAPI contract finalized)
- Email service credentials configured (SendGrid/SES/Mailgun)

**Acceptance Criteria:**
- [ ] All 6 auth endpoints match OPENAPI.md exactly
- [ ] Session cookie has HttpOnly, Secure (prod), SameSite=Strict flags
- [ ] Rate limiting enforced (5/min login, 3/hour reset)
- [ ] Password reset token is hashed and one-time use
- [ ] Frontend signup/login flows work end-to-end
- [ ] Google OAuth completes successfully
- [ ] 50+ auth integration test cases; 95%+ coverage
- [ ] Cross-domain isolation test: user from one household cannot see users from another

**Testing:** Continuous
- Unit tests: password hashing, token generation/validation, session lifecycle
- Integration tests: auth endpoints, OAuth flow, session persistence, rate limiting
- Security tests: password reset token handling, session expiration, CSRF tokens
- Authorization tests: 401 responses, session validation

**Issue Count:** ~10 issues

---

### M2: Household & Membership (Weeks 3-4)

**Objective:** Implement household creation, membership management, and invitation system.

**Scope:**
- Household model (soft-delete, code generation, ownership model)
- Membership model (role-based: owner/member)
- Invitation system (email-based, token-based, expiration)
- Authorization middleware (verify household membership on all requests)
- Frontend household selector, creation, management UI

**Key Decisions:**
- Household code: 8-character alphanumeric, unique, regeneration invalidates old code immediately
- Soft-delete: sets deleted_at, preserves data for 30 days before hard-delete
- Ownership: PROTECT FK (cannot delete user if owns household)
- Invitations: 32-byte random token, hashed before storage, 30-day expiration, one-time use

**Deliverables:**
1. Household model (name, description, code, owner_id→User PROTECT, deleted_at, timestamps)
2. Membership model (household_id, user_id, role [owner|member], unique(household_id, user_id), joined_at, CASCADE on both FKs)
3. Invitation model (household_id, email, token_hash, state [pending|accepted|revoked|expired], created_at, expires_at, accepted_at)
4. Household endpoints:
   - GET /households (list user's households)
   - POST /households (create, set owner=current_user)
   - GET /households/{id} (get details)
   - PATCH /households/{id} (update, owner only)
   - DELETE /households/{id} (soft-delete, owner only)
   - GET /households/{id}/code (get current code)
   - POST /households/{id}/code (regenerate, owner only)
   - POST /households/{id}/members (invite by email, owner only)
   - GET /households/{id}/members (list members)
   - DELETE /households/{id}/members/{user_id} (remove member, owner only)
   - POST /households/join (join by code; no {id} — server resolves household from the code)
   - GET /households/{id}/invitations (list invitations, owner only)
   - POST /households/{id}/invitations/{token}/accept (accept invitation)
   - DELETE /households/{id}/invitations/{token} (revoke, owner only)
5. Household authorization middleware (verify membership before accessing household-scoped data)
6. Frontend components:
   - Household selector/switcher (shows user's households, allows switching)
   - Create household form
   - Household settings page (edit name/description, manage members)
   - Member list (remove button for owner)
   - Invite member form
   - Join by code form
   - Accept invitation from email link
7. Email templates: household invitation, invitation accepted
8. Integration tests:
   - Household CRUD (create, edit, soft-delete)
   - Code generation and regeneration
   - Membership authorization (owner vs. member permissions)
   - Invitation flow (send, accept, revoke, expire)
   - Cross-household isolation (non-member cannot access household data; returns 403)
   - User deletion impact (owner protection, member removal)

**Key Dependencies:**
- M1 complete (authentication working)
- OpenAPI spec updated with household endpoints

**Acceptance Criteria:**
- [ ] Household CRUD works; soft-delete preserves data
- [ ] Household code: 8-char unique, regeneration invalidates old code
- [ ] Membership: role-based, creator is owner, others are members
- [ ] Invitations: token-hashed, one-time use, 30-day expiration
- [ ] Authorization: cross-household isolation verified (100+ test cases)
- [ ] User cannot delete household if they own it (PROTECT FK)
- [ ] Removing member: Membership deleted, user loses access
- [ ] Frontend household switcher works; all API calls use active household
- [ ] Frontend invitation email link works end-to-end

**Testing:** Continuous
- Unit tests: soft-delete logic, code generation, token hashing
- Integration tests: CRUD endpoints, invitation flow, code join flow
- Authorization tests: owner-only actions, member permissions, cross-household isolation (100+ cases)
- Security tests: token handling, email link validation

**Issue Count:** ~10 issues

---

### M3: Task Management (Weeks 4-5) — *Parallel after M2*

**Objective:** Implement task CRUD, assignment to household members, completion tracking.

**Scope:**
- Task model (single assignment to Membership, not User)
- Task endpoints with filtering, pagination, authorization
- Frontend task list, creation, editing, assignment, completion UI
- Task authorization and cross-household isolation tests

**Key Decisions:**
- Single assignee per task (references Membership, not User, for household scoping)
- Task deletion: hard-delete only (creator/owner only)
- If assigned member is removed from household: task assigned_to_id → NULL
- Task completion: assigned member or owner only; sets completed_at, completed_by_id

**Deliverables:**
1. Task model (household_id, title, description, due_date, created_by_id→User, assigned_to_id→Membership nullable, completed, completed_by_id→User nullable, completed_at, timestamps)
2. Task endpoints:
   - GET /households/{id}/tasks (list, filters: completed, assigned_to_id, due_date range; pagination)
   - POST /households/{id}/tasks (create, created_by=current_user)
   - GET /households/{id}/tasks/{task_id} (get details)
   - PATCH /households/{id}/tasks/{task_id} (edit: creator/owner can reassign; any member can edit other fields)
   - DELETE /households/{id}/tasks/{task_id} (hard-delete, creator/owner only)
   - PATCH /households/{id}/tasks/{task_id}/complete (mark complete, assigned member or owner only)
3. Task authorization:
   - Creator can edit, reassign, delete
   - Owner can edit, reassign, delete any task
   - Assigned member can mark complete
   - Any member can create
4. Frontend components:
   - Task list page (open/completed sections, filters, pagination)
   - Create task form (title required, description, due_date, assigned_to dropdown)
   - Task detail page (view details, edit button, delete button, complete toggle)
   - Edit task form (pre-fills, reassignment dropdown)
   - Assignment dropdown (shows only household members)
5. Integration tests:
   - Task CRUD (create, read, list, update, delete)
   - Authorization matrix (creator, owner, assigned member, random member, non-member)
   - Task reassignment and unassignment on member removal
   - Filtering (by status, assignee, due date)
   - Cross-household isolation

**Key Dependencies:**
- M2 complete (household & membership working)

**Acceptance Criteria:**
- [ ] All task endpoints match OPENAPI.md
- [ ] Single assignee per task; references Membership (not User)
- [ ] Authorization enforced (creator/owner can edit/delete, assigned member can complete)
- [ ] Task unassigned if member removed from household
- [ ] Frontend filtering and pagination work
- [ ] Frontend task list updates after mutations (TanStack Query invalidation)
- [ ] 50+ authorization test cases for task operations
- [ ] Cross-household isolation verified

**Testing:** Continuous
- Unit tests: task state transitions, completion timestamps
- Integration tests: CRUD endpoints, filtering, pagination, authorization
- Authorization tests: creator/owner/assigned/non-member permissions (50+ cases)
- Security tests: cross-household access prevention

**Issue Count:** ~6 issues

---

### M4: Shopping List (Weeks 4-5) — *Parallel after M2*

**Objective:** Implement shopping list with item tracking and purchase status.

**Scope:**
- ShoppingItem model (name, quantity, purchased status, payer)
- Shopping endpoints (CRUD, filtering by purchase status)
- Frontend shopping list UI with sections and status toggle

**Key Decisions:**
- Any household member can create shopping items
- Creator and owner can edit/delete
- Any member can toggle purchased status
- Hard-delete only (no soft-delete for shopping items)

**Deliverables:**
1. ShoppingItem model (household_id, name, quantity, purchased, purchased_by_id→User nullable, purchased_at nullable, created_by_id→User, timestamps)
2. Shopping endpoints:
   - GET /households/{id}/shopping (list, filters: purchased status; pagination)
   - POST /households/{id}/shopping (create item, created_by=current_user)
   - PATCH /households/{id}/shopping/{item_id} (update name/quantity/purchased)
   - DELETE /households/{id}/shopping/{item_id} (delete, creator/owner only)
   - DELETE /households/{id}/shopping/purchased (bulk-delete all purchased items; requires household membership; per FR-44 — bulk permanent deletion, not an archive)
3. Frontend components:
   - Shopping list page (pending and purchased sections)
   - Add item form (name required, quantity)
   - Edit item form
   - Toggle purchased checkbox
   - Delete button
   - "Clear purchased" bulk action button with confirmation dialog
4. Tests:
   - CRUD operations
   - Authorization (creator/owner can delete, any member can toggle)
   - Cross-household isolation

**Key Dependencies:**
- M2 complete (household & membership working)

**Acceptance Criteria:**
- [ ] All shopping endpoints match OPENAPI.md
- [ ] Item list filtered by purchased status
- [ ] Any member can toggle purchased; sets purchased_by_id and purchased_at
- [ ] Frontend sections (pending/purchased) update on status change
- [ ] Authorization enforced for delete operations

**Testing:** Continuous
- Unit tests: state transitions
- Integration tests: CRUD endpoints, filtering
- Authorization tests: delete permissions
- Cross-household isolation

**Issue Count:** ~4-5 issues

---

### M5: Expense Tracking (Weeks 4-5) — *Parallel after M2*

**Objective:** Implement expense tracking with category breakdown and payer attribution.

**Scope:**
- Expense model (amount_cents, category, payer, creator)
- Expense endpoints (CRUD, filtering, sorting)
- Frontend expense list with category breakdown

**Key Decisions:**
- Amount stored in cents (no decimals)
- Payer: defaults to creator, immutable after creation (PROTECT)
- Creator and owner can edit/delete (except payer field)
- Any member can view
- Hard-delete only

**Deliverables:**
1. Expense model (household_id, amount_cents, category [groceries|utilities|entertainment|other], payer_id→User PROTECT, description, created_by_id→User, timestamps)
2. Expense endpoints:
   - GET /households/{id}/expenses (list, filters: category, payer, date range; sorted by date desc; pagination; response meta includes total_cents and by_category aggregates over all filtered expenses, not just the current page — satisfies FR-49)
   - POST /households/{id}/expenses (create, defaults payer=creator)
   - PATCH /households/{id}/expenses/{expense_id} (update except payer, creator/owner only)
   - DELETE /households/{id}/expenses/{expense_id} (hard-delete, creator/owner only)
3. Frontend components:
   - Expense list page (sorted by date, shows total and per-category breakdown)
   - Create expense form (amount in dollars converted to cents, category dropdown, payer dropdown, description)
   - Edit expense form
   - Delete button with confirmation
   - Category breakdown stats (pie chart or text summary)
4. Tests:
   - CRUD operations
   - Amount validation (no negative, no decimals)
   - Payer immutability
   - Authorization
   - Cross-household isolation

**Key Dependencies:**
- M2 complete

**Acceptance Criteria:**
- [ ] All expense endpoints match OPENAPI.md
- [ ] Amount stored in cents (not decimals)
- [ ] Payer immutable after creation
- [ ] Filtering by category, payer, date range works
- [ ] Sorted by date (newest first)
- [ ] Frontend shows total and per-category breakdown
- [ ] Authorization enforced

**Testing:** Continuous
- Unit tests: amount conversion, state validation
- Integration tests: CRUD endpoints, filtering, sorting
- Authorization tests: payer immutability, delete permissions
- Cross-household isolation

**Issue Count:** ~4-5 issues

---

### M6: Inventory Management (Weeks 4-5) — *Parallel after M2*

**Objective:** Implement flexible inventory tracking with categories and locations.

**Scope:**
- InventoryItem model (name, quantity, unit, category, location)
- Inventory endpoints (CRUD, filtering)
- Frontend inventory list with optional category filtering

**Key Decisions:**
- Quantity is a positive integer (not a freeform string); optional free-form `unit` field for display (e.g., "boxes", "bottles")
- Optional category and location fields
- Creator and owner can edit/delete
- Hard-delete only

**Deliverables:**
1. InventoryItem model (household_id, name, quantity [positive integer], unit nullable, category nullable, location nullable, created_by_id→User, timestamps)
2. Inventory endpoints:
   - GET /households/{id}/inventory (list, filters: category optional; pagination)
   - POST /households/{id}/inventory (create item)
   - PATCH /households/{id}/inventory/{item_id} (update quantity/unit/category/location)
   - DELETE /households/{id}/inventory/{item_id} (hard-delete, creator/owner only)
3. Frontend components:
   - Inventory list page (filterable by category)
   - Add inventory form (name required, quantity as number input, optional unit/category/location)
   - Edit inventory form
   - Increment/decrement controls (operate on integer quantity)
   - Delete button
4. Tests:
   - CRUD operations
   - Quantity validation (positive integer; reject freeform strings)
   - Optional field validation
   - Authorization
   - Cross-household isolation

**Key Dependencies:**
- M2 complete

**Acceptance Criteria:**
- [ ] All inventory endpoints match OPENAPI.md
- [ ] Quantity is a positive integer; unit is optional free-form text
- [ ] Category/location optional
- [ ] Filtering by category works
- [ ] Quantity increments/decrements correctly
- [ ] Authorization enforced

**Testing:** Continuous
- Unit tests: state transitions
- Integration tests: CRUD endpoints, filtering
- Authorization tests: delete permissions
- Cross-household isolation

**Issue Count:** ~4-5 issues

---

### M7: Dashboard (Weeks 5-6)

**Objective:** Implement minimal household dashboard with overview and quick actions.

**Approved Scope (MUST-HAVE):**
- Household identification (name, member count)
- Member overview (list of household members)
- Pending tasks (open, due-soon, overdue)
- Shopping summary (pending item count)
- Quick task creation button
- Quick shopping item creation button

**Explicitly NOT Included:**
- ✗ Analytics, trends, productivity metrics
- ✗ Charts, rankings, visualizations
- ✗ Activity feeds, notifications, activity tracking
- ✗ Expense settlements, splitting, reconciliation
- ✗ Archive or history views
- ✗ Real-time updates or WebSockets

**Deliverables:**
1. Dashboard endpoint:
   - GET /households/{id}/dashboard (aggregated data)
   - Returns: household info, members, pending tasks (3), shopping (pending count), expenses (last 5, total)
2. Frontend Dashboard page:
   - Household card (name, member count, code)
   - Pending tasks widget (due soon/overdue, quick complete toggle)
   - Shopping summary (count, quick add button)
   - Recent expenses (last 5, total)
   - Quick action buttons (create task, add shopping item)
   - Link to detailed views (tasks, shopping, expenses, inventory, settings)
3. Tests:
   - Dashboard endpoint returns correct aggregated data
   - Authorization (only members see their household dashboard)
   - Data freshness (reflects latest changes)

**Key Dependencies:**
- M3, M4, M5, M6 complete (tasks, shopping, expenses, inventory working)

**Acceptance Criteria:**
- [ ] Dashboard endpoint match OPENAPI.md
- [ ] Displays household info, members, pending tasks (up to 3), shopping summary, recent expenses
- [ ] Quick action buttons work (create task, add shopping item)
- [ ] Responsive design
- [ ] Authorization verified (only members see their household)

**Testing:**
- Unit tests: data aggregation logic
- Integration tests: dashboard endpoint, data freshness
- Authorization tests: member-only access

**Issue Count:** ~2 issues (Backend endpoint + Frontend page)

---

### M8: Integration & Hardening (Weeks 6-7)

**Objective:** Cross-domain integration validation, security and accessibility review, regression testing, performance confirmation.

**Scope (Cross-Cutting Only — No Duplication of Feature Tests):**
- Complete end-to-end user journeys (signup → household → task → dashboard, etc.)
- Cross-domain integration (task creation appears on dashboard, expenses affect household view, etc.)
- Authorization regression (verify PROTECT/403/401 behaviors hold across all endpoints)
- Cross-household isolation (user A in household X cannot access household Y data)
- Security review (CSRF, rate limiting, password hashing, SQL injection prevention)
- Accessibility review (WCAG 2.1 AA compliance)
- API contract conformance (Backend endpoints match OPENAPI.md exactly)
- Regression testing (smoke tests ensure all M0-M7 features still work)
- Performance confirmation (hit targets: <200ms for large datasets, <500KB bundle, <500ms at 100 concurrent users)
- Documentation finalization

**Note:** Feature-level unit tests, API tests, and component tests belong in M0-M7. M8 does NOT repeat them; M8 validates integration and holistic properties.

**Key Deliverables:**
1. **End-to-End Workflows:**
   - Signup → create household → invite member → member joins → create task → mark complete → view on dashboard
   - Create expense → appears on dashboard → filters work → delete works
   - Add shopping items → toggle purchased → view on dashboard
   - Member removal → user loses access → tasks unassigned
   - Cross-household isolation verified
2. **Security & Compliance Review:**
   - CSRF token validation on all state-changing requests
   - Password hashing (bcrypt/Argon2) verified
   - Session expiration and cleanup working
   - SQL injection prevention (parameterized queries only)
   - Rate limiting enforced (login 5/min, reset 3/hour, API 100/15min)
   - Input validation (format, length, enum, type)
   - Authorization matrix verified (403/401 correct)
3. **Accessibility Review:**
   - WCAG 2.1 AA compliance check
   - Keyboard navigation tested
   - Screen reader compatibility verified
4. **API Contract Validation:**
   - Every endpoint tested against OPENAPI.md spec
   - Response formats match spec
   - Error codes correct
5. **Performance Confirmation:**
   - Database indexes in place (18+ per ERD)
   - No N+1 queries
   - Load test: 100 concurrent users target <500ms response
   - Frontend bundle <500KB main chunk
   - GET large datasets (1000 tasks) target <200ms
6. **Documentation Finalization:**
   - API documentation (OpenAPI rendered)
   - Deployment guide (step-by-step)
   - Development setup guide (tested with fresh developer)
   - Security considerations (CSRF, rate limiting, session management)
   - Testing guide
   - Troubleshooting guide

**Acceptance Criteria:**
- [ ] End-to-end workflows: signup → household → task → dashboard (full user journey passes)
- [ ] Backend: 90%+ code coverage (unit + integration)
- [ ] Backend: 100+ cross-domain integration test cases
- [ ] Backend: 100+ authorization/isolation test cases
- [ ] Backend: All 40+ API endpoints have integration tests
- [ ] Frontend: 70%+ component coverage
- [ ] Frontend: E2E tests for critical workflows (login, create household, create task, view dashboard)
- [ ] Security: Password reset token tested (hashed, one-time, 1-hour expiration)
- [ ] Security: Session cookie flags correct (HttpOnly, Secure, SameSite=Strict)
- [ ] Security: Rate limiting enforced and tested
- [ ] Performance: GET /households/{id}/tasks with 1000 tasks returns <200ms
- [ ] Performance: No N+1 queries detected
- [ ] Performance: Bundle size <500KB main chunk
- [ ] Documentation: All 4 guides tested with external person

**Testing:** Comprehensive
- Integration tests across all domains
- Security tests (auth, rate limiting, validation, injection prevention)
- Performance tests (load testing, query analysis, bundle size)

**Issue Count:** ~7-8 issues

---

### M9: Deployment Readiness (Week 8)

**Objective:** Prepare for production launch: Docker images, monitoring, final verification, go-live.

**Scope:**
- Production deployment setup (Docker images, environment configuration)
- Monitoring and observability (error tracking, logging)
- Pre-launch verification (smoke tests, backups, security scan)
- Launch and early monitoring

**Deliverables:**
1. Deployment infrastructure:
   - Docker images: Django (optimized, Alpine-based), React (nginx-based), PostgreSQL
   - Environment variables configured for production (secrets via environment, not committed)
   - Database migrations automated on deployment
   - Static assets built and optimized (React)
   - Health check endpoint (/health, returns 200 OK when ready)
2. Monitoring setup:
   - Structured JSON logging to stdout
   - Error tracking (Sentry free tier or similar)
   - Application health dashboard (basic metrics)
3. Pre-launch verification:
   - Smoke tests on production environment (signup, create household, create task)
   - Database backup tested and restore procedure documented
   - Rollback procedure documented and tested
   - Security scan: dependency vulnerabilities checked (pip audit, npm audit)
   - Load test baseline: 100 concurrent users, target <500ms response
   - Performance baseline: response times, bundle sizes, database queries
4. Launch:
   - Feature flags (if necessary; probably not for MVP launch)
   - Announcement/marketing (if applicable)
   - First 24 hours monitoring (watch for errors, performance issues)
   - Post-launch incident response runbook

**Acceptance Criteria:**
- [ ] Deployment: Dockerfile for all services; images built and pushed to registry
- [ ] Deployment: Production secrets in environment (not committed)
- [ ] Deployment: Database migrations run automatically on deploy
- [ ] Monitoring: Errors logged to Sentry with context
- [ ] Monitoring: Health check endpoint responds 200
- [ ] Verification: Smoke tests pass (signup, household, task)
- [ ] Verification: Database backup tested
- [ ] Verification: Load test shows <500ms at 100 concurrent users
- [ ] Security: Dependency scan shows no critical vulnerabilities
- [ ] Launch: MVP accessible at production URL
- [ ] Launch: Incident response runbook documented

**Issue Count:** ~3 issues

---

## Summary of Issues by Repository and Milestone

**Note:** This table reflects the actual current GitHub backlog (as created), not the original 68-issue planning estimate below. Backend has no M9 milestone (deployment issues for that domain are not tracked there); Backend M6 and Frontend M6 issue counts were also corrected against the live backlog.

| Repository | M0 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | Total |
|------------|----|----|----|----|----|----|----|----|----|----|-------|
| **Backend** | 5 | 5 | 6 | 3 | 3 | 3 | 3 | 1 | 3 | 0 | 32 |
| **Frontend** | 4 | 4 | 5 | 2 | 2 | 2 | 2 | 1 | 2 | 0 | 24 |
| **Infrastructure** | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 4 |
| **Automation** | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 4 |
| **Documentation** | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 3 |
| **TOTAL** | 16 | 9 | 11 | 5 | 5 | 5 | 5 | 2 | 6 | 3 | **67** |

**Planning history:** Original scoping reduced from 71 to a 68-issue estimate through consolidation (documentation setup 3→1, test acceptance criteria folded into feature issues, M5 reorganized into parallel M3-M6). The actual created backlog is 67 issues — close to but not identical to the estimate, which was never a hard target. Issue count is not tracked as a completion metric; scope and acceptance criteria are.

---

## Critical Cross-Repository Dependencies

### M0 → Everything
- Backend and Frontend scaffolds must be compatible
- Docker Compose must coordinate ports and services
- OpenAPI spec is published in Documentation; both teams reference it
- GitHub Actions must be working (enforces test passage before merge)

### M1 → M2+
- Auth endpoints must be implemented before household features
- Session middleware must be configured before any other endpoints

### M2 → M3-M6 (Parallel)
- Household membership check required for all feature endpoints
- Each feature (task, shopping, expense, inventory) is independent after M2

### M3-M6 → M7 (Dashboard)
- Dashboard aggregates data from all four feature domains
- Must wait for all features to be stable before building dashboard

### M3-M7 → M8 (Integration)
- All features must be implemented before end-to-end testing
- Performance baseline requires realistic data volumes

### M7-M8 → M9 (Deployment)
- All testing and security hardening must be complete
- Smoke tests and load tests run before launch

---

## API Contract Separation: Frontend Independence

**Frontend can develop in parallel without waiting for Backend implementation:**

1. **Week 1 (M0):** Generate TypeScript types and API client from OpenAPI spec
   - Tool: OpenAPI Generator, swagger-typescript-api, or similar
   - Output: `src/types/api.ts` with all request/response types
   - Output: `src/api/client.ts` with API methods typed from spec
2. **Week 2+ (M1+):** Frontend uses generated types and creates mock API responses
   - Mock API responses matching OpenAPI spec
   - Frontend UI development proceeds in parallel
   - Test UI logic against mocked API
3. **Integration:** Once Backend implements endpoints, Frontend switches from mock to real API
   - No changes needed if Backend adheres to OpenAPI spec (contract)
   - Full integration tests run when both sides are ready

**Backend Responsibility:**
- Implement endpoints exactly as specified in OPENAPI.md
- Update OpenAPI spec BEFORE implementation changes
- Write integration tests validating each endpoint against OpenAPI spec

---

## MVP Completion Gates (Release-Level Acceptance Criteria)

**Requirement:** All 10 user journeys must pass end-to-end before release. Closing GitHub issues alone is NOT sufficient for launch.

**Critical User Journeys (Must All Pass):**

### Journey 1: User Signup & Household Creation
```
1. User navigates to app
2. Signup page loads
3. User enters email, password, name
4. User submits signup
5. Account created, session started
6. Redirected to household selector
7. "Create Household" button available
8. User enters household name
9. Household created, user is owner
10. Dashboard loads for household
```
✓ **Gate Criteria:** User can create account and household; can access household dashboard

### Journey 2: Household Invitation & Member Join
```
1. Owner navigates to household settings
2. Member list visible
3. Owner enters member email in invite form
4. Invitation sent (email received)
5. Member clicks email link
6. Joins household, redirected to dashboard
7. Can see household tasks and data
```
✓ **Gate Criteria:** Invitation flow works end-to-end; member can join and access data

### Journey 3: Household Code Join (Alternative)
```
1. Owner views household settings
2. Copies household code
3. Shares code with member
4. Member uses "Join by Code" button
5. Enters code
6. Joins household immediately
7. Household appears in selector
```
✓ **Gate Criteria:** Code-based join works; immediate access granted

### Journey 4: Task Management
```
1. User views household dashboard
2. "Create Task" button available
3. User creates task (title, description, due date, assignee)
4. Task appears on dashboard and in task list
5. Assigned member marks task complete
6. Dashboard updates to show completion
7. Task moves to "Completed" section
```
✓ **Gate Criteria:** Tasks can be created, assigned, completed; updates appear immediately

### Journey 5: Shopping List
```
1. User navigates to shopping list
2. Adds shopping item (name, quantity)
3. Item appears on list under "Pending"
4. Member marks item purchased
5. Item moves to "Purchased" section
6. Shopping summary shows on dashboard
```
✓ **Gate Criteria:** Shopping items work; purchase toggle updates immediately

### Journey 6: Expense Tracking
```
1. User navigates to expenses
2. Creates expense (amount, category, payer, description)
3. Expense appears on list with date, amount, payer
4. Expense filters work (by category, payer, date)
5. Expense total and breakdown shows
6. Recent expenses appear on dashboard
```
✓ **Gate Criteria:** Expenses work; filters, totals, dashboard integration correct

### Journey 7: Inventory Management
```
1. User navigates to inventory
2. Adds inventory item (name, quantity, category, location)
3. Item appears in list
4. Item filters work (by category)
5. Item quantity can be edited
6. Item can be deleted
```
✓ **Gate Criteria:** Inventory works; basic CRUD operations correct

### Journey 8: Household Switching
```
1. User with multiple households in selector
2. Clicks switcher dropdown
3. Selects different household
4. Dashboard reloads for new household
5. Tasks, shopping, expenses are from new household
6. Cross-household isolation: cannot see data from other households
```
✓ **Gate Criteria:** Household switching works; no cross-household data leakage

### Journey 9: Member Removal & Permission Loss
```
1. Owner navigates to household settings
2. Removes member from household
3. Member logs out and logs back in
4. Household no longer visible in selector
5. Cannot access household data (GET request returns 403)
6. Tasks assigned to removed member are unassigned (assigned_to_id = NULL)
```
✓ **Gate Criteria:** Member removal works; access lost immediately; no orphaned tasks

### Journey 10: Authorization Isolation
```
1. User is member (not owner) of household
2. Attempts to delete household (DELETE /households/{id})
3. Gets 403 Forbidden
4. Cannot remove other members
5. Cannot edit household settings
6. Owner can perform all actions
```
✓ **Gate Criteria:** Authorization matrix enforced; non-owners have read-only access (mostly)

**MVP Releasable When:** All 10 user journeys pass end-to-end AND performance baseline met (<500ms at 100 concurrent users)

---

## Timeline Estimate (Preliminary)

**Note:** This is a planning assumption, not a commitment. Actual velocity depends on team size, experience, and complexity encountered.

- **M0:** 1 week (foundation setup)
- **M1:** 2 weeks (auth + email)
- **M2:** 1.5 weeks (household + membership)
- **M3-M6:** 2 weeks (parallel feature development; critical path is longest feature, ~1.5 weeks)
- **M7:** 0.5 weeks (dashboard)
- **M8:** 1.5 weeks (integration + hardening)
- **M9:** 0.5 weeks (deployment + launch)

**Total: ~9-10 weeks (with 4-way parallelization in M3-M6)**

---

## Key Consolidations from Original Plan

1. **Documentation Setup (M0):**
   - Original: 3 issues (1.6 OpenAPI, 1.7 dev setup, 1.11 docs structure)
   - Revised: 1 issue covering all three
   - Rationale: All documentation tasks are related and belong in Documentation repo; can be completed together

2. **Testing Strategy:**
   - Original: Separate test issues for auth (2.6), tasks (4.3); shopping/expenses/inventory tests buried in M6
   - Revised: Each feature includes tests in acceptance criteria or as separate issue if complex
   - Rationale: Testing is continuous; M6 focuses on cross-domain, not catching up

3. **Dashboard:**
   - Original: Not explicitly represented; implied in "M6 testing"
   - Revised: Explicit M7 milestone with specific scope
   - Rationale: Product requirement from PRD; needs dedicated work after features are stable

4. **Milestone Structure:**
   - Original: Linear M1 → M7
   - Revised: Parallelizable M0 → M1 → M2 → {M3-M6 parallel} → M7 → M8 → M9
   - Rationale: Shopping, Expenses, Inventory are independent after Household/Membership; can develop in parallel with Tasks

5. **Infrastructure vs. Automation:**
   - Original: Mixed concerns (Docker Compose in Backend, Docker build in Automation)
   - Revised: Clear separation:
     - Infrastructure: PostgreSQL, env config, Docker image specs, production deployment
     - Automation: CI/CD pipelines (GitHub Actions), test automation, build automation
   - Rationale: Different responsibilities; different teams likely

---

## Next Steps for Review

1. **Verify Milestone Structure**
   - Does M0-M9 breakdown make sense?
   - Are dependencies correct?
   - Can M3-M6 truly be parallelized, or are there hidden dependencies?

2. **Validate Issue Count & Sizing**
   - Are 68 issues appropriately sized?
   - Are there further consolidation opportunities?
   - Are any issues too small or too large?

3. **Confirm Testing Approach**
   - Is continuous testing per feature sufficient?
   - Should M8 (Integration & Hardening) have dedicated test issues?
   - Are acceptance criteria in feature issues clear enough for testing?

4. **Confirm Feature Scope**
   - Dashboard scope: is it focused enough? (excluded analytics, feeds, settlements)
   - Are secondary features (shopping, expenses, inventory) scoped correctly?
   - Is anything missing from MVP scope?

5. **Confirm Dependencies**
   - Are cross-repository dependencies explicit?
   - Is the OpenAPI contract separation clear (Frontend can develop without Backend)?

6. **Confirm MVP Completion Gates**
   - Do the 10 user journeys represent complete MVP acceptance?
   - Are there other critical journeys to include?

---

## Files Provided

- IMPLEMENTATION_PLAN_REVISED.md (this file): 68-issue structure, M0-M9 milestones
- GITHUB_ISSUES_PROPOSAL_REVISED.md (to follow): Detailed issue specifications with new numbering

---
