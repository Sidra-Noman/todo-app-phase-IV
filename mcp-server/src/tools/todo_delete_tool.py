"""
MCP Tool for deleting todos.
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
from backend.src.database import SessionLocal


class TodoDeleteParams(BaseModel):
    todo_id: UUID


def execute_delete_todo(params: TodoDeleteParams, user_id: UUID) -> Dict[str, Any]:
    """
    Execute the delete todo operation.
    """
    todo_service = TodoService()

    try:
        # Create a new database session
        db = SessionLocal()

        # Delete the todo
        success = todo_service.delete_todo(db, params.todo_id, user_id)

        if success:
            result = {
                "success": True,
                "message": "Todo deleted successfully"
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