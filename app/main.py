from fastapi import FastAPI

from app.presentation.routers.user_routers import router as user_router
from app.presentation.routers.profile_routers import router as profile_router
from app.presentation.routers.task_routers import router as task_router



app = FastAPI()

app.include_router(user_router)
app.include_router(profile_router)
app.include_router(task_router)