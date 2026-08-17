# PRD: Household, membership, and invitations

> **Status:** Accepted  
> Owner: Documentation repository (product ownership TBD)
> Last reviewed: 2026-08-16
> Canonical for: MVP household lifecycle, owner/member behavior, membership, email invitations, join codes, member removal, and household switching
> Supersedes: household and member requirements in the [archived umbrella MVP PRD](../../archive/2026-08-16-design-and-planning/prd-householdhub-mvp.md)

## 1. Overview

A household is the product's collaboration and authorization boundary. The MVP lets a verified user create or join multiple private households, select one active context, invite members by email, and join with a separate household code. It preserves household data through a 30-day recoverable deletion period while denying normal access immediately.

## 2. Goals

- Make household creation and joining understandable without documentation.
- Maintain exactly one owner and one membership per user/household pair.
- Support secure, recoverable email invitations for existing and new users.
- Support a simple, separately protected household join code.
- Revoke removed-member and deleted-household access immediately.
- Preserve household resources during the approved recovery window.

## 3. User stories

### HH-US-001: Create a household

**Description:** As a verified user, I want to create a household so that I can coordinate with the people I live with.

**Acceptance criteria:**

- Creation requires a household name and a supported ISO 4217 household currency code; description is optional.
- The creator becomes the authoritative owner and receives a matching owner membership atomically.
- The new household appears in the user's household selector and opens its minimal dashboard.
- The product presents clear next actions to invite a member or create a task.

### HH-US-002: Invite a person by email

**Description:** As an owner, I want to invite a specific verified email identity so that only the intended recipient can join.

**Acceptance criteria:**

- At most one pending invitation exists for the same household and normalized email.
- Sending or resending produces a high-entropy, single-use credential; resend rotates it and invalidates every prior credential and stale validated intent for that token generation.
- A delivery failure leaves recoverable pending state and supports rate-limited resend.
- The owner can list invitations and revoke one by its non-secret invitation identifier.

### HH-US-003: Continue an invitation through authentication

**Description:** As an invitee, I want the invitation to survive normal same-browser authentication and verification so that I do not have to reopen the original link.

**Acceptance criteria:**

- The fragment credential is exchanged immediately, discarded, and replaced only by a non-secret server-side invitation reference/intention.
- That intent survives signup, login, verification, and authentication-session rotation in the same browser/session.
- After authentication and verification, the system revalidates current invitation state and normalized verified-email equality, shows the approved safe preview, and requires explicit acceptance.
- Cross-device verification does not copy the pending intent. The user may return to the originating session; another session must use a current valid link, and if the original bearer was already exchanged, that means obtaining the rotated link through resend rather than replaying the consumed bearer.

### HH-US-004: Join with a household code

**Description:** As a verified authenticated user, I want to use a shared household code so that I can join without an email invitation.

**Acceptance criteria:**

- A valid current code joins the user once and makes the household available in the selector.
- Invalid and unknown codes receive a uniform response, and attempts are rate-limited.
- Regeneration immediately invalidates the previous code.
- The code is never exposed in generic household or dashboard responses.

### HH-US-005: Remove a member

**Description:** As an owner, I want to remove a member so that their household access ends immediately without deleting shared content.

**Acceptance criteria:**

- The removed member is denied on every subsequent server request for the household.
- Content they created remains in the household and remains attributed to the user while that user record exists.
- Tasks assigned through the removed membership become unassigned.
- The product does not promise a visible former-assignee name or assignment history in MVP.

### HH-US-006: Delete and recover a household

**Description:** As an owner, I want deletion to remove normal access immediately while allowing limited support recovery from mistakes.

**Acceptance criteria:**

- Owner-confirmed deletion soft-deletes the household and immediately denies normal member access.
- Memberships, invitations, tasks, shopping items, expenses, and inventory remain during the 30-day retention window.
- Only support/administration can recover the household during MVP.
- After 30 days, an idempotent purge permanently deletes the household and its retained resources.

## 4. Functional requirements

### Household and ownership

- **HH-FR-001:** Household creation must support required name and supported ISO 4217 `currency_code`, with optional description; creation authorization is defined only by the permissions matrix.
- **HH-FR-002:** Creation must set the creator as `Household.owner_id` and create the matching `owner` Membership atomically.
- **HH-FR-003:** `Household.owner_id` is the authoritative owner reference for MVP. A matching owner Membership must always exist, and owner-membership removal is forbidden.
- **HH-FR-004:** Owner and member roles are immutable in MVP. Public ownership transfer and role management are unavailable.
- **HH-FR-005:** Household update must support name and description under the permissions-matrix rule. Household currency cannot be changed through the MVP product or API.
- **HH-FR-006:** A user may be an active member of multiple households and must explicitly select the household context whose data is displayed.
- **HH-FR-007:** The member list must show member name, role, and join date.

### Membership and removal

- **HH-FR-008:** Only one Membership may exist for a given household/user pair; duplicate join attempts must not create another.
- **HH-FR-009:** Member removal must use the permissions-matrix rule, hard-delete the Membership, forbid removal of the owner Membership, and deny household access on every subsequent request.
- **HH-FR-010:** Removing a member must not delete household content they created. Tasks assigned to their removed Membership become unassigned.
- **HH-FR-011:** MVP does not preserve or display removed-assignee identity as task assignment history.
- **HH-FR-012:** Server-side revocation is immediate. Client-cached data may disappear on normal invalidation, refetch, or denied-response handling.

### Email invitations

- **HH-FR-013:** Invitation create, resend, list, and revoke actions must use the permissions-matrix rules.
- **HH-FR-014:** An invitation is bound to the recipient's canonically normalized, verified email address and has pending, accepted, revoked, or expired lifecycle state derived from its timestamps and actions.
- **HH-FR-015:** An active member must not receive a new invitation to the same household, and at most one pending invitation may exist per household/normalized email. Resend rotates the token and invalidates the prior token and any intent bound to its generation.
- **HH-FR-016:** Invitations expire 30 days after issue according to `expires_at`, are single-use, and are revoked by non-secret invitation identifier rather than by bearer token.
- **HH-FR-017:** Invitation acceptance requires a HouseHoldHub account, authentication, verified-email equality, a safe preview, and explicit acceptance.
- **HH-FR-018:** The bearer credential must be a high-entropy value carried only in the URI fragment on landing, exchanged immediately in a POST body, removed from browser-visible navigation state, and never retained after exchange. The full security rules are canonical in the [security model](../../security/security-model.md).
- **HH-FR-019:** The server stores only a cryptographic hash of the bearer credential. It must never enter server-visible paths or query strings, logs, referrers, telemetry, analytics, or persistent browser storage.
- **HH-FR-020:** Successful exchange may store only a non-secret validated reference such as `pending_invitation_id` in the server-side session. The bearer token itself must not be stored there.
- **HH-FR-021:** The validated invitation intent must remain bound to the invitation/token generation and survive normal same-browser signup, login, verification, and session rotation.
- **HH-FR-022:** Before preview or acceptance, the system must revalidate that the invitation exists and is not expired, revoked, rotated, or consumed, and that the authenticated verified email matches.
- **HH-FR-023:** Acceptance must atomically create the Membership at most once and consume the invitation.
- **HH-FR-024:** Cross-device verification updates account verification globally but does not transfer pending invitation intent between devices or sessions. The originating session may continue; a different session must use a current valid invitation link, and an already exchanged single-use bearer cannot be replayed. MVP must not add global per-user pending-invitation state solely for this case.
- **HH-FR-025:** Email comparison must use the selected Django/django-allauth stack's canonical normalization without provider-specific dot or plus-address transformations.
- **HH-FR-026:** Provider-delivery failure must leave recoverable pending invitation state and a rate-limited resend path. Provider acceptance must not be presented as confirmed inbox delivery.

### Household join code

- **HH-FR-027:** Every active household has a separate, globally unique eight-character uppercase alphanumeric bearer join code.
- **HH-FR-028:** Join-code read and regeneration must use the permissions-matrix rules. Generic household, member, and dashboard responses must omit it.
- **HH-FR-029:** Regeneration must immediately invalidate the former code.
- **HH-FR-030:** Code joining must apply the eligibility rule in the permissions matrix, require the valid current code, rate-limit attempts, and return a uniform invalid-code response.
- **HH-FR-031:** The join code is distinct from email invitations and does not inherit their recipient-email binding.

### Deletion, recovery, and owner lifecycle

- **HH-FR-032:** Household deletion must use the permissions-matrix rule and require confirmation.
- **HH-FR-033:** Deletion soft-deletes the household, immediately removes normal access, and preserves memberships and household resources for 30 days.
- **HH-FR-034:** Recovery during the retention window is support/administration-only in MVP. Successful recovery restores the preserved household, Memberships, and resources to active normal access.
- **HH-FR-035:** After 30 days, a scheduled idempotent purge must hard-delete the household and retained household resources.
- **HH-FR-036:** Owner account disablement must revoke sessions and deny authentication while retaining the User, `Household.owner_id`, and owner Membership.
- **HH-FR-037:** An owner may not be anonymized or hard-deleted while still owning an active household. Administration must first resolve every owned household through deletion or a future separately approved administrative transfer mechanism.
- **HH-FR-038:** Legal/privacy retention and anonymization behavior remains governed by bounded decision `D03`; this PRD does not create a public ownership-transfer workflow.

## 5. Authorization boundary

The canonical action-by-role rules are in the [permissions matrix](../permissions-matrix.md). Household data outside the caller's active memberships is treated as outside scope; authenticated in-household denial and wire-status behavior follow OpenAPI and the shared API conventions.

## 6. Non-goals

- Admin, restricted-member, guest, or custom roles.
- Public owner transfer, owner removal, role promotion, or demotion.
- Household discovery or search.
- Self-service recovery of a deleted household.
- Cross-device transfer of pending invitation intent.
- A global user invitation inbox introduced solely to bridge devices.
- Provider-specific email-address transformations.
- Household currency changes in the MVP.

## 7. Success and verification

- Creation, email invitation, same-browser auth/verification continuation, explicit acceptance, code join, switching, removal, soft deletion, support recovery, and purge journeys meet their acceptance criteria.
- Negative tests cover duplicate membership, wrong verified email, rotated/revoked/expired/consumed invitation, stale intent, invalid code, non-owner actions, owner removal, deleted-household access, and cross-household isolation.
- Delivery failure is recoverable without exposing sensitive tokens or falsely claiming delivery.
- Verification follows the [testing strategy](../../quality/testing-strategy.md) and [release acceptance](../../quality/release-acceptance.md).

## 8. Legacy traceability

| Legacy ID | Canonical requirement |
|---|---|
| `FR-8`–`FR-12`, `FR-15` | `HH-FR-001`–`HH-FR-007` and the permissions matrix |
| `FR-13`–`FR-14` | `HH-FR-032`–`HH-FR-035` (30-day window and support-only recovery now explicit) |
| `FR-16`–`FR-19` | `HH-FR-013`–`HH-FR-031` and the permissions matrix (transport, verification, resend, and code protections expanded) |
| `FR-20`–`FR-23`, `FR-25`–`FR-26` | `HH-FR-007`–`HH-FR-012` and the permissions matrix |
| `FR-24` | `HH-FR-010`–`HH-FR-011`; visible removed-assignee history is superseded and post-MVP |
| Legacy owner-deletion text | `HH-FR-036`–`HH-FR-038` |

## 9. Open questions

No unresolved semantic blocker. Jurisdiction and retention details remain bounded decision `D03` under the [roadmap](../roadmap.md).
