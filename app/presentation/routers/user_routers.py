
from fastapi import APIRouter, status, HTTPException, Depends



router = APIRouter(tags=["auth"])



@router.post("/signup")
async def signup():
    pass


@router.post("/login")
async def login():
    pass


@router.get("/info")
async def get_info():
    pass


@router.patch("/update")
async def update():
    pass


@router.delete("/delete/{user_id}")
async def delete():
    pass


@router.post("/logout")
async def logout():
    pass


@router.post("/password/reset")
async def password_reset():
    pass