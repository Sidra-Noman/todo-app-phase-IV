"""
MCP Tool for adding todos.
This tool follows the MCP specification for safe access to todo functionality.
"""

from typing import Dict, Any
from pydantic import BaseModel
from uuid import UUID
import os
import sys
from pathlib import Path

# Add backend to path so we can import models and services
sys.path.append(os.path.join(Path(__file__).parent.parent.parent.parent, 'backend'))

from backend.src.services.todo_service import TodoService
from backend.src.models.todo import TodoCreate
from backend.src.database import SessionLocal


class TodoAddParams(BaseModel):
    title: str
    is_complete: bool = False


def execute_add_todo(params: TodoAddParams, user_id: UUID) -> Dict[str, Any]:
    """
    Execute the add todo operation.
    """
    todo_service = TodoService()

    try:
        # Create a new database session
        db = SessionLocal()

        # Create the todo
        todo_create = TodoCreate(title=params.title, is_complete=params.is_complete)
        new_todo = todo_service.create_todo(db, todo_create, user_id)

        # Prepare response
        result = {
            "success": True,
            "todo": {
                "id": str(new_todo.id),
                "title": new_todo.title,
                "is_complete": new_todo.is_complete,
                "created_at": new_todo.created_at.isoformat(),
                "updated_at": new_todo.updated_at.isoformat()
            }
        }
    except Exception as e:
        result = {
            "success": False,
            "error": str(e)
        }
    finally:
        db.close()

    return result