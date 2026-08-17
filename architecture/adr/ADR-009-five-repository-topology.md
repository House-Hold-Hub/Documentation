# ADR-009: Five-repository topology

> **Status:** Accepted  
> **Date:** 2026-08-16  
> **Owner:** Documentation repository; cross-repository engineering governance  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Five-repository topology and responsibility boundaries  
> **Supersedes:** [ADR-001](ADR-001-multi-repository-structure.md)  
> **Superseded by:** —

## Context

ADR-001 selected a multi-repository architecture but described only Backend, Frontend, and Infrastructure. HouseHoldHub now has five first-class repositories, and shared documentation and automation need explicit ownership rather than being treated as incidental files in another repository.

The topology must preserve independent service delivery while providing one home for shared contracts and one home for reusable automation.

## Decision

Use five first-class repositories:

1. **Backend** — Django/DRF service code, executable models and migrations, backend tests, provider-neutral email adapter and templates, its service Dockerfile, and its service GitHub Actions workflow.
2. **Frontend** — React application, frontend tests, its service Dockerfile, and its service GitHub Actions workflow.
3. **Infrastructure** — deployment manifests, runtime-target configuration, managed-service provisioning, credentials and secret rotation, and provider health configuration.
4. **Automation** — reusable automation, shared policy and pipeline assets, integration-test support and fixtures, and secret scanning.
5. **Documentation** — shared product, architecture, machine-readable API contract, security, quality, and planning documentation.

Documentation owns the shared product and API contracts. Backend and Frontend must review breaking API-contract changes. Each service repository owns its implementation and service-local workflow, while Automation may supply shared assets consumed by those workflows.

The Documentation-owned [OpenAPI specification](../../api/openapi.yaml) is the sole route and wire-contract source of truth. Integration work across repositories coordinates against that contract rather than duplicating route inventories.

## Consequences

### Positive

- Shared contracts have an explicit owner independent of either consumer.
- Reusable automation and policy can evolve without conflating it with runtime infrastructure.
- Backend, Frontend, and deployment configuration retain independent histories and delivery workflows.
- Breaking API changes have a defined cross-repository review path.

### Costs and risks

- Changes spanning repositories require coordinated reviews and compatible release sequencing.
- Integration tests must obtain compatible Backend, Frontend, Infrastructure, and contract revisions.
- Repository links and ownership metadata require maintenance.
- Atomic cross-repository commits are not possible.

### Required controls

- Breaking OpenAPI changes require Documentation, Backend, and Frontend review.
- Service repositories keep service-specific Dockerfiles and workflows; Infrastructure must not become a duplicate source for them.
- Automation owns reusable assets, not the execution state of service releases.
- Live GitHub issues, not Markdown counts, remain authoritative for execution state.

## Supersession

This ADR fully supersedes ADR-001. ADR-001 remains as historical evidence of the initial multi-repository decision, but its three-repository tree and ambiguous API-specification location are non-normative.

## Related decisions

- [ADR-014: API contract governance](ADR-014-api-contract-governance.md)
- [Technology baseline](../technology-baseline.md)
- [Architecture overview](../overview.md)
