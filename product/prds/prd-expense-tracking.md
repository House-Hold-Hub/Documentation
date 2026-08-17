# PRD: Expense tracking

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP household expense recording, money and currency semantics, payer behavior, incurred date, categories, editing, history, and aggregation
> Supersedes: expense requirements in the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md)

## 1. Overview

Expense tracking is a supporting MVP workflow for recording household spending. It is a shared ledger, not a settlement system. Every household has one required immutable MVP currency, and every expense snapshots that currency while storing its positive amount as ISO minor units.

## 2. Goals

- Let household collaborators record a positive expense under the permissions-matrix rule.
- Preserve unambiguous monetary meaning across ISO 4217 currencies.
- Preserve payer attribution without blocking later user deletion.
- Provide a chronological shared log, supported filters, total, and category totals.
- Keep splitting, settlement, currency change, and conversion out of MVP.

## 3. User stories

### EXP-US-001: Record an expense

**Description:** As an active member, I want to record an expense with its actual calendar date so that the household log is accurate.

**Acceptance criteria:**

- The expense requires a positive `amount_minor`, one approved category, and explicit `incurred_on`; description and payer selection are optional.
- The official frontend defaults `incurred_on` to the user's browser-local calendar date before submission.
- If payer is omitted, it defaults to the creator; any selected payer is an active member when the expense is created.
- The expense copies the household's immutable currency code and does not offer per-expense currency selection.

### EXP-US-002: Review household spending

**Description:** As an active member, I want to review and filter expenses so that I can understand recorded spending.

**Acceptance criteria:**

- All active members can view the household expense log ordered by incurred date, newest first.
- The log supports category, payer, and incurred-date filtering.
- It exposes the total and per-category totals for the matching expense set.
- All aggregated amounts share the household's one currency; no conversion occurs.

### EXP-US-003: Correct or delete an expense

**Description:** As an authorized household actor, I want to correct ordinary details or delete an expense while preserving original payer and currency meaning.

**Acceptance criteria:**

- Edit and delete actions follow their permissions-matrix rules.
- Payer and currency are immutable after creation.
- Payer deletion leaves the expense in place with a legitimate null payer reference.
- Expense deletion has no MVP recovery interface.

## 4. Functional requirements

### Monetary and currency semantics

- **EXP-FR-001:** Every household must have one required supported ISO 4217 `currency_code`, immutable through the MVP product and API.
- **EXP-FR-002:** Each expense must store `amount_minor` as a strictly positive integer and `currency_code` as an ISO 4217 code.
- **EXP-FR-003:** `amount_minor` represents the currency's minor units according to the applicable ISO currency exponent; the product must not assume every supported currency has two decimal minor units.
- **EXP-FR-004:** The backend owns validation and interpretation of supported ISO currency semantics.
- **EXP-FR-005:** On creation, the expense copies the household's currency code. For every MVP household expense, `Expense.currency_code == Household.currency_code`.
- **EXP-FR-006:** Expense currency is immutable. MVP provides neither household currency change nor per-expense currency selection.
- **EXP-FR-007:** MVP performs no exchange-rate conversion, mixed-currency aggregation, valuation-date calculation, or reporting conversion.

### Expense data and lifecycle

- **EXP-FR-008:** Expense creation must support required `amount_minor`, category, and `incurred_on`; description and payer are optional, and creation authorization is defined only by the permissions matrix.
- **EXP-FR-009:** `incurred_on` is an explicit calendar-date input. The official frontend must set its initial value from the browser-local calendar date and send it; the backend must not silently derive it from server UTC or deployment-local time.
- **EXP-FR-010:** External API clients are responsible for supplying the intended `incurred_on`; no persisted user timezone is required solely for expense creation.
- **EXP-FR-011:** The allowed categories are exactly Food, Utilities, Maintenance, Entertainment, and Other.
- **EXP-FR-012:** If payer is omitted, it defaults to the creator. A supplied payer must be an active member of the same household at creation.
- **EXP-FR-013:** Payer is immutable after creation. This rule is enforced as authorization/domain behavior, not by using `PROTECT` as a substitute.
- **EXP-FR-014:** The payer relationship is nullable and uses user-deletion behavior equivalent to `SET NULL`, so deletion does not delete or block the expense.
- **EXP-FR-015:** The authorized household expense view must order expenses by `incurred_on`, newest first.
- **EXP-FR-016:** Expense viewing must support filtering by category, payer, and incurred-date range.
- **EXP-FR-017:** The expense view must expose the total and per-category totals for the matching filtered set. All values are `amount_minor` in the one household currency.
- **EXP-FR-018:** An edit authorized by the permissions matrix may change mutable amount, category, description, and incurred date. Payer and currency remain immutable.
- **EXP-FR-019:** Expense deletion must use the permissions-matrix rule and is permanent; MVP has no expense-recovery interface.
- **EXP-FR-020:** Expense changes use pure last-write-wins and become visible through normal invalidation/refetch, page load, navigation, or manual refresh.

## 5. Authorization boundary

The canonical expense action-by-role rules are in the [permissions matrix](../permissions-matrix.md). Request/response details and aggregate schema are defined only in [OpenAPI](../../api/openapi.yaml).

## 6. Design requirements

- The official frontend accepts a human-readable positive amount and submits the corresponding `amount_minor` using the supported currency's ISO exponent.
- The UI displays the expense currency but does not offer per-expense selection.
- The log presents incurred date, amount and currency, payer when present, category, description when present, and creator attribution as defined by OpenAPI.
- Loading, empty, validation-error, authorization-denied, and mutation-error states must be handled.

## 7. Non-goals

- Multiple payers, split participants, settlement balances, or “who owes whom” calculations.
- A promise that future splitting can be introduced without data migration.
- Custom categories.
- Household currency changes, per-expense currency selection, exchange rates, conversion, valuation dates, or mixed-currency totals.
- Receipt or attachment storage.
- Expense widgets on the MVP dashboard.

Any household currency-change feature requires a dedicated product/data-model decision covering historical expenses, aggregation, conversion policy, exchange-rate source, valuation dates, and reporting.

## 8. Success and verification

- Create, local-date default, payer default/selection, view, filter, aggregate, edit, user-deletion null payer, and delete journeys meet their acceptance criteria.
- Tests cover ISO currencies with non-two-decimal exponents, zero/negative rejection, cross-household payer rejection, inactive payer rejection, immutable payer/currency, each category, and same-currency aggregation.
- Release verification follows the [testing strategy](../../quality/testing-strategy.md) and [release acceptance](../../quality/release-acceptance.md).

## 9. Legacy traceability

| Legacy ID | Canonical requirement |
|---|---|
| `FR-45` | `EXP-FR-001`–`EXP-FR-012` and the permissions matrix; legacy generic amount is now `amount_minor`, `currency_code`, and explicit `incurred_on` |
| `FR-46`–`FR-47` | `EXP-FR-012`–`EXP-FR-015` |
| `FR-48`–`FR-49` | `EXP-FR-015`–`EXP-FR-017` |
| `FR-50`–`FR-51` | `EXP-FR-013`–`EXP-FR-014`, `EXP-FR-018`–`EXP-FR-019`, and the permissions matrix; legacy `PROTECT` claims are superseded |
| `FR-52` | `EXP-FR-011` |
| Legacy `amount_cents` and single-currency assumptions | Superseded by `EXP-FR-001`–`EXP-FR-007` |
| `FR-59`–`FR-62`, `FR-67` | `EXP-FR-020` and umbrella cross-cutting requirements |

## 10. Open questions

None for MVP. Household currency change and expense splitting require separate post-MVP decisions.
