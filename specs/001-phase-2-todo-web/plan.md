# Implementation Plan: Phase 2 Todo Web Application

**Branch**: `001-phase-2-todo-web` | **Date**: 2026-01-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-phase-2-todo-web/spec.md`

## Summary

Phase II of the Evolution of Todo project converts the Phase I in-memory console application into a full-stack web application. The implementation adds user authentication via Better Auth, persistent storage using Neon Serverless PostgreSQL, and a responsive Next.js frontend. Users can register, sign in, and manage their personal todo list with full CRUD operations.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI (backend web framework), SQLModel (ORM), Next.js 14+ (frontend framework), Better Auth (authentication)
**Storage**: Neon Serverless PostgreSQL with SQLModel for ORM
**Testing**: pytest (backend), Jest/Vitest (frontend), Playwright (E2E)
**Target Platform**: Web browser (desktop and mobile)
**Project Type**: Full-stack web application (backend + frontend)
**Performance Goals**: API response under 200ms p95, page load under 3 seconds
**Constraints**: No AI frameworks, no background workers, no real-time features, no advanced analytics
**Scale/Scope**: Single-tenant, individual user data isolation, no team features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase Compliance Verification

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| Phase II Allowed | Python REST API | PASS | FastAPI confirmed |
| Phase II Allowed | Neon PostgreSQL | PASS | Database specified |
| Phase II Allowed | SQLModel ORM | PASS | ORM specified |
| Phase II Allowed | Next.js Frontend | PASS | Framework confirmed |
| Phase II Allowed | Better Auth | PASS | Auth framework confirmed |
| Phase Isolation | No AI/Agents | PASS | Excluded by requirement |
| Phase Isolation | No Background Jobs | PASS | Excluded by requirement |
| Phase Isolation | No Real-time | PASS | Excluded by requirement |
| Security | Password Hashing | PASS | Required by spec |
| Security | User Data Isolation | PASS | Enforced by API |

### Gate Status: PASS

All constitution requirements satisfied. No violations requiring complexity tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-2-todo-web/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── auth.yaml        # Authentication API contract
│   └── todos.yaml       # Todo API contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLModel entity definitions
│   ├── services/        # Business logic layer
│   ├── api/             # FastAPI routes and controllers
│   ├── core/            # Configuration and startup
│   └── schemas/         # Pydantic request/response models
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/        # API contract tests
├── alembic/             # Database migrations
└── requirements.txt

frontend/
├── src/
│   ├── app/             # Next.js App Router pages
│   ├── components/      # Reusable UI components
│   ├── services/        # API client and auth services
│   ├── hooks/           # Custom React hooks
│   └── types/           # TypeScript type definitions
├── tests/
│   ├── unit/
│   └── e2e/             # Playwright tests
├── public/              # Static assets
├── next.config.js
├── tailwind.config.js
└── package.json

docs/                    # Documentation
scripts/                 # Utility scripts
.env.example             # Environment template
```

**Structure Decision**: Full-stack web application with separate backend and frontend directories. Backend uses Python/FastAPI/SQLModel as per constitution. Frontend uses Next.js with App Router. Monorepo structure for simplified development workflow.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. All technology choices align with Phase II allowed technologies.

---

## Phase 0: Research

See [research.md](research.md) for technology decisions and best practices.

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](data-model.md) for entity definitions and relationships.

### API Contracts

See [contracts/](contracts/) directory for OpenAPI specification files:
- [auth.yaml](contracts/auth.yaml) - Authentication endpoints
- [todos.yaml](contracts/todos.yaml) - Todo CRUD endpoints

### Quickstart Guide

See [quickstart.md](quickstart.md) for local development setup instructions.
