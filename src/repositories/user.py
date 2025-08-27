from typing import Iterable
from uuid import UUID

from sqlalchemy import select

from src.dependencies import container
from src.engines.postgres_storage import PostgresEngine
from src.models.user import UserDB


class UserRepository:
    def __init__(self):
        self.db: PostgresEngine = container.resolve(PostgresEngine)

    async def get_users_by_uuids(self, user_uuids: Iterable[UUID]) -> list[UserDB]:
        stmt = select(UserDB).where(UserDB.uuid.in_(user_uuids))

        result = await self.db.select(stmt)  # noqa
        return result if result else None
