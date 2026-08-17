# HouseHoldHub MVP - System Design Document

**Version:** 3.0 (Decisions Resolved)  
**Date:** August 16, 2026  
**Status:** MVP Architecture Complete, Ready for Domain Model Review  
**Source of Truth:** `tasks/prd-householdhub-mvp.md`

---

## Executive Summary

HouseHoldHub MVP is a collaborative household management web application that enables trusted household members to organize tasks, shopping, expenses, and inventory. This System Design translates product requirements into concrete technical architecture with all critical decisions resolved.

**Resolved Technology Stack:**
- **Backend:** Python + Django + Django REST Framework
- **Database:** PostgreSQL 14+ with Django ORM migrations
- **Authentication:** Django session-based with HTTP-only secure cookies
- **Sessions:** Database-backed (Django sessions table)
- **Frontend:** React 18+ with TypeScript
- **Frontend State:** TanStack Query (React Query) for server-state management
- **API Style:** REST with resource-oriented endpoints
- **Development:** Docker Compose (PostgreSQL, Django, React)
- **Deployment:** Platform-neutral (Docker-based); platform chosen post-MVP

**Architectural Patterns:**
- **Concurrency:** Last-write-wins with optional conflict detection per entity
- **Authorization:** Household membership scoping at database and application layers
- **Task Assignment:** Single assignee per task (nullable assignment to Membership, not User)
- **Synchronization:** API-based with cache invalidation (no real-time transport)

**NOT Included in MVP:**
- Redis (may be added post-MVP for caching/scaling)
- Background worker queues (async tasks can be added later)
- WebSockets/Server-Sent Events (polling-based sync sufficient)
- Message brokers (single-server architecture)
- Distributed tracing (request IDs + structured logging sufficient)

---

## Part 1: Technology Decisions

### 1. Backend Framework: Django + Django REST Framework

**Decision:** Use Python + Django + Django REST Framework for the backend

**Rationale:**
- Mature, battle-tested framework with 15+ years of production use
- Excellent authentication and session management (built-in, no custom code needed)
- Powerful ORM with migrations, relationships, querysets
- Built-in security protections (CSRF, XSS, SQL injection prevention)
- Well-suited to relational, permission-heavy applications (household scoping, authorization)
- Excellent fit with PostgreSQL (native support, JSON operators, etc.)
- Django REST Framework adds declarative API endpoints with validation, serialization, pagination
- Reduces the amount of custom infrastructure required for MVP

**Alternatives Considered:**
- FastAPI: Modern, async-first, but overkill for MVP; requires more custom auth/ORM work
- Express/Node.js: Functional but less mature defaults for security and permissions
- Flask: Lightweight but requires more custom work for auth/ORM/validation

**Trade-offs:**
- Django has some conventions and boilerplate (acceptable for long-term maintainability)
- Larger framework (good: fewer dependencies to manage; bad: more to learn)
- Python may be slower than Node.js/Go (acceptable for household-scale application)

**Risks:**
- Team must have Python expertise (or be willing to learn Django)
- Dependency on Django security updates (mitigated by active community)

**Migration Path:**
- Start with Django for MVP simplicity
- Can migrate to FastAPI/Express if performance becomes critical (unlikely for 10k-100k households)

---

### 2. Database: PostgreSQL with Django ORM

**Decision:** PostgreSQL 14+ with Django ORM for all database interactions

**Rationale:**
- Relational model aligns perfectly with domain entities and relationships
- ACID transactions important for financial consistency (expenses)
- Full-featured query language and operators (JSON, arrays, full-text search)
- Django ORM provides type-safe querysets, migrations, validation
- Scales from single instance (MVP) to enterprise without fundamental changes
- Row-level security available for future household isolation optimization

**Migrations:**
- Use Django migrations exclusively (not Liquibase/Flyway)
- Migrations are Python files, integrated with Django development workflow
- Apply automatically on deployment with `python manage.py migrate`

**MVP Deployment:**
- Single PostgreSQL instance (not Multi-AZ, not replicated)
- Backups via database provider (Docker volume for dev, RDS/Heroku for production)

---

### 3. Session Management: Database-Backed Django Sessions

**Decision:** Use Django's database-backed session engine (not Redis) for MVP

**Rationale:**
- Django provides built-in session middleware and database backend
- No additional dependency; uses same PostgreSQL database
- Simple, secure, and sufficient for MVP scale (100-10k sessions)
- User login/logout, session expiration all built-in
- Backward-compatible with authentication system

**Session Lifecycle:**
- Session created on login via `django.contrib.auth.login()`
- Stored in `django_session` table with session_id, session_data, expire_date
- Automatic cleanup: Django provides `clearsessions` management command (can run nightly)
- Expires after TTL (configurable, default 2 weeks)
- HTTP-only, Secure, SameSite=Strict cookies set automatically

**Migration Path (if needed post-MVP):**
- Migrate to Redis caching layer if:
  - Scaling to 100k+ concurrent sessions
  - Session lookups become bottleneck
  - Caching other data becomes necessary
- Process:
  1. Add Redis as optional cache backend (not session backend)
  2. Cache frequently-accessed queries (household memberships, user permissions)
  3. Later, move session backend to Redis if database queries exceed acceptable latency
- **Critical:** Ensure application code doesn't depend on Redis; treat as optional cache

**Redis NOT Required for MVP:**
- No Redis cluster, no single Redis instance required
- Database sessions sufficient for expected MVP scale
- Cost savings: ~$0.50-2/hour if would have used Redis

---

### 4. API Design: REST with Django REST Framework

**Decision:** REST API with resource-oriented endpoints using Django REST Framework

**Rationale:**
- REST is familiar, well-standardized, easy to implement and test
- Django REST Framework provides validation, serialization, pagination, filtering
- Easy to version and deprecate endpoints (url versioning via /api/v1/, /api/v2/)
- Can extend to GraphQL post-MVP without breaking REST API

**Implementation:**
- Django REST Framework class-based views (ViewSet, ModelViewSet)
- Serializers for request validation and response serialization
- Built-in pagination (page/limit), filtering, sorting
- Built-in authentication: Django session authentication
- Built-in permissions: Custom permission classes for household membership checks

---

### 5. Frontend: React 18+ with TypeScript

**Decision:** React 18+ with TypeScript, TanStack Query, React Router, Tailwind CSS

**Rationale:**
- React is mature, widely-adopted, excellent component model
- TypeScript provides type safety for large applications
- TanStack Query (React Query) explicitly designed for server-state management
- React Router v6 for client-side navigation
- Tailwind CSS for rapid UI development without custom CSS

**Components:**
- React 18+ with functional components and hooks
- TanStack Query for API caching, background refetch, loading states
- React Hook Form for form validation and submission
- Zod for schema validation (types + runtime)
- Protected routes with authentication context
- Active household context for multi-household support

**Build & Development:**
- Vite or Create React App for development server
- TypeScript for type checking
- ESLint + Prettier for code quality
- Docker container for deployment

---

### 6. Concurrency Model: Last-Write-Wins

**Decision:** Last-write-wins for MVP with optional conflict detection for high-contention entities

**Implementation:**
- All mutable entities include `updated_at` timestamp
- For most entities: Accept latest write unconditionally
- For high-contention entities (shopping/inventory): Optional version checking
  - Client includes `updated_at` in PATCH/PUT request
  - Server compares timestamp; if stale, return 409 Conflict
  - Client refetches and retries with latest data

**Per-Entity Conflict Detection:**

| Entity | Contention Level | Conflict Detection |
|--------|------------------|-------------------|
| Task title/description | Low | No (accept last write) |
| Task assignment | Low | No (accept last write) |
| Expense | Very low | No (accept last write) |
| Shopping item purchased status | Medium | Optional (can detect conflicts) |
| Inventory quantity | Medium | Optional (can detect conflicts) |

**Rationale:**
- PRD allows last-write-wins for MVP
- Household members are trusted (unlikely to edit simultaneously)
- Page refresh on focus mitigates stale data
- Full conflict resolution UI deferred to post-MVP

---

### 7. Authorization: Household-Scoped Membership

**Decision:** Household membership enforced at database, middleware, and application layers

**Implementation:**
1. **Database Layer:** All queries include `WHERE household_id IN (user's household_ids)`
2. **Middleware Layer:** Verify user is member of requested household before route handler
3. **Application Layer:** Check object-level permissions (creator/owner can delete, etc.)
4. **API Layer:** Return 403 Forbidden for unauthorized access

**Role-Based Permissions:**

| Action | Owner | Member |
|--------|-------|--------|
| Create task | ✓ | ✓ |
| Edit task (ordinary fields: title, description, due_date)† | ✓ | ✓ (any member) |
| Delete task | ✓ | Creator only |
| Assign task (at creation) | ✓ | ✓ (any member) |
| Reassign task (change/clear assignment after creation) | ✓ | Creator only |
| Complete/un-complete task | ✓ (any task) | Assigned member only if assigned; any active member if unassigned |
| Delete household | ✓ | ✗ |
| Invite member | ✓ | ✗ |
| Remove member | ✓ | ✗ |
| View household data | ✓ | ✓ (all members) |

**† Field-level authorization on `PATCH /tasks/{id}`:** the `assigned_to_id` field is excluded from the "any member can edit" grant. Non-creator, non-owner members may update title/description/due_date via this endpoint, but a request that also changes `assigned_to_id` must be rejected (403) unless the requester is the task's creator or the Household Owner. Enforced at the serializer/permission layer, not by exposing a separate endpoint.

---

## Part 2: Domain Model (Final)

### Core Entities & Relationships

#### 1. User
```
Attributes:
  - id: UUID (primary key)
  - email: string (unique, indexed)
  - password_hash: string (bcrypt/Argon2)
  - name: string
  - google_id: string (nullable, for OAuth)
  - created_at: timestamp
  - updated_at: timestamp
  - deleted_at: timestamp (nullable, soft-delete only)

Ownership:
  - Owns multiple Household records (household.owner_id → user.id)
  - Created at signup or first OAuth login
  - Soft-deleted on account deletion; personal data anonymized in household contexts
  - Cannot be deleted while owning active households

Lifetime:
  - Created: signup or OAuth first login
  - Active: can authenticate, access owned/member households
  - Soft-Deleted: deleted_at set; cannot authenticate; marked as "deleted user" in household content
  - Hard-Deleted: after retention period — not fixed for MVP; account deletion is administrative/case-by-case (self-service deletion is post-MVP, per PD-4), so no defined self-service TTL applies yet

Foreign Keys:
  - None (users don't depend on households; households depend on users)
```

#### 2. Household
```
Attributes:
  - id: UUID (primary key)
  - name: string
  - description: string (nullable)
  - code: string (unique, indexed, shareable household code)
  - owner_id: UUID → User (foreign key, on delete PROTECT)
  - created_at: timestamp
  - updated_at: timestamp
  - deleted_at: timestamp (nullable, soft-delete)

Ownership:
  - Every household has exactly one owner (user)
  - Owner cannot be changed; only owner can delete household
  - owner_id is PROTECT: a user who owns a household cannot be hard-deleted until ownership is transferred. Self-service account deletion and ownership transfer are post-MVP (per PD-4); MVP account deletion is an administrative/support process only.

Children:
  - Multiple Membership records (household_id → membership.household_id)
  - Multiple Task records (household_id → task.household_id)
  - Multiple ShoppingItem records (household_id → shopping_item.household_id)
  - Multiple Expense records (household_id → expense.household_id)
  - Multiple InventoryItem records (household_id → inventory_item.household_id)
  - Multiple Invitation records (household_id → invitation.household_id)

Lifetime:
  - Created: user creates household; user becomes owner
  - Active: members can access and modify household data
  - Soft-Deleted: deleted_at set; members immediately lose access; all child data (Memberships, Tasks, ShoppingItems, Expenses, InventoryItems, Invitations) is PRESERVED, not deleted; recoverable for 30 days
  - Hard-Deleted: after the 30-day retention period; all child data cascade-deleted (irreversible)

Foreign Key Behavior:
  - Membership records: CASCADE, but only at hard-delete (soft-delete preserves them)
  - Task/Shopping/Expense/Inventory records: CASCADE, but only at hard-delete (soft-delete preserves them)
  - Invitation records: CASCADE, but only at hard-delete (soft-delete preserves them)
  - User (owner_id): PROTECT — hard-delete of the owning user is blocked while the household exists

Uniqueness:
  - code: globally unique; can be regenerated (old code becomes invalid immediately)

Note:
  - Household is the security boundary; all data scoped by household_id
  - Soft-deletion allows recovery (no cascading deletion of children); hard deletion is permanent and cascades to all children
```

#### 3. Membership
```
Attributes:
  - id: UUID (primary key)
  - household_id: UUID → Household (foreign key, on delete CASCADE)
  - user_id: UUID → User (foreign key, on delete CASCADE)
  - role: enum (owner, member)
  - joined_at: timestamp
  - created_at: timestamp

Ownership:
  - No owner; record belongs to household + user combination
  - Unique constraint: (household_id, user_id) — only one membership per household per user

Relationships:
  - References User and Household
  - Referenced by: Task.assigned_to_id (nullable, single assignee per task)

Lifetime:
  - Created: user accepts invitation or joins via household code
  - Active: user can access household data per role permissions
  - Removed: user removed by owner OR user deletes account
  - Hard-Delete: no recovery (immediate access loss)

On Member Removal:
  - Membership hard-deleted immediately
  - User loses access to household
  - User's created tasks/shopping/expenses/inventory remain (attributed to "deleted user" or user_id)
  - Tasks assigned to removed user become unassigned (assigned_to set to NULL)
  - User's name displayed in history ("Task created by User X" even if user_id is null)

On Household Hard-Delete (not soft-delete — see Household Deletion Behavior below):
  - All Membership records hard-deleted (cascade)
  - All users lose access immediately

Foreign Key Behavior:
  - household_id: ON DELETE CASCADE (delete membership if household deleted)
  - user_id: ON DELETE CASCADE (delete membership if user deleted)

Uniqueness:
  - (household_id, user_id): unique constraint — one membership per household per user
```

#### 4. Invitation
```
Attributes:
  - id: UUID (primary key)
  - household_id: UUID → Household (foreign key, on delete CASCADE)
  - email: string (email of invited user)
  - token_hash: string (hashed; plaintext never stored)
  - state: enum (pending, accepted, revoked, expired)
  - created_at: timestamp
  - expires_at: timestamp
  - accepted_at: timestamp (nullable, when invitation accepted)

Ownership:
  - Created by household owner
  - Only owner can revoke invitations

Lifetime:
  - Pending: awaiting user action (accept or expiration)
  - Accepted: user clicked link and created/verified account; user added to Membership
  - Revoked: owner revoked invitation before expiration
  - Expired: TTL passed without acceptance

Security:
  - token: 32 bytes random, base64 encoded, hashed before storage (SHA-256)
  - Token includes both email and token_hash in database for verification
  - One-time use: token marked as used immediately after acceptance
  - Expiration: after 30-day TTL, state set to expired

Foreign Key Behavior:
  - household_id: ON DELETE CASCADE (delete invitation if household deleted)

On Invitation Accepted:
  - Check if user with that email exists
  - If exists: Add Membership record for that user
  - If not exists: Create User record, then add Membership
  - Mark Invitation.state = accepted, accepted_at = now()

Note:
  - Email invitations are for existing users
  - Household code is alternative join method (no expiration)
```

#### 5. Task
```
Attributes:
  - id: UUID (primary key)
  - household_id: UUID → Household (foreign key, on delete CASCADE)
  - title: string
  - description: string (nullable)
  - due_date: date (nullable)
  - created_by_id: UUID → User (foreign key, on delete set null)
  - assigned_to_id: UUID → Membership (foreign key, on delete set null, nullable)
  - completed: boolean (default false)
  - completed_by_id: UUID → User (foreign key, on delete set null, nullable)
  - completed_at: timestamp (nullable)
  - created_at: timestamp
  - updated_at: timestamp

Ownership:
  - Created by: household member (created_by_id)
  - Completed by: assigned member or household owner; if the task is unassigned, any active household member (see Assignment Model below)
  - Can reassign: creator or owner
  - Can delete: creator or owner

Assignment Model:
  - assigned_to_id: nullable reference to Membership (not User)
  - Rationale: Assignment must be scoped to household membership; if user is removed from household, task becomes unassigned
  - Single assignee per task (not TaskAssignment entity for MVP)
  - Zero assignees: task is open; any member can complete it
  - One assignee: assigned member can complete it; other members cannot mark complete (owner can always complete)

Lifetime:
  - Created: any member creates task; status = open
  - Assigned: creator or member assigns to another member
  - Completed: assigned member/owner (or any active member if unassigned) marks completed (completed_at = now(), completed = true)
  - Un-completed: same actors may set completed = false; completed_at is cleared (set to NULL) — not immutable
  - Deleted: creator or owner deletes (hard-delete, no recovery)

On Member Removal:
  - If task assigned to removed member: assigned_to_id set to NULL (task becomes unassigned)
  - Task remains in household
  - History preserved: created_by_id unchanged (user still referenced in "created by X")

On Household Hard-Delete (not soft-delete — see Household Deletion Behavior below):
  - All tasks hard-deleted (cascade)

Foreign Key Behavior:
  - household_id: ON DELETE CASCADE
  - created_by_id: ON DELETE SET NULL (task remains if creator deleted)
  - assigned_to_id: ON DELETE SET NULL (task becomes unassigned if member removed)
  - completed_by_id: ON DELETE SET NULL

Notes:
  - No recurring task metadata (post-MVP feature)
  - No comments or attachments (post-MVP feature)
  - Completion tracking simple: boolean + timestamp (not audit log for MVP)
```

#### 6. ShoppingItem
```
Attributes:
  - id: UUID (primary key)
  - household_id: UUID → Household (foreign key, on delete CASCADE)
  - name: string
  - quantity: string (nullable, e.g., "2 lbs", "1 dozen")
  - purchased: boolean (default false)
  - purchased_by_id: UUID → User (foreign key, on delete set null, nullable)
  - purchased_at: timestamp (nullable)
  - created_by_id: UUID → User (foreign key, on delete set null)
  - created_at: timestamp
  - updated_at: timestamp

Ownership:
  - Created by: household member (created_by_id)
  - Can edit: any member
  - Can delete: creator or owner
  - Marked purchased by: any member

Lifetime:
  - Created: any member adds shopping item; purchased = false
  - Updated: any member updates quantity/name
  - Marked Purchased: any member marks purchased (purchased = true, purchased_by_id = current_user, purchased_at = now())
  - Toggled: any member can toggle between purchased/unpurchased (resets purchased_by, purchased_at)
  - Deleted: creator or owner deletes (hard-delete, no recovery)

On Household Hard-Delete (not soft-delete — see Household Deletion Behavior below):
  - All shopping items hard-deleted (cascade)

Foreign Key Behavior:
  - household_id: ON DELETE CASCADE
  - created_by_id: ON DELETE SET NULL
  - purchased_by_id: ON DELETE SET NULL

Notes:
  - No purchased item recovery; deleted items are gone
  - No grouping/categorization for MVP (post-MVP feature)
  - Simple list-based interface (no drag-drop, no sorting for MVP)
```

#### 7. Expense
```
Attributes:
  - id: UUID (primary key)
  - household_id: UUID → Household (foreign key, on delete CASCADE)
  - amount_cents: integer (no decimals; 1 USD = 100 cents)
  - category: enum (Food, Utilities, Maintenance, Entertainment, Other)
  - payer_id: UUID → User (foreign key, on delete set null, nullable)
  - description: string (nullable)
  - created_by_id: UUID → User (foreign key, on delete set null)
  - created_at: timestamp
  - updated_at: timestamp

Ownership:
  - Created by: household member (created_by_id)
  - Can edit: creator or owner
  - Can delete: creator or owner
  - Payer: user who paid for the expense (may differ from creator)

Payer Default:
  - If payer_id not specified: defaults to created_by_id
  - Payer immutable after creation (to avoid changing history)

Lifetime:
  - Created: any member logs expense
  - Updated: creator or owner edits amount/category/description/payer
  - Deleted: creator or owner deletes (hard-delete, no recovery)

On Household Hard-Delete (not soft-delete — see Household Deletion Behavior below):
  - All expenses hard-deleted (cascade)

Foreign Key Behavior:
  - household_id: ON DELETE CASCADE
  - created_by_id: ON DELETE SET NULL
  - payer_id: ON DELETE SET NULL

Notes:
  - No settlement/splitting (post-MVP feature)
  - No currency support (assume single household currency; can add post-MVP)
  - No attachments (post-MVP feature)
  - No expense sharing calculations
```

#### 8. InventoryItem
```
Attributes:
  - id: UUID (primary key)
  - household_id: UUID → Household (foreign key, on delete CASCADE)
  - name: string
  - quantity: integer (positive; not a freeform string)
  - unit: string (nullable; free-form display metadata, e.g., "boxes", "bottles")
  - category: string (nullable, e.g., "pantry", "cleaning supplies")
  - location: string (nullable, e.g., "bedroom closet")
  - created_by_id: UUID → User (foreign key, on delete set null)
  - created_at: timestamp
  - updated_at: timestamp

Ownership:
  - Created by: household member (created_by_id)
  - Can edit: any member (quantity, unit, category, location)
  - Can delete: creator or owner

Lifetime:
  - Created: any member adds inventory item
  - Updated: any member updates quantity or details (increment/decrement modifies quantity numerically)
  - Deleted: creator or owner deletes (hard-delete, no recovery)

On Household Hard-Delete (not soft-delete — see Household Deletion Behavior below):
  - All inventory items hard-deleted (cascade)

Foreign Key Behavior:
  - household_id: ON DELETE CASCADE
  - created_by_id: ON DELETE SET NULL

Notes:
  - No low-stock alerts (post-MVP feature)
  - No expiration tracking (post-MVP feature)
  - Quantity is a positive integer with an optional free-form unit (e.g., quantity=2, unit="boxes")
  - Optional grouping/categorization (can leave category/location blank)
```

---

## Domain Model Validation

### Entity Cardinalities

```
User
  1 : * Household (owner_id)
  1 : * Membership (user_id)
  1 : * Task (created_by_id)
  1 : * Task (completed_by_id)
  1 : * ShoppingItem (created_by_id)
  1 : * ShoppingItem (purchased_by_id)
  1 : * Expense (created_by_id)
  1 : * Expense (payer_id)
  1 : * InventoryItem (created_by_id)

Household
  1 : * Membership (household_id)
  1 : * Task (household_id)
  1 : * ShoppingItem (household_id)
  1 : * Expense (household_id)
  1 : * InventoryItem (household_id)
  1 : * Invitation (household_id)
  1 : 1 User (owner_id)

Membership
  * : 1 Household (household_id)
  * : 1 User (user_id)
  1 : * Task (assigned_to_id) [nullable]

Task
  * : 1 Household (household_id)
  * : 1 User (created_by_id) [nullable on delete]
  * : 1 User (completed_by_id) [nullable on delete]
  * : 1 Membership (assigned_to_id) [nullable, ON DELETE SET NULL]

ShoppingItem
  * : 1 Household (household_id)
  * : 1 User (created_by_id) [nullable on delete]
  * : 1 User (purchased_by_id) [nullable on delete]

Expense
  * : 1 Household (household_id)
  * : 1 User (created_by_id) [nullable on delete]
  * : 1 User (payer_id) [nullable on delete]

InventoryItem
  * : 1 Household (household_id)
  * : 1 User (created_by_id) [nullable on delete]

Invitation
  * : 1 Household (household_id)
```

### Household Scoping Verification

**All entities scoped by household_id:**
✓ Membership: household_id (users can only see members of their households)
✓ Task: household_id (tasks only visible to household members)
✓ ShoppingItem: household_id (items only visible to household members)
✓ Expense: household_id (expenses only visible to household members)
✓ InventoryItem: household_id (items only visible to household members)
✓ Invitation: household_id (invitations only visible to household owner/members)

**Query Pattern:**
```
SELECT * FROM task 
WHERE household_id IN (
  SELECT household_id FROM membership WHERE user_id = current_user_id
)
```

### Ownership vs. Authorship

| Entity | Author (who created) | Owner (who can delete) | Notes |
|--------|----------------------|------------------------|-------|
| User | Self (signup) | Self or admin | User can delete own account |
| Household | User (creates) | User (owner_id) | Only owner can delete |
| Membership | Invitation or join | Household owner | Owner can remove members |
| Task | Member (created_by) | Creator or owner | Creator or owner can delete |
| ShoppingItem | Member (created_by) | Creator or owner | Creator or owner can delete |
| Expense | Member (created_by) | Creator or owner | Creator or owner can delete |
| InventoryItem | Member (created_by) | Creator or owner | Creator or owner can delete |
| Invitation | Household owner | Household owner | Only owner can revoke |

### Member Removal Behavior

**When a member is removed from a household:**

1. **Membership record:** Hard-deleted immediately
2. **User access:** User can no longer see/access household
3. **User data in household:** Preserved (attribution remains)
4. **Tasks:** If assigned to removed member, assignment cleared (assigned_to_id = NULL)
5. **Task creation attribution:** Remains (created_by_id unchanged, references user by name)
6. **Shopping items:** Created by removed member remain (created_by_id unchanged)
7. **Expenses:** Created by removed member remain (created_by_id unchanged)
8. **Inventory:** Created by removed member remain (created_by_id unchanged)

**UI Display after member removal:**
- Tasks: "Task created by X" (even if X was removed)
- Shopping: "Added by X" (even if X was removed)
- Expenses: "Created by X" (even if X was removed)

### Household Deletion Behavior

**When household is soft-deleted (recoverable):**

1. **Household record:** `deleted_at` set; no physical deletion
2. **User access:** All members lose access immediately (queries filter on `deleted_at IS NULL`)
3. **Membership records:** PRESERVED — no cascading deletion
4. **Task records:** PRESERVED — no cascading deletion
5. **Shopping items:** PRESERVED — no cascading deletion
6. **Expenses:** PRESERVED — no cascading deletion
7. **Inventory:** PRESERVED — no cascading deletion
8. **Invitation records:** PRESERVED — no cascading deletion

**Recovery (within retention period):** Admin clears `deleted_at`; all child data and access are restored exactly as they were — because nothing was cascade-deleted during soft-delete.

**Retention period:** 30 days

**After retention period (hard-delete, irreversible):**
- Household record and all child records (Memberships, Tasks, ShoppingItems, Expenses, InventoryItems, Invitations) are physically deleted via cascade
- No recovery possible
- Cannot be undone

**Purge trigger (who runs the hard-delete):** MVP has no background worker queue (see "NOT Included in MVP" above), so the retention purge is a Django management command (e.g. `python manage.py purge_expired_households`) that queries `Household.objects.filter(deleted_at__lte=now() - 30 days)` and hard-deletes each match. This follows the same pattern already used for session cleanup (`python manage.py clearsessions`, above): scheduled via external cron (or the platform's scheduled-job feature) rather than an in-process worker. Cron scheduling is an Infrastructure/Automation (M9) deployment concern; the command itself is a Backend deliverable.

### Invitation Lifecycle

**Email Invitation (for existing users):**
```
1. Owner initiates: POST /api/v1/households/{id}/members
   { email: "user@example.com" }

2. System checks: Is user with this email already registered?
   - If YES: Create Invitation record (email, token_hash, state=pending)
   - If NO: Create Invitation record + send email

3. Owner can revoke: DELETE /api/v1/households/{id}/invitations/{token}
   - state = revoked (no longer accepted)

4. User accepts: GET /invitation/accept?token=X
   - Hash token, verify it exists and is pending
   - Verify not expired
   - Create Membership record for user + household
   - state = accepted, accepted_at = now()
   - User redirected to household

5. Expiration:
   - If not accepted by expires_at: state = expired
   - User can request new invitation (old one still exists but unusable)
```

**Household Code Join:**
```
1. Owner generates code: POST /api/v1/households/{id}/code
   - Returns: code (e.g., "ABC-DEF-123")
   - Code stored in household.code, never expires, can be regenerated

2. User joins: POST /api/v1/households/join
   { code: "ABC-DEF-123" }

3. System checks:
   - Find household by code
   - Create Membership record for user + household
   - Return household details

4. Code regeneration:
   - POST /api/v1/households/{id}/code/regenerate
   - Generate new code; replace code in household.code
   - Old code becomes invalid immediately (resolved: Option A — no grace period)
```

### Foreign Key Cascade Behavior

**Note:** `household_id` CASCADE below fires only on **hard-delete** of the household (after the 30-day retention period). Household **soft-delete** does not cascade — see [Household Deletion Behavior](#household-deletion-behavior).

| FK | On Delete | Rationale |
|----|-----------|-----------|
| Task.household_id | CASCADE (hard-delete only) | Delete tasks if household hard-deleted |
| Task.created_by_id | SET NULL | Keep task if user deleted; attributed to "deleted user" |
| Task.assigned_to_id | SET NULL | Unassign if membership removed |
| ShoppingItem.household_id | CASCADE (hard-delete only) | Delete items if household hard-deleted |
| ShoppingItem.created_by_id | SET NULL | Keep item if user deleted |
| Expense.household_id | CASCADE (hard-delete only) | Delete expenses if household hard-deleted |
| Expense.created_by_id | SET NULL | Keep expense if user deleted |
| InventoryItem.household_id | CASCADE (hard-delete only) | Delete items if household hard-deleted |
| InventoryItem.created_by_id | SET NULL | Keep item if user deleted |
| Membership.household_id | CASCADE (hard-delete only) | Remove membership if household hard-deleted |
| Membership.user_id | CASCADE | Remove membership if user deleted |

---

## Part 3: Django Implementation Notes

### Django Models

Each entity maps to a Django Model:

```python
# models/user.py
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, indexed=True)
    password_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

# models/household.py
class Household(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True, indexed=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

# models/membership.py
class Membership(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('member', 'Member'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [('household', 'user')]

# models/task.py
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_tasks')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Authentication: Django Contrib Auth

Use Django's built-in authentication:
```python
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import LoginView, LogoutView

class CustomUser(AbstractUser):
    # Extend with household-specific fields if needed
    pass
```

Django provides:
- User model with password hashing
- Authentication middleware
- Login/logout views
- Permission framework
- Session management

### Session Management: Django Session Framework

```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks (configurable)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Set True in production
SESSION_COOKIE_SAMESITE = 'Strict'
```

Django provides:
- Session table (`django_session`)
- Automatic session cleanup (`python manage.py clearsessions`)
- Session middleware
- Request.session object

### Permissions & Authorization

Use Django's permission framework + custom permission checks:

```python
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission

class IsHouseholdMember(BasePermission):
    """User must be member of the household"""
    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(
            household=obj.household,
            user=request.user
        ).exists()

class CanDeleteTask(BasePermission):
    """User must be creator or household owner"""
    def has_object_permission(self, request, view, obj):
        is_creator = obj.created_by == request.user
        is_owner = obj.household.owner == request.user
        return is_creator or is_owner

class CanReassignTask(BasePermission):
    """Field-level check: only creator or household owner may change assigned_to_id.
    Applied in the Task serializer/view on PATCH when 'assigned_to_id' is present
    in the request payload; other fields (title, description, due_date) remain
    editable by any household member regardless of this check."""
    def has_object_permission(self, request, view, obj):
        is_creator = obj.created_by == request.user
        is_owner = obj.household.owner == request.user
        return is_creator or is_owner
```

---

## Part 4: REST API Design

### Endpoint Structure

```
/api/v1/
├── auth/
│   ├── signup           (POST)
│   ├── login            (POST)
│   ├── logout           (POST)
│   ├── me               (GET) — current user
│   ├── forgot-password  (POST)
│   └── reset-password   (POST)
├── households/
│   ├── /                (GET list, POST create)
│   ├── /{id}            (GET, PATCH edit, DELETE soft-delete)
│   ├── /{id}/code       (GET generate code, POST regenerate)
│   ├── /{id}/members    (GET list members)
│   │   └── POST         (invite by email)
│   │   └── /{user_id} DELETE (remove member)
│   ├── /{id}/join       (POST join by code)
│   ├── /{id}/invitations (GET list, DELETE revoke)
│   │   └── /{token}/accept (POST accept invitation)
│   └── /{id}/
│       ├── tasks        (GET list, POST create)
│       │   └── /{task_id} (GET, PATCH, DELETE)
│       │       └── /complete (PATCH)
│       ├── shopping     (GET list, POST create)
│       │   └── /{item_id} (GET, PATCH, DELETE)
│       ├── expenses     (GET list, POST create)
│       │   └── /{expense_id} (GET, PATCH, DELETE)
│       └── inventory    (GET list, POST create)
│           └── /{item_id} (GET, PATCH, DELETE)
```

---

## Part 5: Database Migrations

### Django Migrations

```bash
# Create migrations from models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Revert specific migration (if needed)
python manage.py migrate app_name 0001
```

### Initial Schema

Use Django ORM to define schema in models.py; migrations generated automatically.

Example migration file (auto-generated):
```python
# migrations/0001_initial.py
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    initial = True
    
    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                # ... more fields
            ],
        ),
        # ... more models
    ]
```

---

## Part 6: Development & Testing

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: householdhub
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./Backend
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://dev:dev@db:5432/householdhub
      DEBUG: "true"
    depends_on:
      - db
    volumes:
      - ./Backend:/app

  frontend:
    build: ./Frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000/api/v1
    depends_on:
      - backend
    volumes:
      - ./Frontend:/app

volumes:
  postgres_data:
```

### Testing Strategy

**Unit Tests:**
- Test models, serializers, validators in isolation
- Use pytest + pytest-django

**Integration Tests:**
- Test API endpoints with real database
- Verify authorization enforcement
- Verify household isolation

**Authorization Tests (Critical):**
- Test owner can delete
- Test member cannot delete
- Test cross-household access prevention
- Test creator can delete own resources

---

## Summary: MVP Stack

**Backend:**
- Python 3.9+
- Django 4.2+ (LTS)
- Django REST Framework
- PostgreSQL 14+ client (psycopg2)
- Python Decouple (environment variables)
- Pytest + pytest-django (testing)

**Frontend:**
- Node.js 18+
- React 18+
- TypeScript
- TanStack Query
- React Router v6
- React Hook Form
- Tailwind CSS
- Vite (or CRA)

**Development:**
- Docker & Docker Compose
- Git

**Deployment (TBD):**
- Platform-agnostic (Docker containers)
- PostgreSQL managed (Heroku/AWS RDS/etc.)
- Django settings for environment (DEBUG, SECRET_KEY, ALLOWED_HOSTS, etc.)

---

## Next Steps

1. **Domain Model Review** — Validate entity definitions, cardinalities, FK behavior above
2. **Create ADRs** — Document the 8 architectural decisions
3. **Implementation Planning** — Break down into tasks and sprints
4. **Setup Project** — Create Backend/Frontend directory structure, Django project, React app
5. **Begin Development** — Start with authentication + household management

---

