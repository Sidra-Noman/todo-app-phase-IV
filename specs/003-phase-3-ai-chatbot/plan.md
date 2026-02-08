# Implementation Plan: Phase III - AI-Powered Todo Chatbot

**Branch**: `003-phase-3-ai-chatbot` | **Date**: 2026-01-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-phase-3-ai-chatbot/spec.md`

## Summary

Phase III of the Evolution of Todo project integrates an AI-powered chatbot into the existing full-stack application. The implementation adds a natural language interface that allows authenticated users to manage their todos using conversational commands. The chatbot operates through MCP tools to maintain security and statelessness, while leveraging Cohere for natural language processing.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI (backend web framework), SQLModel (ORM), Cohere Python SDK, Next.js 14+ (frontend framework)
**Storage**: Neon Serverless PostgreSQL with SQLModel for ORM (existing from Phase II)
**Testing**: pytest (backend), Jest/Vitest (frontend), Playwright (E2E)
**Target Platform**: Web browser (desktop and mobile)
**Project Type**: Full-stack web application with AI integration
**Performance Goals**: API response under 200ms p95, chatbot response under 3 seconds
**Constraints**: No direct AI database access, MCP tool usage required, stateless backend required, Cohere as sole AI provider
**Scale/Scope**: Single-tenant, individual user data isolation, no team features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase Compliance Verification

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| Phase III Allowed | Cohere AI Integration | PASS | Confirmed as sole AI provider |
| Phase III Allowed | MCP Tool Architecture | PASS | Tools confirmed for operations |
| Phase III Allowed | Stateless Backend | PASS | All state stored in PostgreSQL |
| Phase III Allowed | Existing API Preservation | PASS | No changes to existing APIs |
| Security | User Data Isolation | PASS | MCP tools enforce user scoping |
| Security | No Direct AI Database Access | PASS | MCP tools mediate all access |
| Architecture | Backend Authority | PASS | Existing backend remains authoritative |
| Architecture | Environment Variable API Keys | PASS | Cohere key from env vars |

### Gate Status: PASS

All constitution requirements satisfied. No violations requiring complexity tracking.

## Project Structure

### Documentation (this feature)

```text
specs/003-phase-3-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── chat.yaml        # Chat API contract
│   └── mcp-tools.yaml   # MCP tools API contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLModel entity definitions (includes new chat entities)
│   ├── services/        # Business logic layer (includes chat service)
│   ├── api/             # FastAPI routes and controllers (includes chat endpoint)
│   ├── core/            # Configuration and startup (includes Cohere config)
│   ├── schemas/         # Pydantic request/response models (includes chat models)
│   └── ai/              # AI integration layer (Cohere client, intent parsing)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/        # API contract tests
├── alembic/             # Database migrations
└── requirements.txt     # Added Cohere SDK dependency

frontend/
├── src/
│   ├── app/             # Next.js App Router pages (includes chat page)
│   ├── components/      # Reusable UI components (includes chat UI)
│   ├── services/        # API client and auth services (includes chat API client)
│   ├── hooks/           # Custom React hooks
│   └── types/           # TypeScript type definitions (includes chat types)
├── tests/
│   ├── unit/
│   └── e2e/             # Playwright tests
├── public/              # Static assets
├── next.config.js
├── tailwind.config.js
└── package.json

mcp-server/              # New directory for MCP tools
├── src/
│   ├── tools/           # MCP tool implementations (todo operations)
│   ├── server.py        # MCP server entry point
│   └── config.py        # MCP configuration
└── requirements.txt     # MCP server dependencies
```

**Structure Decision**: Full-stack extension of Phase II with new chatbot functionality. Backend extends with AI layer and chat endpoints. Frontend adds chat UI. MCP server provides secure tool access for AI operations.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. All technology choices align with Phase III allowed technologies.

---

## Phase 0: Research

See [research.md](research.md) for technology decisions and best practices.

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](data-model.md) for entity definitions and relationships.

### API Contracts

See [contracts/](contracts/) directory for OpenAPI specification files:
- [chat.yaml](contracts/chat.yaml) - Chatbot endpoint API
- [mcp-tools.yaml](contracts/mcp-tools.yaml) - MCP tools API

### Quickstart Guide

See [quickstart.md](quickstart.md) for local development setup instructions.