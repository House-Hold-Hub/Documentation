# HouseHoldHub MVP - Corrected Domain Model with Deletion Semantics

**Date:** August 16, 2026  
**Status:** Final (Ready for ERD & OpenAPI)

---

## Core Principles

1. **Household Scoping:** All data scoped by household_id; users access only their household data
2. **Soft-Delete Preservation:** Soft-delete must preserve data for recovery (no cascading during soft-delete)
3. **Hard-Delete Cascading:** Only irreversible hard-delete can cascade-delete child records
4. **Historical Attribution:** User-created data remains attributed even if user deleted
5. **Ownership Protection:** Households must always have valid ownership strategy

---

## Deletion Semantics: Soft vs. Hard

### Soft-Delete (Reversible, Recoverable)

**Soft-delete operation:**
- Set `deleted_at = now()` 
- **NO cascading deletions** (preserve data for recovery)
- Users lose access immediately
- Data remains in database, marked as deleted

**Recovery (within retention period):**
- Clear `deleted_at` timestamp
- Users regain access
- All child data restored

**Example: Soft-delete household**
```
Household.deleted_at = now()  ← Soft-delete
↓
Users lose access immediately
↓
Memberships, Tasks, Shopping, Expenses, Inventory REMAIN in database
↓
Within 30-day recovery window: Admin can recover household
↓
After 30 days: Transition to hard-delete (irreversible)
```

### Hard-Delete (Irreversible, Permanent)

**Hard-delete operation (only after soft-delete retention period):**
- Physically remove all records
- Cascade-delete child records
- No recovery possible
- Permanent deletion

**Example: Hard-delete household (after retention period)**
```
Household already soft-deleted for 30+ days
↓
Hard-delete triggers:
  - DELETE household record
  - DELETE all Membership records (cascade)
  - DELETE all Task records (cascade)
  - DELETE all ShoppingItem records (cascade)
  - DELETE all Expense records (cascade)
  - DELETE all InventoryItem records (cascade)
  - DELETE all Invitation records (cascade)
↓
No recovery possible
```

---

## Entity Definitions (With Deletion Semantics)

### 1. User

**Purpose:** Account and identity for authentication

**Key Attributes:**
- id (UUID)
- email (unique, indexed)
- password_hash (bcrypt/Argon2)
- name (display name)
- google_id (nullable, for OAuth)
- created_at, updated_at, deleted_at (soft-delete only)

**Relationships:**
- Owns multiple Households (1:N) 
- Participates in multiple Memberships (1:N)
- Creates/completes Tasks, ShoppingItems, Expenses, InventoryItems (1:N)

**Household Ownership & Deletion Strategy:**

| Scenario | Behavior | Rationale |
|----------|----------|-----------|
| User account deleted (MVP: administrative/support process only; no self-service endpoint) | Soft-delete user; user cannot authenticate | Self-service deletion is post-MVP |
| User soft-deleted; owns household | Household remains; ownership unchanged | Preserve household for other members |
| User soft-deleted for 30+ days; owns household | **Resolved (Option A):** PROTECT FK blocks hard-delete until ownership is transferred | Cannot hard-delete a user who owns an active household |

**Foreign Key Strategy for User Deletion:**
- Household.owner_id: **PROTECT** (prevent deletion if user owns households) — **Option A, chosen for MVP:** requires ownership transfer before hard-delete
  - Option B (anonymize household owner) and Option C (auto-designate new owner from members) are deferred; self-service deletion and ownership-transfer UI are post-MVP per PD-4
- Task.created_by_id: **SET NULL** (preserve task; attribute as "deleted user")
- Task.completed_by_id: **SET NULL** (preserve completion record)
- ShoppingItem.created_by_id: **SET NULL** (preserve item; attribute as "deleted user")
- ShoppingItem.purchased_by_id: **SET NULL** (preserve purchase history)
- Expense.created_by_id: **SET NULL** (preserve expense; attribute as "deleted user")
- Expense.payer_id: **SET NULL** (preserve payer information)
- InventoryItem.created_by_id: **SET NULL** (preserve item; attribute as "deleted user")
- Membership.user_id: **CASCADE** (remove membership when user deleted)

**Lifecycle:**
1. User creates account (signup or OAuth)
2. User active: can authenticate and access households
3. Account deleted via administrative/support process (MVP; no self-service endpoint): deleted_at set; cannot authenticate
4. Personal data anonymized: name/email hashed or removed from household contexts
5. After retention period: Hard-delete (requires ownership resolution first)

**Invariant:** A household must never be without a valid owner.

---

### 2. Household

**Purpose:** Container for shared data within a group of cohabiting users

**Key Attributes:**
- id (UUID, PK)
- name, description
- code (unique, shareable join code)
- owner_id (FK→User, PROTECT)
- created_at, updated_at, deleted_at (soft-delete)

**Relationships:**
- Owned by exactly one User (1:1 via owner_id)
- Has multiple Memberships (1:N)
- Contains Tasks, ShoppingItems, Expenses, InventoryItems (1:N each)
- Has Invitations (1:N)

**Soft-Delete (Recoverable):**
```
Household.deleted_at = now()
↓
Users immediately lose access
↓
All child data (Memberships, Tasks, Shopping, Expenses, Inventory, Invitations) 
  REMAINS in database
↓
Data recoverable for 30 days (retention period, confirmed)
↓
Admin can recover: clear deleted_at
```

**Hard-Delete (After Retention Period):**
```
Household.deleted_at is set AND now() > (deleted_at + 30 days)
↓
Hard-delete (irreversible):
  - DELETE Household
  - DELETE all Memberships (cascade)
  - DELETE all Tasks (cascade)
  - DELETE all ShoppingItems (cascade)
  - DELETE all Expenses (cascade)
  - DELETE all InventoryItems (cascade)
  - DELETE all Invitations (cascade)
↓
No recovery possible
```

**Foreign Key Behavior:**
- Household.owner_id → User: **PROTECT** (prevent user deletion if owns household)
- Membership.household_id → Household: **CASCADE** (remove memberships on household hard-delete)
- Task.household_id → Household: **CASCADE** (delete tasks on household hard-delete)
- ShoppingItem.household_id → Household: **CASCADE** (delete items on household hard-delete)
- Expense.household_id → Household: **CASCADE** (delete expenses on household hard-delete)
- InventoryItem.household_id → Household: **CASCADE** (delete items on household hard-delete)
- Invitation.household_id → Household: **CASCADE** (delete invitations on household hard-delete)

**Invariants:**
- Every household has exactly one owner (User)
- Code is globally unique; can be regenerated (invalidates old code)
- All data in household is deleted (cascade) only during hard-delete, never during soft-delete

---

### 3. Membership

**Purpose:** Represents user's membership in a household with role

**Key Attributes:**
- id (UUID, PK)
- household_id (FK→Household)
- user_id (FK→User)
- role (enum: owner, member)
- joined_at, created_at

**Constraints:**
- UNIQUE(household_id, user_id) — only one membership per household per user
- Foreign keys: Both CASCADE on delete

**Relationships:**
- References Household (N:1)
- References User (N:1)
- Referenced by Task.assigned_to (N:1 optional)

**Deletion Behavior:**

| Trigger | Behavior | Rationale |
|---------|----------|-----------|
| Household soft-deleted | Memberships REMAIN (data preserved for recovery) | Recover household → recover memberships |
| Household hard-deleted (after retention) | Memberships CASCADE-deleted | Irreversible household deletion cascades |
| User deleted | Memberships CASCADE-deleted | User account deleted → lose all memberships |
| Member removed by owner | Membership hard-deleted | Immediate access loss |

**Invariants:**
- Only one membership per (household, user) pair
- Role is immutable (cannot change owner→member or vice versa)
- On hard-delete cascade, users lose access immediately

---

### 4. Invitation

**Purpose:** Email invitations to join a household

**Key Attributes:**
- id (UUID, PK)
- household_id (FK→Household)
- email (target email)
- token_hash (SHA-256 hash of token; plaintext never stored)
- state (enum: pending, accepted, revoked, expired)
- created_at, expires_at, accepted_at (nullable)

**Relationships:**
- References Household (N:1)
- Triggers Membership creation on acceptance

**Deletion Behavior:**

| Trigger | Behavior | Rationale |
|---------|----------|-----------|
| Household soft-deleted | Invitations REMAIN (data preserved) | Recover household → recover invitations |
| Household hard-deleted | Invitations CASCADE-deleted | Irreversible deletion cascades |
| Invitation accepted | State = accepted; invitation no longer usable | Cannot re-accept same invitation |
| Invitation revoked | State = revoked; cannot be accepted | Owner can revoke invitations |
| Invitation expires (past expires_at) | State = expired; cannot be accepted | Time-limited invitations |

**Foreign Key Behavior:**
- Invitation.household_id → Household: **CASCADE** (on hard-delete only)

**Invariants:**
- Token is one-time use (marked as used immediately after acceptance)
- Expiration: cannot accept invitation after expires_at
- Revocation: owner can revoke anytime

---

### 5. Task

**Purpose:** Household task or chore

**Key Attributes:**
- id (UUID, PK)
- household_id (FK→Household)
- title, description, due_date
- created_by_id (FK→User, SET NULL)
- assigned_to_id (FK→Membership, SET NULL) ← **Single assignee, not User**
- completed (boolean)
- completed_by_id (FK→User, SET NULL)
- completed_at, created_at, updated_at

**Assignment Model:**
- **Single assignee per task** (nullable)
- References **Membership, not User** (ensures household scoping)
- If assigned member removed from household: assigned_to_id → NULL (task unassigned)
- Zero assignees: task is open; any member can complete

**Deletion Behavior:**

| Trigger | Behavior | Rationale |
|---------|----------|-----------|
| Household soft-deleted | Tasks REMAIN (data preserved) | Recover household → recover tasks |
| Household hard-deleted | Tasks CASCADE-deleted | Irreversible deletion cascades |
| Task deleted by creator/owner | Task hard-deleted | Immediate deletion; no recovery |
| Creator user deleted | Task REMAINS; created_by_id = NULL | Preserve task; attribute as "deleted user" |
| Assigned member deleted/removed | Task REMAINS; assigned_to_id = NULL | Task becomes unassigned |

**Foreign Key Behavior:**
- Task.household_id → Household: **CASCADE** (on hard-delete only)
- Task.created_by_id → User: **SET NULL** (preserve task if creator deleted)
- Task.assigned_to_id → Membership: **SET NULL** (unassign if member removed)
- Task.completed_by_id → User: **SET NULL** (preserve completion record)

**Invariants:**
- Single assignee per task (no multi-assignment in MVP)
- Assigned member or household owner can mark complete; if the task is unassigned, any active household member can mark it complete
- The same rule applies to un-completing (`completed: false`): assigned member/owner, or any active member on an unassigned task
- Creator can reassign or delete
- Owner can delete any task
- `completed_at` is set when `completed` transitions to `true` and cleared (NULL) when it transitions back to `false`; not immutable

---

### 6. ShoppingItem

**Purpose:** Shopping list item

**Key Attributes:**
- id (UUID, PK)
- household_id (FK→Household)
- name, quantity
- purchased (boolean)
- purchased_by_id (FK→User, SET NULL)
- purchased_at, created_by_id, created_at, updated_at

**Deletion Behavior:**

| Trigger | Behavior | Rationale |
|---------|----------|-----------|
| Household soft-deleted | Items REMAIN (data preserved) | Recover household → recover shopping list |
| Household hard-deleted | Items CASCADE-deleted | Irreversible deletion cascades |
| Item deleted by creator/owner | Item hard-deleted | Immediate deletion; no recovery |
| Creator user deleted | Item REMAINS; created_by_id = NULL | Preserve item; attribute as "deleted user" |
| Marked purchased; user deleted | Item REMAINS; purchased_by_id = NULL | Preserve purchase history |

**Foreign Key Behavior:**
- ShoppingItem.household_id → Household: **CASCADE** (on hard-delete only)
- ShoppingItem.created_by_id → User: **SET NULL**
- ShoppingItem.purchased_by_id → User: **SET NULL**

**Invariants:**
- Any member can update item or mark purchased
- Creator or owner can delete
- Purchased items can be toggled back to unpurchased
- No quantity units enforced (freeform string)

---

### 7. Expense

**Purpose:** Household expense (groceries, utilities, etc.)

**Key Attributes:**
- id (UUID, PK)
- household_id (FK→Household)
- amount_cents (integer; no decimals)
- category (enum: Food, Utilities, Maintenance, Entertainment, Other)
- payer_id (FK→User, SET NULL, nullable; defaults to creator)
- description, created_by_id, created_at, updated_at

**Payer Logic:**
- If payer_id not specified on creation: defaults to created_by_id
- Payer immutable after creation (prevent changing historical attribution)

**Deletion Behavior:**

| Trigger | Behavior | Rationale |
|---------|----------|-----------|
| Household soft-deleted | Expenses REMAIN (data preserved) | Recover household → recover expenses |
| Household hard-deleted | Expenses CASCADE-deleted | Irreversible deletion cascades |
| Expense deleted by creator/owner | Expense hard-deleted | Immediate deletion; no recovery |
| Creator user deleted | Expense REMAINS; created_by_id = NULL | Preserve expense; attribute as "deleted user" |
| Payer user deleted | Expense REMAINS; payer_id = NULL | Preserve payer information |

**Foreign Key Behavior:**
- Expense.household_id → Household: **CASCADE** (on hard-delete only)
- Expense.created_by_id → User: **SET NULL**
- Expense.payer_id → User: **SET NULL**

**Invariants:**
- Amount stored in cents (100 = $1.00) to avoid float precision
- Categories are predefined enum
- No currency field (assume single household currency)
- No expense splitting in MVP

---

### 8. InventoryItem

**Purpose:** Household inventory (pantry, supplies, etc.)

**Key Attributes:**
- id (UUID, PK)
- household_id (FK→Household)
- name, quantity (positive integer), unit (nullable string; free-form display metadata, e.g. "boxes", "bottles"), category (nullable), location (nullable)
- created_by_id, created_at, updated_at

**Deletion Behavior:**

| Trigger | Behavior | Rationale |
|---------|----------|-----------|
| Household soft-deleted | Items REMAIN (data preserved) | Recover household → recover inventory |
| Household hard-deleted | Items CASCADE-deleted | Irreversible deletion cascades |
| Item deleted by creator/owner | Item hard-deleted | Immediate deletion; no recovery |
| Creator user deleted | Item REMAINS; created_by_id = NULL | Preserve item; attribute as "deleted user" |

**Foreign Key Behavior:**
- InventoryItem.household_id → Household: **CASCADE** (on hard-delete only)
- InventoryItem.created_by_id → User: **SET NULL**

**Invariants:**
- Any member can update quantity/details
- Creator or owner can delete
- Quantity is a positive integer (not a freeform string); unit is optional free-form display text, stored separately (e.g. quantity=2, unit="boxes")

---

## Deletion State Machine

```
User Account:
  Active
    ↓ [user deletes account]
  Soft-Deleted (deleted_at set)
    ↓ [after retention period]
  Hard-Deleted (all memberships, attribution set to null)
    
Household:
  Active
    ↓ [owner deletes household]
  Soft-Deleted (deleted_at set; all data preserved)
    ↓ [users lose access immediately; data recoverable for 30 days]
    ├─ [admin recovers within 30 days]
    │   ↓
    │   Active (deleted_at cleared; users regain access)
    │
    └─ [after 30 days; automated or admin hard-delete]
      ↓
      Hard-Deleted (all memberships, tasks, items cascade-deleted)
        ↓
      Irreversible (no recovery possible)
```

---

## Foreign Key Summary

| FK | Parent | Child | Constraint | Notes |
|----|--------|-------|-----------|-------|
| Household.owner_id | User | Household | PROTECT | Cannot delete user if owns household |
| Membership.household_id | Household | Membership | CASCADE | On hard-delete only; soft-delete preserves |
| Membership.user_id | User | Membership | CASCADE | On user deletion; membership removed |
| Task.household_id | Household | Task | CASCADE | On hard-delete only; soft-delete preserves |
| Task.created_by_id | User | Task | SET NULL | Preserve task; attribute preserved |
| Task.assigned_to_id | Membership | Task | SET NULL | Unassign if member removed |
| Task.completed_by_id | User | Task | SET NULL | Preserve completion record |
| ShoppingItem.household_id | Household | ShoppingItem | CASCADE | On hard-delete only; soft-delete preserves |
| ShoppingItem.created_by_id | User | ShoppingItem | SET NULL | Preserve item; attribute preserved |
| ShoppingItem.purchased_by_id | User | ShoppingItem | SET NULL | Preserve purchase history |
| Expense.household_id | Household | Expense | CASCADE | On hard-delete only; soft-delete preserves |
| Expense.created_by_id | User | Expense | SET NULL | Preserve expense; attribute preserved |
| Expense.payer_id | User | Expense | SET NULL | Preserve payer information |
| InventoryItem.household_id | Household | InventoryItem | CASCADE | On hard-delete only; soft-delete preserves |
| InventoryItem.created_by_id | User | InventoryItem | SET NULL | Preserve item; attribute preserved |
| Invitation.household_id | Household | Invitation | CASCADE | On hard-delete only; soft-delete preserves |

---

## Database-Level Invariants (Enforced by Constraints)

✓ Email unique per user  
✓ Household code unique globally  
✓ One membership per (household, user) pair  
✓ Household always has owner (owner_id NOT NULL)  
✓ Task assigned to member of same household (enforced by FK to Membership, not User)  
✓ All domain entities scoped by household_id  

---

## Application-Level Invariants (Requires Validation)

✓ Soft-delete household must not cascade-delete child records (app logic)  
✓ Hard-delete household (after retention) must cascade-delete all child records (app logic)  
✓ User cannot be hard-deleted if owns households (app validates; FK PROTECT backs this up)  
✓ Task assignment cannot reference member from different household (FK to Membership enforces)  
✓ Only creator/owner can delete tasks/shopping/expenses/inventory (app permission checks)  
✓ Only owner can delete household, invite, remove members (app permission checks)  
✓ Expense payer immutable after creation (app validation)  
✓ Invitation one-time use (app marks as accepted; state prevents re-use)  

---

## Resolved Decisions (formerly "Remaining Blockers")

1. **User Account Deletion Workflow:** **Resolved — Option A.** `Household.owner_id` uses PROTECT; hard-delete of a user is blocked until household ownership is transferred. Self-service account deletion and ownership-transfer UI are post-MVP (per PD-4); for MVP, account deletion requests are handled through an administrative/support process only — no self-service endpoint or UI.

2. **Retention Periods:** **Resolved for MVP-relevant cases.**
   - Household soft-delete to hard-delete: **30 days**
   - Session expiration: **14 days**
   - User soft-delete to hard-delete: Not fixed for MVP — account deletion is administrative/case-by-case (per PD-4), not a self-service flow with a defined TTL. Revisit when self-service deletion ships post-MVP.

3. **Household Code Regeneration:** **Resolved — Option A.** Regenerating a household code invalidates the old code immediately.

---

## Summary: 8 Entities, Correct Deletion Semantics

| Entity | Type | Parent | Soft-Delete | Hard-Delete | Notes |
|--------|------|--------|------------|------------|-------|
| User | Principal | N/A | Preserves | Cascades (PROTECT on ownership) | Account deletion |
| Household | Aggregate | User | Preserves data | Cascades all children | Security boundary |
| Membership | Association | Household+User | Preserves | Cascades | Role-based scoping |
| Invitation | Transaction | Household | Preserves | Cascades | Time-limited, one-time |
| Task | Domain | Household | Preserves | Cascades | Single assignee (Membership) |
| ShoppingItem | Domain | Household | Preserves | Cascades | Purchase tracking |
| Expense | Domain | Household | Preserves | Cascades | Attribution preserved |
| InventoryItem | Domain | Household | Preserves | Cascades | Basic tracking |

---

