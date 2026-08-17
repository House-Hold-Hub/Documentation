# Contributing to HouseHoldHub Documentation

> **Status:** Accepted  
> **Owner:** Documentation repository  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Documentation contribution and cross-repository contract-change workflow

## Principles

1. Put information in the artifact that owns it, as defined by the [canonical source map](README.md#canonical-source-map).
2. Link to canonical detail instead of copying it.
3. Describe planned behavior as planned; do not imply that an empty implementation repository already provides it.
4. Use lowercase kebab-case filenames except for `README.md`, `CONTRIBUTING.md`, and `ADR-NNN-*.md`.
5. Add concise metadata to normative Markdown: status, repository/team owner, last-reviewed date, canonical scope, and supersession links where relevant.
6. Preserve decision history. Supersede an accepted ADR with a new ADR rather than rewriting its original decision.

## Choosing the right document

- Change a PRD for product behavior, scope, or acceptance outcomes.
- Change the permissions matrix for product authorization rules, then link the affected PRD to it.
- Add or supersede an ADR for a durable technical decision with meaningful alternatives or consequences.
- Change the domain model for conceptual entities, relationships, lifecycle, and invariants.
- Change `api/openapi.yaml` for any route, method, request, response, error, or operation-security change.
- Change the security model for cross-cutting threat controls and security lifecycle requirements.
- Change quality documents for test strategy or release evidence.
- Change the implementation plan for sequencing and dependencies, never for live issue status.

## Status and review

New normative documents begin as `Draft` or `Proposed`. A reviewer with responsibility for the affected repository or product area may advance them to `Accepted`. When a document is replaced, mark it `Superseded`, name the replacement, and retain or archive it according to the [archive policy](archive/README.md).

Do not use filename adjectives such as `final`, `corrected`, `revised`, or `complete` to communicate status.

## API contract changes

The Documentation repository owns the machine-readable contract. For any API change:

1. Update [`api/openapi.yaml`](api/openapi.yaml) first or in the same coordinated change.
2. Update the responsible PRD only if product behavior changes; do not add a second route inventory.
3. Update the domain model or an ADR only if conceptual invariants or a durable decision change.
4. Obtain Backend and Frontend review for breaking changes.
5. Validate OpenAPI syntax and contract quality before merge.
6. Regenerate Backend/Frontend contract artifacts when those repositories provide generation workflows.
7. Coordinate rollout so incompatible producer and consumer versions are not released independently.

A breaking change includes removing or renaming a route or field, narrowing an accepted value, changing requiredness or nullability, changing authentication requirements, or changing an established response/status behavior.

## ADR workflow

Use the template and numbering guidance in [`architecture/adr/README.md`](architecture/adr/README.md). An ADR must include status, context, decision, consequences, and supersession metadata where applicable. Code snippets are illustrative unless the ADR explicitly identifies an executable repository artifact.

## PRD workflow

Use the [PRD index and boundaries](product/prds/README.md). Keep the umbrella MVP PRD focused on product-wide goals, scope, cross-feature journeys, and release outcomes. Put feature-specific behavior and acceptance criteria in the responsible feature PRD. Put route/schema detail in OpenAPI and technical rationale in ADRs.

## Validation checklist

Before proposing a documentation change:

- confirm all internal Markdown links resolve;
- validate `api/openapi.yaml` syntactically and with the repository's configured contract checks when they exist;
- search active documentation for terminology superseded by accepted decisions;
- verify required/status/nullability metadata is consistent across PRDs, the domain model, and OpenAPI without duplicating wire definitions;
- confirm archived documents are not linked as current authority;
- confirm live issue counts or status have not been copied into Markdown;
- record intentionally deferred decisions with their trigger or deadline rather than choosing them implicitly.

Exact formatter, linter, generator, and dependency commands remain owned by repository configuration once those files exist. Do not invent commands in documentation before the repositories define them.
