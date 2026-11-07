
from uuid import UUID

from app.application.dtos.dtos import UpdateProfileDTO
from app.application.interface.uow import UnitOfWork
from app.domain.repositories.repositories import ProfileRepository, UserRepository
from app.domain.entities import entities
from app.core.shared.exceptions import ConflictException, NotFoundException



class ProfileService:
    def __init__(self, uow: UnitOfWork, repository: ProfileRepository, user_repository: UserRepository):
        self.uow = uow
        self.repository = repository
        self.user_repository = user_repository


    async def create(
        self,
        *,
        user_id: UUID
    ) -> entities.Profile:
        async with self.uow:
            user = await self.user_repository.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundException(
                    message="user with this id not found."
                )
            exists = await self.repository.get_by_user_id(user_id=user_id)
            if exists:
                raise ConflictException(
                    message="profile already exists for this user."
                )
            profile = await self.repository.create(user_id=user_id)
            await self.uow.commit()

            return profile


    async def get_info(
        self,
        *,
        user_id: UUID
    ) -> entities.Profile:
        profile = await self.repository.get_by_user_id(user_id=user_id)
        if not profile:
            raise NotFoundException(
                message="profile with this user id not found."
            )
        
        return profile


    async def update(
        self,
        *,
        user_id: UUID,
        payload: UpdateProfileDTO
    ) -> entities.Profile:
        async with self.uow:
            profile = await self.repository.get_by_user_id(user_id=user_id)
            if not profile:
                raise NotFoundException(
                    message="profile with this user id not found."
                )

            """ update data """
            if "first_name" in payload.model_fields_set:
                profile.update_firstname(first_name=payload.first_name)
            if "last_name" in payload.model_fields_set:
                profile.update_lastname(last_name=payload.last_name)
            if "bio" in payload.model_fields_set:
                profile.update_bio(bio=payload.bio)
            if "image" in payload.model_fields_set:
                profile.update_image(image=payload.image)

            await self.repository.update(user_id=user_id, payload=profile)
            await self.uow.commit()
            return profile
            