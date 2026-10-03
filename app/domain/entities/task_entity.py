from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import date, datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(kw_only=True)
class Task:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    title: str
    description: str | None = None
    status_task: bool
    created_at: date = field(default_factory=utc_now)
    updated_at: date = field(default_factory=utc_now)


@dataclass(kw_only=True)
class UpdateTask:
    title: str | None = None
    description: str | None = None
    status_task: bool | None = None