from fastapi import APIRouter, status

from uuid import UUID


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/create")
async def create_task(*, user_id: UUID):
    pass


@router.get("/detail/{title}")
async def get_task_by_title(*, user_id: UUID, title: str):
    pass


@router.get("/list")
async def list_tasks(*, user_id: UUID):
    pass


@router.get("/list-by-status")
async def list_tasks_by_status(*, user_id: UUID, status: bool):
    pass


@router.put("/update")
async def update_task(*, user_id: UUID, task_id: UUID):
    pass


@router.delete("/delete")
async def delete_task(*, user_id: UUID, task_id: UUID):
    pass