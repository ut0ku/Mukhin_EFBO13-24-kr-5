from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.dependencies import get_current_user, get_storage
from app.schemas import Task, TaskCreate, TaskStatusUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    current_user: dict[str, object] = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Task:
    return storage.create(task_in, int(current_user["id"]))


@router.get("", response_model=list[Task])
def list_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    min_priority: int | None = Query(default=None, ge=1, le=5),
    current_user: dict[str, object] = Depends(get_current_user),
    storage=Depends(get_storage),
) -> list[Task]:
    tasks = storage.list_for_owner(int(current_user["id"]))
    if status_filter is not None:
        tasks = [task for task in tasks if task.status == status_filter]
    if min_priority is not None:
        tasks = [task for task in tasks if task.priority >= min_priority]
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    current_user: dict[str, object] = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Task:
    task = storage.get_for_owner(task_id, int(current_user["id"]))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: int,
    task_update: TaskStatusUpdate,
    current_user: dict[str, object] = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Task:
    task = storage.get_for_owner(task_id, int(current_user["id"]))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return storage.update_status(task, task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: dict[str, object] = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Response:
    deleted = storage.delete_for_owner(task_id, int(current_user["id"]))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
