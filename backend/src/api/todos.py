from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List
from uuid import UUID
from ..core.database import get_session
from ..models.user import User
from ..schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse, TodoSingleResponse
from ..services.todo_service import TodoService
from .dependencies import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", response_model=TodoListResponse)
def list_todos(
    isComplete: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todos = TodoService.get_todos_by_user_id(session, current_user.id, isComplete)
    # Apply pagination manually for simple Phase II
    paginated_todos = todos[offset : offset + limit]

    return {
        "todos": [
            {
                "id": t.id,
                "title": t.title,
                "is_complete": t.is_complete,
                "created_at": t.created_at,
                "updated_at": t.updated_at
            } for t in paginated_todos
        ],
        "total": len(todos)
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoSingleResponse)
def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = TodoService.create_todo(session, current_user.id, todo_data)
    return {
        "todo": {
            "id": todo.id,
            "title": todo.title,
            "is_complete": todo.is_complete,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at
        }
    }

@router.get("/{todoId}", response_model=TodoSingleResponse)
def get_todo(
    todoId: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = TodoService.get_todo_by_id(session, todoId, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {
        "todo": {
            "id": todo.id,
            "title": todo.title,
            "is_complete": todo.is_complete,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at
        }
    }

@router.patch("/{todoId}", response_model=TodoSingleResponse)
def update_todo(
    todoId: UUID,
    todo_update: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = TodoService.get_todo_by_id(session, todoId, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo = TodoService.update_todo(session, todo, todo_update)
    return {
        "todo": {
            "id": updated_todo.id,
            "title": updated_todo.title,
            "is_complete": updated_todo.is_complete,
            "created_at": updated_todo.created_at,
            "updated_at": updated_todo.updated_at
        }
    }

@router.delete("/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todoId: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = TodoService.get_todo_by_id(session, todoId, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    TodoService.delete_todo(session, todo)
    return None

@router.post("/{todoId}/toggle", response_model=TodoSingleResponse)
def toggle_todo(
    todoId: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = TodoService.get_todo_by_id(session, todoId, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    toggled_todo = TodoService.toggle_todo(session, todo)
    return {
        "todo": {
            "id": toggled_todo.id,
            "title": toggled_todo.title,
            "is_complete": toggled_todo.is_complete,
            "created_at": toggled_todo.created_at,
            "updated_at": toggled_todo.updated_at
        }
    }
