from fastapi import FastAPI,Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from db.connection import connect_to_db
from api.central_api import router
from config import settings
from core.errors import UsersErrors
from schemas.responses import APIResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await connect_to_db()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware,secret_key=settings.google_secret_key)

app.include_router(router)
 
@app.exception_handler(UsersErrors)
async def global_exception_handler(request: Request,exc: UsersErrors):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            message="error",
            data = exc.message
        ).model_dump()
    )
