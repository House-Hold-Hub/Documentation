# HouseHoldHub Testing Strategy

> **Status:** Accepted  
> **Owner:** Backend, Frontend, Automation, and Infrastructure repositories  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** MVP test philosophy, traceability, and required scenario coverage  
> **Supersedes:** Test-count and coverage-percentage gates in archived planning snapshots

## Purpose

Testing is risk- and behavior-based. The goal is evidence that approved product journeys, authorization boundaries, API contracts, lifecycle rules, and operational controls work together. The strategy does not use an arbitrary number of tests or an unsupported merge-blocking coverage percentage as a proxy for confidence.

Exact commands, runners, compatible package versions, and repository-local checks are owned by implementation manifests and workflow configuration. The approved frontend unit/component stack is Vitest with React Testing Library; CI/CD runs on GitHub Actions.

## Sources for test traceability

Every material test scenario traces to one or more of:

- an umbrella or feature requirement in [`product/prds/`](../product/prds/README.md);
- an authorization rule in [`product/permissions-matrix.md`](../product/permissions-matrix.md);
- a conceptual invariant in [`architecture/domain-model.md`](../architecture/domain-model.md);
- an accepted decision in the [ADR index](../architecture/adr/README.md);
- an operation, schema, or error in [`api/openapi.yaml`](../api/openapi.yaml);
- a security control in [`security/security-model.md`](../security/security-model.md);
- a release journey in [`release-acceptance.md`](release-acceptance.md).

Requirements and scenarios should be identifiable in test names or test metadata without duplicating full requirement text in the test suite.

## Test layers

### Domain and service tests

Exercise validation, state transitions, lifecycle, and authorization at the central write/query boundaries. High-risk invariants include owner/owner-Membership consistency, same-household assignment, invitation generation binding, email verification, session revocation, household soft deletion, immutable expense payer/currency, and positive quantity/amount rules.

### API contract tests

Validate implemented operations against the machine-readable OpenAPI contract, including:

- request and response requiredness and nullability;
- authentication and CSRF expectations;
- 400/401/403/404/409 behavior;
- absence of 422 and concurrency-specific 409 behavior;
- stable Create, Update, Summary, and Response shapes;
- public-operation `security: []` overrides;
- household scoping and non-disclosure.

OpenAPI syntax and contract linting run in CI. Backend and Frontend generation/compatibility checks are added when their manifests define those workflows.

### Frontend component and integration tests

Use Vitest and React Testing Library for user-observable states and interactions. Cover loading, empty, success, validation, authorization-loss, and recoverable-error behavior. Tests should query accessible roles/names and avoid coupling to internal component structure.

TanStack Query synchronization is verified through mutation response handling, targeted invalidation/refetch, and 403/404 cleanup. WebSocket or SSE behavior is not tested because it is not part of the MVP.

Responsive verification covers the approved 375 CSS-pixel mobile target and 1280 CSS-pixel-and-above desktop target. Desktop is the MVP design priority, but core mobile workflows must remain usable.

### End-to-end journey tests

Automate the critical journeys in [release acceptance](release-acceptance.md) at the highest practical fidelity. End-to-end tests focus on cross-repository contracts and high-value user outcomes rather than reproducing every lower-layer assertion.

### Operational verification

Infrastructure and Automation provide smoke, migration, rollback, backup/restore, scheduled-cleanup, secret-scanning, dependency-security, logging-redaction, health/readiness, and error-tracking checks. The exact production provider and numeric alert/recovery thresholds remain bounded decisions D02 and D04.

## Mandatory authorization and isolation coverage

Authorization and household isolation require complete scenario coverage, not statistical sampling.

For every household-scoped operation, cover as applicable:

1. unauthenticated caller;
2. unverified authenticated account;
3. active household member with permitted action;
4. active member without owner/creator/assignee authority;
5. household owner;
6. removed or revoked member on the next request;
7. user from another household using a valid foreign identifier;
8. nonexistent object;
9. soft-deleted household;
10. conflicting terminal or duplicate state.

Expected semantics are 401 unauthenticated, 404 nonexistent or outside scope, 403 known in-household action denied, 400 request/domain validation, and 409 duplicate or incompatible state. A 409 must not be used for optimistic concurrency in the MVP.

## Required security scenario families

- Signup verification gates normal access and handles resend failure safely.
- Password reset is enumeration-safe in body, status, and observable timing behavior.
- OAuth state validation rejects forged/missing state.
- Existing-email OAuth collision cannot auto-link; explicit linking requires recent reauthentication.
- Login and privilege changes rotate the current session as specified.
- Sessions expire after the approved 14-day lifetime and remain revocable earlier.
- Logout, reset, password/email/provider changes, disable, and restoration enforce the session-revocation matrix.
- CSRF is required for every unsafe browser operation, including public operations with `security: []`.
- Invitation fragments never reach request URLs, referrers, storage, logs, analytics, or error context.
- Invitation exchange is one-use, rate-limited, email-bound, and retains only a non-secret generation-bound intent.
- Resend/rotation invalidates prior verifiers and exchanged stale intents.
- Invitation acceptance rechecks state and email identity atomically and rejects replay.
- Join-code failures are uniform and rate-limited; regeneration immediately invalidates the prior code.
- Active household join codes remain globally unique, including collision-safe creation and regeneration behavior.
- Logs and delivery records redact all approved secret and sensitive fields.
- Representative injection payloads cannot alter backend queries or commands, and user-controlled text/error content cannot execute as browser markup or script.

## Domain-specific minimum coverage

### Household and membership

- Household creation atomically creates the authoritative owner relationship and matching owner Membership.
- Owner Membership cannot be removed.
- Disable retains ownership integrity while denying access; prohibited anonymization/hard deletion is rejected.
- Soft delete immediately denies normal access but preserves children for the 30-day window.
- Support recovery and scheduled purge are idempotent.

### Tasks

- Every row in the approved task permission matrix is covered, including unassigned completion and reopen using the same rule as completion.
- Assignment to a Membership from another household is rejected at the central write boundary.
- Removed assignee becomes unassigned without exposing assignment history.
- Last-write-wins accepts sequentially received valid updates and does not emit a concurrency 409.

### Shopping and inventory

- Any-member mutations and creator/owner deletion rules match the permissions matrix.
- Shopping bulk clear requires the approved confirmation flow and clears only purchased items.
- Inventory quantity is a positive integer; decrement below one is rejected rather than treated as delete.
- Inventory category grouping does not alter location metadata or authorization.

### Expenses

- Payer defaults to creator, must be an active member at creation, cannot be changed, and becomes null if the User is deleted.
- `incurred_on` is required and validated; the Backend never substitutes a server-UTC date.
- `amount_minor` is a strictly positive integer.
- Supported ISO currencies with zero-, two-, and three-digit minor-unit exponents are interpreted without assuming cents.
- Expense currency is copied from the immutable Household currency and cannot be mass-assigned or changed.
- Totals and category totals sum only same-currency `amount_minor` values and return their currency context; no conversion occurs.

### Dashboard

- `as_of` is required and validated as a real calendar date.
- Overdue, today, and the inclusive next-seven-day boundary behave deterministically, including leap-day cases.
- Undated tasks are absent from the preview but included in the complete pending count.
- Preview ordering follows due date, creation timestamp, and stable identifier; results are capped at three.
- Query/cache identity includes household and `as_of`.

## Coverage reporting

Coverage is reported to reveal untested code and trends. It is not a merge gate until the team has an executable baseline and approves a justified threshold. Branch or line percentages do not replace mandatory authorization, isolation, state, and error scenarios.

## Performance testing

Current numeric latency, throughput, bundle-size, dataset-size, and concurrency figures in historical plans are hypotheses, not acceptance gates. Before adopting a target, define:

- percentile;
- endpoint or journey set;
- representative dataset;
- environment and dependency topology;
- concurrency profile;
- measurement duration.

Performance-only indexes require representative queries/data and query-plan evidence. Qualitative regression checks and basic smoke/load observations may begin earlier.

## Test data and providers

Tests use isolated households and explicit cross-household fixtures. Automation supplies fake transactional-email/provider support so verification, reset, and invitation behavior can be exercised without logging or retaining plaintext credentials. Tests must not use real personal data before decision gate D03 is resolved.

## Deferred quality inputs

- **D01:** Exact auth constants before M1/M8.
- **D02:** Exact email/deployment/monitoring providers before their integration and launch gates.
- **D03:** Privacy and retention policy before real personal data.
- **D04:** Numeric recovery, availability, and alert thresholds before M9 launch sign-off.
- **D06:** Exact package/tool versions at scaffolding; performance indexes after evidence.
