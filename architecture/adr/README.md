# Architecture decision records

> **Status:** Accepted  
> **Owner:** Documentation repository; Architecture/Engineering stewardship  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** ADR discovery, status, numbering, and supersession links

Architecture decision records preserve the context and consequences of durable technical and architectural choices. An ADR is immutable as a historical decision: later changes use a new ADR and explicit supersession metadata rather than silently rewriting the original rationale.

Implementation snippets in historical ADRs are illustrative records, not current setup instructions. The [technology baseline](../technology-baseline.md), repository manifests/lockfiles, [domain model](../domain-model.md), [OpenAPI](../../api/openapi.yaml), and Backend models/migrations own their respective current details.

## Index

| ADR | Decision | Status | Supersession |
|---|---|---|---|
| [ADR-001](ADR-001-multi-repository-structure.md) | Multi-repository architecture (original three-repository topology) | Superseded | Superseded by ADR-009 |
| [ADR-002](ADR-002-django-rest-framework.md) | Django + Django REST Framework backend | Accepted | Django-version portion superseded by ADR-010 |
| [ADR-003](ADR-003-postgresql-persistence.md) | PostgreSQL persistence | Accepted | — |
| [ADR-004](ADR-004-session-based-authentication.md) | Session-based authentication (original contract) | Superseded | Superseded by ADR-011 |
| [ADR-005](ADR-005-household-scoped-authorization.md) | Household scoping through Membership | Accepted | Ownership/permission details superseded by ADR-012 |
| [ADR-006](ADR-006-api-based-synchronization.md) | API-based synchronization without real-time transport | Accepted | — |
| [ADR-007](ADR-007-database-backed-sessions.md) | Database-backed sessions; no required Redis | Accepted | Cookie/registry/revocation details superseded by ADR-011 |
| [ADR-008](ADR-008-single-assignee-task-model.md) | Zero-or-one Task assignee | Accepted | Same-household enforcement claim superseded by ADR-012 |
| [ADR-009](ADR-009-five-repository-topology.md) | Five first-class repositories | Accepted | Supersedes ADR-001 |
| [ADR-010](ADR-010-backend-runtime-baseline.md) | Python 3.14 + Django 5.2 LTS backend baseline | Accepted | Supersedes Django-version portion of ADR-002 |
| [ADR-011](ADR-011-identity-and-session-security.md) | Identity, verification, OAuth linking, and session security | Accepted | Supersedes ADR-004 and parts of ADR-007 |
| [ADR-012](ADR-012-ownership-and-authorization.md) | Owner invariant, household authorization, and assignment integrity | Accepted | Supersedes parts of ADR-005 and ADR-008 |
| [ADR-013](ADR-013-invitation-security.md) | Invitation token transport and authenticated handoff | Accepted | Replaces pre-baseline design examples |
| [ADR-014](ADR-014-api-contract-governance.md) | Documentation-owned OpenAPI and contract review | Accepted | Replaces ambiguous ownership and competing inventories |
| [ADR-015](ADR-015-transactional-email-delivery.md) | Post-commit bounded synchronous email delivery | Accepted | Replaces pre-baseline email execution examples |

## Status meanings

- **Proposed:** Under review and not authoritative.
- **Accepted:** Current durable decision; its metadata may identify narrowly superseded portions that do not invalidate the core decision.
- **Superseded:** Historical only; follow its `Superseded by` link.
- **Rejected:** Considered but never adopted.

## Creating or changing an ADR

1. Use the next unused three-digit identifier. Never reuse or renumber an existing ADR.
2. Include Status, Date, Owner, Supersedes, and Superseded by metadata.
3. State Context, Decision, and Consequences, including costs and risks.
4. Link every superseded record in both directions.
5. Keep product behavior in PRDs, readable action permissions in the permissions matrix, wire schemas/routes in OpenAPI, and exact implementation details in the owning repository.
6. For a breaking API-contract decision, follow [ADR-014](ADR-014-api-contract-governance.md) and obtain Documentation, Backend, and Frontend review.

## Historical preservation

Superseded ADRs remain in this directory so links and decision history stay stable. Other obsolete design snapshots belong in the non-normative archive and must not appear as current alternatives in this index.
