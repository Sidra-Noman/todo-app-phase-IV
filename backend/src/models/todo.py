from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class TodoBase(SQLModel):
    title: str = Field(max_length=500)
    is_complete: bool = Field(default=False)


class Todo(TodoBase, table=True):
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)  # Fixed the foreign key reference
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    title: str


class TodoRead(TodoBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    is_complete: Optional[bool] = None


from .user import User
