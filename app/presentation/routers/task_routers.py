
from fastapi import APIRouter, status, HTTPException, Depends


router = APIRouter(tags=["tasks"])



@router.post("/create-task")
async def create():
    pass


@router.get("/task/{task_id}")
async def get_detail():
    pass


@router.get("/search")
async def search():
    pass


@router.get("/list")
async def list_tasks():
    pass


@router.get("/list/by-status/{status}")
async def list_by_status():
    pass


@router.patch("/update/task/{task_id}")
async def update():
    pass


@router.delete("/delete/task/{task_id}")
async def delete():
    pass