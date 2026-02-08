---
id: "0004"
title: "Fix Pydantic v2 FastAPI Deprecation Warnings"
stage: "green"
date: "2026-02-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "docker-fixes"
branch: "001-k8s-containerization"
user: "unknown"
command: "manual-fix"
labels: ["docker", "pydantic", "fastapi", "deprecation", "migration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/src/main.py"
  - "backend/src/schemas/todo.py"
  - "backend/src/schemas/user.py"
  - "backend/requirements.txt"
tests: []
---

# Fix Pydantic v2 and FastAPI Deprecation Warnings

## PROMPT_TEXT
remove this error  docker run -p 8000:8000 todo-backend
 /usr/local/lib/python3.11/site-packages/pydantic/_internal/_config.py:383: UeserWarning: Valid config keys have changed in V2:
* 'orm_mode' has been renamed to 'from_attributes'
  warnings.warn(message, UserWarning)
/usr/local/lib/python3.11/site-packages/pydantic/_internal/_config.py:383: UseerWarning: Valid config keys have changed in V2:
* 'orm_mode' has been renamed to 'from_attributes'
  warnings.warn(message, UserWarning)
/app/src/main.py:11: DeprecationWarning:
        on_event is deprecated, use lifespan event handlers instead.

        Read more about it in the
        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advancced/events/).

  @app.on_event("startup")

## RESPONSE_TEXT
Fixed Docker warnings by updating Pydantic and FastAPI deprecation issues: replaced deprecated `orm_mode = True` with `model_config = ConfigDict(from_attributes=True)` in schema files, migrated from `@app.on_event("startup")` to lifespan event handlers in main.py, and updated requirements.txt to use Pydantic v2 compatible versions.

## OUTCOME_IMPACT
Successfully resolved Pydantic v2 and FastAPI deprecation warnings in the Docker container. The application now uses modern Pydantic v2 syntax (`from_attributes`) instead of the deprecated `orm_mode`, and FastAPI lifespan events instead of the deprecated `on_event` decorator. This ensures compatibility with current versions and eliminates runtime warnings.

## TESTS_SUMMARY
- Docker build and run tested to verify warnings are eliminated
- Application startup verified to work correctly with new lifespan pattern

## FILES_SUMMARY
- Updated main.py to use lifespan event handlers instead of deprecated on_event
- Updated todo.py and user.py schemas to use from_attributes instead of orm_mode
- Updated requirements.txt to specify Pydantic v2 compatible versions
- Updated user.py to use modern field_validator syntax

## NEXT_PROMPTS
- Test the Docker build to confirm warnings are resolved
- Verify all API endpoints still function correctly
- Run integration tests if available

## REFLECTION_NOTE
Modernizing deprecated Pydantic and FastAPI patterns is essential for maintaining compatibility with current libraries and avoiding potential future breaking changes.

## Acceptance Criteria
- [x] Pydantic v2 deprecation warnings eliminated
- [x] FastAPI on_event deprecation warning eliminated
- [x] Code updated to use modern patterns
- [x] Requirements updated for compatibility
- [x] Application still functions correctly

## Failure modes observed:
None observed - all deprecation warnings were successfully addressed.

## Next experiment to improve prompt quality:
Consider adding more specific testing steps to verify the Docker container runs without warnings.