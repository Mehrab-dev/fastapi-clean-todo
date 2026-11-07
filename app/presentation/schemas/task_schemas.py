
from pydantic import BaseModel, Field

from uuid import UUID
from datetime import datetime



class TaskCreateSchema(BaseModel):
    title: str = Field(..., max_length=255, description="title of the task")
    description: str | None = Field(None, max_length=600, description="description of the task")


class TaskUpdateSchema(BaseModel):
    title: str | None = Field(None, max_length=255, description="title of the task")
    description: str | None = Field(None, max_length=600, description="description of the task")
    is_complete: bool | None = Field(None, description="state of the task")


class TaskResponseSchema(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    is_complete: bool = False
    created_at: datetime
    updated_at: datetime