# Backlog reconciliation report

> **Status:** Draft  
> **Owner:** Documentation repository  
> **Last reviewed:** 2026-08-17  
> **Canonical for:** Nothing  
> **Purpose:** Point-in-time reconciliation between the canonical documentation and the live GitHub backlog of the `House-Hold-Hub` organization, covering Phase 1 (audit) and Phase 2 (consistency validation).

## Warning

This report is an audit artifact. It is **canonical for nothing** and it does not modify or redefine any accepted PRD, ADR, OpenAPI operation, permission rule, domain invariant, security control, roadmap decision, or quality strategy. Where it states that a live issue is wrong, the authority is always the cited canonical document, never this file.

Live GitHub issues and milestones remain canonical for execution state, issue count, assignment and status. `planning/github-issues-draft.md` remains a Draft candidate decomposition, canonical for nothing, and was **not** treated as independently authoritative here.

**No GitHub mutation was performed.** No issue, state, title, body, label, milestone or dependency was created, edited, closed or deleted. The proposals below await approval.

## 0. Canonical baseline

This reconciliation was derived from an immutable commit of the Documentation repository. Phase 3 mutation of the live backlog is traceable to this SHA.

| Field | Value |
|---|---|
| Repository | `House-Hold-Hub/Documentation` |
| Baseline commit | `3006cae70caba1829d0ad8cfcc9b17af5791f052` |
| Short SHA | `3006cae` |
| Committed | `2026-08-17T16:33:39+02:00` |
| Branch | `main` |
| Files | 60 canonical documents |
| Pushed to origin | **No** — local commit only; pushing requires separate approval |

Before this commit the Documentation repository had **no commits at all**, so there was no immutable reference a backlog mutation could cite. The two audit artifacts are deliberately *excluded* from the baseline commit: recording the baseline SHA inside a file that is itself part of that commit would be circular. They are committed separately, after the fact, referencing this SHA.

The four sibling repositories (Automation, Backend, Frontend, Infrastructure) also have no commits. They contain only a `.gitignore` and no application code, so they need no baseline for this reconciliation — but note that Phase 3 will create and edit issues against repositories whose default branches are still empty.

## 1. Executive summary

The Documentation repository was rewritten into its current governed form on 2026-08-16: the monolithic PRD, system design and ERD snapshots were archived and replaced by seven feature PRDs, a permissions matrix, a domain model, fifteen ADRs, a standalone machine-readable OpenAPI contract, a security model, a testing strategy, release acceptance criteria, a roadmap and an implementation plan.

The 69 live GitHub issues were generated **before** that rewrite, from the now-archived snapshots. The backlog is therefore a faithful projection of a superseded architecture. Every one of the 69 issues requires at least a reference correction; 17 distinct drift families were identified, several of which invert a canonical decision rather than merely restating it loosely.

The single most consequential finding is that **the canonical corpus itself is internally consistent**. All 26 Phase 2 consistency checks pass with zero conflicts. Every supersession is explicit and bidirectional, every ADR that was partially superseded names both its successor and the exact portion superseded, and no two accepted documents disagree in the areas audited. This means the reconciliation is a one-directional projection problem: the backlog must be corrected to match the documentation, and no documentation change is required or proposed.

### Counts

| Candidate action | Count |
|---|---|
| `KEEP` | 0 |
| `UPDATE` | 65 |
| `SPLIT` | 6 |
| `MERGE` | 1 |
| `CREATE` | 3 |
| `CLOSE_SUPERSEDED` | 0 |
| **Total candidates** | **75** |

| Live issue disposition | Count |
|---|---|
| `KEEP` | 0 |
| `UPDATE` | 66 |
| `SPLIT` | 3 |
| `MERGE` | 0 |
| `CLOSE_SUPERSEDED` | 0 |
| **Total live issues** | **69** |

A candidate action and a live-issue disposition are different things and are counted separately. One live issue may map to several candidates and one candidate may absorb several live issues, so the two totals are not expected to match.

### Candidates by repository

| Repository | UPDATE | SPLIT | MERGE | CREATE | Total |
|---|---|---|---|---|---|
| Automation | 4 | 0 | 0 | 0 | 4 |
| Backend | 31 | 6 | 0 | 1 | 38 |
| Documentation | 3 | 0 | 0 | 0 | 3 |
| Frontend | 24 | 0 | 0 | 2 | 26 |
| Infrastructure | 3 | 0 | 1 | 0 | 4 |

### Candidates by milestone

| Milestone | Candidates |
|---|---|
| M0 | 16 |
| M1 | 12 |
| M2 | 16 |
| M3 | 5 |
| M4 | 5 |
| M5 | 5 |
| M6 | 5 |
| M7 | 2 |
| M8 | 6 |
| M9 | 3 |

### Candidate derivation — draft 68 to final 75

The final candidate set is derived from the Draft decomposition in `planning/github-issues-draft.md`, which is canonical for nothing and was used only as a starting inventory. The arithmetic reconciles exactly:

| Step | Δ | Running |
|---|---|---|
| Draft candidates (`M0-B1` … `M9-A1`) | — | **68** |
| Draft candidates removed or redefined out of existence | −0 | 68 |
| Draft candidates carried forward | 68 | 68 |
| Extra candidates from splitting one live issue into several | +3 | 71 |
| Extra candidate from preserving an existing live decomposition | +1 | 72 |
| New canonical units discovered (no draft lineage) | +3 | **75** |

**Every one of the 68 draft candidates survives.** None was dropped, and none was merged out of existence — the single MERGE redistributes scope between two draft candidates that both survive (`M0-B4` and `M0-I1`), so it adds and removes nothing.

#### The +3 from splitting live issues

| Draft candidate | Expands to | Driver |
|---|---|---|
| `M1-B3` | `M1-B3`, `M1-B4`, `M1-B5` | Backend#8 bundles credential auth, the email-verification lifecycle and password recovery, and omits the CSRF bootstrap entirely. Split along contract operation groups. **+2** |
| `M2-B4` | `M2-B4`, `M2-B5` | Backend#14 bundles the owner-facing invitation lifecycle with the invitee handoff, and encodes the superseded token-accept workflow for the latter. **+1** |

#### The +1 from preserving an existing live decomposition

| Draft candidate | Expands to | Driver |
|---|---|---|
| `M1-F1` | `M1-F1`, `M1-F4` | The draft bundles "authentication/session state and protected navigation" into one candidate, but the live backlog already separates them as Frontend#5 (auth context) and Frontend#7 (protected routing). Preserving the finer live boundary keeps both issue numbers. This is the draft under-decomposing, **not** a split introduced by this audit. **+1** |

#### The +3 new canonical units

| Candidate | Why the draft has no equivalent |
|---|---|
| `M2-B7` — household soft-delete recovery | HH-FR-034 requires support/administration recovery within the 30-day window and release Journey 13 requires it demonstrated. The draft's `M2-B1` covers the soft-delete marker and nothing covers recovery. `CREATE`. |
| `M2-B9` — critical audit events | The security model requires audit events for invitation, membership and household lifecycle actions. The draft has no audit candidate at all. Live Backend#33 already carries this work, so it is `UPDATE`, not `CREATE` — valid work the draft omitted. |
| `M2-B10` — idempotent scheduled purge | HH-FR-035 requires the purge and the implementation plan places it among M2 outcomes. The draft has no purge candidate. Live Backend#34 already carries it, so it is `UPDATE` — again valid work the draft omitted. |

Two of the three new units are `UPDATE` rather than `CREATE`: they are gaps in the **draft**, not gaps in the **backlog**. This is a concrete demonstration that the draft is not authoritative — the live backlog contained required canonical work the draft had lost.

#### Reconciliation against the 6 new issues Phase 3 will open

| Source | Count |
|---|---|
| `CREATE` candidates (no live issue exists) | 3 |
| `SPLIT` successors carrying no primary role | 3 |
| **Total new GitHub issues in Phase 3** | **6** |

The other 69 candidates map onto the 69 existing issue numbers, all of which are preserved.

## 2. Notable decisions

### 2.1 `CREATE` — canonical work with no live issue (3)

**`M1-F3` — Implement Google login and explicit reauthenticated account linking/unlinking** (Frontend, M1)

> No live Frontend issue covers explicit account linking or unlinking. Frontend#6 provides only a Google login button, leaving IA-FR-008, the linking journey and the unlink operation unrepresented.

Add the Frontend half of collision-safe linking: a Google login entry point, a collision path that explains why automatic linking did not occur, an explicit connect action gated on recent reauthentication, and an unlink action with the same gate. Communicate that other sessions are revoked.

**`M2-B7` — Implement household soft-delete recovery and the support/administration path** (Backend, M2)

> HH-FR-034 requires support/administration recovery of a soft-deleted household within the 30-day window, restoring the preserved household, Memberships and resources to active normal access. Release Journey 13 requires that recovery be demonstrated and idempotent. No live issue covers it: Backend#11 covers only the soft-delete marker and Backend#34 only the purge.

Add the missing middle of the deletion lifecycle: an administrative recovery path that restores a soft-deleted household and its preserved children to normal access, is idempotent, refuses households already purged, and emits the critical audit events the security model requires.

**`M2-F4` — Implement the invitation fragment landing, exchange and verified acceptance flow** (Frontend, M2)

> No live Frontend issue covers the invitation landing page. ADR-013's landing-page protections, the fragment handling rules and the explicit-acceptance flow are entirely unrepresented in the backlog, although release Journey 2 depends on them.

Add the invitee-facing flow: read the verifier from the URI fragment, remove it from browser-visible navigation state immediately, never write it to localStorage or sessionStorage, exchange it through a rate-limited POST body, and discard the raw value. Serve the landing route with a restrictive Content Security Policy, Referrer-Policy: no-referrer and Cache-Control: no-store, and admit no third-party script that could observe the fragment. After authentication and verification, render only the safe preview and require an explicit acceptance action.

### 2.2 `SPLIT` — live issues whose boundary the canon changed (3 issues → 6 candidates)

**Backend#4** → `M0-B4`, `M0-I1`

Bundles the Backend service Dockerfile with a full-stack docker-compose covering React and PostgreSQL. Ownership splits: the Backend image stays here, the composition moves to Infrastructure per the technology baseline and ADR-009, and the React image moves to Frontend.

**Backend#8** → `M1-B3`, `M1-B4`, `M1-B5`

Bundles credential auth, verification and recovery while omitting the CSRF bootstrap and every email-lifecycle operation the contract defines. Splits along contract operation groups so each unit has verifiable boundaries; D01 constants and status 422 removed throughout.

**Backend#14** → `M2-B4`, `M2-B5`

Encodes the superseded /invitations/{token}/accept workflow and revocation by bearer token. Splits into owner lifecycle (create, list, revoke by identifier, resend with rotation) and the invitee handoff (exchange, safe preview, explicit acceptance) that ADR-013 and the contract require.

### 2.3 `MERGE` — ownership correction (1)

**`M0-I1` — Define the local PostgreSQL and full-stack runtime composition boundary**

Absorbs: Infrastructure#1 (primary), Backend#4 (split_source)

Absorb the full-stack compose scope from Backend#4 into Infrastructure, which the technology baseline names as the owner of local full-stack orchestration consuming service-owned images. Remove the inverted dependency on Backend#4 and replace it with dependencies on the two service Dockerfile candidates. PostgreSQL 14+ is the approved family; the exact deployed version stays with Infrastructure configuration.

### 2.4 `CLOSE_SUPERSEDED` — none, and why

No live issue is proposed for closure. This is a deliberate finding rather than an omission.

The backlog's drift is pervasive but it is almost always a *portion* of an issue rather than the whole of it. Where the canon deleted work outright — dashboard expense widgets, the `/invitations/{token}/accept` workflow, the `google_id` field, `amount_cents` — that deleted work always sits inside an issue whose remaining scope is still required. The correct action in each case is `UPDATE` (remove the deleted scope) or `SPLIT` (separate the surviving parts), not closure. Closing those issues would discard valid work along with the invalid.

Two candidates came close to closure and are recorded here for review:

- **Documentation#1** describes building a documentation tree that already exists in canonical form, and most of its acceptance criteria are already satisfied. It is proposed as `UPDATE`, narrowed to the residual work (contract publication and CI validation), rather than closed. See open question OQ-2.
- **Backend#4** loses its largest component to Infrastructure but retains a real deliverable (the Backend service Dockerfile), so it splits rather than closes.

If a future review prefers a cleaner mapping to the candidate draft over issue-number preservation, these two are the first candidates to revisit.

## 3. Drift families

Every family below is a case where a live issue asserts something a named canonical document forbids or replaces. Ordered roughly by blast radius.

| ID | Family | Canonical rule | Affected |
|---|---|---|---|
| D-01 | Superseded runtime baseline | ADR-010 and the technology baseline fix Python 3.14 and Django 5.2 LTS. Exact patches are D06 and belong to manifests/lockfiles. | Backend#1, Backend#5 |
| D-02 | Forbidden identity fields | ADR-011 and IA-FR-002/005/009 forbid a bespoke password field and a provider-specific `google_id`; provider identity uses django-allauth `SocialAccount` and verification uses allauth's verified-email record. | Backend#2, Backend#6 |
| D-03 | Inverted contract ownership | ADR-014 and ADR-009 make the Documentation-owned `api/openapi.yaml` the sole route and wire-contract source of truth; Backend implements and validates against it. | Backend#3, Frontend#3, Documentation#1 |
| D-04 | Inverted runtime ownership | The technology baseline assigns local full-stack orchestration to Infrastructure consuming service-owned images; ADR-009 keeps service Dockerfiles in service repositories. | Backend#4, Infrastructure#1 |
| D-05 | Missing required household currency | HH-FR-001 and `HouseholdCreateRequest` require a supported ISO 4217 `currency_code`; it is immutable thereafter. | Backend#11, Frontend#10 |
| D-06 | Superseded invitation workflow | ADR-013 and HH-FR-016/018/019/020/023 require fragment transport, a rate-limited exchange, a non-secret generation-bound intent, a safe preview, explicit acceptance, and revocation by non-secret invitation identifier. The contract defines `exchangeInvitationVerifier`, `previewPendingInvitation`, `acceptPendingInvitation` and `resendHouseholdInvitation`. | Backend#14, Frontend#11 |
| D-07 | Superseded money model | EXP-FR-002/003/013/014 require `amount_minor` interpreted through the ISO minor-unit exponent, a snapshotted immutable `currency_code`, an explicit `incurred_on`, `SET NULL` payer behaviour, and the categories Food/Utilities/Maintenance/Entertainment/Other. The domain model states `amount_cents` is not a canonical field or concept. | Backend#23, Backend#24, Frontend#18, Frontend#19 |
| D-08 | Dashboard scope inflation | `DashboardResponse` defines exactly seven required fields with `maxItems: 3` and no expense field; DASH-FR-003/007/008 require a client-supplied `as_of`, a deterministic three-task preview and a separate complete pending count. Expense widgets on the dashboard are an explicit MVP non-goal. | Backend#29, Frontend#22 |
| D-09 | Numeric test-count and coverage quotas | The testing strategy rejects an arbitrary number of tests or an unsupported merge-blocking coverage percentage as a proxy for confidence; the MVP PRD states closing a particular number of issues or tests is not a product acceptance criterion. | Backend#16/19/22/25/28/30, Frontend#8/13/15/17/19/21/23 |
| D-10 | Unqualified performance gates | The testing strategy requires percentile, endpoint set, dataset, environment, concurrency profile and duration before a figure becomes a target; the roadmap lists fixed bundle-size and Lighthouse thresholds among gates needing that context first. | Backend#30/32, Frontend#24, Automation#4 |
| D-11 | Deferred vendors selected | D02 defers the managed email provider until before M1 integration and the deployment, secret-store and monitoring providers until before M9. ADR-015 keeps email behind a provider-neutral adapter. | Backend#10, Infrastructure#4 |
| D-12 | Deferred security constants fixed | D01 defers exact password-policy, reset-token and rate-limit constants; safe launch defaults are chosen before M1 implementation and locked at M8. | Backend#8, Backend#31 |
| D-13 | Session and OAuth contradictions | ADR-011 requires `SameSite=Lax` for OAuth top-level redirects, mandatory validated state, and states that logout ends only the HouseHoldHub session. IA-FR-008 forbids automatic linking and requires explicit, recently reauthenticated linking. | Backend#7, Backend#9, Backend#31 |
| D-14 | Invalid integrity guarantee | ADR-012 and TASK-FR-003 explicitly forbid this claim: a normal foreign key validates existence, not equality with a separate `household_id`. The guaranteed mechanism is service-layer validation plus negative integrity tests. | Backend#17 |
| D-15 | Non-contract status code | ADR-014 and api/README state the API never returns 422; validation failures are 400. | Backend#8, Backend#27 |
| D-16 | Archived documents cited as normative | All are archived. The repository README states archived documents are non-navigational and must not be cited as current requirements; each legacy `FR-nn` has a named canonical successor in the PRD traceability tables. | ~20 issues across all five repositories |
| D-17 | Wrong title prefix | ADR-009 assigns repository-local workflow entry points to the service repository. The issues are in the correct repository; only the prefix is wrong. | Backend#5, Frontend#4 |

**D-01 — Superseded runtime baseline**

- *Observed:* `Django 6.x` in title and dependencies.
- *Canonical rule:* ADR-010 and the technology baseline fix Python 3.14 and Django 5.2 LTS. Exact patches are D06 and belong to manifests/lockfiles.
- *Affected:* Backend#1, Backend#5

**D-02 — Forbidden identity fields**

- *Observed:* `password_hash` and `google_id` on the User model; `AbstractUser` without UUID identity.
- *Canonical rule:* ADR-011 and IA-FR-002/005/009 forbid a bespoke password field and a provider-specific `google_id`; provider identity uses django-allauth `SocialAccount` and verification uses allauth's verified-email record.
- *Affected:* Backend#2, Backend#6

**D-03 — Inverted contract ownership**

- *Observed:* Backend publishes a generated schema at `/api/schema/openapi.yaml`; Frontend generates types from `OPENAPI.md`.
- *Canonical rule:* ADR-014 and ADR-009 make the Documentation-owned `api/openapi.yaml` the sole route and wire-contract source of truth; Backend implements and validates against it.
- *Affected:* Backend#3, Frontend#3, Documentation#1

**D-04 — Inverted runtime ownership**

- *Observed:* Backend owns the full-stack `docker-compose`; Infrastructure#1 declares a dependency on it.
- *Canonical rule:* The technology baseline assigns local full-stack orchestration to Infrastructure consuming service-owned images; ADR-009 keeps service Dockerfiles in service repositories.
- *Affected:* Backend#4, Infrastructure#1

**D-05 — Missing required household currency**

- *Observed:* Household creation collects name and description only.
- *Canonical rule:* HH-FR-001 and `HouseholdCreateRequest` require a supported ISO 4217 `currency_code`; it is immutable thereafter.
- *Affected:* Backend#11, Frontend#10

**D-06 — Superseded invitation workflow**

- *Observed:* `POST /households/{id}/invitations/{token}/accept`, revocation by bearer token, invitation created through the members operation, no resend.
- *Canonical rule:* ADR-013 and HH-FR-016/018/019/020/023 require fragment transport, a rate-limited exchange, a non-secret generation-bound intent, a safe preview, explicit acceptance, and revocation by non-secret invitation identifier. The contract defines `exchangeInvitationVerifier`, `previewPendingInvitation`, `acceptPendingInvitation` and `resendHouseholdInvitation`.
- *Affected:* Backend#14, Frontend#11

**D-07 — Superseded money model**

- *Observed:* `amount_cents`, dollars-to-cents conversion, `PROTECT` payer, category enum `groceries|utilities|entertainment|other`.
- *Canonical rule:* EXP-FR-002/003/013/014 require `amount_minor` interpreted through the ISO minor-unit exponent, a snapshotted immutable `currency_code`, an explicit `incurred_on`, `SET NULL` payer behaviour, and the categories Food/Utilities/Maintenance/Entertainment/Other. The domain model states `amount_cents` is not a canonical field or concept.
- *Affected:* Backend#23, Backend#24, Frontend#18, Frontend#19

**D-08 — Dashboard scope inflation**

- *Observed:* `recent_expenses`, `expenses_total_cents`, five-task preview, no `as_of`, no complete pending count.
- *Canonical rule:* `DashboardResponse` defines exactly seven required fields with `maxItems: 3` and no expense field; DASH-FR-003/007/008 require a client-supplied `as_of`, a deterministic three-task preview and a separate complete pending count. Expense widgets on the dashboard are an explicit MVP non-goal.
- *Affected:* Backend#29, Frontend#22

**D-09 — Numeric test-count and coverage quotas**

- *Observed:* `100+ cases`, `50+ cases`, `20+ cases`, `15+ cases`, `coverage >95%`, `coverage >90%`.
- *Canonical rule:* The testing strategy rejects an arbitrary number of tests or an unsupported merge-blocking coverage percentage as a proxy for confidence; the MVP PRD states closing a particular number of issues or tests is not a product acceptance criterion.
- *Affected:* Backend#16/19/22/25/28/30, Frontend#8/13/15/17/19/21/23

**D-10 — Unqualified performance gates**

- *Observed:* `<200ms`, `100 concurrent users`, `<500ms`, `main bundle <500KB`, `Lighthouse >80`, `18+ indexes`.
- *Canonical rule:* The testing strategy requires percentile, endpoint set, dataset, environment, concurrency profile and duration before a figure becomes a target; the roadmap lists fixed bundle-size and Lighthouse thresholds among gates needing that context first.
- *Affected:* Backend#30/32, Frontend#24, Automation#4

**D-11 — Deferred vendors selected**

- *Observed:* `SendGrid/SES/Mailgun`, `Sentry free tier`.
- *Canonical rule:* D02 defers the managed email provider until before M1 integration and the deployment, secret-store and monitoring providers until before M9. ADR-015 keeps email behind a provider-neutral adapter.
- *Affected:* Backend#10, Infrastructure#4

**D-12 — Deferred security constants fixed**

- *Observed:* Password minimum length 10 with complexity, 5 logins/min per IP, 3 resets/hour per email, 1-hour reset token.
- *Canonical rule:* D01 defers exact password-policy, reset-token and rate-limit constants; safe launch defaults are chosen before M1 implementation and locked at M8.
- *Affected:* Backend#8, Backend#31

**D-13 — Session and OAuth contradictions**

- *Observed:* `SameSite=Strict`; logout clears the Google session; account linking optional; no OAuth state validation.
- *Canonical rule:* ADR-011 requires `SameSite=Lax` for OAuth top-level redirects, mandatory validated state, and states that logout ends only the HouseHoldHub session. IA-FR-008 forbids automatic linking and requires explicit, recently reauthenticated linking.
- *Affected:* Backend#7, Backend#9, Backend#31

**D-14 — Invalid integrity guarantee**

- *Observed:* A cross-table `CHECK` constraint is claimed to guarantee same-household task assignment.
- *Canonical rule:* ADR-012 and TASK-FR-003 explicitly forbid this claim: a normal foreign key validates existence, not equality with a separate `household_id`. The guaranteed mechanism is service-layer validation plus negative integrity tests.
- *Affected:* Backend#17

**D-15 — Non-contract status code**

- *Observed:* Acceptance criteria admit `422`.
- *Canonical rule:* ADR-014 and api/README state the API never returns 422; validation failures are 400.
- *Affected:* Backend#8, Backend#27

**D-16 — Archived documents cited as normative**

- *Observed:* `DOMAIN_MODEL_CORRECTED.md`, `ERD.md`, `OPENAPI.md`, `SYSTEM_DESIGN.md`, and legacy `FR-nn` identifiers.
- *Canonical rule:* All are archived. The repository README states archived documents are non-navigational and must not be cited as current requirements; each legacy `FR-nn` has a named canonical successor in the PRD traceability tables.
- *Affected:* ~20 issues across all five repositories

**D-17 — Wrong title prefix**

- *Observed:* `[M0-Automation]` on repository-local service workflows.
- *Canonical rule:* ADR-009 assigns repository-local workflow entry points to the service repository. The issues are in the correct repository; only the prefix is wrong.
- *Affected:* Backend#5, Frontend#4

## 4. Values that must be preserved

Not every number in the backlog is drift. These are approved, fully specified, and must survive the cleanup of D-09 and D-10:

| Value | Source |
|---|---|
| 14-day session lifetime | ADR-011 revocation matrix; IA-FR-012 |
| 30-day invitation expiry | ADR-013; HH-FR-016; `InvitationOwnerResponse.expires_at` |
| 30-day household retention before purge | HH-FR-033/035; domain model deletion lifecycle |
| 8-character uppercase alphanumeric join code | HH-FR-027; ADR-013; security model |
| At most 3 dashboard preview tasks | DASH-FR-007; `DashboardResponse.due_tasks.maxItems` |
| 7-day inclusive due-soon window | DASH-FR-005 |
| 375 / 1280 CSS-pixel responsive targets | Testing strategy; release acceptance |
| 5 expense categories | EXP-FR-011; `ExpenseCategory` enum |

## 5. Reconciliation matrix — candidates

Full records, including acceptance criteria and dependency intent, are in `backlog-reconciliation-matrix.json`.

| Candidate | MS | Repo | Live issue(s) | Action | Proposed title | Conf |
|---|---|---|---|---|---|---|
| `M0-B1` | M0 | Backend | Backend#1 | `UPDATE` | Scaffold Django project on the approved Python 3.14 / Django 5.2 LTS runtime baseline | high |
| `M0-B2` | M0 | Backend | Backend#2 | `UPDATE` | Establish the custom UUID User model and initial migration skeleton | high |
| `M0-B3` | M0 | Backend | Backend#3 | `UPDATE` | Configure DRF and validate the implementation against the Documentation-owned OpenAPI contract | high |
| `M0-B4` | M0 | Backend | Backend#4 | `SPLIT` | Add the Backend service Dockerfile and local runtime configuration | high |
| `M0-B5` | M0 | Backend | Backend#5 | `UPDATE` | Add the Backend repository-local GitHub Actions workflow | high |
| `M0-F1` | M0 | Frontend | Frontend#1 | `UPDATE` | Scaffold the React 19 / TypeScript / Vite application with native CSS Modules and design tokens | high |
| `M0-F2` | M0 | Frontend | Frontend#2 | `UPDATE` | Build the session/CSRF-aware API client with safe error and redaction behaviour | high |
| `M0-F3` | M0 | Frontend | Frontend#3 | `UPDATE` | Generate TypeScript contract artifacts from the Documentation-owned OpenAPI contract | high |
| `M0-F4` | M0 | Frontend | Frontend#4 | `UPDATE` | Establish Vitest / React Testing Library and the Frontend repository-local workflow | high |
| `M0-I1` | M0 | Infrastructure | Infrastructure#1, Backend#4 | `MERGE` | Define the local PostgreSQL and full-stack runtime composition boundary | high |
| `M0-I2` | M0 | Infrastructure | Infrastructure#2 | `UPDATE` | Define the environment and secret configuration contract without selecting deferred vendors | high |
| `M0-A1` | M0 | Automation | Automation#1 | `UPDATE` | Provide reusable build and pipeline assets consumable by service repositories | high |
| `M0-A2` | M0 | Automation | Automation#2 | `UPDATE` | Provide shared test, contract and security gates | high |
| `M0-A3` | M0 | Automation | Automation#3 | `UPDATE` | Provide local setup automation that consumes real repository manifests | high |
| `M0-D1` | M0 | Documentation | Documentation#1 | `UPDATE` | Publish the documentation architecture and validate the OpenAPI contract in CI | high |
| `M0-D2` | M0 | Documentation | Documentation#2 | `UPDATE` | Maintain contribution, contract-review and cross-repository governance | high |
| `M1-B1` | M1 | Backend | Backend#6 | `UPDATE` | Implement the custom UUID User with django-allauth email identity and verification gating | high |
| `M1-B2` | M1 | Backend | Backend#7 | `UPDATE` | Implement database sessions, the indexed session registry, rotation and the revocation matrix | high |
| `M1-B3` | M1 | Backend | Backend#8 | `SPLIT` | Implement CSRF bootstrap, signup, login, logout and current-user operations | high |
| `M1-B4` | M1 | Backend | Backend#8 | `SPLIT` | Implement the email verification and primary-email change lifecycle | high |
| `M1-B5` | M1 | Backend | Backend#8 | `SPLIT` | Implement enumeration-safe password recovery and authenticated password change | high |
| `M1-B6` | M1 | Backend | Backend#9 | `UPDATE` | Implement Google OAuth trust validation and explicit collision-safe linking | high |
| `M1-B7` | M1 | Backend | Backend#10 | `UPDATE` | Implement the provider-neutral transactional email adapter with durable delivery state | high |
| `M1-F1` | M1 | Frontend | Frontend#5 | `UPDATE` | Implement authentication and session state with verification awareness | high |
| `M1-F2` | M1 | Frontend | Frontend#6 | `UPDATE` | Implement signup, verification, login, recovery and recoverable-delivery UX | high |
| `M1-F3` | M1 | Frontend | — | `CREATE` | Implement Google login and explicit reauthenticated account linking/unlinking | high |
| `M1-F4` | M1 | Frontend | Frontend#7 | `UPDATE` | Implement protected routing with verification gating | high |
| `M1-F5` | M1 | Frontend | Frontend#8 | `UPDATE` | Add identity security, accessibility and contract tests | high |
| `M2-B1` | M2 | Backend | Backend#11 | `UPDATE` | Implement Household with immutable ISO 4217 currency, join code and soft-delete lifecycle | high |
| `M2-B2` | M2 | Backend | Backend#12 | `UPDATE` | Implement Membership and the owner invariants | high |
| `M2-B3` | M2 | Backend | Backend#13 | `UPDATE` | Implement household and member operations from the contract | high |
| `M2-B4` | M2 | Backend | Backend#14 | `SPLIT` | Implement the invitation model and owner lifecycle operations | high |
| `M2-B5` | M2 | Backend | Backend#14 | `SPLIT` | Implement invitation verifier exchange, safe preview and explicit acceptance | high |
| `M2-B6` | M2 | Backend | Backend#15 | `UPDATE` | Implement owner-only join-code read/regenerate and rate-limited joining | high |
| `M2-B7` | M2 | Backend | — | `CREATE` | Implement household soft-delete recovery and the support/administration path | high |
| `M2-B8` | M2 | Backend | Backend#16 | `UPDATE` | Complete household authorization and negative isolation coverage | high |
| `M2-B9` | M2 | Backend | Backend#33 | `UPDATE` | Emit critical audit events for invitation, membership and household lifecycle actions | high |
| `M2-B10` | M2 | Backend | Backend#34 | `UPDATE` | Implement the idempotent scheduled purge of soft-deleted households | high |
| `M2-F1` | M2 | Frontend | Frontend#9 | `UPDATE` | Implement the household selector and switcher | high |
| `M2-F2` | M2 | Frontend | Frontend#10 | `UPDATE` | Implement household creation including the required currency | high |
| `M2-F3` | M2 | Frontend | Frontend#11 | `UPDATE` | Implement member and invitation management | high |
| `M2-F4` | M2 | Frontend | — | `CREATE` | Implement the invitation fragment landing, exchange and verified acceptance flow | high |
| `M2-F5` | M2 | Frontend | Frontend#12 | `UPDATE` | Implement the join-by-code flow | high |
| `M2-F6` | M2 | Frontend | Frontend#13 | `UPDATE` | Add household, membership and invitation UI and security tests | high |
| `M3-B1` | M3 | Backend | Backend#17 | `UPDATE` | Implement Task with service-layer same-household assignment validation | high |
| `M3-B2` | M3 | Backend | Backend#18 | `UPDATE` | Implement task operations and last-write-wins behaviour | high |
| `M3-B3` | M3 | Backend | Backend#19 | `UPDATE` | Complete the task permission and isolation matrix coverage | high |
| `M3-F1` | M3 | Frontend | Frontend#14 | `UPDATE` | Implement task list, forms, assignment, completion and deletion UX | high |
| `M3-F2` | M3 | Frontend | Frontend#15 | `UPDATE` | Add task UI, accessibility, permission-loss and contract tests | high |
| `M4-B1` | M4 | Backend | Backend#20 | `UPDATE` | Implement ShoppingItem | high |
| `M4-B2` | M4 | Backend | Backend#21 | `UPDATE` | Implement shopping operations including clear-purchased | high |
| `M4-B3` | M4 | Backend | Backend#22 | `UPDATE` | Complete shopping permission and isolation coverage | high |
| `M4-F1` | M4 | Frontend | Frontend#16 | `UPDATE` | Implement pending/purchased shopping UI with confirmed bulk clear | high |
| `M4-F2` | M4 | Frontend | Frontend#17 | `UPDATE` | Add shopping UI and synchronization tests | high |
| `M5-B1` | M5 | Backend | Backend#23 | `UPDATE` | Implement Expense with amount_minor, snapshotted currency, category and incurred_on | high |
| `M5-B2` | M5 | Backend | Backend#24 | `UPDATE` | Implement expense operations, filters and same-currency aggregates | high |
| `M5-B3` | M5 | Backend | Backend#25 | `UPDATE` | Complete expense money, date, permission and isolation coverage | high |
| `M5-F1` | M5 | Frontend | Frontend#18 | `UPDATE` | Implement browser-local expense date, forms, filters and same-currency totals | high |
| `M5-F2` | M5 | Frontend | Frontend#19 | `UPDATE` | Add expense UI, exponent-formatting and contract tests | high |
| `M6-B1` | M6 | Backend | Backend#26 | `UPDATE` | Implement InventoryItem with the positive-quantity invariant | high |
| `M6-B2` | M6 | Backend | Backend#27 | `UPDATE` | Implement inventory operations and category grouping support | high |
| `M6-B3` | M6 | Backend | Backend#28 | `UPDATE` | Complete inventory permission and isolation coverage | high |
| `M6-F1` | M6 | Frontend | Frontend#20 | `UPDATE` | Implement grouped inventory display and CRUD UX | high |
| `M6-F2` | M6 | Frontend | Frontend#21 | `UPDATE` | Add inventory quantity, permission and UI tests | high |
| `M7-B1` | M7 | Backend | Backend#29 | `UPDATE` | Implement dashboard aggregation with required as_of and the deterministic task preview | high |
| `M7-F1` | M7 | Frontend | Frontend#22 | `UPDATE` | Implement the minimal dashboard with browser-local as_of query identity | high |
| `M8-B1` | M8 | Backend | Backend#30 | `UPDATE` | Automate the cross-feature release journeys | high |
| `M8-B2` | M8 | Backend | Backend#31 | `UPDATE` | Complete authentication, authorization, isolation and abuse hardening | high |
| `M8-B3` | M8 | Backend | Backend#32 | `UPDATE` | Establish a representative performance and query baseline with evidence-based indexing | high |
| `M8-F1` | M8 | Frontend | Frontend#23 | `UPDATE` | Automate critical browser journeys and accessibility checks | high |
| `M8-F2` | M8 | Frontend | Frontend#24 | `UPDATE` | Address measured frontend regressions without unsupported numeric gates | high |
| `M8-D1` | M8 | Documentation | Documentation#3 | `UPDATE` | Reconcile shipped behaviour, contract, guides and release evidence | high |
| `M9-I1` | M9 | Infrastructure | Infrastructure#3 | `UPDATE` | Provision the selected production runtime, secrets, database, migrations and rollback | high |
| `M9-I2` | M9 | Infrastructure | Infrastructure#4 | `UPDATE` | Configure the selected monitoring and error provider with redacted logging and health checks | high |
| `M9-A1` | M9 | Automation | Automation#4 | `UPDATE` | Automate pre-launch contract, smoke, security, migration, restore and rollback checks | high |

## 6. Reconciliation matrix — live issue dispositions

Each of the 69 live issues has exactly one disposition. Mapping is many-to-many.

| Issue | Disposition | Maps to | Rationale |
|---|---|---|---|
| Automation#1 | `UPDATE` | `M0-A1` | Retained but reframed from service release execution to a reusable build asset, with the registry target left to D02. |
| Automation#2 | `UPDATE` | `M0-A2` | Retained and broadened from branch protection to the shared contract, dependency-security and secret-scanning gates Automation owns. |
| Automation#3 | `UPDATE` | `M0-A3` | Retained; the compose dependency repointed from Backend#4 to the Infrastructure-owned composition. |
| Automation#4 | `UPDATE` | `M9-A1` | Retained as pre-launch verification; the 100-user/<500ms gate removed and the missing contract, migration, restore and rollback checks added. |
| Backend#1 | `UPDATE` | `M0-B1` | Represents the canonical Backend scaffold; corrected from Django 6.x to the Django 5.2 LTS / Python 3.14 baseline with dependency pins deferred to D06. |
| Backend#2 | `UPDATE` | `M0-B2` | Narrowed from an all-8-entity stub to the custom UUID User plus initial migration skeleton, which is the only model work M0 owns; forbidden password_hash and google_id fields removed. |
| Backend#3 | `UPDATE` | `M0-B3` | Retained as the DRF foundation but inverted from publishing a generated schema to validating against the Documentation-owned contract. |
| Backend#4 | `SPLIT` | `M0-B4`, `M0-I1` | Bundles the Backend service Dockerfile with a full-stack docker-compose covering React and PostgreSQL. Ownership splits: the Backend image stays here, the composition moves to Infrastructure per the technology baseline and ADR-009, and the React image moves to Frontend. |
| Backend#5 | `UPDATE` | `M0-B5` | Correct repository for a service-local workflow; title prefix and D06-deferred tool choices corrected, coverage gate removed. |
| Backend#6 | `UPDATE` | `M1-B1` | Remains the identity implementation issue but is rebuilt on the canonical model: UUID User, allauth email identity and verification gating, with password_hash and google_id removed. |
| Backend#7 | `UPDATE` | `M1-B2` | Retained and broadened from session configuration to the indexed session registry, rotation and the full revocation matrix; SameSite corrected from Strict to Lax. |
| Backend#8 | `SPLIT` | `M1-B3`, `M1-B4`, `M1-B5` | Bundles credential auth, verification and recovery while omitting the CSRF bootstrap and every email-lifecycle operation the contract defines. Splits along contract operation groups so each unit has verifiable boundaries; D01 constants and status 422 removed throughout. |
| Backend#9 | `UPDATE` | `M1-B6` | Retained as the OAuth issue but corrected on three canon violations: optional linking, clearing the Google session at logout, and missing state/issuer/audience validation. |
| Backend#10 | `UPDATE` | `M1-B7` | Retained as the transactional email issue; named vendors removed pending D02, the on_commit sequence added, and the dependency cycle with Backend#8 broken. |
| Backend#11 | `UPDATE` | `M2-B1` | Retained as the Household model issue with the required immutable ISO 4217 currency and the canonical join-code specification added. |
| Backend#12 | `UPDATE` | `M2-B2` | Retained as the Membership issue with the ADR-012 owner invariants and role immutability added. |
| Backend#13 | `UPDATE` | `M2-B3` | Retained as household and member operations; the regeneration path is corrected, member removal is added to close a real gap, and join-code read/regenerate moves to the code candidate. |
| Backend#14 | `SPLIT` | `M2-B4`, `M2-B5` | Encodes the superseded /invitations/{token}/accept workflow and revocation by bearer token. Splits into owner lifecycle (create, list, revoke by identifier, resend with rotation) and the invitee handoff (exchange, safe preview, explicit acceptance) that ADR-013 and the contract require. |
| Backend#15 | `UPDATE` | `M2-B6` | Already targets the correct POST /households/join operation; broadened to absorb owner-only code read/regenerate and to add rate limiting, uniform failure and eligibility rules. |
| Backend#16 | `UPDATE` | `M2-B8` | Retained as the authorization and isolation suite; the 100+ case and >95% coverage quotas are replaced by the mandatory scenario matrix and the 403/404 semantics corrected. |
| Backend#17 | `UPDATE` | `M3-B1` | Retained as the Task model issue; the cross-table CHECK guarantee that ADR-012 forbids is replaced by service-layer validation plus negative integrity tests. |
| Backend#18 | `UPDATE` | `M3-B2` | Largely canon-consistent already, including the unassigned-completion rule; archived references removed and last-write-wins stated explicitly. |
| Backend#19 | `UPDATE` | `M3-B3` | Retained; 50+ case and >95% coverage quotas replaced by full permission-matrix row coverage. |
| Backend#20 | `UPDATE` | `M4-B1` | Retained; ERD citation replaced by the domain model and purchase-attribution clearing made explicit. |
| Backend#21 | `UPDATE` | `M4-B2` | Already canon-consistent on bulk clear-purchased; only the archived contract reference is corrected. |
| Backend#22 | `UPDATE` | `M4-B3` | Retained; 20+ case quota replaced by matrix coverage. |
| Backend#23 | `UPDATE` | `M5-B1` | Retained as the Expense model issue but corrected on five canon violations: amount_cents, the wrong category enum, PROTECT payer, missing currency snapshot and missing incurred_on. |
| Backend#24 | `UPDATE` | `M5-B2` | Retained; aggregate fields corrected from total_cents to total_amount_minor with currency context, and ordering and filtering moved to incurred_on. |
| Backend#25 | `UPDATE` | `M5-B3` | Retained; 20+ case quota replaced by the required money and date scenarios including non-two-decimal exponents. |
| Backend#26 | `UPDATE` | `M6-B1` | Retained; already canon-consistent apart from the archived ERD citation. |
| Backend#27 | `UPDATE` | `M6-B2` | Retained; status 422 removed and below-one decrement rejection made explicit. |
| Backend#28 | `UPDATE` | `M6-B3` | Retained; 20+ case quota replaced by matrix and quantity-invariant coverage. |
| Backend#29 | `UPDATE` | `M7-B1` | Retained as the dashboard endpoint but heavily corrected: expense fields removed entirely, required as_of added, and the complete pending count plus deterministic three-task preview specified. |
| Backend#30 | `UPDATE` | `M8-B1` | Retained as the journey suite; 100+ case, >90% coverage and the 100-user/<200ms gates replaced by the release-acceptance journeys. |
| Backend#31 | `UPDATE` | `M8-B2` | Retained as security hardening; D01 constants and SameSite=Strict removed, and the missing required security families added. |
| Backend#32 | `UPDATE` | `M8-B3` | Retained as the performance issue; the <200ms gate and the 18+ index count replaced by an evidence-based baseline under D06. |
| Backend#33 | `UPDATE` | `M2-B9` | Valid work absent from the candidate draft, required by the security model's audit-event list. Retained and broadened to the full canonical event set. |
| Backend#34 | `UPDATE` | `M2-B10` | Valid work absent from the candidate draft, required by HH-FR-035. Retained, archived citations replaced, and proposed to move from M8 to M2 to match the implementation plan's household outcomes. |
| Documentation#1 | `UPDATE` | `M0-D1` | Retained but narrowed to the residual canonical work — contract publication and CI validation — since the repository structure the issue describes already exists in canonical form. |
| Documentation#2 | `UPDATE` | `M0-D2` | Retained as governance; the ADR-009/014 breaking-change review rule added and D06-deferred formatter choices removed. |
| Documentation#3 | `UPDATE` | `M8-D1` | Retained as the documentation reconciliation issue; fresh-developer gates removed and archived architecture references replaced. |
| Frontend#1 | `UPDATE` | `M0-F1` | Retained as the Frontend scaffold; CSS Modules and design tokens added, the Vite environment prefix corrected, and the service Dockerfile absorbed from Backend#4. |
| Frontend#2 | `UPDATE` | `M0-F2` | Retained as the API client; error-logging criteria corrected to satisfy the redaction rules and the CSRF bootstrap contract made explicit. |
| Frontend#3 | `UPDATE` | `M0-F3` | Retained; generation retargeted from the archived OPENAPI.md to the Documentation-owned contract with revision stamping. |
| Frontend#4 | `UPDATE` | `M0-F4` | Correct repository for a service-local workflow; title prefix corrected and the Vitest/RTL harness added. |
| Frontend#5 | `UPDATE` | `M1-F1` | Retained as the auth context; verification state added so the restricted pre-verification surface can be presented. |
| Frontend#6 | `UPDATE` | `M1-F2` | Retained as the auth pages; the reset bearer moves from the URL to the fragment and the verification lifecycle screens are added. |
| Frontend#7 | `UPDATE` | `M1-F4` | Retained as route protection; extended to require verified identity, not only a session. |
| Frontend#8 | `UPDATE` | `M1-F5` | Retained; the 20+ case quota is replaced by the required security families and the email-link token assertion corrected to fragment handling. |
| Frontend#9 | `UPDATE` | `M2-F1` | Retained as the switcher; household added to query cache identity so switching cannot leak the prior household. |
| Frontend#10 | `UPDATE` | `M2-F2` | Retained as household creation; the required currency_code added and the invented name-length rule removed. |
| Frontend#11 | `UPDATE` | `M2-F3` | Retained as member and invitation management; invitation operations retargeted to the contract and revocation moved to invitation identifier. |
| Frontend#12 | `UPDATE` | `M2-F5` | Already targets the correct join operation; only uniform failure presentation is added. |
| Frontend#13 | `UPDATE` | `M2-F6` | Retained; the 15+ case quota is replaced by the mandatory invitation security scenarios. |
| Frontend#14 | `UPDATE` | `M3-F1` | Largely canon-consistent already, including permission-aware assignment; archived reference removed and accessibility requirements added. |
| Frontend#15 | `UPDATE` | `M3-F2` | Retained; the 20+ case quota is replaced by behaviour coverage plus accessibility and permission-loss cases. |
| Frontend#16 | `UPDATE` | `M4-F1` | Retained; the bulk-clear confirmation is required to state permanence and accessibility requirements are added. |
| Frontend#17 | `UPDATE` | `M4-F2` | Retained; the 15+ case quota is replaced by behaviour and invalidation coverage. |
| Frontend#18 | `UPDATE` | `M5-F1` | Retained as the expense page but corrected on money semantics: dollars-to-cents conversion replaced by exponent-aware amount_minor, and the missing incurred_on field added. |
| Frontend#19 | `UPDATE` | `M5-F2` | Retained; the 15+ case quota and the dollars-to-cents assertion are both replaced by exponent-aware formatting tests. |
| Frontend#20 | `UPDATE` | `M6-F1` | Retained; legacy FR and archived contract references replaced and below-one feedback required. |
| Frontend#21 | `UPDATE` | `M6-F2` | Retained; the 15+ case quota replaced by behaviour coverage. |
| Frontend#22 | `UPDATE` | `M7-F1` | Retained as the dashboard page; the five-task preview corrected to three, the complete pending count added, and as_of derived from the browser-local date. |
| Frontend#23 | `UPDATE` | `M8-F1` | Retained as the E2E suite; the 20+ case quota replaced by the release journeys and accessibility plus responsive verification added. |
| Frontend#24 | `UPDATE` | `M8-F2` | Retained as frontend performance work; the fixed bundle-size and Lighthouse thresholds are demoted from gates to reported observations. |
| Infrastructure#1 | `UPDATE` | `M0-I1` | Retained as the local database and runtime issue; absorbs the composition scope from Backend#4 and drops the inverted dependency on it. |
| Infrastructure#2 | `UPDATE` | `M0-I2` | Retained as the environment contract; kept provider-neutral with the D02 and D03 gates recorded. |
| Infrastructure#3 | `UPDATE` | `M9-I1` | Retained as production deployment; archived reference replaced, backup and restore added, and the D02/D04 gates recorded. |
| Infrastructure#4 | `UPDATE` | `M9-I2` | Retained as monitoring; the named vendor removed pending D02 and the redaction requirements added. |

## 7. Milestones

### 7.1 Naming authority

The canonical source map assigns milestone **outcomes, sequence and dependencies** to the implementation plan, and **current work, issue count, ownership and status** to live GitHub milestones. The roadmap is canonical for the product boundary and deferred-decision deadlines, not for milestone naming.

No canonical artifact claims authority over milestone *titles*. This report therefore proposes **no milestone renaming**. The cosmetic difference between the GitHub title `M2 - Household & Membership` and the plan's `M2 — Household, membership, and invitations` is recorded as OQ-1 rather than acted on.

### 7.2 Membership changes

One milestone reassignment is proposed:

- **Backend#34** (scheduled purge command) from **M8** to **M2**. The implementation plan lists "purged idempotently by a scheduled command" among the M2 household outcomes; M9 owns only the deployment scheduling, already covered by Infrastructure#3. Medium confidence — see OQ-4.

### 7.3 The empty Documentation M9 milestone

Documentation carries an M9 milestone with zero issues. Rather than closing it for being empty, the canon was searched for Documentation-owned M9 work:

- The implementation plan's M9 outcomes assign provisioning to Infrastructure and workflow entry points to Automation and the service repositories.
- The README ownership table assigns *production runbook implementation* to **Infrastructure**, not Documentation.
- Release acceptance requires operational documents but places them with the selected runtime, which is Infrastructure's boundary.
- The candidate draft lists no `M9-D` item; Documentation's candidates are M0 and M8 only.
- The roadmap's "additional operations detail" item is genuinely unassigned to a repository.

**Conclusion:** no canonical artifact places Documentation-owned work in M9, so closing the empty milestone is proposed — but at medium confidence, because the roadmap's unassigned operations-detail item could reasonably be argued into Documentation. Recorded as OQ-3. Closing a milestone is not deleting an issue and no issue is affected.

### 7.4 No empty milestone is created

Every proposed repository/milestone pair contains at least one candidate. Backend has no M9 and Frontend has no M9; neither is proposed, since neither repository owns M9 work.

## 8. Labels

> **OQ-9 resolved: this migration is deferred in full.** Phase 3 performs **no** label mutation — no creation, rename, application or removal. The inventory and mapping below are retained as advisory input to an independent later normalization pass. Current labels on all 69 issues are preserved exactly. Verification rule 12c enforces zero actionable label changes.

### 8.1 The actual situation

The premise that two label schemes compete in production is **incorrect**. The structured taxonomy (`area:*`, `type:*`, `priority:*`) is **defined in all five repositories but applied to zero issues**. All 69 issues carry only legacy free-form labels. This is one live scheme plus one dormant scheme.

No canonical label taxonomy exists anywhere in the Documentation repository. The proposal below is therefore an explicit reconciliation decision requiring approval, **not** a pre-existing requirement, and **nothing is applied in this phase**.

### 8.2 Definition inconsistencies

- Automation lacks `area:api`, `area:ci`, `area:dashboard` and `area:infrastructure`, which the other four repositories define — the dormant taxonomy is not even uniform.
- Backend alone defines `test-api` and `test-diagnostic`, both unused; they appear to be diagnostic residue.
- `priority:*` is defined in four repositories but not Automation, and is unused everywhere.

### 8.3 Proposed mapping

| Label | Repos | Uses | Disposition | Target | Rationale |
|---|---|---|---|---|---|
| `backend` | B | 34 | remove | — | Redundant: the repository already identifies the service. |
| `frontend` | F | 24 | remove | — | Redundant with the repository. |
| `infrastructure` | B,I | 5 | replace | `area:infrastructure` | Domain dimension; repo identity is implicit. |
| `automation` | A,B,F | 6 | remove | — | Redundant with the repository. |
| `testing` | B,F | 14 | replace | `type:test` | Work-type dimension. |
| `e2e` | F | 1 | replace | `type:test` | Test granularity belongs in the title, not a second test label. |
| `integration` | B | 1 | replace | `type:test` | Same as above. |
| `ui` | F | 10 | remove | — | Every Frontend feature issue is UI; carries no filter value. |
| `react` | F | 1 | remove | — | Framework is fixed by the technology baseline. |
| `routing` | F | 1 | remove | — | Too granular for a cross-repo taxonomy. |
| `context` | F | 1 | remove | — | Implementation detail. |
| `types` | F | 1 | replace | `area:api` | Generated types are contract work. |
| `household` | B,F | 10 | replace | `area:household` | Domain dimension. |
| `invitation` | B | 1 | replace | `area:household` | Invitations are part of the household domain. |
| `task` | B,F | 5 | replace | `area:tasks` | Domain dimension. |
| `shopping` | B,F | 5 | replace | `area:shopping` | Domain dimension. |
| `expense` | B,F | 5 | replace | `area:expenses` | Domain dimension. |
| `inventory` | B,F | 5 | replace | `area:inventory` | Domain dimension. |
| `dashboard` | B,F | 2 | replace | `area:dashboard` | Domain dimension. |
| `authentication` | B,F | 8 | replace | `area:auth` | Domain dimension. |
| `oauth` | B | 1 | replace | `area:auth` | Part of the identity domain. |
| `session` | B | 1 | replace | `area:auth` | Part of the identity domain. |
| `authorization` | B | 2 | replace | `security` | Authorization work is a security classification. |
| `email` | B | 3 | replace | `area:email` | ADR-015 makes transactional email a first-class concern spanning identity and household. |
| `api` | B,F | 9 | replace | `area:api` | Domain dimension. |
| `drf` | B | 1 | remove | — | Framework is fixed by the technology baseline. |
| `models` | B | 4 | remove | — | Implementation detail; area:* already locates the work. |
| `database` | B,I | 3 | replace | `area:infrastructure` | Folds into the infrastructure domain. |
| `docker` | A,B,I | 3 | replace | `area:infrastructure` | Folds into the infrastructure domain. |
| `deployment` | A,I | 2 | replace | `area:infrastructure` | Folds into the infrastructure domain. |
| `configuration` | I | 1 | replace | `area:infrastructure` | Folds into the infrastructure domain. |
| `monitoring` | I | 1 | replace | `area:infrastructure` | Folds into the infrastructure domain. |
| `ci-cd` | A,B,F | 4 | replace | `area:ci` | Domain dimension. |
| `setup` | A,B,F | 3 | replace | `type:chore` | Work-type dimension. |
| `launch` | A | 1 | replace | `type:chore` | Work-type dimension. |
| `documentation` | all | 3 | replace | `type:docs` | Work-type dimension; new label required. |
| `security` | B | 2 | retain | `security` | Cross-cutting classification the canon repeatedly requires. |
| `performance` | B,F | 2 | retain | `performance` | Cross-cutting classification; note that numeric gates remain deferred. |
| `high-priority` | B,F | 4 | replace | `priority:high` | Aligns with the structured priority dimension. |
| `test-api` | B | 0 | remove | — | Diagnostic residue; defined only in Backend, never applied. |
| `test-diagnostic` | B | 0 | remove | — | Diagnostic residue; defined only in Backend, never applied. |

Repository key: A=Automation, B=Backend, D=Documentation, F=Frontend, I=Infrastructure.

### 8.4 Labels proposed for addition

| Label | Rationale |
|---|---|
| `area:email` | Transactional email concern spanning identity and household invitations (ADR-015). New. |
| `type:docs` | Documentation work. New; replaces the free-form `documentation` label. |
| `architecture` | Work that changes or depends on an accepted ADR. New; applied sparingly. |
| `area:api / area:ci / area:dashboard / area:infrastructure in Automation` | These four area labels are defined in the other four repositories but missing from Automation, so the taxonomy is not uniform. |

GitHub's default labels (`bug`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`) are retained untouched in all five repositories.

### 8.5 Resulting dimensions

Four non-overlapping dimensions, plus two cross-cutting classifications:

- **`area:*`** — domain: `auth`, `household`, `tasks`, `shopping`, `expenses`, `inventory`, `dashboard`, `api`, `ci`, `infrastructure`, `email`.
- **`type:*`** — work type: `feature`, `chore`, `test`, `docs`.
- **`priority:*`** — `critical`, `high`, `medium`, `low`.
- **Cross-cutting** — `security`, `performance`, `architecture`.

Repository identity is not duplicated as a label, which is why `backend`, `frontend`, `automation` and the UI/framework labels are proposed for removal rather than mapping.

## 9. Dependencies

### 9.1 Current state

**Zero native GitHub dependencies exist.** `GET /repos/{repo}/issues/{n}/dependencies/blocked_by` returns `200 []` for all 69 issues. Every dependency in the backlog today is Markdown prose in a `## Dependencies` section, which is documentation and carries no enforcement.

### 9.2 Blocking versus ordering

Markdown references were **not** mechanically converted. Each was classified:

- **Blocking** — the work genuinely cannot complete without the prerequisite. Only these become proposed native `blocked_by` edges. **21 edges proposed.**
- **Ordering / informational** — sequencing preference or shared context, such as "All M0-M7 Backend issues" on a hardening issue. These stay as prose and are marked `native: false`. A blanket reference to a milestone's worth of issues is not a dependency; it is a milestone relationship, and GitHub already models that through the milestone itself.

### 9.3 Defects found in the declared graph

| Defect | Detail | Proposed fix |
|---|---|---|
| **Cycle** | Backend#8 declares a dependency on Backend#10 (email service) while Backend#10 declares a dependency on Backend#8. A two-node cycle. | The email adapter is the prerequisite. Remove the Backend#10 → Backend#8 edge; the auth operations depend on the adapter, not the reverse. |
| **Inverted** | Infrastructure#1 depends on Backend#4 for `docker-compose`, but Infrastructure owns full-stack composition. | Remove the edge; Infrastructure#1 absorbs the compose scope and instead depends on the two service-image candidates. |
| **Unresolvable** | "All M0-M7 Backend issues" (Backend#30, #31, #32) and "All previous milestones" (Automation#4, Infrastructure#3, #4) cannot be expressed as native edges. | Classify as ordering, retain as prose, and rely on milestone sequencing. |
| **Stale reference** | Frontend#2 cites Frontend#4 for generated types; the generated-types issue is Frontend#3. | Repoint to Frontend#3. |
| **Moved target** | Automation#3 depends on Backend#4 for compose. | Repoint to Infrastructure#1. |

The proposed blocking graph was checked for cycles and is **acyclic** ([]).

### 9.4 Native dependency API

The API is readable and the account holds admin on all five repositories. Two questions remain open until a single probe at the start of Phase 3:

1. the exact request body for `POST .../dependencies/blocked_by` — cross-repository edges are expected to use the numeric issue `id` (for example Backend#11 is `id=5164176311`) rather than the `#number`;
2. whether cross-repository edges are accepted at all in this organization.

**No issue will claim a native dependency that the API has not confirmed.** If an edge cannot be written, the mutation log will say so rather than reporting success.

## 10. Phase 2 — consistency validation

**26 checks pass, 0 canonical conflicts.**

| Check | Result | Detail |
|---|---|---|
| C1a every matrix-governed action has an OpenAPI operation | `PASS` | [] |
| C1b identity/session/CSRF operations excluded from the permissions check | `INFO` | 16 operations out of scope: changePassword, completeGoogleOAuth, getCsrfToken, getCurrentUser, login, logout, requestPasswordReset, requestPrimaryEmailChange, resendEmailVerificati… |
| C1c matrix-forbidden mutations have no writable contract surface | `PASS` | [] |
| C1d public household recovery and ownership transfer absent from the contract | `PASS` |  |
| C2a every canonical FR maps to at least one proposed candidate | `PASS` | 132 FRs; uncovered=[] |
| C2b covering candidates carry explicit acceptance criteria | `PASS` | 0 FRs whose covering candidates rely on retained live-issue criteria:  |
| C2c every coverage reference resolves | `PASS` | set() |
| C3a expense category enum matches the domain model | `PASS` | ['Food', 'Utilities', 'Maintenance', 'Entertainment', 'Other'] |
| C3b amount_minor is a positive integer in the contract | `PASS` |  |
| C3c amount_cents absent from the contract | `PASS` |  |
| C3d domain model states amount_cents is non-canonical | `PASS` |  |
| C3e DashboardResponse carries no expense or inventory field | `PASS` |  |
| C3f dashboard preview capped at three | `PASS` |  |
| C3g dashboard as_of is a required query parameter | `PASS` |  |
| C3h household create requires currency_code | `PASS` |  |
| C3i contract declares no 422 response | `PASS` | 422 appears only in the prose rule 'The API does not return 422' |
| C3j no google_id anywhere in the contract | `PASS` |  |
| C4a every supersession target exists | `PASS` | [] |
| C4b every supersession target is Accepted | `PASS` | [] |
| C4c supersession graph is acyclic | `PASS` | [] |
| C4d superseded ADRs name a successor | `INFO` | ADR-001-multi-repository-structure.md=Superseded, ADR-004-session-based-authentication.md=Superseded |
| C5a no proposal introduces a roadmap non-goal | `PASS` | [] |
| C6a no candidate selects a D02-deferred vendor | `PASS` | [] |
| C6b no candidate fixes a D01 constant in acceptance criteria | `PASS` | [] |
| C6c no candidate asserts an unqualified performance or coverage gate | `PASS` | [] |
| C6d no candidate asserts a numeric test-count quota | `PASS` | [] |
| C7a no proposed content restates a contract schema | `PASS` | [] |
| C8a proposed blocking-dependency graph is acyclic | `PASS` | [] |
| C8b blocking edges proposed | `INFO` | 21 edges across 24 nodes |

### 10.1 No canonical conflict found

No genuine disagreement between two accepted canonical documents was found in any audited area. Consequently no issue is parked, and no documentation change is proposed. The corpus governs itself through artifact-specific authority rather than a "newest document wins" rule, and every supersession is explicit:

- ADR-001 → ADR-009 (full); ADR-004 → ADR-011 (full);
- ADR-002 → ADR-010 (Django-version portion only); ADR-005 → ADR-012 (ownership/error/integrity portions); ADR-007 → ADR-011 (cookie/CSRF/registry/revocation portions); ADR-008 → ADR-012 (same-household enforcement claim only).

Each partially superseded ADR names both its successor and the exact portion superseded, so no reader can mistake a retained decision for a replaced one.

### 10.2 Requirement coverage

All **132** canonical `*-FR-nnn` requirements across the eight PRDs trace to at least one proposed candidate carrying objectively verifiable acceptance criteria. Coverage is many-to-one by design: no dedicated issue per requirement is required or proposed.

### 10.3 Scope of the permissions check

The permissions-matrix ↔ OpenAPI check covers the **37** operations the matrix actually governs, out of **53** total. The remaining **16** are technical identity, session, CSRF and email-verification operations that the matrix deliberately does not govern; they are validated against ADR-011 and the security model instead and are **not** flagged for lacking a household-permission row.

Actions the matrix marks unavailable were confirmed to have no writable contract surface: `HouseholdUpdateRequest` exposes only `name` and `description`, and `ExpenseUpdateRequest` exposes neither `payer_id` nor any currency field. No public recovery or ownership-transfer operation exists.

## 11. Frozen decisions

All nine open questions were resolved by project decision on 2026-08-17. They are frozen for Phase 3 and recorded in the matrix under `frozen_decisions`, so the mutation is reproducible from the artifact alone. **No open question remains, and every candidate is now high confidence.**

| OQ | Subject | Decision | Phase 3 effect |
|---|---|---|---|
| **OQ-1** | Milestone naming authority | Do not rename any milestone. All current GitHub milestone titles remain unchanged. The canon establishes no naming authority and title normalization is outside this reconciliation. | 0 milestone renames. |
| **OQ-2** | Documentation#1 disposition | Keep Documentation#1 and UPDATE it, narrowing scope to the remaining canonical OpenAPI publication, validation and CI contract work. | Documentation#1 updated in place; no closure; no new issue. |
| **OQ-3** | Empty Documentation M9 milestone | Defer. The empty Documentation M9 milestone stays open and unchanged. No M9 Documentation candidate is created and the milestone is not closed. | 0 milestone closures; 0 new candidates. |
| **OQ-4** | Backend#34 milestone | Move Backend#34 from M8 to M2. | 1 milestone reassignment. |
| **OQ-5** | Automation build-asset boundary | Automation owns a reusable callable build asset; service repositories own invocation and execution. No registry or provider is selected before D02. | Automation#1 scope and acceptance criteria rewritten. |
| **OQ-6** | Session/registry issue boundary | Session configuration, the indexed registry, rotation and the revocation matrix stay together in Backend#7 / M1-B2. | No split; candidate count unchanged. |
| **OQ-7** | Expense category visualization | Require the total and per-category expense totals. Neither require nor forbid a chart; visual presentation remains a design decision. | Frontend#18 acceptance criteria state totals only. |
| **OQ-8** | Household support-recovery mechanism | Explicitly defer the implementation mechanism. M2-B7 specifies only canonical, objectively verifiable outcomes: support/admin-only recovery within retention, restoration of access and state, idempotency and auditability. No public or internal API is introduced and no management-command or Django-admin implementation is chosen here. | M2-B7 created with outcome-only criteria. |
| **OQ-9** | Label taxonomy | Defer the structured-label migration entirely. Phase 3 performs no label mutation. Current labels are preserved exactly. Taxonomy normalization is an independent later pass. | 0 label creations, renames, applications or removals. |

Three decisions defer work out of this reconciliation entirely — **OQ-1** (milestone naming), **OQ-3** (empty Documentation M9 milestone) and **OQ-9** (label taxonomy). Each is separable and none blocks the backlog correction.

**OQ-9 has the largest effect.** The proposed organization-wide label migration is not executed. Every candidate's actionable `label_changes.add` and `label_changes.remove` are empty; the proposal survives only under `proposed_add` / `proposed_remove`, flagged advisory by `label_migration_status.deferred`. Current labels on all 69 issues are preserved exactly. Verification rule 12c enforces this — Phase 3 cannot mutate a label without failing preflight.

**OQ-8** keeps `M2-B7` outcome-only: support/admin-only recovery within retention, restoration of access and state, idempotency, and auditability. No public or internal API is introduced and no management-command or Django-admin implementation is chosen. Verification rule 12k scans its criteria for mechanism language and fails if any appears.

Six candidates carry a `decided_by` reference recording which decision determined them: `M0-A1` (OQ-5), `M0-D1` (OQ-2), `M1-B2` (OQ-6), `M2-B7` (OQ-8), `M2-B10` (OQ-4), `M5-F1` (OQ-7).

### Confidence after freezing

**75 high, 0 medium, 0 low.** Before freezing, six candidates were medium because a decision was outstanding. `high` now covers two provenances: a correction that follows directly from a cited canonical rule, and a correction determined by an approved decision recorded above. The `decided_by` field distinguishes them, so canonical authority is never confused with project choice.

## 11A. Phase 3 mutation counts

Exact, frozen. Anything not listed is zero.

| Mutation | Count |
|---|---|
| Issues updated in place, number preserved | 69 |
| — of which narrowed as SPLIT sources | 3 |
| New issues from `CREATE` candidates | 3 |
| New issues from `SPLIT` successors | 3 |
| **Total new issues** | **6** |
| Issues closed | 0 |
| Issues deleted | 0 |
| Milestone reassignments | 1 |
| Milestone renames — OQ-1 deferred | 0 |
| Milestone closures — OQ-3 deferred | 0 |
| Milestones created | 0 |
| Label mutations of any kind — OQ-9 deferred | 0 |
| Native `blocked_by` edges, pending Gate E | 21 |
| Invalid Markdown dependency references removed | 4 |

Backlog after Phase 3: **69 existing + 6 new = 75 issues.** All 69 existing numbers preserved; none closed, none deleted.

### The 6 new issues

| Candidate | Repo | MS | Origin | Title |
|---|---|---|---|---|
| `M1-F3` | Frontend | M1 | `CREATE` — no live issue | Implement Google login and explicit reauthenticated account linking/unlinking |
| `M2-B7` | Backend | M2 | `CREATE` — no live issue | Implement household soft-delete recovery and the support/administration path |
| `M2-F4` | Frontend | M2 | `CREATE` — no live issue | Implement the invitation fragment landing, exchange and verified acceptance flow |
| `M1-B4` | Backend | M1 | `SPLIT` successor of Backend#8 | Implement the email verification and primary-email change lifecycle |
| `M1-B5` | Backend | M1 | `SPLIT` successor of Backend#8 | Implement enumeration-safe password recovery and authenticated password change |
| `M2-B5` | Backend | M2 | `SPLIT` successor of Backend#14 | Implement invitation verifier exchange, safe preview and explicit acceptance |

### The 1 milestone reassignment

**Backend#34** — `M8` → `M2` (OQ-4). The implementation plan places the idempotent scheduled purge among M2 household outcomes; M9 retains only the deployment scheduling, already covered by Infrastructure#3. Backend M8 keeps 3 candidates; Backend M2 rises to 10.

## 12. Verification results

Both suites were executed against live GitHub state after the matrix was generated.

| # | Invariant | Result |
|---|---|---|
| 1a | Candidate identifiers unique | PASS — 75 unique |
| 1b | Exactly one valid action per candidate | PASS |
| 2a | All 69 live issues present exactly once | PASS |
| 2b | Exactly one valid disposition per live issue | PASS |
| 2c | Live set matches the GitHub snapshot | PASS |
| 3a | Candidate→issue and issue→candidate mappings agree bidirectionally | PASS |
| 3b | Every issue reference resolves to a real candidate | PASS |
| 4a | CREATE candidates have no live issues | PASS — 3 candidates |
| 4b | closure_kind valid and exclusive to CLOSE_SUPERSEDED | PASS |
| 4c | CLOSE_SUPERSEDED count | INFO — 0 |
| 5a | confidence is exactly high | medium | low | PASS |
| 5b | Every low-confidence candidate files an open question | PASS — vacuous, 0 low |
| 6a | No archived document cited as a normative source | PASS |
| 6b | Archived names in drift/supersession context | INFO — 22, all permitted |
| 7a | Candidate action counts match the summary | PASS |
| 7b | Live disposition counts match the summary | PASS |
| 8a | GitHub still returns exactly the 69 audited issues | PASS |
| 8b | Every audited issue is still open | PASS |
| 9a | No native dependency was written | PASS — all 69 return [] |
| 9b | No issue modified during this session (updated_at predates it) | PASS |
| 9c | Label sets match the Phase 0 inventory | PASS |
| 9d | Milestone sets match the Phase 0 inventory | PASS |
| 9e | Every inventoried label exists in GitHub | PASS |
| 10a | No proposed milestone is empty | PASS |

**22 passed, 0 failed, 3 informational** on the matrix suite; **26 passed, 0 conflicts, 0 warnings, 3 informational** on the consistency suite.

The no-mutation invariant is evidenced three ways: no native dependency exists on any of the 69 issues; every issue's `updated_at` predates this session, and any GitHub write of any kind would have bumped it; and label and milestone sets are byte-identical to the Phase 0 inventory.

## 13. Phase 3 readiness

Not executed. When approved, the mutation sequence is:

1. probe the native dependency API with one edge and read it back;
2. apply label taxonomy changes (additions first, then re-labelling, then removals of now-unused labels);
3. apply milestone membership changes (Backend#34 to M2);
4. update the 66 `UPDATE` issues in place, preserving their numbers;
5. create the 6 `SPLIT` successor issues and the 3 `CREATE` issues, then narrow the 3 split sources;
6. write native `blocked_by` edges and read each back;
7. close the empty Documentation M9 milestone if OQ-3 is approved.

Updated bodies use the agreed structure — `# Summary`, `## Scope`, `## Acceptance Criteria`, `## Dependencies`, `## PRD References`, `## OpenAPI References`, `## Architecture / ADR References` — including only the sections that apply. Bodies **reference** OpenAPI operation identifiers and PRD requirement identifiers for traceability and never restate request, response or schema contracts, which would create the competing inventory ADR-014 forbids.

Phase 4 then re-reads GitHub and verifies existence, absence of duplicates, titles, repository ownership, milestone assignment, labels, state, real native dependencies, cross-repository correctness and the absence of cycles.

## 14. Appendix A — complete structural records

Every record below shows both directions of the mapping. `primary` marks the contributor whose GitHub issue number the candidate inherits; a candidate with no primary is created new in Phase 3.

### A.1 SPLIT candidates (6)

#### `M0-B4` — Add the Backend service Dockerfile and local runtime configuration

- **Milestone / repo:** M0 / Backend
- **Action:** `SPLIT`   **Confidence:** high   **Draft lineage:** `M0-B4`
- **Forward → live issues:** Backend#4 (`primary`)
- **Reverse ← live issues:** Backend#4 disposition `SPLIT` → `M0-B4`, `M0-I1`
- **Issue number inherited:** Backend#4
- **Sources:** `architecture/technology-baseline.md`, `architecture/adr/ADR-009-five-repository-topology.md`, `architecture/overview.md`

**Detected drift**

- Backend#4 owns the full-stack docker-compose covering django, react and postgres. The technology baseline assigns local full-stack orchestration to Infrastructure, consuming service-owned images; ADR-009 requires service repositories to keep service-specific Dockerfiles and forbids Infrastructure becoming a duplicate source for them.
- Scope includes a Dockerfile for React, which belongs to Frontend.

**Proposed correction**

Split by ownership. This candidate keeps only the Backend service Dockerfile, .dockerignore and local runtime configuration in the Backend repository. The compose/orchestration half moves to M0-I1 in Infrastructure, and the React image to M0-F1 in Frontend.

**Acceptance criteria**

- [ ] The Backend Dockerfile builds and runs the service independently of any compose file.
- [ ] The Backend repository contains no full-stack compose definition.

**Dependencies**

- remove: Frontend#1 (React scaffold) — no longer needed once the React image leaves this issue
- native `blocked_by` (intent): `Backend#1`

#### `M1-B3` — Implement CSRF bootstrap, signup, login, logout and current-user operations

- **Milestone / repo:** M1 / Backend
- **Action:** `SPLIT`   **Confidence:** high   **Draft lineage:** `M1-B3`
- **Forward → live issues:** Backend#8 (`primary`)
- **Reverse ← live issues:** Backend#8 disposition `SPLIT` → `M1-B3`, `M1-B4`, `M1-B5`
- **Issue number inherited:** Backend#8
- **Sources:** `api/openapi.yaml`, `api/README.md`, `architecture/adr/ADR-011-identity-and-session-security.md`, `product/prds/prd-identity-authentication.md`, `product/roadmap.md`

**Detected drift**

- Backend#8 bundles credential auth, email verification and password recovery into one issue while omitting the CSRF bootstrap and every email-lifecycle operation the contract defines.
- Hard-codes D01 constants: minimum password length 10 with complexity, 5 logins/min per IP, 3 resets/hour per email, 1-hour reset token.
- Acceptance criteria admit status 422, which the contract never uses.
- References the archived OPENAPI.md.

**Proposed correction**

Split Backend#8 along contract operation groups. This candidate covers the CSRF bootstrap plus signup, login, logout and current-user operations. Remove all D01 constants and reference the decision instead; safe launch defaults are selected before implementation, then reviewed and locked at M8. Remove 422 from the error set.

**Acceptance criteria**

- [ ] Operations getCsrfToken, signup, login, logout and getCurrentUser behave as the contract defines.
- [ ] Unsafe requests, including operations declaring security: [], require X-CSRFToken.
- [ ] Error responses use 400/401/403/404/409 only; no 422 is returned.
- [ ] No password-policy or rate-limit constant is fixed in the issue; D01 governs the values.

#### `M1-B4` — Implement the email verification and primary-email change lifecycle

- **Milestone / repo:** M1 / Backend
- **Action:** `SPLIT`   **Confidence:** high   **Draft lineage:** `M1-B3`
- **Forward → live issues:** Backend#8 (`split_source`)
- **Reverse ← live issues:** Backend#8 disposition `SPLIT` → `M1-B3`, `M1-B4`, `M1-B5`
- **Issue number inherited:** **none — new issue created in Phase 3**
- **Sources:** `api/openapi.yaml`, `product/prds/prd-identity-authentication.md`, `architecture/adr/ADR-011-identity-and-session-security.md`, `security/security-model.md`

**Detected drift**

- No live issue covers verifyEmail, resendEmailVerification, requestPrimaryEmailChange or verifyPrimaryEmailChange, all of which the contract defines and IA-FR-003/004 require.

**Proposed correction**

Create the verification lifecycle as its own unit: verify, rate-limited resend, and the primary-email change request/verify pair. Primary-email change requires recent reauthentication, rotates the current session and revokes all others. Verification credentials are bearer material and never appear in a server-visible path or query.

**Acceptance criteria**

- [ ] An unverified account can reach only the verification lifecycle; every other operation is denied.
- [ ] Resend is rate-limited and leaves recoverable pending state when provider submission fails.
- [ ] Primary-email change requires recent reauthentication, rotates the current session and revokes all others.
- [ ] No verification credential appears in a request path, query string, log, referrer or persistent browser storage.

**Dependencies**

- native `blocked_by` (intent): `M1-B1`, `M1-B2`, `M1-B7`

#### `M1-B5` — Implement enumeration-safe password recovery and authenticated password change

- **Milestone / repo:** M1 / Backend
- **Action:** `SPLIT`   **Confidence:** high   **Draft lineage:** `M1-B3`
- **Forward → live issues:** Backend#8 (`split_source`)
- **Reverse ← live issues:** Backend#8 disposition `SPLIT` → `M1-B3`, `M1-B4`, `M1-B5`
- **Issue number inherited:** **none — new issue created in Phase 3**
- **Sources:** `api/openapi.yaml`, `product/prds/prd-identity-authentication.md`, `security/security-model.md`, `architecture/adr/ADR-011-identity-and-session-security.md`, `product/roadmap.md`

**Detected drift**

- Backend#8 fixes the reset token at 32 bytes with SHA-256 and a 1-hour expiry and sets reset rate limits; these are D01 constants.
- Enumeration safety is not stated as a requirement, and the security model additionally requires that response timing not disclose whether a provider call occurred.
- The changePassword operation is absent.

**Proposed correction**

Separate recovery and change into their own unit. Reset requests return an enumeration-safe result in body, status and observable timing regardless of account existence or provider outcome. Reset credentials are time-limited, single-use, stored only as a hash and never retained in plaintext. Successful reset revokes every session; authenticated change preserves/rotates the current session and revokes all others. Defer the exact constants to D01.

**Acceptance criteria**

- [ ] Reset requests are indistinguishable in body, status and observable timing for existing and non-existing accounts.
- [ ] A reset credential is single-use and invalidated after use; plaintext is never persisted.
- [ ] Successful reset revokes every session; authenticated change revokes all sessions except the rotated current one.

**Dependencies**

- native `blocked_by` (intent): `M1-B1`, `M1-B2`, `M1-B7`

#### `M2-B4` — Implement the invitation model and owner lifecycle operations

- **Milestone / repo:** M2 / Backend
- **Action:** `SPLIT`   **Confidence:** high   **Draft lineage:** `M2-B4`
- **Forward → live issues:** Backend#14 (`primary`)
- **Reverse ← live issues:** Backend#14 disposition `SPLIT` → `M2-B4`, `M2-B5`
- **Issue number inherited:** Backend#14
- **Sources:** `architecture/adr/ADR-013-invitation-security.md`, `product/prds/prd-household-membership-invitations.md`, `architecture/domain-model.md`, `api/openapi.yaml`, `security/security-model.md`, `product/permissions-matrix.md`

**Detected drift**

- Invitation creation is routed through POST /households/{id}/members; the contract defines POST /households/{household_id}/invitations.
- Revocation is DELETE /households/{id}/invitations/{token} — revocation by bearer token. HH-FR-016 and ADR-013 require revocation by non-secret invitation identifier.
- Resend is absent although the contract defines it and resend must rotate the verifier and invalidate the prior generation and any intent bound to it.
- The model omits token generation/version identity, without which rotation cannot invalidate an already-exchanged intent.
- Acceptance criteria cite the archived DOMAIN_MODEL_CORRECTED.md.

**Proposed correction**

Split Backend#14 into owner lifecycle and invitee handoff. This candidate covers the model and the owner-facing operations: create, list, revoke by invitation identifier and resend. Add token generation/version identity to the model. Resend rotates the verifier and invalidates both the prior verifier and any server-side intent bound to the old generation; ADR-013 marks an in-place hash replacement that leaves an old intent valid as nonconforming.

**Acceptance criteria**

- [ ] Invitations are created and listed through the contract's invitation operations, not through the members operation.
- [ ] Revocation addresses the invitation by its non-secret identifier; no operation accepts a bearer token in a path.
- [ ] Resend rotates the verifier and invalidates the previous verifier and every intent bound to the previous generation.
- [ ] At most one pending invitation exists per household and normalized email, and an active member cannot be invited again.
- [ ] Only a cryptographic hash of the verifier is stored; expiry is 30 days from the current issuance or resend.

#### `M2-B5` — Implement invitation verifier exchange, safe preview and explicit acceptance

- **Milestone / repo:** M2 / Backend
- **Action:** `SPLIT`   **Confidence:** high   **Draft lineage:** `M2-B4`
- **Forward → live issues:** Backend#14 (`split_source`)
- **Reverse ← live issues:** Backend#14 disposition `SPLIT` → `M2-B4`, `M2-B5`
- **Issue number inherited:** **none — new issue created in Phase 3**
- **Sources:** `architecture/adr/ADR-013-invitation-security.md`, `security/security-model.md`, `product/prds/prd-household-membership-invitations.md`, `api/openapi.yaml`, `product/permissions-matrix.md`, `quality/release-acceptance.md`

**Detected drift**

- Backend#14 accepts invitations at POST /households/{id}/invitations/{token}/accept, placing the bearer token in a server-visible path. ADR-013 and the security model forbid this; the contract replaces it with exchangeInvitationVerifier, previewPendingInvitation and acceptPendingInvitation.
- No non-secret, generation-bound session intent; the flow as written cannot survive signup, login, verification and session rotation.
- No verified-email equality revalidation before preview or acceptance.
- 'Accepting valid token creates Membership' skips the required explicit acceptance step and the safe preview.

**Proposed correction**

Implement the three-step handoff the canon requires. Exchange accepts the verifier in a rate-limited POST body and stores only a non-secret invitation reference bound to the validated verifier generation; exchange alone grants no membership and no preview. After authentication and verified-email confirmation the server revalidates existence, expiry, revocation, rotation and consumption plus normalized verified-email equality, then returns only the approved safe preview. Acceptance is explicit and atomically creates at most one Membership while consuming the invitation. Duplicate Membership uses 409.

**Acceptance criteria**

- [ ] The verifier is accepted only in a POST body and never in a path or query.
- [ ] Exchange stores a non-secret invitation reference plus generation binding, never the verifier itself.
- [ ] The intent survives signup, login, verification and session rotation in the same browser, and becomes unusable after resend rotation or revocation.
- [ ] Preview is returned only after authentication, verification and normalized verified-email equality.
- [ ] Acceptance is atomic, single-use, and rejects replay of a consumed verifier; a duplicate Membership returns 409.

**Dependencies**

- native `blocked_by` (intent): `M2-B4`, `M1-B1`, `M1-B2`

### A.2 MERGE candidate (1)

#### `M0-I1` — Define the local PostgreSQL and full-stack runtime composition boundary

- **Milestone / repo:** M0 / Infrastructure
- **Action:** `MERGE`   **Confidence:** high   **Draft lineage:** `M0-I1`
- **Forward → live issues:** Infrastructure#1 (`primary`), Backend#4 (`split_source`)
- **Reverse ← live issues:** Infrastructure#1 disposition `UPDATE` → `M0-I1`; Backend#4 disposition `SPLIT` → `M0-B4`, `M0-I1`
- **Issue number inherited:** Infrastructure#1
- **Sources:** `architecture/technology-baseline.md`, `architecture/adr/ADR-009-five-repository-topology.md`, `architecture/overview.md`, `planning/mvp-implementation-plan.md`

**Detected drift**

- Infrastructure#1 declares a dependency on Backend#4 for docker-compose, inverting the canonical ownership: Infrastructure owns local full-stack orchestration and Backend owns only its service image.
- The compose definition currently lives in Backend#4.

**Proposed correction**

Absorb the full-stack compose scope from Backend#4 into Infrastructure, which the technology baseline names as the owner of local full-stack orchestration consuming service-owned images. Remove the inverted dependency on Backend#4 and replace it with dependencies on the two service Dockerfile candidates. PostgreSQL 14+ is the approved family; the exact deployed version stays with Infrastructure configuration.

**Acceptance criteria**

- [ ] A single Infrastructure-owned compose definition brings up PostgreSQL plus the Backend and Frontend service images.
- [ ] No compose definition remains in the Backend repository.
- [ ] Data persists across container restarts and the schema is created by Django migrations.

**Dependencies**

- remove: Infrastructure#1 → Backend#4 (inverted ownership dependency)
- native `blocked_by` (intent): `Backend#4 (service image)`, `Frontend#1 (service image)`

### A.3 CREATE candidates (3)

#### `M1-F3` — Implement Google login and explicit reauthenticated account linking/unlinking

- **Milestone / repo:** M1 / Frontend
- **Action:** `CREATE`   **Confidence:** high   **Draft lineage:** `M1-F3`
- **Forward → live issues:** none (`CREATE`)
- **Reverse ← live issues:** none — no existing issue references this candidate
- **Issue number inherited:** none — new issue created in Phase 3
- **Sources:** `product/prds/prd-identity-authentication.md`, `architecture/adr/ADR-011-identity-and-session-security.md`, `security/security-model.md`, `api/openapi.yaml`, `quality/release-acceptance.md`

**Detected drift**

- No live Frontend issue covers explicit account linking or unlinking. Frontend#6 provides only a Google login button, leaving IA-FR-008, the linking journey and the unlink operation unrepresented.

**Proposed correction**

Add the Frontend half of collision-safe linking: a Google login entry point, a collision path that explains why automatic linking did not occur, an explicit connect action gated on recent reauthentication, and an unlink action with the same gate. Communicate that other sessions are revoked.

**Acceptance criteria**

- [ ] A colliding Google identity presents an explicit link path and never silently merges accounts.
- [ ] Link and unlink both prompt for recent reauthentication before submission.
- [ ] The user is told that linking or unlinking ends their other sessions.

**Dependencies**

- native `blocked_by` (intent): `Backend#9`, `Frontend#5`

#### `M2-B7` — Implement household soft-delete recovery and the support/administration path

- **Milestone / repo:** M2 / Backend
- **Action:** `CREATE`   **Confidence:** high   **Draft lineage:** none
- **Forward → live issues:** none (`CREATE`)
- **Reverse ← live issues:** none — no existing issue references this candidate
- **Issue number inherited:** none — new issue created in Phase 3
- **Sources:** `product/prds/prd-household-membership-invitations.md`, `architecture/domain-model.md`, `architecture/adr/ADR-012-ownership-and-authorization.md`, `quality/release-acceptance.md`, `architecture/overview.md`

**Detected drift**

- HH-FR-034 requires support/administration recovery of a soft-deleted household within the 30-day window, restoring the preserved household, Memberships and resources to active normal access. Release Journey 13 requires that recovery be demonstrated and idempotent. No live issue covers it: Backend#11 covers only the soft-delete marker and Backend#34 only the purge.

**Proposed correction**

Add the missing middle of the deletion lifecycle: an administrative recovery path that restores a soft-deleted household and its preserved children to normal access, is idempotent, refuses households already purged, and emits the critical audit events the security model requires.

**Acceptance criteria**

- [ ] Recovery within the retention window restores the household, its Memberships and its resources to normal access.
- [ ] Recovery is idempotent and safe to retry.
- [ ] Recovery is unavailable as a public product action for owners and members.
- [ ] Delete, recovery and purge each emit a critical audit event containing no sensitive payload.

**Dependencies**

- native `blocked_by` (intent): `M2-B1`, `M2-B9`

#### `M2-F4` — Implement the invitation fragment landing, exchange and verified acceptance flow

- **Milestone / repo:** M2 / Frontend
- **Action:** `CREATE`   **Confidence:** high   **Draft lineage:** `M2-F4`
- **Forward → live issues:** none (`CREATE`)
- **Reverse ← live issues:** none — no existing issue references this candidate
- **Issue number inherited:** none — new issue created in Phase 3
- **Sources:** `architecture/adr/ADR-013-invitation-security.md`, `security/security-model.md`, `product/prds/prd-household-membership-invitations.md`, `api/openapi.yaml`, `quality/release-acceptance.md`

**Detected drift**

- No live Frontend issue covers the invitation landing page. ADR-013's landing-page protections, the fragment handling rules and the explicit-acceptance flow are entirely unrepresented in the backlog, although release Journey 2 depends on them.

**Proposed correction**

Add the invitee-facing flow: read the verifier from the URI fragment, remove it from browser-visible navigation state immediately, never write it to localStorage or sessionStorage, exchange it through a rate-limited POST body, and discard the raw value. Serve the landing route with a restrictive Content Security Policy, Referrer-Policy: no-referrer and Cache-Control: no-store, and admit no third-party script that could observe the fragment. After authentication and verification, render only the safe preview and require an explicit acceptance action.

**Acceptance criteria**

- [ ] The verifier never appears in a request path or query, in browser history, in storage, in telemetry or in error context.
- [ ] The fragment is removed from navigation state before any other script runs.
- [ ] The landing response carries a restrictive CSP, Referrer-Policy: no-referrer and Cache-Control: no-store.
- [ ] Acceptance requires an explicit user action after the safe preview; the preview alone creates no membership.
- [ ] The flow completes after signup, login, verification and session rotation in the same browser without reopening the link.

**Dependencies**

- native `blocked_by` (intent): `Backend#14`, `Frontend#5`

### A.4 Live issues with `SPLIT` disposition (3)

#### Backend#4

- **Disposition:** `SPLIT`
- **Forward → candidates:** `M0-B4`, `M0-I1`
- **Reverse ← candidates:** `M0-B4` lists Backend#4 as `primary`; `M0-I1` lists Backend#4 as `split_source`
- **Number retained by:** `M0-B4`
- **New issues created:** `M0-I1`

Bundles the Backend service Dockerfile with a full-stack docker-compose covering React and PostgreSQL. Ownership splits: the Backend image stays here, the composition moves to Infrastructure per the technology baseline and ADR-009, and the React image moves to Frontend.

#### Backend#8

- **Disposition:** `SPLIT`
- **Forward → candidates:** `M1-B3`, `M1-B4`, `M1-B5`
- **Reverse ← candidates:** `M1-B3` lists Backend#8 as `primary`; `M1-B4` lists Backend#8 as `split_source`; `M1-B5` lists Backend#8 as `split_source`
- **Number retained by:** `M1-B3`
- **New issues created:** `M1-B4`, `M1-B5`

Bundles credential auth, verification and recovery while omitting the CSRF bootstrap and every email-lifecycle operation the contract defines. Splits along contract operation groups so each unit has verifiable boundaries; D01 constants and status 422 removed throughout.

#### Backend#14

- **Disposition:** `SPLIT`
- **Forward → candidates:** `M2-B4`, `M2-B5`
- **Reverse ← candidates:** `M2-B4` lists Backend#14 as `primary`; `M2-B5` lists Backend#14 as `split_source`
- **Number retained by:** `M2-B4`
- **New issues created:** `M2-B5`

Encodes the superseded /invitations/{token}/accept workflow and revocation by bearer token. Splits into owner lifecycle (create, list, revoke by identifier, resend with rotation) and the invitee handoff (exchange, safe preview, explicit acceptance) that ADR-013 and the contract require.

## 15. Appendix B — identity and session gap coverage

The Phase 1 audit flagged two clusters of canonical identity work that no live issue covered. Both are now fully assigned. The table maps each contract operation to the candidate that owns it and the issue number that will carry it.

### B.1 Email verification, change, password and CSRF lifecycle

| Contract operation | Candidate | Issue | Origin |
|---|---|---|---|
| `getCsrfToken` | `M1-B3` | Backend#8 (number retained) | was absent from Backend#8's scope |
| `signup` | `M1-B3` | Backend#8 (number retained) | already present |
| `login` | `M1-B3` | Backend#8 (number retained) | already present |
| `logout` | `M1-B3` | Backend#8 (number retained) | already present |
| `getCurrentUser` | `M1-B3` | Backend#8 (number retained) | already present |
| `verifyEmail` | `M1-B4` | new issue | gap — no live issue covered it |
| `resendEmailVerification` | `M1-B4` | new issue | gap |
| `requestPrimaryEmailChange` | `M1-B4` | new issue | gap |
| `verifyPrimaryEmailChange` | `M1-B4` | new issue | gap |
| `requestPasswordReset` | `M1-B5` | new issue | was in Backend#8 carrying D01 constants |
| `resetPassword` | `M1-B5` | new issue | was in Backend#8 carrying D01 constants |
| `changePassword` | `M1-B5` | new issue | gap — absent from every live issue |

`M1-B3` inherits Backend#8's number; `M1-B4` and `M1-B5` are created in Phase 3. Frontend counterparts are `M1-F2` (verification screens, reset bearer moved to the URI fragment) and `M1-F4` (verified-identity route gating).

### B.2 Indexed user-session registry and revocation matrix

Owned entirely by **`M1-B2`**, which retains **Backend#7**'s number (disposition `UPDATE`). Backend#7 previously covered only session configuration and specified `SameSite=Strict`, which ADR-011 contradicts.

| Revocation event | Required server-side result |
|---|---|
| Normal logout | Revoke the current session only |
| Password reset | Revoke every session for the account |
| Authenticated password change | Preserve/rotate current; revoke all others |
| Primary-email change | Recent reauthentication; rotate current; revoke all others |
| OAuth link or unlink | Recent reauthentication; rotate current; revoke all others |
| Account disable or soft deletion | Revoke every session immediately |
| Account restoration | Fresh authentication; never restore old sessions |

`M1-B2` also carries the indexed registry itself (IA-FR-013 — revocation without decoding or scanning session payloads, and no device-management UI), session rotation at authentication and identity-security boundaries, the `SameSite=Lax` correction, the readable CSRF cookie, and preservation of the non-secret invitation intent across rotation (ADR-013).

Events are *triggered* from the operations owned by `M1-B5` (reset, change), `M1-B4` (email change) and `M1-B6` (link/unlink), so those candidates declare `M1-B2` as a blocking dependency. See OQ-6 on whether `M1-B2` should itself be split.

