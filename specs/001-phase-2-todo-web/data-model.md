# Data Model: Phase 2 Todo Web Application

## Overview

This document defines the database schema for the Phase II full-stack todo application. The schema uses SQLModel which provides both SQLAlchemy ORM capabilities and Pydantic validation.

## Entities

### User

Represents a registered user account in the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Default: uuid4() | Unique user identifier |
| email | str | Unique, MaxLength: 255, Email format | User's email address (login identifier) |
| password_hash | str | MaxLength: 255 | Bcrypt hashed password |
| created_at | datetime | Default: UTC now | Account creation timestamp |
| updated_at | datetime | Default: UTC now, OnUpdate: UTC now | Last profile update timestamp |

**Relationships**:
- One-to-Many with Todo (user can have many todos)

**Indexes**:
- `idx_user_email` on email column (unique lookup)

**Constraints**:
- Email must be unique across all users
- Email format validated (RFC 5322 standard)
- Password never stored in plaintext

### Todo

Represents a todo item owned by a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Default: uuid4() | Unique todo identifier |
| user_id | UUID | ForeignKey, Not Null | Reference to owning user |
| title | str | MaxLength: 500, Not Null | Todo text content |
| is_complete | bool | Default: False | Completion status flag |
| created_at | datetime | Default: UTC now | Todo creation timestamp |
| updated_at | datetime | Default: UTC now, OnUpdate: UTC now | Last modification timestamp |

**Relationships**:
- Many-to-One with User (many todos belong to one user)
- Cascade delete: When user is deleted, all their todos are deleted

**Indexes**:
- `idx_todo_user_id` on user_id column (filter by owner)
- Composite index on (user_id, created_at) for sorted queries

**Constraints**:
- Title cannot be empty or whitespace-only
- Title maximum 500 characters
- User must exist when creating todo

## Entity Relationship Diagram

```
+--------+       +--------+
|  User  |       |  Todo  |
+--------+       +--------+
   |1            *|
   +-------------+
   (one-to-many)
```

## Validation Rules

### User Validation (Pydantic)

```python
# Signup request validation
email: EmailStr (RFC 5322 format)
password: MinLength(8), MaxLength(128)
password_confirm: Equals password

# Signin request validation
email: EmailStr
password: MinLength(1)
```

### Todo Validation (Pydantic)

```python
# Create todo validation
title: MinLength(1), MaxLength(500), Strip whitespace

# Update todo validation
title: Optional[MinLength(1), MaxLength(500)]
is_complete: Optional[bool]
```

## Database Migrations

### Migration Tool: Alembic

Alembic will be used for managing schema changes over time.

### Initial Migration Schema

The initial migration creates:
1. `users` table with all User fields and constraints
2. `todos` table with all Todo fields and constraints
3. Foreign key constraint from todos.user_id to users.id
4. Cascade delete rule for user → todos relationship
5. All indexes defined above

### Future Migrations

When schema changes are needed:
1. Generate migration: `alembic revision -m "description"`
2. Edit migration file with changes
3. Apply migration: `alembic upgrade head`

## Seeding Strategy

### Initial Data

No mandatory seeding required. The application starts with empty tables.

### Test Data (Development Only)

For local development, consider seeding:
- A test user account
- Sample todos for the test user
- Use factory pattern (e.g., Faker) for realistic data

## Performance Considerations

### Query Patterns

**Frequent Queries**:
- Get all todos for user (ordered by created_at DESC)
- Get single todo by ID with user validation
- Create new todo
- Update todo status
- Delete todo

**Index Strategy**:
- Primary key lookups are optimized by default (B-tree)
- `idx_todo_user_id` enables fast user-scoped queries
- Composite index supports sorting within user scope

### Connection Management

- SQLModel connection pooling configured for web server
- Pool size: 5 connections (adjust based on load)
- Max overflow: 10 connections (for burst traffic)
- Timeout: 30 seconds for connection acquisition

## Security Considerations

### Data Isolation

- All todo queries MUST include user_id filter
- API layer validates ownership before operations
- Database views can enforce user-scoped access if needed

### Password Storage

- Passwords hashed with bcrypt (work factor: 12)
- Never stored in plaintext
- Never logged or exposed in errors

### Sensitive Data

- Password hash is the only truly sensitive field
- Email is personally identifiable information (PII)
- Logs must not contain password hashes or sensitive data
