from fastapi.testclient import TestClient


def create_task(client: TestClient, owner_id: str, title: str, status: str = "todo", priority: int = 3) -> dict:
    response = client.post(
        "/tasks",
        headers={"X-User-Id": owner_id, "X-User-Role": "user"},
        json={"title": title, "description": None, "status": status, "priority": priority},
    )
    assert response.status_code == 201
    return response.json()


def test_users_me_returns_current_user(client: TestClient) -> None:
    response = client.get(
        "/users/me",
        headers={"X-User-Id": "10", "X-User-Role": "user"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": 10, "role": "user"}


def test_missing_user_id_returns_401(client: TestClient) -> None:
    response = client.get("/users/me")

    assert response.status_code == 401


def test_regular_user_gets_403_on_admin_stats(client: TestClient) -> None:
    response = client.get(
        "/admin/stats",
        headers={"X-User-Id": "10", "X-User-Role": "user"},
    )

    assert response.status_code == 403


def test_admin_gets_statistics_for_all_tasks(client: TestClient) -> None:
    create_task(client, "10", "Task 1", status="todo")
    create_task(client, "10", "Task 2", status="todo")
    create_task(client, "11", "Task 3", status="in_progress")
    create_task(client, "11", "Task 4", status="done")
    create_task(client, "12", "Task 5", status="done")

    response = client.get(
        "/admin/stats",
        headers={"X-User-Id": "1", "X-User-Role": "admin"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "total_tasks": 5,
        "by_status": {"todo": 2, "in_progress": 1, "done": 2},
    }


def test_regular_user_cannot_delete_foreign_task_via_tasks_route(client: TestClient) -> None:
    task = create_task(client, "10", "Task 1")

    response = client.delete(
        f"/tasks/{task['id']}",
        headers={"X-User-Id": "11", "X-User-Role": "user"},
    )

    assert response.status_code == 404


def test_admin_can_delete_foreign_task_via_admin_route(client: TestClient) -> None:
    task = create_task(client, "10", "Task 1")

    response = client.delete(
        f"/admin/tasks/{task['id']}",
        headers={"X-User-Id": "1", "X-User-Role": "admin"},
    )

    assert response.status_code == 204
    verify = client.get(
        "/admin/stats",
        headers={"X-User-Id": "1", "X-User-Role": "admin"},
    )
    assert verify.json()["total_tasks"] == 0


def test_swagger_routes_grouped_by_tags(client: TestClient) -> None:
    openapi = client.get("/openapi.json").json()

    assert openapi["paths"]["/tasks"]["post"]["tags"] == ["tasks"]
    assert openapi["paths"]["/users/me"]["get"]["tags"] == ["users"]
    assert openapi["paths"]["/admin/stats"]["get"]["tags"] == ["admin"]
