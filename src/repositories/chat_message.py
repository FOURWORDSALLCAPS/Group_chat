from uuid import UUID

from sqlalchemy import select, and_

from src.dependencies import container
from src.engines.postgres_storage import PostgresEngine
from src.models.chat_messages import ChatMessageDB
from src.repositories.base import BaseRepository


class ChatMessageRepository(BaseRepository):
    def __init__(self):
        db: PostgresEngine = container.resolve(PostgresEngine)
        super().__init__(db, ChatMessageDB)

    async def get_chat_history_by_chat_uuid(
        self, chat_uuid: UUID
    ) -> list[ChatMessageDB]:
        stmt = select(ChatMessageDB).where(and_(ChatMessageDB.chat_uuid == chat_uuid))

        result = await self.db.select(stmt)  # noqa
        return result if result else None
