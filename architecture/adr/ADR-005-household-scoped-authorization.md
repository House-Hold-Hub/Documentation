# ADR-005: Household-Scoped Authorization via Membership

**Date:** August 16, 2026  
**Status:** Accepted  
**Author:** Security/Product Team  
**Owner:** Documentation repository; Product/Security/Backend stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** Membership-based household scoping, subject to ADR-012  
**Superseded by:** [ADR-012: Household ownership and authorization invariants](ADR-012-ownership-and-authorization.md) (ownership, error, integrity, and permission-detail portions)

> **Record scope:** Membership-based household scoping remains accepted. The current owner invariant is defined by ADR-012, and the [permissions matrix](../../product/permissions-matrix.md) is authoritative for product actions. Code and permission tables below are historical and non-normative.

---

## Context

HouseHoldHub supports multiple households. Each user may belong to multiple households. We must enforce:
- Users can only access data from households they are members of
- Permissions vary by role (owner vs. member)
- Some actions are owner-only (delete household, invite members)
- Some actions are member actions (create tasks, mark shopping items)

Design question: How do we model and enforce household scoping?

Options:
1. **Membership entity with roles** (owner/member in membership record)
2. **User-to-Household foreign key with role** (single role per user)
3. **Permission table** (fine-grained permissions per user per household)

---

## Decision

Use a **Membership entity** that represents a user's membership in a household with a role (owner or member).

```
User → Membership → Household
       (role: owner/member)
```

---

## Rationale

### Why Membership Entity?

1. **Clean Separation of Concerns**
   - User is account and identity
   - Household is domain entity for collaborative data
   - Membership links them with a role

2. **Supports Multiple Households**
   - User can have multiple Membership records (one per household)
   - Each Membership has its own role (could be owner in one, member in another)
   - Easy to query: "User's households" or "Household's members"

3. **Enables Role-Based Permissions**
   - Membership.role = owner or member
   - Simple enum; can extend to admin, moderator, etc. post-MVP
   - Easy to check: "Is user owner of this household?"

4. **On Member Removal**
   - Delete Membership record; user loses access immediately
   - User's created data (tasks, expenses) remains in household
   - Clean separation: user is deleted, but their contributions remain

5. **On Household Deletion**
   - Delete all Membership records
   - All users lose access immediately
   - Clear semantics

6. **Auditable**
   - joined_at timestamp on Membership shows when user joined
   - Useful for member management UI

---

## Alternatives Considered

### Single User-to-Household FK with Role
- **Pros:** Simpler schema (no intermediate entity)
- **Cons:** User limited to single household; doesn't support multi-household
- **Not chosen:** PRD requires multi-household support

### Permission Table (Fine-Grained)
- **Pros:** Extremely flexible; can grant individual permissions
- **Cons:** Overkill for MVP; role-based model sufficient
- **Not chosen:** Start simple; add fine-grained permissions if needed post-MVP

---

## Consequences

### Positive
- ✓ Clean separation of user identity and household membership
- ✓ Supports multi-household users
- ✓ Role-based permissions straightforward
- ✓ Auditable (joined_at timestamp)
- ✓ Easy to understand and reason about
- ✓ Easy to query (find user's households, find household's members)

### Negative
- ✗ One additional database table (Membership)
- ✗ Queries require join between User, Membership, Household

### Migration Path
- Membership to fine-grained permissions: Add Permission table alongside Membership; gradually migrate
- Membership to simpler model: Flatten if multi-household no longer needed

---

## Implementation

### Django Model

```python
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
```

### Authorization Checks

#### Database Layer
All queries filtered by household membership:
```python
# Get tasks for a user's household
tasks = Task.objects.filter(
    household_id__in=Membership.objects.filter(user=user).values_list('household_id')
)
```

#### Middleware/Route Layer
Verify user is member before processing:
```python
def get_household_and_verify_membership(user, household_id):
    membership = Membership.objects.filter(
        user=user,
        household_id=household_id
    ).first()
    
    if not membership:
        raise PermissionDenied("Not a member of this household")
    
    return membership
```

#### Permission Classes
DRF permission classes for specific actions:
```python
class IsHouseholdMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(
            household=obj.household,
            user=request.user
        ).exists()

class IsHouseholdOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        membership = Membership.objects.filter(
            household=obj.household,
            user=request.user
        ).first()
        return membership and membership.role == 'owner'

class CanDeleteTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_creator = obj.created_by == request.user
        is_owner = Membership.objects.filter(
            household=obj.household,
            user=request.user,
            role='owner'
        ).exists()
        return is_creator or is_owner
```

### Role-Based Permissions

| Action | Owner | Member |
|--------|-------|--------|
| Create task | ✓ | ✓ |
| Delete household | ✓ | ✗ |
| Invite member | ✓ | ✗ |
| Remove member | ✓ | ✗ |
| Delete task (own) | ✓ | ✓ |
| Delete task (others) | ✓ | ✗ |

---

## Related ADRs

- ADR-001: Multi-repository architecture (household scoping affects both frontend and backend)
- ADR-002: Django + Django REST Framework (Django ORM makes this pattern straightforward)

---
