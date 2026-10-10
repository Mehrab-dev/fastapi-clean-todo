from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_session_database
from app.application.usecases.user_service import UserService
from app.infrastructure.repositories.user_repository import SqlalchemyUserRepository



def get_user_service(
    session: AsyncSession = Depends(get_session_database)
) -> UserService:
    repository = SqlalchemyUserRepository(session=session)
    return UserService(repository=repository)