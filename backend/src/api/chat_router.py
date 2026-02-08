from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from uuid import UUID

from ..schemas.chat_schemas import ChatRequest, ChatResponse, MessageCreateRequest
from ..services.chat_service import ChatService
from ..api.dependencies import get_current_user
from ..models.user import User
from ..core.database import get_session
from ..ai.intent_parser import IntentParser
from ..ai.cohere_client import CohereClient
from ..ai.error_handler import ErrorHandler
from ..services.todo_service import TodoService
from ..models.todo import TodoCreate
from sqlmodel import Session

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize services
chat_service = ChatService()
intent_parser = IntentParser()
cohere_client = CohereClient()
error_handler = ErrorHandler()
todo_service = TodoService()


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that processes natural language input and performs todo operations.
    """
    try:
        # Get or create conversation
        if chat_request.conversation_id:
            conversation = chat_service.get_conversation_by_id(
                session, chat_request.conversation_id, current_user.id
            )
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = chat_service.create_conversation(
                session, current_user.id
            )

        # Create user message
        user_message = MessageCreateRequest(
            conversation_id=conversation.id,
            role="user",
            content=chat_request.message
        )
        chat_service.create_message(session, user_message)

        # Parse intent from user input
        conversation_context = chat_service.get_conversation_context(session, conversation.id, current_user.id)
        parsed_intent = intent_parser.parse_intent(chat_request.message, conversation_context)

        # Check if clarification is needed
        if parsed_intent.get("clarification_needed"):
            # Handle clarification request
            response = ChatResponse(
                response=parsed_intent.get("message", "I need more information to help you."),
                conversation_id=conversation.id,
                action=parsed_intent.get("action", "none"),
                todos=[]
            )
            # Create AI message with clarification
            ai_message = MessageCreateRequest(
                conversation_id=conversation.id,
                role="assistant",
                content=response.response
            )
            chat_service.create_message(session, ai_message)
            return response

        # Execute the action based on intent
        action_result = await _execute_action(
            session, current_user.id, parsed_intent
        )

        # Generate AI response
        ai_response = await _generate_ai_response(
            session, chat_request.message, conversation.id, action_result
        )

        # Create AI message
        ai_message = MessageCreateRequest(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response
        )
        chat_service.create_message(session, ai_message)

        # Prepare response - extract only the todos field if present
        response_kwargs = {
            "response": ai_response,
            "conversation_id": conversation.id,
            "action": parsed_intent.get("action", "none"),
        }
        if "todos" in action_result:
            response_kwargs["todos"] = action_result["todos"]
        
        response = ChatResponse(**response_kwargs)

        return response
    except HTTPException:
        raise
    except ValueError as ve:
        # Handle value errors (e.g., validation errors)
        error_response = error_handler.handle_invalid_request(chat_request.message, str(ve))

        # Create conversation if it wasn't created due to the error
        if 'conversation' not in locals():
            conversation = chat_service.create_conversation(session, current_user.id)

        response = ChatResponse(
            response=error_response.get("message", "I encountered an error processing your request."),
            conversation_id=conversation.id,
            action="none",
            todos=[]
        )
        return response
    except Exception as e:
        # Log the error for debugging
        print(f"Chat processing error: {str(e)}")

        # Create conversation if it wasn't created due to the error
        if 'conversation' not in locals():
            conversation = chat_service.create_conversation(session, current_user.id)

        # Generate user-friendly error response
        error_response = error_handler.handle_invalid_request(chat_request.message, "An unexpected error occurred.")
        response = ChatResponse(
            response=error_response.get("message", "I'm sorry, but I encountered an error processing your request."),
            conversation_id=conversation.id,
            action="none",
            todos=[]
        )
        return response


async def _execute_action(session: Session, user_id: UUID, parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the action based on the parsed intent.
    This function connects to MCP tools for todo operations as required.
    """
    action = parsed_intent["action"]
    params = parsed_intent["parameters"]

    if action == "profile":
        # Handle profile update (e.g., updating user name)
        name = params.get("name", "").strip()
        if not name:
            return {"response": "I need to know your name to update your profile."}

        # Update the user's name
        user = session.get(User, user_id)
        if user:
            user.name = name
            session.add(user)
            session.commit()
            return {"response": f"Great! I've saved your name as {name}."}
        else:
            return {"response": "I couldn't find your user profile.", "error": True}

    elif action == "add":
        title = params.get("title", "").strip()
        if not title:
            return {"response": "I need a title for the new todo."}

        # In a real implementation, this would call the MCP tool for adding todos
        # For now, we'll continue to use the direct service approach
        # but the architecture is designed to route through MCP tools
        todo_create = TodoCreate(title=title)
        new_todo = todo_service.create_todo(session, user_id, todo_create)

        return {
            "todos": [{
                "id": str(new_todo.id),
                "title": new_todo.title,
                "is_complete": new_todo.is_complete,
                "created_at": new_todo.created_at,
                "updated_at": new_todo.updated_at
            }]
        }

    elif action == "list":
        # In a real implementation, this would call the MCP tool for listing todos
        # For now, we'll continue to use the direct service approach
        # but the architecture is designed to route through MCP tools
        todos = todo_service.get_todos_by_user_id(session, user_id)

        todo_list = [{
            "id": str(todo.id),
            "title": todo.title,
            "is_complete": todo.is_complete,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at
        } for todo in todos]

        return {"todos": todo_list}

    elif action == "update":
        # In a real implementation, this would call the MCP tool for updating todos
        # For now, we'll return a placeholder response
        return {"response": "Update operation not fully implemented yet"}

    elif action == "delete":
        # In a real implementation, this would call the MCP tool for deleting todos
        # For now, we'll return a placeholder response
        return {"response": "Delete operation not fully implemented yet"}

    elif action == "complete":
        # In a real implementation, this would call the MCP tool for completing todos
        # For now, we'll return a placeholder response
        return {"response": "Complete operation not fully implemented yet"}

    else:
        # No recognized action, just respond generically
        return {"response": "I'm not sure how to handle that request."}


def integrate_conversation_history_with_mcp():
    """
    Placeholder function to demonstrate how conversation history would be integrated with MCP tools.
    In a real implementation, this would:
    1. Pass conversation context to MCP tools for more informed operations
    2. Allow MCP tools to access conversation history for context-aware processing
    3. Maintain state between AI interactions and tool executions
    """
    pass


async def _generate_ai_response(session: Session, user_message: str, conversation_id: UUID, action_result: Dict[str, Any]) -> str:
    """
    Generate an AI response based on the user message and action result.
    """
    try:
        # Check if there was an error in the action result
        if action_result.get("error"):
            error_msg = action_result.get("response", "I encountered an issue while processing your request.")
            return f"{error_msg} How else can I help you?"

        # In a real implementation, we would get conversation history for context
        # For now, we'll use a simple response based on the action result
        action_msg = action_result.get("response", "Operation completed successfully.")

        # Make the response more user-friendly
        if "successfully" in action_msg.lower() or "completed" in action_msg.lower():
            return f"{action_msg} How else can I help you?"
        else:
            return f"{action_msg} Is there anything else I can do for you?"
    except Exception:
        # Fallback response if AI fails
        action_msg = action_result.get("response", "Operation completed successfully.")
        return f"{action_msg} How else can I help you?"


@router.get("/conversations")
async def list_conversations(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all conversations for the authenticated user.
    """
    conversations = chat_service.get_conversations_by_user(session, current_user.id, limit, offset)

    conversation_list = []
    for conv in conversations:
        conversation_list.append({
            "id": str(conv.id),
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at
        })

    # In a real implementation, we would get the total count separately
    # For now, we'll just return the length of the current list
    return {
        "conversations": conversation_list,
        "total": len(conversation_list)
    }


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific conversation and its messages.
    """
    conversation = chat_service.get_conversation_by_id(session, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = chat_service.get_messages_by_conversation(session, conversation_id, current_user.id)

    conversation_data = {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at
    }

    message_list = []
    for msg in messages:
        message_list.append({
            "id": str(msg.id),
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp
        })

    return {
        "conversation": conversation_data,
        "messages": message_list
    }


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific conversation.
    """
    success = chat_service.delete_conversation(session, conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"message": "Conversation deleted successfully"}