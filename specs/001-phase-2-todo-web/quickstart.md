# Quickstart: Phase 2 Todo Web Application

This guide covers setting up the local development environment for the Phase II full-stack todo application.

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend runtime |
| PostgreSQL Client | Latest | Database administration |
| Git | Latest | Version control |
| uv | Latest (recommended) | Python package management |

## Initial Setup

### 1. Clone and Enter Project

```bash
git clone <repository-url>
cd todo-app/Phase-II
```

### 2. Setup Backend

```bash
# Create virtual environment
cd backend
uv venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

### 3. Setup Database (Neon PostgreSQL)

1. Create a Neon account at https://neon.tech
2. Create a new project
3. Copy the connection string from project settings
4. Add to backend `.env`:

```env
DATABASE_URL=postgresql://user:password@ep-xxx.region.neon.tech/dbname?sslmode=require
```

### 4. Setup Frontend

```bash
cd frontend
npm install
cp .env.example.local .env.local
# Edit .env.local with your configuration
```

### 5. Configure Environment Variables

**Backend (.env)**:
```env
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-at-least-32-chars
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

### Start Backend

```bash
cd backend
source .venv/bin/activate  # or activate your venv
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

- API running at: http://localhost:8000
- API documentation: http://localhost:8000/docs

### Start Frontend

```bash
cd frontend
npm run dev
```

- Frontend running at: http://localhost:3000

### Access the Application

1. Open http://localhost:3000
2. Click "Sign Up" to create an account
3. Verify email (check console for development)
4. Sign in with new credentials
5. Start adding todos!

## Development Workflow

### Running Tests

**Backend Tests**:
```bash
cd backend
pytest
```

**Frontend Tests**:
```bash
cd frontend
npm test
```

**E2E Tests**:
```bash
cd frontend
npm run test:e2e
```

### Database Migrations

**Create new migration**:
```bash
cd backend
alembic revision -m "description"
# Edit generated file in alembic/versions/
```

**Apply migrations**:
```bash
cd backend
alembic upgrade head
```

### Code Formatting

**Backend**:
```bash
cd backend
ruff check .  # Linting
ruff format .  # Formatting
```

**Frontend**:
```bash
cd frontend
npm run format  # Prettier
npm run lint    # ESLint
```

## Project Structure

```
Phase-II/
├── backend/
│   ├── src/
│   │   ├── api/          # FastAPI routes
│   │   ├── models/       # SQLModel entities
│   │   ├── services/     # Business logic
│   │   ├── schemas/      # Pydantic models
│   │   └── core/         # Configuration
│   ├── tests/
│   ├── alembic/          # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router pages
│   │   ├── components/   # Reusable components
│   │   ├── services/     # API client
│   │   └── hooks/        # Custom React hooks
│   ├── tests/
│   └── package.json
└── specs/001-phase-2-todo-web/
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md
    └── contracts/
```

## Common Tasks

### Adding a New API Endpoint

1. Define Pydantic schema in `backend/src/schemas/`
2. Create model in `backend/src/models/` (if new entity)
3. Add business logic in `backend/src/services/`
4. Create route in `backend/src/api/`
5. Add tests in `backend/tests/`
6. Update API contract in `specs/.../contracts/`

### Adding a New Frontend Page

1. Create page in `frontend/src/app/`
2. Add components in `frontend/src/components/`
3. Update API client in `frontend/src/services/`
4. Add tests in `frontend/tests/`

### Debugging Tips

**Backend**: Use `--reload` flag; check logs in terminal
**Frontend**: Use React DevTools; check Network tab for API calls
**Database**: Use psql or GUI tool to inspect data

## Troubleshooting

### Connection Refused to Backend

- Verify backend is running on port 8000
- Check CORS_ORIGINS includes frontend URL
- Ensure no firewall blocking the port

### Database Connection Errors

- Verify DATABASE_URL is correct
- Check Neon project is active (not suspended)
- Ensure SSL mode is set correctly

### Frontend API Calls Failing

- Check browser console for CORS errors
- Verify NEXT_PUBLIC_API_URL points to running backend
- Check backend is accessible from browser (not just localhost)

### Session Issues

- Clear browser cookies
- Check session cookie is being set
- Verify BETTER_AUTH_SECRET is consistent

## Next Steps

After development environment is ready:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement tasks following TDD approach
3. Run tests to verify implementation
4. Commit and push changes

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com/docs)
- [Neon Documentation](https://neon.tech/docs)
