# HouseHoldHub MVP GitHub Issue Import Draft

> **Status:** Draft  
> **Owner:** Five HouseHoldHub repositories  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Nothing; candidate work decomposition only  
> **Supersedes:** The [archived revised GitHub-issue proposal](../archive/2026-08-16-design-and-planning/GITHUB_ISSUES_PROPOSAL_REVISED.md) as an active planning artifact

## Warning

This file is not execution truth. Live GitHub issues and milestones own issue count, assignment, status, estimates, dependencies, and completion. Nothing here has been created in GitHub yet.

The detailed source proposal is preserved as a dated historical snapshot in the [design-and-planning archive](../archive/2026-08-16-design-and-planning/). It contains superseded technology, model, API, permission, count, and quality claims and must not be imported verbatim.

Before issue creation, each candidate below must be reconciled against:

- the responsible [feature PRD](../product/prds/README.md);
- the [permissions matrix](../product/permissions-matrix.md);
- accepted [ADRs](../architecture/adr/README.md) and the [domain model](../architecture/domain-model.md);
- the current [`api/openapi.yaml`](../api/openapi.yaml);
- the [testing strategy](../quality/testing-strategy.md) and [release acceptance](../quality/release-acceptance.md).

## Import rules

1. Create issues only after repository manifests and contract paths exist.
2. Do not copy historical issue counts, week estimates, test-count quotas, coverage gates, performance thresholds, or route/schema text.
3. Link the canonical requirement/operation rather than duplicating it.
4. Keep service-repository workflows local; link reusable Automation assets where appropriate.
5. Add explicit dependency links for cross-repository contract changes.
6. Split or merge candidates based on implementation evidence; candidate identifiers are not permanent issue numbers.

## M0 candidate set — engineering foundation

### Backend

- `M0-B1` — Scaffold Python/Django/DRF project with approved runtime baseline.
- `M0-B2` — Establish custom UUID User and initial domain migration skeleton.
- `M0-B3` — Configure versioned REST/OpenAPI integration and repository checks.
- `M0-B4` — Add Backend service Dockerfile and local runtime configuration.
- `M0-B5` — Add repository-local GitHub Actions workflow using shared Automation assets where applicable.

### Frontend

- `M0-F1` — Scaffold React/TypeScript/Vite/npm application with native CSS Modules and design tokens.
- `M0-F2` — Establish session/CSRF-aware API client and safe error/redaction behavior.
- `M0-F3` — Generate TypeScript contract artifacts from Documentation-owned OpenAPI.
- `M0-F4` — Add Vitest/React Testing Library and repository-local GitHub Actions workflow.

### Infrastructure

- `M0-I1` — Define local PostgreSQL/full-stack runtime boundary.
- `M0-I2` — Define environment/secret configuration contract without choosing deferred production vendors.

### Automation

- `M0-A1` — Provide reusable build/pipeline assets.
- `M0-A2` — Provide shared test/contract/security gates.
- `M0-A3` — Provide local setup automation where it can consume real repository manifests.

### Documentation

- `M0-D1` — Publish and validate documentation architecture and OpenAPI contract.
- `M0-D2` — Maintain contribution, contract-review, and cross-repository governance.

## M1 candidate set — identity and authentication

### Backend

- `M1-B1` — Implement custom UUID User, allauth email identities, and verification gating.
- `M1-B2` — Implement database sessions, indexed user-session registry, rotation, and revocation matrix.
- `M1-B3` — Implement email/password signup, verification/resend, login/logout, reset/change, and CSRF contract.
- `M1-B4` — Implement Google OAuth trust validation and explicit collision-safe linking/unlinking.
- `M1-B5` — Implement provider-neutral transactional email, durable delivery state, and safe recovery.

### Frontend

- `M1-F1` — Implement authentication/session state and protected navigation.
- `M1-F2` — Implement signup, verification, login, reset, and recoverable delivery UX.
- `M1-F3` — Implement Google login and explicit reauthenticated linking flows.
- `M1-F4` — Add identity security, accessibility, and contract tests.

## M2 candidate set — household, membership, and invitations

### Backend

- `M2-B1` — Implement Household, immutable currency, join code, and soft-delete lifecycle.
- `M2-B2` — Implement Membership and owner invariants.
- `M2-B3` — Implement household/member operations from OpenAPI.
- `M2-B4` — Implement invitation lifecycle, delivery, fragment exchange, generation-bound intent, preview, acceptance, resend, and revoke.
- `M2-B5` — Implement owner-only join-code read/regenerate and rate-limited join.
- `M2-B6` — Complete household authorization and negative isolation tests.

### Frontend

- `M2-F1` — Implement household selector/switcher.
- `M2-F2` — Implement household creation with currency.
- `M2-F3` — Implement member and invitation management.
- `M2-F4` — Implement secure invitation fragment handoff and verified acceptance.
- `M2-F5` — Implement join-by-code flow.
- `M2-F6` — Add household/membership/invitation UI and security tests.

## M3 candidate set — task management

### Backend

- `M3-B1` — Implement Task and same-household Membership assignment validation.
- `M3-B2` — Implement task operations and last-write-wins behavior from OpenAPI.
- `M3-B3` — Complete task permission and isolation matrix tests.

### Frontend

- `M3-F1` — Implement task list/forms/assignment/completion/reopen/delete UX.
- `M3-F2` — Add task UI, accessibility, permission-loss, and contract tests.

## M4 candidate set — shopping list

### Backend

- `M4-B1` — Implement ShoppingItem.
- `M4-B2` — Implement shopping operations including clear-purchased.
- `M4-B3` — Complete shopping permission/isolation tests.

### Frontend

- `M4-F1` — Implement pending/purchased shopping UI and confirmed bulk clear.
- `M4-F2` — Add shopping UI and synchronization tests.

## M5 candidate set — expense tracking

### Backend

- `M5-B1` — Implement Expense with `amount_minor`, immutable currency/payer, category, and `incurred_on`.
- `M5-B2` — Implement expense operations, filters, and same-currency aggregates.
- `M5-B3` — Complete expense money/date/permission/isolation tests.

### Frontend

- `M5-F1` — Implement browser-local expense date, forms, filters, and same-currency totals.
- `M5-F2` — Add expense UI, exponent-formatting, and contract tests.

## M6 candidate set — inventory management

### Backend

- `M6-B1` — Implement InventoryItem and positive-quantity invariant.
- `M6-B2` — Implement inventory operations and category grouping support.
- `M6-B3` — Complete inventory permission/isolation tests.

### Frontend

- `M6-F1` — Implement inventory grouped display and CRUD UX.
- `M6-F2` — Add quantity, permission, and UI tests.

## M7 candidate set — minimal dashboard

### Backend

- `M7-B1` — Implement dashboard aggregation with required `as_of`, complete pending count, deterministic three-task preview, and shopping summary.

### Frontend

- `M7-F1` — Implement minimal dashboard and browser-local `as_of` query identity.

## M8 candidate set — integration and hardening

### Backend

- `M8-B1` — Automate cross-feature release journeys.
- `M8-B2` — Complete authentication, authorization, isolation, CSRF, token, session, redaction, and abuse hardening.
- `M8-B3` — Establish representative performance/query baseline and evidence-based indexing.

### Frontend

- `M8-F1` — Automate critical browser journeys and accessibility checks.
- `M8-F2` — Address measured frontend regressions without unsupported numeric gates.

### Documentation

- `M8-D1` — Reconcile shipped behavior, contract, guides, and release evidence.

## M9 candidate set — deployment readiness

### Infrastructure

- `M9-I1` — Provision selected production runtime, secrets, database, migrations, backup/restore, and rollback.
- `M9-I2` — Configure selected monitoring/error provider, redacted logging, health/readiness, and scheduled maintenance.

### Automation

- `M9-A1` — Automate pre-launch contract, smoke, security, migration, restore, rollback, and release checks.

## Decision gates before import

- D01 and the email portion of D02 block final M1 issue acceptance criteria.
- D03 blocks use of real personal data.
- Deployment/monitoring portions of D02 and D04 block final M9 acceptance criteria.
- D05 blocks calendar estimates, not dependency planning.
- D06 blocks exact scaffold commands/dependency acceptance and performance-index issues.
