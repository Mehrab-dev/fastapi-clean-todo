from fastapi import APIRouter, status

from uuid import UUID


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/detail/{user_id}")
async def get_profile(*, user_id: UUID):
    pass


@router.put("/update")
async def update_profile(*, user_id: UUID):
    pass