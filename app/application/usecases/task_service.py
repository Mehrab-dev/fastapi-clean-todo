
from uuid import UUID

from app.domain.repositories.repositories import TaskRepository
from app.domain.entities import entities



class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository


    async def create_task(
        self,
        *,
        user_id: UUID,
        payload: entities.Task
    ) -> entities.Task:
        return await self.repository.create(user_id=user_id, payload=payload)


    async def search_task(
        self,
        *,
        user_id: UUID,
        title: str
    ) -> list[entities.Task]:
        return await self.repository.search_by_title(user_id=user_id, title=title)


    async def list_tasks(
        self,
        *,
        user_id: UUID,
        offset: int = 0,
        limit: int = 5,
    ) -> list[entities.Task]:
        return await self.repository.list_tasks(user_id=user_id, offset=offset, limit=limit)


    async def list_tasks_by_status(
        self,
        *,
        user_id: UUID,
        status: bool
    ) -> list[entities.Task]:
        return await self.repository.list_by_status(user_id=user_id, status=status)


    async def update_task(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        payload: entities.UpdateTask
    ) -> entities.Task:
        return await self.repository.update_by_task_id(user_id=user_id, task_id=task_id, payload=payload)


    async def delete_task(
        self,
        *,
        user_id: UUID,
        task_id: UUID
    ) -> None:
        await self.repository.delete_by_task_id(user_id=user_id, task_id=task_id)