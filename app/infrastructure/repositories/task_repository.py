from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import TaskRepository
from app.domain.entities.task_entity import Task as task_entity, UpdateTask
from app.infrastructure.database.mappers import TaskMapper
from app.infrastructure.database.models import TaskModel



class SqlalchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, *, user_id: UUID, payload: task_entity) -> task_entity:
        model = TaskMapper.to_model(entity=payload)
        model.user_id = user_id
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return TaskMapper.to_domain(model=model)


    async def get_task_by_title(self, *, user_id: UUID, title: str) -> task_entity | None:
        statement = select(TaskModel).where(TaskModel.title == title, TaskModel.user_id == user_id)
        result = await self.session.execute(statement=statement)
        task = result.scalar_one_or_none()
        if task is None:
            return None
        return TaskMapper.to_domain(model=task)


    async def list_tasks(self, *, user_id: UUID, offset: int = 0, limit: int = 5) -> list[task_entity]:
        statement = select(TaskModel).where(TaskModel.user_id == user_id).offset(offset=offset).limit(limit=limit)
        result = await self.session.execute(statement=statement)
        tasks = result.scalars()
        return [TaskMapper.to_domain(task) for task in tasks]


    async def list_tasks_by_status(self, *, user_id: UUID, status_task: bool, offset: int = 0, limit: int = 5) -> list[task_entity]:
        statement = select(TaskModel).where(TaskModel.user_id == user_id, TaskModel.status_task == status_task).offset(offset=offset).limit(limit=limit)
        result = await self.session.execute(statement=statement)
        tasks = result.scalars()

        return [TaskMapper.to_domain(task) for task in tasks]


    async def update_task_by_task_id(self, *, user_id: UUID, task_id: UUID, payload: UpdateTask) -> task_entity | None:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.id == task_id
            )
        result = await self.session.execute(statement=statement)
        task = result.scalar_one_or_none()
        if task is None:
            return None
        
        """ change data """
        if payload.title is not None:
            task.title = payload.title
        if payload.description is not None:
            task.description = payload.description
        if payload.status_task is not None:
            task.status_task = payload.status_task
        await self.session.commit()
        await self.session.refresh(task)
        return TaskMapper.to_domain(model=task)


    async def delete_task_by_task_id(self, *, user_id: UUID, task_id: UUID) -> None:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.id == task_id
        )
        result = await self.session.execute(statement=statement)
        task = result.scalar_one_or_none()
        if task is None:
            return 
        await self.session.delete(task)
        await self.session.commit()