# HouseHoldHub MVP - GitHub Issues Proposal

**Date:** August 16, 2026  
**Status:** Proposed (awaiting review before creation)  
**Total Issues:** 68 across 5 repositories

---

## Milestone 1: Project Foundation & Infrastructure

### Backend Repository (7 issues)

#### 1.1 Django Project Scaffold
- **Title:** `[M1-Backend] Initialize Django project structure`
- **Goal/Context:** Set up Django project with proper structure for HouseHoldHub MVP. This is the foundation for all backend development.
- **Implementation Scope:**
  - Create Django project: `householdhub`
  - Create Django apps: `api`, `users`, `households`, `tasks`, `shopping`, `expenses`, `inventory`
  - Configure settings.py: database, installed apps, middleware, REST framework, CORS
  - Create requirements.txt with: Django 6.x, DRF, psycopg2, python-decouple
  - Create .env.example with sample environment variables
  - Create manage.py and wsgi.py
- **Acceptance Criteria:**
  - [ ] `python manage.py runserver` starts on localhost:8000
  - [ ] `python manage.py migrate` runs without errors
  - [ ] All Django apps registered in INSTALLED_APPS
  - [ ] DRF configured with JSON renderer and session authentication
  - [ ] CORS configured for localhost:3000 (Frontend)
  - [ ] Database settings use environment variable (DATABASE_URL)
- **Dependencies/Blockers:** Infrastructure repo must have Docker/PostgreSQL ready
- **Relevant System Design References:** Part 3 (Django Implementation)
- **Suggested Labels:** `backend`, `setup`, `high-priority`
- **Milestone:** M1

#### 1.2 Docker Compose Setup
- **Title:** `[M1-Backend] Configure Docker Compose for local development`
- **Goal/Context:** Enable full-stack development with `docker-compose up`. Must coordinate Backend, Frontend, and PostgreSQL.
- **Implementation Scope:**
  - Create docker-compose.yml with services: postgres, django, react
  - Create Dockerfile for Django (Alpine-based, Python 3.14)
  - Create Dockerfile for React (Node + Vite)
  - Create .dockerignore files
  - Document ports: 8000 (Django), 3000 (React), 5432 (PostgreSQL)
  - Volume mounts for code (hot reload in development)
- **Acceptance Criteria:**
  - [ ] `docker-compose up` brings up all three services
  - [ ] Django service connects to PostgreSQL successfully
  - [ ] React service accessible at localhost:3000
  - [ ] Backend API accessible at localhost:8000/api/v1
  - [ ] Hot reload works for Python code changes
  - [ ] Hot reload works for React code changes
- **Dependencies/Blockers:** Requires Django scaffold (1.1) and React scaffold (Frontend 1.1)
- **Relevant System Design References:** Part 8 (Docker Compose Setup)
- **Suggested Labels:** `backend`, `infrastructure`, `docker`, `setup`
- **Milestone:** M1

#### 1.3 Database Models Stub
- **Title:** `[M1-Backend] Create Django ORM stubs for all entities`
- **Goal/Context:** Define empty models for all 8 entities before implementing features. Models should match ERD exactly.
- **Implementation Scope:**
  - User model (email, password_hash, name, google_id, timestamps, deleted_at)
  - Household model (name, description, code, owner_id, timestamps, deleted_at)
  - Membership model (household_id, user_id, role, joined_at, timestamps)
  - Invitation model (household_id, email, token_hash, state, timestamps)
  - Task model (household_id, title, description, due_date, created_by_id, assigned_to_id, completed, completed_at, timestamps)
  - ShoppingItem model (household_id, name, quantity, purchased, purchased_by_id, purchased_at, created_by_id, timestamps)
  - Expense model (household_id, amount_cents, category, payer_id, description, created_by_id, timestamps)
  - InventoryItem model (household_id, name, quantity, category, location, created_by_id, timestamps)
  - Add all FKs, constraints, indexes as documented in ERD.md
- **Acceptance Criteria:**
  - [ ] All 8 models created in Django ORM
  - [ ] All FKs match ERD (CASCADE, SET NULL per specification)
  - [ ] All unique/check constraints created
  - [ ] UUID primary keys used
  - [ ] Meta.unique_together for Membership and Invitation
  - [ ] All timestamps auto_now/auto_now_add set correctly
  - [ ] Soft-delete via deleted_at field (no physical deletion in models yet)
  - [ ] `python manage.py makemigrations` generates migration
  - [ ] `python manage.py migrate` runs successfully
- **Dependencies/Blockers:** Django scaffold (1.1) must be complete
- **Relevant Documentation References:** ERD.md (complete entity definitions), DOMAIN_MODEL_CORRECTED.md (deletion semantics)
- **Suggested Labels:** `backend`, `database`, `models`
- **Milestone:** M1

#### 1.4 Django REST Framework Setup
- **Title:** `[M1-Backend] Configure Django REST Framework and serializers scaffold`
- **Goal/Context:** Set up DRF with basic serializers for all models. Serializers will evolve in each milestone.
- **Implementation Scope:**
  - Create serializers.py in api app with stubs for all 8 models
  - Configure DRF settings: pagination (20 default, max 100), filtering, sorting
  - Create base ViewSet class with household scoping checks
  - Create permission classes: IsAuthenticated, IsHouseholdMember, IsOwner, IsCreator
  - Configure OpenAPI/Swagger documentation
- **Acceptance Criteria:**
  - [ ] All 8 serializers created (ModelSerializer base)
  - [ ] Pagination configured (page, limit, total)
  - [ ] Filtering backend configured
  - [ ] Sorting backend configured
  - [ ] Permission classes created and documented
  - [ ] Swagger documentation accessible at /api/schema/
  - [ ] OpenAPI YAML can be downloaded
- **Dependencies/Blockers:** Django scaffold (1.1), models stub (1.3)
- **Relevant System Design References:** Part 5 (REST API Design), Part 6 (Permissions & Authorization)
- **Suggested Labels:** `backend`, `api`, `drf`
- **Milestone:** M1

#### 1.5 CI/CD Pipeline - Backend
- **Title:** `[M1-Automation] Set up GitHub Actions for Backend tests`
- **Goal/Context:** Automate testing, linting, and coverage checks on every PR.
- **Implementation Scope:**
  - Create .github/workflows/backend-test.yml
  - Steps: checkout, setup Python, install dependencies, lint (flake8), run tests (pytest), coverage report
  - Configure to run on: push to main, pull requests
  - Set required status check (tests must pass before merge)
  - Report coverage to PR (codecov or built-in)
- **Acceptance Criteria:**
  - [ ] Workflow runs on PR and reports results
  - [ ] Linting errors fail the workflow
  - [ ] Test failures fail the workflow
  - [ ] Coverage report visible on PR
  - [ ] Status check required (no merge without passing)
  - [ ] Workflow can be manually triggered for debugging
- **Dependencies/Blockers:** Django scaffold (1.1)
- **Relevant System Design References:** Part 14 (Testing Strategy)
- **Suggested Labels:** `automation`, `ci-cd`, `backend`
- **Milestone:** M1

#### 1.6 OpenAPI Specification Document
- **Title:** `[M1-Documentation] Publish OpenAPI specification to Documentation repo`
- **Goal/Context:** Create single source of truth for API contract. Both Backend and Frontend teams reference this.
- **Implementation Scope:**
  - Copy OPENAPI.md from project root to Documentation repo
  - Set up rendering (Swagger UI or ReDoc)
  - Create README with API documentation overview
  - Document authentication (session-based, HTTP-only cookies)
  - Document error response format
  - Document pagination/filtering conventions
- **Acceptance Criteria:**
  - [ ] OpenAPI YAML accessible via Documentation repo
  - [ ] Swagger UI renders all endpoints
  - [ ] ReDoc renders (or similar tool)
  - [ ] API documentation accessible to all team members
  - [ ] README explains how to use specification
- **Dependencies/Blockers:** None (documentation only)
- **Relevant System Design References:** Part 5 (REST API Design), OPENAPI.md
- **Suggested Labels:** `documentation`, `api`
- **Milestone:** M1

#### 1.7 Development Setup Guide
- **Title:** `[M1-Documentation] Create developer setup guide`
- **Goal/Context:** New developers can set up environment and start coding within 30 minutes.
- **Implementation Scope:**
  - Document prerequisites (Docker, Git, Python, Node)
  - Step-by-step setup: clone repos, `docker-compose up`, verify running
  - Explain directory structure
  - Document database: how to reset, how to seed
  - Document environment variables
  - Troubleshooting section
  - Links to Backend, Frontend, and Infrastructure repos
- **Acceptance Criteria:**
  - [ ] Setup guide tested with fresh developer (not original author)
  - [ ] All steps verified to work
  - [ ] Screenshots/clarity for Docker commands
  - [ ] Explains what each service does
  - [ ] Provides commands for common tasks (reset DB, clear cache, etc.)
- **Dependencies/Blockers:** All M1 Backend items (1.1-1.6)
- **Relevant System Design References:** Part 8 (Development Setup)
- **Suggested Labels:** `documentation`, `setup`
- **Milestone:** M1

---

### Frontend Repository (5 issues)

#### 1.8 React Project Scaffold
- **Title:** `[M1-Frontend] Initialize React 19 + TypeScript + Vite project`
- **Goal/Context:** Set up Frontend project with proper structure, TypeScript, and build tool.
- **Implementation Scope:**
  - Create Vite + React 19 project with TypeScript
  - Install dependencies: react-router, react-query, react-hook-form, zod, axios
  - Configure tsconfig.json
  - Create project structure: src/pages, src/components, src/hooks, src/api, src/context, src/types, src/utils
  - Create .env.example with REACT_APP_API_URL=http://localhost:8000/api/v1
  - Create package.json scripts: dev, build, test
- **Acceptance Criteria:**
  - [ ] `npm run dev` starts dev server on localhost:3000
  - [ ] TypeScript compiles without errors
  - [ ] React Router configured (Routes placeholder)
  - [ ] Axios client configured with base URL from env
  - [ ] TanStack Query (React Query) configured with QueryClient
  - [ ] Build produces bundle
  - [ ] tsconfig paths configured for easy imports (@/components, etc.)
- **Dependencies/Blockers:** Docker Compose setup (1.2) for Node version compatibility
- **Relevant System Design References:** Part 10 (Frontend Architecture)
- **Suggested Labels:** `frontend`, `setup`, `react`
- **Milestone:** M1

#### 1.9 API Client & HTTP Interceptors
- **Title:** `[M1-Frontend] Create API client with Axios and interceptors`
- **Goal/Context:** Centralized HTTP communication with consistent error handling and auth context.
- **Implementation Scope:**
  - Create src/api/client.ts: Axios instance with base URL, interceptors
  - Implement request interceptor: add CSRF token, log requests
  - Implement response interceptor: handle 401 (logout), 403 (permission error), 5xx (error toast)
  - Handle HTTP error responses and map to user-friendly messages
  - Implement retry logic for transient failures (5xx with exponential backoff)
- **Acceptance Criteria:**
  - [ ] Axios client accepts base URL from environment
  - [ ] CSRF tokens included in POST/PATCH/DELETE requests
  - [ ] 401 responses trigger logout redirect
  - [ ] 403 responses show permission error toast
  - [ ] Errors logged with context (URL, params, response)
  - [ ] Retry logic works (max 3 retries, exponential backoff)
- **Dependencies/Blockers:** React scaffold (1.8)
- **Relevant System Design References:** Part 10 (Frontend Architecture), OPENAPI.md (authentication)
- **Suggested Labels:** `frontend`, `api`
- **Milestone:** M1

#### 1.10 CI/CD Pipeline - Frontend
- **Title:** `[M1-Automation] Set up GitHub Actions for Frontend tests`
- **Goal/Context:** Automate linting, type-checking, testing on every PR.
- **Implementation Scope:**
  - Create .github/workflows/frontend-test.yml
  - Steps: checkout, setup Node, install dependencies, lint (eslint), type-check (tsc), test (vitest), build
  - Configure to run on: push to main, pull requests
  - Set required status check
- **Acceptance Criteria:**
  - [ ] Workflow runs on PR
  - [ ] Linting errors fail
  - [ ] Type checking errors fail
  - [ ] Build failures fail
  - [ ] Status check required
- **Dependencies/Blockers:** React scaffold (1.8)
- **Relevant System Design References:** Part 14 (Testing Strategy)
- **Suggested Labels:** `automation`, `ci-cd`, `frontend`
- **Milestone:** M1

#### 1.11 Project Documentation Structure
- **Title:** `[M1-Documentation] Set up Documentation repo structure`
- **Goal/Context:** Centralized place for all documentation: API, architecture, user guides.
- **Implementation Scope:**
  - Create docs/architecture/ with links to ADRs, System Design, ERD, OpenAPI
  - Create docs/api/ with OpenAPI specification
  - Create docs/guides/ with setup guide, deployment guide, etc.
  - Create README.md explaining structure
  - Set up Jekyll or similar for documentation site (optional for MVP)
- **Acceptance Criteria:**
  - [ ] All documentation files linked and organized
  - [ ] README explains structure
  - [ ] Team can easily find: API docs, architecture docs, guides
- **Dependencies/Blockers:** None (documentation only)
- **Relevant System Design References:** All of SYSTEM_DESIGN.md, ERD.md, OPENAPI.md
- **Suggested Labels:** `documentation`
- **Milestone:** M1

---

### Infrastructure Repository (3 issues)

#### 1.12 PostgreSQL Configuration
- **Title:** `[M1-Infrastructure] Configure PostgreSQL for development and production`
- **Goal/Context:** Database infrastructure ready for schema migration and feature development.
- **Implementation Scope:**
  - Create Dockerfile for PostgreSQL (Alpine-based, PostgreSQL 14+)
  - Configure connection settings: host, port, credentials
  - Create docker-compose.yml entry for PostgreSQL service
  - Document backup/restore procedures
  - Create database initialization script (schema, initial data)
  - Set up environment variables for DATABASE_URL
- **Acceptance Criteria:**
  - [ ] PostgreSQL runs in Docker
  - [ ] Connection string in DATABASE_URL format
  - [ ] Database accessible from Django container
  - [ ] Schema can be created with `python manage.py migrate`
  - [ ] Data can be backed up and restored
  - [ ] Persistence: data survives container restart
- **Dependencies/Blockers:** Docker Compose setup (1.2)
- **Relevant System Design References:** Part 7 (Persistence Design), ERD.md (schema)
- **Suggested Labels:** `infrastructure`, `database`, `docker`
- **Milestone:** M1

#### 1.13 Environment Configuration Template
- **Title:** `[M1-Infrastructure] Create .env configuration templates`
- **Goal/Context:** Team members have clear template for environment variables without leaking secrets.
- **Implementation Scope:**
  - Create .env.example with all required environment variables
  - Document each variable: purpose, example value, required/optional
  - Include: DATABASE_URL, SECRET_KEY, DEBUG, ALLOWED_HOSTS, GOOGLE_OAUTH_*, EMAIL_*
  - Create .env.development, .env.staging, .env.production templates
  - Document secrets management (never commit .env, use password manager)
- **Acceptance Criteria:**
  - [ ] .env.example has all variables needed to run system
  - [ ] Each variable documented with purpose
  - [ ] Examples provided for each
  - [ ] README explains how to set up .env locally
  - [ ] Documentation warns against committing .env
- **Dependencies/Blockers:** None (configuration only)
- **Relevant System Design References:** Part 13 (Infrastructure), SYSTEM_DESIGN.md
- **Suggested Labels:** `infrastructure`, `configuration`
- **Milestone:** M1

#### 1.14 Docker Image Build & Push Pipeline
- **Title:** `[M1-Automation] Set up Docker image building and registry push`
- **Goal/Context:** Automate building and pushing Docker images for Backend and Frontend.
- **Implementation Scope:**
  - Create GitHub Actions workflow for Docker image build (on main push, PR)
  - Build and push to Docker registry (Docker Hub or GitHub Container Registry)
  - Tag images with commit SHA and `latest` tag
  - Document image naming conventions
  - Set up registry credentials in GitHub secrets
- **Acceptance Criteria:**
  - [ ] GitHub Actions builds Docker images on push to main
  - [ ] Images pushed to registry with correct tags
  - [ ] Registry credentials securely stored (not in code)
  - [ ] Images can be pulled and run locally
  - [ ] Build process documented
- **Dependencies/Blockers:** Requires Docker Compose setup (1.2)
- **Relevant System Design References:** Part 13 (Infrastructure & Deployment)
- **Suggested Labels:** `automation`, `ci-cd`, `docker`, `infrastructure`
- **Milestone:** M1

---

## Milestone 2: Authentication & Session Management

### Backend Repository (6 issues)

#### 2.1 User Model & Django Auth Setup
- **Title:** `[M2-Backend] Implement User model with email/password authentication`
- **Goal/Context:** Core user account functionality. Foundation for all subsequent authentication.
- **Implementation Scope:**
  - Extend Django's AbstractUser or create custom User model
  - Fields: email (unique, indexed), password_hash, name, google_id (nullable), deleted_at
  - Configure Django auth backend to use email instead of username
  - Implement password hashing with Django's built-in (PBKDF2) or override with bcrypt/Argon2
  - Soft-delete: filter queries with `deleted_at IS NULL`
- **Acceptance Criteria:**
  - [ ] User model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] `python manage.py createsuperuser` works with email
  - [ ] Password stored as hash (not plaintext)
  - [ ] User can be soft-deleted (deleted_at set)
  - [ ] Queries automatically filter deleted users
  - [ ] Migrations work correctly
  - [ ] Django admin works with custom User model
- **Dependencies/Blockers:** Django scaffold (1.1), models stub (1.3)
- **PRD References:** FR-1-7 (authentication requirements)
- **OpenAPI References:** POST /auth/signup, POST /auth/login
- **ADR References:** ADR-002 (Django backend), ADR-004 (session auth)
- **Suggested Labels:** `backend`, `authentication`, `high-priority`
- **Milestone:** M2

#### 2.2 Session Management & Django Sessions Table
- **Title:** `[M2-Backend] Configure session-based authentication with database backend`
- **Goal/Context:** Enable stateful session management with HTTP-only cookies.
- **Implementation Scope:**
  - Configure Django session backend: `django.contrib.sessions.backends.db`
  - Set session middleware (already in scaffold)
  - Configure session cookie settings: HttpOnly=True, Secure=True (prod), SameSite=Strict
  - Set session TTL: 14 days (configurable via SESSION_COOKIE_AGE)
  - Create session cleanup management command: `python manage.py clearsessions`
  - Document session lifecycle (creation, expiration, cleanup)
- **Acceptance Criteria:**
  - [ ] POST /auth/login sets session cookie with HttpOnly flag
  - [ ] Session data stored in django_session table
  - [ ] Session cookie expires after TTL
  - [ ] Session can be validated with GET /auth/me
  - [ ] Logout (POST /auth/logout) clears session
  - [ ] CSRF middleware configured and working
  - [ ] Cookie flags correct (HttpOnly, Secure on prod, SameSite=Strict)
- **Dependencies/Blockers:** User model (2.1), Django sessions app (1.1)
- **System Design References:** ADR-007 (database-backed sessions), SYSTEM_DESIGN.md Part 3
- **Suggested Labels:** `backend`, `authentication`, `session`
- **Milestone:** M2

#### 2.3 Email/Password Authentication Endpoints
- **Title:** `[M2-Backend] Implement signup, login, logout, password reset endpoints`
- **Goal/Context:** Complete user authentication flow via email/password.
- **Implementation Scope:**
  - POST /auth/signup: validate email/password, create user, start session
  - POST /auth/login: validate email/password, start session, return user + households
  - POST /auth/logout: clear session
  - POST /auth/forgot-password: generate reset token, send email
  - POST /auth/reset-password: validate token, update password, invalidate sessions
  - GET /auth/me: return current authenticated user
  - Implement rate limiting: 5 login attempts per IP per minute, 3 password reset per email per hour
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md specification
  - [ ] Email validation (format, unique)
  - [ ] Password validation (length, complexity per security requirements)
  - [ ] Reset token: 32-byte random, hashed before storage, 1-hour expiration
  - [ ] Rate limiting enforced (5/min login, 3/hour reset)
  - [ ] Errors return 400/401/422 as per spec
  - [ ] Integration tests: 100% of auth endpoints
- **Dependencies/Blockers:** User model (2.1), session management (2.2), email service (Infrastructure)
- **PRD References:** FR-1-6 (authentication)
- **OpenAPI References:** /auth/signup, /auth/login, /auth/logout, /auth/forgot-password, /auth/reset-password
- **ADR References:** ADR-004 (session-based auth)
- **Suggested Labels:** `backend`, `authentication`
- **Milestone:** M2

#### 2.4 Google OAuth 2.0 Integration
- **Title:** `[M2-Backend] Implement Google OAuth 2.0 authentication`
- **Goal/Context:** Enable social login via Google for convenience.
- **Implementation Scope:**
  - Install django-allauth or similar library
  - Configure Google OAuth app (create in Google Cloud Console)
  - Implement OAuth flow: redirect → Google → callback → session
  - Handle new user registration via OAuth
  - Handle existing user OAuth linkage
  - Implement logout that clears Google session
- **Acceptance Criteria:**
  - [ ] GET /auth/google redirects to Google login
  - [ ] Google callback endpoint creates/updates user
  - [ ] User redirected to Frontend with session cookie
  - [ ] Existing users can OAuth without creating duplicate
  - [ ] OAuth user can password-reset normally
  - [ ] Integration test: full OAuth flow
- **Dependencies/Blockers:** User model (2.1), session management (2.2)
- **PRD References:** FR-4 (Google OAuth)
- **System Design References:** ADR-004 (authentication options considered)
- **Suggested Labels:** `backend`, `authentication`, `oauth`
- **Milestone:** M2

#### 2.5 Email Service Integration
- **Title:** `[M2-Backend] Integrate SendGrid/SES for transactional emails`
- **Goal/Context:** Send password reset and authentication emails reliably.
- **Implementation Scope:**
  - Configure email backend (SendGrid, AWS SES, or Mailgun)
  - Create email templates: password-reset, OAuth confirmation, invitation
  - Implement send_password_reset_email(user), send_invitation_email(invitation)
  - Configure from address, reply-to, subject templates
  - Handle email failures gracefully (log, retry later)
- **Acceptance Criteria:**
  - [ ] Password reset email sends within 1 second
  - [ ] Email contains reset link with token
  - [ ] Token in link matches hashed token in DB
  - [ ] Email provider credentials in environment (not committed)
  - [ ] Email failures logged but don't crash request
  - [ ] Email templates professional and clear
  - [ ] Integration test: reset email sent, link works
- **Dependencies/Blockers:** User model (2.1), email configuration (Infrastructure 1.13)
- **System Design References:** SYSTEM_DESIGN.md Part 3 (email strategy)
- **Suggested Labels:** `backend`, `email`
- **Milestone:** M2

#### 2.6 Authentication Tests & Integration
- **Title:** `[M2-Backend] Write comprehensive authentication integration tests`
- **Goal/Context:** Ensure auth security and correctness through automated testing.
- **Implementation Scope:**
  - Test signup: valid, invalid email, duplicate email, weak password
  - Test login: valid, invalid credentials, rate limiting
  - Test logout: session cleared
  - Test password reset: valid token, invalid token, expired token
  - Test OAuth: new user, existing user
  - Test session: persistent across requests, expires, CSRF protection
  - Test authorization: 401 without session, 200 with session
- **Acceptance Criteria:**
  - [ ] 50+ authentication test cases
  - [ ] All happy paths passing
  - [ ] All error paths returning correct status codes
  - [ ] Rate limiting tested and enforced
  - [ ] Session lifecycle tested
  - [ ] OAuth flow tested end-to-end
  - [ ] Coverage: >95% of auth code
- **Dependencies/Blockers:** All auth endpoints (2.1-2.5)
- **System Design References:** Part 14 (testing strategy)
- **Suggested Labels:** `backend`, `testing`, `authentication`
- **Milestone:** M2

---

### Frontend Repository (4 issues)

#### 2.7 Authentication Context & useAuth Hook
- **Title:** `[M2-Frontend] Create authentication context and useAuth hook`
- **Goal/Context:** Centralized user state management for authenticated operations.
- **Implementation Scope:**
  - Create src/context/AuthContext.tsx with user state
  - Implement useAuth hook to access user and auth methods
  - Provide user info throughout app without prop drilling
  - Handle logout (clear user, redirect to login)
  - Persist user state across page refresh (check GET /auth/me on load)
  - Loading state while checking authentication
- **Acceptance Criteria:**
  - [ ] AuthContext provides user, loading, login, logout methods
  - [ ] useAuth hook accessible from any component
  - [ ] User persists on page refresh
  - [ ] Loading spinner while checking auth
  - [ ] User can call useAuth().logout() from any page
  - [ ] TypeScript types for user object
- **Dependencies/Blockers:** React scaffold (1.8), API client (1.9)
- **System Design References:** SYSTEM_DESIGN.md Part 10 (frontend architecture)
- **Suggested Labels:** `frontend`, `authentication`
- **Milestone:** M2

#### 2.8 Authentication Pages (Signup, Login, Password Reset)
- **Title:** `[M2-Frontend] Implement signup, login, and password reset pages`
- **Goal/Context:** User-facing authentication flows.
- **Implementation Scope:**
  - Create src/pages/SignupPage.tsx: email, password, name inputs, validation
  - Create src/pages/LoginPage.tsx: email, password inputs, validation, Google button
  - Create src/pages/PasswordResetPage.tsx: email input, sends reset email
  - Create src/pages/PasswordResetConfirmPage.tsx: token from URL, new password inputs
  - Form validation: React Hook Form + Zod
  - Error/success toasts after submission
  - Links between pages (login → signup, login → reset, etc.)
- **Acceptance Criteria:**
  - [ ] Signup page: validates email format, password strength, shows errors
  - [ ] Signup submission creates user, starts session, redirects to household selection
  - [ ] Login page: validates credentials, shows errors, redirects on success
  - [ ] Google OAuth button: redirects to Google, completes flow
  - [ ] Password reset: email input, sends reset email, shows confirmation
  - [ ] Reset confirm: validates token from URL, allows new password, redirects to login
  - [ ] All forms use React Hook Form + Zod
  - [ ] Toasts for success/error messages
  - [ ] Responsive design (mobile-friendly)
- **Dependencies/Blockers:** Auth endpoints (2.1-2.5), Auth context (2.7), API client (1.9)
- **PRD References:** FR-1-6 (authentication)
- **OpenAPI References:** All /auth/* endpoints
- **Suggested Labels:** `frontend`, `ui`, `authentication`
- **Milestone:** M2

#### 2.9 Protected Routes & Login Redirect
- **Title:** `[M2-Frontend] Implement protected route wrapper and automatic login redirect`
- **Goal/Context:** Prevent unauthorized access to protected pages.
- **Implementation Scope:**
  - Create ProtectedRoute component that checks useAuth() user
  - Redirect to login if not authenticated
  - Show loading spinner while checking auth
  - Implement route guards in React Router
  - Add404 page for unknown routes
- **Acceptance Criteria:**
  - [ ] Protected pages require authentication
  - [ ] Unauthenticated users redirected to login
  - [ ] Loading spinner shows while checking
  - [ ] Deep links work (redirect to login, then to original page after login)
  - [ ] 404 page shown for unknown routes
- **Dependencies/Blockers:** Auth context (2.7), React Router setup (1.8)
- **System Design References:** SYSTEM_DESIGN.md Part 10 (frontend architecture)
- **Suggested Labels:** `frontend`, `authentication`, `routing`
- **Milestone:** M2

---

## Milestone 3: Household Management & Membership

### Backend Repository (5 issues)

#### 3.1 Household Model & Soft-Delete Logic
- **Title:** `[M3-Backend] Implement Household model with soft-delete and scoping`
- **Goal/Context:** Foundation for household isolation (security boundary).
- **Implementation Scope:**
  - Household model: name, description, code (unique), owner_id (FK to User, PROTECT), deleted_at
  - Generate unique code (8 alphanumeric) on creation
  - Soft-delete: set deleted_at, don't cascade delete children
  - Manager method: `active_households()` filters deleted_at IS NULL
  - Ensure all queries filter by deleted_at
- **Acceptance Criteria:**
  - [ ] Household model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] Code generated as unique, 8-char alphanumeric
  - [ ] Soft-delete doesn't cascade (data preserved)
  - [ ] Queries filter deleted_at automatically (via manager)
  - [ ] ForeignKey owner_id set to PROTECT (cannot delete owner)
  - [ ] Migrations correct
- **Dependencies/Blockers:** Models stub (1.3), User model (2.1)
- **PRD References:** FR-8-14 (household management)
- **OpenAPI References:** /households/* endpoints
- **ADR References:** ADR-005 (household scoping)
- **Suggested Labels:** `backend`, `household`, `high-priority`
- **Milestone:** M3

#### 3.2 Membership Model & Role-Based Permissions
- **Title:** `[M3-Backend] Implement Membership model with role-based authorization`
- **Goal/Context:** Define user's role within household (owner vs. member).
- **Implementation Scope:**
  - Membership model: household_id, user_id, role (owner/member), joined_at
  - Unique constraint: (household_id, user_id)
  - Foreign keys: CASCADE for both (hard delete on user/household deletion)
  - Manager method: `get_membership(user_id, household_id)` returns member or None
  - Permission classes: IsHouseholdMember (any member), IsHouseholdOwner (owner only), IsCreator (creator of resource)
- **Acceptance Criteria:**
  - [ ] Membership model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] One membership per (household, user) pair
  - [ ] Role enum: owner, member
  - [ ] Permission classes work correctly
  - [ ] Queries join to verify membership before returning data
  - [ ] Migrations correct
- **Dependencies/Blockers:** Models stub (1.3), Household model (3.1)
- **System Design References:** ADR-005 (household-scoped authorization)
- **Suggested Labels:** `backend`, `authorization`, `household`
- **Milestone:** M3

#### 3.3 Household CRUD Endpoints
- **Title:** `[M3-Backend] Implement household endpoints (list, create, get, update, delete)`
- **Goal/Context:** Full household lifecycle via API.
- **Implementation Scope:**
  - GET /households: list user's households (join Membership)
  - POST /households: create household, set owner=current_user
  - GET /households/{id}: get household details
  - PATCH /households/{id}: update name/description (owner only)
  - DELETE /households/{id}: soft-delete (owner only)
  - GET /households/{id}/code: get current code
  - POST /households/{id}/code: regenerate code (owner only)
  - Serializers with household context
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md
  - [ ] Household list filters deleted_at
  - [ ] Create sets owner automatically
  - [ ] Code generation returns 8-char unique code
  - [ ] Regenerate invalidates old code (overwrites in DB)
  - [ ] Update requires owner permission
  - [ ] Delete soft-deletes (sets deleted_at)
  - [ ] All endpoints verify household membership
- **Dependencies/Blockers:** Household model (3.1), Membership model (3.2), auth endpoints (2.1-2.5)
- **PRD References:** FR-8-14
- **OpenAPI References:** /households, /households/{id}, /households/{id}/code
- **Suggested Labels:** `backend`, `household`, `api`
- **Milestone:** M3

#### 3.4 Invitation Model & Email Invitations
- **Title:** `[M3-Backend] Implement invitation model and email invitation flow`
- **Goal/Context:** Allow household owners to invite members via email.
- **Implementation Scope:**
  - Invitation model: household_id, email, token_hash, state, created_at, expires_at, accepted_at
  - Generate secure token: 32-byte random, base64 encoded
  - Hash token before storage (SHA-256)
  - States: pending, accepted, revoked, expired
  - Manager methods: `active_invitations()`, `is_token_valid(token)`
  - Email sending: password-reset style with acceptance link
  - Endpoints:
    - POST /households/{id}/members: invite by email (owner only)
    - GET /households/{id}/invitations: list invitations (owner only)
    - DELETE /households/{id}/invitations/{token}: revoke (owner only)
    - POST /households/{id}/invitations/{token}/accept: accept invitation
- **Acceptance Criteria:**
  - [ ] Invitation model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] Token hashed (never plaintext in DB)
  - [ ] Token one-time use (state transitions prevent re-use)
  - [ ] Expiration: 30 days default (configurable)
  - [ ] Owner can revoke pending invitation
  - [ ] Email contains unique link with token
  - [ ] Accepting valid token creates Membership
  - [ ] Accepting invalid/expired token returns 404
  - [ ] Tests: token generation, hashing, one-time use, expiration
- **Dependencies/Blockers:** Membership model (3.2), email service (2.5)
- **PRD References:** FR-16-22 (member invitations)
- **OpenAPI References:** /households/{id}/members (POST), /households/{id}/invitations/*
- **ADR References:** ADR-005 (membership lifecycle)
- **Suggested Labels:** `backend`, `invitation`, `email`
- **Milestone:** M3

#### 3.5 Household Code Join Endpoints
- **Title:** `[M3-Backend] Implement join by household code endpoint`
- **Goal/Context:** Allow members to join via shareable code (no email needed).
- **Implementation Scope:**
  - POST /households/{id}/join: accepts household code
  - Validates code matches household
  - Creates Membership for authenticated user (role=member)
  - Returns household details on success
  - Handles: code not found (404), user already member (409), household deleted (403)
- **Acceptance Criteria:**
  - [ ] POST /households/{id}/join with valid code creates membership
  - [ ] Returns household details on success
  - [ ] Invalid code returns 404
  - [ ] Already member returns 409
  - [ ] Soft-deleted household returns 403
  - [ ] User cannot join same household twice
  - [ ] Tests: valid code, invalid code, already member
- **Dependencies/Blockers:** Household model (3.1), Membership model (3.2)
- **PRD References:** FR-18 (join by code)
- **OpenAPI References:** /households/{id}/join
- **Suggested Labels:** `backend`, `household`, `membership`
- **Milestone:** M3

---

### Frontend Repository (4 issues)

#### 3.6 Household Selection & Switcher UI
- **Title:** `[M3-Frontend] Create household selector and switcher component`
- **Goal/Context:** Enable users to see and switch between multiple households.
- **Implementation Scope:**
  - Show household list after login (from GET /households response)
  - Create household switcher dropdown in header
  - Show current household name
  - Allow switching to different household (updates app context)
  - Store active household in state (AuthContext or separate HouseholdContext)
- **Acceptance Criteria:**
  - [ ] After login, user shown list of their households
  - [ ] Household switcher in header
  - [ ] Clicking household name shows dropdown list
  - [ ] Selecting household updates app state
  - [ ] All subsequent API calls use active household
  - [ ] Household persists across page refresh (store in localStorage or session)
- **Dependencies/Blockers:** Auth context (2.7), household endpoints (3.3)
- **System Design References:** SYSTEM_DESIGN.md Part 10 (active household context)
- **Suggested Labels:** `frontend`, `ui`, `household`
- **Milestone:** M3

#### 3.7 Create Household Page
- **Title:** `[M3-Frontend] Implement create household form and page`
- **Goal/Context:** Allow authenticated users to create new households.
- **Implementation Scope:**
  - Create src/pages/CreateHouseholdPage.tsx
  - Form inputs: name (required), description (optional)
  - Validation: name required, name length 3-100 chars
  - Submit to POST /households
  - On success: redirect to household dashboard
  - Show error toasts on failure
- **Acceptance Criteria:**
  - [ ] Form validates name required
  - [ ] Submits to POST /households
  - [ ] On success: household added to list, user redirected to it
  - [ ] On failure: error toast shown
  - [ ] Cancel button returns to previous page
- **Dependencies/Blockers:** Household endpoints (3.3), household context
- **PRD References:** FR-8-9
- **OpenAPI References:** POST /households
- **Suggested Labels:** `frontend`, `ui`, `household`
- **Milestone:** M3

#### 3.8 Member List & Invitation Management UI
- **Title:** `[M3-Frontend] Implement member list and invite member form`
- **Goal/Context:** View household members and invite new ones.
- **Implementation Scope:**
  - Create src/pages/HouseholdSettingsPage.tsx
  - Show member list: name, joined_at, role
  - Show invite form: email input
  - Owner can: remove members, invite members
  - Members can: view other members
  - Show pending invitations
  - Owner can revoke pending invitations
- **Acceptance Criteria:**
  - [ ] Member list fetched from GET /households/{id}/members
  - [ ] Shows name, joined date, role
  - [ ] Owner can remove members (DELETE /households/{id}/members/{user_id})
  - [ ] Owner can invite by email (POST /households/{id}/members)
  - [ ] Pending invitations shown
  - [ ] Owner can revoke invitation
  - [ ] Confirmation dialog before remove
  - [ ] Success toasts after actions
- **Dependencies/Blockers:** Household endpoints (3.3), invitation endpoints (3.4)
- **OpenAPI References:** GET/POST /households/{id}/members, GET/DELETE /households/{id}/invitations
- **Suggested Labels:** `frontend`, `ui`, `household`
- **Milestone:** M3

#### 3.9 Join Household by Code UI
- **Title:** `[M3-Frontend] Create join by code page`
- **Goal/Context:** Allow users to join household via shareable code.
- **Implementation Scope:**
  - Create src/pages/JoinHouseholdPage.tsx or modal
  - Input: household code
  - Submit to POST /households/{id}/join (where {id} is inferred from code?)
  - On success: household added to list, redirect to it
  - On failure: error message
- **Acceptance Criteria:**
  - [ ] Form accepts household code input
  - [ ] Submits to correct endpoint
  - [ ] On success: household added, user redirected
  - [ ] On failure: error shown
  - [ ] Code input validated (length, format)
- **Dependencies/Blockers:** Household join endpoints (3.5)
- **OpenAPI References:** POST /households/{id}/join
- **Suggested Labels:** `frontend`, `ui`, `household`
- **Milestone:** M3

---

## Milestone 4: Task Management

### Backend Repository (3 issues)

#### 4.1 Task Model with Single Assignment
- **Title:** `[M4-Backend] Implement Task model with single Membership assignment`
- **Goal/Context:** Tasks with single assignee (references Membership, not User, for household scoping).
- **Implementation Scope:**
  - Task model: household_id, title, description, due_date, created_by_id, assigned_to_id→Membership (nullable), completed, completed_by_id, completed_at
  - Manager method: `active_tasks(household_id)` filters deleted_at (not implemented yet, hard-delete only)
  - Assignment validation: assigned_to_id must be in same household as task
  - Check constraint: assigned_to household matches task household
- **Acceptance Criteria:**
  - [ ] Task model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] assigned_to_id is nullable FK to Membership (not User)
  - [ ] Check constraint ensures same household
  - [ ] completed_at auto-set when completed=True
  - [ ] Queries return created_by name and assigned_to name for display
- **Dependencies/Blockers:** Models stub (1.3), Membership model (3.2)
- **PRD References:** FR-27-36 (task management)
- **OpenAPI References:** /households/{id}/tasks*
- **ADR References:** ADR-008 (single-assignee model)
- **Suggested Labels:** `backend`, `task`, `high-priority`
- **Milestone:** M4

#### 4.2 Task CRUD Endpoints
- **Title:** `[M4-Backend] Implement task endpoints (list, create, get, update, delete, complete)`
- **Goal/Context:** Full task lifecycle via API.
- **Implementation Scope:**
  - GET /households/{id}/tasks: list tasks, filters (completed, assigned_to_id, due_date), pagination
  - POST /households/{id}/tasks: create task
  - GET /households/{id}/tasks/{task_id}: get task details
  - PATCH /households/{id}/tasks/{task_id}: update (any member, but creator/owner can reassign)
  - DELETE /households/{id}/tasks/{task_id}: hard-delete (creator/owner only)
  - PATCH /households/{id}/tasks/{task_id}/complete: mark complete (assigned member or owner only)
  - All endpoints verify household membership
  - Authorization: creator/owner for delete/reassign, assigned member for mark complete
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md
  - [ ] GET list: pagination (page, limit), filters work, sorted by date
  - [ ] POST: creates with created_by=current_user
  - [ ] PATCH: any member can edit, but creator/owner can reassign
  - [ ] DELETE: creator/owner only
  - [ ] Complete: assigned member or owner only, sets completed_at
  - [ ] If assigned member is removed from household, task becomes unassigned (assigned_to_id=NULL)
  - [ ] All return serialized task with names (created_by_name, assigned_to_name)
- **Dependencies/Blockers:** Task model (4.1), auth & membership (3.1-3.2)
- **PRD References:** FR-27-36
- **OpenAPI References:** /households/{id}/tasks, /households/{id}/tasks/{task_id}
- **Suggested Labels:** `backend`, `task`, `api`
- **Milestone:** M4

#### 4.3 Task Tests & Authorization
- **Title:** `[M4-Backend] Write task CRUD and authorization tests`
- **Goal/Context:** Ensure task operations respect authorization model.
- **Implementation Scope:**
  - Test create: valid, invalid (missing title), sets created_by
  - Test list: filters (completed, assignee, due_date), pagination
  - Test update: creator can edit, other members cannot (gets 403), owner can edit any
  - Test reassign: creator can assign, member cannot reassign others
  - Test mark complete: assigned member only, owner always
  - Test delete: creator/owner only, 403 for others
  - Test cross-household: prevent access to tasks from different household
  - Test unassignment on member removal
- **Acceptance Criteria:**
  - [ ] 50+ task test cases
  - [ ] Authorization matrix tested (creator, owner, assigned member, random member, non-member)
  - [ ] All error cases returning correct status (403 for unauthorized)
  - [ ] Cross-household isolation verified
  - [ ] Unassignment on member removal tested
  - [ ] Coverage >95% of task code
- **Dependencies/Blockers:** Task endpoints (4.2)
- **System Design References:** Part 14 (testing strategy)
- **Suggested Labels:** `backend`, `task`, `testing`
- **Milestone:** M4

---

### Frontend Repository (3 issues)

#### 4.4 Task List Page & Filtering
- **Title:** `[M4-Frontend] Create task list page with filtering and pagination`
- **Goal/Context:** Display household tasks with options to filter and search.
- **Implementation Scope:**
  - Create src/pages/TaskListPage.tsx
  - Fetch tasks from GET /households/{id}/tasks
  - Display in sections: open tasks, completed tasks
  - Filters: by assignee, by status, by due date
  - Pagination: next/prev or infinite scroll
  - Each task shows: title, assignee, due date, created by
  - Click task to view/edit details
- **Acceptance Criteria:**
  - [ ] Tasks fetched on load
  - [ ] Filters work (assignee dropdown, status toggle, date range)
  - [ ] Pagination works
  - [ ] Responsive design
  - [ ] TanStack Query: cache invalidated after mutations
- **Dependencies/Blockers:** Task endpoints (4.2), household context
- **OpenAPI References:** GET /households/{id}/tasks
- **Suggested Labels:** `frontend`, `ui`, `task`
- **Milestone:** M4

#### 4.5 Task Create & Edit Forms
- **Title:** `[M4-Frontend] Implement task creation and editing forms`
- **Goal/Context:** User interface for creating and modifying tasks.
- **Implementation Scope:**
  - Create modal/page: create task form
  - Inputs: title (required), description, due_date, assigned_to_id (dropdown)
  - Validation: title required, due_date optional
  - Submit to POST /households/{id}/tasks
  - Edit task form (same as create, but PATCH)
  - Assignment dropdown shows household members
  - Form validation with React Hook Form + Zod
- **Acceptance Criteria:**
  - [ ] Create form: title required, other fields optional
  - [ ] Assignment dropdown: shows household members
  - [ ] Submit POST /households/{id}/tasks
  - [ ] On success: task added to list, modal closes
  - [ ] Edit form: pre-fills existing values
  - [ ] PATCH /households/{id}/tasks/{task_id}
  - [ ] Validation errors shown inline
- **Dependencies/Blockers:** Task endpoints (4.2), member list (3.3)
- **OpenAPI References:** POST/PATCH /households/{id}/tasks
- **Suggested Labels:** `frontend`, `ui`, `task`, `form`
- **Milestone:** M4

#### 4.6 Task Detail & Completion UI
- **Title:** `[M4-Frontend] Create task detail view and completion toggle`
- **Goal/Context:** View task details and mark tasks complete.
- **Implementation Scope:**
  - Create src/pages/TaskDetailPage.tsx
  - Show task info: title, description, due date, assignee, created by, created at
  - Edit button (only for creator/owner)
  - Delete button (only for creator/owner)
  - Assign dropdown (only for creator/owner)
  - Complete toggle (only for assigned member or owner)
  - Show completion status: who completed, when
  - Link back to task list
- **Acceptance Criteria:**
  - [ ] Task detail loaded from GET /households/{id}/tasks/{task_id}
  - [ ] Edit button visible only for creator/owner
  - [ ] Delete button visible only for creator/owner
  - [ ] Assign dropdown visible only for creator/owner
  - [ ] Complete toggle visible for assigned member and owner
  - [ ] Clicking complete: PATCH /tasks/{id}/complete
  - [ ] Shows "Completed by X on date" if complete
  - [ ] Delete with confirmation dialog
- **Dependencies/Blockers:** Task endpoints (4.2)
- **OpenAPI References:** GET/PATCH/DELETE /households/{id}/tasks/{task_id}, PATCH /tasks/{task_id}/complete
- **Suggested Labels:** `frontend`, `ui`, `task`
- **Milestone:** M4

---

## Milestones 5-7 Issues (Condensed for Space)

Due to length, I'll provide issue summaries for Milestones 5-7. Full details follow the same pattern as M1-M4.

---

## Milestone 5: Secondary Features (Shopping, Expenses, Inventory)

### 5.1-5.3 Shopping List (Backend)
- **5.1:** ShoppingItem model (name, quantity, purchased, purchased_by_id, created_by_id)
- **5.2:** Shopping endpoints (GET, POST, PATCH, DELETE /households/{id}/shopping*)
- **5.3:** Shopping tests (CRUD, authorization)

### 5.4-5.6 Expense Tracking (Backend)
- **5.4:** Expense model (amount_cents, category enum, payer_id defaults to creator, immutable)
- **5.5:** Expense endpoints (list with category/payer filters, create, update, delete)
- **5.6:** Expense tests

### 5.7-5.9 Inventory Management (Backend)
- **5.7:** InventoryItem model (name, quantity, category, location, created_by_id)
- **5.8:** Inventory endpoints
- **5.9:** Inventory tests

### 5.10-5.12 Shopping UI (Frontend)
- **5.10:** Shopping list page with pending/purchased sections
- **5.11:** Add/edit shopping item forms
- **5.12:** Mark purchased toggle and delete UI

### 5.13-5.15 Expense UI (Frontend)
- **5.13:** Expense list page with category breakdown
- **5.14:** Create/edit expense forms (amount, category, payer, description)
- **5.15:** Expense detail and delete UI

### 5.16-5.18 Inventory UI (Frontend)
- **5.16:** Inventory list page with optional category filtering
- **5.17:** Add/edit inventory item forms
- **5.18:** Inventory detail and delete UI

---

## Milestone 6: Testing, Security, Performance

### 6.1 Backend Integration Tests
- Test full signup → create household → invite → task creation workflow
- Cross-household isolation tests (100+ cases)
- Authorization matrix verification

### 6.2 Frontend Integration Tests
- Login, household creation, member invitation, task creation workflows
- Task list filtering and pagination

### 6.3 Security Hardening
- CSRF token validation in all state-changing requests
- Rate limiting verification (login, reset, API)
- SQL injection prevention tests
- Password hashing verification

### 6.4 Performance Optimization
- Database query optimization (no N+1)
- Index verification
- Load testing (1000 concurrent users)
- Response time baseline

### 6.5 API Documentation
- OpenAPI specification rendered and published
- Deployment guide created and tested
- Development setup guide tested with new developer

---

## Milestone 7: Launch Preparation

### 7.1 Deployment Infrastructure
- Docker images built and pushed to registry
- Environment variables configured (production secrets)
- Database migrations automated

### 7.2 Monitoring & Observability
- Logging configured (structured JSON)
- Error tracking setup (Sentry or similar)
- Health check endpoint

### 7.3 Pre-Launch Verification
- Smoke tests on production
- Database backup/restore tested
- Security scan (vulnerabilities)
- Load test baseline

### 7.4 Launch
- Feature flag for MVP (if needed)
- Announcement/marketing
- Monitor first 24 hours

---

## Summary of Issues by Repository

| Repository | M1 | M2 | M3 | M4 | M5 | M6 | M7 | Total |
|------------|----|----|----|----|----|----|----|----|
| **Backend** | 7 | 6 | 5 | 3 | 9 | 3 | 0 | 33 |
| **Frontend** | 5 | 4 | 4 | 3 | 8 | 2 | 0 | 26 |
| **Infrastructure** | 3 | 0 | 0 | 0 | 0 | 1 | 1 | 5 |
| **Automation** | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 3 |
| **Documentation** | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 4 |
| **Total** | 19 | 10 | 9 | 6 | 17 | 7 | 3 | **71** |

---

## Cross-Repository Dependency Map

```
M1: Foundation
  ├─ Backend: Django scaffold, models stub, DRF setup
  ├─ Frontend: React scaffold, API client
  ├─ Infrastructure: PostgreSQL, Docker Compose, env config
  └─ Automation: CI/CD pipelines

M2: Authentication (depends on M1)
  ├─ Backend: User model, sessions, auth endpoints, OAuth
  ├─ Frontend: Auth context, signup/login/reset pages, protected routes
  └─ Infrastructure: Email service

M3: Households (depends on M2)
  ├─ Backend: Household model, Membership model, invitation system
  └─ Frontend: Household selector, create/settings pages, member mgmt

M4: Tasks (depends on M3)
  ├─ Backend: Task model, CRUD endpoints, authorization
  └─ Frontend: Task list, create/edit/detail pages

M5: Secondary Features (depends on M4)
  ├─ Backend: Shopping, Expense, Inventory models & endpoints
  └─ Frontend: UI for all three features

M6: Testing (depends on M5)
  ├─ Backend: Integration tests, security tests
  ├─ Frontend: Component and E2E tests
  └─ Documentation: API docs, deployment guide

M7: Launch (depends on M6)
  ├─ Infrastructure: Deployment setup
  ├─ Automation: Launch pipeline
  └─ All: Pre-launch verification
```

---

## Next Steps

1. Review this proposal for:
   - Issue size (are they appropriately sized?)
   - Issue titles and descriptions (are they clear?)
   - Acceptance criteria (are they objective and testable?)
   - Cross-repository dependencies (are they explicit?)
   - Milestone assignments (does the order make sense?)

2. Approve or request changes

3. Create GitHub issues in the respective repositories

4. Assign to team members and begin development

---

