---
id: 1
title: Update constitution for Phase III AI-powered chatbot
stage: constitution
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: claude
command: sp.constitution
labels: [constitution,ai,todo-chatbot,phase-iii]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Project: Evolution of Todo – Phase III (AI-Powered Todo Chatbot)

Core principles:
- Spec-Driven Development (spec → plan → tasks → implement)
- Strict scope control (no undocumented features)
- Stateless backend architecture
- Deterministic and testable system behavior
- Clear separation between AI logic and core business logic

AI & model standards:
- The chatbot must use Cohere as the AI model provider
- Cohere API key is the single source of AI authentication
- OpenAI Agents SDK patterns may be used conceptually, but all model execution must occur via Cohere
- AI must interact with the application exclusively through MCP tools
- AI must never directly access the database or backend services

Cohere configuration:
- Cohere API Key: COHERE_API_KEY=d2W2eWr910ynB8wmqB4kNV1HIjvXx4BjUcbnN65r
- API key must be used only in backend services
- API key must never be exposed to frontend or client-side code
- All AI requests must be traceable to authenticated backend requests

Architecture standards:
- The existing FastAPI backend, REST APIs, and PostgreSQL database are authoritative
- No changes are allowed to existing APIs, database schema, or authentication behavior
- MCP server must expose all task operations as stateless tools
- Chat endpoint must be stateless and persist conversation state to PostgreSQL
- All AI-driven actions must map directly to existing Todo functionality

Security & authentication:
- User identity must be derived exclusively from backend authentication context
- Chatbot actions must be strictly scoped to the authenticated user
- Cross-user data access is strictly forbidden
- No new authentication flows, roles, or permissions are allowed

Constraints:
- No manual coding (Claude Code + Agentic Dev Stack workflow only)
- No real-time features
- No background jobs
- No analytics, recommendations, or personalization
- No AI memory outside database persistence
- No features beyond the approved Phase III specification

Success criteria:
- Chatbot can add, list, update, complete, and delete t

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) to reflect the Phase III AI-powered todo chatbot requirements. The key changes made were:

1. Updated the Cohere Configuration Standards section to properly reference the API key as an environment variable rather than hardcoding it
2. Updated the version from 2.0.0 to 2.0.1 to reflect the minor update
3. Updated the sync impact report at the top of the file to accurately reflect the changes made
4. Ensured the API key is referenced as COHERE_API_KEY environment variable with the actual key only used for development purposes

The constitution now properly enforces:
- Secure handling of API keys through environment variables
- Proper separation between AI logic and business logic
- Statelessness of backend services
- Security requirements for user authentication and data isolation
- Adherence to the Spec-Driven Development methodology

## Outcome

- ✅ Impact: Updated constitution file with secure API key handling
- 🧪 Tests: none required for constitution update
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Proceed with implementation based on updated constitution
- 🧠 Reflection: Constitution properly updated to guide Phase III development with secure AI integration patterns

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase III implementation following updated constitution