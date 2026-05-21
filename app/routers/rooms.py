from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status

from app.room_manager import room_manager

router = APIRouter(tags=["rooms"])


@router.get("/rooms/{room_id}/users")
def get_room_users(room_id: str) -> dict[str, object]:
    return {"room_id": room_id, "users": room_manager.get_users(room_id)}


@router.websocket("/ws/rooms/{room_id}")
async def websocket_room(websocket: WebSocket, room_id: str) -> None:
    await websocket.accept()

    username = websocket.query_params.get("username")
    if username is None or not username.strip():
        await websocket.close(code=1008)
        return

    username = username.strip()
    room_manager.connect(room_id, username, websocket)

    await room_manager.broadcast(
        room_id,
        {"type": "connected", "room_id": room_id, "username": username},
    )

    try:
        while True:
            payload = await websocket.receive_json()
            if payload.get("type") != "message":
                continue

            text = str(payload.get("text", ""))
            if len(text) > 300:
                await websocket.send_json({"type": "error", "detail": "Message is too long"})
                continue

            await room_manager.broadcast(
                room_id,
                {
                    "type": "message",
                    "room_id": room_id,
                    "username": username,
                    "text": text,
                },
            )
    except WebSocketDisconnect:
        pass
    finally:
        room_manager.disconnect(room_id, username, websocket)
