from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_storage, require_admin

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/stats")
def get_stats(storage=Depends(get_storage)) -> dict[str, object]:
    tasks = storage.list_all()
    return {"total_tasks": len(tasks), "by_status": storage.count_by_status()}


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_task(task_id: int, storage=Depends(get_storage)) -> Response:
    deleted = storage.delete_any(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
