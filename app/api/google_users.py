from fastapi import Request,APIRouter
from services.users import google_login,user_google_login

router = APIRouter(prefix="/google")

@router.get("/login")
async def login(request: Request):
    await google_login(request)

@router.get("/callback",name="google_callback")
async def call_back(request: )
