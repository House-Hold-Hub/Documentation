# Product requirements

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: Active HouseHoldHub product-requirements documents

This directory contains approved product behavior. The [MVP umbrella PRD](prd-householdhub-mvp.md) defines the release boundary and links to one authoritative PRD for each included feature. Feature PRDs define observable behavior and product scope; they do not define routes, persistence implementation, dependency versions, or deployment configuration.

## Active PRDs

| Document | Responsibility |
|---|---|
| [HouseHoldHub MVP](prd-householdhub-mvp.md) | MVP problem, outcomes, release scope, cross-feature journeys, and legacy requirement disposition |
| [Identity and authentication](prd-identity-authentication.md) | Signup, verification, login, Google identity linking, password recovery, account access, and session-revocation behavior |
| [Household, membership, and invitations](prd-household-membership-invitations.md) | Household lifecycle, owner/member roles, invitations, join codes, member removal, and household switching |
| [Task management](prd-task-management.md) | Task creation, assignment, editing, completion/reopening, filtering, and removal effects |
| [Shopping list](prd-shopping-list.md) | Shared shopping items, purchased state, deletion, and bulk clearing |
| [Expense tracking](prd-expense-tracking.md) | Monetary representation, household currency, payer rules, dates, categories, expense history, and totals |
| [Inventory management](prd-inventory-management.md) | Positive quantities, item metadata, category grouping, editing, and deletion |
| [Dashboard](prd-dashboard.md) | Minimal household overview, due-soon calculation, pending counts, shopping summary, and quick actions |

The readable action-by-role source is the [permissions matrix](../permissions-matrix.md). Post-MVP direction and bounded unresolved decisions are in the [roadmap](../roadmap.md).

## Boundaries

- Product behavior belongs in a PRD. The umbrella PRD must not restate detailed feature requirements.
- Action-by-role rules belong in the permissions matrix. PRDs link to it instead of maintaining parallel authorization tables.
- Conceptual entities and invariants belong in the [domain model](../../architecture/domain-model.md).
- Durable technical decisions belong in [ADRs](../../architecture/adr/README.md).
- Routes, request/response schemas, requiredness, nullability, and wire errors belong only in the [OpenAPI contract](../../api/openapi.yaml).
- Security controls and threat-oriented requirements belong in the [security model](../../security/security-model.md).
- Release verification belongs in [release acceptance](../../quality/release-acceptance.md).
- Live issue state and issue counts belong in GitHub, not PRDs.

## Requirement identifiers and changes

Feature requirements use a stable domain prefix, such as `TASK-FR-001`. The umbrella PRD records how the legacy `FR-1` through `FR-69` requirements moved. When an approved decision changed a legacy requirement, the new PRD states the supersession explicitly; historical wording remains available only in the archive.

Changing an approved requirement requires product approval and coordinated review of every affected canonical artifact. A route or schema change must update OpenAPI through the contract-change workflow; editing a PRD alone does not change the wire contract.
