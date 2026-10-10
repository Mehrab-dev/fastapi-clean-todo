
from uuid import UUID

from app.domain.repositories.repositories import ProfileRepository
from app.shared.exceptions import ConflictError, ResourceNotFoundError
from app.domain.entities import entities



class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository


    async def create_profile(
        self,
        *,
        user_id: UUID
    ) -> None:
        exists_profile = await self.repository.get_by_user_id(user_id=user_id)
        if exists_profile:
            raise ConflictError(
                message="profile with this user_id already exists."
            )
        await self.repository.create(user_id=user_id)


    async def get_profile(
        self,
        *,
        user_id: UUID
    ) -> entities.Profile:
        profile = await self.repository.get_by_user_id(user_id=user_id)
        if not profile:
            raise ResourceNotFoundError(
                message="profile with this user_id nof found."
            )
        return profile


    async def update_profile(
        self,
        *,
        user_id: UUID,
        payload: entities.UpdateProfile
    ) -> entities.Profile:
        profile = await self.repository.get_by_user_id(user_id=user_id)    
        if profile:
            raise ResourceNotFoundError(
                message="profile with this user_id not found."
            )
        return await self.repository.update_by_user_id(user_id=user_id, payload=payload)