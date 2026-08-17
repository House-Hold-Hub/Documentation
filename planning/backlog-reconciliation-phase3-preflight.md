# Phase 3 preflight

> **Status:** Draft
> **Owner:** Documentation repository
> **Last reviewed:** 2026-08-17
> **Canonical for:** Nothing — operational gate checklist
> **Purpose:** Conditions that must hold before any mutation of the live GitHub backlog, and the
> immutable revisions that mutation must be traceable to.

## Traceability anchors

Phase 3 executes **only** from these revisions. If either changes, the preflight is void and the
reconciliation must be re-derived.

| Role | SHA |
|---|---|
| Reconciliation-artifact commit (the matrix revision to execute from) | `870385e461b632b6a02f08300ff75242fb9e9d40` |
| Canonical documentation baseline (the source the matrix was derived from) | `3006cae70caba1829d0ad8cfcc9b17af5791f052` |

Repository: `House-Hold-Hub/Documentation`, branch `main`, both commits present on `origin`.

Every issue body written in Phase 3 that needs to cite its provenance cites `870385e`. No issue body
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

35 invariants pass, 0 fail, stable across repeated runs. Notably:

| # | Gate | Status |
|---|---|---|
| B1 | Exactly one action per candidate; ids unique | **PASS** — 75 candidates |
| B2 | Exactly one disposition per live issue; all 69 present once | **PASS** |
| B3 | Forward and reverse mappings agree bidirectionally | **PASS** |
| B4 | At most one `primary` per candidate; every retained issue is `primary` in exactly one | **PASS** |
| B5 | `MERGE` candidates have ≥2 contributors and exactly one `primary` | **PASS** |
| B6 | `closure_kind` model valid and exclusive to `CLOSE_SUPERSEDED` | **PASS** — 0 closures |
| B7 | No archived document cited as a normative source | **PASS** |
| B8 | Schema documents both action axes and the Phase 3 primary rule | **PASS** — schema 1.1 |
| B9 | Proposed blocking-dependency graph is acyclic | **PASS** — 21 edges, 24 nodes |

## Gate C — canonical consistency (satisfied)

| # | Gate | Status |
|---|---|---|
| C1 | Zero unresolved canonical-document conflicts | **PASS** — 26/26 checks |
| C2 | All 132 `*-FR-nnn` requirements covered with verifiable criteria | **PASS** |
| C3 | No proposal introduces a roadmap non-goal | **PASS** |
| C4 | No proposal implicitly resolves D01–D06 | **PASS** |
| C5 | No proposal restates a contract schema | **PASS** |

## Gate D — decisions required (OPEN — blocks Phase 3)

Phase 3 must not begin until these are answered. Each changes what gets written.

| # | Gate | Status |
|---|---|---|
| D1 | OQ-1 milestone naming authority | **OPEN** |
| D2 | OQ-2 Documentation#1 disposition | **OPEN** |
| D3 | OQ-3 empty Documentation M9 milestone | **OPEN** |
| D4 | OQ-4 Backend#34 milestone move M8 → M2 | **OPEN** |
| D5 | OQ-5 Automation build-asset boundary | **OPEN** |
| D6 | OQ-6 session/registry issue boundary | **OPEN** |
| D7 | OQ-7 expense category visualization | **OPEN** |
| D8 | OQ-8 household recovery mechanism | **OPEN** |
| D9 | OQ-9 label taxonomy approval | **OPEN** — blocks all label mutation |

## Gate E — capability probes (must run at Phase 3 start, before any write)

| # | Gate | Status |
|---|---|---|
| E1 | Exact request body for `POST .../dependencies/blocked_by` confirmed by one probe, read back | **UNVERIFIED** |
| E2 | Cross-repository dependency edges accepted by this organization | **UNVERIFIED** |
| E3 | Numeric issue `id` (not `#number`) is the correct dependency reference | **UNVERIFIED** — e.g. Backend#11 is `id=5164176311` |

No issue may claim a native dependency the API has not confirmed. If an edge cannot be written, the
execution log records the failure rather than reporting success.

## Gate F — environmental notes (non-blocking, acknowledge before proceeding)

- The four sibling repositories (Automation, Backend, Frontend, Infrastructure) have **no commits**
  and contain only a `.gitignore`. Phase 3 will create and edit issues against repositories whose
  default branches are empty. This is legal but worth conscious acknowledgement.
- The token holds admin on all five repositories, so milestone and label mutation will succeed
  without further permission escalation. Nothing constrains a mistake except this checklist.

## Mutation order (when all gates pass)

1. Probe the native dependency API with one edge and read it back (Gate E).
2. Apply label taxonomy: additions first, then re-labelling, then removal of now-unused labels.
3. Apply milestone membership changes.
4. Update the 66 `UPDATE` issues in place, preserving their numbers.
5. Create the 6 new issues: 3 `CREATE` candidates and 3 `SPLIT` successors carrying no `primary`.
6. Narrow the 3 `SPLIT` source issues to their retained scope.
7. Write native `blocked_by` edges and read each one back.
8. Close the empty Documentation M9 milestone only if OQ-3 is approved.

Issue bodies use the agreed structure — `# Summary`, `## Scope`, `## Acceptance Criteria`,
`## Dependencies`, `## PRD References`, `## OpenAPI References`,
`## Architecture / ADR References` — including only the sections that apply. Bodies **reference**
OpenAPI operation identifiers and PRD requirement identifiers and never restate request, response or
schema contracts, which would create the competing inventory ADR-014 forbids.

## Standing prohibitions

Never delete an issue. Never delete documentation. No force-push. No history rewrite. No secrets in
issue bodies. No product requirement is modified to make an existing issue look correct. If a mutation
cannot be performed safely through the available API, report it rather than reporting success.
