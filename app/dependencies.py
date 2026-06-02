from fastapi import Request,Depends


async def get_pool(request: Request):
    return request.app.state.pool

async def get_connection(pool = Depends(get_pool)):
    async with pool.acquire() as conn:
        yield conn
        