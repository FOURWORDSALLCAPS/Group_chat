import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.engines.websocket_client import websocket_manager


router = APIRouter(
    prefix="/ws",
    tags=["Websocket"],
)


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    user_id = str(uuid.uuid4())
    await websocket_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()

            await websocket_manager.broadcast(
                {
                    "type": "message",
                    "username": data["username"],
                    "content": data["content"],
                    "timestamp": data["timestamp"],
                }
            )

    except WebSocketDisconnect:
        await websocket_manager.disconnect(user_id)
