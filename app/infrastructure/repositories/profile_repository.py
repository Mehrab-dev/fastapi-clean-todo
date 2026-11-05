
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from uuid import UUID

from app.infrastructure.database.models import ProfileModel
from app.domain.entities import entities
from app.infrastructure.database.mappers import ProfileMapper
from app.domain.repositories.repositories import ProfileRepository
from app.core.shared.exceptions import ConflictException



class SqlalchemyProfileRepository(ProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(
        self,
        *,
        user_id: UUID
    ) -> entities.Profile:
        model = ProfileMapper.to_model(entity=entities.Profile(user_id=user_id))
        self.session.add(model)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            error_msg = str(exc.orig).lower()
            if "unique" in error_msg and "user_id" in error_msg:
                raise ConflictException(
                    message="profile with this user_id already exists."
                ) from exc
            raise ConflictException(
                message="data integrity violation."
            ) from exc

        return ProfileMapper.to_domain(model=model)


    async def get_by_user_id(
        self,
        *,
        user_id: UUID
    ) -> entities.Profile | None:
        statement = select(ProfileModel).where(
            ProfileModel.user_id == user_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return ProfileMapper.to_domain(model=model)


    async def update(
        self,
        *,
        user_id: UUID,
        payload: entities.Profile
    ) -> entities.Profile | None:
        statement = select(ProfileModel).where(
            ProfileModel.user_id == user_id
        )
        result = await self.session.execute(statement=statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        
        """ update data """
        model.first_name = payload.first_name
        model.last_name = payload.last_name
        model.bio = payload.bio
        model.image = payload.image

        await self.session.flush()
        return ProfileMapper.to_domain(model=model)        