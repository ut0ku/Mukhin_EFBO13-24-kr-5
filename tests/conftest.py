import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.room_manager import room_manager
from app.storage import task_store


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_task_store() -> None:
    task_store.reset()
    room_manager.reset()

