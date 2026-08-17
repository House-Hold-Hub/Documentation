# ADR-012: Household ownership and authorization invariants

> **Status:** Accepted  
> **Date:** 2026-08-16  
> **Owner:** Backend repository with Product, Security, and Documentation governance  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Owner invariants, household authorization, and assignment integrity  
> **Supersedes:** The ownership/role details of [ADR-005](ADR-005-household-scoped-authorization.md) and the assignment-integrity claim in [ADR-008](ADR-008-single-assignee-task-model.md)  
> **Superseded by:** —

## Context

ADR-005 correctly selected Membership as the basis for household scoping, while the earlier domain material alternated between `Household.owner_id` and an owner-role Membership as the source of ownership. Separately, ADR-008 and historical models claimed that pointing `Task.assigned_to` at Membership automatically guarantees that the assignee belongs to the Task's Household. A normal foreign key validates only that the Membership exists; it does not enforce equality with a separate `Task.household_id`.

The MVP needs one authoritative owner reference, a synchronized role representation for permission checks, and an honest enforcement mechanism for household isolation and assignment integrity.

## Decision

### Ownership

- `Household.owner_id` is the authoritative MVP owner reference.
- A matching Membership for `(household, owner_id)` with role `owner` must exist.
- Household creation and administrative repair maintain the Household owner reference and matching Membership atomically.
- Removal of the owner Membership is forbidden.
- Public ownership transfer is outside MVP scope.
- Membership roles are immutable through the MVP product and API. Promotion, demotion, and any role change that would violate the owner invariant are forbidden.

### Owner account lifecycle

An owner account may be disabled: revoke all sessions immediately, deny authentication/access, and retain the User, `owner_id`, and owner Membership.

An owner User must not be anonymized or hard-deleted while it owns an active Household. Before either action, an administrative lifecycle must resolve every owned Household through household deletion or a separately approved future administrative ownership-transfer mechanism. Exact legal/privacy behavior remains governed by deferred decision D03.

### Household access and authorization

- All household-owned reads and mutations begin from a query scoped to an active Membership in the requested Household.
- Action authorization then applies the canonical product permission rules.
- Product permissions are defined in the [permissions matrix](../../product/permissions-matrix.md), not duplicated in this ADR.
- A nonexistent or outside-scope object produces `404`; a known in-household action denied by role/authorship produces `403`; unauthenticated access produces `401`.
- Member removal produces immediate server-side denial on every subsequent request.
- PostgreSQL RLS is not used for MVP. Backend scoping, authorization checks, and comprehensive negative isolation tests are the enforcement model.

### Task assignment integrity

- A Task has zero or one assignee Membership.
- The assignee Membership must belong to the same Household as the Task.
- Application/service-layer validation plus comprehensive negative integrity and authorization tests is the guaranteed MVP mechanism.
- A normal foreign key or cross-table `CHECK` is not claimed to guarantee the invariant.
- A composite database foreign key may be added only if it can be represented cleanly by the chosen Django/PostgreSQL implementation; it is not required for the MVP guarantee.
- When an assignee Membership is removed, the Task becomes unassigned. Visible removed-assignee history is not an MVP promise.

## Consequences

### Positive

- Ownership checks have one authoritative reference.
- The matching Membership keeps ordinary role-based queries simple without creating a second source of truth.
- Disabling an owner is possible without corrupting the aggregate.
- Assignment integrity is based on an implementable guarantee rather than an invalid database claim.
- The absence of RLS is explicit and compensated by required negative tests.

### Costs and risks

- Owner-reference and owner-Membership writes require an atomic service operation and repair/audit checks.
- Administrative account deletion must identify owned Households and refuse unsafe anonymization/hard deletion.
- Every household-owned query must use the scoped access path; missing a scope is a security defect.
- Service-layer assignment validation must cover create, reassignment, bulk/import paths if later introduced, and races around Membership removal.

## Supersession

ADR-005 remains accepted for the Membership-based scoping pattern, but its older role/action table and deletion descriptions are non-normative where the permissions matrix or this ADR differs. ADR-008 remains accepted for single-assignee tasks; this ADR supersedes only its statement that the ordinary Membership foreign key guarantees same-household assignment.

## Related decisions

- [Domain model](../domain-model.md)
- [Security model](../../security/security-model.md)
- [Permissions matrix](../../product/permissions-matrix.md)
- [ADR-008: Single-assignee tasks](ADR-008-single-assignee-task-model.md)
