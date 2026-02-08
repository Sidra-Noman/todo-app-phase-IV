"""
MCP Tool for listing todos.
This tool follows the MCP specification for safe access to todo functionality.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from uuid import UUID
import os
import sys
from pathlib import Path

# Add backend to path so we can import models and services
sys.path.append(os.path.join(Path(__file__).parent.parent.parent.parent, 'backend'))

from backend.src.services.todo_service import TodoService
from backend.src.database import SessionLocal


class TodoListParams(BaseModel):
    is_complete: Optional[bool] = None
    limit: int = 50
    offset: int = 0


def execute_list_todos(params: TodoListParams, user_id: UUID) -> Dict[str, Any]:
    """
    Execute the list todos operation.
    """
    todo_service = TodoService()

    try:
        # Create a new database session
        db = SessionLocal()

        # Get todos
        todos = todo_service.get_todos_by_user(
            db,
            user_id,
            is_complete=params.is_complete,
            limit=params.limit,
            offset=params.offset
        )

        # Prepare response
        result = {
            "success": True,
            "todos": [
                {
                    "id": str(todo.id),
                    "title": todo.title,
                    "is_complete": todo.is_complete,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                } for todo in todos
            ]
        }
    except Exception as e:
        result = {
            "success": False,
            "error": str(e)
        }
    finally:
        db.close()

    return result