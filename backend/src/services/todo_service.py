from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models.todo import Todo
from ..schemas.todo import TodoCreate, TodoUpdate

class TodoService:
    @staticmethod
    def get_todos_by_user_id(session: Session, user_id: UUID, is_complete: Optional[bool] = None) -> List[Todo]:
        statement = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        if is_complete is not None:
            statement = statement.where(Todo.is_complete == is_complete)
        return session.exec(statement).all()

    @staticmethod
    def create_todo(session: Session, user_id: UUID, todo_data: TodoCreate) -> Todo:
        new_todo = Todo(
            user_id=user_id,
            title=todo_data.title,
            is_complete=False
        )
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        return new_todo

    @staticmethod
    def get_todo_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def update_todo(session: Session, todo: Todo, todo_update: TodoUpdate) -> Todo:
        update_data = todo_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo, key, value)
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(session: Session, todo: Todo) -> None:
        session.delete(todo)
        session.commit()

    @staticmethod
    def toggle_todo(session: Session, todo: Todo) -> Todo:
        todo.is_complete = not todo.is_complete
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
