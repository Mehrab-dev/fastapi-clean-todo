from pydantic import BaseModel, Field

from typing import Optional
from datetime import datetime



class ProfileResponseSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None
    created_at: datetime
    updated_at: datetime




class ProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None