from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from uuid import UUID

from ..schemas.chat_schemas import (
    ConversationListResponse,
    ConversationDetailResponse,
    MessageCreateRequest
)
from ..services.chat_service import ChatService
from ..api.dependencies import get_current_user
from ..models.user import User
from ..core.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/chat/conversations", tags=["Conversations"])

# Initialize service
chat_service = ChatService()


@router.get("/", response_model=ConversationListResponse)
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


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
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


@router.delete("/{conversation_id}")
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