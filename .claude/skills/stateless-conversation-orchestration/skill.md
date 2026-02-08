# Skill: Stateless Conversation Orchestration

## When to Use This Skill
- Handling chat API requests
- Managing conversation history

## How This Skill Works
1. Load conversation from database
2. Append new user message
3. Run AI agent
4. Store assistant response
5. Return response
6. Retain no in-memory state

## Output Format
- conversation_id
- assistant response
- tool calls (if any)

## Quality Criteria
- Fully stateless
- Restart-safe
- Deterministic behavior