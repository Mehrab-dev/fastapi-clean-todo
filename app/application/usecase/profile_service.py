
from uuid import UUID

from app.domain.repositories.repositories import ProfileRepository
from app.domain.entities.profile_entity import Profile as profile_entity, UpdateProfile




class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository


    # GET /profiles/detail/{user_id}
    async def get_profile(
        self,
        *,
        user_id: UUID
    ) -> profile_entity | None:
        result = await self.repository.get_profile_by_user_id(user_id=user_id)
        if result is None:
            raise ValueError("no profile has been created for this user!")
        return result


    # PUT /profiles/update
    async def update_profile(
        self,
        *,
        user_id: UUID,
        payload: UpdateProfile,
        image: str | None = None
    ) -> profile_entity | None:
        result = await self.repository.update_profile(user_id=user_id, payload=payload, image=image)
        if result is None:
            raise ValueError("no profile has been created for this user!")
        return result
    