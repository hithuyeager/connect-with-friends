from fastapi import WebSocket
from  .auth import verify_user

class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str,dict[str,WebSocket]]

    async def connect(
        self,
        websocket: WebSocket,
        room_id: str
        ):
        await websocket.accept()
        user_id = verify_user(websocket)
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        self.rooms[room_id][user_id] = websocket
    def disconnect(self,user_id: str,room_id: str):
        if room_id in self.rooms:
            self.rooms[room_id].pop(user_id)
        
    async def send_to_room(self,data :dict,room_id: str,sender: WebSocket):
        if room_id not in self.rooms:
            return
        for connection in self.rooms[room_id]:
            if connection == sender:
                continue
            await connection.send_json(data)

manager = ConnectionManager()