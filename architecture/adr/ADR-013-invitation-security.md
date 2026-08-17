# ADR-013: Invitation token security and authenticated handoff

> **Status:** Accepted  
> **Date:** 2026-08-16  
> **Owner:** Backend repository with Frontend, Security, and Documentation review  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Invitation bearer transport, exchange, and authenticated handoff  
> **Supersedes:** Invitation transport and acceptance examples in the [archived system design](../../archive/2026-08-16-design-and-planning/SYSTEM_DESIGN.md) and other pre-baseline material  
> **Superseded by:** —

## Context

An email invitation link must carry a bearer secret to a browser without exposing it through normal server request logs, proxy paths, query analytics, referrers, or persistent browser storage. Acceptance also spans signup, login, email verification, and session rotation. Requiring the original link after every step would make the journey brittle, while storing the bearer token in the session would extend the secret's lifetime unnecessarily.

Invitation resend and revocation add another requirement: a successfully exchanged but not yet accepted intent must become invalid when its token generation is rotated or the Invitation becomes ineligible.

## Decision

### Token transport and storage

- Generate a high-entropy invitation bearer token.
- Place the token in the URI fragment. The fragment must never be sent in a server-visible request path or query string.
- The landing page exchanges the token immediately through a protected POST body.
- Remove the token from browser-visible navigation state immediately after processing.
- Never persist it in `localStorage` or `sessionStorage`.
- Never write it to application logs, telemetry, analytics, error-reporting context, referrers, or caches.
- Store only a cryptographic hash of the token server-side.
- Make the token single-use, bound to the normalized verified recipient email, and subject to the approved Invitation expiry.
- Resending rotates the token and invalidates the previous generation.

The canonical security rule is:

> Bearer tokens must never appear in server-visible request paths, query strings, logs, referrers, telemetry, analytics, or persistent browser storage.

This replaces the ambiguous historical shorthand that tokens must not appear in URLs.

### Landing-page protections

The landing and exchange flow requires:

- a restrictive Content Security Policy;
- `Referrer-Policy: no-referrer`;
- `Cache-Control: no-store`;
- rate-limited exchange attempts;
- CSRF protection where applicable;
- no third-party scripts that can observe the fragment before it is removed.

The exchange design must remain minimal. It must not introduce a second long-lived bearer credential.

### Non-secret authenticated handoff

After successful exchange:

1. discard the bearer token;
2. retain only a non-secret validated Invitation reference/intent in the server-side session;
3. bind that intent to the exact invitation token generation that was validated;
4. preserve the intent through normal session rotation in the same browser during signup, login, and email verification.

The session may store an Invitation identifier and a non-secret generation binding, or an equivalent server-side reference. It must never store the bearer token or its reusable plaintext equivalent. Token rotation invalidates every stale intent from an earlier generation even if the Invitation identifier itself is unchanged.

After authentication and verified-email confirmation, the server must revalidate that the Invitation:

- still exists;
- has not expired;
- has not been revoked, rotated, or consumed;
- remains bound to the authenticated account's normalized verified email.

The application then shows only the approved safe preview, requires explicit acceptance, and creates the Membership while consuming the Invitation atomically.

### Browser and device continuity

- The same browser/session can continue after verification without reopening the original link.
- Verification on another device verifies the account globally but does not transfer pending Invitation intent to that device.
- The user may return to the originating browser or obtain and open a newly issued current invitation link in the other session. An already exchanged single-use verifier cannot be reused for cross-device continuation.
- Do not create global per-user pending-invitation state solely for cross-device continuation in MVP.

### Email identity and invitation lifecycle

- Normalize email using the selected Django/django-allauth identity stack.
- Do not apply provider-specific transformations such as Gmail dot removal or plus-address stripping.
- Require account authentication and verified email before acceptance.
- Allow one pending Invitation per Household and normalized email.
- Revoke by Invitation identifier, not bearer token.
- Derive expiration from `expires_at`.
- Keep the Household join code as a distinct bearer mechanism.

The approved MVP Invitation lifetime is 30 days. Changing it requires an explicit security/product decision rather than a silent configuration change.

### Household join-code separation

The join code is an 8-character uppercase alphanumeric code. Only the owner may read or regenerate it. Generic Household and dashboard responses omit it. Join attempts are rate-limited and return a uniform invalid-code response; regeneration immediately invalidates the previous code.

## Consequences

### Positive

- The invitation bearer secret avoids common server and analytics URL surfaces.
- The token is discarded early, limiting exposure after exchange.
- Same-browser signup and verification can complete without reopening the link.
- Generation binding makes resend rotation effective against already exchanged stale intents.
- Email binding prevents a forwarded invitation from being accepted by a different verified identity.

### Costs and risks

- Frontend bootstrap code must process and remove the fragment before any untrusted script can inspect it.
- Session rotation must deliberately preserve the non-secret intent while continuing to rotate authentication state.
- The backend must revalidate eligibility at final acceptance; exchange success cannot reserve membership indefinitely.
- Cross-device continuation is intentionally limited in MVP.
- Security tests must cover leakage surfaces, replay, resend rotation, revocation, expiry, email mismatch, races, and atomic consumption.

## Related decisions

- [Security model](../../security/security-model.md)
- [Domain model](../domain-model.md)
- [ADR-011: Identity and session security](ADR-011-identity-and-session-security.md)
- [OpenAPI](../../api/openapi.yaml)
