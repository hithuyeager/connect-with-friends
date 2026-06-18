from fastapi import WebSocket,WebSocketDisconnect
from datetime import datetime
from hashlib import sha256
import asyncpg

from ws.connection_manager import manager
from core.security import verify_access_token
import repositories.websocket_repo as repo
from core import errors as error

def generate_room_id(user1_id: str, user2_id: str):
    sorted_ids = sorted([user1_id,user2_id])
    combined = f"{sorted_ids[0]}:{sorted_ids[1]}"
    return sha256(combined.encode()).hexdigest()[:16]

async def search_users(conn: asyncpg.Connection ,search_users: str, current_user_id: str):
    users = await repo.search_users(conn,search_users,current_user_id)
    if not users:
        raise error.NoUsersMatchError()
    return users

async def chat_system(
    websocket: WebSocket,
    room_id: str,
    access_token: str,
    conn: asyncpg.Connection
):
    user = verify_access_token(access_token)
    user_id = user["sub"]
    await manager.connect(websocket,room_id,user_id)
    notify_entry = {
        "type" : "system",
        "message" : f"{user_id} joined the room",
        "timestamp" : datetime.utcnow().isoformat()
    }

    await manager.send_to_room(notify_entry,room_id,user_id)

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
            await repo.add_messages(conn,room_id,user_id,data["message"])
            await manager.send_to_room(payload,room_id,user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id,room_id)
        await manager.send_to_room({
            "type": "system",
            "message": f"{user_id} left the room",
            "timestamp": datetime.utcnow().isoformat()
        }, room_id, user_id)