# Product permissions matrix

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: Readable MVP action-by-actor authorization rules
> Supersedes: Permission tables and role summaries in the legacy MVP PRD, system-design snapshots, domain-model snapshots, and planning documents

## Purpose and use

This matrix is the readable product source for who may perform each MVP action. Feature PRDs own lifecycle and validation behavior; [OpenAPI](../api/openapi.yaml) owns operation-level wire contracts. The Backend must enforce this matrix on every request, scoped to the active household.

## Actors and terms

- **Owner:** the user referenced by `Household.owner_id`, with a matching active `owner` Membership.
- **Member:** an active non-owner Membership in the household.
- **Active member:** owner or member whose Membership and household permit current access.
- **Creator:** the user attributed as creating a task, shopping item, expense, or inventory item.
- **Assignee:** the user represented by the task's current active same-household Membership assignment.
- **Intended invitee:** the authenticated user whose canonically normalized verified email matches the invitation.
- **Eligible code joiner:** a verified authenticated user who is not already a member of the household and possesses its current join code.
- **Support/administration:** an internal operational actor, not a public household role.
- **Non-member:** any user without active membership in the household.

“No” means the action is denied and must not reveal outside-scope household data. Exact HTTP status semantics remain canonical in OpenAPI.

## Identity and household access

| Action | Owner | Member | Verified authenticated non-member | Unverified or unauthenticated user | Support/administration |
|---|---|---|---|---|---|
| Create a household | Yes | Yes, independently of existing memberships | Yes | No | Not a product role |
| List/select own accessible households | Yes | Yes | Yes; result may be empty | No | Not a product role |
| View household details | Yes | Yes | No | No | Only through approved support procedure |
| View dashboard and household resources | Yes | Yes | No | No | Only through approved support procedure |
| View member list | Yes | Yes | No | No | Only through approved support procedure |
| Update household name/description | Yes | No | No | No | Only through approved support procedure |
| Change household currency | No; unavailable in MVP | No | No | No | No MVP currency-change workflow |
| Delete household into recoverable state | Yes, with confirmation | No | No | No | Only through approved support procedure |
| Recover soft-deleted household within 30 days | No public action | No public action | No | No | Yes |
| Remove a non-owner member | Yes | No | No | No | Only through approved support procedure |
| Remove owner Membership | No | No | No | No | Forbidden while ownership invariant applies |
| Transfer ownership or change roles | No; unavailable in MVP | No | No | No | No approved transfer workflow in MVP |

## Email invitations

| Action | Owner | Member | Intended invitee | Other user / non-member | Support/administration |
|---|---|---|---|---|---|
| Create email invitation | Yes | No | No | No | Only through approved support procedure |
| List household invitations | Yes | No | No | No | Only through approved support procedure |
| Resend invitation / rotate token | Yes | No | No | No | Only through approved support procedure |
| Revoke invitation by invitation ID | Yes | No | No | No | Only through approved support procedure |
| Exchange fragment bearer token for non-secret session intent | If token holder | If token holder | Yes, as token holder | Yes, as token holder; exchange alone grants no membership or preview | Not required |
| View safe invitation preview | No join flow needed; already a member | No join flow needed; already a member | Yes, only after authentication, verification, and revalidation | No | Only through approved support procedure |
| Accept invitation | No new Membership; duplicate rejected | No new Membership; duplicate rejected | Yes, after explicit acceptance and all lifecycle checks | No | No normal product action |

Token possession alone authorizes only the bounded exchange step. It does not bypass account authentication, verified-email matching, current invitation state, explicit acceptance, or duplicate-membership protection.

## Household join code

| Action | Owner | Member | Eligible code joiner | Other user | Support/administration |
|---|---|---|---|---|---|
| Read current code | Yes | No | No | No | Only through approved support procedure |
| Regenerate current code | Yes | No | No | No | Only through approved support procedure |
| Join using current code | Already a member; duplicate rejected | Already a member; duplicate rejected | Yes | No if unauthenticated, unverified, invalid code, or already a member | No normal product action |

## Tasks

| Action | Owner | Member who is creator | Member who is current assignee | Other active member | Non-member |
|---|---|---|---|---|---|
| View/list/filter | Yes | Yes | Yes | Yes | No |
| Create | Yes | Yes | Yes | Yes | No |
| Assign at creation to self or another active member | Yes | Yes | Yes | Yes, as creator of the new task | No |
| Edit title/description/due date | Yes | Yes | Yes | Yes | No |
| Set/change/clear assignment after creation | Yes | Yes | No, unless also creator | No | No |
| Complete assigned task | Yes | If also assignee | Yes | No | No |
| Reopen assigned task | Yes | If also assignee | Yes | No | No |
| Complete or reopen unassigned task | Yes | Yes | Not applicable | Yes | No |
| Delete | Yes | Yes | No, unless also creator | No | No |

## Shopping list

| Action | Owner | Member who is creator | Other active member | Non-member |
|---|---|---|---|---|
| View/list/filter | Yes | Yes | Yes | No |
| Create | Yes | Yes | Yes | No |
| Edit name/quantity | Yes | Yes | Yes | No |
| Mark purchased/unpurchased | Yes | Yes | Yes | No |
| Delete one item | Yes | Yes | No | No |
| Clear all purchased items | Yes, with confirmation | Yes, with confirmation | Yes, with confirmation | No |

The any-member bulk-clear permission is intentionally broader than individual-item deletion and remains a permanent bulk delete, not an archive.

## Expenses

| Action | Owner | Member who is creator | Other active member | Non-member |
|---|---|---|---|---|
| View/filter totals and entries | Yes | Yes | Yes | No |
| Create expense | Yes | Yes | Yes | No |
| Choose an active same-household payer at creation | Yes | Yes | Yes | No |
| Edit mutable expense details | Yes | Yes | No | No |
| Change payer after creation | No | No | No | No |
| Change expense currency after creation | No | No | No | No |
| Delete expense | Yes | Yes | No | No |

## Inventory

| Action | Owner | Member who is creator | Other active member | Non-member |
|---|---|---|---|---|
| View/group items | Yes | Yes | Yes | No |
| Create | Yes | Yes | Yes | No |
| Edit name/quantity/unit/category/location | Yes | Yes | Yes | No |
| Increment/decrement while result remains at least one | Yes | Yes | Yes | No |
| Delete | Yes | Yes | No | No |

## Cross-cutting enforcement rules

- Every household-scoped read and write requires an active Membership unless the table explicitly defines a pre-membership invitation/code action.
- A known active member denied an in-household action receives the shared authorization behavior; a nonexistent or outside-scope object uses the shared not-found behavior. OpenAPI owns the exact response contract.
- Member removal takes effect on every subsequent server request. Stale client data does not confer access.
- The security model and authorization ADR define the enforcement architecture; this matrix defines the product result that must be enforced and negatively tested.
- Task assignment and expense payer selection must reject a Membership/user outside the selected household.
- Pure last-write-wins does not change who is authorized to mutate a resource.

## Change control

Any change to an action in this matrix is a product authorization decision. It requires corresponding review of the affected feature PRD, domain/security invariants, OpenAPI operations, and authorization/isolation tests. Documentation must not add a route-specific exception without first changing this matrix through the approved decision process.
