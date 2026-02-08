from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .todo import Todo
    from .conversation import Conversation


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    todos: List["Todo"] = Relationship(back_populates="user", cascade_delete=True)
    conversations: List["Conversation"] = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    name: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserSignIn(SQLModel):
    email: str
    password: str
