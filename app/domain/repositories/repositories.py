
from abc import ABC, abstractmethod

from uuid import UUID

from app.domain.entities import entities



class UserRepository(ABC):
    @abstractmethod
    async def create(self, *, payload: entities.User) -> entities.User:
        ...

    @abstractmethod
    async def get_by_id(self, *, user_id: UUID) -> entities.User | None:
        ...

    @abstractmethod
    async def get_by_email(self, *, email: str) -> entities.User | None:
        ...

    @abstractmethod
    async def update(self, *, user_id: UUID, payload: entities.User) -> entities.User | None:
        ...

    @abstractmethod
    async def delete(self, *, user_id: UUID) -> bool:
        ...



class ProfileRepository(ABC):
    @abstractmethod
    async def create(self, *, user_id: UUID) -> entities.Profile:
        ...

    @abstractmethod
    async def get_by_user_id(self, *, user_id: UUID) -> entities.Profile | None:
        ...

    @abstractmethod
    async def update(self, *, user_id: UUID, payload: entities.Profile) -> entities.Profile | None:
        ...



class TaskRepository(ABC):
    @abstractmethod
    async def create(self, *, user_id: UUID, payload: entities.Task) -> entities.Task:
        ...

    @abstractmethod
    async def get_by_id(self, *, user_id: UUID, task_id: UUID) -> entities.Task | None:
        ...

    @abstractmethod
    async def search_by_title(self, *, user_id: UUID, query: str) -> list[entities.Task]:
        ...

    @abstractmethod
    async def list_tasks(self, *, user_id: UUID, offset: int = 0, limit: int = 5) -> list[entities.Task]:
        ...

    @abstractmethod
    async def list_tasks_by_status(self, *, user_id: UUID, status: bool, offset: int = 0, limit: int = 5) -> list[entities.Task]:
        ...

    @abstractmethod
    async def update(self, *, user_id: UUID, task_id: UUID, payload: entities.Task) -> entities.Task | None:
        ...

    @abstractmethod
    async def delete(self, *, user_id: UUID, task_id: UUID) -> bool:
        ...