# ADR-007: Database-Backed Sessions for MVP (No Redis)

**Date:** August 16, 2026  
**Status:** Accepted  
**Author:** Infrastructure/Engineering Team  
**Owner:** Documentation repository; Backend/Infrastructure stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** Database-backed sessions and no required Redis, subject to ADR-011  
**Superseded by:** [ADR-011: Identity and session security](ADR-011-identity-and-session-security.md) (cookie, CSRF, registry, and revocation portions only)

> **Record scope:** Database-backed Django sessions and no required Redis remain accepted. Numeric performance claims, session-inspection suggestions, cookie examples, and provider examples below are historical and non-normative.

---

## Context

HouseHoldHub requires session storage for authenticated user requests. We must choose where to store sessions:

Options:
1. **Database-Backed Sessions** (Django sessions table)
   - Stored in PostgreSQL `django_session` table
   - No additional dependency; uses same database
   - Slower than in-memory but sufficient for MVP

2. **Single Redis Instance**
   - In-memory data store
   - Faster than database
   - Additional dependency and operational overhead
   - Acceptable for MVP at higher scale

3. **Redis Cluster**
   - Distributed Redis with replication and failover
   - High availability; handles node failures
   - Significant operational complexity
   - Overkill for MVP

---

## Decision

Use **Django's database-backed session engine** (PostgreSQL) for MVP. **Redis is NOT a required dependency.**

```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

---

## Rationale

### Why Database-Backed Sessions?

1. **Zero Additional Dependencies**
   - Uses PostgreSQL (already required)
   - No Redis server to manage
   - No Redis deployment complexity
   - No Redis monitoring/alerting needed

2. **Sufficient for MVP Scale**
   - Expected MVP: 100-10,000 concurrent sessions
   - PostgreSQL can handle 10k+ session lookups per second
   - Database query latency acceptable for authentication (10-50ms)
   - Session lookup is single row lookup (very fast)

3. **Automatically Managed**
   - Django handles session creation/deletion
   - `django.contrib.sessions` middleware loads session on every request
   - TTL-based cleanup via `python manage.py clearsessions` (can run nightly)
   - No custom session management code needed

4. **Auditable**
   - Session data stored as JSON; can inspect sessions
   - Useful for debugging and user support
   - Can see what user data is in session

5. **Simpler Development**
   - Docker Compose only needs PostgreSQL (not Redis)
   - No Redis configuration or troubleshooting
   - Faster local development iteration

6. **Familiar Pattern**
   - Django developers understand database sessions
   - No learning curve for Redis
   - Easy to debug (can query `django_session` table directly)

---

## Alternatives Considered

### Redis (Single Instance)
- **Pros:** Faster than database; standard for production
- **Cons:** Additional dependency; operational overhead; overkill for MVP
- **Not chosen:** Database sessions sufficient until load testing proves need

### Redis Cluster
- **Pros:** High availability; handles failures
- **Cons:** Significant operational complexity; not needed for MVP
- **Not chosen:** Premature optimization; overkill for MVP

---

## Consequences

### Positive
- ✓ No additional infrastructure or dependencies
- ✓ Uses existing PostgreSQL database
- ✓ Simpler local development (Docker Compose only needs PostgreSQL)
- ✓ Easier to debug (can query session data directly)
- ✓ Sufficient for MVP scale

### Negative
- ✗ Slightly slower than Redis (acceptable latency ~10-50ms per lookup)
- ✗ Session lookups add load to database (minimal for MVP scale)
- ✗ Not suitable if scaling to 100k+ concurrent users (future)

### Performance Characteristics
- Session creation: ~5-10ms (database insert)
- Session lookup: ~1-5ms (single row query, indexed)
- Session deletion: ~5-10ms (database delete)
- Total per-request overhead: ~1-5ms (session lookup only; creation/deletion on login/logout)

At 10,000 concurrent sessions with 1-second request rate:
- 10,000 session lookups/sec × 5ms = 50 seconds of database time
- PostgreSQL on moderate hardware can handle 1000+ qps
- **Conclusion:** Database sessions fine for MVP scale

---

## Migration Path (Post-MVP)

If load testing shows database sessions are bottleneck:

1. **Add Redis Cache Layer (Without Changing Sessions)**
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   
   # Sessions still use database, but other queries can use Redis cache
   SESSION_ENGINE = 'django.contrib.sessions.backends.db'
   ```
   - This caches frequently-accessed data (household memberships, permissions)
   - Doesn't change session storage; reduces database load elsewhere

2. **Migrate to Redis Sessions (When Necessary)**
   ```python
   # settings.py
   SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
   SESSION_CACHE_ALIAS = 'default'
   ```
   - Only if database session lookups become bottleneck
   - Transparent to application code
   - Requires Redis availability (can fallback to database if Redis down)

3. **Add Redis Cluster (If Scaling Critical)**
   - Only when 10k+ concurrent users and HA required
   - Deploy Redis cluster with replication and failover
   - Application code unchanged (just change connection URL)

**Key Point:** Application code doesn't depend on Redis; treat as optional cache/performance layer.

---

## Implementation

### Django Configuration

```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks (configurable)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # In production
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
```

### Initial Setup

```bash
# Apply migrations (creates django_session table)
python manage.py migrate

# Run daily cleanup (remove expired sessions)
python manage.py clearsessions
```

### Monitoring (Post-MVP)

```bash
# Query session count
SELECT COUNT(*) FROM django_session;

# Query active sessions
SELECT COUNT(*) FROM django_session WHERE expire_date > NOW();

# Query by user (if storing user_id in session)
SELECT * FROM django_session WHERE session_data LIKE '%user_id%';
```

---

## Deployment

### Development
- PostgreSQL in Docker Compose
- Sessions automatically created in database
- No Redis needed

### Production
- PostgreSQL (managed: Heroku Postgres, RDS, DigitalOcean, etc.)
- Sessions stored in database
- Optional: Add Redis later for caching if needed

---

## Related ADRs

- ADR-003: PostgreSQL persistence
- ADR-004: Session-based authentication
- ADR-002: Django + Django REST Framework

---
