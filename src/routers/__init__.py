from fastapi import APIRouter

from src.routers.chat import router as chat_router
from src.routers.user import router as user_router
from src.routers.auth import router as auth_router
from src.routers.chat_history import router as chat_history_router
from src.routers.websocket import router as websocket_router
from src.settings import settings

router = APIRouter(prefix="/v1", include_in_schema=settings.DEVELOP)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(chat_history_router)
router.include_router(chat_router)
router.include_router(websocket_router)
