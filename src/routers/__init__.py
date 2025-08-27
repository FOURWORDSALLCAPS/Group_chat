from fastapi import APIRouter

from src.routers.chat_history import router as chat_history_router
from src.settings import settings

router = APIRouter(prefix="/v1", include_in_schema=settings.DEVELOP)
router.include_router(chat_history_router)
