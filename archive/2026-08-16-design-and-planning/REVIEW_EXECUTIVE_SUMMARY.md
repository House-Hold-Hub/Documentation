# System Design Review: Executive Summary
**Date:** August 16, 2026  
**Reviewer:** Claude Code  
**Status:** Review Complete, Revisions Applied

---

## What Was Wrong with System Design v1.0

The original System Design made prescriptive technology choices and infrastructure decisions without validating them against actual project constraints:

1. **Invented technology stack** (Node.js/Express, Winston, Flyway) without knowing the backend framework
2. **Prescribed Redis Cluster** as MVP requirement without scaling justification
3. **Contradictory deployment strategy** ("AWS ECS or Heroku" — incompatible platforms)
4. **Arbitrary operational constants** (30-day TTLs, 100 req/15min, 85% coverage) without justification
5. **Overcomplicated MVP** with infrastructure for future scaling (distributed tracing, Prometheus, async queues)
6. **Confused terminology** (last-write-wins vs. optimistic concurrency control)
7. **Backend-agnostic issues** (prescribed Django-specific and Node.js-specific tech without deciding backend)
8. **Overclaimed security** ("all attack vectors" without specific threat model)

---

## What Changed in System Design v2.0

### ✓ Core Decisions Retained (Sound)
- REST API architecture
- PostgreSQL for relational data
- Session-based authentication with HTTP-only cookies
- React + TanStack Query for frontend
- Household membership scoping
- Owner/member authorization model
- Last-write-wins concurrency

### ✗ Technology Prescriptions Removed
- Winston → Framework will choose logging solution
- Liquibase/Flyway → Framework will provide migrations
- Node.js assumptions → Backend framework TBD
- Redis Cluster → Changed to optional; single instance or database sessions sufficient

### ✗ Infrastructure Simplifications
- ✗ Redis Cluster (use single instance or database sessions)
- ✗ AWS RDS Multi-AZ (single-AZ for MVP)
- ✗ AWS ElastiCache (single instance if using Redis)
- ✗ AWS ECS (deployment platform TBD)
- ✗ Distributed tracing (request IDs sufficient)
- ✗ Prometheus/Grafana (post-MVP)

### ✗ Arbitrary Constants Removed
- 30-day session TTL → TBD configuration
- 30-day invitation expiry → TBD configuration
- 100 req/15min rate limit → TBD configuration
- All alert thresholds → TBD
- All RTO/RPO targets → TBD

### ✓ TBD Decisions Explicitly Marked
1. Backend framework (Django/FastAPI/Express/Flask?)
2. Session storage (database/single-Redis/HA?)
3. Deployment platform (Heroku/AWS/other?)
4. Task assignment model (single vs. multiple assignees?)
5. Data retention policies (14/30/90 days?)
6. Rate limiting configuration (per-IP/per-user?)

---

## Files Created/Updated

### 1. ARCHITECTURE_REVIEW.md (New)
Detailed critical review against 12 architectural principles. Identifies:
- Issues with each technology choice
- Why the choice was problematic
- Recommendation for resolution

### 2. SYSTEM_DESIGN.md (Revised)
Complete rewrite focusing on MVP architecture. Sections:

| Section | Status | Key Change |
|---------|--------|-----------|
| Part 1: Core Decisions | ✓ Kept | Validated decisions with clear rationale |
| Part 2: Domain Model | ✓ Kept | Unchanged; model is sound |
| Part 3: Auth & Sessions | ✓ Revised | Framework-agnostic; session storage TBD |
| Part 4: Authorization | ✓ Kept | Unchanged; model is clear |
| Part 5: REST API | ✓ Kept | Unchanged; endpoint design is sound |
| Part 6: Database Design | ✓ Revised | Removed Liquibase; use framework migrations |
| Part 7: Observability | ✓ Simplified | Only MVP observability (logging, correlation IDs) |
| Part 8: Development Setup | ✓ Simplified | Docker Compose; no infrastructure prescriptions |
| Part 9: Deployment | ✓ Revised | TBD; three options with tradeoffs |
| Part 10: Frontend | ✓ Revised | Technology assumed pending validation |
| Part 11: Testing | ✓ Kept | Strategy unchanged |
| Part 12: Security | ✓ Revised | Bounded claims; documented scope |
| Part 13: Data Lifecycle | ✓ Kept | Unchanged |
| Part 14: ADR Framework | ✓ Kept | Added ADRs for deferred decisions |
| Part 15: Unresolved Decisions | ✓ New | Explicit list of blockers |

### 3. SYSTEM_DESIGN_REVISION_SUMMARY.md (New)
Summary of what changed and why:
- Decisions retained (with justification)
- Decisions changed (with rationale)
- Technologies removed (with explanation)
- Unresolved decisions (with impact)
- Dependencies lists (final)
- Next steps

### 4. REVIEW_EXECUTIVE_SUMMARY.md (This File)
High-level overview of the review process and outcomes.

---

## Critical Decisions Required Before Implementation

### 1. Backend Framework
**Must decide:** Django? FastAPI? Express? Flask? Other?

**Impact:**
- Authentication implementation (use framework's built-in or custom)
- Session management (database-backed or external)
- Database migrations (Django ORM, Alembic, Knex.js, etc.)
- Testing framework and patterns
- Deployment requirements

**Recommendation:** Choose based on team expertise and project requirements, not arbitrary preference.

### 2. Session Storage Strategy
**Must decide:** Database sessions? Single Redis? Redis HA?

**Options:**
- **Database sessions:** Simple, no new dependency, slower. Best for Django.
- **Single Redis:** Fast, adds dependency, SPOF acceptable for MVP. Best for Node.js/FastAPI.
- **Redis HA/Cluster:** Overkill for MVP; use only if proven necessary by load testing.

**Recommendation:** Use framework's default initially; optimize post-MVP.

### 3. Deployment Platform
**Can be deferred** to later (optional; not a blocker).

**Options:**
- **Heroku:** Simplest, managed, ~$50-150/month for MVP
- **AWS:** More control, configurable, ~$100-300/month for MVP
- **Other:** DigitalOcean, self-hosted, etc.

**Recommendation:** Use Docker Compose for local development; decide deployment platform when ready to launch (not before).

### 4. Task Assignment Model
**Must clarify:** Can one task have multiple assignees?

**Current assumption:** Single assignee per task (simpler data model).

**Impact:**
- If single assignee: Use simple nullable `assigned_to_id` field (no TaskAssignment entity)
- If multiple assignees: Keep TaskAssignment association entity

**Recommendation:** Confirm with product team; no evidence in PRD for multi-assignment.

---

## Removed Complexity (Why Not in MVP)

### ✗ Redis Cluster
- **Reason:** MVP doesn't need HA for sessions. Use database or single Redis.
- **When to add:** If load testing shows 10k+ concurrent sessions or if availability becomes critical.
- **Cost saved:** ~$0.50-2/hour if AWS ElastiCache cluster (instead of single instance).

### ✗ Multi-AZ RDS
- **Reason:** MVP doesn't need HA for database. Single instance sufficient.
- **When to add:** If availability becomes critical after launch.
- **Cost saved:** ~$0.50-1/hour if AWS RDS with failover.

### ✗ Distributed Tracing
- **Reason:** Request IDs + structured logging are sufficient for debugging MVP.
- **When to add:** If latency becomes critical and you need span-level visibility.
- **Cost saved:** ~$0.30-1/hour if DataDog/New Relic.

### ✗ Prometheus/Grafana
- **Reason:** Application logs + basic monitoring are sufficient for MVP.
- **When to add:** Post-launch if you need metrics dashboards.
- **Cost saved:** Operational overhead (setup, maintenance, disk space).

### ✗ Async Job Queue
- **Reason:** Send emails synchronously for MVP (acceptable latency).
- **When to add:** If email sending becomes a bottleneck or needs retries.
- **Cost saved:** Infrastructure and operational complexity.

---

## Quality Improvements

### Better Separation of Concerns
- Product requirements (PRD) ← clear, stable
- Product architecture (SYSTEM_DESIGN.md) ← MVP-focused
- Technology decisions (TBD documents) ← flexible, chosen per-project
- Implementation details (Backend/Frontend) ← team-specific

### Clear Decision Ownership
Every critical decision now identifies the decision owner (TBD vs. specific team).

### Explicit Assumptions
Previously invisible assumptions are now documented and marked as TBD.

### Migration Paths
For every MVP choice, the upgrade path to production-scale is documented.

---

## What's Ready for Implementation

✓ **Product Architecture** — Core design decisions are sound  
✓ **Domain Model** — Entities and relationships defined  
✓ **Authorization Model** — Owner/member permissions clear  
✓ **API Design** — Endpoint structure and patterns defined  
✓ **Security Controls** — Scope and implementation approach documented  
✓ **Testing Strategy** — Unit, integration, authorization, E2E coverage defined  

⏳ **Not yet ready** — Waiting for critical decisions (Part 15)

---

## Next Steps (Recommended Order)

### Phase 1: Resolve Critical Decisions (1-2 days)
- [ ] Team decides on backend framework
- [ ] Team decides on session storage strategy
- [ ] Product clarifies task assignment model
- [ ] Team decides on deployment platform (or defer to pre-launch)

### Phase 2: Technology Decision Document (1 day)
- [ ] Create TECHNOLOGY_DECISIONS.md
- [ ] Document backend framework choice with justification
- [ ] Document framework-specific implementation details (auth, migrations, testing)
- [ ] Document deployment platform choice (if decided)

### Phase 3: Domain Model Validation (1 day)
- [ ] Confirm all entities and relationships
- [ ] Validate deletion behaviors
- [ ] Confirm authorization per entity

### Phase 4: Database Schema (2-3 days)
- [ ] Generate SQL schema from ORM models
- [ ] Create initial migration
- [ ] Test schema with sample data

### Phase 5: Implementation Planning (2-3 days)
- [ ] Create feature breakdown
- [ ] Estimate effort per feature
- [ ] Plan development sprints
- [ ] Create implementation task list

### Phase 6: Begin Development (Ongoing)
- [ ] Backend: Authentication + household management
- [ ] Frontend: Auth UI + household selection
- [ ] Expand to tasks, shopping, expenses, inventory in incremental sprints

---

## Key Success Metrics

### Clarity
- [ ] All critical decisions documented with rationale
- [ ] No contradictions between components (resolved)
- [ ] Clear separation of MVP vs. future features

### Simplicity
- [ ] No unnecessary infrastructure for MVP
- [ ] Deployable on single small server ($10-50/month)
- [ ] Local development with Docker Compose only
- [ ] No operational overhead for MVP

### Flexibility
- [ ] Technology choices can be swapped (React→Vue, PostgreSQL→MySQL if needed)
- [ ] Clear migration paths when scaling
- [ ] Framework-agnostic architecture design

---

## Document Map

```
HouseHoldHub/
├── tasks/
│   ├── prd-householdhub-mvp.md (Product requirements — stable)
│   └── PRD-REVISION-SUMMARY.md (Changes from PRD v1 to v2)
├── SYSTEM_DESIGN.md (v2.0 — MVP-focused architecture)
├── ARCHITECTURE_REVIEW.md (Detailed review findings)
├── SYSTEM_DESIGN_REVISION_SUMMARY.md (What changed v1→v2 and why)
├── REVIEW_EXECUTIVE_SUMMARY.md (This file)
├── TECHNOLOGY_DECISIONS.md (TBD — to be created)
├── Backend/ (TBD — implementation)
├── Frontend/ (TBD — implementation)
└── Infrastructure/ (TBD — deployment)
```

---

## Approval Checklist for Team Review

Before proceeding to implementation planning, team should confirm:

- [ ] **Product:** PRD and SYSTEM_DESIGN.md align; no changes to product scope needed
- [ ] **Backend:** Backend framework choice decided (or explicitly deferred)
- [ ] **Backend:** Session storage strategy chosen (or explicitly deferred)
- [ ] **Frontend:** Frontend framework choice confirmed (React assumed; validate)
- [ ] **DevOps:** Deployment platform approach clear (MVP + future path)
- [ ] **Domain:** Task assignment model confirmed (single assignee assumption accepted)
- [ ] **Architecture:** All critical decisions in Part 15 resolved or explicitly deferred

Once approved, proceed to Phase 1: Resolve Critical Decisions.

---

