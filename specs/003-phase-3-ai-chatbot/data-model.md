# Data Model: Phase III - AI-Powered Todo Chatbot

## Overview

This document defines the additional database schema needed for the Phase III AI-powered chatbot functionality. The schema extends the existing Phase II data model by adding entities for conversation tracking while maintaining compatibility with the existing structure.

## New Entities

### Conversation

Represents a user's chat session with the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Default: uuid4() | Unique conversation identifier |
| user_id | UUID | ForeignKey, Not Null | Reference to owning user (foreign key to users.id) |
| title | str | MaxLength: 100 | Auto-generated title for the conversation |
| created_at | datetime | Default: UTC now | Conversation creation timestamp |
| updated_at | datetime | Default: UTC now, OnUpdate: UTC now | Last message timestamp |

**Relationships**:
- Many-to-One with User (many conversations belong to one user)
- One-to-Many with Message (one conversation contains many messages)

**Indexes**:
- `idx_conversation_user_id` on user_id column (filter by owner)
- `idx_conversation_created_at` on created_at for chronological ordering

**Constraints**:
- User must exist when creating conversation
- All conversations are scoped to the authenticated user

### Message

Represents individual user or AI messages within a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Default: uuid4() | Unique message identifier |
| conversation_id | UUID | ForeignKey, Not Null | Reference to parent conversation |
| role | str | Choices: 'user','assistant', Not Null | Who sent the message |
| content | str | MaxLength: 4000, Not Null | The message text content |
| timestamp | datetime | Default: UTC now | When the message was sent |
| metadata | JSON | Nullable | Additional context (intent, parameters, etc.) |

**Relationships**:
- Many-to-One with Conversation (many messages belong to one conversation)
- Cascade delete: When conversation is deleted, all messages are deleted

**Indexes**:
- `idx_message_conversation_id` on conversation_id for conversation retrieval
- `idx_message_timestamp` on timestamp for chronological ordering

**Constraints**:
- Conversation must exist when creating message
- Role must be either 'user' or 'assistant'

## Extended Relationships

### User Extension

The existing User entity maintains relationships with new chat entities:

**New Relationships**:
- One-to-Many with Conversation (user can have many conversations)
- Cascade delete: When user is deleted, all their conversations and messages are deleted

## Entity Relationship Diagram

```
+--------+       +------------------+       +---------+
|  User  |       |  Conversation    |       | Message |
+--------+       +------------------+       +---------+
    |1            |1         *|               |1    *|
    +-------------+           +----------------+     |
    (one-to-many)             (one-to-many)         |
                                                     |
                                                     |
                                                     v
                                            +------------------+
                                            | todo_operations  |
                                            | (via MCP tools)  |
                                            +------------------+
```

## Validation Rules

### Conversation Validation (Pydantic)

```python
# Create conversation validation
user_id: UUID (must exist in users table)
title: Optional[MaxLength(100)] (auto-generated if not provided)

# Query validation
conversation_id: UUID (ownership validated at API layer)
```

### Message Validation (Pydantic)

```python
# Create message validation
conversation_id: UUID (must exist and belong to user)
role: Literal['user', 'assistant'] (strict role validation)
content: MinLength(1), MaxLength(4000) (content length limits)
metadata: Optional[Dict[str, Any]] (flexible metadata for AI context)
```

## Database Migrations

### Migration Tool: Alembic

Existing Alembic setup will be extended to handle new chatbot schema changes.

### New Migration Schema

The new migration creates:
1. `conversations` table with all Conversation fields and constraints
2. `messages` table with all Message fields and constraints
3. Foreign key constraint from conversations.user_id to users.id
4. Foreign key constraint from messages.conversation_id to conversations.id
5. Cascade delete rules for user → conversations → messages relationship
6. All indexes defined above

## Performance Considerations

### Query Patterns

**Frequent Queries**:
- Get all conversations for user (ordered by updated_at DESC)
- Get messages for a specific conversation (ordered by timestamp ASC)
- Get recent messages for conversation context
- Count conversations per user

**Index Strategy**:
- Primary key lookups are optimized by default (B-tree)
- `idx_conversation_user_id` enables fast user-scoped queries
- `idx_message_conversation_id` optimizes message retrieval per conversation
- `idx_message_timestamp` supports chronological message ordering

### Connection Management

- Existing SQLModel connection pooling configuration applies
- No additional pool configuration needed for chat entities
- Connection reuse with existing backend pool

## Security Considerations

### Data Isolation

- All conversation queries MUST include user_id filter
- All message queries MUST include conversation_id filter with user validation
- API layer validates ownership before any chat operations
- Foreign key constraints prevent cross-user data access

### Sensitive Data

- No additional sensitive data beyond existing schema
- Message content is treated as user-generated content
- No PII stored in messages beyond what user explicitly shares
- No authentication tokens or system secrets in chat data

### Access Control

- Conversations and messages are accessible only by owning user
- MCP tools ensure AI operations are properly scoped to user
- No cross-user sharing or collaboration features
- Administrator access follows existing admin patterns if implemented