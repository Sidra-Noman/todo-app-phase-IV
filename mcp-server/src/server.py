from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID
import uvicorn

from .config import mcp_config
from .tools.todo_tools import (
    TodoTools, TodoAddParams, TodoUpdateParams,
    TodoCompleteParams, TodoDeleteParams, TodoListParams
)

# Initialize FastAPI app
app = FastAPI(
    title="Todo App MCP Tools API",
    description="MCP tools for AI-powered todo operations",
    version="1.0.0"
)

# Initialize tools
todo_tools = TodoTools()


def get_user_from_session():  # Placeholder for actual session validation
    """
    Placeholder for getting user ID from session.
    In a real implementation, this would extract user info from the session context.
    """
    # For now, we'll return a mock user ID
    # In practice, this would come from the authentication context
    return UUID("12345678-1234-5678-9abc-123456789abc")


@app.post("/api/mcp/tools/todos/add")
async def add_todo_endpoint(params: TodoAddParams, user_id: UUID = Depends(get_user_from_session)):
    """
    Add a new todo via MCP tool.
    """
    result = todo_tools.add_todo(params, user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.get("/api/mcp/tools/todos/list")
async def list_todos_endpoint(
    is_complete: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    user_id: UUID = Depends(get_user_from_session)
):
    """
    List todos via MCP tool.
    """
    params = TodoListParams(is_complete=is_complete, limit=limit, offset=offset)
    result = todo_tools.list_todos(params, user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.patch("/api/mcp/tools/todos/{todo_id}/update")
async def update_todo_endpoint(
    todo_id: UUID,
    title: Optional[str] = None,
    is_complete: Optional[bool] = None,
    user_id: UUID = Depends(get_user_from_session)
):
    """
    Update a todo via MCP tool.
    """
    params = TodoUpdateParams(todo_id=todo_id, title=title, is_complete=is_complete)
    result = todo_tools.update_todo(params, user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.delete("/api/mcp/tools/todos/{todo_id}/delete")
async def delete_todo_endpoint(
    todo_id: UUID,
    user_id: UUID = Depends(get_user_from_session)
):
    """
    Delete a todo via MCP tool.
    """
    params = TodoDeleteParams(todo_id=todo_id)
    result = todo_tools.delete_todo(params, user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.post("/api/mcp/tools/todos/{todo_id}/complete")
async def complete_todo_endpoint(
    todo_id: UUID,
    user_id: UUID = Depends(get_user_from_session)
):
    """
    Complete a todo via MCP tool.
    """
    params = TodoCompleteParams(todo_id=todo_id)
    result = todo_tools.complete_todo(params, user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "mcp-server"}


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=mcp_config.server_host,
        port=mcp_config.server_port,
        reload=mcp_config.debug
    )