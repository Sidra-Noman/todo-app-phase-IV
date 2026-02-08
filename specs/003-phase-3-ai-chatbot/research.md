# Research: Phase III - AI-Powered Todo Chatbot

## Technology Decisions

### Cohere Integration

**Decision**: Use Cohere Python SDK for AI integration
**Rationale**: Aligns with constitution requirement to use Cohere as the sole AI provider. Official SDK provides better error handling, rate limiting, and integration patterns.
**Alternatives considered**:
- Direct REST API calls: More complex to implement, more error-prone
- OpenAI SDK with Cohere: Would violate constitution requirement

### MCP Server Implementation

**Decision**: Implement dedicated MCP server using Python
**Rationale**: Provides secure isolation between AI and backend services, enables proper authentication/authorization, and follows constitutional requirements for MCP tool architecture.
**Alternatives considered**:
- Direct API calls from AI: Would violate "no direct database access" requirement
- JavaScript MCP server: Would complicate authentication context

### Conversation Storage

**Decision**: Store conversations in PostgreSQL using new tables that follow existing schema patterns
**Rationale**: Maintains statelessness requirement, leverages existing database infrastructure, and ensures data isolation
**Alternatives considered**:
- Separate database: Would complicate deployment and maintenance
- In-memory storage: Would violate statelessness requirement

### Frontend Integration

**Decision**: Add chat UI as new page/component in existing Next.js application
**Rationale**: Maintains existing application structure, leverages existing authentication, and provides seamless user experience
**Alternatives considered**:
- Separate application: Would complicate user authentication flow
- Embedded widget: Would require more complex state management

## Best Practices Applied

### AI Safety Patterns

- Input validation and sanitization before sending to AI
- Output validation and sanitization before executing operations
- Rate limiting for AI requests to prevent abuse
- Error handling for AI service unavailability

### Security Measures

- All AI operations go through authenticated MCP tools
- Conversation history is user-scoped and isolated
- No sensitive data exposed to AI models
- Proper authentication context maintained throughout

### Performance Optimization

- Caching of frequently accessed data
- Efficient database queries for conversation history
- Asynchronous AI processing where possible
- Connection pooling for database operations

## Unknowns Resolved

### Authentication Context in AI Operations

**Issue**: How to maintain user authentication context when AI performs operations
**Resolution**: MCP tools will receive authentication context from the chat endpoint and validate user permissions before executing operations

### Natural Language Understanding

**Issue**: How to reliably extract user intent from natural language
**Resolution**: Use Cohere's classification capabilities combined with structured prompting to identify user intent (add, list, update, delete, complete) and extract parameters

### Error Handling for Ambiguous Requests

**Issue**: How to handle requests that are unclear or impossible to fulfill
**Resolution**: Implement clarification flow where AI asks for more specific information when requests are ambiguous

### Conversation Context Management

**Issue**: How to maintain conversation context across multiple exchanges
**Resolution**: Store conversation history in database and include relevant context in AI requests, using reference to recent messages when needed