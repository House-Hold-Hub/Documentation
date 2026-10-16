# ADR-016: Authentication launch security defaults

> **Status:** Accepted  
> **Date:** 2026-10-17  
> **Owner:** Backend repository with Security and Documentation governance  
> **Last reviewed:** 2026-10-17  
> **Canonical for:** The `D01` launch defaults: password policy, one-time bearer constants, recent-reauthentication window, and authentication rate limits  
> **Supersedes:** —  
> **Superseded by:** —

## Context

The [roadmap](../../product/roadmap.md) defers `D01` (exact password-policy, password-reset-token, and authentication/rate-limit constants) with a two-step deadline: choose safe launch defaults before M1 authentication implementation and contract generation, then review and lock them by M8 hardening. The [security model](../../security/security-model.md) repeats that authentication contract implementation cannot start until the defaults exist.

M1 authentication work is now ready to start. The contract already declares `429` with an optional `Retry-After` header (`TooManyRequests`) on the operations that need abuse protection, and the Backend currently runs on Django and django-allauth defaults, some of which are unsafe for this product (a multi-day reset-link lifetime, per-process in-memory throttle counters). [ADR-011](ADR-011-identity-and-session-security.md) already fixes the 14-day session lifetime and [ADR-013](ADR-013-invitation-security.md) the 30-day invitation lifetime; this ADR does not change either.

The technology baseline excludes Redis, Celery, and queues, so any shared counter state must live in PostgreSQL.

## Decision

These values are the MVP launch defaults. They apply from M1, are configurable in the Backend's settings so M8 can change them without code changes, and are reviewed and locked by M8 hardening. A deployed environment must not disable them; test settings may.

### Password policy

The policy follows the memorized-secret guidance of NIST SP 800-63B for a single-factor password.

- **Length:** at least 15 and at most 128 characters, counted in Unicode code points. Longer input is rejected with `400`, never silently truncated. The contract declares these bounds as `minLength`/`maxLength` on the new-password fields of `signup`, `resetPassword`, and `changePassword`. The `login` password and `changePassword`'s `current_password` carry no bounds, so a later policy change never makes an existing credential unusable and a failed login stays `401`.
- **Characters:** any Unicode characters, including spaces, are accepted as entered.
- **No composition rules** (required character classes), no periodic expiry, no password hints, and no knowledge-based recovery questions.
- **Blocklist:** keep Django's common-password and user-attribute-similarity (email and name) validators. Django's all-numeric validator is not used: rejecting a password only because every character is a digit is a composition rule, and short common numeric passwords are already below the length minimum or on the common-password list. A breached-password lookup against an external service is not part of the launch defaults; adding one is an M8 decision because it introduces a third-party data flow.
- **Hashing:** Django's default password hasher with the work factor of the Django release in use, including Django's rehash-on-login upgrade. The Backend does not pin an iteration count.
- A password that fails the policy returns `400` with field-level details; no other status is used.

### One-time bearer credentials

These apply to the email-verification, primary-email-change, and password-reset bearers. Invitation verifiers keep the rules, storage, and 30-day lifetime of [ADR-013](ADR-013-invitation-security.md): their cryptographic hash is always persisted with the invitation and its verifier generation. Only the entropy row below also applies to them.

| Property | Launch default |
|---|---|
| Entropy | At least 256 bits from a cryptographically secure random source |
| Storage | Only a SHA-256 digest of the bearer is persisted; a stateless HMAC token that is never persisted also conforms if it keeps every property in this table. The stateless alternative never applies to invitation verifiers |
| Use | Single-use; consumption is atomic with the state change it authorizes |
| Rotation | Issuing a new bearer of the same purpose for the same account or address invalidates every earlier one |
| Password-reset lifetime | 1 hour |
| Email-verification lifetime | 24 hours |
| Primary-email-change verification lifetime | 1 hour |

An expired, consumed, rotated, or unknown bearer produces the same response as the operation's other invalid-bearer outcomes.

### Recent reauthentication

Operations that require recent reauthentication accept an authentication or reauthentication performed in the current session within the last **5 minutes**.

### Authentication rate limits

Each operation below is limited on every key listed; exceeding any one returns `429` (`RATE_LIMITED`). The Backend always sends `Retry-After` on these responses, set to the whole seconds until the exhausted window frees a slot. The contract keeps the header optional, which an always-present header satisfies, so clients must still handle a `429` without it. Windows may be fixed or sliding.

| Operation | Limits |
|---|---|
| `signup` | 10 per hour per client IP; 3 per hour per submitted email |
| `login` | 30 per minute per client IP; 5 failed attempts per 5 minutes per submitted email |
| `verifyEmail` | 20 per 5 minutes per client IP |
| `resendEmailVerification` | 1 per 2 minutes and 5 per hour per user |
| `requestPrimaryEmailChange` | 5 per hour per user; 3 per hour per requested email |
| `verifyPrimaryEmailChange` | 10 per 5 minutes per user |
| `requestPasswordReset` | 20 per hour per client IP; 3 per hour per submitted email |
| `resetPassword` | 20 per 5 minutes per client IP |
| `createHouseholdInvitation` | 20 per hour per inviting user |
| `resendHouseholdInvitation` | 1 per 2 minutes and 5 per day per invitation |
| `exchangeInvitationVerifier` | 20 per 5 minutes per client IP |

Rules that make the limits safe:

- **Enumeration safety.** A per-email limit counts the normalized submitted address whether or not an account exists, and a limited request returns the same `429` either way. `requestPasswordReset` stays enumeration-safe in body, status, and timing.
- **No lockout.** Limits delay attempts; they never disable an account, so an attacker cannot lock a victim out. A login refused with `429` is refused even when the password is correct, so the limit is not a password oracle. A successful login clears that email's failed-attempt count.
- **Shared, atomic, PostgreSQL-backed counters.** Counters are shared by every application process and stored in PostgreSQL. Checking and consuming a slot is one atomic operation: a single conditional statement (for example an upsert that increments and returns the count) or a transaction that holds a row lock on the counter. Concurrent requests for the same key can never together exceed the limit. A read-then-write through Django's cache API does not conform: Django documents `incr()` as non-atomic on backends without native increment support, including its database cache. Per-process memory does not conform in a deployed environment. If the limiter cannot record a request, the request is rejected rather than allowed. No Redis or queue is introduced.
- **django-allauth's built-in limits are turned off.** Its limiter (65.19.7) keeps a timestamp list in Django's cache behind an advisory `cache.add` lock. With the default per-process cache it is not shared, and with the database cache its lock can be taken twice when a stale lock row is left behind. It hashes email keys without a secret. It reports a throttled login as a form validation error, which the API would return as `400` instead of `429`. Its built-in values would also differ from this table. The Backend therefore enforces these limits with its own limiter and disables allauth's, so only one set of limits applies.
- **Minimized keys.** Counter keys derived from an email address or client IP are keyed hashes (an HMAC under a server-side secret), never plaintext or an unkeyed digest, and counter entries expire with their window. Their retention otherwise follows `D03`.
- **Client IP.** The client IP comes from the request's peer address unless Infrastructure configures a trusted proxy; client-supplied forwarding headers are never trusted by default.
- **Operations without `429`.** An operation whose contract does not declare `429` is not rate-limited until the contract adds it; this ADR adds no `429` response.

## Consequences

### Positive

- M1 authentication can be implemented against explicit, reviewable values instead of framework defaults.
- Reset links live for an hour instead of the multi-day framework default.
- Limits are enforced consistently across processes without new infrastructure.
- Enumeration safety and the no-lockout rule keep throttling from creating new attack surfaces.

### Costs and risks

- A 15-character minimum adds friction at signup; Google sign-in remains the low-friction path.
- Shared networks (a household behind one address) share per-IP limits; the per-IP values are set high enough for a household's normal use, and M8 revisits them with observed traffic.
- Database-backed counters add a locked write per limited request, and the Backend maintains its own small limiter instead of reusing django-allauth's.
- Without a breached-password check, a long but leaked password is accepted until M8 decides otherwise.

## Related decisions

- [Roadmap: deferred decision D01](../../product/roadmap.md)
- [Security model](../../security/security-model.md)
- [ADR-011: Identity and session security](ADR-011-identity-and-session-security.md)
- [ADR-013: Invitation security](ADR-013-invitation-security.md)
- [ADR-015: Transactional email delivery](ADR-015-transactional-email-delivery.md)
