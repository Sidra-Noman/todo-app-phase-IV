# Research: Phase 2 Todo Web Application

## Technology Decisions

### Backend Framework: FastAPI

**Decision**: Use FastAPI for the Python REST API backend.

**Rationale**:
- FastAPI is a modern, high-performance web framework for Python
- Built-in support for REST APIs with automatic OpenAPI documentation
- Excellent performance comparable to Node.js and Go
- Native Pydantic integration for data validation
- Type hints support for better developer experience
- Async support for handling concurrent requests
- Active community and production use

**Alternatives Considered**:
- Flask: Simpler but requires more boilerplate for REST APIs; no native async
- Django: Full-featured but overkill for this scope; higher learning curve
- Starlette: Lower-level; FastAPI provides better developer experience

### ORM: SQLModel

**Decision**: Use SQLModel as the ORM layer for database operations.

**Rationale**:
- SQLModel is built on top of SQLAlchemy and Pydantic
- Unifies data models and Pydantic schemas (no duplication)
- Type-safe database operations with Python type hints
- Seamless integration with FastAPI
- Supports complex queries when needed
- Database-agnostic design (works with PostgreSQL, SQLite, etc.)

**Alternatives Considered**:
- SQLAlchemy Core: More powerful but steeper learning curve; separate schema definitions
- Tortoise ORM: Async-native but less documentation; smaller community
- Raw SQL with psycopg: No ORM benefits; higher error risk; harder maintenance

### Authentication: Better Auth

**Decision**: Use Better Auth for authentication.

**Rationale**:
- Better Auth provides a simple, type-safe authentication library
- Works well with React and Next.js (frontend) and integrates with backend
- Supports email/password authentication out of the box
- Session-based auth with secure cookie handling
- TypeScript-first design for better developer experience
- Extensible for additional providers in future

**Alternatives Considered**:
- NextAuth.js: Popular but Next.js-specific; our backend is separate Python API
- Auth.js: Similar to NextAuth; less flexibility with external APIs
- Custom auth: Higher development effort; security risks if implemented incorrectly

### Database: Neon Serverless PostgreSQL

**Decision**: Use Neon as the PostgreSQL hosting provider.

**Rationale**:
- Neon is a serverless PostgreSQL platform
- Automatic scaling and connection pooling
- Generous free tier for development
- Excellent TypeScript/JavaScript SDK support
- Built-in branch support for development workflows
- Managed infrastructure reduces operational burden

**Alternatives Considered**:
- Supabase: PostgreSQL-based but more feature-rich (includes Auth, Storage)
- Railway/Render: Simpler hosting but less specialized for PostgreSQL
- Self-hosted PostgreSQL: Higher operational overhead; not serverless

### Frontend: Next.js 14+

**Decision**: Use Next.js 14 with App Router for the frontend.

**Rationale**:
- Next.js 14 provides React framework with server-side rendering
- App Router enables React Server Components for better performance
- File-based routing simplifies page structure
- Built-in API routes can proxy backend calls if needed
- Excellent TypeScript support
- Large ecosystem of components and tools
- Responsive design capabilities with CSS frameworks

**Alternatives Considered**:
- React with Vite: Simpler build setup but no SSR; more manual configuration
- Remix: Modern full-stack framework but smaller ecosystem
- Gatsby: Static site focused; less dynamic capability

### CSS Framework: Tailwind CSS

**Decision**: Use Tailwind CSS for styling.

**Rationale**:
- Utility-first approach speeds up development
- Built-in responsive design support
- Small bundle size (unused CSS purged)
- Easy to maintain and extend
- Excellent developer experience with autocomplete
- Works seamlessly with Next.js

### API Communication: fetch with TanStack Query

**Decision**: Use native fetch with TanStack Query for API calls.

**Rationale**:
- TanStack Query (React Query) provides caching, mutations, and state management
- Reduces boilerplate for data fetching
- Built-in caching and background refetching
- Loading and error state handling
- Optimistic updates for better UX

**Alternatives Considered**:
- Axios: Popular but adds another dependency; fetch is native
- SWR: Similar to TanStack Query; both are good choices
- TanStack Query has slightly better TypeScript support

## Best Practices

### Backend Architecture

- **Layered Architecture**: API routes → Services → Models
- **Separation of Concerns**: Each layer has specific responsibility
- **Error Handling**: Centralized exception handling with meaningful messages
- **Input Validation**: Pydantic models for request validation
- **Authentication**: Dependency injection for auth context

### Database Design

- **Schema Versioning**: Use Alembic for migration management
- **Indexing**: Index foreign keys and frequently queried columns
- **Connection Pooling**: Use SQLModel connection pooling
- **Soft Deletes**: Consider for future recovery features

### Frontend Architecture

- **Component Structure**: Atomic design (atoms, molecules, organisms)
- **State Management**: React Context for auth state; TanStack Query for server state
- **Page Layouts**: Shared layouts for consistent navigation
- **Form Handling**: React Hook Form for form state and validation

### Security

- **Password Hashing**: Use bcrypt with appropriate work factor
- **Session Management**: Secure, HTTP-only cookies
- **CORS**: Configure for specific frontend origin only
- **Rate Limiting**: Implement basic rate limiting on auth endpoints
- **Input Sanitization**: Validate all inputs on backend

## Integration Patterns

### Frontend-Backend Communication

1. Frontend calls backend REST API with fetch
2. Auth token included in Authorization header (Bearer scheme)
3. Backend validates token and extracts user context
4. Backend performs operation and returns JSON response
5. Frontend updates React Query cache on mutations

### Session Flow

1. User submits credentials on frontend
2. Frontend POSTs to backend `/api/auth/signin`
3. Backend validates and creates session
4. Backend returns session cookie (HTTP-only)
5. Frontend redirects to todos page
6. Subsequent requests include session cookie
7. Backend validates session and enriches request context
8. On logout, session is invalidated and cookie cleared

## Development Environment

### Required Tools

- Python 3.11+
- Node.js 18+
- PostgreSQL client (psql or GUI tool)
- Git

### Environment Variables

```
# Backend
DATABASE_URL=postgresql://user:password@host:5432/db
BETTER_AUTH_SECRET=your-secret-key
CORS_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Local Development Workflow

1. Start Neon database (connection via URL)
2. Run backend: `cd backend && uvicorn src.main:app --reload`
3. Run frontend: `cd frontend && npm run dev`
4. Access frontend at `http://localhost:3000`
5. API docs at `http://localhost:8000/docs`
