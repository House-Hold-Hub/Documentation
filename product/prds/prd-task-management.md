# PRD: Task management

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP household task creation, assignment, editing, completion, reopening, filtering, and deletion behavior
> Supersedes: task requirements in the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md)

## 1. Overview

Task management is a primary MVP workflow. Active household members collaborate on a shared linear task list, optionally assign one active household member, and mark work complete or reopen it under explicit permissions.

## 2. Goals

- Support creation of clear household tasks under the permissions-matrix rule.
- Support zero or one same-household assignee without requiring assignment.
- Keep ordinary task details collaboratively editable while protecting reassignment and deletion.
- Make completion and reopening rules predictable.
- Preserve tasks when members leave while removing invalid assignments.

## 3. User stories

### TASK-US-001: Create and optionally assign a task

**Description:** As an active member, I want to create a task and optionally assign it so that responsibility is visible.

**Acceptance criteria:**

- A title is required; description and due date are optional.
- The creator may leave the task unassigned or choose one active member of the same household.
- A user or Membership outside the household cannot be assigned.
- The new task is visible to household members after normal mutation invalidation/refetch.

### TASK-US-002: Edit a task collaboratively

**Description:** As an active member, I want to update ordinary details while assignment remains controlled.

**Acceptance criteria:**

- Ordinary editing supports title, description, and due date for actors authorized by the permissions matrix.
- Assignment changes use the matrix's distinct assignment rule rather than ordinary-edit authorization.
- A request that attempts an unauthorized assignment change is denied rather than silently ignoring the field.
- Valid concurrent updates use last-write-wins with no optimistic-concurrency conflict promise.

### TASK-US-003: Complete or reopen a task

**Description:** As an authorized member, I want to change completion state so that the shared list reflects current work.

**Acceptance criteria:**

- Assigned and unassigned tasks each use their state-specific completion rule in the permissions matrix.
- Reopening uses exactly the same authorization rule as completion for the task's current assignment state.
- Completing records the completion time and actor; reopening clears the active completion time according to the domain model.
- Completed tasks remain visible with a clear visual distinction.

### TASK-US-004: Find relevant tasks

**Description:** As a member, I want to filter the task list so that I can focus on relevant work.

**Acceptance criteria:**

- The list can be filtered by assignee, completion state, and due-date criteria.
- Open and completed states remain understandable without relying on color alone.
- The list is linear; a Kanban workflow is not required.

### TASK-US-005: Remove a member safely

**Description:** As a remaining member, I want tasks to remain usable after an assignee leaves.

**Acceptance criteria:**

- Removing the assigned Membership makes the task unassigned.
- The task and its creator attribution remain while the corresponding User record exists.
- No visible former-assignee name or assignment-history promise exists in MVP.

## 4. Functional requirements

- **TASK-FR-001:** Task creation must support a required title, optional description, and optional due date; creation authorization is defined only by the permissions matrix.
- **TASK-FR-002:** At creation, assignment may be empty or reference one active member of the same household, including the creator where authorized.
- **TASK-FR-003:** The guaranteed MVP assignment-integrity mechanism is service/application validation plus comprehensive negative integrity and authorization tests. Documentation must not claim that a normal foreign key or cross-table check alone proves same-household assignment.
- **TASK-FR-004:** Ordinary task-detail editing must support title, description, and due date as a separately authorized action.
- **TASK-FR-005:** Setting, changing, or clearing assignment after creation must use the distinct assignment rule in the permissions matrix rather than ordinary-edit authorization.
- **TASK-FR-006:** Task deletion must use the permissions-matrix rule and is permanent; MVP has no task-recovery interface.
- **TASK-FR-007:** Completion of an assigned task must use the assigned-task completion rule in the permissions matrix.
- **TASK-FR-008:** Completion of an unassigned task must use the unassigned-task completion rule in the permissions matrix.
- **TASK-FR-009:** Reopening uses exactly the same authorization rule as completion.
- **TASK-FR-010:** Completion state must expose whether the task is complete and retain the completion actor and timestamp while complete, subject to legitimate nulls defined by the domain model and OpenAPI.
- **TASK-FR-011:** Completed tasks remain visible and visually distinct.
- **TASK-FR-012:** Members may filter tasks by assignee, completion state, and due-date criteria.
- **TASK-FR-013:** A task must retain creation and update timestamps, creator attribution, and current assignment as defined by the domain model.
- **TASK-FR-014:** Removing an assigned Membership must leave the task in place and set the current assignment to unassigned.
- **TASK-FR-015:** MVP does not preserve or display former-assignee identity as assignment history.
- **TASK-FR-016:** Concurrent task edits use pure last-write-wins. MVP must not expose an unsupported optimistic-concurrency `409 Conflict` behavior.
- **TASK-FR-017:** Task changes must be visible through normal client invalidation/refetch, page load, navigation, or manual refresh; real-time push is not required.

## 5. Authorization boundary

The canonical task action-by-role rules are in the [permissions matrix](../permissions-matrix.md). Wire-level errors and schemas are defined only by [OpenAPI](../../api/openapi.yaml).

## 6. Design requirements

- Use a linear list with visible title, current assignee or unassigned state, optional due date, and completion state.
- Assignment choices must contain only active members of the selected household.
- Completion state and available actions must be understandable to keyboard and assistive-technology users.
- Loading, empty, validation-error, authorization-denied, and mutation-error states must be handled.

## 7. Non-goals

- Multiple assignees.
- Recurring tasks or recurrence metadata.
- Task comments, mentions, attachments, or notifications.
- Assignment-history presentation or preserved removed-assignee display.
- Kanban, calendar integration, real-time push, or offline mutation queues.
- Optimistic concurrency, conflict detection, merge, or undo.

## 8. Success and verification

- Create, edit, assign, reassign, unassign, complete, reopen, filter, delete, and removed-assignee journeys meet their acceptance criteria.
- Negative scenarios cover every actor/resource-state combination in the permissions matrix and cross-household assignment/access attempts.
- Last-write-wins behavior is tested without expecting edit-conflict responses.
- Release verification follows the [testing strategy](../../quality/testing-strategy.md) and [release acceptance](../../quality/release-acceptance.md).

## 9. Legacy traceability

| Legacy ID | Canonical requirement |
|---|---|
| `FR-27`–`FR-30` | `TASK-FR-001`–`TASK-FR-006` and the permissions matrix |
| `FR-31`–`FR-32` | `TASK-FR-007`–`TASK-FR-009` and the permissions matrix (reopening now explicit) |
| `FR-33`–`FR-36` | `TASK-FR-010`–`TASK-FR-013` |
| `FR-24` | `TASK-FR-014`–`TASK-FR-015`; former-assignee history wording superseded |
| `FR-59`–`FR-62`, `FR-67` | `TASK-FR-016`–`TASK-FR-017` and umbrella cross-cutting requirements |

## 10. Open questions

None for MVP. Optimistic concurrency requires a separate post-MVP decision.
