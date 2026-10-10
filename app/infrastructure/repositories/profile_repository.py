from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import ProfileRepository
from app.infrastructure.database.mappers import ProfileMapper
from app.infrastructure.database.models import ProfileModel
from app.domain.entities import entities
from app.shared.exceptions import ConflictError, ResourceNotFoundError



class SqlalchemyProfileRepository(ProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, *, user_id: UUID) -> None:
        statement = select(ProfileModel).where(
            ProfileModel.user_id == user_id
        )
        result = await self.session.execute(statement=statement)
        exists_model = result.scalar_one_or_none()
        if exists_model is not None:
            raise ConflictError(message="profile with this user id already exists.")
        model = ProfileModel(user_id=user_id)
        self.session.add(model)
        await self.session.commit()


    async def get_by_user_id(self, *, user_id: UUID) -> entities.Profile:
        statement = select(ProfileModel).where(
            ProfileModel.user_id == user_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            raise ResourceNotFoundError(message="profile was not found with this user_id")
        return ProfileMapper.to_domain(model=model)


    async def update_by_user_id(self, *, user_id: UUID, payload: entities.UpdateProfile) -> entities.Profile:
        statement = select(ProfileModel).where(
            ProfileModel.user_id == user_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            raise ResourceNotFoundError(message="profile was not found with this user_id")
        if payload.first_name is not None:
            model.first_name = payload.first_name
        if payload.last_name is not None:
            model.last_name = payload.last_name
        if payload.bio is not None:
            model.bio = payload.bio
        if payload.image is not None:
            model.image = payload.image
        await self.session.commit()
        await self.session.refresh(model)
        return ProfileMapper.to_domain(model=model)