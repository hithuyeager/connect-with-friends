from fastapi import APIRouter
from .google_users import router as google_router
from .app_users import router as app_router

router = APIRouter()

router.include_router(google_router,prefix="/google")
router.include_router(app_router,prefix="/app")

