# ADR-003: PostgreSQL for Persistence

**Date:** August 16, 2026  
**Status:** Accepted  
**Author:** Engineering Team  
**Owner:** Documentation repository; Backend/Infrastructure stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** PostgreSQL as the MVP persistence technology  
**Superseded by:** —

> **Record scope:** The PostgreSQL selection remains accepted. Exact deployed versions belong to Infrastructure configuration, executable schema belongs to Backend models/migrations, and the implementation/vendor/performance examples below are historical and non-normative. PostgreSQL row-level security is not used for MVP.

---

## Context

HouseHoldHub MVP requires a database to persist:
- User accounts and authentication
- Households and memberships
- Tasks, shopping items, expenses, inventory
- Sessions (if database-backed)

Requirements:
- ACID transactions (important for expenses and financial consistency)
- Relational model (users, households, tasks, etc. with relationships)
- Multi-user application (concurrent access)
- Scalable (MVP to 10k-100k households without architectural change)

Options:
1. **PostgreSQL** (relational, ACID, feature-rich)
2. **MySQL** (relational, ACID, simpler)
3. **MongoDB** (document-oriented, NoSQL)
4. **SQLite** (file-based, simple)

---

## Decision

Use **PostgreSQL 14+** as the primary and only data store for MVP.

---

## Rationale

### Why PostgreSQL?

1. **ACID Transactions**
   - Essential for financial data (expenses, multi-step operations)
   - Ensures data consistency even under concurrent access

2. **Relational Model**
   - Natural fit for domain (users, households, tasks, relationships)
   - Foreign keys enforce data integrity
   - Joins are efficient and well-optimized

3. **Rich Feature Set**
   - JSON/JSONB for semi-structured data (extensible future features)
   - Arrays for storing lists (if needed)
   - Full-text search for searching tasks, shopping, inventory
   - Row-level security (RLS) for future household isolation optimization
   - Window functions for analytics (future dashboards)

4. **Django ORM Integration**
   - Django's ORM is built for relational databases
   - Excellent PostgreSQL-specific support (native JSON, arrays, UUID, etc.)
   - QuerySet API is powerful and flexible

5. **Production-Grade**
   - Used by major companies (Shopify, Netflix, Instagram, GitHub, etc.)
   - Excellent reliability and stability
   - Strong open-source community
   - Excellent tooling (pgAdmin, DBeaver, etc.)

6. **Scalability**
   - Scales from single instance (MVP) to enterprise without architectural change
   - Sharding is possible if needed (future)
   - Replication for HA (future)
   - Connection pooling straightforward

7. **Cost**
   - Open-source (free)
   - Managed versions affordable (Heroku Postgres, RDS, DigitalOcean, etc.)
   - Single instance sufficient for MVP

---

## Alternatives Considered

### MySQL
- **Pros:** Similar to PostgreSQL; slightly faster for some operations
- **Cons:** Fewer advanced features; less mature for JSON; less suitable for complex relational queries
- **Not chosen:** PostgreSQL's feature set justifies slightly higher resource usage

### MongoDB
- **Pros:** Flexible schema; good for rapidly-evolving data model
- **Cons:** Document-oriented (not relational); weaker ACID guarantees; household scoping harder
- **Not chosen:** Relational model is more suitable for this domain; ACID important for expenses

### SQLite
- **Pros:** Simple; no server setup; good for prototyping
- **Cons:** Not suitable for multi-user web application; concurrent write limitations
- **Not chosen:** SQLite only appropriate for development; MVP is multi-user web application

---

## Consequences

### Positive
- ✓ ACID guarantees for data consistency
- ✓ Excellent fit for relational domain model
- ✓ Rich query capabilities
- ✓ Django ORM perfectly suited
- ✓ Scales from MVP to enterprise
- ✓ Managed versions very affordable
- ✓ Excellent tooling and community

### Negative
- ✗ Slightly more complex than simpler databases
- ✗ Requires schema planning upfront
- ✗ Not suitable for unstructured data (documents, media files)

### Migration Path
- PostgreSQL single instance → single instance with replicas (HA)
- PostgreSQL single instance → PostgreSQL cluster (sharding, future)
- PostgreSQL → other database: Only necessary if domain fundamentally changes to document-oriented

---

## Implementation

### Schema

Define all tables via Django ORM models:
```python
# models.py
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Constraints
    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
```

Migrations auto-generated:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Connection

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'householdhub',
        'USER': 'householdhub_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Development

```bash
# Docker Compose
docker-compose up -d db

# Or local install
brew install postgresql
createdb householdhub
```

### MVP Deployment

Single PostgreSQL instance (not replicated, not sharded):
- Heroku Postgres (managed)
- AWS RDS (managed)
- DigitalOcean Managed Database (managed)
- Self-hosted (unmanaged)

All provide automated backups, monitoring, and simple scaling.

---

## Related ADRs

- ADR-002: Django + Django REST Framework backend
- ADR-007: Database-backed sessions for MVP

---
