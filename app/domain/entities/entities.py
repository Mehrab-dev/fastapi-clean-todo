
from dataclasses import dataclass, field

from uuid import UUID
from datetime import datetime

from app.core.shared.datetime import utc_now



@dataclass(kw_only=True)
class User:
    email: str
    password: str
    id: UUID | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def _touch(self) -> None:
        self.updated_at = utc_now()

    def update_email(self, email: str) -> None:
        self.email = email
        self._touch()

    def update_password(self, password: str) -> None:
        self.password = password
        self._touch()

    def activate(self) -> None:
        self.is_active = True
        self._touch()

    def deactivate(self) -> None:
        self.is_active = False
        self._touch()



@dataclass(kw_only=True)
class Profile:
    user_id: UUID
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    image: str | None = None
    id: UUID | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def _touch(self) -> None:
        self.updated_at = utc_now()

    def update_firstname(self, first_name: str) -> None:
        self.first_name = first_name
        self._touch()

    def update_lastname(self, last_name: str) -> None:
        self.last_name = last_name
        self._touch()

    def update_bio(self, bio: str) -> None:
        self.bio = bio
        self._touch()

    def update_image(self, image: str) -> None:
        self.image = image
        self._touch()



@dataclass(kw_only=True)
class Task:
    user_id: UUID
    title: str
    description: str | None = None
    id: UUID | None = None
    is_complete: bool = False
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def _touch(self) -> None:
        self.updated_at = utc_now()

    def update_title(self, title: str) -> None:
        self.title = title
        self._touch()

    def update_description(self, description: str) -> None:
        self.description = description
        self._touch()

    def complete(self) -> None:
        self.is_complete = True
        self._touch()

    def uncomplete(self) -> None:
        self.is_complete = False
        self._touch()
