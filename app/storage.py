from __future__ import annotations

from dataclasses import dataclass, field

from app.schemas import Task, TaskCreate, TaskStatusUpdate


@dataclass
class TaskStore:
    _tasks: list[Task] = field(default_factory=list)
    _next_id: int = 1

    def reset(self) -> None:
        self._tasks.clear()
        self._next_id = 1

    def create(self, task_in: TaskCreate, owner_id: int) -> Task:
        task = Task(id=self._next_id, owner_id=owner_id, **task_in.model_dump())
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_for_owner(self, owner_id: int) -> list[Task]:
        return [task for task in self._tasks if task.owner_id == owner_id]

    def list_all(self) -> list[Task]:
        return list(self._tasks)

    def get_for_owner(self, task_id: int, owner_id: int) -> Task | None:
        for task in self._tasks:
            if task.id == task_id and task.owner_id == owner_id:
                return task
        return None

    def get_any(self, task_id: int) -> Task | None:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_status(self, task: Task, update: TaskStatusUpdate) -> Task:
        task.status = update.status
        return task

    def delete_for_owner(self, task_id: int, owner_id: int) -> bool:
        for index, task in enumerate(self._tasks):
            if task.id == task_id and task.owner_id == owner_id:
                del self._tasks[index]
                return True
        return False

    def delete_any(self, task_id: int) -> bool:
        for index, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[index]
                return True
        return False

    def count_by_status(self) -> dict[str, int]:
        counts = {"todo": 0, "in_progress": 0, "done": 0}
        for task in self._tasks:
            counts[task.status] = counts.get(task.status, 0) + 1
        return counts


task_store = TaskStore()
