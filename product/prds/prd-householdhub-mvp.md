# PRD: HouseHoldHub MVP

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP problem, product outcomes, release boundary, and cross-feature journeys
> Supersedes: the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md) as the active specification

## 1. Product overview

HouseHoldHub is a responsive web application for families, couples, roommates, and other shared households. It gives household members one place to coordinate tasks, shopping, expenses, and inventory instead of distributing those responsibilities across messages, notes, and verbal reminders.

The MVP establishes secure identity and household boundaries, then delivers shared task and shopping workflows plus basic expense, inventory, and dashboard capabilities. Detailed behavior lives in the feature PRDs linked below.

## 2. Problem and outcomes

Households need a clear, shared view of responsibilities and common household information. The MVP must:

- let a person create and verify an account, authenticate, and create or join a household;
- let an owner invite and manage household members without exposing one household's data to another;
- let trusted household members coordinate assigned or unassigned tasks;
- support a shared shopping list, expense log, and inventory;
- provide a small household dashboard that points members to the core workflows;
- keep permissions understandable and make failed verification or invitation delivery recoverable.

## 3. Users and roles

The MVP has two household roles:

- **Owner:** the household's single authoritative owner, with the owner actions defined in the [permissions matrix](../permissions-matrix.md).
- **Member:** an active household collaborator with the member actions defined in the permissions matrix.

Roles are fixed for the MVP. Public ownership transfer, promotion, demotion, and additional roles are post-MVP. A person may belong to multiple households and explicitly select the active household context.

## 4. MVP capability map

| Capability | Priority | Canonical behavior |
|---|---|---|
| Identity and authentication | Foundational | [Identity and authentication PRD](prd-identity-authentication.md) |
| Household, membership, and invitations | Foundational | [Household, membership, and invitations PRD](prd-household-membership-invitations.md) |
| Task management | Primary | [Task-management PRD](prd-task-management.md) |
| Shopping list | Primary | [Shopping-list PRD](prd-shopping-list.md) |
| Expense tracking | Supporting | [Expense-tracking PRD](prd-expense-tracking.md) |
| Inventory management | Supporting | [Inventory-management PRD](prd-inventory-management.md) |
| Household dashboard | Foundational overview | [Dashboard PRD](prd-dashboard.md) |

The priority labels describe product emphasis; every row remains required for the approved MVP release.

## 5. Cross-feature user journeys

### MVP-US-001: Create an account and household

As a new user, I want to create and verify an account and establish a household so that I can begin coordinating shared work.

**Acceptance criteria:**

- The user can complete signup, verification, household creation, and dashboard arrival without external documentation.
- The journey does not require unnecessary repeated authentication or re-entry of already accepted data.
- Household creation makes the creator the owner and creates the matching owner membership atomically.
- The application gives clear next steps to invite a member or create a first task.

### MVP-US-002: Join an invited household

As an invitee, I want an invitation to survive the normal signup, login, verification, and session-rotation flow in the same browser so that I can review and explicitly accept it.

**Acceptance criteria:**

- The invitation is revalidated after authentication and verified-email confirmation.
- A valid invitation shows only the approved safe preview and requires explicit acceptance.
- Acceptance atomically consumes the invitation and creates at most one membership.
- Delivery failure leaves a recoverable pending state with a rate-limited resend path.

### MVP-US-003: Coordinate household work

As an active member, I want to use tasks and the shopping list and see relevant summaries on the dashboard so that household work stays visible.

**Acceptance criteria:**

- Supported mutations are persisted server-side and reflected after normal invalidation, refetch, navigation, or manual refresh.
- The dashboard's task and shopping summaries follow their feature PRDs.
- Every request remains scoped to the active household.

### MVP-US-004: Switch households safely

As a user in multiple households, I want to switch the active household so that I see only the selected household's data.

**Acceptance criteria:**

- The household selector lists only households the user may currently access.
- Switching context reloads household-scoped data for the selected household.
- Data from another household is never mixed into the selected context.

### MVP-US-005: Revoke former-member access

As an owner, I want removed members to lose server-side access immediately so that household information remains protected.

**Acceptance criteria:**

- Every subsequent request from the removed member is denied for that household.
- Client-cached information disappears through normal invalidation, refetch, or denied-response handling.
- Household content remains, and tasks assigned to the removed membership become unassigned.

## 6. Cross-cutting product requirements

- **MVP-FR-001:** All household resources and aggregate views must be scoped to an active household membership.
- **MVP-FR-002:** All supported mutations must be validated and persisted server-side; client validation is supplementary.
- **MVP-FR-003:** After a mutation, the official client must invalidate or refetch affected data so normal use presents sufficiently fresh state.
- **MVP-FR-004:** Concurrent edits use pure last-write-wins for MVP. The product does not promise merge behavior, edit warnings, or optimistic-concurrency `409 Conflict` responses.
- **MVP-FR-005:** The application must work responsively at desktop and mobile viewport sizes supported by release acceptance.
- **MVP-FR-006:** Core workflows must meet the accessibility expectations in release acceptance, including keyboard operation, meaningful labels, and presentation that does not rely on color alone.
- **MVP-FR-007:** The signup-to-household journey is evaluated by application-controlled steps, clarity, successful completion, lack of redundant authentication/data entry, and delivery-failure recovery. External email transit and user waiting time are excluded; no numeric interaction-time threshold is approved.
- **MVP-FR-008:** Critical invitation, member-change, and household-deletion events must be auditable according to the security and operations requirements.

Security controls are canonical in the [security model](../../security/security-model.md); the HTTP contract is canonical in [OpenAPI](../../api/openapi.yaml); verification is canonical in [release acceptance](../../quality/release-acceptance.md).

## 7. MVP non-goals

The MVP does not include:

- advanced household roles, public ownership transfer, or role management;
- file or image attachments;
- comments, mentions, household messaging, or an activity feed;
- recurring tasks, task assignment history, or real-time WebSocket/SSE synchronization;
- notifications about household activity beyond transactional identity and invitation email;
- expense splitting, settlement, custom categories, currency conversion, mixed-currency reporting, or per-expense currency selection;
- complex inventory classification, low-stock alerts, or automatic deletion when quantity reaches zero;
- analytics, rankings, productivity reports, or expense widgets on the dashboard;
- offline mutation queues or conflict resolution;
- native mobile applications, external calendar/tool integrations, household discovery, or additional social providers;
- self-service account deletion or a device/session-management interface.

Post-MVP direction is recorded without commitment in the [roadmap](../roadmap.md).

## 8. Release outcome

The MVP is product-complete only when the approved end-to-end journeys pass, the authorization and household-isolation scenarios are covered, no critical defect blocks a core workflow, and the release requirements in [release acceptance](../../quality/release-acceptance.md) are satisfied. Closing a particular number of issues or tests is not a product acceptance criterion.

## 9. Canonical boundaries

- This document owns the MVP boundary and cross-feature outcomes.
- Feature behavior belongs only in the linked feature PRDs.
- The [permissions matrix](../permissions-matrix.md) owns the readable action-by-role rules.
- The [domain model](../../architecture/domain-model.md) owns conceptual entities and invariants.
- [OpenAPI](../../api/openapi.yaml) owns routes, request/response schemas, requiredness, nullability, and wire errors.
- Repository manifests and lockfiles own exact dependency versions.
- Live GitHub issues own execution state and issue counts.

## 10. Legacy requirement disposition

This table preserves traceability from the former monolithic PRD. “Superseded” means the historical wording remains evidence but is not active behavior.

| Legacy requirement(s) | Canonical destination | Disposition |
|---|---|---|
| `FR-1`–`FR-7` | [Identity and authentication](prd-identity-authentication.md) | Split and reconciled; email verification, explicit OAuth linking, and session revocation are now explicit |
| `FR-8`–`FR-15` | [Household, membership, and invitations](prd-household-membership-invitations.md) | Split and reconciled; includes required immutable household currency and exact 30-day deletion lifecycle |
| `FR-16`–`FR-23`, `FR-25`–`FR-26` | [Household, membership, and invitations](prd-household-membership-invitations.md) and [permissions matrix](../permissions-matrix.md) | Split and expanded with approved invitation and join-code lifecycle; action-by-role rules moved to the matrix |
| `FR-24` | [Household, membership, and invitations](prd-household-membership-invitations.md) and [task management](prd-task-management.md) | Partially superseded: task becomes unassigned; no MVP promise to display the removed assignee's name or assignment history |
| `FR-27`–`FR-36` | [Task management](prd-task-management.md) and [permissions matrix](../permissions-matrix.md) | Split; completion and reopening use the same matrix rule, and assignment integrity is clarified |
| `FR-37`–`FR-44` | [Shopping list](prd-shopping-list.md) and [permissions matrix](../permissions-matrix.md) | Split without product-scope loss; action-by-role rules moved to the matrix |
| `FR-45`–`FR-52` | [Expense tracking](prd-expense-tracking.md) and [permissions matrix](../permissions-matrix.md) | Split and superseded where necessary: `amount_minor`, ISO currency snapshot, `incurred_on`, five approved categories, and `SET NULL` payer behavior |
| `FR-53`–`FR-58` | [Inventory management](prd-inventory-management.md) and [permissions matrix](../permissions-matrix.md) | Split and clarified: category grouping, location metadata, rejection below quantity one, and matrix-owned authorization |
| `FR-59`–`FR-62` | `MVP-FR-002`–`MVP-FR-004` and synchronization ADR | Consolidated; pure last-write-wins replaces unsupported conflict responses |
| `FR-63`–`FR-66`, `FR-68`–`FR-69` | [Security model](../../security/security-model.md), [testing strategy](../../quality/testing-strategy.md), and feature PRDs | Moved to their canonical control and verification sources; invitation URL wording is superseded by the approved server-visible-location rule |
| `FR-67` | `MVP-FR-003` | Kept and clarified as invalidation/refetch freshness, not real-time delivery |
| Numeric workflow-time, test-count, coverage, issue-count, and unsupported performance claims | [Release acceptance](../../quality/release-acceptance.md), [testing strategy](../../quality/testing-strategy.md), and [roadmap](../roadmap.md) | Superseded; no arbitrary gates are active |

## 11. Open questions

No unresolved product question blocks the MVP documentation migration. The explicitly bounded `D01`–`D06` decisions remain deferred under the deadlines in the [roadmap](../roadmap.md).
