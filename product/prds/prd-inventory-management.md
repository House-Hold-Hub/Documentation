# PRD: Inventory management

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP household inventory items, positive quantities, display metadata, category grouping, editing, and deletion
> Supersedes: inventory requirements in the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md)

## 1. Overview

Inventory management is a supporting MVP workflow for keeping a basic shared count of household supplies. It supports positive integer quantity, optional unit/category/location metadata, and category-based grouping without adding stock automation or complex classification.

## 2. Goals

- Let household collaborators add and maintain basic inventory under the permissions matrix.
- Keep quantity semantics explicit and valid.
- Use category as the primary grouping and location as display metadata.
- Allow creator/owner deletion while keeping ordinary edits collaborative.

## 3. User stories

### INV-US-001: Add an inventory item

**Description:** As an active member, I want to record an item and quantity so that the household can see current supplies.

**Acceptance criteria:**

- Name and positive integer quantity are required.
- Unit, category, and location are optional.
- Unit and location are display metadata and do not change numeric quantity semantics.

### INV-US-002: Maintain inventory

**Description:** As an active member, I want to edit details or adjust quantity so that the shared state remains current.

**Acceptance criteria:**

- Authorized editing supports name, quantity, unit, category, and location.
- Increment and decrement operate on an integer quantity.
- A change that would reduce quantity below one is rejected; it is not interpreted as deletion.
- Updated state is visible after normal mutation invalidation/refetch.

### INV-US-003: Browse and delete inventory

**Description:** As a household member, I want items grouped meaningfully and obsolete items removable by an authorized actor.

**Acceptance criteria:**

- Items with a category can be grouped by category; location remains item-level display metadata.
- Item deletion follows the permissions-matrix rule and is permanent.
- Deletion has no MVP recovery interface.

## 4. Functional requirements

- **INV-FR-001:** Inventory-item creation must support required name and positive integer quantity; creation authorization is defined only by the permissions matrix.
- **INV-FR-002:** Unit, category, and location are optional. Unit and location are free-form display metadata distinct from quantity.
- **INV-FR-003:** Inventory update must support name, quantity, unit, category, and location under the permissions-matrix rule.
- **INV-FR-004:** Quantity increment and decrement must preserve a positive integer. Any request that would produce a value below one must be rejected, not converted into deletion.
- **INV-FR-005:** The inventory view must support category grouping when category is present. Location may be displayed but is not a separate MVP grouping system.
- **INV-FR-006:** Each item must expose current quantity and last-modified time.
- **INV-FR-007:** Inventory-item deletion must use the permissions-matrix rule and is permanent; MVP has no recovery interface.
- **INV-FR-008:** Inventory changes use pure last-write-wins and become visible through normal invalidation/refetch, page load, navigation, or manual refresh.

## 5. Authorization boundary

The canonical inventory action-by-role rules are in the [permissions matrix](../permissions-matrix.md). OpenAPI alone defines the wire contract.

## 6. Design requirements

- Present item name, positive quantity, optional unit, optional category, optional location, and last-modified time.
- Category grouping must still provide an understandable uncategorized presentation.
- Quantity controls must be keyboard operable and must communicate rejected below-one changes.
- Loading, empty, validation-error, authorization-denied, and mutation-error states must be handled.

## 7. Non-goals

- Zero or negative quantity.
- Treating decrement-to-zero as deletion.
- Automatic low-stock alerts, reorder rules, or shopping-list synchronization.
- Complex category/location taxonomies, analytics, attachments, or scanning.
- Real-time push, offline mutation queues, or edit-conflict detection.

## 8. Success and verification

- Add, edit, increment, decrement, group, and delete journeys meet their acceptance criteria.
- Negative scenarios cover zero/negative/non-integer quantity, below-one decrement, unauthorized delete, removed-member access, and cross-household access.
- Release verification follows the [testing strategy](../../quality/testing-strategy.md) and [release acceptance](../../quality/release-acceptance.md).

## 9. Legacy traceability

| Legacy ID | Canonical requirement |
|---|---|
| `FR-53`–`FR-56` | `INV-FR-001`–`INV-FR-004`, `INV-FR-007`, and the permissions matrix |
| `FR-57`–`FR-58` | `INV-FR-005`–`INV-FR-006` |
| `FR-59`–`FR-62`, `FR-67` | `INV-FR-008` and umbrella cross-cutting requirements |

## 10. Open questions

None for MVP.
