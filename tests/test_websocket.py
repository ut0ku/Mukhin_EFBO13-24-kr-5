import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect


def test_connect_to_room_with_valid_username(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        event = websocket.receive_json()

    assert event == {"type": "connected", "room_id": "python", "username": "alice"}


def test_send_message_and_receive_response_via_websocket(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()
        websocket.send_json({"type": "message", "text": "Всем привет"})
        event = websocket.receive_json()

    assert event == {
        "type": "message",
        "room_id": "python",
        "username": "alice",
        "text": "Всем привет",
    }


def test_two_clients_in_same_room_receive_same_message(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as alice_ws:
        alice_ws.receive_json()
        with client.websocket_connect("/ws/rooms/python?username=bob") as bob_ws:
            bob_ws.receive_json()
            alice_ws.receive_json()

            alice_ws.send_json({"type": "message", "text": "Hello room"})
            alice_event = alice_ws.receive_json()
            bob_event = bob_ws.receive_json()

    expected = {
        "type": "message",
        "room_id": "python",
        "username": "alice",
        "text": "Hello room",
    }
    assert alice_event == expected
    assert bob_event == expected


def test_users_from_different_rooms_do_not_receive_foreign_messages(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as python_ws:
        python_ws.receive_json()
        with client.websocket_connect("/ws/rooms/javascript?username=bob") as js_ws:
            js_ws.receive_json()

            python_ws.send_json({"type": "message", "text": "Hello Python"})
            python_event = python_ws.receive_json()

            js_ws.send_json({"type": "message", "text": "Hello JS"})
            js_event = js_ws.receive_json()

    assert python_event == {
        "type": "message",
        "room_id": "python",
        "username": "alice",
        "text": "Hello Python",
    }
    assert js_event == {
        "type": "message",
        "room_id": "javascript",
        "username": "bob",
        "text": "Hello JS",
    }


def test_too_long_message_returns_error(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()
        websocket.send_json({"type": "message", "text": "x" * 301})
        event = websocket.receive_json()

    assert event == {"type": "error", "detail": "Message is too long"}


def test_user_removed_from_room_after_disconnect(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()

    response = client.get("/rooms/python/users")

    assert response.status_code == 200
    assert response.json() == {"room_id": "python", "users": []}


def test_blank_username_closes_with_1008(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=   ") as websocket:
        with pytest.raises(WebSocketDisconnect) as exc_info:
            websocket.receive_json()

    assert exc_info.value.code == 1008
