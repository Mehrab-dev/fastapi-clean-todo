from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import ProfileRepository
from app.infrastructure.database.mappers import ProfileMapper
from app.domain.entities.profile_entity import Profile as profile_entity, UpdateProfile
from app.infrastructure.database.models import ProfileModel



class Sqlalchemy_ProfileRepository(ProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_profile_by_user_id(self, *, user_id: UUID) -> None:
        payload = ProfileModel(user_id=user_id)
        self.session.add(payload)
        
        await self.session.commit()
        await self.session.refresh(payload)



    async def get_profile_by_user_id(self, *, user_id: UUID) -> profile_entity | None:
        result = await self.session.execute(
            select(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return ProfileMapper.to_domain(model=model)



    async def update_profile(self, *, user_id: UUID, payload: UpdateProfile) -> profile_entity | None:
        result = await self.session.execute(
            select(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        
        # change data
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