# HouseHoldHub Security Model

> **Status:** Accepted  
> **Owner:** Documentation repository; implemented by Backend, Frontend, Infrastructure, and Automation  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Cross-cutting identity, session, token, isolation, logging, and audit requirements  
> **Supersedes:** Security guidance scattered across archived system-design and planning snapshots

## Scope and authority

This document consolidates security outcomes and lifecycle rules. The [permissions matrix](../product/permissions-matrix.md) owns readable product authorization, accepted [ADRs](../architecture/adr/README.md) own durable technical rationale, and [`api/openapi.yaml`](../api/openapi.yaml) owns operation security and wire behavior. This document does not duplicate request or response schemas.

## Security boundaries

- Every household-scoped request is authenticated and authorized against current server-side state.
- Household membership is the tenant-isolation boundary. Access to one household conveys no knowledge of another household's resources.
- Browser-held bearer material is minimized. HouseHoldHub authentication uses server-side sessions, not browser-stored access tokens.
- Secrets and personal data are minimized in logs, delivery metadata, telemetry, and third-party systems.
- Security-sensitive state transitions are atomic and revalidated when consumed; prior validation is not a permanent authorization grant.

## Identity and email verification

HouseHoldHub uses a custom UUID Django user model created before the first migration. Django authentication and django-allauth own password hashing, email-address verification state, and provider identity relationships. The application does not define a bespoke password field, duplicate `email_verified` boolean, or provider-specific `google_id` field.

Email/password accounts must verify ownership of their email address before normal application access. Before verification, the session may access only the minimum verification lifecycle: verification status, rate-limited resend, safe correction of a pending email where supported, logout, and cancellation. It cannot access households, invitation previews, or normal application features.

A trusted OAuth provider's verified-email claim may satisfy verification only after issuer, audience, state, and provider trust validation. Provider-specific alias transformations are forbidden. Email matching uses the canonical normalization and verified-address representation supported by Django/django-allauth; it does not remove Gmail dots or plus-address suffixes.

## Google OAuth and account linking

- A Google identity whose email does not collide with an existing local account may complete normal social signup.
- An email collision never triggers automatic linking and must not create an ambiguous duplicate account.
- Linking requires authentication to the existing account, recent reauthentication, and an explicit connect action.
- Provider identity is represented through django-allauth `SocialAccount` or its supported equivalent.
- Google access and refresh tokens are not persisted unless a future feature requires Google API access and receives a separate decision.
- HouseHoldHub logout ends only the HouseHoldHub session; it does not attempt to log the user out of Google.

OAuth `state` is mandatory and validated. Standards-required OAuth callback values may appear in the callback query, but must be redacted from logs and error-reporting context.

## Session and CSRF protection

Authentication uses PostgreSQL-backed Django sessions. Redis is not an MVP dependency.

- The server-side session lifetime is 14 days, subject to earlier expiry, rotation, or revocation under the events below.
- The session cookie is `HttpOnly` and `Secure` outside local development.
- The Django CSRF cookie is readable by the official frontend so it can send `X-CSRFToken` on every unsafe request.
- `SameSite=Lax` is used where the validated OAuth top-level redirect flow requires the pre-authentication session.
- Same-origin frontend/API deployment is the default topology. Any later cross-origin deployment needs an explicit CORS/credential review.
- A public operation in OpenAPI (`security: []`) is unauthenticated, not CSRF-exempt. Public unsafe browser requests still use the CSRF bootstrap and header contract.
- Session identifiers rotate after authentication and security-sensitive privilege changes. Only explicitly approved, non-secret state may survive rotation.

The Backend maintains an indexed user-session registry compatible with Django/django-allauth. It supports server-side revocation without adding MVP device-management UI or continuous activity tracking.

| Event | Required session behavior |
|---|---|
| Normal logout | Revoke the current HouseHoldHub session |
| Password reset | Revoke every session for the account |
| Authenticated password change | Preserve and rotate the current session; revoke all others |
| Primary-email change | Require recent reauthentication, rotate the current session, and revoke all others |
| OAuth link or unlink | Require recent reauthentication, rotate the current session, and revoke all others |
| Account disable or soft deletion | Revoke every session immediately |
| Account restoration | Require fresh authentication; never restore old sessions |

Django's authentication-hash/session invalidation behavior remains in force where applicable. Session cleanup is a scheduled operational requirement.

## Invitation verifier transport and acceptance

Email invitations use a high-entropy bearer verifier in the URI fragment. A fragment is the only approved bearer exception to the general URL rule because it is processed by the browser and is not sent in the HTTP request target.

The landing flow must:

1. read the fragment without sending it to the server as a path or query value;
2. avoid localStorage and sessionStorage;
3. remove it from browser-visible navigation state immediately;
4. exchange it through a rate-limited POST body;
5. prevent it from reaching application logs, telemetry, analytics, error context, referrers, or persistent browser storage;
6. use a restrictive Content Security Policy, `Referrer-Policy: no-referrer`, and `Cache-Control: no-store`;
7. discard the raw verifier after exchange.

Only a cryptographic verifier hash is stored with the invitation. The verifier is single-use, expires after the approved 30-day invitation lifetime, and rotates on resend. A successful exchange retains only a non-secret, generation-bound invitation intent in the DB-backed session. The intent must identify the validated invitation/verifier generation so resend or rotation makes every older intent unusable. An in-place hash replacement that leaves an old intent valid is nonconforming.

The same-browser intent survives signup, login, email verification, and normal session-key rotation. It does not become global user state and is not automatically copied across devices. A cross-device verification makes the account verified globally, but continuation occurs in the originating session or through a newly valid invitation link.

Exchange does not create membership. After authentication and email verification, the server rechecks that the invitation and its verifier generation are current, pending, unexpired, unrevoked, and unconsumed; verifies that a normalized verified address matches the invitation target; returns only the approved safe preview; and requires explicit acceptance. Acceptance locks and consumes the invitation atomically while enforcing membership uniqueness. Owners revoke by invitation identifier, not by bearer verifier.

## Other bearer credentials

Bearer credentials must never appear in server-visible request paths, query strings, logs, referrers, telemetry, analytics, or persistent browser storage. This rule applies to password-reset and email-verification credentials as well as invitations. Standards-required OAuth callback parameters are narrowly excepted from the path/query ban but remain mandatory, validated, and redacted.

Bearer credentials are high entropy, time limited, single purpose, stored only as cryptographic hashes where server persistence is necessary, and invalidated after successful use. Exact password policy, reset-token constants, and rate limits remain decision gate D01; safe launch defaults must be selected before authentication contract implementation.

Password-reset requests always return an enumeration-safe response regardless of account existence or provider outcome. Response timing must not trivially disclose whether a provider call occurred for an existing account.

## Household authorization and isolation

The Backend enforces household access through current Membership records, household-scoped service/query boundaries, object authorization, and comprehensive negative isolation tests. PostgreSQL row-level security is not part of the MVP.

- `Household.owner_id` is the authoritative owner reference.
- A matching owner Membership is created and maintained atomically; owner Membership removal is forbidden.
- Public MVP ownership transfer does not exist.
- Disabling an owner revokes access but preserves the User, `owner_id`, and owner Membership.
- An owner cannot be anonymized or hard-deleted while owning an active household; administrative lifecycle handling must first resolve every owned household. Legal and retention specifics remain decision gate D03.
- Membership removal takes effect on the next server request. Frontend cache cleanup may occur through normal invalidation, refetch, or 403/404 handling, but cached client state is never authorization.

Task assignment uses a Membership reference. Same-household assignment is guaranteed by centralized service/write validation and negative integrity tests. Documentation must not claim that a normal foreign key or a cross-table PostgreSQL `CHECK` enforces this invariant. A clean composite database constraint may supplement, but not replace, the approved MVP guarantee.

Cross-household or otherwise out-of-scope object identifiers return 404. A known in-household action denied by the permissions matrix returns 403.

## Household join-code protection

The household join code is a separate bearer mechanism from invitations.

- It is globally unique and consists of eight uppercase alphanumeric characters.
- Only the owner may read or regenerate it.
- It is omitted from generic household and dashboard responses.
- Join attempts are rate-limited and use a uniform invalid-code response.
- The code is submitted in a request body, not a server-visible path or query.
- Regeneration immediately invalidates the previous code.

## Input handling and browser content safety

- Server-side boundaries validate untrusted request values before domain use; client validation is supplementary.
- Untrusted values must never be interpolated into SQL or equivalent command text. Backend persistence uses the Django ORM or parameterized operations with equivalent injection resistance.
- User-controlled household, task, shopping, expense, inventory, and identity text is rendered as text with context-appropriate output encoding. The MVP does not render arbitrary user-supplied HTML; any future rich-content feature requires an explicit sanitization policy and security review.
- Content Security Policy and framework protections complement, but do not replace, safe input handling and contextual output encoding.
- Security verification includes representative injection and cross-site-scripting attempts across user-controlled fields and browser-rendered error states.

## Transactional email security

The Backend owns a provider-neutral adapter, templates, token ordering, delivery state, resend behavior, safe errors, audit events, and tests. Infrastructure owns provider provisioning, verified sender/domain configuration, SPF/DKIM/DMARC, credentials, rotation, and provider health. Automation owns test-provider fixtures, integration support, and secret scanning.

The MVP sequence is: commit domain state, invoke a bounded synchronous provider call from `transaction.on_commit()`, and durably record the minimum delivery outcome needed for recovery. Provider exceptions never imply rollback of committed domain state. Verification and invitation failures retain recoverable pending state and support rate-limited resend. Provider acceptance means accepted for processing, not delivered to the inbox.

Delivery/audit records may store identifiers, status, attempt timing/count, provider request identifier, and safe error class. They must not store plaintext authentication, reset, or invitation credentials; full sensitive links; rendered secret-bearing bodies; cookies; OAuth values; or unnecessary recipient PII. No queue, Redis, Celery, or dedicated worker is introduced solely for MVP email. The exact managed provider remains decision gate D02.

## Logging, telemetry, and error handling

- Production logging is structured and includes request correlation without logging request secrets or sensitive bodies.
- Redaction applies at application, proxy, analytics, and error-tracking boundaries.
- Passwords, cookies, CSRF values, bearer verifiers, household join codes, OAuth code/state, email bodies, and full secret-bearing URLs are never logged.
- Personal email, expense, and household data is recorded only when necessary for the approved operational or audit purpose.
- Client telemetry must not capture URL fragments, request bodies containing credentials, or broad URL/parameter dumps.
- Security failures use the canonical status/error behavior in [API conventions](../api/README.md); details do not disclose cross-household existence or account registration state.

## Audit events

Critical audit events are required for invitation creation, resend, exchange outcome, acceptance, and revocation; member joins, removals, and role/ownership administration; and household soft deletion, recovery, and purge. Authentication, verification, account-link, account-disable, and session-revocation events must provide enough safe metadata for incident review without retaining credentials.

The exact audit schema and retention period are governed by decision gate D03. Audit records never contain bearer values or rendered messages.

## Verification requirements

The [testing strategy](../quality/testing-strategy.md) requires complete role/state/error coverage for authorization and household isolation. Security acceptance includes CSRF tests, OAuth state and account-collision tests, session-rotation/revocation tests, invitation replay/rotation/expiry tests, redaction tests, join-code abuse tests, and email enumeration/failure tests.

## Deferred security decisions

- **D01:** Password validators, reset-token constants, and rate-limit values are selected before M1 authentication implementation and revisited by M8 hardening.
- **D02:** The managed email provider is selected before M1 email integration; deployment, secret-store, and monitoring providers are selected before M9.
- **D03:** Launch jurisdiction and user/audit/security/email/session retention are resolved before processing real personal data, including real-email staging.
- **D04:** Numeric recovery and alert thresholds are resolved after D02/D03 and before M9 launch sign-off.

These are bounded decision gates, not permission to weaken the qualitative controls above.
