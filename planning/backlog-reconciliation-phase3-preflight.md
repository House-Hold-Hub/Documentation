# Phase 3 preflight

> **Status:** Draft
> **Owner:** Documentation repository
> **Last reviewed:** 2026-08-17 (decisions frozen)
> **Canonical for:** Nothing — operational gate checklist
> **Purpose:** Conditions that must hold before any mutation of the live GitHub backlog, and the
> immutable revisions that mutation must be traceable to.

## Traceability anchors

Phase 3 executes **only** from these revisions. If either changes, the preflight is void and the
reconciliation must be re-derived.

| Role | SHA |
|---|---|
| **Frozen matrix — the revision Phase 3 executes from** | `086831d65d2a5d5dbd0c441ed3c1e4d9481a5ea8` |
| Reconciliation-artifact commit (pre-freeze, superseded) | `870385e461b632b6a02f08300ff75242fb9e9d40` |
| Canonical documentation baseline (the source the matrix was derived from) | `3006cae70caba1829d0ad8cfcc9b17af5791f052` |

`870385e` carried the matrix **before** the nine decisions were frozen. Phase 3 must execute from
`086831d`, which is the only revision containing `frozen_decisions` and the neutralized label
changes. Executing from `870385e` would apply the label migration that OQ-9 deferred.

Repository: `House-Hold-Hub/Documentation`, branch `main`, both commits present on `origin`.

Every issue body written in Phase 3 that needs to cite its provenance cites `086831d`. No issue body
may contain a Git SHA in place of a canonical requirement reference — SHAs establish *when* a decision
was made, not *what* the requirement is.

## Gate A — provenance (satisfied)

| # | Gate | Status |
|---|---|---|
| A1 | Documentation has a durable committed baseline | **PASS** — `3006cae` |
| A2 | Reconciliation artifacts committed against that baseline | **PASS** — `870385e`, parent `3006cae` |
| A3 | `origin/main` resolves to the reconciliation commit | **PASS** |
| A4 | Baseline reachable from `origin/main` | **PASS** — direct parent |
| A5 | Both artifacts present remotely and byte-identical to local | **PASS** |
| A6 | No history rewrite, amend or force-push | **PASS** |

## Gate B — matrix integrity (satisfied)

47 invariants pass, 0 fail, stable across repeated runs. Notably:

| # | Gate | Status |
|---|---|---|
| B1 | Exactly one action per candidate; ids unique | **PASS** — 75 candidates |
| B2 | Exactly one disposition per live issue; all 69 present once | **PASS** |
| B3 | Forward and reverse mappings agree bidirectionally | **PASS** |
| B4 | At most one `primary` per candidate; every retained issue is `primary` in exactly one | **PASS** |
| B5 | `MERGE` candidates have ≥2 contributors and exactly one `primary` | **PASS** |
| B6 | `closure_kind` model valid and exclusive to `CLOSE_SUPERSEDED` | **PASS** — 0 closures |
| B7 | No archived document cited as a normative source | **PASS** |
| B8 | Schema documents both action axes and the Phase 3 primary rule | **PASS** — schema 1.2 |
| B10 | All nine decisions frozen; zero actionable label changes | **PASS** — rules 12a–12m |
| B9 | Proposed blocking-dependency graph is acyclic | **PASS** — 21 edges, 24 nodes |

## Gate C — canonical consistency (satisfied)

| # | Gate | Status |
|---|---|---|
| C1 | Zero unresolved canonical-document conflicts | **PASS** — 26/26 checks |
| C2 | All 132 `*-FR-nnn` requirements covered with verifiable criteria | **PASS** |
| C3 | No proposal introduces a roadmap non-goal | **PASS** |
| C4 | No proposal implicitly resolves D01–D06 | **PASS** |
| C5 | No proposal restates a contract schema | **PASS** |

## Gate D — decisions (SATISFIED — frozen 2026-08-17)

All nine open questions are resolved. Full text in `frozen_decisions` in the matrix and §11 of the
report.

| # | Gate | Resolution | Status |
|---|---|---|---|
| D1 | OQ-1 milestone naming | No milestone renamed | **PASS (deferred out of scope)** |
| D2 | OQ-2 Documentation#1 | `UPDATE`, narrowed to OpenAPI publication/validation/CI | **PASS** |
| D3 | OQ-3 Documentation M9 milestone | Deferred; left open and unchanged | **PASS (deferred)** |
| D4 | OQ-4 Backend#34 milestone | Move M8 → M2 | **PASS** |
| D5 | OQ-5 Automation boundary | Reusable callable asset; service repos invoke; no provider before D02 | **PASS** |
| D6 | OQ-6 session/registry boundary | Kept together in Backend#7 / `M1-B2` | **PASS** |
| D7 | OQ-7 expense visualization | Totals required; chart neither required nor forbidden | **PASS** |
| D8 | OQ-8 recovery mechanism | Mechanism deferred; `M2-B7` states outcomes only | **PASS** |
| D9 | OQ-9 label taxonomy | Migration deferred entirely; **zero** label mutation | **PASS (deferred)** |

Enforcement: rules 12a–12l assert every one of these in the matrix. Rule 12c fails preflight if any
candidate carries an actionable label change; rule 12k fails if `M2-B7` names an implementation
mechanism.

## Gate E — capability probes (must run at Phase 3 start, before any write)

## Gate E — capability probes (SATISFIED — probed 2026-08-17)

| # | Gate | Status |
|---|---|---|
| E1 | Exact request body confirmed by probe and read back | **PASS** — `POST .../dependencies/blocked_by` with `{"issue_id": <numeric id>}` → 201 |
| E2 | Cross-repository edges accepted by this organization | **PASS** — Automation#3 ← Infrastructure#1 accepted, read back with `repository.full_name` |
| E3 | Numeric issue `id` is the correct reference | **PASS** — `id`, not `#number`, not `node_id` |
| E4 | Removal verified, no reciprocal or duplicate residue | **PASS** — `DELETE .../blocked_by/{issue_id}` → 200; both sides return to 0 |
| E5 | Idempotency characterized | **PASS** — duplicate create → 422 with no residual state; delete of a missing edge → 200 no-op |
| E6 | Repository returned to exact pre-probe state | **PASS** — 0 edges before, 0 after; 0 issue-field drift |

Full HTTP evidence is in Entry 9 of the execution log.

**Required change to the Phase 3 dependency algorithm:** create is not idempotent by repetition. A
duplicate `POST` returns **422 `Target issue has already been taken`**, which the algorithm must treat
as *edge already present* — a success-equivalent outcome — and never as a failure. Without this, a
retry or resumed run would abort on edges it had already written. Self-dependencies are rejected with
422 by the API, so the acyclicity guarantee is enforced server-side for the trivial case; multi-hop
cycles remain the matrix's responsibility and were verified acyclic.

No issue may claim a native dependency the API has not confirmed. If an edge cannot be written, the
execution log records the failure rather than reporting success.

## Gate F — environmental notes (non-blocking, acknowledge before proceeding)

- The four sibling repositories (Automation, Backend, Frontend, Infrastructure) have **no commits**
  and contain only a `.gitignore`. Phase 3 will create and edit issues against repositories whose
  default branches are empty. This is legal but worth conscious acknowledgement.
- The token holds admin on all five repositories, so milestone and label mutation will succeed
  without further permission escalation. Nothing constrains a mistake except this checklist.

## Exact mutation counts (frozen)

| Mutation | Count |
|---|---|
| Issues updated in place, number preserved | 69 |
| New issues created | 6 |
| Issues closed | 0 |
| Issues deleted | 0 |
| Milestone reassignments | 1 (Backend#34 M8 → M2) |
| Milestone renames / closures / creations | 0 / 0 / 0 |
| Label mutations of any kind | **0** |
| Native `blocked_by` edges | 21 (pending Gate E) |

Backlog after Phase 3: 69 existing + 6 new = **75 issues**.

## Mutation order (when Gate E passes)

1. Probe the native dependency API with one edge and read it back (Gate E).
2. ~~Label taxonomy~~ — **skipped, OQ-9 deferred. Perform no label mutation.**
3. Reassign Backend#34 from M8 to M2. No other milestone is touched.
4. Update the 66 straightforward `UPDATE` issues in place, preserving their numbers.
5. Create the 6 new issues: `M1-F3`, `M2-B7`, `M2-F4` (`CREATE`) and `M1-B4`, `M1-B5`, `M2-B5`
   (`SPLIT` successors).
6. Narrow the 3 `SPLIT` source issues — Backend#4, #8, #14 — to their retained scope.
7. Write the 21 native `blocked_by` edges and read each one back.
8. ~~Close the empty Documentation M9 milestone~~ — **skipped, OQ-3 deferred.**

Issue bodies use the agreed structure — `# Summary`, `## Scope`, `## Acceptance Criteria`,
`## Dependencies`, `## PRD References`, `## OpenAPI References`,
`## Architecture / ADR References` — including only the sections that apply. Bodies **reference**
OpenAPI operation identifiers and PRD requirement identifiers and never restate request, response or
schema contracts, which would create the competing inventory ADR-014 forbids.

## Standing prohibitions

Never delete an issue. Never delete documentation. No force-push. No history rewrite. No secrets in
issue bodies. No product requirement is modified to make an existing issue look correct. If a mutation
cannot be performed safely through the available API, report it rather than reporting success.
