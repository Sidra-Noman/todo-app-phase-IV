from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    is_complete: Optional[bool] = None

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic.config import ConfigDict

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    is_complete: Optional[bool] = None

class TodoResponse(TodoBase):
    id: UUID
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TodoListResponse(BaseModel):
    todos: List[TodoResponse]
    total: int

class TodoSingleResponse(BaseModel):
    todo: TodoResponse
