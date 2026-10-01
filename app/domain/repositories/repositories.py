from abc import ABC, abstractmethod

from uuid import UUID

from app.domain.entities.user_entity import User as user_entity
from app.domain.entities.profile_entity import Profile as profile_entity, UpdateProfile
from app.domain.entities.task_entity import Task as task_entity, UpdateTask




class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, *, payload: user_entity) -> str:
        raise NotImplementedError

    @abstractmethod
    async def update_email_by_id(self, *, id: UUID, new_email: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def update_password_by_id(self, *, id: UUID, new_password: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, *, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, *, email: str) -> user_entity | None:
        raise NotImplementedError



class ProfileRepository(ABC):
    @abstractmethod
    async def create_profile_by_user_id(self, *, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_profile_by_user_id(self, *, user_id: UUID) -> profile_entity | None:
        raise NotImplementedError

    @abstractmethod
    async def update_profile(self, *, user_id: UUID, payload: UpdateProfile, image: str | None) -> profile_entity | None:
        raise NotImplementedError



class TaskRepository(ABC):
    @abstractmethod
    async def create_task(self, *, user_id: UUID, payload: task_entity) -> task_entity:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_title(self, *, user_id: UUID, title: str) -> task_entity | None:
        raise NotImplementedError

    @abstractmethod
    async def list_tasks(self, *, user_id: UUID, offset: int = 0, limit: int = 5) -> list[task_entity]:
        raise NotImplementedError

    @abstractmethod
    async def list_tasks_by_status(self, *, user_id: UUID, status: bool, offset: int = 0, limit: int = 5) -> list[task_entity]:
        raise NotImplementedError

    @abstractmethod
    async def update_task_by_task_id(self,  *, user_id: UUID, task_id: UUID, payload: UpdateTask) -> task_entity | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_task_by_task_id(self, *, user_id: UUID, task_id: UUID) -> None:
        raise NotImplementedError