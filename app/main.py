from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from db.connection import connect_to_db
from api.central_api import router
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await connect_to_db()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware,secret_key=settings.google_secret_key)

app.include_router(router)
