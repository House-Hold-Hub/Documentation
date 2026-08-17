# ADR-011: Identity and session security

> **Status:** Accepted  
> **Date:** 2026-08-16  
> **Owner:** Backend repository with Security and Documentation governance  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Identity representation, verification, linking, CSRF, and session security  
> **Supersedes:** [ADR-004](ADR-004-session-based-authentication.md) and the cookie/session-management examples in [ADR-007](ADR-007-database-backed-sessions.md)  
> **Superseded by:** —

## Context

The MVP supports email/password authentication and Google OAuth in a browser application. The historical session ADR selected secure server-side sessions, but its examples made the CSRF cookie unreadable, used `SameSite=Strict` without accounting for OAuth top-level redirects, allowed ambiguous automatic social-account linking, and did not define account-wide session revocation.

The updated decision must keep Django's supported identity/session facilities, prevent account takeover at email collisions, and allow immediate server-side revocation without introducing device-management UI or continuous activity tracking.

## Decision

### Identity model

- Use the custom UUID Django User from [ADR-010](ADR-010-backend-runtime-baseline.md), integrated with Django authentication and django-allauth.
- Use django-allauth's verified-email representation as the canonical verification state.
- Use django-allauth `SocialAccount`, or its supported equivalent, as the provider-identity relationship.
- Do not add a bespoke password field or provider-specific `google_id`.
- Do not persist Google access or refresh tokens unless a future feature requires Google API access.

### Email verification

Email/password users must prove ownership of their email before normal application access. Before verification, expose only the minimum verification lifecycle: verification status, resend, safe correction/change of the pending email where supported, and cancel/logout.

A trusted OAuth provider's verified-email claim may satisfy verification only after correct issuer, audience, and provider-trust validation.

### Google signup and linking

If a Google identity's email does not correspond to an existing local account, normal social signup may create the local account under the approved identity model.

If the email collides with an existing account:

- do not link automatically;
- do not create an ambiguous duplicate;
- require authentication to the existing account;
- require recent reauthentication;
- require an explicit connect action.

Link and unlink operations require recent reauthentication. HouseHoldHub logout ends only the HouseHoldHub session; it does not log the user out of Google.

### Browser session and CSRF contract

- Use database-backed Django sessions and an indexed user-session registry compatible with Django/django-allauth.
- Configure the MVP HouseHoldHub session to expire after 14 days. Logout, required revocation, and Django authentication-hash invalidation may end it earlier; 14 days is not a guaranteed minimum login duration.
- Prefer a same-origin frontend/API deployment.
- Store the session identifier in an `HttpOnly`, `Secure` cookie.
- Use a readable Django CSRF cookie and send its value in `X-CSRFToken` for unsafe requests.
- Use `SameSite=Lax` where required for OAuth top-level redirects.
- Require OAuth `state` and validate it on return.
- Rotate the HouseHoldHub session after authentication and security-sensitive identity changes.
- Keep Django's built-in authentication-hash/session-security behavior where applicable.

The registry is indexed by user/session identity sufficiently to revoke sessions without decoding or scanning session payloads. MVP does not include device-management UI or continuous activity tracking.

### Revocation matrix

| Event | Required server-side result |
|---|---|
| Normal logout | Revoke the current HouseHoldHub session |
| Password reset | Revoke all sessions |
| Authenticated password change | Preserve/rotate the current session; revoke all others |
| Primary-email change | Require recent reauthentication, rotate current session, revoke all others |
| OAuth link or unlink | Require recent reauthentication, rotate current session, revoke all others |
| Account disable or soft deletion | Immediately revoke all sessions |
| Account restoration | Require fresh authentication; never restore old sessions |

An invitation's non-secret pending intent may survive the same browser's required session rotation as defined by [ADR-013](ADR-013-invitation-security.md). The bearer invitation token never enters the session.

## Consequences

### Positive

- Identity state relies on supported Django/django-allauth representations instead of parallel application flags and provider fields.
- Explicit linking prevents email-collision account takeover.
- Indexed session ownership enables immediate account-wide revocation.
- The CSRF cookie/header design works with the official SPA while the session cookie remains unreadable to JavaScript.
- Session rotation protects authentication boundary changes without breaking an approved same-browser invitation journey.

### Costs and risks

- Backend session lifecycle must update the registry atomically enough to avoid orphaned valid sessions.
- Authentication tests must cover session preservation, rotation, and revocation for each security event.
- OAuth trust validation and linking flows are more involved than automatic email linking.
- Same-origin deployment is preferred but not guaranteed; any cross-origin deployment must preserve the same CSRF and cookie properties deliberately.

## Supersession

ADR-004 is retained as the historical selection of session authentication but is fully superseded by this more precise identity/session decision. ADR-007 remains accepted for database-backed storage and the absence of Redis; its historical cookie examples and assumptions about inspecting session payloads are non-normative where they conflict with this ADR.

## Related decisions

- [Security model](../../security/security-model.md)
- [ADR-007: Database-backed sessions](ADR-007-database-backed-sessions.md)
- [ADR-013: Invitation security](ADR-013-invitation-security.md)
