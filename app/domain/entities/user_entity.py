from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import date, datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)



@dataclass(kw_only=True)
class User:
    id: UUID = field(default_factory=uuid4)
    email: str
    password: str
    is_active: bool
    created_at: date = field(default_factory=utc_now)
    updated_at: date = field(default_factory=utc_now)