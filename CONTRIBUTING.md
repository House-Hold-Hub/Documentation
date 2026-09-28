# Contributing to HouseHoldHub Documentation

> **Status:** Accepted  
> **Owner:** Documentation repository  
> **Last reviewed:** 2026-09-28  
> **Canonical for:** Documentation contribution, implementation contribution standards, and cross-repository contract-change workflow

## Principles

1. Put information in the artifact that owns it, as defined by the [canonical source map](README.md#canonical-source-map).
2. Link to canonical detail instead of copying it.
3. Describe planned behavior as planned; do not imply that an empty or incomplete implementation repository already provides it.
4. Use lowercase kebab-case filenames except for `README.md`, `CONTRIBUTING.md`, and `ADR-NNN-*.md`.
5. Add concise metadata to normative Markdown: status, repository/team owner, last-reviewed date, canonical scope, and supersession links where relevant.
6. Preserve decision history. Supersede an accepted ADR with a new ADR rather than rewriting its original decision.
7. Treat repository-owned manifests, lockfiles, compiler/test configuration, scripts, and CI workflows as authoritative for exact dependency versions and executable tool commands.
8. Do not select or document an exact formatter, linter, package/lock strategy, database driver, or other `D06` detail here unless the responsible repository has selected it in committed configuration.

## Choosing the right document

- Change a PRD for product behavior, scope, or acceptance outcomes.
- Change the permissions matrix for product authorization rules, then link the affected PRD to it.
- Add or supersede an ADR for a durable technical decision with meaningful alternatives or consequences.
- Change the domain model for conceptual entities, relationships, lifecycle, and invariants.
- Change `api/openapi.yaml` for any route, method, request, response, error, or operation-security change.
- Change the security model for cross-cutting threat controls and security lifecycle requirements.
- Change quality documents for test strategy or release evidence.
- Change the implementation plan for sequencing and dependencies, never for live issue status.

## Implementation contribution standards

These standards describe cross-repository expectations. Exact commands, formatter/linter choices, dependency pins, generated-file rules, and check entry points belong to the repository being changed. Follow its committed configuration and the approved [technology baseline](architecture/technology-baseline.md); do not invent missing tooling in this guide.

### Backend

Backend contributions must:

- remain within the approved Backend runtime and framework baseline;
- keep executable persistence changes in Backend models and migrations rather than documenting speculative database schema here;
- implement routes, request/response shapes, wire errors, and operation security from the Documentation-owned OpenAPI contract rather than creating a competing API definition;
- include migrations when an executable persistence-schema change requires them;
- add or update tests for changed behavior, including relevant authorization, validation, and failure cases;
- run the Backend repository's committed checks and CI entry points before merge.

**Example:** when adding a response field, change `api/openapi.yaml` before or with the Backend implementation. The Backend change then implements that contract and updates its tests. A migration is added only if persistence changes; the field is not redefined as a second normative wire schema in Backend documentation.

### Frontend

Frontend contributions must:

- remain within the approved React, TypeScript, Vite, npm, and native CSS/CSS Modules/custom-properties baseline;
- consume routes and wire shapes from the Documentation-owned OpenAPI contract instead of maintaining a hand-written competing route/schema inventory;
- regenerate contract-derived artifacts when the Frontend repository provides a committed generation workflow;
- keep component and integration behavior covered by the repository's configured tests, including relevant loading, error, authorization-loss, and accessibility behavior;
- run the Frontend repository's committed checks and CI entry points before merge.

**Example:** when consuming a newly added API field, do not invent a local endpoint or incompatible response type. Use the contract-defined field, regenerate repository-owned contract artifacts when that workflow exists, and update the affected component tests.

### Tooling example

A contribution guide may say **"run the repository's configured format, lint, type, test, and build checks"** and link to that repository's committed scripts or workflow. It must not choose a formatter or linter merely to make this document more specific while `D06` leaves that choice to repository configuration.

## Status and review

New normative documents begin as `Draft` or `Proposed`. A reviewer with responsibility for the affected repository or product area may advance them to `Accepted`. When a document is replaced, mark it `Superseded`, name the replacement, and retain or archive it according to the [archive policy](archive/README.md).

Do not use filename adjectives such as `final`, `corrected`, `revised`, or `complete` to communicate status.

## API contract changes

The Documentation repository owns the machine-readable contract. For any API change:

1. Update [`api/openapi.yaml`](api/openapi.yaml) first or in the same coordinated change as producer/consumer work.
2. Update the responsible PRD only if product behavior changes; do not add a second route inventory.
3. Update the domain model or add/supersede an ADR only if conceptual invariants or a durable decision change.
4. For a breaking change, obtain review from all three responsible repositories: **Documentation** as contract owner, **Backend** as producer, and **Frontend** as consumer.
5. Validate OpenAPI syntax, references, and contract quality before merge.
6. Regenerate Backend/Frontend contract artifacts when those repositories provide generation workflows.
7. Coordinate rollout so incompatible producer and consumer versions are not released independently.

A breaking change includes removing or renaming a route or field, narrowing an accepted value, changing requiredness or nullability, changing authentication requirements, or changing an established response/status behavior.

The contract change must merge before or with the implementation changes that depend on it. Backend or Frontend changes must not establish a new wire contract first and leave Documentation to catch up later.

### Coordinating cross-repository pull requests

When one change spans repositories:

- link the related Documentation, Backend, and Frontend pull requests or issues;
- identify which change owns the contract and which changes implement or consume it;
- keep implementation PRs compatible with the contract revision they reference;
- do not merge an incompatible producer or consumer independently;
- include Infrastructure or Automation only when deployment or shared-pipeline behavior is actually affected.

## ADR workflow

Use the template and numbering guidance in [`architecture/adr/README.md`](architecture/adr/README.md). An ADR must include status, context, decision, consequences, and supersession metadata where applicable. Code snippets are illustrative unless the ADR explicitly identifies an executable repository artifact.

## PRD workflow

Use the [PRD index and boundaries](product/prds/README.md). Keep the umbrella MVP PRD focused on product-wide goals, scope, cross-feature journeys, and release outcomes. Put feature-specific behavior and acceptance criteria in the responsible feature PRD. Put route/schema detail in OpenAPI and technical rationale in ADRs.

## Validation checklist

Before proposing a documentation or cross-repository governance change:

- confirm all internal Markdown links resolve;
- validate `api/openapi.yaml` syntactically and with the repository's configured contract checks when it changes;
- search active documentation for terminology superseded by accepted decisions;
- verify required/status/nullability metadata is consistent across PRDs, the domain model, and OpenAPI without duplicating wire definitions;
- confirm archived documents are not linked as current authority;
- confirm live issue counts or status have not been copied into Markdown;
- record intentionally deferred decisions with their trigger or deadline rather than choosing them implicitly;
- for Backend or Frontend code changes, use the exact commands and tool configuration committed in that repository;
- for breaking OpenAPI changes, confirm Documentation, Backend, and Frontend review is represented and the contract change precedes or accompanies implementation changes.

Exact formatter, linter, generator, dependency, and packaging commands remain owned by repository configuration. The [roadmap's `D06` decision](product/roadmap.md#deferred-decisions-and-required-deadlines) must not be resolved implicitly by this guide.
