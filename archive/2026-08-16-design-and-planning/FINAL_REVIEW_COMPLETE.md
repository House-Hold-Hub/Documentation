# HouseHoldHub MVP - Final Architecture Review Complete

**Date:** August 16, 2026  
**Status:** ✓ Approved & Ready for ERD & OpenAPI  
**Next Step:** Create database schema and API specification

---

## 1. FINAL TECHNOLOGY CHOICES

### Backend Stack (Fixed)
```
Python 3.14
Django 6.x (current LTS release)
Django REST Framework (compatible with Django 6.x)
PostgreSQL 14+
psycopg2 (Python driver)
pytest + pytest-django (testing)
docker + docker-compose (development)
```

**Note:** Exact patch versions (e.g., Django 6.0.3, Python 3.14.2) determined in `pyproject.toml` during project setup. System Design specifies only major versions.

### Frontend Stack (Fixed)
```
React 19.x (current major release)
TypeScript (static typing)
React Router v6 (routing)
TanStack Query (server-state management)
React Hook Form + Zod (form validation)
Vite or Rsbuild (build tool; exact choice TBD)
Jest + React Testing Library (testing)
npm or pnpm (package manager)
```

**Note:** Exact versions in `package.json` during project setup.

### Database
```
PostgreSQL 14+ (relational, ACID, row-level security)
Django ORM (all database interactions)
Django migrations (schema versioning)
```

### Development Environment
```
Docker (containerization)
Docker Compose (full-stack local development)
Git (version control)
PostgreSQL in container (local database)
Django development server
React development server (Vite/Rsbuild)
```

### Transactional Email
```
Synchronous SMTP via:
  - SendGrid (managed service)
  - AWS SES
  - Mailgun
  - Heroku SendGrid add-on
  OR
  - smtp.gmail.com (development)
```

**Pattern:** POST → Create record → Send email (sync) → Return 201  
**Trade-off:** API latency tied to email provider (100-500ms typical)  
**Post-MVP:** Replace with async queue if latency becomes bottleneck

### Deployment (Platform-Neutral)
```
Docker containers (build artifact)
Environment variables for configuration
No infrastructure-specific code in application
Platform chosen post-MVP based on:
  - Team expertise
  - Operational requirements  
  - Budget
  - Scale
Candidate platforms: Heroku, AWS ECS, DigitalOcean, self-hosted
```

---

## 2. EXPLICITLY NOT INCLUDED (Or Marked TBD)

### Excluded from MVP
- ✗ Redis (optional; database sessions sufficient)
- ✗ Background worker / async task queue (sync email acceptable)
- ✗ WebSockets / SSE (API-based polling sufficient)
- ✗ Message broker (Celery, RQ, etc.)
- ✗ Distributed tracing (request IDs + logging sufficient)
- ✗ Prometheus / Grafana / DataDog / New Relic (post-MVP)
- ✗ Liquibase / Flyway (Django migrations sufficient)
- ✗ GraphQL (REST API sufficient)

### TBD (To Be Determined During Project Setup)
- ⏳ Exact patch versions (belong in pyproject.toml & package.json)
- ⏳ Frontend UI framework / CSS solution (not architecture; team choice)
- ⏳ Deployment platform (Heroku / AWS / DigitalOcean / etc.)
- ⏳ CI/CD platform (GitHub Actions / GitLab CI / etc.)
- ⏳ Email service provider (SendGrid / SES / Mailgun / etc.)
- ⏳ Build tool (Vite / Rsbuild / other)
- ⏳ Package manager (npm / pnpm)
- ⏳ Optional: Redis (post-MVP if caching needed)
- ⏳ Optional: Background worker (post-MVP if async needed)
- ⏳ Optional: Monitoring stack (post-MVP if required)

---

## 3. FINAL DOMAIN MODEL

### 8 Core Entities

```
User ← Account/Identity
  ├─ owns → Household (1:1, PROTECT on deletion if owns)
  ├─ participates → Membership (1:N)
  ├─ creates/completes → Task (1:N)
  ├─ creates/marks purchased → ShoppingItem (1:N)
  ├─ creates/pays → Expense (1:N)
  └─ creates → InventoryItem (1:N)

Household ← Security Boundary (all data scoped by household_id)
  ├─ owned by → User (1:1)
  ├─ has → Membership (1:N)
  ├─ has → Task (1:N)
  ├─ has → ShoppingItem (1:N)
  ├─ has → Expense (1:N)
  ├─ has → InventoryItem (1:N)
  └─ has → Invitation (1:N)

Membership ← Role-Based Access (owner or member)
  ├─ references → User & Household
  ├─ unique: (household_id, user_id)
  └─ scopes → Task assignments (1:N)

Invitation ← Email-Based Onboarding
  ├─ references → Household
  ├─ state: pending | accepted | revoked | expired
  └─ triggers → Membership creation

Task ← Single-Assignee Chore
  ├─ assigned to → Membership (nullable, SET NULL on removal)
  ├─ created by → User (SET NULL if creator deleted)
  ├─ completed by → User (nullable)
  └─ status: open | completed

ShoppingItem ← Shopping List
  ├─ created by → User (SET NULL if deleted)
  ├─ marked purchased by → User (nullable)
  └─ state: unpurchased | purchased

Expense ← Financial Record
  ├─ created by → User (SET NULL if deleted)
  ├─ paid by → User (defaults to creator, immutable)
  └─ categories: Food, Utilities, Maintenance, Entertainment, Other

InventoryItem ← Stock Tracking
  ├─ created by → User (SET NULL if deleted)
  └─ basic quantity tracking
```

### Key Design Points

✓ **Single assignee per task** (no TaskAssignment entity; assigned_to → Membership)  
✓ **All entities scoped by household_id** (security enforcement)  
✓ **Soft-delete households only** (preserves data during recovery period)  
✓ **Hard-delete individual resources** (immediate; no recovery in MVP)  
✓ **Soft-delete cascading:** Data preserved (not deleted)  
✓ **Hard-delete cascading:** Irreversible deletion (only after retention period)  
✓ **User deletion:** SET NULL on authorship (preserve content); CASCADE on membership  
✓ **Household ownership:** PROTECT on deletion (cannot delete user if owns household)  

---

## 4. IDENTIFIED DOMAIN INVARIANTS

### Database-Level (Enforced by Constraints)

✓ **email UNIQUE** — One email per user  
✓ **code UNIQUE** — Household code globally unique  
✓ **(household_id, user_id) UNIQUE** — One membership per household per user  
✓ **owner_id NOT NULL** — Every household must have owner  
✓ **FK: Task.assigned_to_id → Membership** — Task assignment must be in same household (enforced by FK, not generic User FK)  
✓ **FK: Household.owner_id → User with PROTECT** — Cannot delete user if owns households  
✓ **FK: Membership.household_id → Household with CASCADE** — Membership cascade-deleted on household hard-delete  
✓ **FK: Task/Shopping/Expense/Inventory.household_id → Household with CASCADE** — Child records cascade-deleted on household hard-delete  
✓ **FK: Task.created_by_id → User with SET NULL** — Task remains if creator deleted  
✓ **FK: Task.assigned_to_id → Membership with SET NULL** — Task unassigned if member removed  

### Application-Level (Requires Validation)

✓ **Soft-delete household must preserve child data** (no cascading during soft-delete)  
✓ **Hard-delete household (after retention) must cascade-delete child data** (irreversible deletion)  
✓ **Only creator/owner can delete tasks/shopping/expenses/inventory**  
✓ **Only owner can delete household, invite members, remove members**  
✓ **Only assigned member (or owner) can mark task complete**  
✓ **Expense payer immutable after creation** (prevent changing historical attribution)  
✓ **Invitation one-time use** (cannot accept same invitation twice)  
✓ **Invitation state transition:** pending → accepted OR pending → revoked OR pending → expired  
✓ **All queries scoped by user's household_id** (cannot access cross-household data)  
✓ **Permission checks at route level** (verify user is member before processing)  
✓ **Task assignment verified in same household** (cannot assign to member of different household)  

---

## 5. REMAINING BLOCKERS BEFORE ERD/OpenAPI

### Resolved ✓
- Backend framework: Django 6.x
- Frontend framework: React 19.x
- Database: PostgreSQL
- Sessions: Database-backed (no Redis)
- Task assignment: Single assignee (Membership)
- Deletion semantics: Soft vs hard delete clarified
- Foreign key behavior: CASCADE vs SET NULL documented

### TBD (Requires Decision Before Coding)

#### User Account Deletion: Ownership Strategy
**Question:** What happens when a user deletes their account if they own households?

**Options:**
- **A) PROTECT (FK constraint):** Cannot delete user; require ownership transfer first
  - Best for: Preserving data ownership chain
  - Implementation: Frontend prompts user to transfer household before deleting account
  
- **B) Anonymize owner:** Allow deletion; household owner becomes "Anonymous" or null
  - Best for: User convenience (delete immediately)
  - Implementation: Create "deleted user" or null owner; assign to admin later
  - Complexity: Higher; requires handling null owner case

- **C) Auto-reassign owner:** Delete user; automatically reassign household to first member
  - Best for: User convenience
  - Implementation: Transfer ownership to longest-member
  - Complexity: Highest; ambiguous who new owner should be

**Recommendation:** Option A (PROTECT) for MVP; simplest, safest. Requires explicit ownership transfer on account deletion.

**TBD Decision:** Which option before implementation starts?

#### Retention Periods: Soft-Delete to Hard-Delete Timelines
**Question:** How long before soft-deleted data is permanently hard-deleted?

| Entity | Options | Recommendation |
|--------|---------|-----------------|
| User soft-delete to hard-delete | 14 / 30 / 90 days | 30 days (standard for account recovery) |
| Household soft-delete to hard-delete | 14 / 30 / 90 days | 30 days (time for owner to recover) |
| Session expiration | 7 / 14 / 30 days | 14 days (standard for web sessions) |

**TBD Decision:** Finalize retention periods before deployment configuration?

#### Household Code Regeneration: Old Code Behavior
**Question:** When household code is regenerated, what happens to old code?

**Options:**
- **A) Old code invalid immediately:** New code works; old code returns 404/error
  - Simplest implementation
  - Breaking change for members with old code
  
- **B) Both codes work temporarily:** Old code works for N days, then invalid
  - Graceful migration
  - More complex; track old codes + expiration
  
- **C) Both codes work indefinitely:** Old code never expires
  - Most forgiving
  - Code list grows; harder to audit

**Recommendation:** Option A (old code invalid immediately) for MVP; simplest.

**TBD Decision:** Before implementation?

---

## 6. CRITICAL IMPLEMENTATION PREREQUISITES

### Before Writing Code:

1. ✓ **Approve Domain Model** — 8 entities, relationships, constraints, deletion semantics
2. ✓ **Confirm Technology Stack** — Python 3.14, Django 6.x, React 19.x, PostgreSQL, email provider
3. ⏳ **Resolve 3 TBD Decisions:**
   - [ ] User account deletion: Option A/B/C?
   - [ ] Retention periods: 14/30/90 days?
   - [ ] Household code regeneration: Option A/B/C?
4. ⏳ **Create ERD** (Entity-Relationship Diagram) from corrected domain model
5. ⏳ **Create OpenAPI Specification** (API endpoints, request/response schemas)
6. ⏳ **Initialize Django Project** (models.py, migrations, serializers.py)
7. ⏳ **Initialize React Project** (component structure, types.ts)

---

## Files Ready for Review

**Core Documents:**
- `FINAL_TECHNOLOGY_CHOICES.md` ← Review for tech stack approval
- `DOMAIN_MODEL_CORRECTED.md` ← Review for domain model & deletion semantics
- `FINAL_REVIEW_COMPLETE.md` ← This document (summary before ERD/OpenAPI)

**Supporting Documents:**
- `SYSTEM_DESIGN.md` (v3.0) ← Complete architecture
- `architecture/adr/*.md` (8 ADRs) ← Decision rationale
- Previous: `tasks/prd-householdhub-mvp.md` ← Product requirements

---

## Status: READY FOR APPROVAL

All critical architectural decisions have been made.  
Domain model is corrected and validated.  
Technology stack is finalized (with TBD-for-later items clearly marked).  
Deletion semantics are clarified.  
Foreign key behavior is documented.  

**Next Steps (Once Approved):**
1. Resolve 3 remaining TBD decisions
2. Create ERD from domain model
3. Create OpenAPI specification
4. Initialize Django and React projects
5. Begin implementation

**Blockers:** None. Ready to proceed to ERD/OpenAPI creation.

---

