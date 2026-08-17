# Critical Decisions Resolution Summary

**Date:** August 16, 2026  
**Status:** ✓ All Critical Decisions Resolved  
**Ready for:** Domain Model Review → Implementation Planning

---

## Decisions Resolved

### ✓ 1. Backend Framework: Django + Django REST Framework

**Decision:** Use Python + Django 4.2 LTS + Django REST Framework for the backend API

**Key Benefits:**
- Mature, battle-tested (15+ years in production)
- Built-in authentication, ORM, migrations, security
- Permission framework perfect for household scoping
- Reduces custom infrastructure needed for MVP
- Excellent PostgreSQL integration

**Impact:** Entire backend architecture, development process, testing strategy

**Documented in:** SYSTEM_DESIGN.md Part 1, ADR-002

---

### ✓ 2. Session Storage: Database-Backed (No Redis Required)

**Decision:** Use Django's database-backed session engine (PostgreSQL `django_session` table)

**Key Benefits:**
- Zero additional dependencies (uses existing PostgreSQL)
- Sufficient for MVP scale (10k+ concurrent sessions)
- Simpler development (Docker Compose needs only PostgreSQL)
- Automatic TTL and cleanup via Django

**Constraints:** 
- Acceptable latency ~1-5ms per session lookup
- Scales with database; Redis migration possible later if needed

**Impact:** Infrastructure simplification; reduced deployment complexity

**Documented in:** SYSTEM_DESIGN.md Part 1, ADR-007

---

### ✓ 3. Task Assignment Model: Single Assignee (No TaskAssignment Entity)

**Decision:** Each task has zero or one assignee; no multi-assignment for MVP

**Key Benefits:**
- Simpler data model (8 tables, not 9)
- Faster queries (no join needed)
- Simpler UI (single dropdown, not multi-select)
- Clearer authorization (assigned member or owner can complete)

**Rationale:**
- PRD doesn't require multi-assignment
- Household task workflows typically assign to one person
- Easy to migrate to multi-assign post-MVP if needed

**Assignment Reference:** Task.assigned_to → Membership (not User)
- Ensures assignment is scoped to household membership
- Automatic unassignment if member removed from household

**Impact:** Data model, API design, UI simplicity

**Documented in:** SYSTEM_DESIGN.md Part 2, ADR-008, DOMAIN_MODEL_FINAL.md

---

### ✓ 4. Deployment Platform: TBD (Platform-Neutral Architecture)

**Decision:** Application remains platform-neutral; deployment platform chosen post-MVP

**Key Benefits:**
- Development uses Docker Compose (local PostgreSQL, no deployment concerns)
- Application code not coupled to infrastructure
- Can choose Heroku, AWS, DigitalOcean, or self-hosted based on requirements
- Production deployment platform chosen when operational requirements clear

**Approach:**
- Docker containers for reproducible environments
- Environment variables for configuration (DATABASE_URL, SECRET_KEY, etc.)
- No infrastructure-specific code in application

**Impact:** Flexibility; no premature infrastructure lock-in

**Documented in:** SYSTEM_DESIGN.md Part 9, ADR-001

---

## Architecture Decision Records (ADRs)

All major architectural decisions documented in separate ADR files:

| ADR | Decision | Status |
|-----|----------|--------|
| ADR-001 | Multi-repository architecture (Backend, Frontend, Infrastructure separate) | ✓ Accepted |
| ADR-002 | Django + Django REST Framework backend | ✓ Accepted |
| ADR-003 | PostgreSQL persistence | ✓ Accepted |
| ADR-004 | Session-based authentication with HTTP-only cookies + Google OAuth | ✓ Accepted |
| ADR-005 | Household-scoped authorization via Membership entity | ✓ Accepted |
| ADR-006 | API-based synchronization (no real-time transport) | ✓ Accepted |
| ADR-007 | Database-backed sessions for MVP (no Redis) | ✓ Accepted |
| ADR-008 | Single-assignee task model (no TaskAssignment entity) | ✓ Accepted |

**Location:** `architecture/adr/ADR-*.md`

---

## Complete Domain Model

**8 Core Entities:**

1. **User** — Account and identity (email, password, Google OAuth)
2. **Household** — Container for shared data (name, description, owner)
3. **Membership** — User's membership in household (role: owner/member)
4. **Invitation** — Email invitations to join household (state: pending/accepted/revoked/expired)
5. **Task** — Household task or chore (single assignee to Membership)
6. **ShoppingItem** — Shopping list item (purchased boolean)
7. **Expense** — Household expense (amount in cents, category, payer)
8. **InventoryItem** — Household inventory tracking (name, quantity)

**Key Design Points:**
- ✓ Single assignee per task (assigned_to → Membership, not User)
- ✓ All entities scoped by household_id (security boundary)
- ✓ Soft-delete for households only; hard-delete for individual resources
- ✓ Membership deletion preserves user's created data
- ✓ Foreign key constraints (CASCADE for household scope, SET NULL for content preservation)

**Complete Specification:** `DOMAIN_MODEL_FINAL.md`

---

## Technology Stack (Final)

### Backend
- **Language:** Python 3.9+
- **Framework:** Django 4.2+ LTS
- **REST API:** Django REST Framework
- **Database:** PostgreSQL 14+
- **ORM:** Django ORM (built-in)
- **Migrations:** Django migrations (built-in)
- **Authentication:** Django contrib.auth + django-allauth (for Google OAuth)
- **Sessions:** Django contrib.sessions (database-backed)
- **Testing:** pytest + pytest-django

### Frontend
- **Language:** TypeScript
- **Framework:** React 18+
- **Routing:** React Router v6
- **State Management:** TanStack Query (React Query) for server-state
- **Forms:** React Hook Form + Zod
- **Styling:** Tailwind CSS
- **Build Tool:** Vite (or Create React App)

### Database
- **System:** PostgreSQL 14+
- **Backups:** Managed by deployment platform (Heroku, RDS, etc.)

### Development
- **Containerization:** Docker + Docker Compose
- **Version Control:** Git

### Deployment (TBD)
- **Platform:** Platform-neutral (Docker containers)
- **Options:** Heroku, AWS, DigitalOcean, self-hosted
- **Database:** Managed PostgreSQL service

### NOT Included in MVP
- ✗ Redis (optional; can be added post-MVP for caching)
- ✗ Message queues (async tasks can be added later)
- ✗ WebSockets/SSE (API-based polling sufficient)
- ✗ Distributed tracing (request IDs + logging sufficient)
- ✗ Prometheus/Grafana (post-MVP metrics)
- ✗ Real-time synchronization (post-MVP feature)

---

## Files Created/Updated

### Documentation
- ✓ `SYSTEM_DESIGN.md` (v3.0) — Complete system design with all decisions
- ✓ `DOMAIN_MODEL_FINAL.md` — Final domain model with entity definitions
- ✓ `RESOLUTION_SUMMARY.md` — This document

### Architecture Decision Records
- ✓ `architecture/adr/ADR-001-multi-repository-structure.md`
- ✓ `architecture/adr/ADR-002-django-rest-framework.md`
- ✓ `architecture/adr/ADR-003-postgresql-persistence.md`
- ✓ `architecture/adr/ADR-004-session-based-authentication.md`
- ✓ `architecture/adr/ADR-005-household-scoped-authorization.md`
- ✓ `architecture/adr/ADR-006-api-based-synchronization.md`
- ✓ `architecture/adr/ADR-007-database-backed-sessions.md`
- ✓ `architecture/adr/ADR-008-single-assignee-task-model.md`

### Previous Documentation
- `tasks/prd-householdhub-mvp.md` — Product requirements (unchanged)
- `tasks/PRD-REVISION-SUMMARY.md` — PRD revision history
- `ARCHITECTURE_REVIEW.md` — Critical review findings
- `SYSTEM_DESIGN_REVISION_SUMMARY.md` — v1 to v2 changes

---

## Validation Checklist

### Domain Model Validation
- ✓ All 8 entities defined with attributes and constraints
- ✓ Entity cardinalities verified (1:1, 1:N, N:N)
- ✓ Foreign key behavior documented (CASCADE, SET NULL)
- ✓ Household scoping confirmed on all entities
- ✓ Ownership vs. authorship clarified per entity
- ✓ Member removal behavior specified
- ✓ Household deletion behavior specified
- ✓ Soft-deletion scoped to households only
- ✓ Single assignee model validated (no TaskAssignment entity)

### Architecture Validation
- ✓ Backend framework chosen (Django)
- ✓ Database chosen (PostgreSQL)
- ✓ Authentication mechanism chosen (session-based)
- ✓ Session storage chosen (database-backed)
- ✓ Frontend framework specified (React + TanStack Query)
- ✓ API style chosen (REST)
- ✓ Deployment approach defined (platform-neutral Docker)
- ✓ Concurrency model clarified (last-write-wins)
- ✓ Authorization model validated (Membership-based scoping)
- ✓ Synchronization approach confirmed (API-based, no real-time)

### Completeness
- ✓ All critical decisions documented
- ✓ All trade-offs explained
- ✓ All alternatives considered
- ✓ All risks identified
- ✓ Migration paths documented
- ✓ MVP scope clarified (what's included, what's deferred)

---

## Status: Ready for Review

**All critical decisions have been made and documented.**

Before proceeding to implementation planning, **review and approve:**

1. **DOMAIN_MODEL_FINAL.md** — Validate all 8 entities, relationships, constraints
2. **SYSTEM_DESIGN.md Parts 1-9** — Validate architecture and technical approach
3. **Architecture Decision Records** — Confirm rationale and trade-offs
4. **Technology Stack** — Confirm backend (Django), frontend (React), database (PostgreSQL), sessions (database-backed)

---

## Next Steps (If Approved)

### Phase 1: Implementation Planning
- [ ] Create feature breakdown (auth, households, tasks, shopping, expenses, inventory)
- [ ] Estimate effort per feature
- [ ] Plan development sprints (MVP target: 8-12 weeks)
- [ ] Identify technical dependencies

### Phase 2: Project Setup
- [ ] Initialize Django project structure (Backend/)
- [ ] Initialize React project structure (Frontend/)
- [ ] Create Docker Compose for full-stack development
- [ ] Create GitHub repositories and CI/CD pipelines

### Phase 3: Data Layer
- [ ] Define Django models based on DOMAIN_MODEL_FINAL.md
- [ ] Generate database migrations
- [ ] Create indexes for performance
- [ ] Write model tests

### Phase 4: API Layer
- [ ] Create DRF serializers for each entity
- [ ] Create DRF viewsets and routes
- [ ] Implement authorization/permission checks
- [ ] Generate OpenAPI specification
- [ ] Write API integration tests

### Phase 5: Frontend Layer
- [ ] Create React component structure
- [ ] Implement authentication UI (login, signup, password reset, Google OAuth)
- [ ] Implement household selection UI
- [ ] Implement household management UI (create, invite, join)
- [ ] Implement core features (tasks, shopping, expenses, inventory)
- [ ] Write component and E2E tests

### Phase 6: Polish & Launch
- [ ] Security hardening (CSRF, rate limiting, input validation)
- [ ] Performance optimization (query optimization, caching)
- [ ] Documentation (API docs, user guide, deployment guide)
- [ ] Staging deployment
- [ ] User acceptance testing
- [ ] Production deployment

---

## Questions for Clarification

Before starting implementation, confirm:

1. **Timeline:** What's the target launch date for MVP?
2. **Team:** Who's on the backend team? Frontend team? DevOps?
3. **Development Environment:** Should developers use Docker Compose locally?
4. **Testing:** What test coverage targets? (Recommended: API 85%+, Authorization 100%)
5. **Deployment:** Will deployment platform be decided before or after MVP launch?

---

## End of Resolution Summary

✓ **All critical architectural decisions have been resolved**  
✓ **Complete domain model has been validated**  
✓ **8 ADRs document major technical choices**  
✓ **Ready for team review and approval**

Proceed to implementation planning once approved.

---

