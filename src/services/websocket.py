from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect

from src.dependencies import container
from src.engines.websocket_client import websocket_manager
from src.repositories.user import UserRepository


class WebsocketService:
    def __init__(self) -> None:
        self.user_repository: UserRepository = container.resolve(UserRepository)

    async def connect_chat(self, websocket: WebSocket, user_uuid: UUID):
        user = await self.user_repository.get_by(uuid=user_uuid)

        await websocket_manager.connect(websocket, user.username)
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
            await websocket_manager.disconnect(user.username)
