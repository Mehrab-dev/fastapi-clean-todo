
from pydantic import BaseModel, Field

from uuid import UUID
from datetime import datetime



class ProfileUpdateSchema(BaseModel):
    first_name: str | None = Field(None, max_length=255, description="first name of the user")
    last_name: str | None = Field(None, max_length=255, description="last name of the user")
    bio: str | None = Field(None, max_length=600, description="bio of the user")


class ProfileResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None
    created_at: datetime
    updated_at: datetime