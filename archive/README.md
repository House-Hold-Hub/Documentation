# HouseHoldHub Documentation Archive

> **Status:** Accepted  
> **Owner:** Documentation repository  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Archive policy and provenance only

Archived documents are historical, non-normative snapshots. They may contain mutually contradictory decisions, obsolete versions, invalid implementation examples, unsupported targets, or status claims that were true only during a review stage.

Archived material never overrides an active PRD, ADR, domain model, OpenAPI contract, security model, quality document, repository manifest/migration, or live GitHub state. It is deliberately excluded from the canonical navigation in the repository [README](../README.md).

## 2026-08-16 design and planning archive

[`2026-08-16-design-and-planning/`](2026-08-16-design-and-planning/) preserves the complete set of pre-migration non-ADR snapshots that were replaced, merged, split, or normalized during the documentation-architecture migration. Historical ADRs remain in the active [ADR directory](../architecture/adr/README.md), where explicit status and supersession links preserve their decision lineage.

### Design and review snapshots

- `ARCHITECTURE_REVIEW.md`
- `REVIEW_EXECUTIVE_SUMMARY.md`
- `SYSTEM_DESIGN.md`
- `SYSTEM_DESIGN_REVISION_SUMMARY.md`
- `RESOLUTION_SUMMARY.md`
- `FINAL_REVIEW_COMPLETE.md`
- `DELIVERABLES_COMPLETE.md`

### Technology and data-model snapshots

- `FINAL_TECHNOLOGY_CHOICES.md`
- `DOMAIN_MODEL_FINAL.md`
- `DOMAIN_MODEL_CORRECTED.md`
- `ERD.md`

### API snapshot

- `OPENAPI.md` — fenced historical OpenAPI plus prose; replaced by [`../api/openapi.yaml`](../api/openapi.yaml)

### Product and planning snapshots

- `prd-householdhub-mvp.md` — pre-split umbrella PRD
- `PRD-REVISION-SUMMARY.md`
- `IMPLEMENTATION_PLAN.md`
- `IMPLEMENTATION_PLAN_REVISED.md`
- `GITHUB_ISSUES_PROPOSAL.md`
- `GITHUB_ISSUES_PROPOSAL_REVISED.md`
- `PLANNING_REVIEW_SUMMARY.md`

The archive preserves original filenames and content. No archived filename communicates current status.

## Referencing archived material

Canonical documents may link to an archived file only to explain provenance or supersession. Such a link must label the target as historical. Do not link an archive snapshot as a current setup guide, requirement, route contract, data model, or plan.
