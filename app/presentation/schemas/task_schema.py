from pydantic import BaseModel, Field

from typing import Optional
from datetime import datetime



class TaskCreateSchema(BaseModel):
    title: str = Field(..., max_length=255, description="title of the task")
    description: Optional[str] = Field(None, max_length=600, description="description of the task")
    status_task: bool = Field(..., description="state of the task")



class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255, description="title of the task for update")
    description: Optional[str] = Field(None, max_length=600, description="description of the task for update")
    status_task: Optional[bool] = Field(None, description="state of the task for update")



class TaskResponseSchema(BaseModel):
    title: str
    description: str | None = None
    status_task: bool
    created_at: datetime
    updated_at: datetime