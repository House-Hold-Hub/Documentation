# Phase 4b — live-body hygiene audit and repair list

> **Status:** Draft — proposed repairs, **not applied**
> **Owner:** Documentation repository
> **Last reviewed:** 2026-08-17
> **Canonical for:** Nothing — audit artifact
> **Purpose:** Read-only audit of all 75 live GitHub issue bodies after Phase 3, listing residual
> legacy or contradictory content and the proposed repair for each.

**No GitHub mutation has been performed for this audit.** Labels, milestones, states, dependencies and
issue topology are untouched and must remain so.

## Method

Bodies were read **directly from the GitHub API** for all 75 issues, not from the locally generated
projection. 19 detector rules were applied across the whole body, with negation scoping at the
*clause* level so that prohibition language ("no `google_id`", "Remove 422 from the error set") is not
mistaken for an affirmative legacy assertion.

- Issues scanned: **75**
- Raw rule matches: **17**
- Genuine defects after triage: **4**, across **3 issues**
- Correctly suppressed as prohibition language: **13**
- False positive found during triage: **1** (Frontend#4, "the explicit exclusion of Jest")

Every defect is a **Scope/Acceptance-Criteria contradiction**: the `## Scope` section states the
legacy rule was removed while `## Acceptance Criteria` still asserts it.

## Repair list

| Repo | Issue | Offending text | Reason | Proposed replacement / removal | Canonical source |
|---|---|---|---|---|---|
| Frontend | **#8** | `- [ ] 20+ auth test cases (happy path + errors)` | Arbitrary numeric test-count quota. Scope explicitly says *"Replace numeric test-count and coverage gates with the behaviour/journey matrix; coverage is reported, never merge-blocking"* — the AC contradicts it. | Replace with: `- [ ] Auth happy-path and error-path behaviour is covered across the required security scenario families.` | `quality/testing-strategy.md` §Purpose, §Coverage reporting; `prd-householdhub-mvp.md` §8 |
| Frontend | **#20** | `- [ ] Optional grouping by category displayed when category is set on items (FR-57)` | Legacy monolithic-PRD identifier. Scope explicitly says *"Replace legacy references with INV-FR-005 and INV-FR-006"* — the AC contradicts it. | Replace `(FR-57)` with `(INV-FR-005)` | `product/prds/prd-inventory-management.md` §9 legacy traceability: `FR-57`–`FR-58` → `INV-FR-005`–`INV-FR-006` |
| Frontend | **#20** | `- [ ] Last modified date shown per item (FR-58)` | Same as above. | Replace `(FR-58)` with `(INV-FR-006)` | `product/prds/prd-inventory-management.md` §9 |
| Backend | **#26** | `- [ ] Model created, matches ERD` | Normative reference to an archived snapshot. Scope explicitly says *"Cite the domain model and inventory PRD"* — the AC contradicts it. | Replace with: `- [ ] Model created, matches the canonical domain model` | `architecture/domain-model.md`; `README.md` §Archive policy |

### Not defects — verified during triage

| Issue | Matched text | Why it is correct |
|---|---|---|
| Backend#23 | `amount_cents` | `- [ ] amount_minor is a strictly positive integer; no field named amount_cents exists.` — prohibition |
| Backend#2, #6 | `google_id`, `password_hash` | *"defines neither a password field nor a `google_id`"* — prohibition |
| Backend#8, #27 | `422` | *"Remove 422 from the error set"*, *"no 422 is returned"* — prohibition |
| Documentation#1, #3 | `OPENAPI.md`, `ERD` | *"Drop the archived OPENAPI.md reference"*, *"Replace the archived System Design and ERD references"* — supersession explanation |
| Frontend#4 | `Jest` | *"note the explicit exclusion of Jest"* — prohibition |

## Root cause

All four defects trace to three regex faults in the Phase 3 body scrubber, not to the projection
design. The scrubber ran only over carried-forward acceptance criteria, and:

| # | Fault | Effect |
|---|---|---|
| 1 | Test-count pattern required the digits to be adjacent to the noun: `\d+\+?\s*(test cases\|tests\|cases)` | `20+ auth test cases` did not match because `auth` sits between them. `50+ test cases` and `15+ test cases` did match, which is why only one such defect survived. |
| 2 | Archived-document pattern required the `.md` suffix: `\bERD\.md\b` | `matches ERD` (bare) did not match. `per ERD.md cascade rules` did. |
| 3 | **No rule existed at all** for legacy `FR-nn` identifiers | Every surviving legacy FR reference passed through untouched. |

The Phase 4 verifier then failed to catch the survivors because its hygiene check reused the same
narrow patterns and applied negation detection across the **whole line** rather than per clause, and
because it never compared `## Scope` against `## Acceptance Criteria` for self-contradiction.

## Verifier redesign

The Phase 4 checker is replaced by the Phase 4b rule set so these classes fail automatically.

### R1 — Tolerant quantity patterns

Numeric-gate detectors must allow intervening words between the quantity and its noun:

```
\b\d+\s*\+(?:\s*\w+){0,3}?\s*(?:test cases?|tests|cases|scenarios)\b
```

Applies equally to coverage, latency, concurrency, bundle-size, Lighthouse and index-count gates.

### R2 — Archived references matched with or without an extension

```
\bERD(?:\.md)?\b | \bSYSTEM_DESIGN(?:\.md)?\b | \bDOMAIN_MODEL_[A-Z]+(?:\.md)?\b
| \bOPENAPI\.md\b | \bIMPLEMENTATION_PLAN[A-Z_]*(?:\.md)?\b
| \bGITHUB_ISSUES_PROPOSAL[A-Z_]*(?:\.md)?\b | \bFINAL_TECHNOLOGY_CHOICES(?:\.md)?\b
```

### R3 — Legacy requirement identifiers detected explicitly

```
\(?\bFR-\d{1,2}\b(?:-\d{1,2})?\)?
```

Any `FR-nn` that is not one of the canonical prefixed forms (`MVP-`, `IA-`, `HH-`, `TASK-`, `SHOP-`,
`EXP-`, `INV-`, `DASH-`) is a defect. The repair is always the mapping in the owning PRD's legacy
traceability table.

### R4 — Clause-level negation scoping

Negation is evaluated on the clause containing the match, not the whole line, so a sentence that
prohibits one legacy term cannot mask an affirmative use of another in the same sentence. The negation
vocabulary is extended to include nominalized forms (`exclusion`, `removal`, `replacement`), which the
Frontend#4 false positive exposed.

### R5 — Scope ↔ Acceptance-Criteria contradiction check (new class)

For each issue and each rule class: if `## Scope` contains a *removal statement about that class* and
`## Acceptance Criteria` still contains a *match of that class*, fail — regardless of whether the
exact token appears in both sections. The Phase 4b detector initially reported zero contradictions
because it required token-level overlap between the two sections; the correct test is class-level.

### R6 — Audit the live body, never the local projection

Phase 4 verification must re-read bodies from the GitHub API. Validating the generated projection
against itself cannot detect a scrubber fault, which is precisely how these four defects reached
production.

### R7 — Rule-set self-test

Each detector ships with positive and negative fixtures — including the three real defects above and
the thirteen prohibition-language lines that must **not** fire — so a future regex tightening cannot
silently reintroduce the gap.

## Proposed repair mechanics (not executed)

Four single-line edits across three issue bodies. Each is a `PATCH` of the `body` field only. No
title, label, milestone, state, dependency or topology change. Original bodies are retained in the
session state file, so each edit is reversible.

Awaiting review before any mutation.
