
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from uuid import UUID

from app.infrastructure.database.models import UserModel
from app.domain.repositories.repositories import UserRepository
from app.infrastructure.database.mappers import UserMapper
from app.domain.entities import entities
from app.core.shared.exceptions import (ConflictException)



class SqlalchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(
        self,
        *,
        payload: entities.User
    ) -> entities.User:
        model = UserMapper.to_model(entity=payload)
        self.session.add(model)
        try:
            await self.session.flush()

        except IntegrityError as exc:
            error_msg = str(exc.orig).lower()
            if "unique" in error_msg and "email" in error_msg:
                raise ConflictException(
                    message="user with this email already exists."
                ) from exc
            raise ConflictException(
                message="data integrity violation."
            ) from exc

        return UserMapper.to_domain(model=model)


    async def get_by_id(
        self,
        *,
        user_id: UUID
    ) -> entities.User | None:
        statement = select(UserModel).where(
            UserModel.id == user_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return UserMapper.to_domain(model=model)


    async def get_by_email(
        self,
        *,
        email: str
    ) -> entities.User | None:
        statement = select(UserModel).where(
            UserModel.email == email
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return UserMapper.to_domain(model=model)


    async def update(
        self,
        *,
        user_id: UUID,
        payload: entities.User
    ) -> entities.User | None:
        statement = select(UserModel).where(
            UserModel.id == user_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        """ update data """
        model.email = payload.email
        model.password = payload.password
        model.is_active = payload.is_active

        try:
            await self.session.flush()
        except IntegrityError as exc:
            error_msg = str(exc.orig).lower()
            if "unique" in error_msg and "email" in error_msg:
                raise ConflictException(
                    message="user with this email already exists."
                )
            raise ConflictException(
                message="data integrity violation."
            ) from exc

        return UserMapper.to_domain(model=model)


    async def delete(
        self,
        *,
        user_id: UUID
    ) -> bool:
        statement  = select(UserModel).where(
            UserModel.id == user_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return False

        """ delete data """
        await self.session.delete(model)
        await self.session.flush()
        return True