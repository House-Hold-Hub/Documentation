# Final Technology Choices - HouseHoldHub MVP

**Date:** August 16, 2026  
**Status:** Approved & Frozen (Exact Versions TBD in Project Setup)

---

## Approved Technology Stack

### Backend

| Component | Choice | Notes |
|-----------|--------|-------|
| Language | Python 3.14 | Latest stable; exact minor version TBD in pyproject.toml |
| Framework | Django 6.x | Current LTS release; compatible with Python 3.14 |
| REST API | Django REST Framework | Compatible with selected Django 6.x version |
| Database | PostgreSQL 14+ | Relational; ACID; row-level security |
| Migrations | Django migrations | Built into Django; no external tool (no Liquibase/Flyway) |
| Authentication | django.contrib.auth | Django's built-in; extended with django-allauth for OAuth |
| Sessions | django.contrib.sessions | Database-backed; no Redis required for MVP |
| Testing | pytest + pytest-django | Standard for Django projects |
| Package Manager | pip + pyproject.toml | Standard Python; modern packaging |

**Version Pinning:** Exact patch versions (e.g., Django 6.0.3, Python 3.14.2) determined during project setup in `pyproject.toml`. System Design specifies only major versions.

---

### Frontend

| Component | Choice | Notes |
|-----------|--------|-------|
| Language | TypeScript | Type-safe; large ecosystem; industry standard |
| Framework | React 19.x | Current major version; hooks-based |
| Routing | React Router v6 | Standard for React SPAs |
| State Management | TanStack Query | Server-state management; cache invalidation |
| Form Validation | React Hook Form + Zod | Runtime + static validation |
| Build Tool | Vite | Modern, fast build tool (or Rsbuild/other; TBD) |
| Package Manager | npm or pnpm | Specified in package.json |
| Testing | Jest + React Testing Library | Standard for React projects |
| UI Framework / CSS | **TBD** | Not an architectural decision; to be determined by frontend team |

**Version Pinning:** Exact versions (e.g., React 19.5.0, Vite 5.1.0) determined during project setup in `package.json`. System Design specifies only major versions.

**Note on UI Framework:** Tailwind, Material-UI, Chakra, or custom CSS/BEM are implementation details, not architecture. Frontend team chooses based on team expertise and project preferences. Not prescribed here.

---

### Development Environment

| Component | Choice | Notes |
|-----------|--------|-------|
| Containerization | Docker | Reproducible environments |
| Orchestration | Docker Compose | Local full-stack development (PostgreSQL, Django, React) |
| Version Control | Git | Standard; GitHub or other provider |
| CI/CD | **TBD** | GitHub Actions, GitLab CI, or other; chosen per infrastructure |

---

### Database

| Component | Choice | Notes |
|-----------|--------|-------|
| RDBMS | PostgreSQL 14+ | Relational; ACID; excellent Django support |
| Connection Pool | psycopg2-binary (Python driver) | Standard Django driver |
| Backups | Managed by deployment platform | Heroku, AWS RDS, DigitalOcean, etc. |
| Migrations | Django migrations | Built-in to Django; no external tools |

---

## Deployment (Platform-Neutral)

**Decision:** Application deployed as Docker containers; infrastructure platform chosen post-MVP.

**Approach:**
1. Application code is platform-agnostic
2. Docker images build from Dockerfile
3. Environment configuration via environment variables (DATABASE_URL, SECRET_KEY, etc.)
4. Deployment target (Heroku, AWS ECS, DigitalOcean App Platform, self-hosted) chosen based on:
   - Team expertise
   - Operational requirements
   - Budget constraints
   - Expected scale

**TBD Post-MVP:**
- Deployment platform (Heroku / AWS / DigitalOcean / self-hosted)
- Load balancing strategy
- Database backups and disaster recovery details
- Monitoring and observability infrastructure

---

## Explicitly NOT Included in MVP

### Intentionally Excluded
- ✗ **Redis** (optional; database sessions sufficient; can add for caching post-MVP)
- ✗ **Background worker/queue** (async task processing deferred; sync email acceptable initially)
- ✗ **WebSockets/SSE** (API-based polling sufficient; real-time sync is post-MVP)
- ✗ **Message broker** (Celery, RQ, etc. not needed)
- ✗ **Distributed tracing** (request IDs + structured logging sufficient)
- ✗ **Prometheus/Grafana** (post-MVP metrics dashboards)
- ✗ **APM tools** (DataDog, New Relic post-MVP)
- ✗ **Tailwind CSS** (UI framework is frontend implementation detail, not architecture)
- ✗ **GraphQL** (REST API sufficient; GraphQL post-MVP if needed)
- ✗ **Liquibase/Flyway** (Django migrations sufficient for Python backend)

### May Add Post-MVP
- Optional: Redis for caching and session performance optimization
- Optional: Celery or similar for async email/notifications
- Optional: WebSocket server for real-time features
- Optional: Monitoring/observability stack as scale increases
- Optional: GraphQL API alongside REST

---

## Transactional Email Strategy

**Requirement:** Invitations and authentication require transactional email (signup verification, password reset, household invitations).

**MVP Implementation:** Synchronous email sending via SMTP or managed email service (SendGrid, AWS SES, Mailgun, Heroku SendGrid add-on).

**Pattern:**
```
POST /api/v1/auth/signup
  ↓
Create User record (transaction)
  ↓
Send email (synchronous SMTP)
  ↓
Return 201 Created
```

**Trade-offs:**
- ✓ Simple implementation
- ✓ Immediate feedback to user (email sent before response)
- ✓ No infrastructure overhead (no job queue)
- ✗ API response latency tied to email provider latency (~100-500ms)
- ✗ Email provider downtime blocks user signup

**Mitigation for MVP:**
- Use managed email service with high uptime SLA (SendGrid 99.95%, AWS SES 99.9%)
- Keep email sending fast (<200ms typical)
- Catch email exceptions; fail gracefully (user signed up; email may arrive late)
- Can migrate to async queue later if email latency becomes bottleneck

**Post-MVP:** Replace with background queue (Celery, Dramatiq, etc.) if needed.

---

## Summary: What's Fixed & What's TBD

### ✓ Fixed
- Backend: Python 3.14 + Django 6.x + DRF
- Frontend: React 19.x + TypeScript + TanStack Query
- Database: PostgreSQL 14+
- Development: Docker Compose
- Deployment: Platform-neutral (TBD platform choice)
- Email: Synchronous SMTP (simple; replaceable)

### ✓ Removed from Architecture
- Tailwind CSS (UI implementation; not architecture)
- Liquibase/Flyway (Django migrations sufficient)
- Redis (optional; not required)
- Exact patch versions (belong in dependency files, not architecture)

### ⏳ TBD (To Be Determined Post-MVP or During Project Setup)
- Exact package versions (pyproject.toml, package.json)
- Frontend UI framework/CSS solution
- Deployment platform (Heroku / AWS / DigitalOcean / etc.)
- CI/CD platform (GitHub Actions / GitLab / etc.)
- Exact email service provider
- Monitoring/observability tooling
- Optional: Redis for caching
- Optional: Background worker framework

---

