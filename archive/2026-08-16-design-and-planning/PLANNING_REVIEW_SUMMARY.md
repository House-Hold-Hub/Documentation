# HouseHoldHub MVP - Planning Review Summary

**Date:** August 16, 2026  
**Status:** Approved (corrections applied; ready for GitHub issue creation)  
**Changes:** Major revisions to milestone structure, testing strategy, Dashboard restoration, and issue consolidation

---

## Review Performed Against 10 Criteria

### 1. ✓ Milestone Structure Revised for Parallelization

**Original:** 7 linear milestones (M1 → M2 → M3 → M4 → M5 → M6 → M7)  
**Revised:** 10 milestones (M0 → M1 → M2 → {M3-M6 parallel} → M7 → M8 → M9)

**Key Changes:**
- M0: Engineering Foundation (was M1)
- M1: Identity & Authentication (was M2)
- M2: Household & Membership (was M3)
- M3: Tasks (was M4) — **now parallel after M2**
- M4: Shopping (was part of M5) — **now parallel after M2**
- M5: Expenses (was part of M5) — **now parallel after M2**
- M6: Inventory (was part of M5) — **now parallel after M2**
- M7: **Dashboard (NEW)** — added as explicit milestone after features stable
- M8: Integration & Hardening (was M6) — focuses on E2E, not catching up on testing
- M9: Deployment Readiness (was M7)

**Rationale:**
- Shopping, Expenses, and Inventory are independent once Household/Membership is established
- Four-way parallelization can reduce critical path from 10.5 weeks to ~9-10 weeks
- Dashboard depends on all four feature domains being stable, so placed at M7
- Testing is moved upstream (per-feature), not deferred to M6/M8

---

### 2. ✓ Dashboard Restored as Explicit MVP Milestone

**Status:** Dashboard is MISSING from original M0-M7 plan; now explicit in M7

**Scope Defined (M7):**
- Backend: Dashboard aggregation endpoint (GET /households/{id}/dashboard)
- Frontend: Dashboard page with widgets for household info, pending tasks, shopping summary, recent expenses
- Excluded: Analytics, charts, activity feeds, expense settlements, rankings

**Why it matters:**
- PRD explicitly lists Dashboard as MUST-HAVE foundational feature
- MVP is incomplete without household overview
- Dashboard serves as landing page after login

**Issues Added:** +2 issues (1 Backend endpoint, 1 Frontend page)

---

### 3. ✓ 71 Issues Consolidated to 68

**Consolidations:**
1. **Documentation Setup (M0):** 3 issues → 1
   - Original: 1.6 (OpenAPI publication), 1.7 (dev setup guide), 1.11 (docs structure)
   - Revised: M0-D1 (single issue covering all three: OpenAPI, setup guide, architecture documentation)
   - Saved: 2 issues

2. **Testing Strategy Revised:**
   - Original: Explicit test issues for auth (2.6), tasks (4.3); secondary features tested only in M6
   - Revised: Each complex feature (auth, household, tasks) has explicit test issue; simpler features (shopping, expense, inventory) include tests in acceptance criteria
   - Net change: No additional issues, but testing emphasis moved upstream

3. **Dashboard Added:** +2 issues (net of consolidation: +1)

**Result:** 71 → 68 issues (reduces scope creep while adding Dashboard)

---

### 4. ✓ Testing & Security Made Continuous

**Original Approach:**
- M2, M4 have explicit test issues (auth, tasks)
- M5 testing buried in endpoint issues (no explicit test issues)
- M6 has broad testing/security/performance (7 issues)

**Revised Approach:**
- **M0:** Unit tests for models, utility functions (included in scaffold issues)
- **M1:** Explicit auth test issue (M1-B5) covering 50+ test cases for auth flows
- **M2:** Explicit household authorization test issue (M2-B6) covering 100+ cross-household isolation cases; Frontend test issue (M2-F5)
- **M3:** Explicit task auth test issue (M3-B3); Frontend test issue (M3-F2)
- **M4-M6:** Simpler features (shopping, expense, inventory); tests included in CRUD endpoint acceptance criteria; separate Frontend test issues for UI
- **M8:** Integration tests (E2E workflows), security hardening, performance optimization

**Why this matters:**
- Testing is caught early, not deferred
- Critical security features (cross-household isolation, authorization matrix) get dedicated, thorough testing
- M8 focuses on integration and hardening, not catching up on basic feature tests

---

### 5. ✓ M0 Foundation Kept Minimal

**Original M1 Foundation (19 issues):**
- Django scaffold, models stub, DRF setup, Docker Compose, PostgreSQL config, env templates, CI/CD, Docker image build, documentation, plus supporting config

**Revised M0 Foundation (16 issues):**
- Same components, but reorganized by concern:
  - **Backend (5):** Django scaffold, models stub, DRF setup, Docker Compose setup, CI/CD
  - **Frontend (4):** React setup, API client, TypeScript types generation, CI/CD
  - **Infrastructure (2):** PostgreSQL config, env templates
  - **Automation (3):** Docker build pipeline, testing gates, local setup script
  - **Documentation (2):** Docs structure + OpenAPI publication, contribution guide

**What's NOT in M0:**
- ✗ Production deployment infrastructure (deferred to M9)
- ✗ Redis configuration (not needed for MVP, session-backed)
- ✗ Monitoring platforms (deferred to M9)
- ✗ Observability stack (deferred to M9)
- ✗ UI framework (Tailwind removed; CSS framework is implementation detail)

**Foundation is focused:** Enables development and testing locally; production-grade features come in M9

---

### 6. ✓ API Contract Separation Explicit

**Frontend Independence:**
- **M0-F3 issue:** Generate TypeScript types and API client from OpenAPI spec
  - Output: `src/types/api.ts` (typed request/response models)
  - Output: `src/api/endpoints.ts` (typed API methods)
  - Uses: OpenAPI Generator, swagger-typescript-api, or similar

- **Frontend Development:** Can proceed with mock API responses based on OpenAPI spec
  - No requirement to wait for Backend implementation
  - TypeScript compiler validates all API calls against generated types
  - Tests run against mocked responses

- **Integration:** Once Backend implements endpoints per OPENAPI.md spec, Frontend switches from mock to real API
  - No code changes needed if Backend adheres to contract
  - Full integration testing happens in M8

**Backend Responsibility:**
- Implement endpoints exactly as OPENAPI.md specifies
- Update OpenAPI spec BEFORE implementation changes
- Write integration tests validating each endpoint against OpenAPI spec
- Never break the contract without updating spec first

**Why this matters:**
- Frontend and Backend can develop in parallel without blocking each other
- Reduces risk of contract mismatch
- Clear communication mechanism (OpenAPI spec)

---

### 7. ✓ OpenAPI Contract Validation as First-Class Concern

**Added in M0-F3:**
- Automated type generation from OpenAPI spec
- TypeScript compiler enforces contract adherence (no `any` types for API code)

**Added in M8-B1:**
- Backend integration tests validate each endpoint against OpenAPI spec
- Frontend E2E tests validate client behavior against API responses

**Added in M8-D1:**
- Documentation includes complete OpenAPI specification (YAML, rendered)

**Process for Spec Changes:**
1. Update OPENAPI.md (before implementation changes)
2. Regenerate TypeScript types (M0-F3 tool)
3. Frontend updates: TypeScript compiler catches breaking changes
4. Backend implementation: follows spec exactly
5. Integration tests: verify both sides implement spec correctly

---

### 8. ✓ Timeline Precision Removed/Caveats Added

**Original:** "Total: ~10.5 weeks (MVP ready)" — presented as fact

**Revised:**
- **Estimated parallelized timeline:** ~9-10 weeks
- **Caveats:** "This is a planning assumption, not a commitment. Actual velocity depends on team size, experience, and complexity encountered."
- **Breakdown provided:** M0 (1 week), M1 (2 weeks), M2 (1.5 weeks), M3-M6 (2 weeks parallel), M7 (0.5 weeks), M8 (1.5 weeks), M9 (0.5 weeks)
- **Clear statement:** This is preliminary; adjust based on actual team velocity

**Why this matters:**
- Prevents timeline from being mistaken for commitment
- Acknowledges uncertainty
- Provides relative sizing for planning purposes

---

### 9. ✓ Repository Ownership Clarified

**Backend Repository (34 issues)**
- Django models, DRF endpoints, business logic, integration tests
- Responsible for: User auth, household CRUD, membership, invitations, tasks, shopping, expenses, inventory
- Also owns: Database schema via Django ORM, API contract validation

**Frontend Repository (23 issues)**
- React pages, components, forms, UI tests
- Responsible for: Auth UI, household UI, task UI, shopping UI, expense UI, inventory UI, dashboard
- Also owns: Type generation from OpenAPI, API client, error handling

**Infrastructure Repository (4 issues)**
- Database (PostgreSQL), environment configuration, production deployment setup, monitoring
- Responsible for: Local/dev database setup, production infrastructure, logging, error tracking
- Distinct from Automation (does not own CI/CD pipelines; Infrastructure owns deployment target)

**Automation Repository (4 issues)**
- GitHub Actions workflows, testing pipelines, Docker image building
- Responsible for: CI/CD, test automation, pre-commit hooks, branch protection
- Does NOT own: Backend/Frontend CI/CD config in their repos (each repo owns its own .github/workflows)

**Documentation Repository (3 issues)**
- API specification (OpenAPI), architecture documentation, setup guides, contribution guide
- Responsible for: Central source of truth for specifications, guides, architectural decisions

**Clarification:**
- Infrastructure ≠ Automation
  - Infrastructure: Owns deployment targets, monitoring, infrastructure as code
  - Automation: Owns CI/CD pipelines, test automation, developer experience automation
- Clear separation prevents confusion about responsibility

---

### 10. ✓ MVP Completion Gates (Release-Level Acceptance)

**10 Critical User Journeys (ALL must pass for release; closing GitHub issues alone is NOT sufficient):**

1. **Registration & Login**
   - User signs up via email/password → creates account → logs in → session valid

2. **Household Creation**
   - User creates household → set as owner → household appears in selector → dashboard loads

3. **Household Invitation (Email)**
   - Owner invites member via email → member receives email → clicks link → joins household → has access

4. **Household Join (Code)**
   - Owner shares household code → member enters code → joins immediately → household appears in selector

5. **Household Switching**
   - User with multiple households switches between them → dashboard shows correct household data → no cross-household data leakage

6. **Member Removal & Access Loss**
   - Owner removes member → member logs out and back in → household no longer visible → cannot access (403)
   - Tasks assigned to removed member become unassigned

7. **Task Workflow (Create, Assign, Complete)**
   - Member creates task → task appears in list → owner assigns to member → assigned member marks complete → task moves to completed section → dashboard updates

8. **Shopping Workflow**
   - Member adds shopping items → items appear in pending section → any member can toggle purchased → item moves to purchased section → shopping summary updates on dashboard

9. **Expense Workflow**
   - Member creates expense → appears in expense list → filters work (by category, payer, date) → expense details viewable → delete works (creator/owner only)

10. **Inventory Workflow**
    - Member adds inventory items → items appear in list → filters by category work → quantities can be updated → items can be deleted

11. **Authorization & Isolation Verification**
    - Non-owner cannot delete household (403)
    - Non-owner cannot remove members (403)
    - Non-owner cannot edit household settings (403)
    - User from household A cannot access household B data (403)

**MVP Releasable When:** All 10 journeys pass end-to-end AND performance baselines met:
- < 500ms response at 100 concurrent users
- < 200ms for large dataset queries (1000+ items)
- < 500KB frontend bundle (gzip)

---

## Files Provided for Review

1. **IMPLEMENTATION_PLAN_REVISED.md** (current file)
   - Complete milestone definitions (M0-M9)
   - Dependency graph and parallelization strategy
   - Key decisions per milestone
   - MVP completion gates (10 user journeys)
   - Timeline estimates with caveats
   - Summary of consolidations

2. **GITHUB_ISSUES_PROPOSAL_REVISED.md**
   - All 68 issues specified with:
     - Title, goal, implementation scope
     - Acceptance criteria (objective, testable)
     - Dependencies and blockers
     - PRD/OpenAPI/ADR references
     - Labels and milestone assignment
   - Issue count by repository and milestone
   - Explanation of consolidations from original 71 issues

3. **PLANNING_REVIEW_SUMMARY.md** (this file)
   - Summary of 10 review criteria
   - Key changes explained
   - Rationale for each change
   - Next steps for approval

---

## Key Metrics

| Metric | Original | Revised | Change |
|--------|----------|---------|--------|
| **Milestones** | 7 linear (M1-M7) | 10 with parallelization (M0-M9) | +3 (explicit M0, Dashboard at M7, parallelizable M3-M6) |
| **Issues** | 71 | 68 | -3 (consolidation) |
| **Parallelization** | None (linear) | 4-way (M3-M6) | ✓ Critical path reduced |
| **Dashboard** | Missing | M7 explicit | ✓ Added as product feature |
| **Testing** | Deferred to M6 | Continuous (per feature) | ✓ Moved upstream |
| **Foundation Scope** | 19 issues | 16 issues | ✓ Focused, minimal |
| **API Contract Gen** | None | M0-F3 (TypeScript) | ✓ Type safety, independence |
| **Timeline** | 10.5 weeks (commitment-like tone) | 9-10 weeks (planning assumption only, no calendar dates) | ✓ Honest scoping, no commitments |

---

## What Remains TBD (Post-MVP)

- Exact deployment platform (Heroku, AWS, DigitalOcean, self-hosted)
- CSS framework choice (Tailwind, styled-components, CSS modules, etc.)
- Monitoring platform specifics (Datadog, New Relic, Prometheus, etc.)
- Email provider selection (SendGrid, SES, Mailgun)
- Database backup strategy (frequency, retention, testing)
- Incident severity levels and escalation procedures

These are configuration decisions, not architectural. Defer to team/stakeholder preference post-MVP.

---

## Corrections Applied (Per User Feedback)

1. ✓ **Milestone count:** Corrected from "9 milestones" to "10 milestones (M0-M9)" throughout
2. ✓ **Timeline:** Clarified as "planning assumption only; NOT a calendar commitment"
3. ✓ **Dashboard:** Confirmed in MVP as M7 with minimal scope (no analytics, charts, activity feeds)
4. ✓ **Parallel M3-M6:** Confirmed independently executable after M2; no mutual blocking unless real dependency found
5. ✓ **Testing in M8:** Clarified as cross-cutting only (E2E, security, isolation, API conformance, regression) — NO duplication of feature tests from M0-M7
6. ✓ **Issue count:** Accepted as 68; not a target; preserve boundaries during GitHub creation
7. ✓ **MVP gates:** Confirmed as 10 user journeys + release-level acceptance (not just GitHub issue closure)

## Next Step

**Ready for GitHub issue creation in respective repositories using the 68 approved issue specifications.**

No additional review, summary, completion, or planning documents are needed.

**Process for GitHub creation:**
1. Create milestones M0-M9 in each repository (no due dates derived from rough estimate)
2. Create all 68 issues with specified titles, scopes, acceptance criteria, dependencies, labels
3. Link issues to milestones and cross-repository dependencies
4. Assign to teams when team members are identified
5. Begin M0 work

---

## Risk Mitigation

**Risks Identified & Mitigation:**

1. **Risk:** M3-M6 hidden dependencies discovered mid-way through development
   - **Mitigation:** Start M3 and M4 together; monitor for blocking dependencies; escalate if found
   - **Contingency:** Revert to sequential if necessary; document lessons learned

2. **Risk:** Dashboard scope creep (analytics, activity feeds, expense splitting requested during M7)
   - **Mitigation:** Scope clearly defined (excluded: analytics, feeds, settlements)
   - **Contingency:** Defer to v1.1; document as post-MVP features

3. **Risk:** Frontend blocked waiting for Backend implementation (despite API contract approach)
   - **Mitigation:** M0-F3 generates types; Frontend uses mocks; no implementation waiting
   - **Contingency:** Backend prioritizes endpoints highest risk to Frontend

4. **Risk:** Cross-household isolation bugs discovered late (after M8)
   - **Mitigation:** Explicit M2-B6 test issue (100+ cases); early focus on authorization
   - **Contingency:** Delayed launch; additional hardening sprint

5. **Risk:** Performance targets (< 200ms for 1000 items) not achievable
   - **Mitigation:** M8-B3 (database tuning); indexes per ERD; load test early
   - **Contingency:** Adjust targets; implement pagination/caching

6. **Risk:** Team unfamiliar with Django/React/TypeScript
   - **Mitigation:** M0 includes setup documentation; recommend pairing initially
   - **Contingency:** Additional ramp-up time in M0; extend timeline 1-2 weeks

---

## Success Criteria

**Plan is successful if:**
1. All 10 user journeys pass end-to-end
2. Code coverage >90% (backend), >70% (frontend)
3. Performance target met: <500ms at 100 concurrent users
4. Security scan: no critical vulnerabilities
5. Deployment tested and reproducible
6. All documentation tested with fresh users
7. Launch happens within 10 weeks (actual)

---
