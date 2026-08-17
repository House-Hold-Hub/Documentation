# Backlog reconciliation execution log

> **Status:** Draft
> **Owner:** Documentation repository
> **Last reviewed:** 2026-08-17
> **Canonical for:** Nothing — this is an operational record, not a requirement source
> **Purpose:** Append-only record of actions taken during the reconciliation between the canonical
> documentation and the live GitHub backlog, with the commit SHAs that anchor them.

## Commit anchors

| Role | SHA | Short |
|---|---|---|
| Canonical documentation baseline | `3006cae70caba1829d0ad8cfcc9b17af5791f052` | `3006cae` |
| Reconciliation artifacts (pre-freeze) | `870385e461b632b6a02f08300ff75242fb9e9d40` | `870385e` |
| **Frozen matrix — Phase 3 executes from this** | `086831d65d2a5d5dbd0c441ed3c1e4d9481a5ea8` | `086831d` |

Any Phase 3 mutation must cite `086831d` as the exact matrix revision it executed from, and
`3006cae` as the canonical documentation it was derived from. `870385e` is retained for traceability
as the pre-freeze artifact commit, but **must not** be used as the execution source: it predates the
nine frozen decisions and still carries the label migration that OQ-9 deferred.

Both commits are on `main` in `House-Hold-Hub/Documentation` and are present on `origin`. Neither has
been amended, rebased, or force-pushed.

## Entry 1 — Phase 0: reference capture

- Read the complete non-archived canonical corpus: 8 PRDs, permissions matrix, domain model,
  architecture overview, technology baseline, 15 ADRs, `api/openapi.yaml` and API conventions,
  security model, testing strategy, release acceptance, roadmap, implementation plan, and the Draft
  candidate issue decomposition.
- Captured all 69 live issues across the five repositories with number, title, state, milestone,
  labels and body.
- Captured label and milestone inventories per repository.
- Probed the native GitHub dependency API: readable, and zero dependencies exist.

**Mutations:** none. Read-only (`GET`) requests only.

## Entry 2 — Phase 1: audit

- Classified every live issue against the canonical corpus; identified 17 drift families.
- Produced 75 candidates and 69 live-issue dispositions with many-to-many mapping.
- Inventoried all labels with usage counts and proposed a target taxonomy.
- Classified every declared dependency as blocking or ordering; identified one cycle, one inverted
  edge, three unresolvable blanket references, one stale reference and one moved target.

**Mutations:** none.

## Entry 3 — Phase 2: consistency validation

- Ran 26 consistency checks across PRD, permissions matrix, ADRs, domain model, OpenAPI, roadmap,
  implementation plan and the proposed backlog.
- Result: **zero canonical-document conflicts.** No documentation change was required or proposed.
- Two checks initially reported conflicts; both were defects in the checking logic, verified against
  the specification text and corrected. The canonical documents were correct in both cases.

**Mutations:** none.

## Entry 4 — schema revision 1.1

- Added `action_semantics` documenting `candidate.action` and `live_issue.disposition` as independent
  axes, with an explicit rule that Phase 3 derives the issue number to edit from
  `live_issues[].role == "primary"` and never from `candidate.action`.
- Added role invariants. Writing them exposed a real defect: the six `SPLIT` candidates carried no
  `primary` role, so nothing recorded which sibling inherits the original issue number. Assigned
  Backend#4 → `M0-B4`, Backend#8 → `M1-B3`, Backend#14 → `M2-B4`.
- Added `canonical_baseline` provenance to the matrix.

**Mutations:** none to GitHub.

## Entry 5 — canonical baseline commit

Before this entry the Documentation repository had **no commits at all**, so no immutable reference
existed that a backlog mutation could cite.

- Committed 60 canonical documents as `3006cae`, 20,839 insertions.
- The two audit artifacts were deliberately **excluded**: recording a baseline SHA inside a file that
  is part of that same commit would be circular.
- `.DS_Store` excluded by the existing `.gitignore`.
- Committed to `main`. The repository had no commits, so branching would have left `main` empty.

**Mutations:** local Git only.

## Entry 6 — reconciliation artifact commit

- Committed `planning/backlog-reconciliation-report.md` and
  `planning/backlog-reconciliation-matrix.json` as `870385e`, with `3006cae` as parent.
- Both artifacts record the baseline SHA in their provenance sections.

**Mutations:** local Git only.

## Entry 7 — push to origin

- `git push -u origin main`. No force, no history rewrite, no amend.
- Result: `* [new branch] main -> main`; `origin/main` created.

### Remote verification

| # | Check | Result |
|---|---|---|
| 1 | `origin/main` resolves to the reconciliation commit | **PASS** — `870385e461b632b6a02f08300ff75242fb9e9d40` |
| 2 | Baseline commit reachable from `origin/main` | **PASS** — `3006cae…` is the direct parent |
| 3 | `planning/backlog-reconciliation-report.md` present remotely | **PASS** — blob `b0f83718f2`, 97,792 bytes, matches local |
| 3 | `planning/backlog-reconciliation-matrix.json` present remotely | **PASS** — blob `b2ff9e7d86`, 187,394 bytes, matches local |
| — | Remote tree file count on `main` | 62 (60 baseline + 2 artifacts) |
| — | Baseline commit tree file count | 60 |

**Mutations:** Git push only. No GitHub issue, label, milestone or dependency was touched.

## Entry 8 — decisions frozen and matrix regenerated

All nine open questions resolved by project decision. Matrix regenerated at **schema 1.2** with a
`frozen_decisions` register.

Effects: confidence is now 75 high / 0 medium / 0 low, with `decided_by` recording which decision
determined each of the six previously-medium candidates; every actionable `label_changes` entry is
empty per OQ-9, with the proposal retained as advisory; `M2-B7` states outcomes only per OQ-8;
Backend#34 moved to M2 per OQ-4; acceptance criteria added to `M0-A1`, which OQ-5 unblocked.

Twelve new verification rules (12a–12m) enforce the frozen state. Two baseline checks (11b, 11c) were
corrected: they compared the baseline SHA against `HEAD`, which is wrong now that `HEAD` has advanced
past the baseline. They now assert the baseline is an *ancestor* of `HEAD` and inspect the tree at the
baseline commit itself.

Result: **47 invariants pass, 0 fail** and **26 consistency checks pass, 0 conflicts.**

Committed as `086831d`, which supersedes `870385e` as the Phase 3 execution source.

**Mutations:** none to GitHub.

## Cumulative GitHub mutation status

**Zero issue, label, milestone or dependency mutations have been performed at any point.**

Evidenced by:

- every one of the 69 issues returns `[]` from the native dependency endpoint;
- every issue's `updated_at` predates this session, and any write of any kind would bump it;
- label and milestone sets are identical to the Phase 0 inventory.

## Phase 3 authorization status

**Not authorized.** Gates A, B, C and D all pass — the nine decisions are frozen. **Gate E
(dependency-API capability probes) remains unverified and has not been run**, on instruction.

Phase 3 additionally requires explicit authorization to begin. See
[`backlog-reconciliation-phase3-preflight.md`](backlog-reconciliation-phase3-preflight.md).
