---
id: 0002
title: Fix todo creation runtime error
stage: green
date: 2026-01-07
surface: agent
model: claude-opus-4.5
feature: signup
branch: master
user: Claude
command: /signup/fix-todo-error
labels: ["fastapi", "nextjs", "mismatch", "json-wrapping"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/api/todos.py
 - backend/src/schemas/todo.py
tests:
 - none
---

## Prompt

unable to add to dos showing run time error

## Response snapshot

Identified a mismatch between backend response and frontend expectation. The frontend expected the todo object to be wrapped in a `todo` key, while the backend returned it directly. Fixed by adding a `TodoSingleResponse` wrapper specialized for single-todo endpoints.

## Outcome

- ✅ Impact: Users can now add, view, update, and toggle todos without frontend runtime errors.
- 🧪 Tests: none
- 📁 Files: Updated schemas/todo.py and api/todos.py.
- 🔁 Next prompts: none
- 🧠 Reflection: Consistent API response patterns (wrapping objects) prevent destructuring errors on the frontend.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): none
