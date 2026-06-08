from ws.connection_manager import manager
from fastapi import WebSocket,WebSocketDisconnect
from datetime import datetime

from core.security import verify_access_token

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
            await manager.send_to_room(payload,room_id,websocket)
    except WebSocketDisconnect:
        manager.disconnect(user_id,room_id)
        notify_exit = {
            "type":"system",
            "message" : f"{user_id} has left the room",
            "timestamp" : datetime.utcnow().isoformat()
        }
        await manager.disconnect(user_id,room_id)
