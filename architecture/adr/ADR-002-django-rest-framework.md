# ADR-002: Django + Django REST Framework Backend

**Date:** August 16, 2026  
**Status:** Accepted  
**Author:** Engineering Team  
**Owner:** Documentation repository; Backend/Architecture stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** Django + Django REST Framework selection; runtime versions are superseded  
**Superseded by:** [ADR-010: Backend runtime baseline](ADR-010-backend-runtime-baseline.md) (Django-version and dependency-example portions only)

> **Record scope:** The Django + Django REST Framework selection remains accepted. Django 4.2 and every dependency, identity-model, cookie, and code example below are historical and non-normative; current runtime and version ownership are defined by ADR-010 and the [technology baseline](../technology-baseline.md).

---

## Context

HouseHoldHub MVP requires a backend API for a web application with:
- User authentication and session management
- Multi-tenant data isolation (household scoping)
- Permission model (owner vs. member roles)
- Relational data model (users, households, tasks, expenses, etc.)
- ACID transaction guarantees (for financial data)

We must choose a Python web framework (or other language entirely). Options:
1. **Django + Django REST Framework** (mature, full-featured, batteries-included)
2. **FastAPI** (modern, async-first, lightweight)
3. **Flask** (lightweight, minimal framework)
4. **Express.js/Node.js** (JavaScript ecosystem)
5. **Go (Gin/Echo)** (performance, simplicity)

---

## Decision

Use **Python + Django 4.2 LTS + Django REST Framework** for the backend.

---

## Rationale

### Why Django?

1. **Mature & Battle-Tested**
   - 15+ years of production use
   - Used by Instagram, Spotify, Dropbox, Pinterest
   - Excellent security track record
   - Stable API and minimal breaking changes

2. **Built-In Features (Batteries Included)**
   - User authentication (`django.contrib.auth`)
   - Session management (`django.contrib.sessions`)
   - Permissions and groups (`django.contrib.auth`)
   - Admin interface (`django.contrib.admin`)
   - ORM (`django.db.models`)
   - Database migrations (`django.db.migrations`)
   - CSRF protection (middleware)
   - XSS protection (template auto-escaping)
   - SQL injection prevention (parameterized queries)

3. **Excellent for Permission-Heavy Applications**
   - Built-in permission framework
   - Easy to implement custom permissions
   - Row-level security patterns well-documented
   - Household scoping straightforward with ORM filters

4. **Strong Relational Database Support**
   - Django ORM handles complex queries, relationships, transactions
   - Excellent PostgreSQL support (native JSON, arrays, UUID)
   - Database migrations integrated into development workflow

5. **Django REST Framework**
   - Built on Django, adds REST API capabilities
   - Serializers for validation and transformation
   - Class-based views for standard CRUD patterns
   - Built-in pagination, filtering, sorting
   - Authentication integration (session auth, token auth, etc.)
   - Automatic API documentation (OpenAPI/Swagger)

6. **Reduces Custom Infrastructure**
   - No need for custom auth system (use django.contrib.auth)
   - No need for custom ORM (use Django ORM)
   - No need for custom migrations (use Django migrations)
   - No need for custom session management (use Django sessions)
   - No need for custom permission checks (use Django permissions)

7. **Team Expertise**
   - Python is widely-known language
   - Django is popular framework (large community, many resources)
   - Learning curve reasonable for experienced developers

---

## Alternatives Considered

### FastAPI
- **Pros:** Modern, async-first, automatic API documentation
- **Cons:** Requires more custom work for auth, ORM, migrations; less mature than Django
- **Not chosen:** Django is simpler for MVP with its included features

### Flask
- **Pros:** Lightweight, minimal
- **Cons:** Requires many external dependencies; less opinionated; more work to secure properly
- **Not chosen:** Django's batteries-included approach is better for MVP

### Express.js/Node.js
- **Pros:** JavaScript everywhere; async by default; good for real-time features
- **Cons:** Less mature defaults for security; no built-in ORM (must choose one); requires more custom work
- **Not chosen:** Django's security defaults are better for MVP

### Go (Gin/Echo)
- **Pros:** Excellent performance; compile to single binary
- **Cons:** Different language (fewer people know Go); less mature standard library for web apps
- **Not chosen:** Django is adequate for expected MVP scale; Go is over-engineered for MVP

---

## Consequences

### Positive
- ✓ Built-in auth, sessions, ORM, migrations — minimal custom code
- ✓ Excellent security defaults (CSRF, XSS, SQL injection protection)
- ✓ Permission framework built-in; household scoping straightforward
- ✓ Admin interface for debugging and data management (free)
- ✓ Large community; many tutorials and examples
- ✓ Excellent documentation
- ✓ Easy to hire Django developers
- ✓ Stable API; minimal changes between versions

### Negative
- ✗ Monolithic (includes features we may not use)
- ✗ Python may be slower than Go/Node.js (acceptable for MVP scale)
- ✗ Not async by default (can add async views later if needed)
- ✗ Steeper learning curve than minimal frameworks (Flask)

### Migration Path
- Django to FastAPI: Requires rewrite; not recommended
- Django to other frameworks: Straightforward if API is well-documented

---

## Implementation

### Project Structure

```
Backend/
├── householdhub/              # Django project
│   ├── settings.py            # Configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI (for async tasks, future)
├── api/                        # Django app
│   ├── models.py              # User, Household, Task, etc.
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # DRF viewsets
│   ├── permissions.py         # Custom permission classes
│   ├── authentication.py       # Custom auth if needed
│   ├── urls.py                # API routes
│   └── tests.py               # Tests
├── tests/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container image
└── docker-compose.yml         # Local development
```

### Key Dependencies

```
# requirements.txt
Django==4.2.x
djangorestframework==3.14.x
psycopg2-binary==2.9.x        # PostgreSQL adapter
python-decouple==3.x           # Environment variables
pytest==7.x                    # Testing
pytest-django==4.x
```

### Authentication

Use Django's built-in authentication:
```python
# User model via django.contrib.auth.models.User
# Or extend with AbstractUser for custom fields
```

### Session Management

Use Django's database-backed sessions:
```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks (configurable)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # In production
SESSION_COOKIE_SAMESITE = 'Strict'
```

### Permissions

Leverage Django's permission framework:
```python
# Custom permission classes for DRF
from rest_framework.permissions import BasePermission

class IsHouseholdMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(
            household=obj.household,
            user=request.user
        ).exists()
```

---

## Related ADRs

- ADR-003: PostgreSQL persistence
- ADR-004: Session-based authentication
- ADR-007: Database-backed sessions for MVP

---
