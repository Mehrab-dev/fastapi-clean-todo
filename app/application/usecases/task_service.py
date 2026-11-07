
from app.application.interface.uow import UnitOfWork

from uuid import UUID

from app.domain.entities import entities
from app.application.dtos.dtos import CreateTaskDTO, UpdateTaskDTO
from app.core.shared.exceptions import NotFoundException
from app.domain.repositories.repositories import TaskRepository



class TaskService:
    def __init__(self, uow: UnitOfWork, repository: TaskRepository):
        self.uow = uow
        self.repository = repository


    async def create(
        self,
        *,
        user_id: UUID,
        payload: CreateTaskDTO
    ) -> entities.Task:
        async with self.uow:
            entity_payload = entities.Task(
                user_id=user_id,
                title=payload.title,
                description=payload.description,
            )
            task = await self.repository.create(user_id=user_id, payload=entity_payload)
            await self.uow.commit()

            return task


    async def get_detail(
        self,
        *,
        user_id: UUID,
        task_id: UUID
    ) -> entities.Task:
        task = await self.repository.get_by_id(user_id=user_id, task_id=task_id)
        if not task:
            raise NotFoundException(
                message="task with this id not found."
            )
        return task


    async def search(
        self,
        *,
        user_id: UUID,
        query: str
    ) -> list[entities.Task]:
        return await self.repository.search_by_title(user_id=user_id, query=query)


    async def list_tasks(
        self,
        *,
        user_id: UUID,
        offset: int = 0,
        limit: int = 5
    ) -> list[entities.Task]:
        return await self.repository.list_tasks(user_id=user_id, offset=offset, limit=limit)


    async def list_tasks_by_status(
        self,
        *,
        user_id: UUID,
        status: bool,
        offset: int = 0,
        limit: int = 5
    ) -> list[entities.Task]:
        return await self.repository.list_tasks_by_status(user_id=user_id, status=status, offset=offset, limit=limit)


    async def update(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        payload: UpdateTaskDTO
    ) -> entities.Task:
        async with self.uow:
            task = await self.repository.get_by_id(user_id=user_id, task_id=task_id)
            if not task:
                raise NotFoundException(
                    message="task with this id not found."
                )

            """ update data """
            if "title" in payload.model_fields_set and payload.title is not None:
                task.update_title(title=payload.title)
            if "description" in payload.model_fields_set:
                task.update_description(description=payload.description)
            if "is_complete" in payload.model_fields_set and payload.is_complete is not None:
                if payload.is_complete:
                    task.complete()
                else:
                    task.uncomplete()

            await self.repository.update(user_id=user_id, task_id=task_id, payload=task)
            await self.uow.commit()

            return task


    async def delete(
        self,
        *,
        user_id: UUID,
        task_id: UUID
    ) -> bool:
        async with self.uow:
            task = await self.repository.get_by_id(user_id=user_id, task_id=task_id)
            if not task:
                raise NotFoundException(
                    message="task with this id not found."
                )

            await self.repository.delete(user_id=user_id, task_id=task_id)
            await self.uow.commit()

            return True