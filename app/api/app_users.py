from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
import asyncpg

from schemas.users_schema import Signin,Signup
from schemas.responses import APIResponse
from services.users import app_sign_in,app_sign_up
from dependencies import get_connection

router = APIRouter()

@router.post("/signup")
async def signup(user: Signup,conn: asyncpg.Connection = Depends(get_connection)):
    tokens = await app_sign_up(conn,user.email,user.username,user.password)
    return  JSONResponse(
        status_code=201,
        content=APIResponse(
            message="success",
            data = tokens
        )
    )

@router.post("/signin")
async def signin(user: Signin,conn: asyncpg.Connection = Depends(get_connection)):
    tokens = await app_sign_in(conn,user.email,user.password)
    return  JSONResponse(
        status_code=200,
        content=APIResponse(
            message="success",
            data = tokens
        )
    )
