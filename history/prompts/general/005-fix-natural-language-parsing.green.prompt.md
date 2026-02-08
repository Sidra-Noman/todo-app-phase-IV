---
id: 5
title: "Fix Natural Language Parsing"
stage: green
date_iso: 2026-01-21
surface: agent
model: claude-sonnet-4-5-20250929
feature: "none"
branch: main
user: unknown
command: "manual"
labels: ["chatbot", "intent-parsing", "natural-language", "ai", "todo", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/ai/intent_parser.py"
  - "backend/src/ai/cohere_client.py"
tests_yaml:
  - "simple_test.py (temporary)"
outcome_impact: "Natural language tasks like 'lunch at 2:00' are now correctly added to the to-do list"
tests_summary: "Created and ran tests to verify intent parsing for natural language inputs"
files_summary: "Updated intent parser to recognize natural language patterns for todo creation"
next_prompts: "None"
reflection_note: "Natural language processing requires careful pattern matching to avoid false positives while catching valid inputs"
---

# Fix Natural Language Parsing

## Original Prompt
```
In my To-Do app chatbot, when I send "lunch at 2:00" it replies it can't handle the request.
Please fix the intent parsing/logic so natural language tasks are correctly added to the to-do list.
```

## Summary of Work Completed
Fixed the chatbot's intent parsing to correctly recognize natural language inputs like "lunch at 2:00" and add them to the to-do list. The issue was that the rule-based parser only recognized explicit commands like "add" or "create", but not natural language patterns.

## Changes Made
1. Updated the intent parser in `backend/src/ai/intent_parser.py` to recognize natural language patterns:
   - Added time expression patterns (e.g., "2:00", "3pm")
   - Added activity word recognition (e.g., "lunch", "meeting", "call")
   - Added temporal phrases (e.g., "tomorrow", "afternoon")
   - Added logic to avoid false positives for questions
2. Enhanced the Cohere classification examples in `backend/src/ai/cohere_client.py` with natural language samples

## Technical Details
- Prioritized time-based patterns with higher confidence (0.65) for time-sensitive tasks
- Implemented context-aware pattern matching to avoid false positives
- Maintained backward compatibility with explicit commands
- Added safeguards against misinterpreting questions as tasks

## Outcome
- Natural language inputs like "lunch at 2:00" are now correctly identified as ADD actions
- Time-based tasks receive higher confidence scores for better accuracy
- Activity-based inputs are properly captured as to-dos
- Question patterns are correctly avoided to prevent false positives
- Backward compatibility maintained for existing explicit commands

## Acceptance Criteria Met
- [x] "lunch at 2:00" correctly adds a todo with that title
- [x] Time expressions trigger ADD actions with appropriate confidence
- [x] Activity words in natural language trigger ADD actions
- [x] Questions are not misinterpreted as tasks
- [x] Existing functionality remains intact