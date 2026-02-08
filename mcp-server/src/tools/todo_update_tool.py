"""
MCP Tool for updating todos.
This tool follows the MCP specification for safe access to todo functionality.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from uuid import UUID
import os
import sys
from pathlib import Path

# Add backend to path so we can import models and services
sys.path.append(os.path.join(Path(__file__).parent.parent.parent.parent, 'backend'))

from backend.src.services.todo_service import TodoService
from backend.src.models.todo import TodoUpdate
from backend.src.database import SessionLocal


class TodoUpdateParams(BaseModel):
    todo_id: UUID
    title: Optional[str] = None
    is_complete: Optional[bool] = None


def execute_update_todo(params: TodoUpdateParams, user_id: UUID) -> Dict[str, Any]:
    """
    Execute the update todo operation.
    """
    todo_service = TodoService()

    try:
        # Create a new database session
        db = SessionLocal()

        # Prepare update data
        todo_update = TodoUpdate()
        if params.title is not None:
            todo_update.title = params.title
        if params.is_complete is not None:
            todo_update.is_complete = params.is_complete

        # Update the todo
        updated_todo = todo_service.update_todo(db, params.todo_id, todo_update, user_id)

        if updated_todo:
            result = {
                "success": True,
                "todo": {
                    "id": str(updated_todo.id),
                    "title": updated_todo.title,
                    "is_complete": updated_todo.is_complete,
                    "created_at": updated_todo.created_at.isoformat(),
                    "updated_at": updated_todo.updated_at.isoformat()
                }
            }
        else:
            result = {
                "success": False,
                "error": "Todo not found or not owned by user"
            }
    except Exception as e:
        result = {
            "success": False,
            "error": str(e)
        }
    finally:
        db.close()

    return result