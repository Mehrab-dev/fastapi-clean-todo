from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import UserRepository, ProfileRepository
from app.domain.entities.user_entity import User as user_entity
from app.infrastructure.database.models import UserModel
from app.core.security.password import hash_password, verify_password



class UserService:
    def __init__(self, repository: UserRepository, profile_repository: ProfileRepository):
        self.repository = repository
        self.profile_repository = profile_repository

    # GET /users/signup
    async def signup(
        self,
        *,
        payload: user_entity
    ):
        statement = await self.repository.get_user_by_email(email=payload.email)
        if statement is not None:
            raise ValueError("user with this email already exists!")
        payload.password = hash_password(payload.password)
        
        user_id = await self.repository.create_user(payload=payload)
        await self.profile_repository.create_profile_by_user_id(
            user_id=UUID(user_id)
        )


    # PATCH /users/update-email
    async def update_email(
        self,
        *,
        id: UUID,
        new_email: str
    ) -> str | None:
        statement = await self.repository.get_user_by_email(email=new_email)
        if statement is not None:
            raise ValueError("user with new email already exists!")
        
        return await self.repository.update_email_by_id(id=id, new_email=new_email)


    # PATCH /users/update-password
    async def update_password(
        self,
        *,
        id: UUID,
        new_password: str
    ) -> str | None:
        hashed_password = hash_password(new_password)
        return await self.repository.update_password_by_id(id=id, new_password=hashed_password)


    # DELETE /users/delete
    async def delete_user(
        self,
        *,
        id: UUID
    ) -> None:
        return await self.repository.delete_user_by_id(id=id)


    # GET /users/login
    async def login(self, *, email: str, password: str) -> str | None:
        user = await self.repository.get_user_by_email(email=email)
        if user is None:
            raise ValueError("invalid credentials")
        if not verify_password(password, user.password):
            raise ValueError("invalid credentials")
        return 
        