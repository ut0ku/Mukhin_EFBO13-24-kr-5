from __future__ import annotations

from dataclasses import dataclass, field

from fastapi import WebSocket


@dataclass
class RoomManager:
    rooms: dict[str, dict[str, list[WebSocket]]] = field(default_factory=dict)

    def reset(self) -> None:
        self.rooms.clear()

    def connect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        room = self.rooms.setdefault(room_id, {})
        room.setdefault(username, []).append(websocket)

    def disconnect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        room = self.rooms.get(room_id)
        if room is None:
            return

        connections = room.get(username)
        if connections is None:
            return

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            room.pop(username, None)

        if not room:
            self.rooms.pop(room_id, None)

    async def broadcast(self, room_id: str, payload: dict[str, object]) -> None:
        room = self.rooms.get(room_id)
        if room is None:
            return

        targets: list[WebSocket] = []
        seen: set[int] = set()
        for connections in room.values():
            for websocket in connections:
                websocket_id = id(websocket)
                if websocket_id in seen:
                    continue
                seen.add(websocket_id)
                targets.append(websocket)

        for websocket in targets:
            await websocket.send_json(payload)

    def get_users(self, room_id: str) -> list[str]:
        room = self.rooms.get(room_id)
        if room is None:
            return []
        return sorted(room.keys())


room_manager = RoomManager()
