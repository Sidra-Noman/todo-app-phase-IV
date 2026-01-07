---

description: "Task list for Phase 2 full-stack todo web application"

---

# Tasks: Phase 2 Todo Web Application

**Input**: Design documents from `/specs/001-phase-2-todo-web/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Backend Setup

**Purpose**: Project initialization and backend infrastructure

- [ ] T001 Create backend directory structure per plan.md (backend/src/api, backend/src/models, backend/src/services, backend/src/schemas, backend/src/core)
- [ ] T002 Initialize Python 3.11+ project with uv in backend/ directory
- [ ] T003 Create requirements.txt with FastAPI, SQLModel, uvicorn, alembic, bcrypt, python-multipart, pydantic, pydantic-email-valid
- [ ] T004 [P] Create .env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS variables
- [ ] T005 Create backend/src/core/config.py for environment variable loading
- [ ] T006 Create backend/src/core/database.py for SQLModel engine and session management

---

## Phase 2: Backend Foundational

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create backend/src/models/user.py with SQLModel User entity (id, email, password_hash, created_at, updated_at)
- [ ] T008 Create backend/src/models/todo.py with SQLModel Todo entity (id, user_id, title, is_complete, created_at, updated_at)
- [ ] T009 [P] Configure Alembic for database migrations (backend/alembic.ini, backend/alembic/env.py, backend/alembic/versions/)
- [ ] T010 Generate initial Alembic migration for User and Todo tables
- [ ] T011 [P] Create backend/src/schemas/user.py with Pydantic models for signup/signin requests and user responses
- [ ] T012 [P] Create backend/src/schemas/todo.py with Pydantic models for todo CRUD requests and responses
- [ ] T013 Create backend/src/services/auth_service.py with password hashing (bcrypt) and validation functions
- [ ] T014 Create backend/src/api/dependencies.py with FastAPI dependency for getting current user from session

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1)

**Goal**: New users can create accounts with email and password

**Independent Test**: Can be tested by POSTing to /api/auth/signup with valid data and verifying user record created in database

### Tests for User Story 1 (if TDD requested - skip for now)

### Implementation for User Story 1

- [ ] T015 [US1] Create backend/src/api/auth.py with POST /api/auth/signup endpoint (contracts/auth.yaml)
- [ ] T016 [US1] Implement signup logic: validate email format, check duplicate email, hash password, create user, return success
- [ ] T017 [US1] Add proper error responses for duplicate email (400), validation errors (422)

**Checkpoint**: User registration complete - can create accounts

---

## Phase 4: User Story 2 - User Sign In (Priority: P1)

**Goal**: Registered users can authenticate and receive session

**Independent Test**: Can be tested by POSTing to /api/auth/signin with valid credentials and receiving session cookie

### Tests for User Story 2 (if TDD requested - skip for now)

### Implementation for User Story 2

- [ ] T018 [US2] Add POST /api/auth/signin endpoint to backend/src/api/auth.py (contracts/auth.yaml)
- [ ] T019 [US2] Implement signin logic: lookup user by email, verify password, create session, set HTTP-only cookie
- [ ] T020 [US2] Add POST /api/auth/signout endpoint to backend/src/api/auth.py (contracts/auth.yaml)
- [ ] T021 [US2] Add GET /api/auth/me endpoint to backend/src/api/auth.py for session validation (contracts/auth.yaml)
- [ ] T022 [US2] Implement proper error responses for invalid credentials (401)

**Checkpoint**: Authentication complete - users can sign in and out

---

## Phase 5: User Story 3 - View My Todos (Priority: P1)

**Goal**: Authenticated users see their todo list

**Independent Test**: Can be tested by authenticating and GET /api/todos/ returning only user's todos

### Tests for User Story 3 (if TDD requested - skip for now)

### Implementation for User Story 3

- [ ] T023 [US3] Create backend/src/services/todo_service.py with TodoService class for database operations
- [ ] T024 [US3] Add get_todos_by_user_id method to TodoService (filters by user_id)
- [ ] T025 [US3] Create backend/src/api/todos.py with GET /api/todos/ endpoint (contracts/todos.yaml)
- [ ] T026 [US3] Add authentication dependency to GET /api/todos/ endpoint
- [ ] T027 [US3] Implement todo list response with todos sorted by created_at DESC

**Checkpoint**: View todos complete - users can see their list

---

## Phase 6: User Story 4 - Create Todo (Priority: P1)

**Goal**: Authenticated users can add new todos

**Independent Test**: Can be tested by POSTing to /api/todos/ with title and seeing todo appear in list

### Tests for User Story 4 (if TDD requested - skip for now)

### Implementation for User Story 4

- [ ] T028 [US4] Add create_todo method to TodoService (associates with current user)
- [ ] T029 [US4] Create backend/src/api/todos.py with POST /api/todos/ endpoint (contracts/todos.yaml)
- [ ] T030 [US4] Add request body validation (title required, non-empty, max 500 chars)
- [ ] T031 [US4] Implement todo creation with default is_complete=False

**Checkpoint**: Create todo complete - users can add items

---

## Phase 7: User Story 5 - Edit Todo (Priority: P2)

**Goal**: Authenticated users can modify their todos

**Independent Test**: Can be tested by PATCH /api/todos/{id} with new title and verifying update

### Tests for User Story 5 (if TDD requested - skip for now)

### Implementation for User Story 5

- [ ] T032 [US5] Add get_todo_by_id method to TodoService (with user_id filter for ownership)
- [ ] T033 [US5] Add update_todo method to TodoService (with ownership validation)
- [ ] T034 [US5] Create backend/src/api/todos.py with GET /api/todos/{id} endpoint (contracts/todos.yaml)
- [ ] T035 [US5] Create backend/src/api/todos.py with PATCH /api/todos/{id} endpoint (contracts/todos.yaml)
- [ ] T036 [US5] Add ownership check - return 404 if todo not found or not owned by user
- [ ] T037 [US5] Add title validation on update (non-empty, max 500 chars)

**Checkpoint**: Edit todo complete - users can modify items

---

## Phase 8: User Story 6 - Delete Todo (Priority: P2)

**Goal**: Authenticated users can remove their todos

**Independent Test**: Can be tested by DELETE /api/todos/{id} and verifying todo no longer exists

### Tests for User Story 6 (if TDD requested - skip for now)

### Implementation for User Story 6

- [ ] T038 [US6] Add delete_todo method to TodoService (with ownership validation)
- [ ] T039 [US6] Create backend/src/api/todos.py with DELETE /api/todos/{id} endpoint (contracts/todos.yaml)
- [ ] T040 [US6] Add ownership check - return 404 if todo not found or not owned by user
- [ ] T041 [US6] Implement hard delete (remove from database)

**Checkpoint**: Delete todo complete - users can remove items

---

## Phase 9: User Story 7 - Toggle Todo Complete/Incomplete (Priority: P1)

**Goal**: Authenticated users can mark todos complete/incomplete

**Independent Test**: Can be tested by POST /api/todos/{id}/toggle and verifying is_complete changes

### Tests for User Story 7 (if TDD requested - skip for now)

### Implementation for User Story 7

- [ ] T042 [US7] Add toggle_todo method to TodoService (flips is_complete, with ownership validation)
- [ ] T043 [US7] Create backend/src/api/todos.py with POST /api/todos/{id}/toggle endpoint (contracts/todos.yaml)
- [ ] T044 [US7] Add ownership check - return 404 if todo not found or not owned by user
- [ ] T045 [US7] Return updated todo with new is_complete status

**Checkpoint**: Toggle complete - users can track progress

---

## Phase 10: Frontend Setup

**Purpose**: Initialize Next.js frontend project

- [ ] T046 Create frontend directory with Next.js 14+ App Router structure (frontend/src/app, frontend/src/components, frontend/src/services, frontend/src/hooks, frontend/src/types)
- [ ] T047 Initialize frontend package.json with Next.js, React, TypeScript, Tailwind CSS
- [ ] T048 [P] Configure next.config.js for TypeScript and React
- [ ] T049 [P] Configure tailwind.config.js for styling
- [ ] T050 [P] Create .env.example.local with NEXT_PUBLIC_API_URL variable
- [ ] T051 [P] Create frontend/src/types/index.ts with TypeScript interfaces for User, Todo, API responses

---

## Phase 11: User Story 1 Frontend - Signup Page

**Goal**: Users can create accounts from web UI

**Independent Test**: Can be tested by navigating to /signup, filling form, submitting, and being redirected

### Implementation for Signup Page

- [ ] T052 [US1] Create frontend/src/app/signup/page.tsx with signup form UI
- [ ] T053 [US1] Create frontend/src/services/api.ts with fetch wrapper for API calls (POST /api/auth/signup)
- [ ] T054 [US1] Implement form validation (email format, password min 8 chars, password match)
- [ ] T055 [US1] Handle API errors (duplicate email, validation errors) and display messages
- [ ] T056 [US1] On success, redirect to /signin page

---

## Phase 12: User Story 2 Frontend - Signin Page

**Goal**: Users can sign in from web UI

**Independent Test**: Can be tested by navigating to /signin, entering credentials, and seeing todos page

### Implementation for Signin Page

- [ ] T057 [US2] Create frontend/src/app/signin/page.tsx with signin form UI
- [ ] T058 [US2] Update frontend/src/services/api.ts with POST /api/auth/signin call
- [ ] T059 [US2] Handle session cookie and verify authentication state
- [ ] T060 [US2] Handle API errors (invalid credentials) and display messages
- [ ] T061 [US2] On success, redirect to /todos page
- [ ] T062 [US2] Create frontend/src/hooks/useAuth.ts for managing authentication state
- [ ] T063 [US2] Create frontend/src/app/signout/route.ts or button for signout functionality

---

## Phase 13: User Story 3 Frontend - Todo List Page

**Goal**: Users can view their todo list

**Independent Test**: Can be tested by viewing /todos page while signed in and seeing todos

### Implementation for Todo List Page

- [ ] T064 [US3] Create frontend/src/app/todos/page.tsx with todo list UI
- [ ] T065 [US3] Use TanStack Query to fetch todos from GET /api/todos/
- [ ] T066 [US3] Handle authentication check - redirect to /signin if not authenticated
- [ ] T067 [US3] Implement empty state UI when user has no todos
- [ ] T068 [US3] Display todos in list format with title, completion status, created date
- [ ] T069 [US3] Add visual distinction between complete and incomplete todos

---

## Phase 14: User Story 4 Frontend - Add Todo UI

**Goal**: Users can add new todos

**Independent Test**: Can be tested by adding a todo and seeing it appear in the list

### Implementation for Add Todo

- [ ] T070 [US4] Add todo input component to frontend/src/app/todos/page.tsx
- [ ] T071 [US4] Implement POST /api/todos/ call via TanStack Query mutation
- [ ] T072 [US4] Handle validation errors (empty title) and display messages
- [ ] T073 [US4] Clear input and refetch todos on successful creation
- [ ] T074 [US4] Optimistically update todo list UI on mutation

---

## Phase 15: User Story 5 Frontend - Edit Todo UI

**Goal**: Users can edit their todos

**Independent Test**: Can be tested by editing a todo title and seeing the update

### Implementation for Edit Todo

- [ ] T075 [US5] Add inline edit mode or edit button to todo items
- [ ] T076 [US5] Create frontend/src/app/todos/[id]/edit/page.tsx for dedicated edit page (optional)
- [ ] T077 [US5] Implement PATCH /api/todos/{id} call via TanStack Query mutation
- [ ] T078 [US5] Handle validation errors (empty title) and display messages
- [ ] T079 [US5] Cancel edit reverts to original title
- [ ] T080 [US5] Optimistically update todo list UI on mutation

---

## Phase 16: User Story 6 Frontend - Delete Todo UI

**Goal**: Users can delete their todos

**Independent Test**: Can be tested by deleting a todo and verifying it no longer appears

### Implementation for Delete Todo

- [ ] T081 [US6] Add delete button to each todo item
- [ ] T082 [US6] Implement DELETE /api/todos/{id} call via TanStack Query mutation
- [ ] T083 [US6] Add confirmation dialog before deletion
- [ ] T084 [US6] Optimistically update todo list UI on mutation (remove immediately)

---

## Phase 17: User Story 7 Frontend - Toggle Complete UI

**Goal**: Users can mark todos complete/incomplete

**Independent Test**: Can be tested by clicking toggle and seeing status change

### Implementation for Toggle Complete

- [ ] T085 [US7] Add checkbox or toggle button to each todo item
- [ ] T086 [US7] Implement POST /api/todos/{id}/toggle call via TanStack Query mutation
- [ ] T087 [US7] Optimistically update todo list UI on mutation
- [ ] T088 [US7] Update visual styling when todo is complete (strikethrough, color change)

---

## Phase 18: Frontend Polish

**Purpose**: Cross-cutting concerns and UI improvements

- [ ] T089 Create responsive layout with navigation header in frontend/src/app/layout.tsx
- [ ] T090 [P] Add mobile-responsive styles for all pages using Tailwind CSS
- [ ] T091 [P] Create reusable UI components in frontend/src/components/ (Button, Input, Card, Modal)
- [ ] T092 [P] Handle error states throughout (network failures, API errors)
- [ ] T093 [P] Add loading states and spinners for async operations
- [ ] T094 [P] Handle session expiration (redirect to signin on 401 responses)
- [ ] T095 [P] Add proper type safety throughout frontend code

---

## Phase 19: Integration & Local Dev Setup

**Purpose**: Complete integration and local development workflow

- [ ] T096 Create root .env.example with DATABASE_URL placeholder for both backend and frontend reference
- [ ] T097 [P] Document local development setup in README or update quickstart.md
- [ ] T098 [P] Add scripts for running both backend and frontend in development
- [ ] T099 [P] Configure CORS on backend to allow frontend origin (localhost:3000)
- [ ] T100 [P] Test full auth flow: signup → signin → create todo → view todo → toggle → edit → delete

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Frontend Setup (Phase 10)**: Can start after Foundational phase begins (no backend dependency)
- **Frontend Stories (Phase 11-17)**: Depend on both Foundational completion AND Frontend Setup
  - Can proceed in parallel with backend stories once dependencies met
- **Polish (Phase 18)**: Depends on all frontend user stories being complete
- **Integration (Phase 19)**: Depends on all previous phases complete

### User Story Dependencies

- **User Story 1 (Registration)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Sign In)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (View Todos)**: Can start after Foundational (Phase 2) - Depends on Story 2 (auth) for testing
- **User Story 4 (Create Todo)**: Can start after Foundational (Phase 2) - Depends on Story 3 for UI integration
- **User Story 5 (Edit Todo)**: Can start after Foundational (Phase 2) - Depends on Story 4
- **User Story 6 (Delete Todo)**: Can start after Foundational (Phase 2) - Depends on Story 4
- **User Story 7 (Toggle Complete)**: Can start after Foundational (Phase 2) - Depends on Story 3

### Within Each User Story

- Backend implementation before frontend integration
- Core implementation before error handling
- Story complete before moving to next priority (for sequential work)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Backend user stories can work in parallel once Foundational complete
- Frontend user stories can work in parallel once their backend counterparts complete
- Frontend setup (Phase 10) can overlap with backend user story work
- All tasks for a user story marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 + 2 + Backend Foundation)

1. Complete Phase 1: Backend Setup
2. Complete Phase 2: Backend Foundational
3. Complete Phase 3: User Story 1 (Registration)
4. Complete Phase 4: User Story 2 (Sign In)
5. **STOP and VALIDATE**: Test authentication flow independently
6. If ready, deploy/demo auth functionality

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Signup works!
3. Add User Story 2 → Test independently → Signin works!
4. Add User Story 3 → Test independently → View todos works!
5. Add User Story 4 → Test independently → Create todo works!
6. Add User Story 5 → Test independently → Edit todo works!
7. Add User Story 6 → Test independently → Delete todo works!
8. Add User Story 7 → Test independently → Toggle works!
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

**Developer A (Backend)**:
- Phases 1-2: Backend foundation
- Phases 3-9: Backend user stories

**Developer B (Frontend)**:
- Phase 10: Frontend setup (can start in parallel with A's Phase 2)
- Phases 11-17: Frontend user stories (can start once backend stories complete)

**Synchronization Points**:
- After Phase 2: Frontend can start Phase 10
- After each backend story: Frontend can start corresponding frontend story
- Phase 18-19: Both work together on polish and integration

---

## Task Summary

| Category | Count |
|----------|-------|
| Backend Setup | 6 tasks |
| Backend Foundational | 8 tasks |
| Backend User Stories (7 stories) | ~30 tasks |
| Frontend Setup | 6 tasks |
| Frontend User Stories | ~35 tasks |
| Frontend Polish | 7 tasks |
| Integration | 5 tasks |
| **Total Tasks** | **~100 tasks** |

### User Story Task Distribution

| Story | Backend Tasks | Frontend Tasks |
|-------|--------------|----------------|
| US1: Registration | 3 | 5 |
| US2: Sign In | 4 | 7 |
| US3: View Todos | 4 | 6 |
| US4: Create Todo | 3 | 5 |
| US5: Edit Todo | 5 | 6 |
| US6: Delete Todo | 4 | 4 |
| US7: Toggle Complete | 4 | 4 |

### Parallel Execution Examples

**Example 1: Independent Backend Tasks**
```bash
Task: T007 [P] Create User model
Task: T008 [P] Create Todo model
Task: T011 [P] Create user schemas
Task: T012 [P] Create todo schemas
```

**Example 2: User Story 4 Parallel Work**
```bash
Task: T028 [US4] Add create_todo method to service
Task: T029 [US4] Create POST /todos/ endpoint
Task: T070 [US4] Add todo input component
Task: T071 [US4] Implement create todo mutation
```

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
