import logging
import sys

from fastapi import WebSocket

from src.settings import settings

log = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
log.addHandler(stream_handler)


class WebsocketClient:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

        await websocket.send_json(
            {
                "type": "connection_established",
                "user_count_update": len(self.active_connections),
                "username": username,
            }
        )
        return username

    async def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_json(message)


websocket_manager = WebsocketClient()
