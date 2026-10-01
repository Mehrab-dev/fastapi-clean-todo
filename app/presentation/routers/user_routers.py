from fastapi import APIRouter, status, Depends, HTTPException

from uuid import UUID

from app.presentation.schemas.user_schema import (UserSignUpSchema, UserUpdateEmailSchema,
                                                  UserUpdatePasswordSchema, UserLoginSchema)
from app.application.usecase.user_service import UserService
from app.domain.entities.user_entity import User as user_entity
from app.presentation.dependencies import (get_user_service)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    *,
    payload: UserSignUpSchema,
    service: UserService = Depends(get_user_service)
):
    user = user_entity(
        email=payload.email,
        password=payload.password,
        is_active=True
    )
    try:
        await service.signup(payload=user)
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="signup successfully."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= str(e)
        )



@router.patch("/update-email", status_code=status.HTTP_200_OK)
async def update_email(
    *, 
    id: UUID, 
    new_email: UserUpdateEmailSchema,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.update_email(id=id, new_email=new_email.new_email)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="email updated successfully."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= str(e)
        )



@router.patch("/update-password")
async def update_password(
    *, 
    id: UUID, 
    new_password: UserUpdatePasswordSchema,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.update_password(id=id, new_password=new_password.new_password)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="password updated succesfully."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= str(e)
        )



@router.delete("/delete")
async def delete_user(
    *, 
    id: UUID,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.delete_user(id=id)
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="password deleted successfully."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= str(e)
        )



@router.post("/login")
async def login(
    *, 
    payload: UserLoginSchema,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.login(email=payload.email, password=payload.password)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="logged successfully."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )