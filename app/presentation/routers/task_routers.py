from fastapi import APIRouter, status, Depends, HTTPException

from uuid import UUID

from app.application.usecase.task_service import TaskService
from app.presentation.dependencies import get_task_service
from app.presentation.schemas.task_schema import (TaskCreateSchema, TaskUpdateSchema, 
                                                  TaskResponseSchema)
from app.domain.entities.task_entity import Task as task_entity, UpdateTask


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(
    *, 
    user_id: UUID,
    payload: TaskCreateSchema,
    service: TaskService = Depends(get_task_service)
):
    task = task_entity(
        title=payload.title,
        description=payload.description,
        status_task=payload.status_task
    )
    try:
        await service.create_task(user_id=user_id, payload=task)
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="task created successfully."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= str(e)
        )
    


@router.get("/detail/{title}", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
async def get_task_by_title(
    *, 
    user_id: UUID, 
    title: str,
    service: TaskService = Depends(get_task_service)
):
    try:
        return await service.get_task_by_title(user_id=user_id, title=title)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )



@router.get("/list")
async def list_tasks(
    *, 
    user_id: UUID,
    service: TaskService = Depends(get_task_service)
):
    try:
        return await service.list_tasks(user_id=user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail= str(e)
        )
    


@router.get("/list-by-status", response_model=list[TaskResponseSchema], status_code=status.HTTP_200_OK)
async def list_tasks_by_status(
    *, 
    user_id: UUID, 
    status_task: bool,
    service: TaskService = Depends(get_task_service)
):
    try:
        return await service.list_tasks_by_status(user_id=user_id, status_task=status_task)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )
        


@router.put("/update/{task_id}")
async def update_task(
    *, 
    user_id: UUID, 
    task_id: UUID,
    payload: TaskUpdateSchema,
    service: TaskService = Depends(get_task_service)
):
    payload_domain = UpdateTask(
        title=payload.title,
        description=payload.description,
        status_task=payload.status_task
    )
    try:
        return await service.update_task(user_id=user_id, task_id=task_id, payload=payload_domain)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )
    


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    *, 
    user_id: UUID, 
    task_id: UUID,
    service: TaskService = Depends(get_task_service)
):
    try:
        await service.delete_task(user_id=user_id, task_id=task_id)
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="task deleted successfully."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )