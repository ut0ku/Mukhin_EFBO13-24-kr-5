from fastapi.testclient import TestClient


def test_create_task_success(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={
            "title": "Подготовить тесты",
            "description": "Написать интеграционные тесты для основных сценариев",
            "status": "todo",
            "priority": 4,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Подготовить тесты",
        "description": "Написать интеграционные тесты для основных сценариев",
        "status": "todo",
        "priority": 4,
        "owner_id": 10,
    }


def test_create_task_validation_error_for_short_title(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={
            "title": "Aa",
            "description": "Too short title",
            "status": "todo",
            "priority": 3,
        },
    )

    assert response.status_code == 422


def test_missing_or_invalid_user_header_returns_401(client: TestClient) -> None:
    # missing header
    assert client.get("/tasks").status_code == 401
    assert client.post("/tasks", json={"title": "x", "description": None, "status": "todo", "priority": 1}).status_code == 401
    assert client.get("/tasks/1").status_code == 401
    assert client.patch("/tasks/1/status", json={"status": "done"}).status_code == 401
    assert client.delete("/tasks/1").status_code == 401

    # present but not convertible to int
    bad = {"X-User-Id": "abc"}
    assert client.get("/tasks", headers=bad).status_code == 401
    assert client.post("/tasks", headers=bad, json={"title": "x", "description": None, "status": "todo", "priority": 1}).status_code == 401
    assert client.get("/tasks/1", headers=bad).status_code == 401
    assert client.patch("/tasks/1/status", headers=bad, json={"status": "done"}).status_code == 401
    assert client.delete("/tasks/1", headers=bad).status_code == 401


def test_user_sees_only_own_tasks(client: TestClient) -> None:
    first = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task A", "description": None, "status": "todo", "priority": 2},
    )
    second = client.post(
        "/tasks",
        headers={"X-User-Id": "11"},
        json={"title": "Task B", "description": None, "status": "todo", "priority": 3},
    )

    assert first.status_code == 201
    assert second.status_code == 201

    response = client.get("/tasks", headers={"X-User-Id": "10"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Task A",
            "description": None,
            "status": "todo",
            "priority": 2,
            "owner_id": 10,
        }
    ]


def test_task_filters_by_status_and_min_priority(client: TestClient) -> None:
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task A", "description": None, "status": "todo", "priority": 2},
    )
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task B", "description": None, "status": "done", "priority": 4},
    )
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task C", "description": None, "status": "done", "priority": 5},
    )

    response = client.get(
        "/tasks",
        headers={"X-User-Id": "10"},
        params={"status": "done", "min_priority": 5},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 3,
            "title": "Task C",
            "description": None,
            "status": "done",
            "priority": 5,
            "owner_id": 10,
        }
    ]


def test_update_task_status_success(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task A", "description": None, "status": "todo", "priority": 2},
    )

    response = client.patch(
        f"/tasks/{created.json()['id']}/status",
        headers={"X-User-Id": "10"},
        json={"status": "done"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_foreign_or_missing_task_returns_404(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task A", "description": None, "status": "todo", "priority": 2},
    )
    tid = created.json()["id"]

    assert client.get(f"/tasks/{tid}", headers={"X-User-Id": "11"}).status_code == 404
    assert client.patch(f"/tasks/{tid}/status", headers={"X-User-Id": "11"}, json={"status": "done"}).status_code == 404
    assert client.delete(f"/tasks/{tid}", headers={"X-User-Id": "11"}).status_code == 404

    assert client.get("/tasks/999", headers={"X-User-Id": "10"}).status_code == 404
    assert client.patch("/tasks/999/status", headers={"X-User-Id": "10"}, json={"status": "done"}).status_code == 404
    assert client.delete("/tasks/999", headers={"X-User-Id": "10"}).status_code == 404


def test_delete_task_success(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task A", "description": None, "status": "todo", "priority": 2},
    )

    response = client.delete(f"/tasks/{created.json()['id']}", headers={"X-User-Id": "10"})

    assert response.status_code == 204
    assert response.content == b""


def test_health_route_returns_status_and_env(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "docker")

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "env": "docker"}
