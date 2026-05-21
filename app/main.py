import os

from fastapi import FastAPI

from app.routers.admin import router as admin_router
from app.routers.rooms import router as rooms_router
from app.routers.users import router as users_router
from app.routers.tasks import router as tasks_router

app = FastAPI(title="Task Manager API")

app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(rooms_router)


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok", "env": os.getenv("APP_ENV", "local")}

