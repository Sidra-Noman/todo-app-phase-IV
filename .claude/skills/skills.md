# Skills

## Skill: Core Feature Review
---
name: todo-core-feature-review
description: Review implementation of core Todo features in web application.
---

Core Feature Review
Instructions

Verify all 5 features:

Add

View (list + detail)

Update

Delete

Toggle Complete

Ensure:

Every operation is authenticated

Data is scoped to the logged-in user

State changes persist in database

Red Flags

Missing feature parity with Phase I

Feature works for one user but leaks data across users

Completion toggle not idempotent

## Skill: REST API Review
---
name: todo-rest-api-review
description: Review FastAPI REST endpoints for correctness, security, and REST compliance.
---

REST API Review
Instructions

Validate endpoints:

Correct HTTP methods

Correct URL structure

Proper user scoping

Verify:

Request/response schemas

Status codes (200, 201, 204, 400, 401, 403, 404)

Consistent error responses

Common Issues

Using PUT instead of PATCH (or vice versa)

Trusting user_id from request path

Missing auth dependency

## Skill: Authentication & Authorization Review
---
name: todo-auth-review
description: Review Better Auth frontend flow and FastAPI backend authorization.
---

Authentication Review
Instructions

Frontend

Better Auth handles signup/signin

Tokens/sessions handled securely

Backend

Auth verified independently

Auth middleware or dependency enforced

user_id derived from auth context, not client input

Critical Issues

Backend trusting frontend user_id

Unprotected API routes

Missing authorization checks

## Skill: Database & ORM Review
---
name: todo-database-review
description: Review SQLModel schemas and Neon PostgreSQL persistence.
---

Database Review
Instructions

Schema validation

User–Task relationship enforced

Required fields present

Foreign keys defined

Persistence

Data survives restart

Deterministic ordering (e.g. created_at)

Anti-Patterns

No foreign key to user

Non-deterministic queries

Raw SQL without justification

## Skill: Frontend Integration Review
---
name: todo-frontend-review
description: Review Next.js frontend integration with authenticated backend APIs.
---

Frontend Review
Instructions

Next.js App Router usage

Auth-aware API calls

Loading, error, and empty states

Responsive behavior

Common Problems

Client/server mismatch

Silent API failures

UI not reflecting backend state

## Skill: Agentic Workflow Compliance
---
name: todo-agentic-workflow-review
description: Ensure Spec → Plan → Tasks → Code workflow compliance in Phase II.
---

Workflow Review
Instructions

Spec completeness

Plan justification

Tasks are atomic and testable

Code generated only via Claude Code

Must Have

PHRs for each phase

ADR for authentication strategy

No manual code edits
