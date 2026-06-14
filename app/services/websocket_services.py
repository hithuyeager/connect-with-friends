from ws.connection_manager import manager
from fastapi import WebSocket,WebSocketDisconnect
from datetime import datetime
from hashlib import sha256

from core.security import verify_access_token

def generate_room_id(user1_id: str, user2_id: str):
    sorted_ids = sorted([user1_id,user2_id])
    combined = f"{sorted_ids[0]:{sorted_ids[1]}}"
    return sha256(combined.encode()).hexdigest()[:16]

async def chat_system(
    websocket: WebSocket,
    room_id: str,
    access_token: str
):
    user = verify_access_token(access_token)
    user_id = user["sub"]
    await manager.connect(websocket,room_id,user_id)
    notify_entry = {
        "type" : "system",
        "message" : f"{user_id} joined the room",
        "timestamp" : datetime.utcnow().isoformat()
    }

    await manager.send_to_room(notify_entry,room_id,websocket)

    try:
        while True:
            data = await websocket.receive_json()
            payload = {
                "type" : "message",
                "from" : user_id,
                "message" : data["message"],
                "room_id" : room_id,
                "timestamp" : datetime.utcnow().isoformat()
            }
            await manager.send_to_room(payload,room_id,user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id,room_id)