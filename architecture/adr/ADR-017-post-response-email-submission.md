# ADR-017: Post-response provider call for timing-sensitive email operations

> **Status:** Proposed  
> **Date:** 2026-10-17  
> **Owner:** Backend repository with Security and Documentation governance  
> **Last reviewed:** 2026-10-17  
> **Canonical for:** Where the bounded provider call runs when an operation's response time must not reveal whether an email is sent  
> **Supersedes:** The "synchronous" execution detail of [ADR-015](ADR-015-transactional-email-delivery.md), only for operations that need an enumeration-safe response time  
> **Superseded by:** —

## Context

[ADR-015](ADR-015-transactional-email-delivery.md) fixes the MVP email sequence: commit domain state, `transaction.on_commit()`, a bounded synchronous provider call, then a durable delivery status. It also requires password-reset requests to stay enumeration-safe "regardless of account existence or delivery outcome", and the [security model](../../security/security-model.md) adds that "response timing must not trivially disclose whether a provider call occurred for an existing account."

Those two statements conflict for `requestPasswordReset`. Only an existing, eligible account causes a provider call, so a call made inside the request makes the response slower for exactly those accounts, by up to the provider timeout when the provider is slow or failing. An attacker who submits candidate addresses can then tell which have accounts.

Two ways to keep the call synchronous with the request exist, and both are poor on the MVP topology (a few synchronous web workers, no queue or worker process):

- Pad every reset response to at least the provider timeout. Each request then holds a worker for that long, so a few requests per timeout interval starve login and every other operation.
- Run the call for unknown addresses too. There is no safe provider call to make for an address with no account.

The first Backend implementation ([Backend#36](https://github.com/House-Hold-Hub/Backend/issues/36), [PR 53](https://github.com/House-Hold-Hub/Backend/pull/53)) runs the bounded call after the HTTP response is closed, on a bounded in-process thread. That is an interpretation of ADR-015, not what it literally says, so this ADR asks for the decision explicitly.

A bound on those threads creates a second, subtler channel. If only requests for existing accounts occupy a slot, an attacker who holds all but one slot with accounts they control can ask for a candidate address and then for a controlled one: their own email is refused only if the candidate existed and took the last slot. Each HTTP response is identical, but the outcome is observable in the attacker's inbox. Slot admission and occupancy therefore have to be independent of account existence, not only the response.

## Decision

Keep the ADR-015 sequence and delivery model unchanged: domain state and a minimal `EmailDelivery` record commit together, the provider is called only after that commit, the call is bounded by the configured timeout, and the durable status is honest (`accepted` means provider acceptance only). All ADR-015 data-minimization rules, status values and reconciliation continue to apply.

For an operation whose response time must not reveal whether a provider call is made (today, `requestPasswordReset`), the Backend may run the bounded provider call after the response is closed, on a bounded thread in the web process, instead of inside the request. The following conditions are part of the decision:

1. **Bounded concurrency, no queue.** The number of such calls running at once in one process has a fixed configured limit. When no slot is free, or a thread cannot start, the call is not made and is not buffered. The refusal does no database or provider work, so it costs the same for every request. The delivery of an eligible account stays `pending`, and reconciliation settles it as not submitted. The caller sees the same response either way.
2. **Uniform admission and occupancy.** Every valid request takes one slot, whether or not the address has an account, is eligible, or has anything to submit. Each admitted request holds its slot for the same fixed duration, longer than the provider timeout, however quickly or slowly the provider answered. Admission, refusal and slot occupancy therefore depend only on how many valid requests are in flight, never on which addresses have accounts, so no caller can learn about one address from whether another of its own requests was submitted.
3. **Own resources and honest states.** Each call uses its own database connection, closed as soon as the work ends. Threads are not daemon threads, so a graceful worker shutdown waits for them, at most the slot duration each. The delivery is claimed (`submitting`) and persisted before the provider call. A process that dies during the call leaves `submitting` and one that dies before it leaves `pending`; the existing reconciliation settles these as `unknown` and `not_submitted`.
4. **Response time.** The response still takes a fixed minimum duration for every valid request, covering the few database writes only an existing account performs.
5. **No new infrastructure.** No Redis, Celery, queue or dedicated worker is introduced. Recovery of a skipped or lost email is a new request, as in ADR-015.
6. **Scope.** Every other email flow (verification, primary-email change, invitations) keeps the inline `on_commit` call, because their responses are allowed to report the delivery outcome.

## Consequences

### Positive

- A slow or failing provider, and overload, change neither the body, status nor timing of a reset request, so they cannot reveal which addresses have accounts.
- Contention for the bounded capacity reveals nothing about other addresses: a caller's own requests are admitted or refused the same way whether or not a candidate address exists.
- A web worker is never held by a provider call, so the endpoint cannot be used to starve other operations.
- No queue, broker or worker is added, and ADR-015's status and reconciliation model is reused as is.

### Costs and risks

- Under overload the Backend deliberately drops reset emails (left `pending`, then settled as not submitted). A legitimate user may have to request again, and an attacker who saturates the slots can suppress emails for others during the attack; the existing per-address and per-client limits ([ADR-016](ADR-016-authentication-launch-security-defaults.md)) bound how often that is possible. Capacity is the slot limit divided by the slot duration per process, so unknown addresses consume it too.
- Idle threads hold the slots of requests that had nothing to submit. They are few, short-lived and hold no database connection, but they are deliberate cost, paid so that occupancy reveals nothing.
- Provider-side effects shared by all recipients (the provider's own quota or latency) are inherent to sending any email and are not removed by this ADR; they are bounded by the per-address and per-client limits.
- A killed process can lose an email that was committed but not yet submitted. This is the same failure mode ADR-015 already accepts for a process that dies between commit and callback.
- The in-process thread is a second execution path beside the inline callback; the Backend must keep both covered by tests, including interruption, overload and shutdown.

### Alternatives considered

- **Inline call with a response floor at least the provider timeout.** Literally ADR-015-compliant, but it ties a worker to every reset request. Its occupancy is uniform, but with a few synchronous workers a handful of requests per timeout interval stall every other operation, where the uniform slot confines the damage to reset emails. It remains the fallback if this ADR is rejected, together with more workers.
- **Admit and occupy slots only for eligible accounts.** Rejected: it is the contention oracle described in Context.
- **Reserve slots per address or per client.** Rejected as more machinery than the fixed-duration uniform slot for the same property.
- **A queue, Celery or a worker process.** Excluded by ADR-015 and the technology baseline for the MVP.
- **Unbounded or daemon threads.** Rejected: unbounded threads and connections are a resource-exhaustion risk, and daemon threads are killed mid-call at shutdown.

## Supersession

On acceptance, ADR-015's metadata gains a `Superseded by` link to this ADR for the execution detail above only, and the [decision index](README.md) records the portion. Until then this ADR is not authoritative and ADR-015 stands as written.

## Related decisions

- [ADR-015: Transactional email delivery](ADR-015-transactional-email-delivery.md)
- [ADR-016: Authentication launch security defaults](ADR-016-authentication-launch-security-defaults.md)
- [Security model](../../security/security-model.md)
- [Technology baseline](../technology-baseline.md)
