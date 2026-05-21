from typing import Literal

from pydantic import BaseModel, Field


TaskStatus = Literal["todo", "in_progress", "done"]


class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    description: str | None = None
    status: TaskStatus
    priority: int = Field(ge=1, le=5)


class TaskCreate(TaskBase):
    pass


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class Task(TaskBase):
    id: int
    owner_id: int

