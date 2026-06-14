from fastapi import APIRouter
from .google_users import router as google_router
from .app_users import router as app_router
from .ws_api import router as ws_router

router = APIRouter()

router.include_router(google_router,prefix="/google")
router.include_router(app_router,prefix="/app")
router.include_router(ws_router,prefix="/ws")

