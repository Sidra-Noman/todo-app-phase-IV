from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from ..models.user import User


class ChatService:
    """
    Service layer for chat operations including conversation and message management.
    """

    def create_conversation(self, session: Session, user_id: UUID, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation for a user.
        """
        # Auto-generate title if not provided
        if not title:
            title = f"Chat {self._generate_default_title()}"

        conversation = Conversation(user_id=user_id, title=title)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, session: Session, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
        """
        Retrieve a conversation by ID for a specific user (ensures data isolation).
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    def get_conversations_by_user(self, session: Session, user_id: UUID, limit: int = 20, offset: int = 0) -> List[Conversation]:
        """
        Retrieve all conversations for a specific user.
        """
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)
        return session.exec(statement).all()

    def delete_conversation(self, session: Session, conversation_id: UUID, user_id: UUID) -> bool:
        """
        Delete a conversation by ID for a specific user.
        """
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if conversation:
            session.delete(conversation)
            session.commit()
            return True
        return False

    def create_message(self, session: Session, message_create: MessageCreate) -> Message:
        """
        Create a new message in a conversation.
        """
        message_data = message_create.model_dump() if hasattr(message_create, 'model_dump') else message_create.dict()
        message = Message(**message_data)
        session.add(message)
        session.commit()
        session.refresh(message)

        # Update the conversation's updated_at timestamp
        conversation = self.get_conversation_by_id(session, message.conversation_id,
                                                 self._get_conversation_owner(session, message.conversation_id))
        if conversation:
            conversation.updated_at = message.timestamp
            session.add(conversation)
            session.commit()

        return message

    def get_messages_by_conversation(self, session: Session, conversation_id: UUID, user_id: UUID) -> List[Message]:
        """
        Retrieve all messages for a specific conversation (ensures user owns the conversation).
        """
        # First verify the user owns the conversation
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []

        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc())
        return session.exec(statement).all()

    def get_recent_messages_by_conversation(self, session: Session, conversation_id: UUID, user_id: UUID, limit: int = 10) -> List[Message]:
        """
        Retrieve recent messages for a specific conversation (for context in AI processing).
        """
        # First verify the user owns the conversation
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []

        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.desc()).limit(limit)
        messages = session.exec(statement).all()

        # Reverse the order to return oldest first
        return list(reversed(messages))

    def get_conversation_context(self, session: Session, conversation_id: UUID, user_id: UUID) -> Dict[str, Any]:
        """
        Get conversation context for AI processing.
        """
        # Get recent messages for context
        recent_messages = self.get_recent_messages_by_conversation(session, conversation_id, user_id)

        # Get the user's todos for context
        # Note: We'd need to import todo service for this, but we'll leave it as a placeholder
        # since importing here would create circular dependencies

        context = {
            "recent_messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                } for msg in recent_messages
            ],
            "recent_items": [],  # This would be populated with recent todo items
            "conversation_id": conversation_id
        }

        return context

    def _generate_default_title(self) -> str:
        """
        Generate a default title for a new conversation.
        """
        from datetime import datetime
        return f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    def _get_conversation_owner(self, session: Session, conversation_id: UUID) -> Optional[UUID]:
        """
        Get the user ID that owns a conversation.
        """
        conversation = session.get(Conversation, conversation_id)
        return conversation.user_id if conversation else None