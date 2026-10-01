from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usecase.user_service import UserService
from app.application.usecase.profile_service import ProfileService
from app.application.usecase.task_service import TaskService
from app.infrastructure.database.session import get_database_session
from app.infrastructure.repositories.user_repository import SqlalchemyUserRepository
from app.infrastructure.repositories.profile_repository import SqlalchemyProfileRepository
from app.infrastructure.repositories.task_repository import SqlalchemyTaskRepository



def get_user_service(session: AsyncSession = Depends(get_database_session)) -> UserService:
    repository = SqlalchemyUserRepository(session=session)
    profile_repository = SqlalchemyProfileRepository(session=session)
    return UserService(repository=repository, profile_repository=profile_repository)


def get_profile_service(session: AsyncSession = Depends(get_database_session)) -> ProfileService:
    repository = SqlalchemyProfileRepository(session=session)
    return ProfileService(repository=repository)


def get_task_service(session: AsyncSession = Depends(get_database_session)) -> TaskService:
    repository = SqlalchemyTaskRepository(session=session)
    return TaskService(repository=repository)