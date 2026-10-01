from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Form

from uuid import UUID

from app.application.usecase.profile_service import ProfileService
from app.presentation.dependencies import get_profile_service
from app.presentation.schemas.profile_schema import ProfileUpdateSchema, ProfileResponseSchema
from app.domain.entities.profile_entity import UpdateProfile
from app.infrastructure.storage.image_storage import save_profile_image


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/detail/{user_id}", response_model=ProfileResponseSchema)
async def get_profile(
    *, 
    user_id: UUID,
    service: ProfileService = Depends(get_profile_service)
):
    try:
        return await service.get_profile(user_id=user_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )
    


@router.put("/update", response_model=ProfileResponseSchema)
async def update_profile(
    *, 
    user_id: UUID,
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    bio: str | None = Form(None),
    image: UploadFile | None = File(None),
    service: ProfileService = Depends(get_profile_service)
):
    payload = ProfileUpdateSchema(
        first_name=first_name,
        last_name=last_name,
        bio=bio
    )
    domain_profile = UpdateProfile(
        first_name=payload.first_name,
        last_name=payload.last_name,
        bio=payload.bio
    )
    
    image_path = None
    if image is not None:
        image_path = await save_profile_image(image)
    try:
        return await service.update_profile(user_id=user_id, payload=domain_profile, image=image_path)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )