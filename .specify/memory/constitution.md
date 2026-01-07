<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution)
- Added principles: 5 new principles covering test-first, phase compliance, phase isolation, security, and simplicity
- Added sections: Technology Matrix, Phase Isolation Rules
- Removed sections: All template placeholders replaced
- Templates requiring updates: None needed (templates are consistent with new constitution)
- Follow-up TODOs: None
-->

# Todo App Constitution

## Core Principles

### I. Test-First Development (NON-NEGOTIABLE)

TDD mandatory: Tests written → User approved → Tests fail → Then implement.
The Red-Green-Refactor cycle MUST be strictly enforced for all features.

Rationale: Ensures correctness before implementation, provides regression safety net,
and forces clear feature understanding upfront.

### II. Phase Compliance

Each feature MUST be implemented using only technologies permitted in its target phase:

- **Phase I**: In-memory console application only. No persistence, no network, no auth.
- **Phase II** (starting now):
  - Backend: Python REST API
  - Database: Neon Serverless PostgreSQL
  - ORM/Data layer: SQLModel or equivalent
  - Frontend: Next.js (React, TypeScript)
  - Authentication: Better Auth (signup/signin)
  - Architecture: Full-stack web application
- **Phase III+**: Advanced cloud infrastructure, agents, AI, orchestration

Rationale: Phased development prevents scope creep and maintains clear architectural boundaries.

### III. Phase Isolation

Technology usage is STRICTLY gated by phase:

- Authentication (signup/signin) is allowed STARTING Phase II
- Web frontend is allowed STARTING Phase II
- Neon PostgreSQL is allowed STARTING Phase II
- AI or agent frameworks are NOT allowed until Phase III or later

Violations MUST be flagged during design review and rejected until the appropriate phase.

Rationale: Prevents premature complexity and maintains focus on core functionality.

### IV. Security by Phase

Security controls MUST be appropriate to the phase:

- Phase I: No security requirements (single-user, local only)
- Phase II: Authentication required, password hashing, session management
- Phase III+: Enterprise auth, RBAC, audit logging, compliance controls

Rationale: Security investments should match actual risk exposure.

### V. Simplicity

Start simple. Follow YAGNI (You Aren't Gonna Need It) principles.

- Implement only what is required by the current user stories
- Defer infrastructure decisions until the complexity is actually needed
- Reject "potential future use" as a justification for added complexity

Rationale: Premature abstraction and over-engineering create maintenance burden
and delay delivery of value.

## Technology Matrix

### Phase I: Foundation (In-Memory Console)
- **Type**: Single-user console application
- **Storage**: In-memory data structures only
- **Constraints**: No network, no persistence, no authentication

### Phase II: Full-Stack Web Application
- **Backend**: Python REST API
- **Database**: Neon Serverless PostgreSQL
- **ORM/Data Layer**: SQLModel or equivalent
- **Frontend**: Next.js (React, TypeScript)
- **Authentication**: Better Auth (signup/signin)
- **Architecture**: Client-server web application

### Phase III+: Advanced Capabilities
- **Cloud Infrastructure**: Deployment, scaling, monitoring
- **AI/ML**: Agent frameworks, orchestration, intelligent features
- **Advanced Patterns**: Event sourcing, CQRS, microservices as needed

## Governance

This constitution serves as the authoritative technology policy for the project.
All development decisions MUST comply with these principles.

**Amendment Procedure**:
1. Proposed amendments MUST be documented with rationale
2. Breaking changes require explicit consent from project stakeholders
3. Amendments take effect upon merge to the main branch

**Compliance**:
- All design documents (plan.md) MUST include a Constitution Check section
- Features that violate principles MUST be rejected or justified via complexity tracking
- Periodic reviews ensure ongoing alignment with these principles

**Supremacy**: This constitution supersedes all other development practices and guidelines.

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06
