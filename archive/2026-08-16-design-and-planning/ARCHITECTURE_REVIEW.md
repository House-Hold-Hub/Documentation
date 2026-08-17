# HouseHoldHub MVP - Critical Architecture Review
**Date:** August 16, 2026  
**Reviewer:** Claude Code  
**Status:** Issues Identified, Ready for Revision

---

## Executive Summary

The System Design document introduces prescriptive technology choices and infrastructure requirements without validating them against actual project constraints. This review identifies decisions that were invented without justification, marks unresolved decisions explicitly, removes unnecessary complexity, and separates MVP requirements from future-evolution options.

**Key Findings:**
- ✗ Technology stack prescribed without repository validation
- ✗ Redis cluster required for MVP without scaling justification
- ✗ Dual deployment platforms (AWS ECS + Heroku) without commitment to either
- ✗ Arbitrary operational constants (30-day TTL, 100 req/15min, 85% coverage) without justification
- ✗ Complex observability stack (Prometheus, Grafana, DataDog) for MVP
- ✗ Idempotency keys and distributed tracing not required for MVP
- ✗ Backend framework (Django vs. Express vs. other) not specified
- ✓ Core product architecture (REST, PostgreSQL, session auth) is sound
- ✓ Authorization model (household isolation, owner/member permissions) is correct

---

## Review Against 12 Architectural Principles

### 1. Technology Stack Validation

**Finding:** The System Design prescribes a technology stack without validating against actual repository decisions or constraints.

**Issues:**
- Backend framework not specified (Django/Python? Node.js/Express? FastAPI? Flask?)
- React/TypeScript frontend assumed but not documented as a decision
- Prescribes Winston for Node.js logging (appropriate IF backend is Node; not if Python)
- Prescribes Liquibase/Flyway for migrations (should be Django ORM if Django backend)
- No validation that these choices exist in the repository or have been decided

**What's Invented:**
- Winston as logging framework
- Liquibase/Flyway as migration tools
- Specific npm/Node.js tooling assumptions
- Frontend architecture (React Router, React Hook Form, Zod, Tailwind CSS)

**What's Missing:**
- Documentation of actual backend language/framework
- Documentation of actual frontend framework decisions
- Validation against repository setup

**Action Required:**
Before prescribing technology, document:
1. What backend framework has been chosen or should be chosen?
2. What is the current backend repository state?
3. What frontend framework has been chosen?
4. Which of these choices are already committed vs. TBD?

**Recommendation:**
Create a TECHNOLOGY_DECISIONS.md file documenting:
- Backend framework (with justification if not yet chosen)
- Frontend framework (with justification if not yet chosen)
- Database (PostgreSQL is sound, document the decision)
- Session storage (TBD pending scaling analysis)

---

### 2. Redis as an MVP Dependency

**Finding:** Redis cluster is prescribed as required for session storage without justifying the complexity against MVP requirements.

**Issues:**
- Session-based authentication with HTTP-only cookies is correct
- But Redis cluster is not the only way to achieve this
- No comparison of alternatives: Django/database sessions vs. single Redis vs. Redis HA vs. cluster
- "Redis Cluster for high availability" assumes MVP requires HA without stating the requirement
- Redis Cluster adds operational complexity (cluster management, failover, monitoring)
- Single machine deployment (Heroku, small AWS instance) does not benefit from cluster

**Alternatives Not Evaluated:**
1. **Database-backed sessions (if Django):** Django ORM sessions table, no new dependency
2. **Single Redis instance:** Works for MVP-scale, simpler than cluster, easier to deploy
3. **In-memory sessions (if Heroku):** Works for single-dyno deployments
4. **AWS ElastiCache single node:** Works for low-scale, auto-failover built-in
5. **No sessions (stateless JWT):** Already rejected but not reconsidered per scaling needs

**Migration Path Missing:**
- How to move from single Redis to cluster as load increases
- When cluster becomes necessary vs. when it should be pre-built for MVP

**Action Required:**
Document the session storage decision WITH scaling constraints:
1. What is the target concurrent users for MVP? (10, 100, 1000?)
2. What is the target session count?
3. Do we need HA for MVP or is single-instance acceptable?
4. What is the migration path if we start simple?

**Recommendation:**
- **For MVP:** Single Redis instance (or database sessions if Django) unless explicitly scaling to 10k+ concurrent users
- **Note:** If Django backend, prefer Django ORM sessions (comes free) unless performance testing shows Redis is necessary
- **For production:** Evaluate Redis cluster/AWS ElastiCache at scale, not at MVP

---

### 3. Deployment Architecture

**Finding:** "AWS ECS or Heroku" is not a decision; it's two incompatible platforms presented as equal options.

**Issues:**
- Heroku and AWS ECS require different infrastructure (Procfile vs. Dockerfile vs. ECS task definitions)
- Secrets management differs (Heroku config vars vs. AWS Secrets Manager)
- Database differs (Heroku Postgres vs. AWS RDS)
- Cost and operational model incompatible
- System Design assumes AWS throughout (RDS, ElastiCache, ECS, Secrets Manager, load balancer)
- Then casually mentions Heroku as alternative without explaining the incompatibility

**What's Assumed:**
- AWS RDS for PostgreSQL (requires AWS account, managed instance)
- AWS ElastiCache for Redis (requires AWS account)
- AWS ECS for container orchestration
- AWS Secrets Manager
- Multi-AZ deployment
- Load balancer

**What's NOT Decided:**
- Is AWS the infrastructure platform or is it Heroku?
- Is the MVP self-hosted or on a PaaS?
- What is the deployment target for development?

**Action Required:**
Make an explicit decision:

**Option A: Heroku (simplest for MVP)**
- Frontend: Heroku dyno or Netlify/Vercel
- Backend: Heroku dyno
- Database: Heroku Postgres (built-in)
- Sessions: Heroku Redis add-on (built-in) OR database sessions
- Email: SendGrid add-on
- Cost: ~$50-150/month for MVP
- Operational overhead: Minimal
- Infrastructure: Managed by Heroku

**Option B: AWS (more control, more work)**
- Frontend: CloudFront + S3 (or EC2/ECS)
- Backend: ECS Fargate (or EC2)
- Database: RDS PostgreSQL
- Sessions: ElastiCache OR RDS
- Email: SES
- Cost: ~$100-300/month for MVP (before volume discounts)
- Operational overhead: Moderate (IAM, security groups, monitoring, backups)
- Infrastructure: User manages

**Option C: Docker Compose locally, TBD for MVP deployment**
- Development: Docker Compose (PostgreSQL, Redis, backend, frontend)
- MVP deployment: TBD (decision deferred until ready to ship)
- This removes infrastructure prescriptions from System Design

**Recommendation:**
Choose ONE of the above. The revision should state:

> **Deployment Decision: [OPTION A/B/C — TBD Pending Actual Infrastructure Commitment]**
>
> For MVP development and testing:
> - Docker Compose with PostgreSQL, Redis (single instance), and application services
> - Deployable to any standard Docker host
>
> For MVP production (TBD):
> - Decision deferred to Infrastructure team
> - Options: Heroku (simplest), AWS (more control), DigitalOcean, self-hosted, etc.
> - Infrastructure specification and cost analysis required before commitment

---

### 4. Concurrency Model Clarity

**Finding:** "Last-write-wins with timestamps" conflates two different patterns; the terminology obscures whether conflict detection is happening.

**Issues:**
- **Pure last-write-wins:** Accept all writes, return 200, no conflict detection → data loss on simultaneous edits
- **Optimistic concurrency control:** Client includes timestamp, server rejects if mismatch, return 409 → no data loss
- System Design says "last-write-wins" but then describes returning 409 Conflict if timestamp doesn't match → that's optimistic concurrency control, not last-write-wins

**What's Actually Prescribed:**
```
Client includes updated_at in PATCH/PUT
Server checks timestamp
If mismatch: return 409 Conflict (ask client to refetch)
OR accept latest write unconditionally
```

This is the definition of optimistic concurrency control.

**What's Unclear:**
- Which option is chosen? (409 Conflict vs. accept all?)
- When should we reject vs. accept?
- Is conflict detection actually necessary for MVP domains?

**Per-Domain Analysis:**

| Entity | Concurrent Edits Likely? | Risk | Recommendation |
|--------|---------------------------|------|-----------------|
| Task title/description | Low | Minor; task updated correctly | Accept latest write |
| Task assignment | Low | Very unlikely; one member at a time | Accept latest write |
| Expense amount | Low | Unlikely; expense immutable once payer set | Accept latest write |
| Shopping item quantity | Medium | Possible; multiple people marking purchased | Detect conflict, ask for refetch |
| Inventory quantity | Medium | Possible; multiple people incrementing/decrementing | Detect conflict, ask for refetch |

**Action Required:**
Document concurrency handling per entity:
1. Which entities need conflict detection?
2. For detected conflicts, what's the user experience? (reload page? show dialog?)
3. Is optimistic locking necessary or can we accept simpler patterns?

**Recommendation:**
- **For MVP:** Accept last-write-wins for most domains (simplest)
- **Rationale:** Household members are trusted, conflicts are rare, refetch on page focus mitigates stale data
- **For shopping/inventory:** If concurrent edits of quantities are a concern, add version checking and return 409 on conflict
- **Future:** Implement conflict resolution UI post-MVP if user testing shows need

---

### 5. Arbitrary Operational Constants

**Finding:** The System Design introduces numerous hardcoded values without justification.

**Examples:**
- 30-day session TTL (why 30? why not 7, 14, 90?)
- 30-day invitation expiry (why 30?)
- 30-day household deletion retention (why 30?)
- 100 requests / 15 minutes rate limit (why 100? why 15 min?)
- Password length 10 characters (arbitrary)
- Alert thresholds (error rate >5%, latency >2s, DB query >1s)
- RTO/RPO targets (1 hour RTO, 1 day RPO)
- Coverage goals (85%+)
- bcrypt cost=12 (reasonable but should document alternatives)

**Why This Matters:**
- Operational decisions need justification or should be deferred
- These values will be questioned during implementation and testing
- Premature specificity prevents flexibility

**Action Required:**
For each constant, document:
1. Where does this value come from?
2. What requirement justifies it?
3. Is this MVP-blocking or post-MVP refinement?
4. Who makes the final decision?

**Recommendation:**
Replace arbitrary constants with:
- **Product requirements:** Session duration must be long enough to avoid frequent re-login (TBD based on user testing)
- **Operational decisions:** Defer to operations/infrastructure team with business requirements
- **Technical decisions:** Use safe defaults; can be tuned post-MVP

Example revision:
> **Session TTL:** Configuration parameter (default: 30 days, configurable via environment variable). Reviewed post-MVP based on user behavior and security requirements.

---

### 6. Backend Framework Alignment

**Finding:** System Design assumes specific authentication/session implementation without knowing the backend framework.

**Issues:**
- If backend is Django: Use Django built-in auth and session framework (free, tested, secure)
- If backend is Express: Use express-session with memory/Redis store (good)
- If backend is Flask: Use Flask-Login with session management (good)
- If backend is FastAPI: Use starlette sessions with memory/Redis (good)

**Current Problem:**
- Design specifies "server-side sessions in Redis" generically
- Doesn't leverage framework-specific solutions (e.g., Django's excellent auth system)
- Prescribes implementation details (bcrypt cost=12, Argon2, token hashing) that frameworks may handle

**Action Required:**
Document the backend framework decision first, then align authentication design with framework capabilities.

**Recommendation:**
1. Decide on backend framework (Django, FastAPI, Express, Flask, etc.)
2. Leverage framework's built-in auth/session capabilities
3. Customize only where framework doesn't provide
4. Example for Django:
   > Use Django's built-in `django.contrib.auth` for authentication. Sessions stored in Redis via django-redis (django-cache-framework). Override password validators to match security requirements.

---

### 7. MVP Infrastructure Simplification (YAGNI)

**Finding:** The System Design includes infrastructure and operational tools that are not required for MVP.

**Tools/Components Not Required for MVP:**

| Component | Purpose | MVP Need? | Recommendation |
|-----------|---------|-----------|-----------------|
| Redis Cluster | Session HA | ✗ | Use single instance or database sessions |
| AWS RDS Multi-AZ | High availability | ✗ | Single-AZ for MVP; upgrade post-launch |
| ElastiCache | Session HA | ✗ | Single Redis instance or skip Redis |
| Prometheus | Metrics collection | ✗ | Log to stdout, use application logs |
| Grafana | Metrics visualization | ✗ | Defer to post-MVP monitoring |
| DataDog | APM + monitoring | ✗ | Use free tier or defer |
| New Relic | APM + monitoring | ✗ | Defer or use application logs |
| Distributed tracing | Request correlation | ✗ | Simple request IDs + logging sufficient |
| Asynchronous job queue | Background tasks | ✗ | Send emails synchronously for MVP |
| Idempotency keys | Duplicate submission handling | ✗ | Use standard POST/redirect/GET pattern |
| Liquibase/Flyway | Database migrations | ✗ | Use framework (Django ORM, Alembic, etc.) |

**What's Sufficient for MVP:**
- Application logs to stdout (stdout captured by Docker/Heroku/ECS)
- PostgreSQL single instance (managed or local)
- Redis single instance (optional; use database sessions if not scaling)
- Simple error tracking (Sentry has free tier)
- No distributed tracing needed
- No APM needed
- Standard POST/redirect/GET for form handling (no idempotency keys needed)

**Action Required:**
Remove all "future scaling" infrastructure from MVP System Design. Create a separate "Post-MVP Evolution" section for:
- Scaling from single Redis to cluster
- Adding Prometheus/Grafana
- Adding distributed tracing
- Asynchronous email queue
- etc.

**Recommendation:**
MVP deployment should be deployable on:
- Single small server (Heroku standard dyno)
- Single small AWS instance ($10-50/month)
- Docker Compose on developer laptop

---

### 8. Observability Terminology Correction

**Finding:** The design conflates correlation IDs with distributed tracing; uses imprecise terminology.

**Issues:**
- Request IDs (correlation IDs) are NOT distributed tracing
- Distributed tracing requires instrumentation of every service and time-series recording
- Request IDs alone are just for log correlation
- The design oversells observability capability

**Correct Terminology:**

| Term | What It Is | MVP Need? |
|------|-----------|-----------|
| **Correlation ID / Request ID** | A UUID added to each request, propagated through logs | ✓ Yes |
| **Structured Logging** | JSON logs with context (user_id, household_id, operation) | ✓ Yes |
| **Metrics** | Counters, gauges, histograms (requests, errors, latency) | ✗ Post-MVP |
| **Distributed Tracing** | Instrumented spans across services with timing | ✗ Post-MVP |
| **Application Performance Monitoring (APM)** | Tracing + metrics + profiling with dashboard | ✗ Post-MVP |

**What MVP Actually Needs:**
1. Structured JSON logs to stdout
2. Request ID in all logs
3. Timestamp, level, message, context fields
4. Error stack traces in logs
5. Basic error tracking (Sentry free tier)

**Example Sufficient MVP Logging:**
```json
{"timestamp":"2026-08-16T10:30:45Z","request_id":"abc123","level":"INFO","user_id":"user456","household_id":"hh789","operation":"create_task","duration_ms":45,"status":201}
{"timestamp":"2026-08-16T10:30:46Z","request_id":"def456","level":"ERROR","user_id":"user789","error":"household_not_found","status":404}
```

**Action Required:**
Revise Section 12 (Observability) to describe only MVP-necessary observability.

---

### 9. Idempotency Requirements Reassessment

**Finding:** System Design requires idempotency keys for "critical operations" without identifying which operations genuinely need them.

**Issues:**
- Idempotency keys are useful for operations with side effects that might be retried (payments, external API calls)
- Standard CREATE operations don't need idempotency keys if you use POST (create) → GET (verify) pattern
- Household/Task/Expense creation are not operations with external side effects in MVP (email is async)
- Prescribing idempotency adds complexity (cache management, key generation)

**Which Operations Genuinely Need Idempotency?**
- **Invitation emails:** Yes (if a network error causes retry, we don't want duplicate emails)
- **Password reset emails:** Yes (same reason)
- **Task creation:** No (client can verify creation via subsequent GET request)
- **Expense creation:** No (same reason)

**MVP Sufficient Pattern:**
- POST creates resource, returns 201 with Location header
- Client remembers resource ID
- If client retries (due to network error), POST creates a duplicate
- Client polls GET to find the correct resource
- Or use idempotency key only for email-sending operations

**Action Required:**
Identify which operations genuinely have side effects requiring idempotency.

**Recommendation:**
Implement idempotency keys only for:
- Sending invitation emails (prevent duplicate emails on retry)
- Sending password reset emails (prevent duplicate emails on retry)
All other operations use standard POST/redirect/GET pattern.

---

### 10. Domain Model Validation

**Finding:** The domain model includes TaskAssignment as a separate entity; need to validate whether it's necessary for MVP.

**Issues:**
- PRD says tasks can be "assigned to specific members"
- Doesn't specify: one assignee per task or multiple assignees?
- Current design assumes TaskAssignment association entity (many-to-many)
- If only one assignee per task, a simple nullable `assigned_to_id` is simpler

**Task Assignment Analysis:**
- PRD FR-29: "Assigned members can mark their own assigned tasks as complete"
- PRD FR-32: "Household Owner can mark any task as complete"
- Current design: `TaskAssignment.completed` per assignment

**Two Possible Models:**

**Option A (Current): Multiple Assignees per Task**
```sql
Task: id, household_id, title, description, created_by_id, created_at
TaskAssignment: id, task_id, assigned_to_id, completed, completed_at
```
- Supports assigning one task to multiple people
- More flexible for future features
- More complex for MVP UI

**Option B (Simpler): One Assignee per Task**
```sql
Task: id, household_id, title, description, assigned_to_id, completed, completed_by_id, completed_at, created_by_id
```
- Supports assigning one task to one person
- Simple data model
- Simple UI
- No separate entity needed

**Decision from PRD:**
Looking back at PRD and user requirements, there's no explicit requirement for assigning one task to multiple people. Example workflow shows single assignment: "Task assignment to specific members."

**Action Required:**
Clarify: Can one task be assigned to multiple household members simultaneously?
- If NO: Use Option B (simpler model, no TaskAssignment entity)
- If YES: Use Option A (keep TaskAssignment entity)

**Recommendation:**
For MVP, assume one assignee per task (Option B) unless explicitly stated otherwise. This simplifies:
- Data model (no separate entity)
- UI (single "assigned to" dropdown)
- Queries (no join needed)
- Completion tracking (binary complete/not complete per task)

Supports future multi-assignment in post-MVP iteration.

---

### 11. Security Claims Overclaimed

**Finding:** System Design claims "security controls for all attack vectors" without specific threat modeling.

**Issues:**
- Implies exhaustive security coverage (unrealistic)
- No threat model documented
- No risk assessment
- Some mitigations are generic or overstated

**What's Documented (Good):**
- CSRF protection (tokens)
- XSS protection (HTTP-only cookies)
- SQL injection prevention (parameterized queries)
- Rate limiting (specific endpoints)
- Password hashing (bcrypt/Argon2)
- Secure cookies (flags)

**What's Missing:**
- Threat model (who attacks? what do they want?)
- Risk assessment (which threats are most likely?)
- Risk acceptance (what threats are we accepting for MVP?)
- External service risks (Google OAuth, email service, hosting provider)

**Action Required:**
Document only what's actually implemented. Remove overclaims.

**Recommendation:**
Replace "security controls for all attack vectors" with specific, bounded claims:

> **Implemented Security Controls:**
> - CSRF: Tokens validated on state-changing requests
> - XSS: HTTP-only cookies, framework auto-escaping
> - SQL Injection: Parameterized queries, ORM (if used)
> - Authentication: Email/password (bcrypt), Google OAuth, session-based
> - Authorization: Membership checks at route level, household isolation at query level
> - Rate limiting: 5 login attempts/minute per IP
> - Secrets: Environment variables, no committed credentials
>
> **Not Implemented (Post-MVP):**
> - Audit logging for all data access
> - API key management / OAuth for third parties
> - Advanced threat detection
> - Security scanning / penetration testing
> - DDoS protection

---

### 12. MVP vs. Future Evolution Separation

**Finding:** MVP components not clearly separated from future-evolution components.

**Issues:**
- Redis Cluster prescribed as MVP requirement when single instance would suffice
- RDS Multi-AZ prescribed when single-AZ is acceptable
- Distributed tracing mentioned as MVP observability
- Extensive monitoring infrastructure mentioned as MVP
- Difficult to distinguish what's required for launch vs. what's nice-to-have

**Action Required:**
For every major component, clearly state:
1. **Required for MVP:** Must have before launch
2. **Optional/Configurable:** Can be added without breaking architecture
3. **Future Scaling:** Post-MVP evolution when load requires it
4. **TBD:** Not decided yet; requires decision before implementation

**Example Classification:**

| Component | MVP Status | Notes |
|-----------|-----------|-------|
| PostgreSQL | Required | Core data storage |
| Redis | Optional | Can use DB sessions instead |
| Docker | Required | Containerization for deployment |
| AWS/Heroku | TBD | Deployment platform not yet decided |
| Prometheus | Future | Post-MVP monitoring |
| Grafana | Future | Post-MVP dashboards |
| DataDog | Future | Post-MVP APM |
| Distributed Tracing | Future | Post-MVP observability |
| Async Job Queue | Future | Post-MVP for email/notifications |
| Rate Limiting Middleware | Required | Protects auth endpoints |
| Structured Logging | Required | Essential for debugging |
| Request IDs | Required | Essential for correlation |

---

## Summary of Issues by Severity

### Critical Issues (Block Implementation)
1. Backend framework not specified → can't choose authentication/session approach
2. Deployment platform not decided (AWS vs. Heroku vs. TBD) → contradictory infrastructure prescriptions
3. Session storage complexity not justified (Redis cluster vs. single vs. database sessions)

### Major Issues (Incorrect/Overcomplicated)
4. Concurrency model terminology incorrect (last-write-wins vs. optimistic locking)
5. Arbitrary constants without justification (30-day TTLs, rate limits, RTO/RPO)
6. Idempotency required for operations that don't need it
7. Observability overstated (distributed tracing, APM for MVP)
8. Domain model validation incomplete (TaskAssignment necessity unclear)

### Minor Issues (Clarifications Needed)
9. Technology choices not validated against framework decisions
10. Infrastructure components not classified as MVP/Optional/Future
11. Security claims overclaimed ("all attack vectors")

---

## Recommended Action Plan

### Phase 1: Foundational Decisions (Before Revision)
- [ ] Document backend framework choice (Django/FastAPI/Express/etc.)
- [ ] Decide deployment platform (Heroku / AWS / TBD)
- [ ] Document session storage choice (Django sessions / single Redis / skip Redis)
- [ ] Clarify single vs. multiple assignees per task

### Phase 2: Simplify for MVP
- [ ] Remove "future scaling" infrastructure (cluster, multi-AZ, distributed tracing)
- [ ] Remove arbitrary constants; replace with configuration + decisions
- [ ] Remove unnecessary components (Liquibase/Flyway, async queue, idempotency)
- [ ] Clarify concurrency handling per entity

### Phase 3: Revise System Design
- [ ] Create TECHNOLOGY_DECISIONS.md documenting framework choices
- [ ] Revise SYSTEM_DESIGN.md to be MVP-focused, mark TBD items
- [ ] Add "Post-MVP Evolution" section for future scaling
- [ ] Separate required vs. optional infrastructure

---

