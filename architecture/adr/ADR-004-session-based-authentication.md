# ADR-004: Session-Based Authentication

**Date:** August 16, 2026  
**Status:** Superseded  
**Author:** Security/Engineering Team  
**Owner:** Documentation repository; Security/Backend stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** Historical session-authentication decision provenance only  
**Superseded by:** [ADR-011: Identity and session security](ADR-011-identity-and-session-security.md)

> **Historical scope:** Session authentication remains part of the current baseline, but ADR-011 replaces this record's identity, OAuth-linking, CSRF, cookie, rotation, and revocation details. All implementation examples below are non-normative.

---

## Context

HouseHoldHub MVP is a browser-based web application. Users authenticate and perform actions on behalf of themselves within household contexts.

We must choose an authentication mechanism:
1. **Session-Based** (traditional web: cookies, server-side session state)
2. **JWT** (stateless tokens, more modern)
3. **OAuth 2.0** (delegated auth, for social login)
4. **Hybrid** (session for web, JWT for mobile/API)

---

## Decision

Use **session-based authentication with HTTP-only secure cookies** for the MVP.

Additionally, support **Google OAuth 2.0** as a social login option.

---

## Rationale

### Why Session-Based?

1. **More Secure in Browsers**
   - HTTP-only cookies prevent XSS attacks (JavaScript cannot access session token)
   - JWT stored in localStorage is vulnerable to XSS (attacker can read token)
   - Session token stored in cookie is only sent on HTTP requests, not in JavaScript

2. **Simpler Logout**
   - Session-based: server-side revocation (delete session immediately)
   - JWT: token remains valid until expiration; requires blacklist to revoke
   - Session-based logout is instant and guaranteed

3. **Better for Web Applications**
   - Session-based is standard pattern for traditional web apps
   - Excellent CSRF protection via SameSite cookies and CSRF tokens
   - Django's built-in session middleware handles this automatically

4. **Session Tracking & Auditing**
   - Sessions stored in database; easy to query active sessions
   - Can see who is logged in, from which devices, last activity
   - Important for security monitoring and user support

5. **Works Well with Django**
   - Django's auth system built for sessions
   - Middleware handles session loading on every request
   - Permission checking straightforward

### Why NOT JWT?

- **XSS Vulnerability:** Token stored in localStorage can be stolen
- **Revocation Difficult:** Token remains valid until expiration; revocation requires blacklist
- **Not Ideal for Web:** Better for stateless APIs or mobile apps
- **Over-engineered for MVP:** MVP is single web application, not multiple independent clients

### Why Add Google OAuth?

- **User Convenience:** Users can sign in with Google instead of creating password
- **Reduced Account Management:** Users don't need to remember HouseHoldHub password
- **Social Proof:** "Sign in with Google" button increases trust
- **Implementation:** Django social-auth package makes this straightforward

---

## Alternatives Considered

### Pure JWT (No Sessions)
- **Pros:** Stateless; can scale to multiple servers without session affinity
- **Cons:** Token in localStorage vulnerable to XSS; logout difficult; not ideal for web
- **Not chosen:** Session-based is more secure for browser-based apps

### Multi-Auth (Session + JWT)
- **Pros:** Flexibility for web and mobile
- **Cons:** Adds complexity for MVP; can add later
- **Not chosen:** Defer mobile JWT support to post-MVP; session-based sufficient for web MVP

### OAuth Only (No Username/Password)
- **Pros:** Simplifies account management; delegates to Google
- **Cons:** Users can't sign up without Google; users prefer password option
- **Not chosen:** Support both email/password and OAuth

---

## Consequences

### Positive
- ✓ Secure for browser-based applications (HTTP-only cookies)
- ✓ Simple logout (server-side revocation)
- ✓ Excellent CSRF protection (Django middleware)
- ✓ Session tracking for auditing and user support
- ✓ Works well with Django's built-in auth
- ✓ Familiar pattern for web developers

### Negative
- ✗ Stateful (requires session storage)
- ✗ Cannot easily scale to multiple servers without sticky sessions (mitigated by shared session store)
- ✗ Mobile apps need different strategy (JWT or refresh tokens)

### Migration Path
- Session-based to JWT: Straightforward refactor; token-based auth layer can be added
- Session-based to multi-auth: Add JWT endpoint alongside session-based endpoint
- **Recommended:** Start with sessions; add JWT/mobile support only if needed post-MVP

---

## Implementation

### Django Session Authentication

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    # ...
]

MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # ...
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks (configurable)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Set to True in production
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
```

### Login Flow

```python
from django.contrib.auth import authenticate, login

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Django auth system handles password verification
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        login(request, user)  # Creates session
        return Response({'status': 'logged in'}, status=200)
    else:
        return Response({'error': 'invalid credentials'}, status=401)
```

### Logout Flow

```python
from django.contrib.auth import logout

@api_view(['POST'])
def logout_view(request):
    logout(request)  # Deletes session server-side
    return Response({'status': 'logged out'}, status=200)
```

### Protected Endpoints

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'user': request.user.email})
```

### Google OAuth 2.0

```python
# Install: pip install django-allauth

# settings.py
INSTALLED_APPS = [
    # ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

# Flow:
# 1. Frontend redirects to Google auth endpoint
# 2. Google returns authorization code to backend callback
# 3. Backend exchanges code for user info
# 4. Backend creates/links user account
# 5. Backend creates session and returns to frontend
```

---

## Security Considerations

1. **CSRF Protection:** Django middleware generates and validates CSRF tokens
2. **XSS Protection:** Session token in HTTP-only cookie (cannot be accessed by JavaScript)
3. **Password Hashing:** Django uses PBKDF2 by default (can use bcrypt/Argon2)
4. **Session Expiration:** Automatic cleanup via `python manage.py clearsessions`
5. **Rate Limiting:** Limit login attempts per IP address

---

## Related ADRs

- ADR-002: Django + Django REST Framework backend
- ADR-007: Database-backed sessions for MVP

---
