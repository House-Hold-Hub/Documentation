# PRD Revision Summary: HouseHoldHub MVP

## Revision Date
August 16, 2026

## Overview
The PRD has been revised based on 10 critical blocking decisions and additional clarifications. The revision clarifies scope, resolves contradictions, separates product requirements from implementation decisions, and establishes explicit authorization rules.

---

## Requirements Added

### Authentication & Account Management
- **FR-7:** Users can authenticate with an existing HouseHoldHub account to join invited households

### Household Management
- **FR-15:** User can have an authenticated account in multiple households and switch between them

### Member Management
- **FR-23:** When a member is removed, content they created (tasks, expenses, shopping items, inventory items) remains in the household and is attributed to them
- **FR-24:** Tasks assigned to a removed member become unassigned; member name is preserved in history

### Tasks/Chores Module
- **FR-30:** Any member can edit task details (title, description, due date, etc.)
- **FR-31:** Assigned members can mark their own assigned tasks as complete
- **FR-32:** Household Owner can mark any task as complete

### Shopping List Module
- **FR-38:** Any member can update shopping item details (name, quantity, notes)
- **FR-44:** Members can clear/archive purchased items in bulk with confirmation

### Expenses Module
- **FR-46:** If payer is not specified, expense defaults to the member who created it
- **FR-47:** Expense shows date, amount, payer, category, description, and creator

### Data Synchronization
- **FR-59:** All API changes (tasks, shopping, expenses, inventory) are persisted immediately server-side
- **FR-60:** Client applications should refetch or invalidate relevant data after mutations to ensure consistency
- **FR-61:** Multiple household members can edit the same resource; last-write-wins is acceptable for MVP
- **FR-62:** Concurrent edits of the same resource may result in the later edit overwriting the earlier one; full conflict resolution is post-MVP

### General Requirements & Non-Functional
- **FR-65:** All household data access is scoped to household membership; users cannot access or modify resources belonging to households they are not members of (scoped at query/authorization layer)
- **FR-67:** Users should see sufficiently fresh household data during normal usage (on page load, navigation, after mutations)
- **FR-68:** Household password resets and invitation links must be cryptographically secure and time-limited
- **FR-69:** Invitations and authentication flows must be protected against common attacks (CSRF, brute force, session fixation)

---

## Requirements Changed

### Introduction & Solution Statement
- **Changed:** Removed "collaborate in real-time" from solution description
- **Rationale:** Real-time is post-MVP; MVP uses API-based sync with cache invalidation

### Workflows
- **Workflow 2 (Inviting Members):** Completely restructured to show separate paths for existing users and new users; removed mention of owner notification
- **Workflow 3 (Task Creation):** Removed "real-time" language; replaced with "see task when they refresh or navigate"
- **Workflow 4 (Shopping):** Removed "syncs in real-time" language; replaced with "visible during normal usage"

### Authentication & Account Management
- **FR-1-6:** Significantly simplified and reframed
  - FR-3: Changed from "enforce minimum 8 characters" to "must meet minimum security standards"
  - FR-4: Changed from "valid 1 hour" to "valid for limited period"
  - FR-5: Changed from "30 days or until logout" to "until logout or expiration"
  - FR-6: Removed (replaced with FR-7 for account joining)

### Household Management
- **FR-8-12:** Renumbered and reworded for clarity
  - FR-8: Changed "optional household code" to explicit requirement for unique code
  - FR-10: Changed "never expires" to "can be regenerated; previous becomes invalid"
  - FR-13: Changed "soft-deleted for 30 days" to "placed in recoverable state"

### Member Management
- **FR-16-26:** Complete rewrite with explicit invitation lifecycle and member removal behavior
  - Split invitation into three paths (email for existing user, email for new user, household code)
  - Added explicit invitation states (pending, accepted, revoked, expired)
  - Clarified member removal consequences

### Tasks/Chores Module
- **FR-27-36:** Completely rewritten with explicit authorization rules
  - Removed "soft-deleted; visible to owner for recovery period" language
  - Removed recurring task metadata field (FR-30 in old version)
  - Added explicit rules: creator/owner can reassign/delete; any member can assign
  - Changed from real-time sync to normal refresh pattern

### Shopping List Module
- **FR-37-44:** Renumbered and clarified
  - Changed "Item shows purchaser name and purchase date when marked complete" to clarify purchaser is the person who marks it purchased
  - Added ability to toggle items unpurchased
  - Clarified creator/owner deletion permissions

### Expenses Module
- **FR-45-52:** Renumbered and clarified
  - FR-46: Added explicit default payer rule (defaults to creator if not specified)
  - FR-52: Changed "extensible" to "custom categories are post-MVP"

### Inventory Module
- **FR-53-58:** Renumbered with authorization clarifications
  - Clarified creator/owner deletion permissions
  - Removed complex grouping requirement; made grouping optional

### Session & Security Requirements
- **FR-54/55:** Removed prescriptive language about implementation (server-side validation, XSS prevention)
- **Added FR-63-69:** New product-level security and non-functional requirements focusing on outcomes rather than mechanisms

### Password Requirements
- **Changed:** From "enforce minimum 8 characters" to "password must meet minimum security standards (system enforces complexity appropriate for threat model)"
- **Rationale:** Decouples product requirement from arbitrary implementation detail

### Session Duration
- **Changed:** From "30 days" to "until logout or session expiration"
- **Rationale:** 30 days was arbitrary and not justified; deferred to System Design

---

## Requirements Removed

### Real-Time Synchronization (Old FR-25, 51, 52)
- Removed real-time WebSocket requirement
- Removed offline mutation queueing requirement
- Replaced with API-based synchronization with cache invalidation

### Recurring Task Metadata (Old FR-30)
- Removed: "Task can be marked as 'recurring' with metadata (frequency: daily/weekly/monthly)"
- Rationale: Recurring tasks are post-MVP; no metadata in MVP to avoid prematurely committing to inadequate data model

### Soft Deletion for Individual Entities
- Removed from tasks, shopping items, inventory items
- Kept only for households (FR-13-14)
- Rationale: Simplified MVP; recovery UI not required for individual items

### Soft Deletion General Requirement (Old FR-57)
- Removed: "Deleted data is soft-deleted and retained for 30 days for recovery"
- Replaced with explicit soft-deletion for households only; permanent deletion for individual resources

### Dashboard Notifications (Old Workflow 2, Step 6)
- Removed: "Owner receives notification (future feature) that member joined"
- Rationale: Notifications are post-MVP except for transactional emails

### Real-Time Architecture Patterns (Technical Considerations)
- Removed: WebSocket, polling, real-time sync architecture from Technical Considerations
- Deferred to System Design document as an implementation decision

### Technology Stack Recommendations
- Removed entire "Technology Stack Recommendations (Not Prescriptive)" section
- Rationale: Implementation details belong in System Design, not PRD

### Arbitrary Constraints
- Removed: "30-day session persistence"
- Removed: "Household codes never expire"
- Removed: "Join links valid 30 days" as a fixed requirement (now says "valid for defined period")

---

## Final MVP Feature Hierarchy

### MUST-HAVE (Foundational)
1. **Authentication** (email/password + Google OAuth)
   - Account creation, login, password reset
   - Session management
   - Account required for household membership

2. **Household Management**
   - Create household
   - Modify household name/description
   - Delete household (recoverable)
   - Switch between multiple households (one active context)

3. **Member Management**
   - Invite by email (existing users, new users)
   - Join with household code
   - Remove members (with content preservation)
   - Display member list

4. **Household Authorization & Isolation**
   - Household data access scoped to membership
   - Cross-household data access prevented
   - Owner-only operations (delete, invite, remove)
   - Member-only operations (cannot invite/remove)

5. **Dashboard**
   - Household name
   - Member list
   - Pending task count
   - Tasks due soon (if due dates exist)
   - Shopping list summary (pending item count)
   - Quick action buttons (create task, add shopping item)

---

### PRIMARY MVP (Core Workflows)
1. **Tasks/Chores Module**
   - Create tasks (any member)
   - Assign to members (any member can assign to self/others)
   - Edit task details (any member)
   - Mark complete (assigned member or owner)
   - Reassign/delete (creator or owner)
   - Filter by assignee, status, due date
   - Pending and completed sections

2. **Shopping List Module**
   - Add items (any member)
   - Update items (any member)
   - Mark purchased/unpurchased (any member)
   - Delete items (creator or owner)
   - Separate pending and purchased sections
   - Filter by status

---

### SECONDARY MVP (Supporting Workflows)
1. **Expenses Module**
   - Log expenses with amount, category, description, optional payer
   - Payer defaults to creator if not specified
   - View expense log (sorted by date, newest first)
   - Display total and per-category breakdown
   - Edit/delete own expenses (members); edit/delete any (owner)
   - Predefined categories: Food, Utilities, Maintenance, Entertainment, Other

2. **Inventory Module**
   - Add items with name, quantity, optional category/location
   - Update quantities
   - Edit item details
   - Delete items (creator or owner)
   - Optional grouping by category
   - Display last modified date

---

### POST-MVP (Deferred Features)

**Iteration 2:**
- Recurring task automation
- In-app & email notifications
- Task history and audit log
- Activity feed

**Iteration 3:**
- Expense splitting and settlement
- Advanced member roles
- Calendar view
- Expense attachments

**Iteration 4+:**
- Comments and mentions
- File attachments on tasks
- Mobile apps
- Integrations (Google Calendar, Slack, etc.)
- Advanced analytics
- Guest access
- Custom expense categories
- User profiles (avatars, preferences)

---

## Requirement Traceability

### Goals → Workflows → Requirements
All 69 functional requirements now trace back to at least one of the 6 main user workflows or explicitly listed non-functional requirement.

### Authorization Model Complete
- Tasks: Creation, assignment, editing, completion, reassignment, deletion all specified
- Shopping: Creation, updating, marking purchased, deletion all specified
- Expenses: Creation, editing, deletion with owner-specific privileges specified
- Inventory: Creation, updating, deletion with creator/owner privileges specified
- Household: Owner-only operations clearly marked

---

## Remaining Open Questions for System Design

These decisions belong in a **separate System Design/Architecture document**:

1. **Data Retention:** How long should deleted households remain recoverable?
2. **Session Lifetime:** What is the appropriate session timeout?
3. **Household Code Format:** What should the code format be (length, character set, case-sensitivity)?
4. **Invitation Expiration:** How long should email invitation links remain valid?
5. **Legal/Privacy:** What GDPR and regional privacy compliance requirements apply?
6. **Audit Log Retention:** How long should critical action logs be retained?
7. **Performance SLAs:** What are target response times for API endpoints?
8. **Scalability:** Target concurrent users per household during MVP?
9. **Database Technology:** Which database technology should be used?
10. **Authentication Mechanism:** JWT, session cookies, or other? How are credentials stored and refreshed?
11. **API Design:** REST vs. GraphQL? API versioning strategy?
12. **Conflict Resolution:** Detailed mechanism for handling concurrent edits beyond "last-write-wins"?
13. **Monitoring & Observability:** Logging strategy, error tracking, performance monitoring tools?
14. **Disaster Recovery:** Backup frequency, recovery procedures, RPO/RTO targets?

---

## Key Changes in Principle

### 1. Product vs. Implementation Clarity
- **Before:** Technical Considerations section mixed product requirements with implementation guidance
- **After:** Clear separation between product-level requirements (in PRD) and implementation guidance (deferred to System Design)

### 2. Real-Time Requirement
- **Before:** Contradicted itself (claimed real-time required, but also said can start with polling)
- **After:** Clearly states API-based sync with cache invalidation is MVP; real-time WebSocket is post-MVP

### 3. Authorization Model
- **Before:** Vague permissions table with unclear creator/owner restrictions per entity
- **After:** Explicit authorization rules for every action on every entity type

### 4. Soft Deletion Scope
- **Before:** System-wide soft deletion with 30-day recovery for all entities
- **After:** Soft deletion only for households (recovery period TBD in System Design); permanent deletion for individual entities

### 5. Recurring Tasks
- **Before:** Store metadata in MVP for future automation
- **After:** Defer entire feature to post-MVP; no metadata in MVP

### 6. Multi-Household Support
- **Before:** Explicitly prohibited ("no multi-household accounts")
- **After:** Enabled; users can belong to multiple households (one active context)

### 7. Notifications
- **Before:** Mentioned as feature in Workflow 2 but listed as NICE-TO-HAVE
- **After:** Removed from MVP except for transactional emails (auth, invitations)

### 8. Password & Session Requirements
- **Before:** Arbitrary numbers (8 characters, 30 days)
- **After:** Product requirements (must be secure); exact mechanisms deferred to System Design

---

## Statistics

| Category | Count |
|----------|-------|
| **Total Requirements (FRs)** | 69 |
| **Authentication & Account** | 7 |
| **Household Management** | 8 |
| **Member Management** | 11 |
| **Tasks/Chores** | 10 |
| **Shopping List** | 8 |
| **Expenses** | 8 |
| **Inventory** | 6 |
| **Data Synchronization** | 4 |
| **General & Non-Functional** | 7 |
| **Requirements Added** | 21 |
| **Requirements Changed** | 30+ |
| **Requirements Removed** | 12+ |
| **Workflows** | 6 |
| **MVP Priority Tiers** | 4 (MUST-HAVE, PRIMARY, SECONDARY, POST-MVP) |

---

## Validation Checklist

- [x] All 10 blocking decisions incorporated
- [x] All additional clarifications applied
- [x] Real-time contradiction resolved
- [x] Authorization model complete and unambiguous
- [x] Soft deletion simplified
- [x] Dashboard requirements explicit
- [x] Member removal behavior specified
- [x] Invitation flow covers both user types
- [x] Notifications deferred
- [x] Recurring tasks deferred
- [x] Multi-household support enabled
- [x] Product requirements separated from implementation decisions
- [x] Requirement traceability verified
- [x] Non-functional requirements added (security, privacy, accessibility, reliability)
- [x] Open questions clarified
- [x] Roadmap updated with new iteration breakdown

---

## Next Steps

1. **Review the revised PRD** for accuracy and completeness
2. **Identify any remaining ambiguities** before implementation begins
3. **Create System Design document** addressing the 14 open questions above
4. **Plan implementation** based on finalized PRD and System Design
5. **Create individual feature PRDs** for post-MVP iterations (recurring tasks, notifications, expense splitting, etc.)
