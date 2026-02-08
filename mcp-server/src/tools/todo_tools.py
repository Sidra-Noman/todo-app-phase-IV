from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from uuid import UUID
import os
import sys
from pathlib import Path

# Add backend to path so we can import models and services
sys.path.append(os.path.join(Path(__file__).parent.parent.parent.parent, 'backend'))

from backend.src.services.todo_service import TodoService
from backend.src.models.todo import TodoCreate, TodoUpdate
from backend.src.database import SessionLocal
from backend.src.core.auth import verify_token


class TodoAddParams(BaseModel):
    title: str
    is_complete: Optional[bool] = False


class TodoUpdateParams(BaseModel):
    todo_id: Optional[UUID] = None  # Can be None if using reference
    title: Optional[str] = None
    is_complete: Optional[bool] = None
    reference: Optional[str] = None  # For ambiguous references like "the first one", "the grocery todo", etc.


class TodoCompleteParams(BaseModel):
    todo_id: Optional[UUID] = None  # Can be None if using reference
    reference: Optional[str] = None  # For ambiguous references


class TodoDeleteParams(BaseModel):
    todo_id: Optional[UUID] = None  # Can be None if using reference
    reference: Optional[str] = None  # For ambiguous references


class TodoListParams(BaseModel):
    is_complete: Optional[bool] = None
    limit: Optional[int] = 50
    offset: Optional[int] = 0


class TodoTools:
    """
    MCP-compatible tools for todo operations.
    These tools follow the MCP specification and provide safe access to todo functionality.
    """

    def __init__(self):
        self.todo_service = TodoService()

    def _handle_ambiguous_reference(self, reference: str, user_id: UUID) -> list:
        """
        Helper method to handle ambiguous references to todos (e.g., 'the first one', 'it', etc.)
        """
        # Get all todos for the user
        db = SessionLocal()
        try:
            all_todos = self.todo_service.get_todos_by_user(db, user_id)

            # Match based on the reference
            matched_todos = []
            if reference and reference.lower() != "it" and reference.lower() != "that":
                # Look for todos that match the reference
                for todo in all_todos:
                    if reference.lower() in todo.title.lower():
                        matched_todos.append(todo)
            else:
                # If reference is vague ('it', 'that'), return all todos as ambiguous
                matched_todos = all_todos

            return matched_todos
        finally:
            db.close()

    def add_todo(self, params: TodoAddParams, user_id: UUID) -> Dict[str, Any]:
        """
        Add a new todo for the authenticated user.
        """
        try:
            # Create a new database session
            db = SessionLocal()

            # Create the todo
            todo_create = TodoCreate(title=params.title, is_complete=params.is_complete)
            new_todo = self.todo_service.create_todo(db, todo_create, user_id)

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

    def list_todos(self, params: TodoListParams, user_id: UUID) -> Dict[str, Any]:
        """
        List todos for the authenticated user with optional filters.
        """
        try:
            # Create a new database session
            db = SessionLocal()

            # Get todos
            todos = self.todo_service.get_todos_by_user(
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

    def update_todo(self, params: TodoUpdateParams, user_id: UUID) -> Dict[str, Any]:
        """
        Update an existing todo for the authenticated user.
        """
        try:
            # Create a new database session
            db = SessionLocal()

            # Check if todo_id was provided, if not, try to resolve from reference
            todo_id = params.todo_id
            if not todo_id and params.reference:
                # Handle ambiguous reference
                matched_todos = self._handle_ambiguous_reference(params.reference, user_id)

                if len(matched_todos) == 0:
                    result = {
                        "success": False,
                        "error": f"No todos found matching '{params.reference}'",
                        "clarification_needed": True,
                        "available_options": []
                    }
                elif len(matched_todos) > 1:
                    # Multiple matches - need clarification
                    result = {
                        "success": False,
                        "error": f"Multiple todos match '{params.reference}'. Please be more specific.",
                        "clarification_needed": True,
                        "available_options": [
                            {"id": str(todo.id), "title": todo.title} for todo in matched_todos
                        ]
                    }
                else:
                    # Single match found
                    todo_id = matched_todos[0].id

            # Prepare update data if we have a valid todo_id
            if todo_id:
                todo_update = TodoUpdate()
                if params.title is not None:
                    todo_update.title = params.title
                if params.is_complete is not None:
                    todo_update.is_complete = params.is_complete

                # Update the todo
                updated_todo = self.todo_service.update_todo(db, todo_id, todo_update, user_id)

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
            else:
                # If we couldn't resolve the todo, return the error from ambiguity handling
                pass  # result already set above

        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()

        return result

    def delete_todo(self, params: TodoDeleteParams, user_id: UUID) -> Dict[str, Any]:
        """
        Delete a todo for the authenticated user.
        """
        try:
            # Create a new database session
            db = SessionLocal()

            # Check if todo_id was provided, if not, try to resolve from reference
            todo_id = params.todo_id
            if not todo_id and params.reference:
                # Handle ambiguous reference
                matched_todos = self._handle_ambiguous_reference(params.reference, user_id)

                if len(matched_todos) == 0:
                    result = {
                        "success": False,
                        "error": f"No todos found matching '{params.reference}'",
                        "clarification_needed": True,
                        "available_options": []
                    }
                elif len(matched_todos) > 1:
                    # Multiple matches - need clarification
                    result = {
                        "success": False,
                        "error": f"Multiple todos match '{params.reference}'. Please be more specific.",
                        "clarification_needed": True,
                        "available_options": [
                            {"id": str(todo.id), "title": todo.title} for todo in matched_todos
                        ]
                    }
                else:
                    # Single match found
                    todo_id = matched_todos[0].id

            if todo_id:
                # Delete the todo
                success = self.todo_service.delete_todo(db, todo_id, user_id)

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
            else:
                # If we couldn't resolve the todo, return the error from ambiguity handling
                pass  # result already set above

        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()

        return result

    def complete_todo(self, params: TodoCompleteParams, user_id: UUID) -> Dict[str, Any]:
        """
        Mark a todo as complete for the authenticated user.
        """
        try:
            # Create a new database session
            db = SessionLocal()

            # Check if todo_id was provided, if not, try to resolve from reference
            todo_id = params.todo_id
            if not todo_id and params.reference:
                # Handle ambiguous reference
                matched_todos = self._handle_ambiguous_reference(params.reference, user_id)

                if len(matched_todos) == 0:
                    result = {
                        "success": False,
                        "error": f"No todos found matching '{params.reference}'",
                        "clarification_needed": True,
                        "available_options": []
                    }
                elif len(matched_todos) > 1:
                    # Multiple matches - need clarification
                    result = {
                        "success": False,
                        "error": f"Multiple todos match '{params.reference}'. Please be more specific.",
                        "clarification_needed": True,
                        "available_options": [
                            {"id": str(todo.id), "title": todo.title} for todo in matched_todos
                        ]
                    }
                else:
                    # Single match found
                    todo_id = matched_todos[0].id

            if todo_id:
                # Update the todo to be complete
                updated_todo = self.todo_service.update_todo(
                    db,
                    todo_id,
                    TodoUpdate(is_complete=True),
                    user_id
                )

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
            else:
                # If we couldn't resolve the todo, return the error from ambiguity handling
                pass  # result already set above

        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()

        return result