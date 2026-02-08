# Quickstart: Phase III - AI-Powered Todo Chatbot

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- PostgreSQL database (Neon recommended)
- Cohere API key for AI integration
- Docker (optional, for containerized setup)

## Environment Setup

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Set your Cohere API key:
   ```bash
   # In .env file
   COHERE_API_KEY=your_cohere_api_key_here
   ```

3. Configure database connection:
   ```bash
   # Example for Neon database
   DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```

## Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   # Make sure cohere is included in requirements
   pip install cohere-ai
   ```

3. Run database migrations:
   ```bash
   # From backend directory
   alembic upgrade head
   ```

4. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## MCP Server Setup

1. Navigate to MCP server directory:
   ```bash
   cd mcp-server
   ```

2. Install MCP server dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the MCP server:
   ```bash
   python src/server.py
   ```

## Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Running the Complete Application

1. Start all services in this order:
   - Database (ensure PostgreSQL is running)
   - Backend: `uvicorn src.main:app --reload --port 8000`
   - MCP Server: `python src/server.py`
   - Frontend: `npm run dev`

2. Access the application:
   - Web app: http://localhost:3000
   - Backend API: http://localhost:8000
   - Chat endpoint: http://localhost:8000/api/chat

## Key Features

### Chat Interface
- Navigate to `/chat` to access the AI chatbot
- Natural language commands for todo management
- Conversation history persistence
- Real-time responses

### Supported Commands
- "Add a todo to buy groceries" - creates a new todo
- "Show me my todos" - lists all todos
- "Mark the first todo as complete" - updates todo status
- "Delete the grocery shopping todo" - removes a specific todo
- "Update my meeting todo to tomorrow" - modifies a todo

## Testing

### Backend Tests
```bash
# Run all backend tests
pytest tests/

# Run specific test suites
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
```

### Frontend Tests
```bash
# Run frontend tests
npm run test
npm run test:e2e  # End-to-end tests
```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b 003-phase-3-ai-chatbot-feature
   ```

2. Make your changes following the task list in `specs/003-phase-3-ai-chatbot/tasks.md`

3. Test your changes:
   - Run relevant unit tests
   - Verify API contracts
   - Test frontend integration

4. Commit with conventional commits:
   ```bash
   git add .
   git commit -m "feat(chat): implement cohere integration"
   ```

## Troubleshooting

### Common Issues

1. **Cohere API errors**: Verify `COHERE_API_KEY` is set correctly in environment
2. **Database connection errors**: Check `DATABASE_URL` configuration
3. **Authentication issues**: Ensure session cookies are properly handled
4. **MCP tool access**: Verify MCP server is running and accessible

### Useful Commands

- Check backend health: `curl http://localhost:8000/health`
- Check chat endpoint: `curl http://localhost:8000/api/chat/health`
- View database schema: `alembic history`
- Reset database: `alembic downgrade base && alembic upgrade head`