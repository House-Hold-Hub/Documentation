# HouseHoldHub technology baseline

> **Status:** Accepted  
> **Owner:** Documentation repository; Backend, Frontend, Infrastructure, and Automation review their respective sections  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Approved technology families, toolchain boundaries, and version ownership  
> **Supersedes:** The archived [technology-choice](../archive/2026-08-16-design-and-planning/FINAL_TECHNOLOGY_CHOICES.md) and [system-design](../archive/2026-08-16-design-and-planning/SYSTEM_DESIGN.md) snapshots

## Authority and version policy

This document records approved technology families and architectural constraints. It does not pin exact patch or transitive dependency versions.

- Backend manifests and their lockfiles own actual Python and backend dependency versions.
- `package.json` and its committed npm lockfile own actual frontend package versions.
- Infrastructure runtime configuration owns deployed service and PostgreSQL versions.
- Repository code and configuration must remain within the compatible ranges recorded here.
- Deferred decision D06 must be resolved at the approved scaffold/evidence stages for exact packages, tools, and indexes not already fixed by this baseline.

Where an old architecture document, example, or ADR dependency snippet differs from a current manifest, the manifest is authoritative for the installed version. A durable change to the technology family or approved major/runtime baseline still requires an ADR.

## Backend

| Concern | Approved baseline | Boundary |
|---|---|---|
| Language runtime | Python 3.14 | Exact patch comes from backend runtime/dependency configuration |
| Web framework | Django 5.2 LTS | Supersedes the Django 4.2 portion of ADR-002; see [ADR-010](adr/ADR-010-backend-runtime-baseline.md) |
| REST framework | Django REST Framework | Exact compatible version belongs to backend manifests |
| Authentication integration | Django authentication + django-allauth | Custom UUID User model must exist before the first migration |
| Persistence access | Django ORM and Django migrations | Backend models/migrations are the executable schema |
| Primary database | PostgreSQL 14+ | Exact deployed version belongs to Infrastructure configuration |
| Backend tests | pytest + pytest-django | Test policy belongs to the testing strategy |

The custom User model integrates with Django authentication and django-allauth. It does not define a bespoke password field or provider-specific `google_id`. Provider identities use django-allauth `SocialAccount` or its supported equivalent; verified email uses django-allauth's verified-email representation.

## Frontend

| Concern | Approved baseline | Boundary |
|---|---|---|
| UI runtime | React 19 | Exact package versions belong to `package.json` and its lockfile |
| Language | TypeScript | Compiler configuration belongs to Frontend |
| Build tool | Vite | npm is the package manager |
| Server-state integration | TanStack Query | Cache behavior must respect server authorization and invalidation |
| Routing | React Router | Exact compatible version belongs to the frontend manifest |
| Form/schema support | React Hook Form + Zod | Exact versions belong to the frontend manifest |
| Component tests | Vitest + React Testing Library | Jest is not the MVP frontend test runner |

### CSS and components

The MVP uses native CSS, CSS Modules, and CSS custom properties for design tokens.

- Do not introduce Tailwind, Material UI, or a CSS-in-JS framework for MVP.
- Do not build a generalized project-owned component library upfront.
- Extract reusable components when real repetition, consistency, or accessibility needs justify them.
- Audited headless primitives may be introduced selectively when a control's accessible behavior would otherwise be difficult to implement correctly.

## API and integration

| Concern | Approved baseline |
|---|---|
| API style | Versioned resource-oriented REST over HTTPS |
| Contract | Documentation-owned machine-readable [OpenAPI](../api/openapi.yaml) |
| Authentication | Server-side Django session cookie |
| Browser request integrity | Django CSRF cookie/header contract |
| Synchronization | Request/response API with client cache invalidation and refetch |
| Concurrent writes | Pure last-write-wins for MVP |

OpenAPI is the sole route and wire-contract source of truth. Architecture, product, security, and planning documents may explain intent and policy but must not maintain competing endpoint or schema inventories.

## Data and execution model

- PostgreSQL is the only MVP application datastore.
- Django migrations are the sole application schema-migration mechanism.
- PostgreSQL RLS is not used for MVP household isolation.
- Database-backed Django sessions are used for MVP with the approved 14-day expiry; logout and security revocation may end a session earlier. Redis is not required.
- No WebSockets or server-sent events are required for MVP synchronization.
- No Redis, Celery, queue, dedicated worker, or message broker is introduced solely for transactional email.
- Scheduled household purge and session cleanup run as externally scheduled backend commands or equivalent idempotent jobs; Infrastructure/Automation own scheduling.

Numeric scalability or latency claims from superseded design documents are not acceptance gates. Performance gates remain unresolved until they define percentile, endpoint set, dataset, environment, concurrency profile, and duration.

## Delivery and repository tooling

| Concern | Approved baseline | Ownership |
|---|---|---|
| Version control and hosting | Git + GitHub | Each repository |
| CI/CD | GitHub Actions | Service workflows in service repos; shared assets/policy in Automation |
| Containerization | Docker | Service Dockerfiles in Backend/Frontend; deployment manifests in Infrastructure |
| Local full-stack orchestration | Docker Compose | Infrastructure, consuming service-owned images/configuration |
| Transactional email | Provider-neutral backend adapter with bounded synchronous post-commit call | Backend application behavior; Infrastructure provider provisioning |
| Managed email provider | Deferred | Resolve under D02; adapter prevents product coupling |
| Deployment target | Deferred | Resolve under D02 before the deployment milestone |
| Error tracking/monitoring vendor | Deferred | Resolve under D02; minimum capability remains an MVP launch requirement |

GitHub Actions supersedes earlier documents that left CI/CD technology undecided. The five-repository ownership model is defined by [ADR-009](adr/ADR-009-five-repository-topology.md).

## Explicit MVP exclusions

The following are outside the approved MVP technology baseline unless a later decision changes it:

- Tailwind, Material UI, and CSS-in-JS frameworks;
- Jest as the frontend test runner;
- JWT authentication for the browser application;
- PostgreSQL RLS;
- optimistic-concurrency version checks and conflict-detection `409` responses;
- WebSocket/SSE synchronization;
- Redis as a required dependency;
- queue/worker infrastructure added solely for transactional email;
- GraphQL as a competing MVP API;
- provider-specific OAuth identity fields or persisted Google tokens without a feature need.
