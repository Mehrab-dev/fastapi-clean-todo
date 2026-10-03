
from uuid import UUID

from app.domain.repositories.repositories import TaskRepository
from app.domain.entities.task_entity import Task as task_entity, UpdateTask




class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    # POST /tasks/create
    async def create_task(
        self,
        *,
        user_id: UUID,
        payload: task_entity
    ) -> task_entity:
        return await self.repository.create_task(user_id=user_id, payload=payload)


    # GET /tasks/detail/title
    async def get_task_by_title(
        self,
        *,
        user_id: UUID,
        title: str
    ) -> task_entity | None:
        result = await self.repository.get_task_by_title(user_id=user_id, title=title)
        if result is None:
            raise ValueError("task with this title not found!")
        return result


    # GET /tasks/list
    async def list_tasks(
        self,
        *,
        user_id: UUID
    )   -> list[task_entity]:
        return await self.repository.list_tasks(user_id=user_id)


    # GET /tasks/list-by-status
    async def list_tasks_by_status(
        self,
        *,
        user_id: UUID,
        status_task: bool
    ) -> list[task_entity] | None:
        result = await self.repository.list_tasks_by_status(user_id=user_id, status_task=status_task)
        if result is None:
            raise ValueError(" there are no tasks whit this status")
        return result


    # PUT /tasks/update
    async def update_task(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        payload: UpdateTask
    ) -> task_entity | None:
        result = await self.repository.update_task_by_task_id(user_id=user_id, task_id=task_id, payload=payload)
        if result is None:
            raise ValueError("task not found!")
        return result


    # DELETE /tasks/delete
    async def delete_task(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
    ) -> None:
        result = await self.repository.delete_task_by_task_id(user_id=user_id, task_id=task_id)
        if result is None:
            raise ValueError("does not exists task with task_id")
        return result
           