from dataclasses import dataclass, field

from datetime import datetime, timezone
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


""" user entities """
@dataclass(kw_only=True)
class User:
    id: UUID = field(default_factory=uuid4)
    email: str
    password: str
    is_active: bool = True
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

@dataclass(kw_only=True)
class UpdatePassword:
    new_password: str
    confirm_new_password: str


""" profile entities """
@dataclass(kw_only=True)
class Profile:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(kw_only=True)
class UpdateProfile:
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None




""" task entities """
@dataclass(kw_only=True)
class Task:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    title: str
    description: str | None = None
    status: bool = False
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(kw_only=True)
class UpdateTask:
    title: str | None = None
    description: str | None = None
    status: bool | None = None