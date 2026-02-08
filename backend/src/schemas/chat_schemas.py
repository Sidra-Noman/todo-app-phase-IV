from pydantic import BaseModel
from typing import List, Optional, Literal
from uuid import UUID
from datetime import datetime
from enum import Enum


class ChatAction(str, Enum):
    """Enumeration of possible chat actions."""
    NONE = "none"
    ADD = "add"
    LIST = "list"
    UPDATE = "update"
    DELETE = "delete"
    COMPLETE = "complete"
    PROFILE = "profile"


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str
    conversation_id: Optional[UUID] = None


class TodoItem(BaseModel):
    """Schema for todo items returned in chat responses."""
    id: str  # Changed from UUID to str for JSON serialization
    title: str
    is_complete: bool
    created_at: datetime
    updated_at: datetime


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str
    conversation_id: UUID
    todos: Optional[List[TodoItem]] = None
    action: ChatAction = ChatAction.NONE


class ConversationListItem(BaseModel):
    """Schema for conversation list items."""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationListResponse(BaseModel):
    """Response schema for conversation list."""
    conversations: List[ConversationListItem]
    total: int


class MessageItem(BaseModel):
    """Schema for individual message items."""
    id: UUID
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime


class ConversationDetailResponse(BaseModel):
    """Response schema for conversation detail."""
    conversation: ConversationListItem
    messages: List[MessageItem]


class MessageCreateRequest(BaseModel):
    """Request schema for creating a message."""
    conversation_id: UUID
    role: Literal["user", "assistant"]
    content: str
    metadata: Optional[dict] = None