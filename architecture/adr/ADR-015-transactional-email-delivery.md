# ADR-015: Transactional email delivery

> **Status:** Accepted  
> **Date:** 2026-08-16  
> **Owner:** Backend repository; Infrastructure owns provider provisioning  
> **Last reviewed:** 2026-08-16  
> **Canonical for:** Transactional-email commit, delivery-state, and ownership model  
> **Supersedes:** The transactional-email execution pattern in the [archived technology-choice snapshot](../../archive/2026-08-16-design-and-planning/FINAL_TECHNOLOGY_CHOICES.md) and earlier planning examples  
> **Superseded by:** —

## Context

Verification, password reset, and Household invitations require transactional email. The MVP needs recoverable delivery state and safe token handling without introducing a queue, Redis, Celery, or a dedicated worker solely for email. Sending before domain commit risks delivering a link for state that later rolls back; treating provider acceptance as inbox delivery overstates what the system knows.

## Decision

Use this MVP sequence:

> commit domain state → `transaction.on_commit()` → bounded synchronous provider call → durable delivery status

### Backend ownership

Backend owns:

- a provider-neutral email adapter;
- templates;
- token lifecycle and operation ordering;
- durable delivery state;
- resend behavior;
- safe API errors;
- audit events;
- unit, integration, and failure-path tests.

The post-commit callback must bound provider latency, handle provider exceptions, and persist an honest recoverable status. Verification and Invitation failures leave recoverable pending domain state and support rate-limited resend. Password-reset requests remain enumeration-safe regardless of account existence or delivery outcome.

Provider acceptance means only that the provider accepted the submission. It must not be represented as confirmed inbox delivery.

### Other repository ownership

- **Infrastructure:** provider provisioning; sender/domain verification; SPF, DKIM, and DMARC; credentials; secret rotation; provider health configuration.
- **Frontend:** generic password-reset confirmation; verification resend UX; Invitation resend/recovery UX where applicable.
- **Automation:** test-provider fixtures; integration-test support; secret scanning.
- **Documentation:** shared product, security, and contract requirements.

### Data minimization

Persist only the minimum delivery metadata needed for observability and recovery. Never persist:

- plaintext authentication, reset, or Invitation tokens;
- full sensitive URLs;
- rendered secret-bearing email bodies;
- unnecessary recipient PII.

### Infrastructure boundary

Do not add a queue, Redis, Celery, or a dedicated worker solely for transactional email in MVP. The exact managed provider remains deferred behind the adapter under D02.

## Consequences

### Positive

- Email is not sent for rolled-back domain state.
- Durable status supports support/recovery and rate-limited resend.
- The provider-neutral boundary prevents product behavior from depending on a vendor.
- MVP avoids operating an additional queue/worker stack solely for a low-volume integration.
- Enumeration-safe responses and minimized records reduce security/privacy exposure.

### Costs and risks

- The on-commit provider call adds bounded latency after the domain commit.
- A provider outage can leave pending work that requires user-driven resend or operational recovery.
- Process failure around the callback/status update must not be presented as successful delivery; tests must cover honest unknown/pending outcomes.
- Without a queue, the MVP does not provide automatic asynchronous retry guarantees.

## Supersession

Earlier material showed sending email inside the signup flow and sometimes described provider failure as blocking signup. This ADR supersedes that ordering and failure model. Historical provider names and latency/SLA claims are non-normative.

## Related decisions

- [Security model](../../security/security-model.md)
- [Technology baseline](../technology-baseline.md)
- [ADR-013: Invitation security](ADR-013-invitation-security.md)
