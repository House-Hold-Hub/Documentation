# ADR-010: Backend runtime baseline

> **Status:** Accepted  
> **Date:** 2026-08-16  
> **Owner:** Backend repository with Documentation architecture governance  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Backend runtime and framework baseline ownership  
> **Supersedes:** The Django-version portion of [ADR-002](ADR-002-django-rest-framework.md)  
> **Superseded by:** —

## Context

ADR-002 accepted Django and Django REST Framework but pinned Django 4.2 LTS in its historical decision and examples. Later planning material proposed a different, incorrect baseline. The canonical runtime must be compatible, long-lived, and separate the durable major/runtime choice from exact dependency pins.

The identity model also must be selected before the first migration because changing Django's user model afterward creates avoidable migration complexity.

## Decision

Use:

- Python 3.14;
- Django 5.2 LTS;
- Django REST Framework;
- PostgreSQL through the Django ORM and Django migrations;
- a custom UUID Django User model created before the first migration;
- Django authentication integrated with django-allauth.

The User model uses Django's password facilities and django-allauth's supported email and social-account representations. It does not contain a bespoke password field or provider-specific `google_id`.

Exact Python patch, Django patch, DRF, django-allauth, database adapter, and other dependency versions are owned by Backend manifests and committed lockfiles. The selected versions must be mutually compatible with Python 3.14 and Django 5.2 LTS.

## Consequences

### Positive

- The project uses an LTS Django line with an explicit Python runtime.
- The backend retains Django's integrated authentication, ORM, migration, session, admin, and security facilities.
- Exact security and compatibility updates can be applied through dependency manifests without rewriting the architectural record.
- Establishing the UUID User before migration avoids a later identity-primary-key migration.

### Costs and risks

- Dependencies must be checked for Python 3.14 and Django 5.2 compatibility before they are locked.
- Backend scaffolding must configure the custom User model from the outset.
- Historical Django 4.2 examples cannot be copied as current setup instructions.

### Version ownership

Repository manifests and lockfiles are authoritative for installed versions. This ADR is authoritative for the approved runtime/framework family. A future change away from Python 3.14 or Django 5.2 LTS requires a superseding ADR; a compatible patch upgrade does not.

## Supersession

ADR-002 remains accepted for the durable choice of Django + Django REST Framework. This ADR supersedes only its Django 4.2 baseline and dependency snippets. Those historical sections are non-normative.

## Related decisions

- [Technology baseline](../technology-baseline.md)
- [ADR-003: PostgreSQL persistence](ADR-003-postgresql-persistence.md)
- [ADR-011: Identity and session security](ADR-011-identity-and-session-security.md)
