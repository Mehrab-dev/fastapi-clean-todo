
from fastapi import APIRouter, status, HTTPException, Depends


router = APIRouter(tags=["profiles"])



@router.get("/profile/me")
async def get_profile_info():
    pass


@router.patch("/update/profile/{profile_id}")
async def update():
    pass