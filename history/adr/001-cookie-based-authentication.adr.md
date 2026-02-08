---
id: 1
title: "Cookie-Based Authentication with NextAuth"
date_iso: 2026-01-21
stage: plan
status: accepted
author: claude-sonnet-4-5-20250929
feature: authentication
branch: main
surface: agent
model: claude-sonnet-4-5-20250929
labels: ["authentication", "security", "session", "nextjs"]
links:
  spec: null
  ticket: null
  phr: "history/prompts/general/001-fix-signup-signin-issues.red.prompt.md"
  pr: null
decision_context: |
  The todo app needed a secure authentication system that works well with Next.js. We evaluated JWT tokens vs cookie-based authentication.
concerns: |
  - Security of token storage in browser
  - Session management complexity
  - Cross-site request forgery protection
  - Automatic login persistence
decision_outcome: |
  Chose cookie-based authentication with NextAuth for the following reasons:
  1. Better security - HTTP-only cookies prevent XSS attacks
  2. Automatic inclusion in requests - no manual token management
  3. Built-in CSRF protection
  4. Seamless integration with Next.js
  5. Simpler frontend implementation
  6. Server-side session management
alternatives_considered: |
  - JWT tokens stored in localStorage: Vulnerable to XSS attacks
  - JWT tokens in memory: Lost on page refresh, poor UX
  - OAuth providers only: Limited to external authentication
  - Custom session management: Increased complexity and security risks
pros_and_cons: |
  Pros:
  + Secure HTTP-only cookies
  + Automatic inclusion in requests
  + Built-in session management
  + Good Next.js integration

  Cons:
  - Less flexible than JWT for mobile apps
  - Requires maintaining server-side session state
  - Potential scaling considerations
implementation_notes: |
  - Backend sets HTTP-only session cookie after successful authentication
  - Frontend uses NextAuth with credentials provider
  - API calls include credentials to maintain session
  - Protected routes verify session cookie presence
verification_approach: |
  - Manual testing of signup/signin flows
  - Automated test suite verifying authentication flow
  - Cookie inspection in browser dev tools
  - Session persistence across page refreshes
stakeholders: ["developer", "security"]
reviewers: ["developer"]
---

# Cookie-Based Authentication with NextAuth

## Context
The todo application required a secure authentication system that integrates well with the Next.js frontend and FastAPI backend. The decision was needed to balance security, developer experience, and user experience.

## Decision
We chose to implement cookie-based authentication using NextAuth.js with credentials provider, combined with HTTP-only session cookies managed by the FastAPI backend.

## Rationale
This approach provides the best balance of security and usability:
- HTTP-only cookies protect against XSS attacks by preventing JavaScript access
- Automatic cookie inclusion in requests simplifies API call implementation
- NextAuth provides battle-tested authentication flow with multiple provider options
- Session management is handled server-side for better control

## Consequences
Positive:
- Enhanced security through HTTP-only cookies
- Simplified frontend code with automatic session handling
- Standardized authentication flow through NextAuth
- Protection against CSRF attacks

Negative:
- Requires server-side session state management
- Less portable than JWT tokens for multi-platform scenarios
- Tightly coupled to web browser environment

## Implementation
The implementation combines NextAuth credentials provider with FastAPI session cookies, ensuring secure authentication flow while maintaining good user experience.