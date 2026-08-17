# PRD: HouseHoldHub MVP

## Introduction

HouseHoldHub is a collaborative household management platform designed for people who live together (families, couples, roommates, shared households) to centralize and coordinate their day-to-day responsibilities.

The MVP establishes the core platform with foundational household and member management, primary workflows around shared tasks/chores and shopping lists, and secondary workflows for expenses and inventory management. The architecture is designed to allow independent evolution of each domain after launch.

**Problem Statement:** Households managing multiple responsibilities struggle to coordinate who does what and when. Without a centralized tool, coordination happens across text messages, sticky notes, and verbal reminders—leading to miscommunication, forgotten tasks, and unequal distribution of work.

**Solution:** A shared web application where household members can organize tasks, shopping, and expenses in one place, see who's responsible for what, and track progress together.

---

## Goals

- Enable households to centralize task and responsibility management
- Provide a frictionless household creation/joining flow
- Support collaboration through transparent task assignment and status tracking
- Establish a secure, extensible foundation for independent feature domains
- Enable users to create an account, form/join a household, invite members, and manage their first shared task without documentation

---

## User Roles & Permissions

### Roles

**Household Owner**
- Created the household; has all permissions
- Can invite members, remove members
- Can manage household settings (name, visibility, etc.)
- Implied admin for all features until role separation is needed
- Note: role assignment (e.g. promoting a member to a new role) does not exist in MVP — role is fixed at join time (Owner vs. Member) and is immutable; role management is post-MVP (see Future Roles below)

**Member**
- Invited to the household
- Can view all household data (tasks, shopping, expenses, inventory)
- Can create and interact with content (add tasks, items, expenses)
- Can assign themselves or others to tasks
- Cannot invite new members or remove the household

**Future Roles** (out of MVP scope)
- Admin (manage member roles, household settings)
- Restricted Member (view-only, limited action permissions)
- Guest (temporary, feature-limited access)

### Authorization Model (MVP)

Household members are trusted collaborators. Authorization is explicit per action and is always scoped to household membership.

#### Tasks
- Any member can **create** tasks
- Any member can **assign** a task to themselves or another active household member at creation (zero or one assignee per task)
- Task creator and Household Owner can **reassign or delete** a task
- Any member can **edit** ordinary task details (title, description, due date, etc.), but **not** the assignment — only creator/owner can change who a task is assigned to
- Assigned member can **complete** their own assigned task; any active member can complete an **unassigned** task
- Household Owner can **complete** any task
- Household Owner can **modify or delete** any task

#### Shopping
- Any member can **add and update** shopping items
- Any member can **mark items as purchased/unpurchased**
- Shopping item creator and Household Owner can **delete** shopping items

#### Expenses
- Any member can **create** expenses
- Members can **edit/delete** only expenses they created
- Household Owner can **edit/delete** any expense

#### Inventory
- Any member can **add and update** inventory items
- Inventory item creator and Household Owner can **delete** inventory items

#### Household Management
- Household Owner can **invite members** (by email or household code)
- Household Owner can **remove members**
- Household Owner can **delete household** (enters recoverable state)
- Household Owner can **manage household settings**

#### Authorization Scope & Isolation
- All resource access is scoped to household membership; users cannot access or modify resources belonging to households they are not members of
- When a member is removed from a household, they immediately lose all access to that household's data
- A user must have an authenticated HouseHoldHub account to join a household

---

## Main User Workflows

### Workflow 1: Account & Household Setup (First-Time User)

```
1. User signs up with email/password or Google OAuth
2. User creates new household (name, optional description)
3. System generates household code (optional shareable link)
4. User invited to household as Owner
5. User sees empty household dashboard
6. User can now invite others or start creating tasks
```

**Acceptance Criteria:**
- Signup to household creation takes < 2 minutes
- New user sees clear next-step guidance (invite members, create first task)
- Household code is copyable and shareable

### Workflow 2: Inviting Members

**Path A: Existing User**
```
1. Household Owner clicks "Invite Members" and enters email address
2. System sends invitation email with join link
3. Invitee clicks link and authenticates (if not already logged in)
4. Invitee reviews household and accepts invitation
5. Invitee becomes member of household; appears in member list
```

**Path B: New User**
```
1. Household Owner clicks "Invite Members" and enters email address
2. System sends invitation email with join link
3. Invitee clicks link → directed to signup flow
4. Invitee creates account and authenticates
5. Invitee reviews household and accepts invitation
6. Invitee becomes member of household; appears in member list
```

**Path C: Using Household Code**
```
1. Household Owner shares household code with member
2. New or existing user enters code in their account
3. User is added to household directly; appears in member list
```

**Acceptance Criteria:**
- Email invitations sent from verified sender
- Join links include invitation state (pending, accepted, revoked, expired)
- Join links are revocable by owner; revocation prevents further use
- Household code can be regenerated; previous code becomes invalid
- User cannot join same household twice (prevents duplicates)
- Member appears in household member list immediately upon joining
- Email invitations expire after a defined period (e.g., 30 days)

### Workflow 3: Creating & Assigning Tasks (Primary Workflow)

```
1. User clicks "Add Task" in household
2. User enters task title, optional description, optional due date
3. User optionally assigns task to one other member (single assignee; task may also be left unassigned)
4. Task appears in household task list for all members
5. Assigned member sees task in their personal task list
6. Members mark task complete; task status updates are visible to other members during normal usage (page load, navigation, or manual refresh — see FR-67)
```

**Acceptance Criteria:**
- Task creation takes < 30 seconds
- Assigned member sees task when they refresh or navigate back to the household view
- Task status updates are visible to members during normal usage (on page load, navigation, or manual refresh)
- Unassigned tasks visible to all members; any active member can complete an unassigned task

### Workflow 4: Shopping List Management

```
1. User clicks "Add to Shopping List"
2. User enters item name, optional quantity
3. Item appears in shared shopping list
4. Members check off items as purchased
5. Completed items move to "Purchased" section; purchased items can be cleared (deleted) in bulk
```

**Acceptance Criteria:**
- Shopping items visible to all members when they view the list
- Item state (needed/purchased) updates are visible to members during normal usage
- Clear visual differentiation between pending and purchased items
- Members can toggle items between purchased and unpurchased

### Workflow 5: Expense Tracking (Secondary)

```
1. User clicks "Add Expense"
2. User enters amount, category, description, optional payer
3. Expense appears in household expense log
4. System optionally calculates who owes whom (future feature)
5. Members can view shared expenses history
```

**Acceptance Criteria:**
- Expense recorded with date, amount, payer, category
- All members can view expense history
- Basic filtering/sorting by date or category

### Workflow 6: Household Inventory (Secondary)

```
1. User clicks "Add to Inventory"
2. User enters item name, quantity (positive integer), optional unit, category, location (optional)
3. Item appears in shared inventory
4. Members can update quantities
5. System can optionally alert when items run low (future feature)
```

**Acceptance Criteria:**
- Inventory items grouped by category or location
- Quantities can be incremented/decremented
- All members see current inventory state

---

## Feature Specifications

### MVP Priority Tiers

**MUST-HAVE (Foundational)**
- User authentication (email/password + Google OAuth)
- Household creation and basic settings (name, description)
- Member management (invite, join, list)
- Role-based permissions (Owner vs. Member)
- Dashboard showing household overview

**PRIMARY MVP (Core Workflows)**
- Tasks/Chores module (create, assign, track, complete)
- Shopping List module (create items, mark purchased)

**SECONDARY MVP (Supporting Workflows)**
- Expenses module (log and view shared expenses)
- Inventory module (track household items and quantities)

**NICE-TO-HAVE (MVP+)**
- In-app or email notifications for task assignments and household activity
- Activity feed or timeline view
- Task history and audit log
- Expense splitting and settlement calculations
- Recurring task automation
- Mobile app

**OUT OF SCOPE (Post-MVP)**
- Advanced permission roles (Admin, Restricted Member, Guest)
- Custom expense categories (predefined set only for MVP)
- File uploads or image attachments
- Messaging or comments on tasks
- Integration with external calendars or tools
- Analytics or reporting dashboards
- Mobile native apps (web-responsive is MVP)
- Real-time synchronization via WebSocket/SSE (API-based sync with refresh is MVP)
- Offline mutation queueing and conflict resolution

---

## Functional Requirements

### Authentication & Account Management

- **FR-1:** Users can create account with email + password
- **FR-2:** Users can authenticate with Google OAuth
- **FR-3:** Email addresses must be validated at signup and remain unique per user
- **FR-4:** Passwords must meet minimum security standards (system enforces complexity appropriate for the threat model)
- **FR-5:** Users can reset password via email link (valid for limited period)
- **FR-6:** Sessions persist until explicit logout or session expiration
- **FR-7:** Users can authenticate with an existing HouseHoldHub account to join invited households

### Household Management

- **FR-8:** User can create a new household with a name and optional description; user becomes Household Owner
- **FR-9:** System generates a unique household code (revocable shareable identifier) for each household
- **FR-10:** Household code can be regenerated by owner; previous code becomes invalid
- **FR-11:** System tracks household creation date, owner, and members
- **FR-12:** Owner can modify household name and description
- **FR-13:** Owner can delete household (with confirmation); deletion places household in recoverable state
- **FR-14:** Deleted households remain inaccessible to members but may be recovered during retention period
- **FR-15:** User can have an authenticated account in multiple households and switch between them

### Member Management

- **FR-16:** Owner can invite members by email; system sends invitation email with join link
- **FR-17:** Invitation links are valid for a defined period and include state (pending, accepted, revoked, expired)
- **FR-18:** Owner can revoke sent invitations; revoked links cannot be used
- **FR-19:** User with household code can join household directly (no email required; must have authenticated account)
- **FR-20:** Household displays list of current members with join date and role
- **FR-21:** Owner can remove members from household
- **FR-22:** Removed members immediately lose access to the household and its data
- **FR-23:** When a member is removed, content they created (tasks, expenses, shopping items, inventory items) remains in the household and is attributed to them
- **FR-24:** Tasks assigned to a removed member become unassigned; member name is preserved in history
- **FR-25:** System prevents users from joining the same household twice (prevents duplicate memberships)
- **FR-26:** Member list shows member name, role, and join date

### Tasks/Chores Module (Primary MVP)

- **FR-27:** Any member can create a task with title (required), description (optional), and due date (optional)
- **FR-28:** Any member can assign a task to themselves or another active household member at creation time; a task has zero or one assignee (single assignee per task; multi-assignee is post-MVP)
- **FR-29:** Task creator and Household Owner can reassign (change or clear the assignee) or delete tasks
- **FR-30:** Any member can edit ordinary task details (title, description, due date, etc.); only the task creator or Household Owner can change the task's assignment (see FR-29)
- **FR-31:** Assigned member can mark their own assigned task as complete; an unassigned task can be marked complete by any active household member
- **FR-32:** Household Owner can mark any task as complete
- **FR-33:** Completed tasks remain visible with visual distinction (strikethrough, grayed out, or badge)
- **FR-34:** Task creator and Household Owner can delete tasks (deletion is permanent; no recovery interface in MVP)
- **FR-35:** Task list can be filtered by assignee, status (open/complete), or due date
- **FR-36:** System stores task creation date, last modified date, creator, and current assignee

### Shopping List Module (Primary MVP)

- **FR-37:** Any member can add item to shopping list with name (required) and quantity (optional)
- **FR-38:** Any member can update shopping item details (name, quantity)
- **FR-39:** Any member can mark items as purchased or unpurchased
- **FR-40:** Purchased item shows purchaser name and purchase date; purchaser is the member who marked it purchased
- **FR-41:** Shopping item creator and Household Owner can delete items (deletion is permanent; no recovery interface in MVP)
- **FR-42:** Shopping list displays purchased items separately from pending items (or via status filter)
- **FR-43:** Item list can be filtered by status (pending/purchased)
- **FR-44:** Members can clear purchased items in bulk with confirmation (bulk permanent deletion; not an archive — no archived state is retained). Note: bulk clear is available to any member and is intentionally broader than the single-item delete restriction in FR-41 (creator/owner only) — since any member can already mark an item purchased (FR-39), restricting bulk clear to creator/owner would not meaningfully change who can effectively remove an item, so the simpler any-member rule is used for this bulk action

### Expenses Module (Secondary MVP)

- **FR-45:** Any member can log an expense with amount (required), category (required), description (optional), and payer (optional)
- **FR-46:** If payer is not specified, expense defaults to the member who created it
- **FR-47:** Expense shows date, amount, payer, category, description, and creator
- **FR-48:** All members can view household expense log sorted by date (newest first)
- **FR-49:** System displays total expenses and per-category breakdown
- **FR-50:** Members can edit or delete expenses they created; the payer field is immutable after creation (cannot be changed by edit, to preserve historical attribution)
- **FR-51:** Household Owner can edit or delete any expense (payer remains immutable, per FR-50)
- **FR-52:** Expense categories are predefined (Food, Utilities, Maintenance, Entertainment, Other); custom categories are post-MVP

### Inventory Module (Secondary MVP)

- **FR-53:** Any member can add item to inventory with name (required), quantity (required, positive integer), optional unit (free-form display text, e.g. "boxes", "bottles"), category (optional), and location (optional)
- **FR-54:** Any member can update item quantities (increment/decrement); quantity is always a positive integer, not a freeform string
- **FR-55:** Any member can edit item details (name, unit, category, location)
- **FR-56:** Inventory item creator and Household Owner can delete items (deletion is permanent; no recovery interface in MVP)
- **FR-57:** Inventory items are displayed with optional grouping by category (if provided)
- **FR-58:** System displays current quantity and last modified date for each item

### Data Synchronization

- **FR-59:** All API changes (tasks, shopping, expenses, inventory) are persisted immediately server-side
- **FR-60:** Client applications should refetch or invalidate relevant data after mutations to ensure consistency
- **FR-61:** Multiple household members can edit the same resource; last-write-wins is acceptable for MVP
- **FR-62:** Concurrent edits of the same resource may result in the later edit overwriting the earlier one; full conflict resolution (merge, undo, notifications) is post-MVP

### General Requirements & Non-Functional

- **FR-63:** All input is validated server-side; client-side validation is supplementary only
- **FR-64:** System sanitizes all user input to prevent injection attacks and XSS
- **FR-65:** All household data access is scoped to household membership; users cannot access or modify resources belonging to households they are not members of (scoped at query/authorization layer)
- **FR-66:** System logs critical actions (invitations sent, members added, members removed, households deleted) for audit and debugging
- **FR-67:** Users should see sufficiently fresh household data during normal usage (on page load, navigation, after mutations)
- **FR-68:** Household password resets and invitation links must be cryptographically secure and time-limited
- **FR-69:** Invitations and authentication flows must be protected against common attacks (CSRF, brute force, session fixation)

---

## Non-Goals (Out of MVP Scope)

- **No file uploads or media attachments** on tasks, shopping items, expenses, or inventory
- **No comments, mentions, or messaging** within the app
- **No advanced permission roles** (Owner role only; Admin, Restricted Member, Guest are post-MVP)
- **No expense splitting or settlement calculations** (log shared expenses, but do not calculate who owes whom)
- **No recurring task automation** (recurring task feature is post-MVP)
- **No in-app or email notifications** for household activity (transactional emails for authentication/invitations only)
- **No calendar integration** or external tool sync
- **No mobile native apps** (web-responsive design is MVP)
- **No analytics or household reports** (summary statistics on dashboard are acceptable)
- **No custom expense categories** (predefined set only)
- **No complex inventory grouping/filtering** (optional category/location metadata, basic list display)
- **No user profile customization** (avatars, bios, preferences are post-MVP)
- **No real-time synchronization** via WebSocket/SSE (API-based sync with refresh is sufficient)
- **No offline support** or mutation queueing
- **No additional social authentication providers** (Google only; additional providers are post-MVP)
- **No household discovery or search** (private households; join only via email invite or code)

---

## Design Considerations

### User Interface Principles

- **Simplicity:** Core workflows (create task, invite member, view list) should be discoverable in < 2 clicks
- **Clarity:** Status, assignee, and actions should be immediately visible without modals or navigation
- **Responsiveness:** Works on desktop (1280px+) and mobile (375px+); prioritize desktop for MVP
- **Accessibility:** WCAG 2.1 AA baseline (contrast, keyboard nav, labels)

### Key UI Patterns

- **Dashboard:** Household name, member list, pending task count, tasks due soon (if due dates exist), shopping list summary (pending item count), quick action buttons to create task or add shopping item
- **Task List:** Linear list view (not Kanban); filterable by assignee, status (open/complete), or due date; shows title, assignee, due date, completion status
- **Shopping List:** Checkbox list with items in "Pending" and "Purchased" sections; can toggle items between states
- **Expense Log:** Chronological table showing date, amount, payer, category, description; filterable by date or category
- **Inventory List:** Table with item name, quantity, category (if provided), last modified date; optional grouping by category

### Design Components to Reuse

- Form inputs (text, email, password, number, date, select)
- Modal dialogs (confirm actions, edit details)
- Buttons (primary, secondary, danger actions)
- Lists (members, tasks, items)
- Badges or labels (role, status, category)
- Notifications/toasts (success, error, info)

---

## Product-Level Non-Functional Requirements

### Security & Authorization

- **All API endpoints require authentication** before allowing access to household data
- **Household data is scoped at the authorization layer:** users can only access resources belonging to households they are active members of
- **Password reset links and invitation links** must be cryptographically secure, time-limited, and single-use
- **Passwords must be hashed** using a secure algorithm; plaintext storage is never acceptable
- **User authentication sessions** must be secure against session fixation and hijacking (HTTP-only cookies or secure token handling)
- **Cross-Site Request Forgery (CSRF) protection** must be implemented for state-changing operations
- **Brute-force attack mitigation** must protect login and password reset endpoints
- **No sensitive data** (passwords, tokens, household codes) should appear in logs or URLs

### Data Integrity

- **Household isolation is enforced** at the query/persistence layer, not just the application layer
- **Concurrent edits to the same resource** are handled by last-write-wins; more sophisticated conflict resolution is post-MVP
- **Member removal immediately revokes access;** removed members cannot perform new actions on the household
- **Deleted content** (tasks, shopping items, inventory items) cannot be recovered via the UI in MVP (permanent deletion)
- **Household deletion** places the household in a recoverable state; exact retention period is a System Design decision

### Performance & Reliability

- **API endpoints should respond in acceptable time** for normal household sizes (<100 members); exact SLAs are System Design decisions
- **Core workflows (task creation, shopping item creation, member addition)** should feel responsive to users
- **Data loss should not occur** due to application failure; persistent storage is required

### Accessibility & Usability

- **User interface should be accessible** at WCAG 2.1 AA level (contrast, keyboard navigation, screen reader compatibility)
- **New users should complete signup → household creation → first task in < 5 minutes** without external documentation
- **Household members should understand their roles and permissions** from the UI without confusion

### Privacy

- **User account deletion** must remove or anonymize personal data per applicable regulations. For MVP, account deletion requests are handled through an administrative/support process (no self-service deletion endpoint or UI); self-service account deletion and ownership-transfer workflows are post-MVP
- **Household data export** is not required for MVP but should not be blocked by system design

---

## System Design & Implementation Guidance

The following items are implementation decisions and belong in a separate System Design document:

- Architecture pattern (layered, microservices, monolithic, etc.)
- Technology stack (frontend framework, backend runtime, database, authentication mechanism)
- Real-time synchronization mechanism (polling interval, WebSocket, SSE) — API-based with cache invalidation is MVP
- Domain isolation and module structure for independent evolution
- API design (REST vs. GraphQL) and versioning strategy
- Session management mechanism (JWT, sessions, tokens)
- Password hashing algorithm
- Logging and monitoring infrastructure
- Data retention and deletion policies
- Backup and disaster recovery procedures
- Scaling strategy for growth beyond MVP
- Future extensibility for roles (Admin, Restricted Member, Guest)
- Future expense-splitting data model (should not block MVP design)

---

## Success Metrics

### MVP Launch Criteria

**Product Success:**
- New user can complete signup → household creation → member invitation → first task in < 5 minutes without external documentation
- No critical bugs affecting core workflows (invitations, task creation/assignment, shopping list management)
- User can understand their permissions and intended actions without confusion

**System Reliability & Security (Definition of Done):**
- No security vulnerabilities allowing cross-household data access
- No data loss due to application failure
- Core API endpoints respond in acceptable time for normal household sizes
- User authentication is secure (no session hijacking, brute-force attacks, plaintext credentials)
- Deleted household data is unrecoverable (or recoverable only for defined retention period)

### Post-Launch Product Metrics

- **Household Adoption:** % of created households with 2+ active members (indicates households are multi-person, not just testing)
- **Engagement:** Avg tasks created per household per week (measures ongoing use)
- **Effectiveness:** % of created tasks marked complete (measures value/usability)
- **Retention:** % of users active 30 days after signup (measures product-market fit)

---

## Roadmap & Post-MVP Iterations

### Iteration 2 (Enhanced Collaboration)

- Recurring task automation (configure frequency, auto-generate instances)
- In-app and email notifications for task assignments, household changes, and approaching deadlines
- Task history and audit log (who completed tasks, when)
- Activity feed showing recent household changes

### Iteration 3 (Financial Features)

- Expense splitting (record which members are responsible for sharing an expense)
- Settlement tracking (who owes whom, payment status)
- Expense categories custom to household
- Receipt/attachment support for expenses

### Iteration 4 (Advanced Collaboration & Views)

- Advanced member roles (Admin with permission management, Restricted Member with view-only, Guest with temporary access)
- Calendar view for tasks with due dates
- Task comments and @mentions for discussion
- File/image attachments on tasks and expenses
- Household activity feed with more granular event details

### Iteration 5+ (Extensions & Mobile)

- Mobile native app (iOS/Android)
- Third-party integrations (Google Calendar sync, Slack notifications, etc.)
- Household analytics and reporting (spending trends, task completion rates, member contributions)
- Guest invitations for temporary household access
- Multi-language support
- User profile customization (avatars, display names, preferences)

---

## MVP Constraints & Dependencies

- **Authentication:** MVP supports email/password + Google OAuth only. Architecture must allow adding additional providers (GitHub, Microsoft, Apple) in post-MVP iterations without major refactoring.
- **Synchronization:** API-based synchronization with cache invalidation is sufficient for MVP. Real-time WebSocket synchronization and offline queueing are post-MVP considerations.
- **Household Deletion:** Deleted households must be recoverable for a defined retention period. Exact retention duration is a System Design decision (e.g., 30 days).
- **Multi-Household:** MVP supports users in multiple households with one currently active household context. User must explicitly switch households to access their data.
- **Scalability:** MVP targets support for < 100 active households during launch. Architecture should support growth to 10k+ households without fundamental redesign.
- **Data Model:** Expense data model should not preclude post-MVP expense-splitting implementation (e.g., allow recording of multiple payers without data migration).

---

## Resolved Decisions (for reference)

The following questions were resolved during PRD review:

1. ✓ **Real-Time Synchronization:** API-based synchronization with cache invalidation is MVP; WebSocket/SSE is post-MVP
2. ✓ **Task Authorization:** Any member can create and assign tasks; creator/owner can reassign/delete
3. ✓ **Soft Deletion:** Only household deletion is soft; individual entities are permanently deleted in MVP
4. ✓ **Dashboard:** Intentionally minimal (name, members, pending tasks, due soon, shopping summary, quick actions)
5. ✓ **Household Deletion:** Recoverable, not permanent; retention period is System Design decision
6. ✓ **Member Removal:** Content is preserved; tasks become unassigned
7. ✓ **Multi-Household:** Users can belong to multiple households; one active context at a time
8. ✓ **Invitation Flow:** Support both existing and new users; email invite + household code options
9. ✓ **Notifications:** Deferred to post-MVP (except transactional emails)
10. ✓ **Recurring Tasks:** Deferred to post-MVP; no metadata in MVP

---

## Remaining Open Questions for System Design

1. ✓ **Retention Period:** Resolved — 30 days (see SYSTEM_DESIGN.md "Household Deletion Behavior")
2. ✓ **Session Lifetime:** Resolved — 14 days, database-backed Django sessions (see SYSTEM_DESIGN.md "Session Management")
3. ✓ **Household Code Format:** Resolved — 8-character alphanumeric, unique, regeneration invalidates the old code immediately (see SYSTEM_DESIGN.md, DOMAIN_MODEL_CORRECTED.md)
4. ✓ **Invitation Expiration:** Resolved — 30 days (see DOMAIN_MODEL_CORRECTED.md, Backend#14)
5. **GDPR Compliance:** What data retention and deletion policies apply based on user jurisdiction? (still open)
6. **Audit Log Retention:** How long should critical action logs be retained for audit purposes? (still open; audit logging itself is scoped in Backend#33)
7. **Performance Targets:** What are the specific response time SLAs for core API endpoints? (still open)
8. **Concurrent User Capacity:** What is the target number of concurrent users per household during MVP? (still open)
9. ✓ **Database Technology:** Resolved — PostgreSQL 14+ (see SYSTEM_DESIGN.md)
10. ✓ **Authentication Mechanism:** Resolved — database-backed Django sessions with HTTP-only cookies, not JWT (see SYSTEM_DESIGN.md "Session Management")

---

## Summary

The HouseHoldHub MVP is a secure, collaborative household management platform that enables trusted household members to organize and coordinate shared tasks, shopping, expenses, and inventory.

**Core Design Principles:**
- **Trusted collaboration:** Household members are treated as collaborators with explicit authorization per action, not adversaries
- **Simple and focused:** Only features required for the core workflows; no unnecessary complexity
- **Extensible foundation:** Architecture supports independent post-MVP domain evolution (recurring tasks, notifications, expense splitting, advanced roles)
- **Product-focused PRD:** Describes what the system must do; implementation decisions are deferred to System Design

**MVP Scope:**
- **Foundational:** User authentication (email/password + Google), household creation/management, member invitations and management
- **Primary workflows:** Task creation, assignment, and completion; Shopping list management
- **Secondary workflows:** Expense logging, inventory tracking
- **Explicit authorization:** Clear rules for who can create, edit, delete, and assign resources within a household
- **API-based synchronization:** Sufficiently fresh data for normal usage; real-time WebSocket is post-MVP

**Success:** New users can create an account, form a household, invite a member, and create their first shared task in under 5 minutes without documentation. The platform is secure (no data leaks, proper authentication), reliable (data is persisted), and usable (clear permissions and workflows).
