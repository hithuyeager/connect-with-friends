from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str,list[WebSocket]]

    async def connect(
        self,
        websocket: WebSocket,
        room_id: str,
        user_id: str):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(websocket)