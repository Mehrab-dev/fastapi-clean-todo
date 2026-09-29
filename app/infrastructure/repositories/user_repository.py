from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import UserRepository
from app.domain.entities.user_entity import User as user_entity
from app.infrastructure.database.mappers import UserMapper
from app.infrastructure.database.models import UserModel



class SqlalchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, *, payload: user_entity) -> str:
        model = UserMapper.to_model(entity=payload)

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return str(model.id)


    async def update_email_by_id(self, *, id: UUID, new_email: str) -> str | None:
        model = await self.session.get(UserModel, id)
        if model is None:
            return None

        model.email = new_email
        await self.session.commit()
        await self.session.refresh(model)

        return str(model.id)


    async def update_password_by_id(self, *, id: UUID, new_password: str) -> str | None:
        model = await self.session.get(UserModel, id)
        if model is None:
            return None
        model.password = new_password
        await self.session.commit()
        await self.session.refresh(model)
        return str(model.id)


    async def delete_user_by_id(self, *, id: UUID) -> None:
        model = await self.session.get(UserModel, id)
        if model is None:
            return None
        await self.session.delete(model)
        await self.session.commit()


    async def get_user_by_email(self, *, email: str) -> user_entity | None:
        model = await self.session.get(UserModel, email)
        if model is None:
            return None
        return UserMapper.to_domain(model=model)