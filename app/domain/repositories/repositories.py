from abc import abstractmethod, ABC

from uuid import UUID

from app.domain.entities import entities



class UserRepository(ABC):
    @abstractmethod
    async def create(self, *, payload: entities.User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, *, email: str) -> entities.User | None:
        raise NotImplementedError

    @abstractmethod
    async def update_email_by_id(self, *, id: UUID, new_email: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_password_by_id(self, *, id: UUID, payload: entities.UpdatePassword) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *, id: UUID) -> None:
        raise NotImplementedError



class ProfileRepository(ABC):
    @abstractmethod
    async def create(self, *, user_id: UUID, payload: entities.Profile) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, *, user_id: UUID) -> entities.Profile | None:
        raise NotImplementedError

    @abstractmethod
    async def update_by_user_id(self, *, user_id: UUID, payload: entities.UpdateProfile) -> entities.Profile | None:
        raise NotImplementedError



class TaskRepository(ABC):
    @abstractmethod
    async def create(self, *, user_id: UUID, payload: entities.Task) -> entities.Task:
        raise NotImplementedError

    @abstractmethod
    async def search_by_title(self, *, user_id: UUID, title: str) -> list[entities.Task]:
        raise NotImplementedError

    @abstractmethod
    async def list_tasks(self, *, user_id: UUID, offset: int = 0, limit: int = 5) -> list[entities.Task]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, *, user_id: UUID, status: bool) -> list[entities.Task]:
        raise NotImplementedError

    @abstractmethod
    async def update_by_task_id(self, *, user_id: UUID, task_id: UUID, payload: entities.UpdateTask) -> entities.Task | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_task_id(self, *, user_id: UUID, task_id: UUID) -> None:
        raise NotImplementedError