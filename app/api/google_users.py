from fastapi import Request,APIRouter,Depends
from fastapi.responses import JSONResponse
import asyncpg

from services.users import google_login,user_google_login
from dependencies import get_connection
from schemas.responses import APIResponse

router = APIRouter()

@router.get("/login")
async def login(request: Request):
    return await google_login(request)

@router.get("/callback",name="google_callback")
async def call_back(request: Request,conn: asyncpg.Connection = Depends(get_connection)):
    tokens = await user_google_login(request,conn)
    return JSONResponse(
        status_code=201,
        content=APIResponse(
            message="success",
            data=tokens
        ).model_dump()
    )
