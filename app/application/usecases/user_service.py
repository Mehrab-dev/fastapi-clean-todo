
from uuid import UUID

from app.domain.repositories.repositories import UserRepository
from app.application.dtos.dtos import CreateUserDTO, UpdateUserDTO
from app.domain.entities import entities
from app.core.shared.exceptions import ConflictException, NotFoundException, AuthenticationException
from app.application.interface.uow import UnitOfWork



class UserService:
    def __init__(self, repository: UserRepository, uow: UnitOfWork):
        self.repository = repository
        self.uow = uow


    async def signup(
        self,
        *,
        payload: CreateUserDTO
    ) -> entities.User:
        async with self.uow:
            entity_payload = entities.User(
                email=payload.email,
                password=payload.password
            )
            exists = await self.repository.get_by_email(email=payload.email)
            if exists:
                raise ConflictException(
                    message="user with this email already exists."
                )

            """ signup """
            user = await self.repository.create(payload=entity_payload)
            await self.uow.commit()

            return user


    async def get_info(
        self,
        *,
        user_id: UUID
    ) -> entities.User:
        async with self.uow:
            user = await self.repository.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundException(
                    message="user with this id not found."
                )

            return user


    async def login(
        self,
        *,
        email: str
    ) -> entities.User:
        async with self.uow:
            user = await self.repository.get_by_email(email=email)
            if not user:
                raise AuthenticationException(
                    message="incorrect email or password."
                )

            return user


    async def update(
        self,
        *,
        user_id: UUID,
        payload: UpdateUserDTO
    ) -> entities.User:
        async with self.uow:
            user = await self.repository.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundException(
                    message="user with this id not found."
                )

            """ update data """
            if "email" in payload.model_fields_set and payload.email is not None:
                exists = await self.repository.get_by_email(email=payload.email)
                if exists and exists.id != user_id:
                    raise ConflictException(
                        message="user with this email already exists."
                    )
                user.update_email(email=payload.email)
            if "password" in payload.model_fields_set and payload.password is not None:
                user.update_password(password=payload.password)

            await self.repository.update(user_id=user_id, payload=user)
            await self.uow.commit()

            return user


    async def delete(
        self,
        *,
        user_id: UUID
    ) -> bool:
        async with self.uow:
            user = await self.repository.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundException(
                    message="user with this id not found."
                )
            await self.repository.delete(user_id=user_id)
            await self.uow.commit()

            return True