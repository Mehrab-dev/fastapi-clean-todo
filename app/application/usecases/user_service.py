
from uuid import UUID

from app.domain.repositories.repositories import UserRepository
from app.domain.entities import entities
from app.core.security.password import hash_password, verify_password
from app.shared.exceptions import ConflictError, AuthenticationError




class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def signup(
        self,
        *,
        payload: entities.User
    ) -> None:
        result = await self.repository.get_by_email(email=payload.email)
        if result:
            raise ConflictError(
                message="user with this email already exists."
            )
        hashed_password = hash_password(password=payload.password)
        user = entities.User(
            email=payload.email,
            password=hashed_password,
            is_active=True
        )
        await self.repository.create(payload=user)


    async def login(
        self, 
        *, 
        email: str, 
        password: str
    ) -> entities.User:
        user = await self.repository.get_by_email(email=email)
        if not user:
            raise AuthenticationError(
                message="invalid email or password"
            )

        if not verify_password(password=password, hashed_password=user.password):
            raise AuthenticationError(
                message="invalid email or password"
            )

        return user


    async def update_email(
        self,
        *,
        id: UUID,
        email: str
    ) -> None:
        exists_email = await self.repository.get_by_email(email=email)
        if exists_email:
            raise ConflictError(
                message="email already exists."
            )
        await self.repository.update_email_by_id(id=id, new_email=email)


    async def update_password(
        self,
        *,
        id: UUID,
        password: str
    ) -> None:
        hashed_password = hash_password(password=password)
        await self.repository.update_password_by_id(id=id, password=hashed_password)


    async def delete_user(
        self,
        *,
        id: UUID
    ) -> None:
        await self.repository.delete_by_id(id=id)