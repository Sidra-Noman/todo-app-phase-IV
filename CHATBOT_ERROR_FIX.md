# Chatbot Error Fix - Name Update Feature

## Problem
The user received an error "I couldn't process your request 'add my name sidra noman'. An unexpected error occurred" when trying to set their name via the chatbot.

## Root Causes
1. **No Name Field**: The User model didn't have a `name` field
2. **No Profile Intent**: The intent parser didn't recognize profile-related commands like "add my name"
3. **Wrong Action Type**: Commands like "add my name" were being interpreted as todo creation instead of profile updates

## Solution Implemented

### 1. Updated User Model (`backend/src/models/user.py`)
- Added `name: Optional[str]` field to the User table
- Updated `UserRead` schema to include the name field
- Database migration created to add the column

### 2. Added Profile Intent (`backend/src/schemas/chat_schemas.py`)
- Added `PROFILE = "profile"` to the `ChatAction` enum

### 3. Enhanced Intent Parser (`backend/src/ai/intent_parser.py`)
- Added profile patterns to recognize user intent for name updates:
  - "add my name [name]"
  - "set my name to [name]"
  - "my name is [name]"
  - "call me [name]"
  - "I'm [name]"
- Updated `_map_intent_to_action()` to map "PROFILE" to `ChatAction.PROFILE`

### 4. Added Profile Action Handler (`backend/src/api/chat_router.py`)
- Added profile action case in `_execute_action()` function
- Handles name updates by:
  - Extracting the name from parsed intent
  - Updating the user's name in the database
  - Returning a friendly confirmation message

### 5. Database Migration (`backend/alembic/versions/0003_add_name_to_users.py`)
- Created migration to add `name` column to `users` table
- Supports upgrade and downgrade operations

## How It Works Now
When a user says "add my name sidra noman":
1. Intent parser recognizes it matches the profile pattern
2. Extracts "sidra noman" as the name parameter
3. Returns a PROFILE action with the extracted name
4. The chat router executes the profile action
5. User's name is updated in the database
6. User receives: "Great! I've saved your name as sidra noman."

## Testing
All Python files have been validated for syntax errors:
- ✅ intent_parser.py
- ✅ chat_router.py
- ✅ user.py
- ✅ chat_schemas.py
- ✅ 0003_add_name_to_users.py (migration)

## Next Steps
1. Run the database migration: `python -m alembic upgrade head`
2. Restart the backend server
3. Test with: "add my name sidra noman"
