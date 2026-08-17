# ADR-014: API contract governance

> **Status:** Accepted  
> **Date:** 2026-08-16  
> **Owner:** Documentation repository; Backend and Frontend review breaking changes  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** API contract ownership, review, and compatibility governance  
> **Supersedes:** Ambiguous API-specification ownership in [ADR-001](ADR-001-multi-repository-structure.md) and competing route inventories in pre-baseline design documents  
> **Superseded by:** —

## Context

The earlier documentation repeated routes and example schemas across the PRD, system design, issue plans, and an API draft. That created incompatible authentication declarations, error codes, nullability, invitation flows, and concurrency behavior. A multi-repository system needs one machine-readable wire contract and a review rule that keeps both producers and consumers aligned.

## Decision

### Contract ownership

- The Documentation-owned machine-readable [OpenAPI specification](../../api/openapi.yaml) is the sole route and wire-contract source of truth.
- Backend owns the server implementation; Frontend owns its client integration. Neither may maintain a competing route/schema inventory as normative documentation.
- Backend and Frontend must review breaking contract changes.
- Product behavior remains authoritative in PRDs, conceptual invariants in the domain model, and executable persistence in Backend models/migrations. A conflict between artifact types must be reconciled in each proper source rather than letting one silently override another.

### Authentication and CSRF representation

- Declare session authentication at the OpenAPI root.
- Mark genuinely public operations with operation-level `security: []`.
- Document the readable CSRF cookie and `X-CSRFToken` requirement for unsafe browser requests without exposing session secrets.
- Keep OAuth and Invitation token transport details aligned with the security ADRs; OpenAPI documents only the server-visible exchange contract.

### Schema stability

- Mark always-emitted response properties as required.
- Represent legitimate null values explicitly.
- Use separate Create, Update, Summary, and Response schemas where their requiredness or writable fields differ.
- Do not make immutable fields writable in Update schemas.
- Encode the approved explicit dashboard `as_of=YYYY-MM-DD`, Expense `amount_minor`, Expense `currency_code`, and `incurred_on` contracts in OpenAPI.

### Error semantics

Use the following MVP meanings consistently:

| Status | Meaning |
|---|---|
| `400` | Request or domain validation failed |
| `401` | Authentication is required or invalid |
| `403` | The caller is in the Household but the known action is denied |
| `404` | The object does not exist or is outside the caller's Household scope |
| `409` | Duplicate Membership or another incompatible resource state |

Do not use `422` in MVP unless a later decision adopts it consistently.

MVP uses pure last-write-wins. Do not document optimistic-concurrency tokens or concurrent-edit `409 Conflict` behavior. A `409` remains valid for the incompatible states listed above.

## Consequences

### Positive

- Backend and Frontend integrate against a single reviewable contract.
- Public and authenticated operations cannot inherit the wrong security declaration silently.
- Generated types and contract tests can rely on stable response shapes.
- Error handling is consistent across features without exposing outside-scope resources.

### Costs and risks

- Contract changes must update OpenAPI before or with consumer/producer implementation changes.
- Breaking-change review adds coordination across repositories.
- Human-oriented documents must link to OpenAPI instead of copying convenient route tables.
- CI must eventually validate syntax and detect implementation drift; exact tooling remains part of D06 until selected.

## Supersession

ADR-001 is already superseded by ADR-009; this ADR specifically replaces its ambiguous statement that the API specification could live in Backend or shared documentation. Route/schema examples in historical documents remain evidence only and are not contract sources.

## Related decisions

- [ADR-009: Five-repository topology](ADR-009-five-repository-topology.md)
- [API guidance](../../api/README.md)
- [Security model](../../security/security-model.md)
- [Technology baseline](../technology-baseline.md)
