from datetime import datetime
from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from sqlalchemy import JSON

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageBase(SQLModel):
    """Base model for Message with shared attributes."""
    role: str = Field(regex="^(user|assistant)$")  # Role must be either 'user' or 'assistant'
    content: str = Field(min_length=1, max_length=4000)  # Content length limits
    metadata_: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)  # Metadata field as JSON type


class Message(MessageBase, table=True):
    """Represents individual user or AI messages within a conversation."""
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    conversation_id: UUID


class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: UUID
    conversation_id: UUID
    timestamp: datetime