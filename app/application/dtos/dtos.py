
from pydantic import BaseModel
from dataclasses import dataclass



@dataclass(kw_only=True)
class CreateUserDTO:
    email: str
    password: str


class UpdateUserDTO(BaseModel):
    email: str | None = None
    password: str | None = None


class UpdateProfileDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None


@dataclass(kw_only=True)
class CreateTaskDTO:
    title: str
    description: str | None = None


class UpdateTaskDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    is_complete: bool | None = None