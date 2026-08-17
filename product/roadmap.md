# Product roadmap

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP product boundary, accepted post-MVP themes, and deadlines for deferred decisions
> Supersedes: Roadmap sections and calendar estimates in legacy PRDs and planning snapshots

## How to read this roadmap

This roadmap separates accepted MVP scope from later product direction. Later themes are not approved requirements, delivery commitments, or a calendar schedule. A theme requires its own decision and feature PRD before implementation. Live GitHub issues own execution state and issue counts; the [implementation plan](../planning/mvp-implementation-plan.md) owns milestone sequencing.

## MVP release scope

The MVP includes all capabilities in the [umbrella MVP PRD](prds/prd-householdhub-mvp.md):

- verified email/password identity, Google authentication, explicit linking, password recovery, and revocable sessions;
- private households with owner/member roles, invitations, join codes, member removal, multi-household switching, and 30-day recoverable household deletion;
- shared task management and shopping list;
- basic expense and inventory tracking;
- the minimal household dashboard;
- authorization/isolation, security, testing, release, and minimum operational requirements defined by their canonical documents.

MVP does not become smaller merely because a capability is labeled supporting rather than primary.

## Direction after MVP

### Enhanced collaboration

Accepted areas for future discovery, not yet specified:

- recurring task automation;
- assignment and task history;
- household activity feed;
- task-assignment and household-activity notifications.

### Financial capabilities

Accepted areas for future discovery, not yet specified:

- expense splitting and participant shares;
- settlement tracking;
- household-defined expense categories;
- receipt or other expense attachments;
- a household currency-change feature.

Expense splitting carries no promise of avoiding data migration. A household currency-change feature requires a dedicated product/data decision covering historical expenses, aggregation, conversion policy, exchange-rate source, valuation dates, and reporting.

### Roles and richer collaboration

Accepted areas for future discovery, not yet specified:

- Admin, Restricted Member, Guest, or other roles;
- public or administrative ownership-transfer workflows;
- calendar views and external-calendar integration;
- task comments, mentions, and attachments;
- richer activity/history views.

### Extensions

Accepted areas for future discovery, not yet specified:

- native mobile applications;
- additional authentication providers;
- third-party integrations;
- household analytics and reporting;
- household data export;
- localization;
- user profile customization.

Household data export is not an MVP requirement and no export behavior is approved. Canonical design should not deliberately foreclose a future export decision.

## Post-launch measurement candidates

The legacy PRD identified household adoption (households with multiple active members), tasks created per household, task completion rate, and 30-day user activity as useful post-launch observations. No numeric target or launch gate is approved for these measures; telemetry collection remains subject to the security, privacy, and `D03` decisions.

## Deferred decisions and required deadlines

The following decisions intentionally remain unresolved. They may not be resolved implicitly in product, architecture, OpenAPI, security, planning, or implementation documents.

| ID | Deferred decision | Required resolution deadline |
|---|---|---|
| `D01` | Exact password-policy, password-reset-token, and authentication/rate-limit constants | Choose safe launch defaults before M1 authentication implementation and contract generation; lock and review them by M8 hardening |
| `D02` | Exact managed transactional-email provider; production deployment, secret-store, and monitoring providers | Select managed email before M1 integration; select deployment, secret-store, and monitoring providers before M9 provisioning and launch |
| `D03` | Launch jurisdiction; user-data retention/anonymization; audit, security, email, and session retention | Resolve before any real personal data is processed, including real-email staging |
| `D04` | Numeric RTO, RPO, alert thresholds, and incident severity definitions | Resolve after `D02` and `D03`, before M9 launch sign-off |
| `D05` | Calendar schedule commitment | Set only after named staffing, capacity, and start date are known and approved scope has been re-sized |
| `D06` | Exact compatible patch versions, Backend packaging/lock strategy and PostgreSQL driver, remaining lint/format configuration, and performance-only indexes | Choose compatible patches and tools at M0 scaffold; add performance-only indexes only after representative queries/data and benchmark evidence |

Approved baselines remain fixed while these details are selected: Python 3.14 and Django 5.2 LTS; React 19, TypeScript, Vite, and npm; native CSS, CSS Modules, and CSS custom properties; Vitest and React Testing Library; PostgreSQL; and GitHub Actions. Repository manifests and committed lockfiles own exact dependency versions.

## Later decisions required before feature work

- **Optimistic concurrency:** requires a dedicated decision before any conflict-detection or edit-`409` feature is specified.
- **Household currency change:** requires the financial product/data decision described above before the immutable MVP currency can change.
- **Ownership transfer:** requires an authorization, account-lifecycle, and support decision before public transfer or owner anonymization/hard deletion is implemented.
- **Assignment history:** requires a task-history decision before former-assignee identity is stored or displayed as history.
- **Numeric performance gates:** require a defined percentile, endpoint set, dataset, environment, concurrency profile, and duration before becoming acceptance thresholds.
- **Coverage thresholds:** require an evidence-based baseline before any percentage becomes merge-blocking.
- **Google API access:** requires a feature decision before provider access/refresh tokens may be persisted.
- **Additional operations detail:** should be created only when it can contain executable, environment-specific guidance rather than placeholders.

## Change control

Moving an item into the MVP requires explicit product approval and updates to the umbrella PRD, its feature PRD, release acceptance, and affected canonical contracts. Reordering a directional theme does not itself approve requirements or create a delivery date.
