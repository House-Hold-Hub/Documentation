# HouseHoldHub MVP - Final Domain Model

**Date:** August 16, 2026  
**Status:** Ready for Review  
**All Decisions Resolved**

---

## Overview

This document presents the complete domain model for HouseHoldHub MVP with all critical decisions resolved:

✓ Backend: Django + Django REST Framework  
✓ Database: PostgreSQL  
✓ Sessions: Database-backed (no Redis)  
✓ Task Assignment: Single assignee per task (no TaskAssignment entity)  
✓ Deployment: Platform-neutral (Docker Compose)

---

## Entity Definitions

### 1. User

**Purpose:** User account and identity for authentication

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| email | String | UNIQUE, NOT NULL, Indexed | Login identifier |
| password_hash | String | NOT NULL | bcrypt/Argon2 hash |
| name | String | NOT NULL | Display name |
| google_id | String | UNIQUE, NULL | Google OAuth identifier |
| created_at | Timestamp | NOT NULL, auto | Account creation time |
| updated_at | Timestamp | NOT NULL, auto | Last update |
| deleted_at | Timestamp | NULL | Soft-delete timestamp |

**Relationships:**
- Owns multiple Households (1:N via household.owner_id)
- Participates in multiple Memberships (1:N)
- Creates Tasks, ShoppingItems, Expenses, InventoryItems (1:N)
- Completes Tasks (1:N)
- Pays Expenses (1:N)
- Marks ShoppingItems purchased (1:N)

**Lifecycle:**
- Created: User signs up or first OAuth login
- Active: Can authenticate and access households
- Soft-Deleted: User deletes account; cannot authenticate
- Hard-Deleted: After retention period (TBD)

**Notes:**
- Users can belong to multiple households
- Ownership is tied to individual Household records (not User-based roles)
- Personal data anonymized in household contexts post-deletion

---

### 2. Household

**Purpose:** Container for shared data within a group of cohabiting users

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| name | String | NOT NULL | Display name |
| description | String | NULL | Optional description |
| code | String | UNIQUE, NOT NULL, Indexed | Shareable join code |
| owner_id | UUID | FK→User, NOT NULL | Household owner |
| created_at | Timestamp | NOT NULL, auto | Creation time |
| updated_at | Timestamp | NOT NULL, auto | Last update |
| deleted_at | Timestamp | NULL | Soft-delete timestamp |

**Relationships:**
- Has one Owner (User)
- Has multiple Memberships (1:N)
- Contains Tasks (1:N)
- Contains ShoppingItems (1:N)
- Contains Expenses (1:N)
- Contains InventoryItems (1:N)
- Has Invitations (1:N)

**Constraints:**
- `code`: Globally unique; can be regenerated (old code becomes invalid)
- Foreign key: `owner_id → User` (no cascade; user deletion doesn't delete household)

**Lifecycle:**
- Created: User creates household
- Active: Members can access and modify data
- Soft-Deleted: deleted_at set; members lose access; recoverable for TBD days
- Hard-Deleted: After retention period; data unrecoverable

**Deletion Behavior:**
- On household soft-delete: All Memberships → hard-delete; all Tasks/Shopping/Expenses/Inventory → hard-delete
- On household hard-delete: Permanent; no recovery

**Notes:**
- Households are the security boundary (all data scoped by household_id)
- Owner is single user; cannot be changed
- If owner deletes account, household becomes orphaned (needs admin procedure)

---

### 3. Membership

**Purpose:** Represents a user's membership in a household with a role

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| household_id | UUID | FK→Household, NOT NULL | Household reference |
| user_id | UUID | FK→User, NOT NULL | User reference |
| role | Enum | UNIQUE(household_id, user_id) | owner or member |
| joined_at | Timestamp | NOT NULL, auto | Join time |
| created_at | Timestamp | NOT NULL, auto | Record creation |

**Role Enumeration:**
- `owner`: Can invite, remove members, delete household
- `member`: Can create/edit/assign tasks, but not manage household

**Constraints:**
- UNIQUE(household_id, user_id): Only one membership per household per user
- Foreign keys: Both cascade on delete

**Relationships:**
- References User (N:1)
- References Household (N:1)
- Referenced by Tasks (assigned_to_id → Membership)

**Lifecycle:**
- Created: User accepts invitation or joins via code
- Active: User can access household data per role permissions
- Removed: User removed by owner OR user deletes account
- Hard-Delete: No recovery; immediate access loss

**Deletion Behavior:**
- On user deletion: Membership → hard-delete (user's data remains, membership removed)
- On household deletion: Membership → hard-delete (users lose access)

**Notes:**
- Users can have multiple Memberships (one per household)
- Each Membership tracks when user joined (for auditing)
- Owner role is immutable (cannot change role after creation)

---

### 4. Invitation

**Purpose:** Invites users to join a household

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| household_id | UUID | FK→Household, NOT NULL | Target household |
| email | String | NOT NULL, Indexed | Invited email address |
| token_hash | String | NOT NULL, Indexed | SHA-256 hash of token |
| state | Enum | NOT NULL | pending, accepted, revoked, expired |
| created_at | Timestamp | NOT NULL, auto | Creation time |
| expires_at | Timestamp | NOT NULL | Expiration timestamp |
| accepted_at | Timestamp | NULL | When accepted |

**State Enumeration:**
- `pending`: Awaiting user action (accept or expiration)
- `accepted`: User accepted and added to Membership
- `revoked`: Owner revoked before expiration
- `expired`: TTL passed without acceptance

**Constraints:**
- Foreign key: `household_id → Household` (ON DELETE CASCADE)
- Token security: Plaintext never stored; only SHA-256 hash

**Relationships:**
- References Household (N:1)
- Triggers Membership creation on acceptance

**Lifecycle:**
- Pending: Owner initiates invitation; email sent to user
- Accepted: User clicks link, verifies account, Membership created
- Revoked: Owner can revoke anytime; state = revoked
- Expired: If not accepted by expires_at; state = expired

**Deletion Behavior:**
- Hard-delete on household deletion
- Can be deleted after expiration (old invitations cleaned up)

**Notes:**
- One-time use: Token marked as used immediately after acceptance
- Expiration: TBD (e.g., 30 days)
- Owner can revoke invitations before acceptance
- Users can request new invitation if old one expired

---

### 5. Task

**Purpose:** Represents a household task or chore

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| household_id | UUID | FK→Household, NOT NULL | Household scope |
| title | String | NOT NULL | Task title |
| description | String | NULL | Optional details |
| due_date | Date | NULL | Optional deadline |
| created_by_id | UUID | FK→User, SET NULL | Creator (for attribution) |
| assigned_to_id | UUID | FK→Membership, SET NULL | Single assignee |
| completed | Boolean | NOT NULL, default=false | Completion status |
| completed_by_id | UUID | FK→User, SET NULL | Who completed |
| completed_at | Timestamp | NULL | When completed |
| created_at | Timestamp | NOT NULL, auto | Creation time |
| updated_at | Timestamp | NOT NULL, auto | Last update |

**Constraints:**
- Foreign keys:
  - `household_id → Household`: ON DELETE CASCADE
  - `created_by_id → User`: ON DELETE SET NULL (task remains if creator deleted)
  - `assigned_to_id → Membership`: ON DELETE SET NULL (task unassigned if member removed)
  - `completed_by_id → User`: ON DELETE SET NULL

**Relationships:**
- Belongs to Household (N:1)
- Created by User (N:1)
- Assigned to Membership (N:1, nullable)
- Completed by User (N:1, nullable)

**Assignment Model:**
- Single assignee per task (nullable)
- Assignee references Membership (not User) to enforce household scoping
- If assigned member leaves household, task becomes unassigned (assigned_to_id = NULL)

**Completion Logic:**
- Assigned member can mark complete
- Household owner can mark any task complete
- Other members cannot mark complete (but can reassign to self)
- Completion tracked by timestamp and completing user

**Deletion Behavior:**
- Hard-delete (no recovery); only creator or owner can delete
- If creator deleted: Task remains (created_by_id = NULL)
- If assigned member removed: Task becomes unassigned

**Lifecycle:**
- Open: Created and available for assignment
- Assigned: Member selected to complete task
- Completed: Marked complete with timestamp
- Deleted: Removed from household (no recovery)

**Notes:**
- No recurring task metadata (post-MVP feature)
- No comments or attachments (post-MVP feature)
- Due date is optional (no notifications for overdue tasks in MVP)
- Zero assignees: Task open; any member can complete

---

### 6. ShoppingItem

**Purpose:** Represents an item on the household shopping list

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| household_id | UUID | FK→Household, NOT NULL | Household scope |
| name | String | NOT NULL | Item name |
| quantity | String | NULL | Amount (e.g., "2 lbs") |
| purchased | Boolean | NOT NULL, default=false | Purchase status |
| purchased_by_id | UUID | FK→User, SET NULL | Who marked purchased |
| purchased_at | Timestamp | NULL | When marked purchased |
| created_by_id | UUID | FK→User, SET NULL | Creator |
| created_at | Timestamp | NOT NULL, auto | Creation time |
| updated_at | Timestamp | NOT NULL, auto | Last update |

**Constraints:**
- Foreign keys:
  - `household_id → Household`: ON DELETE CASCADE
  - `created_by_id → User`: ON DELETE SET NULL
  - `purchased_by_id → User`: ON DELETE SET NULL

**Relationships:**
- Belongs to Household (N:1)
- Created by User (N:1)
- Marked purchased by User (N:1, nullable)

**Lifecycle:**
- Added: Any member adds item (purchased = false)
- Updated: Any member updates quantity/name
- Marked Purchased: Any member marks as purchased (purchased = true, purchased_by_id set)
- Toggled: Can toggle back to unpurchased (resets purchased_by_id, purchased_at)
- Deleted: Creator or owner can delete (hard-delete, no recovery)

**Deletion Behavior:**
- Hard-delete; no recovery
- If creator deleted: Item remains (created_by_id = NULL)

**Notes:**
- Quantity is freeform string (no units enforced)
- No categorization for MVP (shopping vs. pantry items)
- No low-stock alerts or notifications
- Purchased items can be toggled back to unpurchased

---

### 7. Expense

**Purpose:** Represents a household expense (e.g., groceries, utilities)

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| household_id | UUID | FK→Household, NOT NULL | Household scope |
| amount_cents | Integer | NOT NULL | Amount in cents (no decimals) |
| category | Enum | NOT NULL | Predefined categories |
| payer_id | UUID | FK→User, SET NULL | Who paid |
| description | String | NULL | Optional notes |
| created_by_id | UUID | FK→User, SET NULL | Who logged expense |
| created_at | Timestamp | NOT NULL, auto | Creation time |
| updated_at | Timestamp | NOT NULL, auto | Last update |

**Category Enumeration:**
- Food
- Utilities
- Maintenance
- Entertainment
- Other

**Constraints:**
- Foreign keys:
  - `household_id → Household`: ON DELETE CASCADE
  - `payer_id → User`: ON DELETE SET NULL (expense remains)
  - `created_by_id → User`: ON DELETE SET NULL

**Relationships:**
- Belongs to Household (N:1)
- Logged by User (created_by_id)
- Paid by User (payer_id, nullable)

**Payer Logic:**
- If payer_id not specified on creation: defaults to created_by_id
- Payer immutable after creation (prevent changing historical data)

**Lifecycle:**
- Logged: Any member logs expense with amount and category
- Edited: Creator or owner can edit amount/category/description/payer
- Deleted: Creator or owner can delete (hard-delete, no recovery)

**Deletion Behavior:**
- Hard-delete; no recovery
- If creator deleted: Expense remains (created_by_id = NULL)
- If payer deleted: Expense remains (payer_id = NULL)

**Notes:**
- Amount stored in cents (100 = $1.00) to avoid float precision issues
- No currency field (assume single household currency)
- No expense splitting or settlement (post-MVP feature)
- No attachments or receipts (post-MVP feature)
- Categories are predefined enum (custom categories post-MVP)

---

### 8. InventoryItem

**Purpose:** Represents a household inventory item (pantry, supplies, etc.)

**Attributes:**
| Attribute | Type | Constraints | Purpose |
|-----------|------|-----------|---------|
| id | UUID | PK | Unique identifier |
| household_id | UUID | FK→Household, NOT NULL | Household scope |
| name | String | NOT NULL | Item name |
| quantity | String or Integer | NOT NULL | Quantity (flexible) |
| category | String | NULL | Optional category |
| location | String | NULL | Optional storage location |
| created_by_id | UUID | FK→User, SET NULL | Creator |
| created_at | Timestamp | NOT NULL, auto | Creation time |
| updated_at | Timestamp | NOT NULL, auto | Last update |

**Constraints:**
- Foreign keys:
  - `household_id → Household`: ON DELETE CASCADE
  - `created_by_id → User`: ON DELETE SET NULL

**Relationships:**
- Belongs to Household (N:1)
- Created by User (N:1)

**Lifecycle:**
- Added: Any member adds item with name and quantity
- Updated: Any member updates quantity or details
- Deleted: Creator or owner can delete (hard-delete, no recovery)

**Deletion Behavior:**
- Hard-delete; no recovery
- If creator deleted: Item remains (created_by_id = NULL)

**Notes:**
- Quantity is flexible (integer or string like "2 boxes")
- Category and location are optional (user can leave blank)
- No low-stock alerts or notifications
- No expiration tracking (post-MVP feature)
- Minimal validation (allows freeform data entry)

---

## Domain Model Diagram

```
User
├── owns → Household (1:1 relationship via owner_id)
├── participates in → Membership (1:N)
├── creates → Task (1:N)
├── completes → Task (1:N)
├── creates → ShoppingItem (1:N)
├── marks purchased → ShoppingItem (1:N)
├── creates → Expense (1:N)
├── pays → Expense (1:N)
└── creates → InventoryItem (1:N)

Household
├── owned by → User (1:1 relationship via owner_id)
├── has → Membership (1:N)
├── has → Task (1:N)
├── has → ShoppingItem (1:N)
├── has → Expense (1:N)
├── has → InventoryItem (1:N)
└── has → Invitation (1:N)

Membership
├── references → Household
├── references → User
├── scopes → Task assignment (1:N)
└── unique constraint: (household_id, user_id)

Invitation
├── references → Household
└── creates → Membership (on acceptance)

Task
├── belongs to → Household
├── created by → User
├── assigned to → Membership (nullable)
├── completed by → User (nullable)
└── single assignee per task

ShoppingItem
├── belongs to → Household
├── created by → User
└── marked purchased by → User (nullable)

Expense
├── belongs to → Household
├── created by → User
└── paid by → User (nullable, defaults to creator)

InventoryItem
├── belongs to → Household
└── created by → User
```

---

## Household Scoping

**All entities scoped by household_id:**

```sql
-- Query pattern for data access control
SELECT *
FROM entity
WHERE household_id IN (
  SELECT household_id
  FROM membership
  WHERE user_id = current_user_id
)
```

- User can only access data from households where they have a Membership
- All queries filtered by household_id
- Cross-household data access prevented at database, middleware, and API layers

---

## Foreign Key Cascade Behavior

| FK | Parent | Child | Behavior | Rationale |
|----|--------|-------|----------|-----------|
| Task.household_id | Household | Task | CASCADE | Delete tasks when household deleted |
| Task.created_by_id | User | Task | SET NULL | Preserve task if creator deleted |
| Task.assigned_to_id | Membership | Task | SET NULL | Unassign task if member removed |
| ShoppingItem.household_id | Household | ShoppingItem | CASCADE | Delete items when household deleted |
| ShoppingItem.created_by_id | User | ShoppingItem | SET NULL | Preserve item if creator deleted |
| Expense.household_id | Household | Expense | CASCADE | Delete expenses when household deleted |
| Expense.created_by_id | User | Expense | SET NULL | Preserve expense if creator deleted |
| InventoryItem.household_id | Household | InventoryItem | CASCADE | Delete items when household deleted |
| InventoryItem.created_by_id | User | InventoryItem | SET NULL | Preserve item if creator deleted |
| Membership.household_id | Household | Membership | CASCADE | Remove membership if household deleted |
| Membership.user_id | User | Membership | CASCADE | Remove membership if user deleted |
| Invitation.household_id | Household | Invitation | CASCADE | Delete invitation if household deleted |

---

## Ownership vs. Authorship

| Entity | Author (created_by) | Owner (can delete) | Can Edit |
|--------|---------------------|-------------------|----------|
| Household | User (creates) | User (owner_id) | Owner only |
| Membership | N/A | Household owner | Owner only |
| Task | Member (created_by) | Creator or owner | Creator or owner |
| ShoppingItem | Member (created_by) | Creator or owner | Any member |
| Expense | Member (created_by) | Creator or owner | Creator or owner |
| InventoryItem | Member (created_by) | Creator or owner | Any member |
| Invitation | Household owner | Household owner | Owner only |

---

## Member Removal Behavior

**When a member is removed from a household:**

1. Membership record: Hard-deleted immediately
2. User access: User can no longer see/access household
3. User data preservation:
   - Tasks created by removed user: Remain (created_by_id unchanged)
   - Tasks assigned to removed user: Become unassigned (assigned_to_id = NULL)
   - Shopping items created: Remain (created_by_id unchanged)
   - Expenses created: Remain (created_by_id unchanged)
   - Inventory items created: Remain (created_by_id unchanged)
4. UI display: "Task created by X" shown even if X was removed

---

## Household Deletion Behavior

**Soft-Deletion (Recoverable):**
- household.deleted_at = now()
- Users immediately lose access
- Data not deleted yet
- Recoverable for TBD days

**Hard-Deletion (After Retention Period):**
- All data permanently deleted:
  - All Membership records
  - All Task records
  - All ShoppingItem records
  - All Expense records
  - All InventoryItem records
  - All Invitation records
- No recovery possible
- Unreversible

---

## Data Retention Policies (TBD)

| Entity | Soft-Delete Period | Hard-Delete After | Notes |
|--------|-------------------|-----------------|-------|
| User | Immediate (deleted_at) | TBD (14/30/90 days?) | Data anonymized in households |
| Household | Immediate (deleted_at) | TBD (14/30/90 days?) | All child data deleted |
| Session | N/A | TTL (2 weeks, configurable) | Auto-cleanup via Django |

---

## Summary: Entity Count & Relationships

- **8 Core Entities:** User, Household, Membership, Invitation, Task, ShoppingItem, Expense, InventoryItem
- **No Association Entities:** Single-assignee task model (no TaskAssignment for MVP)
- **Foreign Keys:** All properly constrained with ON DELETE CASCADE or SET NULL
- **Uniqueness:** Email (User), Household Code, Membership (household_id + user_id)
- **Total Tables:** 8 + Django built-in (auth_user, django_session, etc.)

---

## Next Steps

1. ✓ Domain model reviewed and validated
2. ✓ Foreign key behavior documented
3. ✓ Deletion semantics clarified
4. → Create Django models based on this specification
5. → Generate database migrations
6. → Create API serializers and views
7. → Implement authorization checks
8. → Write integration tests

---

