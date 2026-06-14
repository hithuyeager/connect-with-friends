from fastapi import Request,Depends
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

from core.security import verify_access_token

bearer_schema = HTTPBearer()

async def get_pool(request: Request):
    return request.app.state.pool

async def get_connection(pool = Depends(get_pool)):
    async with pool.acquire() as conn:
        yield conn

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_schema)):
    token = credentials.credentials 
    return verify_access_token(token)     