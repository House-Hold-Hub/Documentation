# PRD: Dashboard

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP household dashboard contents, due-soon calculation, deterministic ordering, pending counts, and quick actions
> Supersedes: dashboard requirements in the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md) and archived planning snapshots

## 1. Overview

The dashboard is a minimal entry point for the selected household. It identifies the household, presents its members, previews at most three due-soon tasks, reports the complete pending-task count and pending-shopping count, and offers quick task and shopping actions. It is not an analytics or finance dashboard.

## 2. Goals

- Orient a member to the currently selected household.
- Show a small deterministic preview of urgent incomplete tasks without hiding the total backlog.
- Show the pending shopping-item count.
- Make task creation and shopping-item addition immediately reachable.
- Avoid timezone ambiguity by requiring the client to supply the calendar reference date.

## 3. User stories

### DASH-US-001: See the household overview

**Description:** As an active member, I want to know which household I am viewing and who belongs to it.

**Acceptance criteria:**

- The dashboard shows household name, member count, and member overview.
- It omits the household join code and other owner-only secrets.
- Only an active household member can view it.

### DASH-US-002: See due-soon tasks

**Description:** As an active member, I want a short urgent-task preview and the full pending count so that I can prioritize without mistaking the preview for the whole backlog.

**Acceptance criteria:**

- The request includes valid `as_of=YYYY-MM-DD` supplied by the client.
- The preview includes only incomplete tasks that are overdue, due on `as_of`, or due during the next seven calendar days inclusive.
- Incomplete tasks without a due date are excluded from the preview but included in the complete pending-task count.
- At most three tasks are returned in the approved deterministic order.

### DASH-US-003: See shopping state and act quickly

**Description:** As an active member, I want the pending shopping count and quick actions so that I can move directly into common work.

**Acceptance criteria:**

- The dashboard shows the complete count of currently unpurchased shopping items.
- Quick actions lead to task creation and shopping-item addition.
- Changes become visible through normal invalidation/refetch; real-time push is not required.

## 4. Functional requirements

- **DASH-FR-001:** The dashboard must identify the selected household by name and expose member count and member overview.
- **DASH-FR-002:** Generic dashboard data must omit the household join code.
- **DASH-FR-003:** The dashboard calculation request must require explicit `as_of=YYYY-MM-DD`.
- **DASH-FR-004:** The official frontend must derive `as_of` from the user's browser-local calendar date. The backend must not derive dashboard “today” from server UTC or deployment-local time.
- **DASH-FR-005:** Given `as_of`, due soon means an incomplete task whose due date is before `as_of` (overdue), equal to `as_of` (due today), or after `as_of` and no later than seven calendar days after it (upcoming).
- **DASH-FR-006:** Incomplete tasks without a due date must be excluded from the due-soon preview.
- **DASH-FR-007:** The preview must return at most three tasks in this deterministic order: overdue first; earliest due date first; oldest creation timestamp first; stable identifier as final tie-breaker.
- **DASH-FR-008:** The dashboard must expose the complete count of all incomplete household tasks separately from the three-task preview, including incomplete tasks without a due date.
- **DASH-FR-009:** The dashboard must expose the complete count of shopping items whose current state is pending/unpurchased.
- **DASH-FR-010:** The dashboard must offer quick actions for creating a task and adding a shopping item.
- **DASH-FR-011:** `as_of` is a current calculation input; accepting it does not establish a historical-dashboard product feature.
- **DASH-FR-012:** No persisted user, household, or application-wide timezone is required solely for this calculation.
- **DASH-FR-013:** Dashboard data must become current through normal invalidation/refetch, page load, navigation, or manual refresh.

## 5. Authorization boundary

The canonical dashboard action-by-role rule is in the [permissions matrix](../permissions-matrix.md). The response schema and `as_of` parameter are defined only in [OpenAPI](../../api/openapi.yaml).

## 6. Design requirements

- Clearly label the three-task list as a preview and keep the full pending count visually distinct.
- Show overdue and due-state information without relying on color alone.
- Provide usable loading, empty, invalid-`as_of`, denied, and error states.
- Support the responsive and accessibility expectations in release acceptance.

## 7. Non-goals

- Expense totals, recent expenses, or any other expense widget.
- Inventory summaries.
- Analytics, charts, rankings, productivity metrics, activity feeds, notifications, or history views.
- Historical dashboard browsing based on arbitrary `as_of` values.
- Persisted timezone solely for dashboard calculation.
- Real-time WebSocket/SSE updates.

## 8. Success and verification

- Overview, pending count, due-window boundary, no-due-date exclusion, deterministic tie-breaking, shopping count, and quick-action journeys meet their acceptance criteria.
- Tests cover dates before/on/one-to-seven-days after/beyond `as_of`, more than three matches, identical due/creation values, undated tasks, and cross-household access.
- Release verification follows the [testing strategy](../../quality/testing-strategy.md) and [release acceptance](../../quality/release-acceptance.md).

## 9. Legacy traceability

| Legacy source | Canonical requirement |
|---|---|
| MVP PRD dashboard UI pattern and resolved decision 4 | `DASH-FR-001`, `DASH-FR-008`–`DASH-FR-010` |
| Revised-plan “three pending tasks” | `DASH-FR-003`–`DASH-FR-008`; “due soon” and complete count are now precise |
| Revised-plan expense widgets | Superseded and excluded by the approved minimal MVP scope |
| `FR-67` | `DASH-FR-013` and umbrella freshness requirement |

## 10. Open questions

None for MVP.
