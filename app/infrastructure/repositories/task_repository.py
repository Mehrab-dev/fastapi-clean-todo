
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from uuid import UUID

from app.domain.entities import entities
from app.infrastructure.database.models import TaskModel
from app.infrastructure.database.mappers import TaskMapper
from app.domain.repositories.repositories import TaskRepository
from app.core.shared.exceptions import ConflictException



class SqlalchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(
        self,
        *,
        user_id: UUID,
        payload: entities.Task
    ) -> entities.Task:
        model = TaskMapper.to_model(entity=payload)
        model.user_id = user_id
        self.session.add(model)
        try:
            await self.session.flush()
        except IntegrityError as exc:

            error_msg = str(exc.orig).lower()
            if "user_id" in error_msg and "title" in error_msg:
                raise ConflictException(
                    message="task with this title for this user already exists."
                ) from exc
            raise ConflictException(
                message="data integrity violation."
            ) from exc

        return TaskMapper.to_domain(model=model)


    async def get_by_id(
        self,
        *,
        user_id: UUID,
        task_id: UUID
    ) -> entities.Task | None:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.id == task_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return TaskMapper.to_domain(model=model)


    async def search_by_title(
        self,
        *,
        user_id: UUID,
        query: str
    ) -> list[entities.Task]:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.title.ilike(f"%{query}%")
        )
        result = await self.session.execute(statement=statement)
        models = result.scalars().all()

        return [TaskMapper.to_domain(model=model) for model in models]


    async def list_tasks(
        self,
        *,
        user_id: UUID,
        offset: int = 0,
        limit: int = 5
    ) -> list[entities.Task]:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id
        ).offset(offset=offset).limit(limit=limit)
        result = await self.session.execute(statement=statement)
        models = result.scalars().all()

        return [TaskMapper.to_domain(model=model) for model in models]


    async def list_tasks_by_status(
        self,
        *,
        user_id: UUID,
        status: bool,
        offset: int = 0,
        limit: int = 5
    ) -> list[entities.Task]:

        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.is_complete == status
        ).offset(offset=offset).limit(limit=limit)
        result = await self.session.execute(statement=statement)
        models = result.scalars().all()

        return [TaskMapper.to_domain(model=model) for model in models]


    async def update(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        payload: entities.Task
    ) -> entities.Task | None:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.id == task_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        """ update data """
        model.title = payload.title
        model.description = payload.description
        model.is_complete = payload.is_complete

        try:
            await self.session.flush()
        except IntegrityError as exc:
            error_msg = str(exc.orig).lower()
            if "user_id" in error_msg and "title" in error_msg:
                raise ConflictException(
                    message="task with this title for this user already exists."
                ) from exc
            raise ConflictException(
                message="data integrity violation."
            ) from exc

        return TaskMapper.to_domain(model=model)


    async def delete(
        self,
        *,
        user_id: UUID,
        task_id: UUID
    ) -> bool:
        statement = select(TaskModel).where(
            TaskModel.user_id == user_id,
            TaskModel.id == task_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True