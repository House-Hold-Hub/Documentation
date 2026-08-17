# HouseHoldHub MVP - GitHub Issues Proposal (Revised)

**Date:** August 16, 2026  
**Status:** Approved (68 issues across 5 repositories, 10 milestones M0-M9)  
**Structure:** 10 milestones (M0-M9) with parallelizable M3-M6

---

## Issue Numbering & Organization

- **Prefix:** `[MX-Repo]` where X is milestone number (0-9) and Repo is repository name
- **Issues listed by repository to clarify ownership** (not by feature)
- **Dependencies shown explicitly** in each issue
- **Cross-repository dependencies highlighted in section below**

---

## Milestone 0: Engineering Foundation (M0)

### Backend Repository (5 issues)

#### M0-B1: Django Project Scaffold
- **Title:** `[M0-Backend] Initialize Django 6.x project structure`
- **Goal:** Set up Django with proper apps, settings, middleware configuration
- **Scope:**
  - Django project: `householdhub`
  - Apps: `api`, `users`, `households`, `tasks`, `shopping`, `expenses`, `inventory`
  - Settings: database (PostgreSQL), installed apps, middleware, DRF, CORS
  - requirements.txt: Django 6.x, DRF, psycopg2, python-decouple, django-extensions
  - .env.example with documented variables
- **Acceptance Criteria:**
  - [ ] `python manage.py runserver` starts on localhost:8000
  - [ ] `python manage.py migrate` runs without errors
  - [ ] All apps registered in INSTALLED_APPS
  - [ ] DRF configured with JSON renderer and session authentication
  - [ ] CORS configured for localhost:3000
  - [ ] DATABASE_URL environment variable used for connections
- **Dependencies:** None (foundation)
- **Labels:** `backend`, `setup`, `high-priority`
- **Milestone:** M0

#### M0-B2: Database Models Skeleton
- **Title:** `[M0-Backend] Create Django ORM models for all 8 entities (stub)`
- **Goal:** Define all models matching ERD before feature development
- **Scope:**
  - User (email, password_hash, name, google_id, deleted_at, timestamps)
  - Household (name, description, code, owner_id, deleted_at, timestamps)
  - Membership (household_id, user_id, role, joined_at, timestamps)
  - Invitation (household_id, email, token_hash, state, expires_at, timestamps)
  - Task (household_id, title, description, due_date, created_by_id, assigned_to_id→Membership, completed, completed_at, timestamps)
  - ShoppingItem (household_id, name, quantity, purchased, purchased_by_id, purchased_at, created_by_id, timestamps)
  - Expense (household_id, amount_cents, category, payer_id, description, created_by_id, timestamps)
  - InventoryItem (household_id, name, quantity, category, location, created_by_id, timestamps)
  - All FKs, constraints, indexes matching ERD.md
  - Soft-delete via deleted_at for appropriate entities
- **Acceptance Criteria:**
  - [ ] All 8 models created
  - [ ] FK behavior matches ERD (CASCADE vs. SET NULL)
  - [ ] Unique constraints: Membership (household_id, user_id), Invitation (household_id, email, token_hash)
  - [ ] Check constraints for enums and validation
  - [ ] Soft-delete via deleted_at (no physical deletion in models)
  - [ ] `python manage.py makemigrations` generates migration
  - [ ] `python manage.py migrate` succeeds
- **Dependencies:** M0-B1 (Django scaffold)
- **References:** ERD.md, DOMAIN_MODEL_CORRECTED.md
- **Labels:** `backend`, `database`, `models`
- **Milestone:** M0

#### M0-B3: Django REST Framework Setup
- **Title:** `[M0-Backend] Configure DRF, base serializers, permission classes`
- **Goal:** Set up DRF foundation for all endpoints
- **Scope:**
  - Serializers scaffold (stubs for all 8 models)
  - Base serializer class with household scoping
  - DRF settings: pagination (20 default, max 100), filters, sorting
  - Permission classes: IsAuthenticated, IsHouseholdMember, IsOwner, IsCreator, IsHouseholdOwner
  - OpenAPI/Swagger schema generation configured
  - URL routing structure (api/v1/ prefix)
- **Acceptance Criteria:**
  - [ ] All 8 model serializers created (stubs)
  - [ ] Pagination configured (page, limit, total)
  - [ ] Filtering and sorting backends configured
  - [ ] Permission classes documented and tested
  - [ ] Swagger documentation accessible at /api/schema/
  - [ ] OpenAPI YAML can be downloaded from /api/schema/openapi.yaml
- **Dependencies:** M0-B1, M0-B2
- **References:** SYSTEM_DESIGN.md Part 5, OPENAPI.md
- **Labels:** `backend`, `api`, `drf`
- **Milestone:** M0

#### M0-B4: Docker Compose for Local Development
- **Title:** `[M0-Backend] Configure Docker Compose with Django, React, PostgreSQL`
- **Goal:** Enable full-stack development with `docker-compose up`
- **Scope:**
  - docker-compose.yml with services: postgres, django, react
  - Dockerfile for Django (Alpine, Python 3.14)
  - Dockerfile for React (Node + Vite)
  - .dockerignore files
  - Volume mounts for code (hot reload)
  - Network configuration for service communication
- **Acceptance Criteria:**
  - [ ] `docker-compose up` brings all services online
  - [ ] Django accessible at localhost:8000
  - [ ] React accessible at localhost:3000
  - [ ] PostgreSQL accessible at localhost:5432
  - [ ] Django connects to PostgreSQL successfully
  - [ ] Hot reload works for Python and React code
  - [ ] Services have proper health checks
- **Dependencies:** M0-B1, M0-B2, M0-F1 (React scaffold)
- **Labels:** `backend`, `infrastructure`, `docker`
- **Milestone:** M0

#### M0-B5: GitHub Actions CI/CD - Backend
- **Title:** `[M0-Automation] Set up GitHub Actions for Backend testing and linting`
- **Goal:** Automate testing, linting, type-checking on every PR
- **Scope:**
  - .github/workflows/backend-test.yml
  - Steps: checkout, setup Python 3.14, install deps, lint (flake8), type-check (mypy), pytest, coverage
  - Required status check (merge blocked if tests fail)
  - Coverage report to PR
- **Acceptance Criteria:**
  - [ ] Workflow runs on PR and reports results
  - [ ] Linting errors fail workflow
  - [ ] Test failures fail workflow
  - [ ] Coverage report visible on PR
  - [ ] Status check required for merge
  - [ ] Workflow can be manually triggered
- **Dependencies:** M0-B1
- **Labels:** `automation`, `ci-cd`, `backend`
- **Milestone:** M0

### Frontend Repository (4 issues)

#### M0-F1: React 19 + TypeScript + Vite Project Setup
- **Title:** `[M0-Frontend] Initialize React 19 + TypeScript + Vite project`
- **Goal:** Set up Frontend with TypeScript, build tool, and folder structure
- **Scope:**
  - Vite + React 19 with TypeScript
  - Dependencies: react-router, TanStack Query, react-hook-form, zod, axios
  - Project structure: src/pages, src/components, src/hooks, src/api, src/context, src/types, src/utils
  - .env.example with REACT_APP_API_URL
  - tsconfig.json with path aliases (@/components, etc.)
  - package.json scripts: dev, build, test, lint
- **Acceptance Criteria:**
  - [ ] `npm run dev` starts on localhost:3000
  - [ ] TypeScript compiles without errors
  - [ ] React Router configured
  - [ ] Axios client configured with env base URL
  - [ ] TanStack Query (React Query) configured
  - [ ] Build produces optimized bundle
  - [ ] Path aliases working (@/components, etc.)
- **Dependencies:** None (foundation)
- **Labels:** `frontend`, `setup`, `react`
- **Milestone:** M0

#### M0-F2: Axios API Client & HTTP Interceptors
- **Title:** `[M0-Frontend] Create API client with Axios and error handling`
- **Goal:** Centralized HTTP communication with consistent error handling
- **Scope:**
  - src/api/client.ts: Axios instance with base URL from env
  - Request interceptor: add CSRF token, logging
  - Response interceptor: handle 401/403/5xx, map to user-friendly messages
  - Error handling utilities
  - Retry logic for transient failures (5xx, max 3 retries, exponential backoff)
  - Types for API requests/responses (from OpenAPI, M0-F4)
- **Acceptance Criteria:**
  - [ ] API base URL from REACT_APP_API_URL environment
  - [ ] CSRF tokens included in requests
  - [ ] 401 triggers logout redirect
  - [ ] 403 shows permission error toast
  - [ ] 5xx errors show retry toast
  - [ ] Errors logged with context (URL, params, response)
  - [ ] Retry logic works (max 3, exponential backoff)
- **Dependencies:** M0-F1
- **Labels:** `frontend`, `api`
- **Milestone:** M0

#### M0-F3: TypeScript Types & API Client Generated from OpenAPI
- **Title:** `[M0-Frontend] Generate TypeScript types and API client from OpenAPI spec`
- **Goal:** Create type-safe API client from OpenAPI specification
- **Scope:**
  - Install openapi-typescript or openapi-generator
  - Generate src/types/api.ts from OPENAPI.md
  - Generate src/api/endpoints.ts with typed API methods
  - Configure generator to output types matching our conventions
  - Document how to regenerate after OpenAPI changes
- **Acceptance Criteria:**
  - [ ] Types generated from OpenAPI spec
  - [ ] API methods typed with request/response types
  - [ ] Types match OpenAPI spec exactly
  - [ ] Can regenerate when spec changes
  - [ ] TypeScript compiler validates all API calls against types
  - [ ] No `any` types for API-related code
- **Dependencies:** M0-F1, OpenAPI spec (from Documentation)
- **References:** OPENAPI.md
- **Labels:** `frontend`, `api`, `types`
- **Milestone:** M0

#### M0-F4: GitHub Actions CI/CD - Frontend
- **Title:** `[M0-Automation] Set up GitHub Actions for Frontend testing and build`
- **Goal:** Automate linting, type-checking, testing on every PR
- **Scope:**
  - .github/workflows/frontend-test.yml
  - Steps: checkout, setup Node, install deps, lint (eslint), type-check (tsc), test (vitest), build
  - Required status check
- **Acceptance Criteria:**
  - [ ] Workflow runs on PR
  - [ ] Linting errors fail
  - [ ] Type checking errors fail
  - [ ] Build failures fail
  - [ ] Status check required for merge
- **Dependencies:** M0-F1
- **Labels:** `automation`, `ci-cd`, `frontend`
- **Milestone:** M0

### Infrastructure Repository (2 issues)

#### M0-I1: PostgreSQL Configuration for Development
- **Title:** `[M0-Infrastructure] Set up PostgreSQL 14+ for local development`
- **Goal:** Database infrastructure for development and testing
- **Scope:**
  - Dockerfile for PostgreSQL (Alpine-based, PostgreSQL 14+)
  - Connection settings (host, port, credentials)
  - docker-compose.yml entry for postgres service
  - Database initialization script
  - .env.example with DATABASE_URL
  - Documentation: connection string format, reset DB commands, seed data
- **Acceptance Criteria:**
  - [ ] PostgreSQL runs in Docker
  - [ ] Connection string in DATABASE_URL format
  - [ ] Database accessible from Django container
  - [ ] Schema created with `python manage.py migrate`
  - [ ] Data persists across container restart
- **Dependencies:** M0-B4 (Docker Compose)
- **References:** ERD.md, SYSTEM_DESIGN.md Part 7
- **Labels:** `infrastructure`, `database`, `docker`
- **Milestone:** M0

#### M0-I2: Environment Configuration Templates
- **Title:** `[M0-Infrastructure] Create .env.example templates for all environments`
- **Goal:** Clear template for environment variables without leaking secrets
- **Scope:**
  - .env.example (required variables with descriptions)
  - .env.development, .env.staging, .env.production templates
  - Document each variable: purpose, example, required/optional
  - Variables: DATABASE_URL, SECRET_KEY, DEBUG, ALLOWED_HOSTS, GOOGLE_OAUTH_*, EMAIL_*
- **Acceptance Criteria:**
  - [ ] .env.example covers all required variables
  - [ ] Each documented with purpose and example
  - [ ] README warns against committing .env
  - [ ] Team can copy .env.example and run system
- **Dependencies:** None
- **Labels:** `infrastructure`, `configuration`
- **Milestone:** M0

### Automation Repository (3 issues)

#### M0-A1: Docker Image Build & Push Pipeline
- **Title:** `[M0-Automation] Set up Docker image building and registry push`
- **Goal:** Automate Docker image builds on push to main
- **Scope:**
  - GitHub Actions workflow for Docker build
  - Build and push to Docker Hub or GitHub Container Registry (GHCR)
  - Tag images: commit SHA + `latest`
  - Store registry credentials in GitHub Secrets
- **Acceptance Criteria:**
  - [ ] GitHub Actions builds images on push to main
  - [ ] Images pushed to registry with correct tags
  - [ ] Registry credentials securely stored
  - [ ] Images can be pulled and run locally
- **Dependencies:** M0-B1, M0-B4
- **Labels:** `automation`, `ci-cd`, `docker`
- **Milestone:** M0

#### M0-A2: Automated Testing Gate Configuration
- **Title:** `[M0-Automation] Configure branch protection and automated gates`
- **Goal:** Enforce code quality requirements before merge
- **Scope:**
  - Branch protection rules for main: require CI/CD passing
  - Require status checks from Backend and Frontend workflows
  - Require PR review (optional, configurable)
  - Auto-dismiss stale reviews on new push
- **Acceptance Criteria:**
  - [ ] PRs cannot be merged without passing tests
  - [ ] All required status checks visible
  - [ ] Configuration documented
- **Dependencies:** M0-B5, M0-F4
- **Labels:** `automation`, `ci-cd`
- **Milestone:** M0

#### M0-A3: Local Development Setup Script
- **Title:** `[M0-Automation] Create setup.sh for quick environment initialization`
- **Goal:** New developers can set up all repos with one command
- **Scope:**
  - setup.sh (or setup-dev.sh): clones repos, creates .env, runs docker-compose
  - Installation of pre-commit hooks (optional, for local linting)
  - Verification script that tests connectivity to all services
- **Acceptance Criteria:**
  - [ ] Script clones necessary repos
  - [ ] Creates .env from .env.example
  - [ ] Brings up docker-compose
  - [ ] Verifies all services are accessible
  - [ ] Script handles common errors
- **Dependencies:** M0-I1, M0-I2, M0-B4
- **Labels:** `automation`, `setup`
- **Milestone:** M0

### Documentation Repository (2 issues)

#### M0-D1: Documentation Repository Structure & OpenAPI Publication
- **Title:** `[M0-Documentation] Set up Documentation repo with OpenAPI spec and guides`
- **Goal:** Centralized, organized documentation for all teams
- **Scope:**
  - docs/ directory structure: architecture/, api/, guides/
  - OpenAPI YAML specification (copy from project root, render with Swagger UI or ReDoc)
  - Developer setup guide (from M0-A3 setup.sh output)
  - Architecture documentation index (links to ADRs, System Design, ERD)
  - README explaining structure
- **Acceptance Criteria:**
  - [ ] Documentation repo created and organized
  - [ ] OpenAPI spec rendered and accessible
  - [ ] Setup guide tested with fresh developer
  - [ ] Architecture documentation linked
  - [ ] README explains how to navigate
- **References:** OPENAPI.md, System Design, ADRs, ERD.md
- **Labels:** `documentation`
- **Milestone:** M0

#### M0-D2: Contribution Guide & Code Standards
- **Title:** `[M0-Documentation] Create contribution guide and code standards`
- **Goal:** Clear expectations for pull requests and code quality
- **Scope:**
  - CONTRIBUTING.md: PR process, branch naming, commit message conventions
  - CODE_STANDARDS.md: naming conventions, folder structure, testing expectations
  - Backend: Django conventions, DRF patterns
  - Frontend: React conventions, component patterns
  - Links to style guides (Black for Python, Prettier for JS)
- **Acceptance Criteria:**
  - [ ] Contribution guide clear and complete
  - [ ] Code standards documented for both Backend and Frontend
  - [ ] Examples provided
- **Labels:** `documentation`
- **Milestone:** M0

---

## Milestone 1: Identity & Authentication (M1)

### Backend Repository (5 issues)

#### M1-B1: User Model & Django Auth Backend
- **Title:** `[M1-Backend] Implement User model with email-based authentication`
- **Goal:** Core user account functionality with custom auth backend
- **Scope:**
  - Custom User model extending AbstractUser (email as USERNAME_FIELD)
  - Fields: email (unique), password_hash, name, google_id (nullable), deleted_at, timestamps
  - Django auth backend using email instead of username
  - Password hashing (Django default PBKDF2, or override with bcrypt/Argon2)
  - Soft-delete queries (filter deleted_at IS NULL)
  - Django admin integration
- **Acceptance Criteria:**
  - [ ] Custom User model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] `python manage.py createsuperuser` works with email
  - [ ] Password stored as hash (not plaintext)
  - [ ] Queries filter deleted_at automatically
  - [ ] Soft-delete sets deleted_at, doesn't remove from DB
  - [ ] Migrations correct
  - [ ] Django admin works
- **Dependencies:** M0-B1, M0-B2, M0-B3
- **PRD References:** FR-1-7 (authentication)
- **OpenAPI References:** /auth/signup, /auth/login
- **Labels:** `backend`, `authentication`, `high-priority`
- **Milestone:** M1

#### M1-B2: Session Management & Django Sessions Table
- **Title:** `[M1-Backend] Configure database-backed session authentication`
- **Goal:** Stateful session management with HTTP-only cookies
- **Scope:**
  - Session backend: django.contrib.sessions.backends.db
  - Session middleware configuration
  - Session cookie settings: HttpOnly=True, Secure=True (prod), SameSite=Strict
  - Session TTL: 14 days (configurable via SESSION_COOKIE_AGE)
  - CSRF middleware configuration
  - Management command: `python manage.py clearsessions`
  - Documentation of session lifecycle
- **Acceptance Criteria:**
  - [ ] POST /auth/login sets session cookie with HttpOnly, Secure, SameSite flags
  - [ ] Session data stored in django_session table
  - [ ] Session expires after TTL
  - [ ] POST /auth/logout clears session
  - [ ] GET /auth/me validates session
  - [ ] CSRF middleware working
  - [ ] Cookie flags correct (HttpOnly, Secure on prod, SameSite=Strict)
- **Dependencies:** M1-B1, M0-B1
- **References:** ADR-007 (database sessions), SYSTEM_DESIGN.md Part 3
- **Labels:** `backend`, `authentication`, `session`
- **Milestone:** M1

#### M1-B3: Email/Password Authentication Endpoints
- **Title:** `[M1-Backend] Implement auth endpoints (signup, login, logout, password reset)`
- **Goal:** Complete email/password authentication flow
- **Scope:**
  - POST /auth/signup: validate email/password, create user, start session
  - POST /auth/login: validate email/password, start session
  - POST /auth/logout: clear session
  - POST /auth/forgot-password: generate reset token, send email
  - POST /auth/reset-password: validate token, update password, invalidate sessions
  - GET /auth/me: return current user or 401
  - Rate limiting: 5 login/min per IP, 3 reset/hour per email
  - Password validation: min length 8, complexity (letter + number + special char)
  - Reset token: 32-byte random, hashed (SHA-256) before storage, 1-hour expiration
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md exactly
  - [ ] Email validation (format, uniqueness)
  - [ ] Password validation (length, complexity)
  - [ ] Reset token hashed and one-time use
  - [ ] Rate limiting enforced
  - [ ] Errors return correct status codes (400/401/422)
  - [ ] Integration tests: all endpoints tested
- **Dependencies:** M1-B1, M1-B2, M1-B5 (email service)
- **PRD References:** FR-1-6 (auth)
- **OpenAPI References:** /auth/*, /users/me
- **Labels:** `backend`, `authentication`, `email`
- **Milestone:** M1

#### M1-B4: Google OAuth 2.0 Integration
- **Title:** `[M1-Backend] Implement Google OAuth 2.0 authentication`
- **Goal:** Enable social login via Google
- **Scope:**
  - django-allauth or similar library
  - Google OAuth app configuration (Google Cloud Console)
  - OAuth flow: redirect → Google → callback → session
  - New user registration via OAuth
  - Linking existing users to Google account (optional for MVP)
  - Logout clears Google session
- **Acceptance Criteria:**
  - [ ] GET /auth/google redirects to Google login
  - [ ] Google callback creates/updates user and session
  - [ ] User redirected to Frontend with session cookie
  - [ ] Existing users don't get duplicate accounts
  - [ ] OAuth users can reset password normally
  - [ ] Integration test: full OAuth flow
- **Dependencies:** M1-B1, M1-B2
- **PRD References:** FR-4 (OAuth)
- **Labels:** `backend`, `authentication`, `oauth`
- **Milestone:** M1

#### M1-B5: Email Service Integration
- **Title:** `[M1-Backend] Integrate SendGrid/SES for transactional emails`
- **Goal:** Send password reset and auth emails reliably
- **Scope:**
  - Email backend configuration (SendGrid, AWS SES, Mailgun)
  - Email templates: password-reset, OAuth confirmation, invitation, member removal
  - Functions: send_password_reset_email(), send_invitation_email()
  - Error handling: log failures, don't crash request
  - Configuration: from address, reply-to, subject templates
  - Credentials in environment (never committed)
- **Acceptance Criteria:**
  - [ ] Password reset email sent within 1 second
  - [ ] Email contains reset link with token
  - [ ] Token in link matches hashed token in DB
  - [ ] Provider credentials in .env (not committed)
  - [ ] Email failures logged but don't crash
  - [ ] Email templates professional and clear
  - [ ] Integration test: reset email sent, link works
- **Dependencies:** M1-B3, M0-I2 (env config)
- **References:** SYSTEM_DESIGN.md Part 3 (email)
- **Labels:** `backend`, `email`
- **Milestone:** M1

### Frontend Repository (4 issues)

#### M1-F1: AuthContext & useAuth Hook
- **Title:** `[M1-Frontend] Create authentication context and useAuth hook`
- **Goal:** Centralized user state management for authenticated operations
- **Scope:**
  - src/context/AuthContext.tsx with user state
  - useAuth hook for accessing user and auth methods
  - Logout method (clear user, redirect to login)
  - Persist user across page refresh (GET /auth/me on load)
  - Loading state while checking auth
  - TypeScript types for user object
- **Acceptance Criteria:**
  - [ ] AuthContext provides user, loading, login, logout
  - [ ] useAuth hook accessible from any component
  - [ ] User persists on page refresh
  - [ ] Loading spinner while checking auth
  - [ ] user object fully typed
- **Dependencies:** M0-F1, M0-F2, M1-B3
- **Labels:** `frontend`, `authentication`, `context`
- **Milestone:** M1

#### M1-F2: Authentication Pages (Signup, Login, Password Reset)
- **Title:** `[M1-Frontend] Implement signup, login, and password reset pages`
- **Goal:** User-facing authentication flows
- **Scope:**
  - src/pages/SignupPage.tsx: email, password, name inputs; validation; submit to POST /auth/signup
  - src/pages/LoginPage.tsx: email, password inputs; Google OAuth button; submit to POST /auth/login
  - src/pages/PasswordResetPage.tsx: email input; submit to POST /auth/forgot-password; success message
  - src/pages/PasswordResetConfirmPage.tsx: token from URL; new password input; submit to POST /auth/reset-password
  - Validation: React Hook Form + Zod
  - Error/success toasts after submission
  - Links between pages
- **Acceptance Criteria:**
  - [ ] Signup validates email format, password strength; shows errors
  - [ ] Signup submits to API; creates user; redirects to household selector
  - [ ] Login validates credentials; shows errors; redirects to household list on success
  - [ ] Google OAuth button redirects to Google, completes flow
  - [ ] Password reset: email input, sends email, shows confirmation
  - [ ] Reset confirm: validates token from URL, allows password change, redirects to login
  - [ ] All forms use React Hook Form + Zod
  - [ ] Toasts for success/error
  - [ ] Responsive design
- **Dependencies:** M1-F1, M0-F2, M0-F3, M1-B3, M1-B4
- **PRD References:** FR-1-6
- **OpenAPI References:** /auth/*
- **Labels:** `frontend`, `ui`, `authentication`
- **Milestone:** M1

#### M1-F3: Protected Routes & Login Redirect
- **Title:** `[M1-Frontend] Implement ProtectedRoute and automatic login redirect`
- **Goal:** Prevent unauthorized access to protected pages
- **Scope:**
  - ProtectedRoute component (checks useAuth().user)
  - Redirect to login if not authenticated
  - Loading spinner while checking auth
  - Route guards in React Router
  - 404 page for unknown routes
- **Acceptance Criteria:**
  - [ ] Protected pages require authentication
  - [ ] Unauthenticated users redirected to login
  - [ ] Loading spinner while checking
  - [ ] Deep links work (redirect to login, then to original page)
  - [ ] 404 page shown for unknown routes
- **Dependencies:** M1-F1
- **Labels:** `frontend`, `authentication`, `routing`
- **Milestone:** M1

#### M1-F4: Authentication Tests & Documentation
- **Title:** `[M1-Frontend] Write auth integration tests and documentation`
- **Goal:** Ensure auth flows work end-to-end
- **Scope:**
  - Integration tests: signup flow, login flow, logout, password reset
  - Tests cover happy path and error cases
  - Test token parsing from email links
  - Tests for session persistence
- **Acceptance Criteria:**
  - [ ] 20+ auth test cases (happy path + errors)
  - [ ] All happy paths passing
  - [ ] Error handling correct
  - [ ] Email link parsing tested
  - [ ] Session persistence verified
- **Dependencies:** M1-F2
- **Labels:** `frontend`, `testing`, `authentication`
- **Milestone:** M1

---

## Milestone 2: Household & Membership (M2)

### Backend Repository (6 issues)

#### M2-B1: Household Model with Soft-Delete & Code Generation
- **Title:** `[M2-Backend] Implement Household model with soft-delete and code generation`
- **Goal:** Foundation for household isolation and security boundary
- **Scope:**
  - Household model: name, description, code (unique 8-char), owner_id (FK PROTECT), deleted_at, timestamps
  - Code generation: 8-char alphanumeric, unique on creation
  - Soft-delete: sets deleted_at, doesn't cascade (data preserved)
  - Manager method: `active_households()` filters deleted_at IS NULL
  - All queries use manager to filter deleted
- **Acceptance Criteria:**
  - [ ] Model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] Code generated (unique 8-char alphanumeric)
  - [ ] Soft-delete doesn't cascade
  - [ ] Queries filter deleted_at automatically
  - [ ] Owner PROTECT FK prevents deletion
  - [ ] Migrations correct
- **Dependencies:** M1-B1, M0-B2
- **PRD References:** FR-8-14
- **OpenAPI References:** /households/*
- **Labels:** `backend`, `household`, `high-priority`
- **Milestone:** M2

#### M2-B2: Membership Model & Role-Based Permissions
- **Title:** `[M2-Backend] Implement Membership model with role-based authorization`
- **Goal:** Define user roles within household (owner vs. member)
- **Scope:**
  - Membership model: household_id, user_id, role (owner|member), joined_at, timestamps
  - Unique constraint: (household_id, user_id)
  - ForeignKeys: CASCADE for both (hard delete on user/household deletion)
  - Manager method: `get_membership(user_id, household_id)`
  - Permission classes: IsHouseholdMember, IsHouseholdOwner, IsCreator
- **Acceptance Criteria:**
  - [ ] Model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] One membership per (household, user) pair
  - [ ] Role enum: owner, member
  - [ ] Permission classes work correctly
  - [ ] Queries verify membership before returning data
  - [ ] Migrations correct
- **Dependencies:** M2-B1, M0-B2
- **References:** ADR-005 (household scoping)
- **Labels:** `backend`, `authorization`, `household`
- **Milestone:** M2

#### M2-B3: Household CRUD Endpoints
- **Title:** `[M2-Backend] Implement household endpoints (CRUD, code, member list)`
- **Goal:** Full household lifecycle via API
- **Scope:**
  - GET /households (list user's households)
  - POST /households (create, set owner=current_user)
  - GET /households/{id} (get details)
  - PATCH /households/{id} (update name/description, owner only)
  - DELETE /households/{id} (soft-delete, owner only)
  - GET /households/{id}/code (get current code)
  - POST /households/{id}/code (regenerate, owner only, invalidates old code)
  - GET /households/{id}/members (list members with roles)
  - Authorization: verify household membership, owner-only actions
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md
  - [ ] List filters deleted_at
  - [ ] Create sets owner automatically
  - [ ] Code generation returns unique 8-char code
  - [ ] Regenerate overwrites code in DB (old code invalid)
  - [ ] Update requires owner permission (403 otherwise)
  - [ ] Delete soft-deletes (sets deleted_at)
  - [ ] All endpoints verify household membership
- **Dependencies:** M2-B1, M2-B2, M1-B3
- **PRD References:** FR-8-14
- **OpenAPI References:** /households, /households/{id}
- **Labels:** `backend`, `household`, `api`
- **Milestone:** M2

#### M2-B4: Invitation Model & Email Invitations
- **Title:** `[M2-Backend] Implement invitation model and email invitation endpoints`
- **Goal:** Allow household owners to invite members via email
- **Scope:**
  - Invitation model: household_id, email, token_hash, state (pending|accepted|revoked|expired), created_at, expires_at, accepted_at
  - Token generation: 32-byte random, base64 encoded
  - Token hashing: SHA-256 before storage
  - Expiration: 30 days default
  - States: pending, accepted, revoked, expired
  - Endpoints:
    - POST /households/{id}/members (invite by email, owner only)
    - GET /households/{id}/invitations (list invitations, owner only)
    - DELETE /households/{id}/invitations/{token} (revoke, owner only)
    - POST /households/{id}/invitations/{token}/accept (accept invitation)
  - Email sending: send invitation with acceptance link
- **Acceptance Criteria:**
  - [ ] Model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] Token hashed (never plaintext in DB)
  - [ ] Token one-time use (state transitions prevent re-use)
  - [ ] Expiration: 30 days default
  - [ ] Owner can revoke pending invitation
  - [ ] Email contains unique link with token
  - [ ] Accepting valid token creates Membership
  - [ ] Accepting invalid/expired token returns 404
  - [ ] Tests: token generation, hashing, one-time use, expiration
- **Dependencies:** M2-B2, M1-B5
- **PRD References:** FR-16-22
- **OpenAPI References:** /households/{id}/members, /households/{id}/invitations/*
- **Labels:** `backend`, `invitation`, `email`
- **Milestone:** M2

#### M2-B5: Household Code Join Endpoint
- **Title:** `[M2-Backend] Implement join by household code endpoint`
- **Goal:** Allow members to join via shareable code
- **Scope:**
  - POST /households/{id}/join (accepts household code as request param)
  - Validates code matches household
  - Creates Membership (role=member) for authenticated user
  - Returns household details on success
  - Handles: code not found (404), already member (409), household deleted (403)
- **Acceptance Criteria:**
  - [ ] POST /households/{id}/join with valid code creates membership
  - [ ] Returns household details
  - [ ] Invalid code returns 404
  - [ ] Already member returns 409
  - [ ] Soft-deleted household returns 403
  - [ ] User cannot join same household twice
  - [ ] Tests: valid code, invalid code, already member
- **Dependencies:** M2-B1, M2-B2
- **PRD References:** FR-18
- **OpenAPI References:** /households/{id}/join
- **Labels:** `backend`, `household`
- **Milestone:** M2

#### M2-B6: Household Authorization & Cross-Household Isolation Tests
- **Title:** `[M2-Backend] Write household authorization and isolation tests (100+ cases)`
- **Goal:** Ensure cross-household isolation prevents unauthorized access
- **Scope:**
  - Authorization matrix: owner vs. member permissions for all household operations
  - Cross-household isolation: user A in household X cannot access household Y data
  - Member removal: user loses access, tasks unassigned
  - Soft-delete: household deleted, members cannot access
  - Code validation: invalid codes, regeneration invalidates old code
  - Invitation flow: send, accept, revoke, expire
- **Acceptance Criteria:**
  - [ ] 100+ test cases for authorization and isolation
  - [ ] Owner: can edit, delete, manage members
  - [ ] Member: can view, cannot edit/delete
  - [ ] Non-member: cannot access (403)
  - [ ] Cross-household: user A cannot see household B data
  - [ ] Member removal: user loses access immediately
  - [ ] Soft-delete: data preserved but inaccessible
  - [ ] Code: regeneration invalidates old code
  - [ ] Invitation: state transitions working
  - [ ] Coverage: >95% of household code
- **Dependencies:** M2-B1 through M2-B5
- **Labels:** `backend`, `testing`, `authorization`
- **Milestone:** M2

### Frontend Repository (5 issues)

#### M2-F1: Household Selector & Switcher UI
- **Title:** `[M2-Frontend] Create household selector and switcher component`
- **Goal:** Enable users to see and switch between multiple households
- **Scope:**
  - Show household list after login
  - Household switcher dropdown in header (shows current household, list on click)
  - Clicking household updates app context
  - Store active household (localStorage or session)
  - All subsequent API calls use active household
- **Acceptance Criteria:**
  - [ ] After login, household list shown
  - [ ] Switcher in header
  - [ ] Clicking shows dropdown with household list
  - [ ] Selecting household updates app state
  - [ ] All API calls use active household
  - [ ] Household persists on page refresh
- **Dependencies:** M1-F1, M2-B3
- **Labels:** `frontend`, `ui`, `household`
- **Milestone:** M2

#### M2-F2: Create Household Page
- **Title:** `[M2-Frontend] Implement create household form and page`
- **Goal:** Allow authenticated users to create new households
- **Scope:**
  - src/pages/CreateHouseholdPage.tsx
  - Form: name (required), description (optional)
  - Validation: name required, length 3-100 chars
  - Submit to POST /households
  - On success: household added to list, user redirected to household selector
  - Error toasts on failure
- **Acceptance Criteria:**
  - [ ] Form validates name required
  - [ ] Submits to POST /households
  - [ ] On success: household added, redirected
  - [ ] On failure: error toast shown
  - [ ] Cancel button returns to previous page
- **Dependencies:** M2-B3
- **PRD References:** FR-8-9
- **OpenAPI References:** POST /households
- **Labels:** `frontend`, `ui`, `household`
- **Milestone:** M2

#### M2-F3: Member List & Invitation Management UI
- **Title:** `[M2-Frontend] Implement member list and invite member form`
- **Goal:** View household members and invite new ones
- **Scope:**
  - src/pages/HouseholdSettingsPage.tsx
  - Member list: name, joined_at, role (owner/member)
  - Owner can: remove members, invite members
  - Members can: view other members
  - Pending invitations list
  - Owner can revoke pending invitations
  - Form: email input for new invitations
- **Acceptance Criteria:**
  - [ ] Member list fetched from API
  - [ ] Shows name, joined date, role
  - [ ] Owner can remove (DELETE /households/{id}/members/{user_id})
  - [ ] Owner can invite (POST /households/{id}/members)
  - [ ] Pending invitations shown
  - [ ] Owner can revoke invitation
  - [ ] Confirmation dialog before remove
  - [ ] Success toasts
- **Dependencies:** M2-B3, M2-B4, M2-B5
- **OpenAPI References:** GET/POST /households/{id}/members, GET/DELETE /households/{id}/invitations
- **Labels:** `frontend`, `ui`, `household`
- **Milestone:** M2

#### M2-F4: Join Household by Code UI
- **Title:** `[M2-Frontend] Create join by code page`
- **Goal:** Allow users to join household via shareable code
- **Scope:**
  - src/pages/JoinHouseholdPage.tsx or modal
  - Form: household code input
  - Submit to POST /households/{id}/join (API finds household from code)
  - On success: household added to list, redirect to household selector
  - On failure: error message shown
- **Acceptance Criteria:**
  - [ ] Form accepts household code input
  - [ ] Submits to correct endpoint
  - [ ] On success: household added, redirected
  - [ ] On failure: error shown
  - [ ] Code input validated
- **Dependencies:** M2-B5
- **OpenAPI References:** POST /households/{id}/join
- **Labels:** `frontend`, `ui`, `household`
- **Milestone:** M2

#### M2-F5: Household & Membership UI Tests
- **Title:** `[M2-Frontend] Write household UI integration tests`
- **Goal:** Ensure household flows work end-to-end
- **Scope:**
  - Test create household flow
  - Test household switcher
  - Test member invitation (email link flow; requires mocking email)
  - Test join by code flow
  - Test member removal
- **Acceptance Criteria:**
  - [ ] 15+ test cases for household flows
  - [ ] Create household tested
  - [ ] Switcher tested
  - [ ] Invitation flow tested
  - [ ] Code join tested
  - [ ] Member removal tested
- **Dependencies:** M2-F1 through M2-F4
- **Labels:** `frontend`, `testing`, `household`
- **Milestone:** M2

---

## Milestone 3: Task Management (M3)

### Backend Repository (3 issues)

#### M3-B1: Task Model with Single Membership Assignment
- **Title:** `[M3-Backend] Implement Task model with single Membership assignment`
- **Goal:** Tasks with single assignee (references Membership for household scoping)
- **Scope:**
  - Task model: household_id, title, description, due_date, created_by_id→User, assigned_to_id→Membership (nullable), completed, completed_by_id→User (nullable), completed_at, timestamps
  - Manager method: `active_tasks()` returns non-deleted tasks
  - Validation: assigned_to_id must be in same household as task
  - Check constraint: assigned_to.household_id == task.household_id
  - Queries return created_by name and assigned_to name for display
- **Acceptance Criteria:**
  - [ ] Model matches DOMAIN_MODEL_CORRECTED.md
  - [ ] assigned_to_id FK to Membership (not User)
  - [ ] Check constraint ensures same household
  - [ ] completed_at auto-set when completed=True
  - [ ] Queries return names for display
  - [ ] Migrations correct
- **Dependencies:** M0-B2, M2-B2
- **PRD References:** FR-27-36 (task management)
- **OpenAPI References:** /households/{id}/tasks*
- **Labels:** `backend`, `task`, `high-priority`
- **Milestone:** M3

#### M3-B2: Task CRUD Endpoints
- **Title:** `[M3-Backend] Implement task endpoints (list, create, get, update, delete, complete)`
- **Goal:** Full task lifecycle via API
- **Scope:**
  - GET /households/{id}/tasks (list, filters: completed, assigned_to_id, due_date; pagination)
  - POST /households/{id}/tasks (create, created_by=current_user)
  - GET /households/{id}/tasks/{task_id} (get details)
  - PATCH /households/{id}/tasks/{task_id} (edit: creator/owner can reassign; any member can update other fields)
  - DELETE /households/{id}/tasks/{task_id} (hard-delete, creator/owner only)
  - PATCH /households/{id}/tasks/{task_id}/complete (mark complete, assigned member or owner only; sets completed_at)
  - Authorization: creator/owner for delete/reassign, assigned member for mark complete
  - If assigned member removed from household: task assigned_to_id → NULL
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md
  - [ ] GET list: pagination (page, limit), filters work, sorted by date
  - [ ] POST: creates with created_by=current_user
  - [ ] PATCH: any member can edit, creator/owner can reassign
  - [ ] DELETE: creator/owner only
  - [ ] Complete: assigned member or owner only, sets completed_at
  - [ ] If member removed: task unassigned
  - [ ] All return serialized task with names
- **Dependencies:** M3-B1, M2-B2, M1-B3
- **PRD References:** FR-27-36
- **OpenAPI References:** /households/{id}/tasks*
- **Labels:** `backend`, `task`, `api`
- **Milestone:** M3

#### M3-B3: Task Authorization & Cross-Household Isolation Tests
- **Title:** `[M3-Backend] Write task CRUD and authorization tests (50+ cases)`
- **Goal:** Ensure task operations respect authorization model
- **Scope:**
  - CRUD tests: create, read, list, update, delete
  - Authorization matrix: creator, owner, assigned member, random member, non-member
  - Cross-household isolation: prevent access to tasks from different household
  - Member removal: task unassignment on member removal
  - Reassignment: only creator/owner can reassign
- **Acceptance Criteria:**
  - [ ] 50+ test cases
  - [ ] Authorization matrix tested
  - [ ] All error cases return correct status (403 for unauthorized)
  - [ ] Cross-household isolation verified
  - [ ] Unassignment on member removal tested
  - [ ] Coverage >95%
- **Dependencies:** M3-B1, M3-B2
- **Labels:** `backend`, `testing`, `task`
- **Milestone:** M3

### Frontend Repository (2 issues)

#### M3-F1: Task List Page & CRUD Forms
- **Title:** `[M3-Frontend] Create task list, create, edit, and detail pages`
- **Goal:** Full task UI for household members
- **Scope:**
  - src/pages/TaskListPage.tsx: display open/completed sections, filters, pagination
  - Create task form (modal or page): title (required), description, due_date, assigned_to_id (dropdown)
  - Edit task form (modal or page)
  - Task detail page: show task info, edit/delete buttons, complete toggle
  - Assignment dropdown: shows only household members
  - Filtering: by assignee, status, due date
  - Pagination: next/prev or infinite scroll
  - Validation: React Hook Form + Zod
- **Acceptance Criteria:**
  - [ ] Task list fetched on load, shows open and completed sections
  - [ ] Filters work (assignee dropdown, status toggle, date range)
  - [ ] Pagination works
  - [ ] Create form: title required, other fields optional, submits to POST
  - [ ] Edit form: pre-fills, submits to PATCH
  - [ ] Detail page: shows all task info, edit/delete visible only for creator/owner
  - [ ] Complete toggle: visible for assigned member and owner
  - [ ] Assignment dropdown: shows household members only
  - [ ] TanStack Query: cache invalidated after mutations
  - [ ] Responsive design
- **Dependencies:** M3-B2, M2-B3
- **OpenAPI References:** /households/{id}/tasks*
- **Labels:** `frontend`, `ui`, `task`
- **Milestone:** M3

#### M3-F2: Task UI Tests
- **Title:** `[M3-Frontend] Write task UI integration tests`
- **Goal:** Ensure task flows work end-to-end
- **Scope:**
  - Test create task flow (form validation, submission)
  - Test task list filtering and pagination
  - Test task edit flow
  - Test task completion
  - Test task deletion
  - Test authorization (creator/owner can delete, assigned member can complete)
- **Acceptance Criteria:**
  - [ ] 20+ test cases for task flows
  - [ ] Create/edit/delete tested
  - [ ] Filtering tested
  - [ ] Pagination tested
  - [ ] Completion tested
  - [ ] Authorization tested
- **Dependencies:** M3-F1
- **Labels:** `frontend`, `testing`, `task`
- **Milestone:** M3

---

## Milestone 4: Shopping List (M4)

### Backend Repository (3 issues)

#### M4-B1: ShoppingItem Model
- **Title:** `[M4-Backend] Implement ShoppingItem model`
- **Scope:**
  - ShoppingItem: household_id, name, quantity, purchased, purchased_by_id→User (nullable), purchased_at (nullable), created_by_id→User, timestamps
- **Acceptance Criteria:**
  - [ ] Model created, matches ERD
  - [ ] Migrations correct
- **Dependencies:** M0-B2, M2-B2
- **Labels:** `backend`, `shopping`, `models`
- **Milestone:** M4

#### M4-B2: Shopping Endpoints (CRUD)
- **Title:** `[M4-Backend] Implement shopping list endpoints`
- **Scope:**
  - GET /households/{id}/shopping (list, filters: purchased status)
  - POST /households/{id}/shopping (create item)
  - PATCH /households/{id}/shopping/{item_id} (update name/quantity/purchased)
  - DELETE /households/{id}/shopping/{item_id} (delete, creator/owner only)
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md
  - [ ] Filtering by purchased status works
  - [ ] Toggling purchased sets purchased_by_id and purchased_at
  - [ ] Authorization enforced
- **Dependencies:** M4-B1, M2-B2, M1-B3
- **OpenAPI References:** /households/{id}/shopping*
- **Labels:** `backend`, `shopping`, `api`
- **Milestone:** M4

#### M4-B3: Shopping Tests
- **Title:** `[M4-Backend] Write shopping CRUD and authorization tests`
- **Scope:**
  - CRUD operations tested
  - Authorization: creator/owner can delete
  - Cross-household isolation
- **Acceptance Criteria:**
  - [ ] 20+ test cases
  - [ ] CRUD tested
  - [ ] Authorization tested
  - [ ] Cross-household isolation verified
- **Dependencies:** M4-B1, M4-B2
- **Labels:** `backend`, `testing`, `shopping`
- **Milestone:** M4

### Frontend Repository (2 issues)

#### M4-F1: Shopping List UI (List, Create, Edit, Toggle)
- **Title:** `[M4-Frontend] Create shopping list page with CRUD forms`
- **Scope:**
  - src/pages/ShoppingListPage.tsx: show pending and purchased items
  - Add item form: name (required), quantity
  - Edit item form
  - Toggle purchased checkbox (any member can toggle, creator/owner can delete)
  - Delete button
- **Acceptance Criteria:**
  - [ ] Shopping list shows pending and purchased sections
  - [ ] Add form works, submits to POST
  - [ ] Edit form works
  - [ ] Toggle checkbox works
  - [ ] Delete works (only for creator/owner)
  - [ ] List updates on mutations
- **Dependencies:** M4-B2, M2-F1
- **OpenAPI References:** /households/{id}/shopping*
- **Labels:** `frontend`, `ui`, `shopping`
- **Milestone:** M4

#### M4-F2: Shopping UI Tests
- **Title:** `[M4-Frontend] Write shopping UI tests`
- **Scope:**
  - Test create, edit, delete flows
  - Test toggle purchased
  - Test authorization
- **Acceptance Criteria:**
  - [ ] 15+ test cases
  - [ ] All flows tested
  - [ ] Authorization tested
- **Dependencies:** M4-F1
- **Labels:** `frontend`, `testing`, `shopping`
- **Milestone:** M4

---

## Milestone 5: Expense Tracking (M5)

### Backend Repository (3 issues)

#### M5-B1: Expense Model
- **Title:** `[M5-Backend] Implement Expense model`
- **Scope:**
  - Expense: household_id, amount_cents, category (groceries|utilities|entertainment|other), payer_id→User PROTECT, description, created_by_id→User, timestamps
- **Acceptance Criteria:**
  - [ ] Model created, matches ERD
  - [ ] Payer FK is PROTECT (immutable)
  - [ ] Amount in cents (no decimals)
  - [ ] Category enum validated
  - [ ] Migrations correct
- **Dependencies:** M0-B2, M2-B2
- **Labels:** `backend`, `expense`, `models`
- **Milestone:** M5

#### M5-B2: Expense Endpoints (CRUD)
- **Title:** `[M5-Backend] Implement expense endpoints`
- **Scope:**
  - GET /households/{id}/expenses (list, filters: category, payer, date range; sorted by date desc)
  - POST /households/{id}/expenses (create, defaults payer=creator)
  - PATCH /households/{id}/expenses/{expense_id} (update except payer, creator/owner only)
  - DELETE /households/{id}/expenses/{expense_id} (hard-delete, creator/owner only)
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md
  - [ ] Filtering works (category, payer, date range)
  - [ ] Sorted by date (newest first)
  - [ ] Payer immutable after creation
  - [ ] Authorization enforced
- **Dependencies:** M5-B1, M2-B2, M1-B3
- **OpenAPI References:** /households/{id}/expenses*
- **Labels:** `backend`, `expense`, `api`
- **Milestone:** M5

#### M5-B3: Expense Tests
- **Title:** `[M5-Backend] Write expense CRUD and authorization tests`
- **Scope:**
  - CRUD operations tested
  - Payer immutability tested
  - Authorization tested
  - Cross-household isolation
- **Acceptance Criteria:**
  - [ ] 20+ test cases
  - [ ] CRUD tested
  - [ ] Payer immutability verified
  - [ ] Authorization tested
- **Dependencies:** M5-B1, M5-B2
- **Labels:** `backend`, `testing`, `expense`
- **Milestone:** M5

### Frontend Repository (2 issues)

#### M5-F1: Expense List & CRUD UI
- **Title:** `[M5-Frontend] Create expense list page with CRUD forms and breakdown`
- **Scope:**
  - src/pages/ExpenseListPage.tsx: list sorted by date, shows total and per-category breakdown
  - Create form: amount (in dollars, converted to cents), category dropdown, payer dropdown, description
  - Edit form (cannot change payer)
  - Delete button
  - Category breakdown stats (pie chart or text summary)
- **Acceptance Criteria:**
  - [ ] Expense list fetched, sorted by date (newest first)
  - [ ] Total and per-category breakdown shown
  - [ ] Create form: amount in dollars, category/payer dropdowns, description
  - [ ] Edit form works, excludes payer field
  - [ ] Delete works (only for creator/owner)
  - [ ] Category breakdown displayed
  - [ ] Responsive design
- **Dependencies:** M5-B2, M2-F1
- **OpenAPI References:** /households/{id}/expenses*
- **Labels:** `frontend`, `ui`, `expense`
- **Milestone:** M5

#### M5-F2: Expense UI Tests
- **Title:** `[M5-Frontend] Write expense UI tests`
- **Scope:**
  - Test create, edit, delete flows
  - Test amount conversion (dollars to cents)
  - Test filtering
  - Test authorization
- **Acceptance Criteria:**
  - [ ] 15+ test cases
  - [ ] All flows tested
  - [ ] Amount conversion verified
  - [ ] Authorization tested
- **Dependencies:** M5-F1
- **Labels:** `frontend`, `testing`, `expense`
- **Milestone:** M5

---

## Milestone 6: Inventory Management (M6)

### Backend Repository (3 issues)

#### M6-B1: InventoryItem Model
- **Title:** `[M6-Backend] Implement InventoryItem model`
- **Scope:**
  - InventoryItem: household_id, name, quantity, category (nullable), location (nullable), created_by_id→User, timestamps
- **Acceptance Criteria:**
  - [ ] Model created, matches ERD
  - [ ] Category and location optional
  - [ ] Migrations correct
- **Dependencies:** M0-B2, M2-B2
- **Labels:** `backend`, `inventory`, `models`
- **Milestone:** M6

#### M6-B2: Inventory Endpoints (CRUD)
- **Title:** `[M6-Backend] Implement inventory endpoints`
- **Scope:**
  - GET /households/{id}/inventory (list, filters: category optional)
  - POST /households/{id}/inventory (create item)
  - PATCH /households/{id}/inventory/{item_id} (update quantity/category/location)
  - DELETE /households/{id}/inventory/{item_id} (hard-delete, creator/owner only)
- **Acceptance Criteria:**
  - [ ] All endpoints match OPENAPI.md
  - [ ] Filtering by category works
  - [ ] Quantity updates correctly
  - [ ] Authorization enforced
- **Dependencies:** M6-B1, M2-B2, M1-B3
- **OpenAPI References:** /households/{id}/inventory*
- **Labels:** `backend`, `inventory`, `api`
- **Milestone:** M6

#### M6-B3: Inventory Tests
- **Title:** `[M6-Backend] Write inventory CRUD and authorization tests`
- **Scope:**
  - CRUD operations tested
  - Optional field validation
  - Authorization tested
  - Cross-household isolation
- **Acceptance Criteria:**
  - [ ] 20+ test cases
  - [ ] CRUD tested
  - [ ] Optional fields validated
  - [ ] Authorization tested
- **Dependencies:** M6-B1, M6-B2
- **Labels:** `backend`, `testing`, `inventory`
- **Milestone:** M6

### Frontend Repository (2 issues)

#### M6-F1: Inventory List & CRUD UI
- **Title:** `[M6-Frontend] Create inventory list page with CRUD forms`
- **Scope:**
  - src/pages/InventoryListPage.tsx: list filterable by category
  - Add item form: name (required), quantity, optional category/location
  - Edit item form
  - Delete button
- **Acceptance Criteria:**
  - [ ] Inventory list fetched, filterable by category
  - [ ] Add form works
  - [ ] Edit form works
  - [ ] Delete works (only for creator/owner)
  - [ ] Category filtering works
  - [ ] Responsive design
- **Dependencies:** M6-B2, M2-F1
- **OpenAPI References:** /households/{id}/inventory*
- **Labels:** `frontend`, `ui`, `inventory`
- **Milestone:** M6

#### M6-F2: Inventory UI Tests
- **Title:** `[M6-Frontend] Write inventory UI tests`
- **Scope:**
  - Test create, edit, delete flows
  - Test filtering
  - Test authorization
- **Acceptance Criteria:**
  - [ ] 15+ test cases
  - [ ] All flows tested
  - [ ] Filtering tested
  - [ ] Authorization tested
- **Dependencies:** M6-F1
- **Labels:** `frontend`, `testing`, `inventory`
- **Milestone:** M6

---

## Milestone 7: Dashboard (M7)

### Backend Repository (1 issue)

#### M7-B1: Dashboard Aggregation Endpoint
- **Title:** `[M7-Backend] Implement dashboard aggregation endpoint`
- **Scope:**
  - GET /households/{id}/dashboard
  - Returns: household info, members, pending tasks (top 3), shopping (pending count), recent expenses (last 5, total)
- **Acceptance Criteria:**
  - [ ] Endpoint matches OPENAPI.md
  - [ ] Aggregates data correctly from all domains
  - [ ] Performs efficiently (no N+1 queries)
  - [ ] Authorization verified (only members)
- **Dependencies:** M3-B2, M4-B2, M5-B2, M6-B2
- **OpenAPI References:** GET /households/{id}/dashboard
- **Labels:** `backend`, `dashboard`, `api`
- **Milestone:** M7

### Frontend Repository (1 issue)

#### M7-F1: Dashboard Page with Quick Actions
- **Title:** `[M7-Frontend] Create household dashboard page (minimal scope)`
- **Scope:**
  - src/pages/DashboardPage.tsx
  - Display household identification (name, member count)
  - Display member list
  - Display pending tasks (open, due-soon, overdue; up to 5)
  - Display shopping summary (pending item count)
  - Quick task creation button
  - Quick shopping item creation button
  - Links to detailed views (task list, shopping list, expenses, inventory, settings)
- **Acceptance Criteria:**
  - [ ] Dashboard loads from GET /households/{id}/dashboard
  - [ ] Shows household info, members, pending tasks, shopping summary
  - [ ] Quick action buttons work (create task, add shopping item)
  - [ ] Links to detailed views work
  - [ ] Responsive design
  - [ ] Authorization verified (only members see their household dashboard)
  - [ ] No analytics, charts, activity feed, or productivity metrics
- **Dependencies:** M7-B1, M3-F1, M4-F1, M5-F1
- **OpenAPI References:** GET /households/{id}/dashboard
- **Labels:** `frontend`, `ui`, `dashboard`
- **Milestone:** M7

---

## Milestone 8: Integration & Hardening (M8)

### Backend Repository (3 issues)

#### M8-B1: Backend Integration Tests (E2E Workflows)
- **Title:** `[M8-Backend] Write end-to-end integration tests (100+ cases)`
- **Goal:** Test full user journeys across all features
- **Scope:**
  - Journey: signup → create household → invite member → member joins → create task → mark complete
  - Journey: create expense → appears on dashboard → filtering works
  - Journey: add shopping items → toggle purchased → appears on dashboard
  - Journey: member removal → access lost → task unassigned
  - Cross-domain: data consistency across features
  - Stress test: 100 concurrent users, target <200ms response
- **Acceptance Criteria:**
  - [ ] 100+ integration test cases
  - [ ] All user journeys passing
  - [ ] Cross-domain consistency verified
  - [ ] Performance baseline: <200ms for 100 concurrent users
  - [ ] No N+1 queries detected
  - [ ] Coverage: >90% of business logic
- **Dependencies:** All M0-M7 Backend issues
- **Labels:** `backend`, `testing`, `integration`
- **Milestone:** M8

#### M8-B2: Security Hardening & Validation Tests
- **Title:** `[M8-Backend] Security hardening and validation testing`
- **Scope:**
  - CSRF token validation: all POST/PATCH/DELETE require valid token
  - Password hashing: bcrypt/Argon2 with proper cost
  - Session security: HttpOnly, Secure (prod), SameSite=Strict flags
  - Input validation: email format, amounts, string lengths, enum values
  - Rate limiting: login 5/min per IP, reset 3/hour per email, API 100/15min per user
  - SQL injection prevention: parameterized queries only
  - Authorization: 403 for unauthorized, 401 for unauthenticated
  - Dependency security scan: pip audit, no critical vulnerabilities
- **Acceptance Criteria:**
  - [ ] CSRF protection verified (tests attempt invalid tokens)
  - [ ] Password hashing verified (bcrypt/Argon2)
  - [ ] Session cookie flags correct
  - [ ] All inputs validated (format, length, enum, type)
  - [ ] Rate limiting enforced and tested
  - [ ] SQL injection prevention verified
  - [ ] Authorization matrix verified (403/401 correct)
  - [ ] Security scan: no critical vulnerabilities
- **Dependencies:** All M0-M7 Backend issues
- **Labels:** `backend`, `security`, `testing`
- **Milestone:** M8

#### M8-B3: Performance Optimization & Database Tuning
- **Title:** `[M8-Backend] Performance optimization and database tuning`
- **Scope:**
  - Query optimization: N+1 prevention via select_related/prefetch_related
  - Index verification: all 18+ indexes created as per ERD
  - Database statistics: ANALYZE run on schema
  - Slow query logging: identify remaining slow queries
  - Batch operations: bulk_create/bulk_update for large datasets
  - Caching strategy: HTTP caching headers, conditional requests
- **Acceptance Criteria:**
  - [ ] All indexes verified in production schema
  - [ ] No N+1 queries in any endpoint
  - [ ] GET /households/{id}/tasks with 1000 tasks returns <200ms
  - [ ] Query execution plans reviewed (no sequential scans on large tables)
  - [ ] Database statistics current
  - [ ] HTTP caching headers configured
- **Dependencies:** All M0-M7 Backend issues
- **Labels:** `backend`, `performance`, `database`
- **Milestone:** M8

### Frontend Repository (2 issues)

#### M8-F1: Frontend E2E Tests
- **Title:** `[M8-Frontend] Write end-to-end tests for critical workflows`
- **Scope:**
  - Login, create household, invite member, member joins, create task, mark complete
  - Create expense, filter expenses
  - Add shopping items, toggle purchased
  - Household switching
  - Member removal and access loss
- **Acceptance Criteria:**
  - [ ] 20+ E2E test cases
  - [ ] All critical workflows passing
  - [ ] Mock API responses for testing
- **Dependencies:** All M0-M7 Frontend issues
- **Labels:** `frontend`, `testing`, `e2e`
- **Milestone:** M8

#### M8-F2: Frontend Performance Optimization
- **Title:** `[M8-Frontend] Frontend performance optimization and bundle analysis`
- **Scope:**
  - Bundle size analysis: main chunk <500KB
  - Code splitting: lazy load pages via React.lazy()
  - Image optimization: compress images, use appropriate formats
  - TanStack Query optimization: cache strategies, stale-while-revalidate
  - Lighthouse audit: aim for >80 on performance, accessibility, best practices
- **Acceptance Criteria:**
  - [ ] Main bundle <500KB (gzip)
  - [ ] Code splitting configured
  - [ ] Images optimized
  - [ ] Lighthouse score >80 (performance)
  - [ ] No console errors
- **Dependencies:** All M0-M7 Frontend issues
- **Labels:** `frontend`, `performance`
- **Milestone:** M8

### Documentation Repository (1 issue)

#### M8-D1: Documentation Finalization & Testing
- **Title:** `[M8-Documentation] Finalize all documentation and test with external users`
- **Scope:**
  - API documentation (OpenAPI rendered)
  - Deployment guide (step-by-step for ops)
  - Development setup guide (tested with 2 fresh developers)
  - Security considerations (rate limiting, session management, CSRF, auth)
  - Testing guide (how to run tests, coverage, performance testing)
  - Troubleshooting guide (common errors and solutions)
  - Architecture guide (ADRs, System Design, ERD, data model)
- **Acceptance Criteria:**
  - [ ] All 4 main guides completed and tested
  - [ ] Setup guide tested with fresh developer; <30 min
  - [ ] Deployment guide tested with fresh ops person
  - [ ] All documentation renders correctly
  - [ ] No broken links
  - [ ] Examples are accurate and runnable
- **Dependencies:** All M0-M7 Backend/Frontend issues
- **Labels:** `documentation`
- **Milestone:** M8

---

## Milestone 9: Deployment Readiness (M9)

### Infrastructure Repository (2 issues)

#### M9-I1: Production Deployment Configuration
- **Title:** `[M9-Infrastructure] Production deployment setup (Docker, env, health checks)`
- **Scope:**
  - Docker images optimized for production
  - Environment variables for production (secrets management)
  - Database migrations automated on deploy
  - Static assets built and optimized
  - Health check endpoint (/health)
  - Rollback procedure documented
- **Acceptance Criteria:**
  - [ ] Docker images built and tested
  - [ ] Production secrets in environment (not committed)
  - [ ] Migrations run automatically
  - [ ] Health check endpoint responds 200
  - [ ] Rollback procedure documented
- **Dependencies:** All previous milestones
- **Labels:** `infrastructure`, `deployment`
- **Milestone:** M9

#### M9-I2: Monitoring & Observability Setup
- **Title:** `[M9-Infrastructure] Set up monitoring, logging, and error tracking`
- **Scope:**
  - Structured JSON logging to stdout
  - Error tracking: Sentry free tier or similar
  - Application health dashboard (basic metrics)
  - Incident response runbook
- **Acceptance Criteria:**
  - [ ] Logs in JSON format
  - [ ] Errors logged to Sentry with context
  - [ ] Health dashboard accessible
  - [ ] Incident runbook documented
- **Dependencies:** All previous milestones
- **Labels:** `infrastructure`, `monitoring`
- **Milestone:** M9

### Automation Repository (1 issue)

#### M9-A1: Pre-Launch Verification & Launch Checklist
- **Title:** `[M9-Automation] Pre-launch verification and launch execution`
- **Scope:**
  - Smoke tests on production (signup, create household, create task)
  - Database backup tested and restore procedure documented
  - Security scan: no critical vulnerabilities
  - Load test baseline: 100 concurrent users, target <500ms
  - Performance baseline captured
  - First 24 hours monitoring plan
- **Acceptance Criteria:**
  - [ ] Smoke tests pass on production
  - [ ] Database backup/restore tested
  - [ ] Security scan: no critical vulnerabilities
  - [ ] Load test: <500ms at 100 concurrent users
  - [ ] Performance metrics captured
  - [ ] 24-hour monitoring plan documented
- **Dependencies:** All previous milestones
- **Labels:** `automation`, `deployment`, `launch`
- **Milestone:** M9

---

## Issue Count Summary

**By Repository:**
- Backend: 34 issues
- Frontend: 23 issues
- Infrastructure: 4 issues
- Automation: 4 issues
- Documentation: 3 issues
- **TOTAL: 68 issues**

**By Milestone:**
| M | Count |
|---|-------|
| M0 | 16 |
| M1 | 9 |
| M2 | 11 |
| M3 | 5 |
| M4 | 5 |
| M5 | 5 |
| M6 | 5 |
| M7 | 2 |
| M8 | 6 |
| M9 | 4 |

**Consolidations from Original Plan (71 → 68):**
1. Documentation setup: 3 issues → 1 (M0-D1 covers OpenAPI, setup guide, architecture docs)
2. Testing moved upstream: Explicit test issues for complex features (auth, household, task); acceptance criteria for simpler features (shopping, expense, inventory)
3. Dashboard: Added M7 as explicit product feature
4. Milestone renumbering: M0-M9 structure with parallelizable M3-M6

---

## Next Steps for Review

1. **Verify Issue Specifications**
   - Are titles clear?
   - Are scopes appropriate?
   - Are acceptance criteria objective and testable?
   - Are dependencies explicit?

2. **Validate Dependencies**
   - Are cross-repository dependencies clear?
   - Can M3-M6 truly be parallelized?
   - Are there hidden blocking dependencies?

3. **Confirm Issue Sizing**
   - Are issues 1-2 days of work (roughly)?
   - Are any too large or too small?

4. **Confirm Milestone Structure**
   - Does M0-M9 make sense?
   - Is testing approach (continuous per feature) sufficient?

5. **Approve for GitHub Issue Creation**
   - Once approved, create all 68 issues in respective repositories
   - Use labels, milestones, and dependencies in GitHub issues

---
