from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import date, datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)



@dataclass(kw_only=True)
class Profile:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None
    created_at: date = field(default_factory=utc_now)
    updated_at: date = field(default_factory=utc_now)


@dataclass(kw_only=True)
class UpdateProfile:
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None