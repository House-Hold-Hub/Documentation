# ADR-006: API-Based Synchronization (No Real-Time Transport)

**Date:** August 16, 2026  
**Status:** Accepted  
**Author:** Product/Engineering Team  
**Owner:** Documentation repository; Product/Frontend/Backend stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** Request/response synchronization without real-time transport  
**Superseded by:** —

> **Record scope:** Request/response synchronization without real-time transport remains accepted. The [OpenAPI specification](../../api/openapi.yaml) owns routes and wire behavior; MVP concurrency is pure last-write-wins with no conflict-detection contract. Library and code examples below are non-normative.

---

## Context

HouseHoldHub requires household members to see collaborative changes (tasks, shopping, expenses, inventory) in a reasonable timeframe. We must choose a synchronization strategy.

Options:
1. **Real-Time Transport** (WebSockets, Server-Sent Events)
   - Changes pushed to all connected clients immediately
   - Low latency (~milliseconds)
   - Complex infrastructure (persistent connections, broadcasting)

2. **API-Based Polling** (Traditional)
   - Client polls server for changes on user action (page navigation, button clicks)
   - Background polling every N seconds (less common)
   - Higher latency (seconds, depending on polling interval)
   - Simple infrastructure

3. **Hybrid** (API + WebSockets)
   - API for most operations
   - WebSockets for critical real-time features
   - Higher complexity

---

## Decision

Use **API-based synchronization with cache invalidation** for MVP. No real-time transport required.

**Pattern:**
1. Client performs mutation (POST/PATCH/DELETE)
2. Server processes and returns updated resource
3. Client invalidates related cache entries (TanStack Query)
4. Client refetches data on page navigation or user action
5. Background refresh on focus (optional, improves UX)

---

## Rationale

### Why API-Based?

1. **Sufficient for MVP**
   - Household members are not all online simultaneously
   - Changes don't require millisecond synchronization
   - PRD states "sufficiently fresh data during normal usage" (not real-time)
   - Collaborative shopping/task lists don't require live synchronization

2. **Simple Infrastructure**
   - Standard HTTP requests
   - Stateless server (easier to scale)
   - No persistent connections to manage
   - Works with any deployment platform
   - Easy to test and debug

3. **Excellent UX with TanStack Query**
   - TanStack Query automatically invalidates cache after mutations
   - Automatic background refetch on window focus
   - Optimistic updates reduce perceived latency
   - Handles race conditions and stale data

4. **Privacy & Cost**
   - No persistent WebSocket connections (saves bandwidth)
   - No server-side connection management (simpler ops)
   - Lower infrastructure costs

5. **Mobile-Friendly**
   - Works on mobile without persistent connection overhead
   - Native apps can use same REST API
   - Simpler implementation for mobile teams

---

## Alternatives Considered

### Real-Time WebSockets
- **Pros:** Immediate synchronization; smooth real-time collaboration
- **Cons:** Complex infrastructure; persistent connections expensive; not needed for MVP
- **Not chosen:** Overkill for MVP; PRD doesn't require real-time

### Server-Sent Events (SSE)
- **Pros:** Server push without WebSockets; simpler than WebSockets
- **Cons:** Still requires persistent connections; not ideal for household-scale use case
- **Not chosen:** API-based is simpler and sufficient

### Hybrid (API + WebSockets for critical features)
- **Pros:** Can add real-time for notifications later
- **Cons:** Adds complexity; infrastructure overhead
- **Not chosen:** Start simple; add real-time only if user testing shows need

---

## Consequences

### Positive
- ✓ Simple REST API (already designed)
- ✓ Stateless server (easier to scale)
- ✓ Works on any deployment platform
- ✓ Works for mobile without special handling
- ✓ Lower infrastructure costs
- ✓ Easier to test and debug
- ✓ TanStack Query handles cache invalidation automatically

### Negative
- ✗ Higher latency than real-time (seconds vs. milliseconds)
- ✗ Client must explicitly refetch (or use background polling)
- ✗ If multiple household members editing simultaneously, last-write-wins may lose earlier edit

### Migration Path
- API to WebSockets: Straightforward migration
  1. Add WebSocket server alongside REST API
  2. Establish persistent connections for connected clients
  3. Broadcast changes to all connected clients
  4. Clients can use WebSocket for push notifications
- **Recommended:** Start with API; add WebSockets only if user testing shows need

---

## Implementation

### Client Cache Invalidation (TanStack Query)

```typescript
// Frontend mutation with cache invalidation
const createTaskMutation = useMutation({
  mutationFn: (task) => api.createTask(householdId, task),
  onSuccess: () => {
    // Invalidate tasks list; causes automatic refetch
    queryClient.invalidateQueries({
      queryKey: ['tasks', householdId]
    });
  }
});

// Optional: background refetch on window focus
useEffect(() => {
  const handleFocus = () => {
    queryClient.refetchQueries();
  };
  
  window.addEventListener('focus', handleFocus);
  return () => window.removeEventListener('focus', handleFocus);
}, [queryClient]);
```

### Server (Django REST Framework)

```python
# Simple REST endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request, household_id):
    # Validate membership
    verify_household_membership(request.user, household_id)
    
    # Create task
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save(
            household_id=household_id,
            created_by=request.user
        )
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)
```

### User Experience

1. **Immediate Feedback:** Optimistic updates show change immediately
2. **Automatic Refresh:** Page navigation triggers refetch
3. **Focus Refresh:** Return to tab shows latest data (optional)
4. **Manual Refresh:** Users can explicitly refresh (⌘R or button)
5. **Stale Data Tolerance:** Few-second delay is acceptable for household tasks/shopping

---

## Limitations & Mitigations

| Limitation | Mitigation |
|-----------|-----------|
| Last-write-wins overwrites earlier edit | Acceptable for MVP; full conflict resolution post-MVP |
| Multiple simultaneous editors may be unaware | Page refresh shows latest state; users can see who edited last |
| Real-time collaboration feel | TanStack Query background refetch mitigates; sufficient for MVP |

---

## Post-MVP Evolution

Once MVP is live and users provide feedback:
1. If real-time is critical: Add WebSocket server alongside REST API
2. If notifications are critical: Add email or in-app notifications (post-MVP)
3. If activity feed is useful: Add to dashboard (can use REST API)

---

## Related ADRs

- ADR-001: Multi-repository architecture
- ADR-002: Django + Django REST Framework
- ADR-006: API-based synchronization

---
