from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str,dict[str,WebSocket]] = {}
    """ 
    self.room = {
        room_id:{
            user_id: WebSocket
            }
        }
    """

    async def connect(
        self,
        websocket: WebSocket,
        room_id: str,
        user_id: str
        ):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        self.rooms[room_id][user_id] = websocket
    def disconnect(self,user_id: str,room_id: str):
        if room_id in self.rooms:
            self.rooms[room_id].pop(user_id)
        
    async def send_to_room(self,data :dict,room_id: str,sender_id: str):
        if room_id not in self.rooms:
            return
        for user_id,connection in self.rooms[room_id].items():
            if user_id == sender_id:
                continue
            await connection.send_json(data)

manager = ConnectionManager()