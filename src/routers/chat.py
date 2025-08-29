import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.settings import settings

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get("/")
async def read_index():
    index_dir = os.path.join(settings.TEMPLATES_DIR, "index.html")
    return FileResponse(index_dir)
