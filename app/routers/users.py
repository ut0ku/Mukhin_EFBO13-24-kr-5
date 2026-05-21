from fastapi import APIRouter, Depends

from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(current_user: dict[str, object] = Depends(get_current_user)) -> dict[str, object]:
    return current_user


@router.get("/{user_id}")
def get_user(user_id: int, current_user: dict[str, object] = Depends(get_current_user)) -> dict[str, object]:
    return {"id": user_id, "role": current_user["role"]}
