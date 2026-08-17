# HouseHoldHub MVP Release Acceptance

> **Status:** Accepted  
> **Owner:** Product and the five HouseHoldHub repositories  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** MVP release journeys and launch evidence  
> **Supersedes:** Release gates and unsupported numeric thresholds in archived implementation plans

## Release rule

The MVP is releasable when every applicable journey below succeeds in a production-like environment, mandatory authorization/isolation scenarios pass, the API contract is validated, and the minimum operational controls are demonstrated. Live GitHub issues own execution status; this document does not own issue count or schedule.

No arbitrary test count, coverage percentage, response-time threshold, or calendar-duration estimate is a release gate. Intentionally deferred launch decisions must be resolved by their stated deadline.

## Journey 1: Email signup and household creation

1. A visitor signs up with email and password.
2. The unverified account receives only the verification lifecycle.
3. Verification succeeds without exposing the bearer in a server-visible URL or log.
4. The verified user creates a household with a required ISO 4217 currency.
5. The server atomically creates matching owner and owner-Membership state.
6. The user reaches the minimal household dashboard using an explicit browser-local `as_of` date.

Evidence includes verification gating/resend recovery, CSRF, session rotation, owner invariants, and no unnecessary repeated authentication or data entry. Product interaction measurement excludes provider and user waiting time and has no unapproved numeric target.

## Journey 2: Email invitation and member join

1. The owner invites a normalized recipient email.
2. Delivery state is recoverable if provider submission fails; resend rotates the verifier.
3. The email link carries the verifier only in the URI fragment.
4. The landing page strips and exchanges it without URL, storage, telemetry, or log exposure.
5. The server retains only a non-secret generation-bound intent through same-browser signup/login/verification rotation.
6. The authenticated verified recipient sees a safe preview only after email match.
7. Explicit acceptance atomically creates Membership and consumes the invitation.
8. Replay, old generation, revoked, expired, duplicate, wrong-email, and cross-household attempts fail with canonical status/privacy behavior.

## Journey 3: Household join code

1. The owner reads the globally unique eight-character uppercase alphanumeric code through an owner-only view.
2. An authenticated verified nonmember submits the code in a request body.
3. A valid code creates one Membership; invalid attempts have a uniform response and are rate-limited.
4. Regeneration immediately invalidates the old code and generic household/dashboard responses never expose either code.
5. Creation and regeneration handle code collisions without allowing two active households to share a code.

## Journey 4: Task management

1. An active member creates a task with optional due date and optional single Membership assignee.
2. Ordinary editing, assignment, deletion, completion, and reopen follow every row of the permissions matrix.
3. Any member can complete/reopen an unassigned task; the assignee or owner can complete/reopen an assigned task.
4. Cross-household assignment and access fail without disclosure.
5. Removing an assigned member clears the assignee and does not expose former-assignee history.
6. Valid concurrent updates use last-write-wins and do not produce an optimistic-concurrency 409.

## Journey 5: Shopping list

1. Any active member adds, edits, and toggles a shopping item.
2. A permitted creator/owner deletes an individual item.
3. Any active member invokes clear-purchased only after the UI confirmation and only purchased items are removed.
4. Another household cannot observe or mutate the list.
5. The dashboard shopping summary refreshes through the approved API/cache-invalidation model.

## Journey 6: Expense tracking

1. The official frontend initializes and submits browser-local `incurred_on` explicitly.
2. A member creates an expense with positive integer `amount_minor`, an approved category, description as supported, and payer defaulting to the creator.
3. The Backend copies the immutable Household ISO currency to the Expense; no per-expense currency choice or conversion is presented.
4. The payer is an active member at creation and cannot be changed later.
5. Filtering and ordering use `incurred_on`.
6. Total and per-category aggregates return same-currency minor-unit sums with explicit currency context.
7. Permitted edit/delete and cross-household denial follow the permissions matrix.

## Journey 7: Inventory management

1. Any active member creates and edits an inventory item with a positive integer quantity.
2. Category grouping is available; location remains display metadata.
3. Decrement below one is rejected rather than interpreted as deletion.
4. Creator/owner deletion and cross-household isolation follow the permissions matrix.

## Journey 8: Dashboard and household switching

1. The user selects a household and requests its dashboard with `as_of=YYYY-MM-DD` derived from the browser-local date.
2. Household identity, member list/summary, complete pending-task count, at most three due-soon tasks, shopping pending count, and approved quick actions render.
3. Due-soon includes incomplete overdue, due-today, and due-through-`as_of + 7` tasks; undated tasks are excluded from the preview.
4. Ordering is deterministic by overdue/due date, creation timestamp, and stable identifier.
5. Expense widgets are absent.
6. Switching households changes every displayed aggregate and cache key without leaking the prior household.

## Journey 9: Member removal and immediate denial

1. An owner removes a non-owner member.
2. The next server request from that member is denied, regardless of client cache.
3. The former member cannot list, read, or mutate household resources.
4. Assignment cleanup and attribution behavior follow the domain model.
5. Invitation/member-change audit events contain no secrets.

## Journey 10: Authorization isolation

For each household-scoped resource, authenticated users outside the household receive 404 for object identifiers. Members receive 403 only for a known in-household action their role/relationship cannot perform. Unauthenticated requests receive 401. Validation is 400, and duplicate/incompatible state is 409. The MVP returns no 422 and no concurrency-specific 409.

## Journey 11: OAuth collision and account linking

1. Google login validates issuer, audience, verified-email claim, and mandatory state.
2. A new noncolliding identity may complete social signup.
3. A collision with an existing account does not auto-link or create an ambiguous duplicate.
4. The authenticated existing user recently reauthenticates and explicitly links/unlinks the provider identity.
5. The current session rotates, all other sessions are revoked, and no Google access/refresh token is retained.

## Journey 12: Account and session lifecycle

Verify the complete session matrix: logout current; password reset all; authenticated password change/current rotation plus other-session revocation; primary-email and OAuth changes with recent reauthentication/current rotation/other revocation; account disable all; restoration only through fresh authentication. An owner may be disabled while ownership records remain; anonymization/hard deletion is blocked until every active owned household is administratively resolved.

## Journey 13: Household deletion, recovery, and purge

1. The owner soft-deletes the household.
2. Normal access stops immediately while memberships and resources remain preserved.
3. Support/admin recovery during the 30-day window restores access idempotently.
4. The externally scheduled purge hard-deletes eligible households and children after 30 days and is safe to retry.
5. Delete, recovery, and purge produce critical audit events without sensitive payloads.

## Contract and quality evidence

- Standalone OpenAPI is syntactically valid and contract checks pass.
- Backend and Frontend agree on requiredness, nullability, status behavior, security, and versioned routes.
- Risk traceability covers every feature requirement and every row of the authorization/isolation matrices.
- Coverage is reported, but no unsupported percentage blocks release.
- The official UI remains usable at the approved mobile target of 375 CSS pixels and desktop target of 1280 CSS pixels and above; desktop remains the MVP design priority without making mobile workflows unusable.
- Household roles, available actions, and denied actions are understandable from the UI without requiring users to infer hidden permission rules.
- Active documentation contains no competing route inventory or stale canonical stack/model claim.
- Server-side input handling resists injection, and browser rendering of user-controlled text and errors resists cross-site scripting.
- Accessibility verification covers WCAG 2.1 AA outcomes, keyboard use, focus management, semantic labels, and non-color-only communication.

## Minimum operational evidence

Before launch, demonstrate:

- health/readiness checks;
- structured redacted logs with request correlation;
- basic error tracking;
- managed secrets and production configuration;
- automated migrations;
- tested backup and restore;
- documented and exercised rollback;
- scheduled household purge and Django session cleanup;
- critical invitation, member, and household-deletion audit events;
- smoke and dependency-security checks;
- minimal incident, recovery, and operational procedures.

No placeholder runbooks are accepted. Operational documents are created when they can describe the selected runtime and executable procedures.

## Decision gates before release

- **D01:** Safe authentication constants before M1; review/lock by M8 hardening.
- **D02:** Managed email provider before M1 integration; deployment, secret-store, and monitoring providers before M9.
- **D03:** Jurisdiction and retention before real personal data is processed.
- **D04:** Numeric RTO/RPO and alert/severity thresholds after D02/D03 and before M9 sign-off.
- **D05:** Any calendar commitment only after staffing, capacity, start date, and re-sizing.
- **D06:** Exact packages/tools at scaffolding; performance-only indexes after representative evidence.
