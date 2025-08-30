from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, Query
from pydantic import Field

from src.services.websocket import WebsocketService


router = APIRouter(
    prefix="/ws",
    tags=["Websocket"],
)


@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    user_uuid: UUID = Query(
        Field(
            description="Уникальный идентификатор пользователя",
            examples=["a3d8f1e4-7b2c-4e9d-8a5f-1b3c9d7e5f2a"],
        )
    ),
    websocket_service: WebsocketService = Depends(),
):
    return await websocket_service.connect_chat(
        websocket=websocket, user_uuid=user_uuid
    )
