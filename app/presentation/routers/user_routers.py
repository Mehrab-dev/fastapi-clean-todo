from fastapi import APIRouter, status

from uuid import UUID


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup():
    pass


@router.patch("/update-email", status_code=status.HTTP_200_OK)
async def update_email(*, id: UUID, new_email: str):
    pass


@router.patch("/update-password")
async def update_password(*, id: UUID, new_password: str):
    pass


@router.delete("/delete")
async def delete_user(*, id: UUID):
    pass


@router.post("/login")
async def login(*, email: str, password: str):
    pass