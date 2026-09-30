from sqlalchemy import select

from uuid import UUID

from app.domain.repositories.repositories import UserRepository
from app.domain.entities.user_entity import User as user_entity
from app.infrastructure.database.models import UserModel
from app.core.security.password import hash_password, verify_password



class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # GET /users/signup
    async def signup(
        self,
        *,
        payload: user_entity
    ) -> str:
        statement = await self.repository.get_user_by_email(email=payload.email)
        if statement is not None:
            raise ValueError("user with this email already exists!")
        payload.password = hash_password(payload.password)
        
        return await self.repository.create_user(payload=payload)


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
        return await self.repository.update_password_by_id(id=id, new_password=new_password)


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
        return "logged successfully."
        