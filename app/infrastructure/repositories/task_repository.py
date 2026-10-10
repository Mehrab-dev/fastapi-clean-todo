from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import TaskRepository
from app.domain.entities import entities
from app.infrastructure.database.mappers import TaskMapper
from app.infrastructure.database.models import TaskModel
from app.shared.exceptions import ResourceNotFoundError



class SqlalchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, *, user_id: UUID, payload: entities.Task) -> entities.Task:
        model = TaskMapper.to_model(entity=payload)
        model.user_id = user_id
        self.session.add(model)
        try:  
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(model)
        return TaskMapper.to_domain(model=model)


    async def search_by_title(self, *, user_id: UUID, title: str) -> list[entities.Task]:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.title.ilike(f"%{title}%")
        )
        result = await self.session.execute(statement=statement)
        models = result.scalars().all()
        return [TaskMapper.to_domain(model=model) for model in models]


    async def list_tasks(self, *, user_id: UUID, offset: int = 0, limit: int = 5) -> list[entities.Task]:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id
        ).order_by(TaskModel.created_at).offset(offset=offset).limit(limit=limit)
        result = await self.session.execute(statement=statement)
        models = result.scalars().all()
        return [TaskMapper.to_domain(model) for model in models]


    async def list_by_status(self, *, user_id: UUID, status: bool) -> list[entities.Task]:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.status == status
        ).order_by(TaskModel.created_at)
        result = await self.session.execute(statement=statement)
        models = result.scalars().all()
        return [TaskMapper.to_domain(model) for model in models]


    async def update_by_task_id(self, *, user_id: UUID, task_id: UUID, payload: entities.UpdateTask) -> entities.Task:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.id == task_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            raise ResourceNotFoundError(message="task with this id not found.")
        if payload.title is not None:
            model.title = payload.title
        if payload.description is not None:
            model.description = payload.description
        if payload.status is not None:
            model.status = payload.status
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(model)
        return TaskMapper.to_domain(model=model)


    async def delete_by_task_id(self, *, user_id: UUID, task_id: UUID) -> None:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.id == task_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            raise ResourceNotFoundError(message="task with this id not found.")
        try:
            await self.session.delete(model)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise