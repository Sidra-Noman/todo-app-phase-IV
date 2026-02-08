from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class ConversationBase(SQLModel):
    """Base model for Conversation with shared attributes."""
    title: Optional[str] = Field(default=None, max_length=100)


class Conversation(ConversationBase, table=True):
    """Represents a user's chat session with the AI assistant."""
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        cascade_delete=True
    )


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime