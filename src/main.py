from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.depends import init_container
from src.routers import router
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    init_container()

    yield


app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    docs_url=settings.DOC_URL if settings.DEVELOP else None,
    default_response_class=ORJSONResponse,
    openapi_url=settings.OPENAPI_URL,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.DEVELOP,
    )
