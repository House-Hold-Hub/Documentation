# PRD: Shopping list

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP shared shopping-item creation, editing, purchase state, deletion, and bulk clearing
> Supersedes: shopping requirements in the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md)

## 1. Overview

The shared shopping list is a primary MVP workflow. Active household members add and update needed items, move them between pending and purchased states, and clear purchased items when they no longer need to be retained.

## 2. Goals

- Keep one shared pending/purchased view for the household.
- Let household collaborators maintain item details and current purchase state under the permissions matrix.
- Preserve creator-controlled deletion for individual items while supporting a simple household-wide clear-purchased action.
- Make current state sufficiently fresh without real-time infrastructure.

## 3. User stories

### SHOP-US-001: Add and edit an item

**Description:** As an active member, I want to add and update a shopping item so that the household knows what is needed.

**Acceptance criteria:**

- Item name is required and quantity is optional.
- Item name and quantity can be updated by actors authorized in the permissions matrix.
- New and updated items are visible to members after normal mutation invalidation/refetch.

### SHOP-US-002: Toggle purchase state

**Description:** As an active member, I want to mark an item purchased or needed again so that the list reflects current state.

**Acceptance criteria:**

- The permissions-matrix action supports both purchased and unpurchased transitions.
- While purchased, the item exposes the purchasing member and purchase date.
- Pending and purchased items are visually distinct and can be viewed separately or filtered by state.

### SHOP-US-003: Delete shopping items

**Description:** As an authorized member, I want to remove obsolete items so that the list stays useful.

**Acceptance criteria:**

- Individual deletion uses its permissions-matrix rule.
- Bulk clear uses its distinct, intentionally broader permissions-matrix rule and requires explicit confirmation.
- Bulk clear permanently deletes the matching items; it does not archive them or create a recoverable state.

## 4. Functional requirements

- **SHOP-FR-001:** Shopping-item creation must support required name and optional quantity; creation authorization is defined only by the permissions matrix.
- **SHOP-FR-002:** Item update must support name and quantity under the permissions-matrix rule.
- **SHOP-FR-003:** Purchase-state update must support both purchased and unpurchased under the permissions-matrix rule.
- **SHOP-FR-004:** A currently purchased item must expose purchaser attribution and purchase date, subject to legitimate nulls after user deletion as defined by the domain model and OpenAPI.
- **SHOP-FR-005:** The shopping view must distinguish pending from purchased items and support status-based viewing or filtering.
- **SHOP-FR-006:** Individual-item deletion must use the permissions-matrix rule and is permanent.
- **SHOP-FR-007:** Bulk clear must use its intentionally broader permissions-matrix rule and require confirmation.
- **SHOP-FR-008:** Bulk clear is permanent deletion, not archive; cleared items have no MVP recovery interface.
- **SHOP-FR-009:** Shopping changes use last-write-wins and become visible through normal invalidation/refetch, page load, navigation, or manual refresh.

## 5. Authorization boundary

The canonical shopping action-by-role rules are in the [permissions matrix](../permissions-matrix.md). OpenAPI alone defines the wire contract.

## 6. Design requirements

- Present pending and purchased sections, or an equivalently clear state filter.
- The purchase control must be keyboard operable and its state must not rely on color alone.
- Bulk clear must communicate that deletion is permanent and require confirmation before submission.
- Loading, empty, validation-error, authorization-denied, and mutation-error states must be handled.

## 7. Non-goals

- Archived purchased items or recovery after deletion.
- Item attachments, comments, or household-activity notifications.
- Real-time push, offline mutation queues, or edit-conflict detection.

## 8. Success and verification

- Add, edit, purchase, unpurchase, individual delete, filter/view-by-state, and confirmed bulk-clear journeys meet their acceptance criteria.
- Negative scenarios cover individual-delete restrictions, household isolation, deleted household, and removed-member access.
- Release verification follows the [testing strategy](../../quality/testing-strategy.md) and [release acceptance](../../quality/release-acceptance.md).

## 9. Legacy traceability

| Legacy ID | Canonical requirement |
|---|---|
| `FR-37`–`FR-40` | `SHOP-FR-001`–`SHOP-FR-004` and the permissions matrix |
| `FR-41`–`FR-43` | `SHOP-FR-005`–`SHOP-FR-006` and the permissions matrix |
| `FR-44` | `SHOP-FR-007`–`SHOP-FR-008` and the permissions matrix; the broader bulk permission is retained |
| `FR-59`–`FR-62`, `FR-67` | `SHOP-FR-009` and umbrella cross-cutting requirements |

## 10. Open questions

None for MVP.
