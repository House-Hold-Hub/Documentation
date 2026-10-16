# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Documentation is one of the five HouseHoldHub repositories (Backend, Frontend, Infrastructure,
Automation, Documentation: ADR-009), cloned as siblings under `..`. It contains no application code:
it is the shared source of truth for product requirements, architecture decisions, the domain model,
the machine-readable API contract (`api/openapi.yaml`), and security, quality and planning guidance
for a household-collaboration web app (Django/DRF + PostgreSQL backend, React/Vite frontend).

The repository is public. `main` changes only through pull requests (ruleset "Protect main": both CI
gates required, review threads resolved, no force-push or deletion). Implementation state lives in
the sibling repositories, not here: check them before describing anything as implemented, and
describe planned behaviour as planned.

## Commands

There is no build, manifest or test suite. CI is two gates in `.github/workflows/gates.yml`, both
reusable workflows from Automation pinned by commit SHA, so tool versions come from `../Automation`
at that SHA (fetch there if the commit is missing). Locally you need Docker and Node/npx.

```bash
# Read the tool pins the way CI resolves them, so local runs cannot drift from it
redocly=$(git -C ../Automation show "$(grep -o 'openapi-validate.yml@[0-9a-f]*' .github/workflows/gates.yml | cut -d@ -f2):.github/workflows/openapi-validate.yml" | sed -n '/redocly-version:/,/default:/s/.*default: //p')
gitleaks=$(git -C ../Automation show "$(grep -o 'secret-scan.yml@[0-9a-f]*' .github/workflows/gates.yml | cut -d@ -f2):.github/workflows/secret-scan.yml" | grep -o 'ghcr.io/gitleaks/gitleaks@sha256:[0-9a-f]*')

# `OpenAPI / validate`: bundle fails on YAML syntax or an unresolved $ref; lint applies redocly.yaml (`recommended`)
npm_config_ignore_scripts=true npx --yes "@redocly/cli@$redocly" bundle api/openapi.yaml --output "${TMPDIR:-/tmp}/openapi-bundled.yaml"
npm_config_ignore_scripts=true npx --yes "@redocly/cli@$redocly" lint api/openapi.yaml --config redocly.yaml

# `Secret scan / scan` as a pull request runs it: default rules over the commits the branch adds.
# Drop --log-opts to scan the whole history, as pushes to main do.
docker run --rm -v "$PWD:/repo:ro" -e GIT_CONFIG_COUNT=1 -e GIT_CONFIG_KEY_0=safe.directory -e GIT_CONFIG_VALUE_0=/repo \
  "$gitleaks" git /repo --log-opts "origin/main..HEAD" --redact --verbose --no-banner

# Backlog issue-body hygiene verifier: offline self-test, then the read-only live audit of every
# issue in the five repositories (needs `gh` auth; exits 1 on any finding)
python3 planning/verify_issue_hygiene.py --selftest
python3 planning/verify_issue_hygiene.py --json "${TMPDIR:-/tmp}/issue-hygiene.json"
```

Only lint errors fail the gate, not warnings. Some warnings describe real behaviour (Google OAuth
start and callback succeed with a `302`, never a `2XX`; the CSRF bootstrap returns only `200`), so do
not add responses the server never sends just to silence them.

No Markdown lint or link checker is configured. The validation checklist in `CONTRIBUTING.md` (links
resolve, no archived document cited as authority, no live issue counts, no superseded terminology,
requiredness/nullability consistent across PRDs, domain model and OpenAPI) is a manual review.

## Architecture

### Authority is per artifact type, not "newest wins"

The canonical source map in `README.md` decides where each fact lives. When documents disagree, the
one responsible for that kind of information wins. Disagreement with a manifest, migration or the
executable contract is drift to reconcile, never licence to silently change an accepted decision.

| Information | Lives only in |
|---|---|
| Product behaviour and acceptance outcomes | `product/prds/`: umbrella MVP PRD for scope and cross-feature journeys, one feature PRD per area |
| Who may perform each action | `product/permissions-matrix.md` |
| Durable technical decisions | `architecture/adr/` |
| Conceptual entities, relationships, invariants | `architecture/domain-model.md` |
| Routes, schemas, requiredness, nullability, wire errors, operation security | `api/openapi.yaml` |
| Cross-cutting security controls | `security/security-model.md` and the security ADRs |
| Test philosophy and release journeys | `quality/` |
| Technology families, without exact pins | `architecture/technology-baseline.md` |
| Exact versions, executable schema | the owning repository's manifests, lockfiles, models and migrations |
| Execution state, issue counts | live GitHub issues |

Link to the owning artifact instead of copying from it: no route or schema inventories outside
OpenAPI (`api/README.md` explains conventions but deliberately lists no routes), no permission
tables outside the matrix, no issue counts or status in Markdown. A change spanning several
categories updates each owning artifact in the same change.

### Lifecycle and history

- Normative documents open with a blockquote metadata block: Status (Draft, Proposed, Accepted,
  Superseded, Archived), Owner, Last reviewed, Canonical for, Supersedes / Superseded by. ADRs add
  Date.
- ADRs are immutable decision records. Changing a decision means a new ADR with the next unused
  three-digit number (never reuse or renumber), `Supersedes` / `Superseded by` links in both
  directions, and a row in `architecture/adr/README.md`. An Accepted ADR may be partly superseded;
  the index records which portion. Code in older ADRs is illustrative, not setup guidance.
- `archive/` holds superseded snapshots moved intact into a dated folder. Never edit them, cite them
  only as labelled provenance, and do not mine them for facts: they contradict each other and the
  current canon.
- `planning/backlog-reconciliation-*` and `planning/github-issues-draft.md` are Draft records,
  canonical for nothing, anchored to commit SHAs; the execution log is append-only.
- Filenames are lowercase kebab-case except `README.md`, `CONTRIBUTING.md` and `ADR-NNN-*.md`.
  `final`, `corrected`, `revised` or `complete` never signal status.

### Requirements, deferred decisions, superseded terms

- PRD requirements use stable IDs `<AREA>-FR-NNN` and stories `<AREA>-US-NNN`, with areas `MVP`,
  `IA` (identity), `HH` (household, membership, invitations), `TASK`, `SHOP`, `EXP`, `INV`, `DASH`.
  Legacy `FR-1`..`FR-69` appear only in the legacy disposition and traceability sections.
- `product/roadmap.md` defers D01–D06 (auth and rate-limit constants; email, deployment, secret-store
  and monitoring vendors; legal retention; RTO/RPO; schedule; exact versions, tools and indexes)
  with deadlines. No document may resolve them implicitly: do not name a vendor, a numeric constant
  or threshold, or an exact patch version or tool choice that those decisions still defer; such a
  tool or patch version becomes citable once the owning repository has committed it. The approved
  baselines stay fixed and citable (Python 3.14, Django 5.2 LTS, React 19, TypeScript, Vite, npm,
  PostgreSQL, GitHub Actions: `product/roadmap.md`, `architecture/technology-baseline.md`), and exact
  dependency versions are owned by each repository's manifests and lockfiles.
- The `RULES` table in `planning/verify_issue_hygiene.py` is the working catalogue of superseded
  claims (`amount_cents`, `google_id`, `password_hash`, Django 6, HTTP 422, `SameSite=Strict`,
  token-in-path invitation routes, numeric test-count, coverage and latency gates, references to
  archived snapshots, ...). Active documents mention these only to prohibit them.

### The OpenAPI contract

`api/openapi.yaml` is OpenAPI 3.0.3 with server base `/api/v1`: one file, internal `$ref`s only,
`components` first, then `paths`. Its conventions (ADR-014, `api/README.md`):

- Root `security: sessionAuth`; a public operation declares `security: []`. Public is not
  CSRF-exempt: every POST, PATCH and DELETE takes `$ref: '#/components/parameters/CsrfToken'`.
- Errors reuse `components/responses` (`BadRequest`, `Unauthorized`, `Forbidden`, `NotFound`,
  `Conflict`, `TooManyRequests`), all with `ErrorResponse`. `404` also covers resources outside the
  caller's household; `403` only a visible resource whose action is denied; `409` duplicates and
  invalid lifecycle transitions. Never `422`, and no concurrency `409` or version fields: writes are
  last-write-wins.
- Create, Update, Summary and Response schemas are separate. Objects set
  `additionalProperties: false`, except Summaries that a Response extends through `allOf`
  (`HouseholdSummary`, `TaskSummary`), where OAS 3.0 would reject the extension's properties.
  Update schemas have `minProperties: 1` and no `required`; always-emitted response properties are
  `required` even when `nullable: true`.
- One-time verification, reset and invitation bearers travel in POST bodies, never in a path or
  query.

### Contract changes cross repositories

OpenAPI changes before or together with the implementation, never after. A breaking change
(removing or renaming a route or field, narrowing values, changing requiredness, nullability,
authentication or status behaviour) needs Documentation, Backend and Frontend review; a PRD changes
only if product behaviour does. Consumers pin a full Documentation commit SHA: Frontend in
`tools/contract/contract.lock.json` (CI regenerates `src/contract/` and compares), Backend in
`contract/documentation-revision.json` with the file's SHA-256 (`manage.py check_api_contract`). A
merged contract change reaches them only when they bump that pin. Backend's local contract check
runs `git -C ../Documentation checkout <pinned commit>`, which can leave this repository on a
detached HEAD.

### CI gates

`gates.yml` calls Automation's `secret-scan.yml` and `openapi-validate.yml` at a full commit SHA,
never a branch or tag; bumping means updating both `uses:` SHAs and the header comment. The
published check names `Secret scan / scan` and `OpenAPI / validate` (caller job name / called job
name) are the required checks in "Protect main": renaming a job silently drops the protection, so
update the ruleset in the same change. Never add `paths:` filters: a skipped required check stays
pending and blocks the pull request. There is no dependency-security gate because there is no
lockfile.

The secret scan runs Gitleaks' default rules over every commit a pull request adds, so a
credential-like string in any commit fails CI even if a later commit removes it: rewrite the branch
instead. Prose can trip it (archived text "Password hashing: ... with proper cost" matched
`generic-api-key`). Exclusions go in `.gitleaksignore` by exact fingerprint only, never per file or
rule. `CONTRIBUTING.md` records whether GitHub-native secret scanning and push protection are on; do
not rely on them, and on this public repository run the scan above before pushing.

## Git workflow

- Conventional Commit subjects (`docs:`, `docs(planning):`, `ci:`), `Refs <repo>#<issue>` in the
  body, branches such as `docs/2-contribution-governance` or `ci/gitleaks-false-positive`, pull
  requests into `main`.
- Pull requests have been merged with merge commits, so every commit on the branch lands on `main`:
  keep throwaway or test commits out of a branch you intend to merge.
- `.claude/worktrees/` (excluded through `.git/info/exclude`) may hold full checkouts of other
  branches; search with `git grep`, or exclude that directory, so stale copies don't show up as
  matches.
