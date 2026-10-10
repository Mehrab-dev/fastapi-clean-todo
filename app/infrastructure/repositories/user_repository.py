from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import UserRepository
from app.domain.entities import entities
from app.infrastructure.database.mappers import UserMapper
from app.shared.exceptions import ConflictError, AuthenticationError
from app.infrastructure.database.models import UserModel




class SqlalchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, *, payload: entities.User) -> None:
        model = UserMapper.to_model(entity=payload)
        self.session.add(model)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError(message="user with this email already exists.") from exc


    async def get_by_email(self, *, email: str) -> entities.User | None:
        statement = select(UserModel).where(
            UserModel.email == email
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        try:
            return UserMapper.to_domain(model=model)
        except IntegrityError:
            await self.session.rollback()
            raise


    async def update_email_by_id(self, *, id: UUID, new_email: str) -> None:
        statement = select(UserModel).where(
            UserModel.id == id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one()
        model.email = new_email
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError(message="user with this email already exists.") from exc



    async def update_password_by_id(self, *, id: UUID, password: str) -> None:
        statement = select(UserModel).where(
            UserModel.id == id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one()
        model.password = password
        await self.session.commit()


    async def delete_by_id(self, *, id: UUID) -> None:
        statement = select(UserModel).where(
            UserModel.id == id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one()
        await self.session.delete(model)
        await self.session.commit()