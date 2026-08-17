# HouseHoldHub MVP - OpenAPI Specification

**Version:** 1.0.0  
**Date:** August 16, 2026  
**Status:** Ready for implementation

---

## Overview

Complete OpenAPI 3.0 specification for HouseHoldHub MVP REST API.

---

## OpenAPI Document (YAML)

```yaml
openapi: 3.0.0
info:
  title: HouseHoldHub MVP API
  version: 1.0.0
  description: Collaborative household management API
  contact:
    name: HouseHoldHub Team
  license:
    name: MIT

servers:
  - url: http://localhost:8000/api/v1
    description: Development
  - url: https://api.householdhub.example.com/api/v1
    description: Production

tags:
  - name: Authentication
    description: User authentication and account management
  - name: Households
    description: Household CRUD and management
  - name: Members
    description: Household membership and invitations
  - name: Tasks
    description: Task/chore management
  - name: Shopping
    description: Shopping list management
  - name: Expenses
    description: Expense tracking
  - name: Inventory
    description: Household inventory
  - name: Dashboard
    description: Aggregated household overview

components:
  securitySchemes:
    sessionAuth:
      type: apiKey
      in: cookie
      name: sessionid
      description: Django session-based authentication

  schemas:
    # ===== Common =====
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          enum: [VALIDATION_ERROR, AUTHENTICATION_ERROR, AUTHORIZATION_ERROR, NOT_FOUND, CONFLICT, INTERNAL_ERROR]
        message:
          type: string
        fields:
          type: object
          additionalProperties:
            type: string

    Pagination:
      type: object
      properties:
        page:
          type: integer
          minimum: 1
          default: 1
        limit:
          type: integer
          minimum: 1
          maximum: 100
          default: 20
        total:
          type: integer

    # ===== User =====
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        created_at:
          type: string
          format: date-time

    UserSignUp:
      type: object
      required:
        - email
        - password
        - name
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 10
        name:
          type: string

    UserLogin:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          format: email
        password:
          type: string

    PasswordReset:
      type: object
      required:
        - email
      properties:
        email:
          type: string
          format: email

    PasswordResetConfirm:
      type: object
      required:
        - token
        - new_password
      properties:
        token:
          type: string
        new_password:
          type: string
          minLength: 10

    # ===== Household =====
    Household:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        description:
          type: string
        code:
          type: string
        owner_id:
          type: string
          format: uuid
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    HouseholdCreate:
      type: object
      required:
        - name
      properties:
        name:
          type: string
        description:
          type: string

    HouseholdUpdate:
      type: object
      properties:
        name:
          type: string
        description:
          type: string

    # ===== Membership =====
    Membership:
      type: object
      properties:
        id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        user_name:
          type: string
          readOnly: true
        role:
          type: string
          enum: [owner, member]
        joined_at:
          type: string
          format: date-time

    MembershipInvite:
      type: object
      required:
        - email
      properties:
        email:
          type: string
          format: email

    HouseholdJoin:
      type: object
      required:
        - code
      properties:
        code:
          type: string

    # ===== Invitation =====
    Invitation:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        state:
          type: string
          enum: [pending, accepted, revoked, expired]
        created_at:
          type: string
          format: date-time
        expires_at:
          type: string
          format: date-time

    InvitationAccept:
      type: object
      required:
        - token
      properties:
        token:
          type: string

    # ===== Task =====
    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
        description:
          type: string
        due_date:
          type: string
          format: date
        assigned_to_id:
          type: string
          format: uuid
        assigned_to_name:
          type: string
          readOnly: true
        completed:
          type: boolean
        completed_by_id:
          type: string
          format: uuid
        completed_at:
          type: string
          format: date-time
        created_by_id:
          type: string
          format: uuid
        created_by_name:
          type: string
          readOnly: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    TaskCreate:
      type: object
      required:
        - title
      properties:
        title:
          type: string
        description:
          type: string
        due_date:
          type: string
          format: date
        assigned_to_id:
          type: string
          format: uuid

    TaskUpdate:
      type: object
      description: >
        title/description/due_date may be changed by any household member.
        assigned_to_id is field-level restricted: only the task's creator or the
        Household Owner may include/change it. A non-creator, non-owner member
        submitting a request that changes assigned_to_id receives 403 Forbidden;
        the same request without assigned_to_id succeeds for ordinary fields.
      properties:
        title:
          type: string
        description:
          type: string
        due_date:
          type: string
          format: date
        assigned_to_id:
          type: string
          format: uuid
          nullable: true
          description: "Restricted field — creator or Household Owner only. See schema description."

    TaskComplete:
      type: object
      description: >
        completed=true marks the task done; completed=false un-marks it (both
        directions use the same request body and the same authorization rule).
        Authorization: if the task has an assignee, only that assigned member or
        the Household Owner may change completed. If the task is unassigned, any
        active household member may change completed. completed_at is set to the
        current time when completed becomes true, and cleared (null) when
        completed becomes false — it is not immutable.
      required:
        - completed
      properties:
        completed:
          type: boolean

    # ===== Shopping Item =====
    ShoppingItem:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        quantity:
          type: string
        purchased:
          type: boolean
        purchased_by_id:
          type: string
          format: uuid
        purchased_by_name:
          type: string
          readOnly: true
        purchased_at:
          type: string
          format: date-time
        created_by_id:
          type: string
          format: uuid
        created_by_name:
          type: string
          readOnly: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    ShoppingItemCreate:
      type: object
      required:
        - name
      properties:
        name:
          type: string
        quantity:
          type: string

    ShoppingItemUpdate:
      type: object
      properties:
        name:
          type: string
        quantity:
          type: string
        purchased:
          type: boolean

    # ===== Expense =====
    Expense:
      type: object
      properties:
        id:
          type: string
          format: uuid
        amount_cents:
          type: integer
        category:
          type: string
          enum: [Food, Utilities, Maintenance, Entertainment, Other]
        payer_id:
          type: string
          format: uuid
        payer_name:
          type: string
          readOnly: true
        description:
          type: string
        created_by_id:
          type: string
          format: uuid
        created_by_name:
          type: string
          readOnly: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    ExpenseCreate:
      type: object
      required:
        - amount_cents
        - category
      properties:
        amount_cents:
          type: integer
          minimum: 0
        category:
          type: string
          enum: [Food, Utilities, Maintenance, Entertainment, Other]
        payer_id:
          type: string
          format: uuid
        description:
          type: string

    ExpenseUpdate:
      type: object
      properties:
        amount_cents:
          type: integer
          minimum: 0
        category:
          type: string
          enum: [Food, Utilities, Maintenance, Entertainment, Other]
        description:
          type: string

    # ===== Inventory Item =====
    InventoryItem:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        quantity:
          type: integer
          minimum: 1
        unit:
          type: string
          nullable: true
          description: 'Free-form display metadata, e.g. "boxes", "bottles". Not stored in quantity.'
        category:
          type: string
        location:
          type: string
        created_by_id:
          type: string
          format: uuid
        created_by_name:
          type: string
          readOnly: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    InventoryItemCreate:
      type: object
      required:
        - name
        - quantity
      properties:
        name:
          type: string
        quantity:
          type: integer
          minimum: 1
        unit:
          type: string
          nullable: true
        category:
          type: string
        location:
          type: string

    InventoryItemUpdate:
      type: object
      properties:
        name:
          type: string
        quantity:
          type: integer
          minimum: 1
        unit:
          type: string
          nullable: true
        category:
          type: string
        location:
          type: string

    # ===== List Responses =====
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'

    HouseholdList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Household'
        meta:
          $ref: '#/components/schemas/Pagination'

    TaskList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Task'
        meta:
          $ref: '#/components/schemas/Pagination'

    ShoppingItemList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/ShoppingItem'
        meta:
          $ref: '#/components/schemas/Pagination'

    ExpenseListMeta:
      description: >
        Pagination fields plus aggregates computed over ALL expenses matching the
        current filters (category/payer_id/date_from/date_to), not just the
        current page. Satisfies FR-49 (total + per-category breakdown).
      allOf:
        - $ref: '#/components/schemas/Pagination'
        - type: object
          properties:
            total_cents:
              type: integer
              description: Sum of amount_cents across all filtered expenses
            by_category:
              type: object
              description: Sum of amount_cents per category, across all filtered expenses
              additionalProperties:
                type: integer

    ExpenseList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Expense'
        meta:
          $ref: '#/components/schemas/ExpenseListMeta'

    InventoryItemList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/InventoryItem'
        meta:
          $ref: '#/components/schemas/Pagination'

    MembershipList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Membership'

    InvitationList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Invitation'

    # ===== Dashboard =====
    DashboardResponse:
      type: object
      properties:
        household:
          $ref: '#/components/schemas/Household'
        member_count:
          type: integer
        members:
          type: array
          items:
            $ref: '#/components/schemas/Membership'
        pending_tasks:
          type: array
          description: Up to 3 open tasks (due-soon/overdue first)
          maxItems: 3
          items:
            $ref: '#/components/schemas/Task'
        shopping_pending_count:
          type: integer
          description: Count of shopping items with purchased=false
        recent_expenses:
          type: array
          description: Up to 5 most recent expenses
          maxItems: 5
          items:
            $ref: '#/components/schemas/Expense'
        expenses_total_cents:
          type: integer
          description: Sum of all household expense amounts, in cents

# ===== PATHS =====
paths:
  # Authentication
  /auth/signup:
    post:
      tags:
        - Authentication
      summary: Sign up new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserSignUp'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '422':
          description: Email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/login:
    post:
      tags:
        - Authentication
      summary: Log in user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserLogin'
      responses:
        '200':
          description: Login successful
          headers:
            Set-Cookie:
              schema:
                type: string
                example: sessionid=abc123; Path=/; HttpOnly; Secure; SameSite=Strict
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  households:
                    type: array
                    items:
                      $ref: '#/components/schemas/Household'
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/logout:
    post:
      tags:
        - Authentication
      summary: Log out user
      security:
        - sessionAuth: []
      responses:
        '200':
          description: Logout successful
          headers:
            Set-Cookie:
              schema:
                type: string
                example: sessionid=; Path=/; HttpOnly; Max-Age=0
        '401':
          description: Not authenticated

  /auth/me:
    get:
      tags:
        - Authentication
      summary: Get current user
      security:
        - sessionAuth: []
      responses:
        '200':
          description: Current user
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: Not authenticated

  /auth/forgot-password:
    post:
      tags:
        - Authentication
      summary: Request password reset
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordReset'
      responses:
        '200':
          description: Password reset email sent
        '400':
          description: Invalid request

  /auth/reset-password:
    post:
      tags:
        - Authentication
      summary: Reset password with token
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordResetConfirm'
      responses:
        '200':
          description: Password reset successful
        '400':
          description: Invalid or expired token

  /auth/google:
    get:
      tags:
        - Authentication
      summary: Start Google OAuth flow
      description: >
        Browser-navigated redirect endpoint (not an XHR/JSON call). Redirects the
        user agent to Google's OAuth consent screen.
      responses:
        '302':
          description: Redirect to Google's OAuth consent screen
          headers:
            Location:
              schema:
                type: string
                format: uri

  /auth/google/callback:
    get:
      tags:
        - Authentication
      summary: Google OAuth callback
      description: >
        Browser-navigated redirect endpoint invoked by Google after consent (not an
        XHR/JSON call). Creates or updates the User record, starts a session
        (Set-Cookie: sessionid), and redirects to the Frontend.
      parameters:
        - name: code
          in: query
          required: true
          schema:
            type: string
        - name: state
          in: query
          required: false
          schema:
            type: string
      responses:
        '302':
          description: Session established; redirect to Frontend
          headers:
            Set-Cookie:
              schema:
                type: string
                example: sessionid=abc123; Path=/; HttpOnly; Secure; SameSite=Strict
            Location:
              schema:
                type: string
                format: uri
        '401':
          description: OAuth exchange failed (invalid code/state)

  # Households
  /households:
    get:
      tags:
        - Households
      summary: List user's households
      security:
        - sessionAuth: []
      responses:
        '200':
          description: List of households
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HouseholdList'
        '401':
          description: Not authenticated

    post:
      tags:
        - Households
      summary: Create new household
      security:
        - sessionAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HouseholdCreate'
      responses:
        '201':
          description: Household created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Household'
        '400':
          description: Validation error
        '401':
          description: Not authenticated

  /households/{id}:
    get:
      tags:
        - Households
      summary: Get household details
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Household details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Household'
        '401':
          description: Not authenticated
        '403':
          description: Not a member of this household
        '404':
          description: Household not found

    patch:
      tags:
        - Households
      summary: Update household (owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HouseholdUpdate'
      responses:
        '200':
          description: Household updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Household'
        '403':
          description: Only owner can update
        '404':
          description: Household not found

    delete:
      tags:
        - Households
      summary: Delete household (owner only, soft-delete)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Household soft-deleted
        '403':
          description: Only owner can delete
        '404':
          description: Household not found

  /households/{id}/code:
    get:
      tags:
        - Households
      summary: Get household join code
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Household code
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: string

    post:
      tags:
        - Households
      summary: Regenerate household code (owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: New code generated
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: string
        '403':
          description: Only owner can regenerate

  # Members
  /households/{id}/members:
    get:
      tags:
        - Members
      summary: List household members
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: List of members
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MembershipList'
        '403':
          description: Not a member

    post:
      tags:
        - Members
      summary: Invite member by email (owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MembershipInvite'
      responses:
        '201':
          description: Invitation sent
        '403':
          description: Only owner can invite
        '422':
          description: Email already member or invalid

  /households/{id}/members/{user_id}:
    delete:
      tags:
        - Members
      summary: Remove member (owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: user_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Member removed
        '403':
          description: Only owner can remove
        '404':
          description: Member not found

  /households/join:
    post:
      tags:
        - Members
      summary: Join household by code
      description: >
        The caller supplies only the household code (they do not know the household's
        UUID in advance); the server resolves the target household from the code.
        This endpoint intentionally has no {id} path parameter.
      security:
        - sessionAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HouseholdJoin'
      responses:
        '200':
          description: Joined household
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Household'
        '404':
          description: Invalid code
        '422':
          description: Already a member

  # Invitations
  /households/{id}/invitations:
    get:
      tags:
        - Members
      summary: List pending invitations (owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: List of invitations
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvitationList'
        '403':
          description: Only owner can view

  /households/{id}/invitations/{token}/accept:
    post:
      tags:
        - Members
      summary: Accept email invitation
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: token
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Invitation accepted
        '404':
          description: Invalid or expired invitation
        '422':
          description: Invitation already used or revoked

  /households/{id}/invitations/{token}:
    delete:
      tags:
        - Members
      summary: Revoke invitation (owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: token
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Invitation revoked
        '403':
          description: Only owner can revoke

  # Tasks
  /households/{id}/tasks:
    get:
      tags:
        - Tasks
      summary: List household tasks
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: completed
          in: query
          schema:
            type: boolean
        - name: assigned_to_id
          in: query
          schema:
            type: string
            format: uuid
        - name: due_before
          in: query
          description: Return tasks with due_date on or before this date
          schema:
            type: string
            format: date
        - name: due_after
          in: query
          description: Return tasks with due_date on or after this date
          schema:
            type: string
            format: date
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskList'

    post:
      tags:
        - Tasks
      summary: Create task
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'

  /households/{id}/tasks/{task_id}:
    get:
      tags:
        - Tasks
      summary: Get task details
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: task_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Task details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          description: Task not found

    patch:
      tags:
        - Tasks
      summary: Update task
      description: >
        Any household member may update title/description/due_date. Changing
        assigned_to_id is restricted to the task's creator or the Household Owner
        (see TaskUpdate schema) — a request from another member that includes a
        changed assigned_to_id is rejected with 403, even though the same request
        without that field would succeed.
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: task_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '403':
          description: Not authorized to edit, or attempted to change assigned_to_id without being creator/owner

    delete:
      tags:
        - Tasks
      summary: Delete task (creator/owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: task_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Task deleted
        '403':
          description: Not authorized

  /households/{id}/tasks/{task_id}/complete:
    patch:
      tags:
        - Tasks
      summary: Mark task complete or un-complete
      description: >
        Sets or clears the task's completed status (see TaskComplete schema for
        the request body). Authorization: assigned member or Household Owner if
        the task has an assignee; any active household member if the task is
        unassigned. This applies symmetrically to un-completing.
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: task_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskComplete'
      responses:
        '200':
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '403':
          description: Not authorized (not the assigned member/owner, or task is unassigned and caller is not an active household member)

  # Shopping
  /households/{id}/shopping:
    get:
      tags:
        - Shopping
      summary: List shopping items
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: purchased
          in: query
          schema:
            type: boolean
      responses:
        '200':
          description: List of shopping items
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ShoppingItemList'

    post:
      tags:
        - Shopping
      summary: Add shopping item
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ShoppingItemCreate'
      responses:
        '201':
          description: Item added
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ShoppingItem'

  /households/{id}/shopping/{item_id}:
    patch:
      tags:
        - Shopping
      summary: Update shopping item
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: item_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ShoppingItemUpdate'
      responses:
        '200':
          description: Item updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ShoppingItem'

    delete:
      tags:
        - Shopping
      summary: Delete shopping item (creator/owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: item_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Item deleted

  /households/{id}/shopping/purchased:
    delete:
      tags:
        - Shopping
      summary: Clear (bulk-delete) all purchased shopping items
      description: >
        Permanently deletes every ShoppingItem in this household with purchased=true.
        This is a bulk hard-delete, not an archive — cleared items are not retained
        or recoverable, and no archived state exists. Requires active household
        membership; frontend must confirm with the user before calling this.
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Purchased items cleared
          content:
            application/json:
              schema:
                type: object
                properties:
                  deleted_count:
                    type: integer
        '403':
          description: Not a household member

  # Expenses
  /households/{id}/expenses:
    get:
      tags:
        - Expenses
      summary: List household expenses
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: category
          in: query
          schema:
            type: string
        - name: payer_id
          in: query
          schema:
            type: string
            format: uuid
        - name: date_from
          in: query
          description: Return expenses created on or after this date
          schema:
            type: string
            format: date
        - name: date_to
          in: query
          description: Return expenses created on or before this date
          schema:
            type: string
            format: date
      responses:
        '200':
          description: List of expenses
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExpenseList'

    post:
      tags:
        - Expenses
      summary: Log expense
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExpenseCreate'
      responses:
        '201':
          description: Expense logged
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Expense'

  /households/{id}/expenses/{expense_id}:
    patch:
      tags:
        - Expenses
      summary: Update expense (creator/owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: expense_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExpenseUpdate'
      responses:
        '200':
          description: Expense updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Expense'

    delete:
      tags:
        - Expenses
      summary: Delete expense (creator/owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: expense_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Expense deleted

  # Inventory
  /households/{id}/inventory:
    get:
      tags:
        - Inventory
      summary: List household inventory
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: category
          in: query
          schema:
            type: string
      responses:
        '200':
          description: List of inventory items
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InventoryItemList'

    post:
      tags:
        - Inventory
      summary: Add inventory item
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InventoryItemCreate'
      responses:
        '201':
          description: Item added
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InventoryItem'

  /households/{id}/inventory/{item_id}:
    patch:
      tags:
        - Inventory
      summary: Update inventory item
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: item_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InventoryItemUpdate'
      responses:
        '200':
          description: Item updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InventoryItem'

    delete:
      tags:
        - Inventory
      summary: Delete inventory item (creator/owner only)
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
        - name: item_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Item deleted

  # Dashboard
  /households/{id}/dashboard:
    get:
      tags:
        - Dashboard
      summary: Get aggregated household dashboard
      description: >
        Returns household info, members, up to 3 pending tasks, shopping pending
        count, and up to 5 recent expenses with a running total. Minimal MVP scope —
        no analytics, charts, activity feed, or productivity metrics.
      security:
        - sessionAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Dashboard data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DashboardResponse'
        '403':
          description: Not a household member

security:
  - sessionAuth: []
```

---

## Key Design Patterns

### Authentication
- All endpoints secured with session-based authentication (cookie: `sessionid`)
- Unauthenticated requests return 401
- User authorization (membership, ownership) enforced per-endpoint

### Pagination
- Query parameters: `page` (default 1), `limit` (default 20, max 100)
- Response includes `meta.page`, `meta.limit`, `meta.total`

### Filtering
- Query parameters per entity: `completed`, `category`, `payer_id`, etc.
- Multiple filters are AND'd together

### Error Responses
- All errors return JSON with `code` and `message`
- HTTP status codes:
  - 200 OK (successful GET, PATCH, POST response)
  - 201 Created (successful POST resource creation)
  - 204 No Content (successful DELETE)
  - 400 Bad Request (malformed request)
  - 401 Unauthorized (authentication required)
  - 403 Forbidden (authorization denied)
  - 404 Not Found (resource doesn't exist or not in user's household)
  - 409 Conflict (concurrent edit conflict)
  - 422 Unprocessable Entity (validation error)
  - 429 Too Many Requests (rate limit exceeded)
  - 500 Internal Server Error

### Household Scoping
- All endpoints verify user is member of household
- Queries automatically scoped to user's households
- Cross-household access returns 403 Forbidden

### Authorization
- Owner actions (delete household, invite, remove members): checked per-endpoint
- Creator actions (edit/delete own task): checked in handler
- Membership required: checked at route level

---

## Implementation Notes

### Django REST Framework Integration
- Use DRF viewsets for standard CRUD operations
- Create custom permission classes for ownership/membership checks
- Use serializers for request validation and response formatting
- Implement `perform_create()` to set `created_by` automatically

### Endpoint Routing
```python
# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'households', HouseholdViewSet, basename='household')
# ... register other viewsets

# Mount under /api/v1/
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include(auth_urls)),
]
```

### CORS Configuration
- Enable CORS for frontend origin during development
- Configure CORS_ALLOWED_ORIGINS in settings.py

### Rate Limiting
- Login endpoint: 5 attempts per minute per IP
- Password reset: 3 attempts per hour per email
- API endpoints: 100 requests per 15 minutes per user (configurable)

---

## Testing the API

### Manual Testing (curl)
```bash
# Signup
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","name":"John Doe"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}' \
  -c cookies.txt

# Get current user
curl http://localhost:8000/api/v1/auth/me \
  -b cookies.txt

# Create household
curl -X POST http://localhost:8000/api/v1/households \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name":"My Household"}'
```

### Automated Testing
- Use pytest + pytest-django for API tests
- Use APIClient from DRF for authenticated requests
- Test authorization by verifying 403 responses for unauthorized users

---

