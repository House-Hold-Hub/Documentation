# HouseHoldHub Documentation

> **Status:** Accepted  
> **Owner:** Documentation repository  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Documentation navigation, authority, lifecycle, and ownership

This repository is the shared source of truth for HouseHoldHub product requirements, durable technical decisions, the API contract, and cross-repository engineering guidance. The application is still in planning: implementation repositories do not yet contain application code or dependency manifests.

## Start here

- [MVP product requirements](product/prds/prd-householdhub-mvp.md)
- [Feature PRD index](product/prds/README.md)
- [Product permissions matrix](product/permissions-matrix.md)
- [Product roadmap](product/roadmap.md)
- [Architecture overview](architecture/overview.md)
- [Technology baseline](architecture/technology-baseline.md)
- [Canonical domain model](architecture/domain-model.md)
- [ADR index](architecture/adr/README.md)
- [Machine-readable API contract](api/openapi.yaml) and [API conventions](api/README.md)
- [Security model](security/security-model.md)
- [Testing strategy](quality/testing-strategy.md)
- [Release acceptance](quality/release-acceptance.md)
- [MVP implementation plan](planning/mvp-implementation-plan.md)
- [Documentation contribution guide](CONTRIBUTING.md)

Archived design and planning snapshots are indexed separately in [archive/README.md](archive/README.md). They are intentionally excluded from the canonical navigation above.

## Canonical source map

HouseHoldHub uses artifact-specific authority rather than a single “newest document wins” rule.

| Information | Canonical source | Must not be duplicated as authority in |
|---|---|---|
| Product goals, scope, behavior, and outcomes | Umbrella and feature PRDs under [`product/prds/`](product/prds/README.md) | ADRs, plans, issues, or API prose |
| Human-readable product authorization | [`product/permissions-matrix.md`](product/permissions-matrix.md) | Feature prose, ADR code samples, or planning checklists |
| Durable architecture decisions and rationale | Accepted ADRs under [`architecture/adr/`](architecture/adr/README.md) | “Final” summaries, plans, or implementation snippets |
| Conceptual entities, relationships, lifecycle, and invariants | [`architecture/domain-model.md`](architecture/domain-model.md) | ERD snapshots, speculative SQL, or framework model examples |
| Routes, request and response shapes, wire errors, and operation security | [`api/openapi.yaml`](api/openapi.yaml) | Route inventories in PRDs, plans, ADRs, or README files |
| Cross-cutting security requirements | [`security/security-model.md`](security/security-model.md) and security ADRs | Scattered framework snippets or issue descriptions |
| Technology choices without exact dependency pins | [`architecture/technology-baseline.md`](architecture/technology-baseline.md) and relevant ADRs | Review summaries or plans |
| Exact dependency and tool versions | Repository manifests and committed lockfiles | This documentation repository |
| Executable persistence schema | Backend models and migrations | Conceptual diagrams or SQL examples in documentation |
| Test philosophy and release journeys | [`quality/`](quality/testing-strategy.md) | Arbitrary issue counts or milestone prose |
| Current work, issue count, ownership, and status | Live GitHub issues and milestones | Markdown issue proposals or planning snapshots |
| Historical context | [`archive/`](archive/README.md) | Active navigation or canonical references |

When sources disagree, use the source responsible for that kind of information. Treat disagreement with a repository manifest, migration, or executable contract as documentation or implementation drift to reconcile; do not silently change an approved product or architecture decision.

## Document lifecycle

Normative Markdown documents declare a status near the top.

- **Draft:** Work in progress; not authoritative.
- **Proposed:** Ready for review but not yet approved.
- **Accepted:** Approved and authoritative for its declared scope.
- **Superseded:** Replaced by an identified document or ADR; retained for traceability.
- **Archived:** Historical and non-normative. It may explain how a decision evolved but cannot override active sources.

Accepted ADRs are historical decision records. Their original decisions are not rewritten silently. A new ADR supersedes an obsolete decision, and both records link to each other.

The labels `FINAL`, `CORRECTED`, `REVISED`, and `COMPLETE` are not lifecycle states and are not used in active filenames.

## Ownership model

No individual document owner has been assigned. Ownership is repository- or team-based:

| Repository | Documentation responsibility |
|---|---|
| Documentation | Shared product requirements, architecture decisions, domain semantics, API contract, security/quality guidance, and cross-repository navigation |
| Backend | Backend implementation, executable models and migrations, API behavior, service Dockerfile, and repository-local checks/workflows |
| Frontend | User interface implementation, generated API client/types, service Dockerfile, and repository-local checks/workflows |
| Infrastructure | Deployment manifests, runtime target configuration, secrets integration, backup/restore configuration, and production runbook implementation |
| Automation | Reusable automation, shared policy and pipeline assets, integration-test support, and secret scanning |

Backend and Frontend reviewers are required for breaking OpenAPI contract changes. Each service repository owns its local workflow entry points; reusable workflow logic belongs to Automation.

## Repository relationships

In the five-repository workspace, the sibling repositories are [Backend](../Backend/), [Frontend](../Frontend/), [Infrastructure](../Infrastructure/), and [Automation](../Automation/). Remote repository URLs have not yet been recorded and must not be guessed.

The repositories integrate through the versioned REST contract in [`api/openapi.yaml`](api/openapi.yaml). Documentation does not imply that any planned component is already implemented.

## Archive policy

Superseded snapshots are moved intact to a dated archive folder. Archive moves preserve filenames so existing review references remain recognizable. Archived files may contain stale or conflicting statements; the archive index labels that explicitly. Canonical documents may link to an archived source for provenance, but archived documents are not included in normal navigation and must not be cited as current requirements.

## Changing documentation

Follow [CONTRIBUTING.md](CONTRIBUTING.md). A change that affects more than one canonical category must update each responsible artifact in the same coordinated change, without copying the same source-of-truth content between them.
