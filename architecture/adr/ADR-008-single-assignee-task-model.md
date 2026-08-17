# ADR-008: Single-Assignee Task Model (No TaskAssignment Entity for MVP)

**Date:** August 16, 2026  
**Status:** Accepted  
**Author:** Product/Engineering Team  
**Owner:** Documentation repository; Product/Backend stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** Zero-or-one Task assignee, subject to ADR-012  
**Superseded by:** [ADR-012: Household ownership and authorization invariants](ADR-012-ownership-and-authorization.md) (same-household enforcement claim only)

> **Record scope:** The zero-or-one assignee decision remains accepted. A normal foreign key to Membership does not guarantee equality between Task and Membership household references; service-layer validation and negative integrity tests provide the MVP guarantee. Code, authorization, estimates, and migration examples below are historical and non-normative.

---

## Context

HouseHoldHub MVP requires task management where users can create and assign tasks to household members. We must decide the task assignment model:

Options:
1. **Single Assignee** (nullable assignment to one member)
   - Task.assigned_to_id → Membership (or User)
   - Simpler data model
   - Limited to one assignee per task

2. **Multiple Assignees** (association entity)
   - Task → TaskAssignment → Membership
   - More flexible
   - More complex data model
   - Useful if one task needs to be assigned to multiple people

---

## Decision

Use a **single-assignee task model** for MVP. Each task may have zero or one assignee.

```python
class Task(models.Model):
    # ...
    assigned_to = ForeignKey(Membership, null=True, blank=True, on_delete=models.SET_NULL)
```

Do NOT create a TaskAssignment association entity for MVP.

---

## Rationale

### Why Single Assignee?

1. **Simpler Data Model**
   - One less database table (no TaskAssignment)
   - Fewer joins in queries
   - Easier to understand and reason about
   - Faster queries (no association table)

2. **Sufficient for MVP**
   - PRD doesn't explicitly require multiple assignees
   - Household task workflows typically assign to one person
   - "Buy milk" assigned to Alice
   - "Fix leaky faucet" assigned to Bob
   - Not common to assign one task to multiple people

3. **Simpler User Interface**
   - Single "Assigned to" dropdown
   - No multi-select component
   - Cleaner UI for MVP

4. **Simpler Authorization**
   - Only assigned member (or owner) can mark complete
   - No complex logic for "any of multiple assignees"
   - Clear semantics

5. **Simpler Completion Tracking**
   - Task.completed boolean (not per-assignment)
   - Task.completed_by_id (who marked complete)
   - Task.completed_at timestamp

---

## Alternatives Considered

### Multiple Assignees (TaskAssignment Entity)
- **Pros:** More flexible; supports assigning to multiple people
- **Cons:** More complex; overkill for MVP; slower queries
- **Not chosen:** No product requirement for multi-assign; add post-MVP if needed

---

## Consequences

### Positive
- ✓ Simpler data model (no TaskAssignment entity)
- ✓ Faster queries (no join)
- ✓ Simpler UI (single dropdown)
- ✓ Simpler authorization logic
- ✓ Easier to understand and maintain

### Negative
- ✗ Cannot assign one task to multiple people in MVP
- ✗ Would require schema change to support multi-assign (add TaskAssignment entity)

### Migration Path
If multi-assign becomes necessary post-MVP:

1. **Create TaskAssignment Entity**
   ```python
   class TaskAssignment(models.Model):
       task = ForeignKey(Task, on_delete=models.CASCADE)
       assigned_to = ForeignKey(Membership, on_delete=models.CASCADE)
       completed = BooleanField(default=False)
       completed_at = DateTimeField(null=True)
       completed_by = ForeignKey(User, on_delete=models.SET_NULL, null=True)
   ```

2. **Migrate Data**
   - For each Task with assigned_to_id, create TaskAssignment
   - Copy completion status to TaskAssignment

3. **Update Queries**
   - "Tasks assigned to member": Join through TaskAssignment
   - "Mark task complete": Create/update TaskAssignment

4. **Update UI**
   - Multi-select for assignees
   - Per-assignee completion tracking

5. **Update Authorization**
   - Any assigned member can mark their assignment complete
   - Multiple members may all mark complete independently

**Time Estimate:** 2-3 days for experienced team

---

## Implementation

### Django Model

```python
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    
    # Single assignee (can be null for unassigned tasks)
    assigned_to = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Completion tracking
    completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='completed_tasks'
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Audit fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Serializer

```python
class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(
        source='assigned_to.user.name',
        read_only=True
    )
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'assigned_to', 
                  'assigned_to_name', 'completed', 'completed_by', 'completed_at']
```

### Authorization

```python
class CanDeleteTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_creator = obj.created_by == request.user
        is_owner = Membership.objects.filter(
            household=obj.household,
            user=request.user,
            role='owner'
        ).exists()
        return is_creator or is_owner

class CanCompleteTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assigned member or owner can complete
        is_assigned = obj.assigned_to and obj.assigned_to.user == request.user
        is_owner = Membership.objects.filter(
            household=obj.household,
            user=request.user,
            role='owner'
        ).exists()
        return is_assigned or is_owner
```

### Endpoint

```python
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, CanCompleteTask])
def complete_task(request, household_id, task_id):
    # Verify membership
    verify_household_membership(request.user, household_id)
    
    # Get task
    task = Task.objects.get(id=task_id, household_id=household_id)
    
    # Mark complete
    task.completed = True
    task.completed_by = request.user
    task.completed_at = timezone.now()
    task.save()
    
    return Response(TaskSerializer(task).data)
```

---

## Future: Multi-Assignee Feature

This ADR can be revisited post-MVP if user feedback indicates:
- Users frequently want to assign tasks to multiple people
- Current single-assign model frustrates users
- Other household management apps offer this feature

At that point:
1. Create TaskAssignment entity
2. Migrate data
3. Update queries and serializers
4. Update UI to support multi-select
5. Update authorization logic

The migration is straightforward and doesn't break existing functionality.

---

## Related ADRs

- ADR-002: Django + Django REST Framework
- ADR-005: Household-scoped authorization via Membership

---
