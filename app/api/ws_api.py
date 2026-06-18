from fastapi import APIRouter,Depends,WebSocket,Query
from fastapi.responses import JSONResponse
import asyncpg

from dependencies import get_connection,get_current_user
from services.websocket_services import search_users
from schemas.responses import APIResponse
from schemas.ws_schemas import DirectRoomSchema
from services.websocket_services import generate_room_id,chat_system

router = APIRouter()

@router.get("/users/search")
async def search_by_name(
    query: str,
    current_user: str = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_connection)
):
    users = await search_users(conn,query,current_user["sub"])
    return JSONResponse(
        status_code=200,
        content=APIResponse(
            message="success",
            data=users
        ).model_dump()
    )
@router.post("/room/direct")
async def create_direct_room(
    data: DirectRoomSchema,
    current_user = Depends(get_current_user)
):
    room_id = generate_room_id(current_user["sub"],data.target_user_id)
    return JSONResponse(
        status_code=201,
        content=APIResponse(
            message="success",
            data = room_id
        ).model_dump()
    )

@router.websocket("/chat/{room_id}")
async def chat_endpoint(
    websocket: WebSocket,
    room_id: str,
    access_token: str = Query(str),
    conn: asyncpg.Connection = Depends(get_connection)
):
    await chat_system(websocket,room_id,access_token,conn)