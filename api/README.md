# API contract conventions

> **Status:** Accepted  
> **Owner:** Documentation, with Backend and Frontend review for breaking changes  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Human API conventions

[`openapi.yaml`](./openapi.yaml) is the sole machine-readable route and schema source of truth for the HouseHoldHub MVP. The former Markdown contract is retained as a [historical archive snapshot](../archive/2026-08-16-design-and-planning/OPENAPI.md); implementations, generated clients, mocks, and contract tests must use this YAML file.

Change the contract before changing Backend or Frontend behavior. Generated artifacts must identify the exact contract revision they were built from, and CI should fail when checked-in generated artifacts drift from that revision. This README explains conventions only; it intentionally does not duplicate the route inventory.

## Authentication and CSRF

The API uses same-origin, database-backed Django sessions selected by an opaque HttpOnly cookie. The inherited MVP session lifetime is 14 days, subject to earlier rotation, logout, identity-security revocation, account disablement, and expiry. The OpenAPI root requires `sessionAuth`; genuinely public operations explicitly override it with `security: []`.

Public does not mean CSRF-exempt. Every unsafe browser request uses the same-origin CSRF bootstrap contract and sends `X-CSRFToken`, including signup, login, password reset, email verification, and invitation exchange. OAuth uses mandatory state validation. Session identifiers rotate at authentication and sensitive identity transitions, and server-side revocation is effective on the next request.

Email verification is mandatory before household access. Google login never auto-links to an existing account based only on matching email; linking is an explicit authenticated flow. Password reset and identity-link changes apply the revocation behavior documented by the affected operation.

Cookie `SameSite` configuration must remain compatible with the chosen OAuth-state persistence design. If OAuth state is retained in the pre-auth Django session, the external top-level callback must receive that session cookie; stale legacy `SameSite=Strict` examples are not contract authority.

## Secret-bearing links and invitations

One-time verification, password-reset, and invitation bearers are placed in the frontend URI fragment, never in an API path or query. The frontend reads a fragment bearer once, immediately removes it from browser history, never persists or logs it, and submits it in the documented POST body.

Invitation exchange stores only a non-secret invitation ID and verifier generation in the server-side browser session. It does not accept the invitation or return a preview. Preview and acceptance require an authenticated, verified, normalized-email match and revalidate all invitation, household, membership, and generation state. Acceptance is atomic. Revocation, verifier rotation, or reissue invalidates stale intents; pending intent is not transferred across devices or stored globally on the user.

## Errors, authorization, and concurrency

All error bodies use `ErrorResponse`.

- `400` covers malformed input and request/domain validation.
- `401` means a valid authenticated session is required.
- `404` covers both nonexistent resources and resources outside the caller's household scope.
- `403` is reserved for an addressable resource the caller may see but may not act on.
- `409` covers duplicates and invalid lifecycle-state transitions.
- `422` is never used.

Writes use last-write-wins. The MVP has no entity version, conditional-write precondition, merge flow, or concurrency-conflict `409`.

Authorization is always checked against active household membership at request time. Removing a member denies further household access on the next request. Current task assignment becomes null when its assignee is removed; the MVP exposes no former-assignee or assignment-history field.

## Schema shapes and nullability

Create, update, summary, and full response schemas are deliberately separate. Response schemas mark their stable fields as required even when a value may be `null`; request schemas distinguish an omitted property from an explicit nullable value. Update schemas reject empty and unknown-property payloads.

Attribution fields may be null after an account lifecycle action, but household content remains. Field-level restrictions in schema and operation descriptions are part of the contract, not merely UI guidance.

## Money and calendar dates

A household has one required, immutable MVP `currency_code`. The backend validates supported ISO 4217 minor-unit semantics. An expense accepts a positive `amount_minor`, snapshots the household currency code server-side, and cannot independently set or later change currency. Aggregates combine only that household currency; no FX conversion exists. The exact ISO metadata package/version is an implementation dependency, not an additional wire field.

`incurred_on`, task `due_date`, and dashboard `as_of` are calendar dates, not timestamps. Expense creation requires the client to send `incurred_on`; the official frontend defaults it from the browser-local date. Dashboard requests likewise send browser-local `as_of`; the backend does not replace it with a server UTC date or persist timezone state. Dashboard due-task selection and deterministic ordering are defined in the machine contract.
