from fastapi import APIRouter, HTTPException, status, Depends

from uuid import UUID

from app.application.usecases.user_service import UserService
from app.presentation.schemas.user_schemas import (UserCreateSchema, UserLoginSchema,
                                                   UserUpdateEmailSchema, UserUpdatePasswordSchema, UserResponseSchema)
from app.presentation.dependencies import get_user_service
from app.domain.entities import entities
from app.shared.exceptions import AuthenticationError, ConflictError


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    *,
    payload: UserCreateSchema,
    service: UserService = Depends(get_user_service)
):
    try:
        user = entities.User(
            email=payload.email,
            password=payload.password,
            is_active=True
        )
        await service.signup(payload=user)
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail={"message" : "user created successfully."}
        )
    except ConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= str(exc.message)
        ) from exc



@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def login(
    *,
    email: str,
    password: str,
    service: UserService = Depends(get_user_service)
) -> entities.User:
    try:
        return await service.login(email=email, password=password)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= str(exc.message)
        ) from exc



@router.patch("/update-email", status_code=status.HTTP_200_OK)
async def update_email(
    *,
    id: UUID,
    payload: UserUpdateEmailSchema,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.update_email(id=id, email=payload.new_email)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message" : "email updated successfully"}
        )
    except ConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= str(exc.message)
        ) from exc



@router.patch("/update-password", status_code=status.HTTP_200_OK)
async def update_password(
    *,
    id: UUID,
    payload: UserUpdatePasswordSchema,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.update_password(id=id, password=payload.new_password)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message" : "password updated successfully."}
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"message" : "password could not be updated"}
        )



@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    *,
    id: UUID,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.delete_user(id=id)
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail={"message" : "user deleted successfully."}
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= {"message" : "user deletion failed"}
        )