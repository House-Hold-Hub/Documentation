# System Design Revision Summary
**Date:** August 16, 2026  
**Revision:** 1.0 → 2.0 (MVP Focus)

---

## Overview

System Design v2.0 eliminates prescriptive technology choices without validation, marks critical unresolved decisions explicitly, removes unnecessary complexity, and clearly separates MVP-required components from future-evolution options.

---

## Architectural Decisions Retained ✓

These core decisions are sound and retained:

1. **REST API** — Pragmatic for MVP, suitable for domain, can evolve to GraphQL post-MVP
2. **PostgreSQL** — Relational model fits domain perfectly, ACID important for expenses
3. **Session-based auth with HTTP-only cookies** — Secure pattern, framework-agnostic
4. **React + TanStack Query** (for frontend) — Explicitly designed for server-state sync
5. **Household membership scoping** — At database, middleware, and API layers
6. **Authorization model** — Owner/member permissions clear and testable
7. **Last-write-wins concurrency** — Per PRD requirement, acceptable for MVP
8. **CSRF/XSS/SQL injection protections** — Standard web application security

---

## Architectural Decisions Changed

### 1. Session Storage: Moved from Requirement to Decision with Alternatives

**v1.0:** "Redis cluster for high availability" (prescribed)  
**v2.0:** "Redis cluster, single Redis, or database sessions — TBD based on backend framework and scale"

**Why:** Redis cluster adds operational complexity without scaling justification for MVP. Alternatives:
- Django ORM sessions (if Django backend) → no new dependency, secure, built-in
- Single Redis instance → fast but stateful, accepts SPOF for MVP
- Database sessions → simple, no new dependency, slower but sufficient

**Migration path documented:** Single Redis or database sessions initially; upgrade to cluster if load testing shows need.

### 2. Deployment Platform: Removed False Choice Between AWS ECS and Heroku

**v1.0:** "AWS ECS or Heroku" (two incompatible options presented equally)  
**v2.0:** "TBD — Choose Heroku (simplest), AWS (more control), or other. Infrastructure specification required before commitment."

**Why:** 
- Heroku and AWS require different infrastructure (Procfile vs. ECS tasks vs. RDS vs. Heroku Postgres)
- System Design v1.0 assumed AWS throughout (RDS, ElastiCache, ECS, Secrets Manager) then casually mentioned Heroku
- This was a contradiction, not a decision

**New approach:**
- Use Docker Compose for local development (framework-agnostic)
- Defer production deployment platform until ready to ship
- Document both options with tradeoffs when needed

### 3. Backend Framework: Moved from Hidden Assumption to Explicit TBD

**v1.0:** Assumed Node.js/Express (prescribed Winston, npm, Flyway, etc.)  
**v2.0:** "Backend framework TBD before implementation. Once chosen, use framework-native solutions for auth, sessions, migrations."

**Why:**
- System Design prescribed specific technologies (Winston for logging, Flyway for migrations, express-session, etc.)
- But no validation that backend is Node.js
- If backend is Django: Use Django ORM migrations (not Flyway), django.contrib.auth (not custom), django.contrib.sessions (not Redis-only)
- If backend is FastAPI: Different approach entirely

**New approach:** Technology decisions documented in separate TECHNOLOGY_DECISIONS.md once framework is chosen.

### 4. Concurrency Model: Clarified Terminology

**v1.0:** "Last-write-wins with timestamps... if mismatch return 409" (contradictory)  
**v2.0:** Clarified two strategies:
- Pure last-write-wins: Accept all writes, no conflict detection (risk: data loss)
- Optimistic concurrency control: Include version/timestamp, reject (409) if stale (risk: user must refetch)

**Per-entity approach:**
- Low-contention entities (tasks, expenses): Accept last-write-wins
- Medium-contention entities (shopping, inventory): Optionally add conflict detection
- Decision per entity based on data integrity requirements

---

## Technologies Removed as Unnecessary ✗

### Backend Framework Prescriptions (Removed)
- ✗ Winston for logging (only Node.js; Django uses logging module, FastAPI uses logging, etc.)
- ✗ Liquibase/Flyway for migrations (only Java; use framework-native: Django ORM, Alembic, Knex.js, etc.)
- ✗ npm, Node.js-specific tooling assumptions (backend language TBD)
- ✗ express-session / passport.js specifics (framework TBD)

### Infrastructure for MVP (Removed)
- ✗ Redis Cluster (single instance or database sessions sufficient)
- ✗ AWS RDS Multi-AZ (single-AZ sufficient for MVP)
- ✗ AWS ElastiCache Cluster (single node sufficient)
- ✗ AWS ECS (Heroku, self-hosted, or other options valid)
- ✗ AWS Secrets Manager (environment variables sufficient for MVP)
- ✗ Load balancer (single server sufficient)

### Observability for MVP (Removed)
- ✗ Prometheus metrics collection (log-based observability sufficient)
- ✗ Grafana dashboards (post-MVP feature)
- ✗ DataDog APM (post-MVP feature)
- ✗ New Relic APM (post-MVP feature)
- ✗ Distributed tracing (request IDs sufficient for MVP)
- ✗ Advanced alerting infrastructure (basic logging sufficient)

### Operations for MVP (Removed)
- ✗ Asynchronous job queue (send emails synchronously)
- ✗ Idempotency keys for all operations (only needed for email-sending)
- ✗ RTO/RPO targets (configure post-MVP based on needs)
- ✗ Test coverage percentage targets (aim for quality, not percentage)

### Arbitrary Constants (Removed)
- ✗ 30-day session TTL (moved to TBD configuration)
- ✗ 30-day invitation expiry (moved to TBD configuration)
- ✗ 30-day household deletion retention (moved to TBD configuration)
- ✗ 100 requests / 15 minutes rate limit (moved to TBD configuration)
- ✗ 10+ character password requirement (moved to framework default)
- ✗ Alert thresholds (error rate >5%, latency >2s, etc.) — moved to TBD
- ✗ bcrypt cost=12 (moved to framework default with note on alternatives)

---

## Unresolved Decisions (Explicitly Marked TBD)

### Critical (Blockers for Implementation)

1. **Backend Framework**
   - Options: Django, FastAPI, Express, Flask, other?
   - Impact: Affects auth, sessions, migrations, testing
   - Timeline: Required before backend development starts

2. **Session Storage Strategy**
   - Options: Database sessions, single Redis, Redis HA
   - Impact: Operational complexity, dependencies, scaling
   - Timeline: Required before backend development starts
   - Depends on: Backend framework choice

3. **Task Assignment Model**
   - Question: Can one task have multiple assignees?
   - Current assumption: Single assignee (simpler model)
   - Impact: Affects data model (TaskAssignment entity yes/no)
   - Timeline: Required before schema design

### Post-MVP (Can Be Deferred)

4. **Deployment Platform**
   - Options: Heroku, AWS, DigitalOcean, self-hosted, other?
   - Impact: Infrastructure choices, cost, operational overhead
   - Timeline: Can be deferred; use Docker Compose for MVP development
   - Recommendation: Decide before launch, not before development

5. **Data Retention Policies**
   - Household soft-delete retention: 14, 30, or 90 days?
   - User soft-delete retention: 14, 30, or 90 days?
   - Impact: Legal compliance, storage costs
   - Timeline: Can use sensible defaults in development; finalize pre-launch

6. **Rate Limiting Configuration**
   - Login attempts: 5 per minute per IP? Configurable?
   - API endpoint limits: 100 per 15 min per user?
   - Impact: Security, user experience
   - Timeline: Can be tuned post-launch based on actual usage

---

## MVP Runtime Dependency List (Final)

**Required:**
- PostgreSQL 14+ (relational database)
- Docker (containerization for deployment)
- Framework of choice (Django, FastAPI, Express, Flask, etc.)
- Frontend framework (React or other)
- Standard libraries (ORM, HTTP client, templating, etc.)

**Optional (but recommended):**
- Redis (if using Redis for sessions; else skip)
- Sentry free tier (error tracking; can use logs instead)

**Not included:**
- Prometheus, Grafana, DataDog, New Relic (post-MVP)
- Redis Cluster (use single instance if using Redis)
- AWS managed services except deployment host (choose post-MVP)

---

## MVP Development Dependency List (Final)

**Backend:**
- Testing framework (pytest for Python, Jest for Node, unittest for Python, etc.)
- Database migration tool (built into Django, Alembic for Flask/FastAPI, Knex.js for Node)
- ORM or query builder (SQLAlchemy, Django ORM, Sequelize, etc.)
- Linting/formatting (black, flake8 for Python; eslint, prettier for Node)

**Frontend:**
- React 18+ (or chosen framework)
- React Query / SWR (server-state management)
- React Router (client-side routing)
- React Hook Form (form validation)
- Testing library (Jest, React Testing Library)
- Linting/formatting (eslint, prettier)

**All:**
- Docker & Docker Compose (local development)
- Version control (git)
- CI/CD (TBD: GitHub Actions, GitLab CI, etc.)

---

## ADRs That Should Now Be Created

Once critical decisions are made:

1. **ADR-001:** REST API over GraphQL (decision & rationale documented)
2. **ADR-002:** PostgreSQL for relational data (decision & rationale documented)
3. **ADR-003:** Session-based authentication with HTTP-only cookies (decision & rationale documented)
4. **ADR-004:** React + TanStack Query for frontend state (decision & rationale documented)
5. **ADR-005:** Last-write-wins concurrency for MVP (decision & rationale documented)
6. **ADR-006:** [Post-Resolution] Backend framework choice
7. **ADR-007:** [Post-Resolution] Session storage strategy
8. **ADR-008:** [Post-Resolution] Deployment platform
9. **ADR-009:** [Post-Resolution] Task assignment model (single vs. multiple assignees)

---

## Key Philosophy Changes

### From: Prescriptive Technology Stack
To: Technology decisions with clear rationale and alternatives

**Impact:** Team can choose appropriate technologies based on expertise and constraints, not arbitrary prescriptions.

### From: Future-Scale Infrastructure in MVP
To: MVP infrastructure only; future-scale options documented for migration

**Impact:** MVP remains simple and deployable; clear path for scaling when needed.

### From: Arbitrary Constants
To: Configuration-driven defaults with decision owners

**Impact:** Values can be tuned based on actual needs and testing; not locked in prematurely.

### From: Assumed Backend Framework
To: Framework-agnostic with per-framework guidance

**Impact:** Backend team has flexibility in framework choice; System Design adapts.

### From: Mixed Product + Implementation Details
To: Clear separation of product architecture and implementation decisions

**Impact:** Product team understands requirements; implementation team understands technical choices.

---

## Next Steps

1. **Resolve 3 Critical Decisions (Section: Unresolved Critical Decisions)**
   - [ ] Decide backend framework (impact: auth, migrations, sessions)
   - [ ] Decide session storage strategy (impact: dependencies, operations)
   - [ ] Confirm task assignment model (impact: data model)

2. **Create TECHNOLOGY_DECISIONS.md**
   - Document backend framework with justification
   - Document framework-specific implementation (auth, migrations, etc.)
   - Document deployment platform choice (if decided) or TBD status
   - Document framework selection rationale

3. **Validate & Update Domain Model**
   - [ ] Confirm task assignment (single assignee assumption)
   - [ ] Validate entity relationships
   - [ ] Confirm deletion behaviors

4. **Create Database Schema**
   - Use framework-native migration tool
   - Generate from ORM models (Django ORM, SQLAlchemy, Sequelize, etc.)
   - Include all entities from SYSTEM_DESIGN.md Part 2

5. **Begin Implementation Planning**
   - Create detailed feature breakdown
   - Estimate effort per feature
   - Plan development sprints

---

## Files Affected

| File | Change | Status |
|------|--------|--------|
| SYSTEM_DESIGN.md | Major revision, removed prescriptions, marked TBD | ✓ Updated |
| ARCHITECTURE_REVIEW.md | New file documenting issues and review findings | ✓ Created |
| TECHNOLOGY_DECISIONS.md | To be created once decisions are made | TBD |
| ADR directory | To be created for major decisions | TBD |
| Backend/requirements.txt or package.json | To be created once framework is chosen | TBD |
| Frontend/package.json | To be created with React setup | TBD |
| Database/migrations | To be created with schema | TBD |

---

