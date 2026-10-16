# ADR-016: Authentication launch security defaults

> **Status:** Proposed  
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

- **Length:** at least 15 characters; at least 128 characters accepted. Longer input is rejected with `400`, never silently truncated.
- **Characters:** any Unicode characters, including spaces, are accepted as entered.
- **No composition rules** (required character classes), no periodic expiry, no password hints, and no knowledge-based recovery questions.
- **Blocklist:** keep Django's common-password, user-attribute-similarity (email and name), and all-numeric validators. A breached-password lookup against an external service is not part of the launch defaults; adding one is an M8 decision because it introduces a third-party data flow.
- **Hashing:** Django's default password hasher with the work factor of the Django release in use, including Django's rehash-on-login upgrade. The Backend does not pin an iteration count.
- A password that fails the policy returns `400` with field-level details; no other status is used.

### One-time bearer credentials

These apply to the email-verification, primary-email-change, and password-reset bearers. Invitation verifiers keep the rules and 30-day lifetime of [ADR-013](ADR-013-invitation-security.md); only the entropy and storage rows below also apply to them.

| Property | Launch default |
|---|---|
| Entropy | At least 256 bits from a cryptographically secure random source |
| Storage | Only a SHA-256 digest of the bearer is persisted; a stateless HMAC token that is never persisted also conforms if it keeps every property in this table |
| Use | Single-use; consumption is atomic with the state change it authorizes |
| Rotation | Issuing a new bearer of the same purpose for the same account or address invalidates every earlier one |
| Password-reset lifetime | 1 hour |
| Email-verification lifetime | 24 hours |
| Primary-email-change verification lifetime | 1 hour |

An expired, consumed, rotated, or unknown bearer produces the same response as the operation's other invalid-bearer outcomes.

### Recent reauthentication

Operations that require recent reauthentication accept an authentication or reauthentication performed in the current session within the last **5 minutes**.

### Authentication rate limits

Each operation below is limited on every key listed; exceeding any one returns `429` (`RATE_LIMITED`) with `Retry-After` set to the whole seconds until the exhausted window frees a slot. Windows may be fixed or sliding.

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
- **Shared, PostgreSQL-backed counters.** Counters are shared by every application process and stored in PostgreSQL (Django's database cache backend conforms); per-process memory does not conform in a deployed environment. No Redis or queue is introduced.
- **Minimized keys.** Counter keys derived from an email address or client IP are keyed hashes, never plaintext, and counter entries expire with their window. Their retention otherwise follows `D03`.
- **Client IP.** The client IP comes from the request's peer address unless Infrastructure configures a trusted proxy; client-supplied forwarding headers are never trusted by default.
- **Operations without `429`.** An operation whose contract does not declare `429` is not rate-limited until the contract adds it; this ADR does not change the contract.

## Consequences

### Positive

- M1 authentication can be implemented against explicit, reviewable values instead of framework defaults.
- Reset links live for an hour instead of the multi-day framework default.
- Limits are enforced consistently across processes without new infrastructure.
- Enumeration safety and the no-lockout rule keep throttling from creating new attack surfaces.

### Costs and risks

- A 15-character minimum adds friction at signup; Google sign-in remains the low-friction path.
- Shared networks (a household behind one address) share per-IP limits; the per-IP values are set high enough for a household's normal use, and M8 revisits them with observed traffic.
- Database-backed counters add a write per limited request.
- Without a breached-password check, a long but leaked password is accepted until M8 decides otherwise.

## Related decisions

- [Roadmap: deferred decision D01](../../product/roadmap.md)
- [Security model](../../security/security-model.md)
- [ADR-011: Identity and session security](ADR-011-identity-and-session-security.md)
- [ADR-013: Invitation security](ADR-013-invitation-security.md)
- [ADR-015: Transactional email delivery](ADR-015-transactional-email-delivery.md)
