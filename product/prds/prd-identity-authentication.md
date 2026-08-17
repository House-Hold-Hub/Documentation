# PRD: Identity and authentication

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP account identity, email verification, authentication, Google linking, password recovery, and user-visible session lifecycle
> Supersedes: identity and authentication requirements in the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md)

## 1. Overview

HouseHoldHub requires an authenticated, verified identity before a person receives normal application access. The MVP supports email/password and Google authentication while preventing ambiguous duplicate accounts, unsafe automatic provider linking, and stale authenticated sessions.

This PRD defines product behavior. Identity representation and session mechanisms are defined by the domain model and ADRs; request and response details are defined only in OpenAPI.

## 2. Goals

- Let a person create and verify an email/password account.
- Let a person authenticate with email/password or a trusted Google identity.
- Provide recoverable, enumeration-safe password reset and email-verification flows.
- Make provider linking an explicit, recently reauthenticated action when an account already exists.
- Revoke sessions after security-sensitive account changes.
- Support invitation continuation through normal authentication and verification in the same browser.

## 3. User stories

### IA-US-001: Register and verify an account

**Description:** As a new user, I want to prove control of my email address so that I can safely access HouseHoldHub.

**Acceptance criteria:**

- Email/password signup creates one account for the normalized unique email address.
- Before verification, the user can access only verification status, resend, safe pending-email correction where supported, and cancel/logout behavior.
- Normal household and feature access is denied until the email is verified.
- Verification state uses the identity stack's canonical verified-email record rather than a separate application flag.

### IA-US-002: Authenticate with email and password

**Description:** As a verified user, I want to log in and log out so that I control access to my account.

**Acceptance criteria:**

- Valid credentials establish a HouseHoldHub session; invalid credentials do not.
- Normal logout revokes the current HouseHoldHub session.
- Logout does not attempt to terminate the user's Google session.
- Protected application access without a valid session is denied.

### IA-US-003: Use Google authentication safely

**Description:** As a user, I want to use a Google identity without accidentally merging or duplicating an existing account.

**Acceptance criteria:**

- A Google identity whose normalized email does not match an existing local account may proceed through normal social signup.
- A matching email never causes automatic linking or creation of an ambiguous duplicate account.
- Linking to an existing account requires authentication to that account, recent reauthentication, and explicit confirmation.
- A trusted provider's verified-email claim satisfies verification only after issuer, audience, and provider trust validation.

### IA-US-004: Recover a forgotten password

**Description:** As an email/password user, I want to reset a forgotten password without revealing whether another person's account exists.

**Acceptance criteria:**

- A reset request gives an enumeration-safe result regardless of account existence or delivery outcome.
- A reset credential is time-limited, single-use, and never retained in plaintext.
- A successful reset revokes all HouseHoldHub sessions and requires fresh authentication.
- Delivery failure leaves a recoverable state with a rate-limited retry path where a matching account exists.

### IA-US-005: Protect sessions after sensitive changes

**Description:** As a user, I want old sessions revoked after a security-sensitive account change so that prior access cannot continue silently.

**Acceptance criteria:**

- An authenticated password change preserves or rotates the current session and revokes all others.
- A primary-email change requires recent reauthentication, rotates the current session, and revokes all others.
- Google link or unlink requires recent reauthentication, rotates the current session, and revokes all others.
- Account disable or soft deletion immediately revokes all sessions.
- Account restoration never restores old sessions and requires fresh authentication.

## 4. Functional requirements

- **IA-FR-001:** Accounts must use a unique normalized email address and a UUID identity. A display name must be available for household member presentation.
- **IA-FR-002:** Email/password signup must use Django authentication and django-allauth-compatible identity records; the product must not maintain a bespoke password field or provider-specific `google_id` field.
- **IA-FR-003:** Email/password accounts must verify email ownership before normal application access.
- **IA-FR-004:** The pre-verification product surface must be limited to the minimum verification lifecycle: verification status, resend, safe pending-email correction where supported, and cancel/logout.
- **IA-FR-005:** Verified-email state must come from django-allauth's verified-email representation or its supported equivalent, not a duplicate application boolean.
- **IA-FR-006:** Google is the only social authentication provider in MVP.
- **IA-FR-007:** A trusted Google verified-email claim may satisfy verification only after correct issuer, audience, and provider-trust validation.
- **IA-FR-008:** Provider-email collision with an existing local account must require authenticated, recently reauthenticated, explicit linking; automatic linking and ambiguous duplicate creation are forbidden.
- **IA-FR-009:** Provider identity relationships must use django-allauth `SocialAccount` or its supported equivalent. Google access and refresh tokens must not be persisted unless a future approved feature requires Google API access.
- **IA-FR-010:** Users must be able to request and complete password reset through a time-limited, single-use recovery flow.
- **IA-FR-011:** Password-reset requests must remain enumeration-safe in response content and observable behavior regardless of account existence or provider outcome.
- **IA-FR-012:** Authentication must use revocable HouseHoldHub sessions with a 14-day server-side lifetime. Normal logout revokes the current session only, and every approved revocation event may end a session sooner.
- **IA-FR-013:** An indexed user-session registry compatible with Django and django-allauth must support the approved revocation behavior without adding device-management UI or continuous activity tracking.
- **IA-FR-014:** Password reset revokes every session. Authenticated password change rotates or preserves the current session and revokes all others.
- **IA-FR-015:** Primary-email change and Google link/unlink require recent reauthentication, rotate the current session, and revoke all other sessions.
- **IA-FR-016:** Account disable or soft deletion revokes all sessions immediately. Restoration requires fresh authentication and never revives an old session.
- **IA-FR-017:** Django's built-in authentication-hash and session-security behavior must be preserved where applicable.
- **IA-FR-018:** Account and authentication state must be able to carry the non-secret, session-bound invitation intent defined by the [household and invitation PRD](prd-household-membership-invitations.md) through same-browser signup, login, verification, and session rotation.
- **IA-FR-019:** Transactional verification and reset delivery must use recoverable pending state and the ownership/failure behavior defined by the security and operational baseline.

Exact password-policy, reset-token, and rate-limit constants remain bounded decision `D01`; see the [roadmap](../roadmap.md).

## 5. Account lifecycle boundary

MVP account disablement denies authentication and revokes sessions while retaining the user record needed for domain integrity. Self-service account deletion is not provided. Administrative anonymization or hard deletion of a household owner is forbidden while that user owns an active household; owned households must first be resolved through household deletion or a future approved administrative transfer mechanism. Jurisdiction, retention, and anonymization behavior remain bounded decision `D03`.

## 6. Authorization and security boundaries

- Normal application access requires a valid session and verified identity.
- Household action permissions are canonical in the [permissions matrix](../permissions-matrix.md).
- Cookie, CSRF, OAuth `state`, token-transport, logging, and secret-handling requirements are canonical in the [security model](../../security/security-model.md).
- Routes, field names, response requiredness/nullability, and wire errors are canonical only in [OpenAPI](../../api/openapi.yaml).

## 7. Non-goals

- Additional social providers.
- Automatic provider linking based only on matching email.
- Provider-specific email rewriting such as Gmail dot removal or plus-address stripping.
- Google API access or retention of Google access/refresh tokens.
- Device-management UI, user-visible session inventory, or continuous session-activity tracking.
- JWT authentication for the MVP web application.
- Self-service account deletion or public household ownership transfer.

## 8. Success and verification

- Signup, verification, login, logout, reset, Google signup, explicit linking, and revocation journeys meet their acceptance criteria.
- Negative tests cover unverified access, invalid sessions, unsafe provider collisions, and every approved revocation trigger.
- Verification and reset failures are recoverable without account enumeration.
- Release verification follows the [testing strategy](../../quality/testing-strategy.md) and [release acceptance](../../quality/release-acceptance.md); no arbitrary test-count or coverage threshold applies.

## 9. Legacy traceability

| Legacy ID | Canonical requirement |
|---|---|
| `FR-1`, `FR-3` | `IA-FR-001`–`IA-FR-005` |
| `FR-2` | `IA-FR-006`–`IA-FR-009` |
| `FR-4` | `IA-FR-002`; exact policy constants deferred under `D01` |
| `FR-5` | `IA-FR-010`–`IA-FR-011`, `IA-FR-019` |
| `FR-6` | `IA-FR-012`–`IA-FR-017` |
| `FR-7` | `IA-FR-018` and the invitation PRD |
| Legacy account-deletion text | Account lifecycle boundary above; legal/privacy details remain `D03` |

## 10. Open questions

No unresolved semantic blocker. `D01` and `D03` remain deliberately deferred to their roadmap deadlines.
