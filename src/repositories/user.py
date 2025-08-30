from typing import Iterable
from uuid import UUID

from sqlalchemy import select, and_

from src.dependencies import container
from src.engines.postgres_storage import PostgresEngine
from src.models.user import UserDB
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        db: PostgresEngine = container.resolve(PostgresEngine)
        super().__init__(db, UserDB)

    async def exist_user(self, username: str) -> bool:
        stmt = select(UserDB).where(and_(UserDB.username == username)).exists()

        return await self.db.execute(select(stmt))  # noqa

    async def get_users_by_uuids(self, user_uuids: Iterable[UUID]) -> list[UserDB]:
        stmt = select(UserDB).where(UserDB.uuid.in_(user_uuids))

        result = await self.db.select(stmt)  # noqa
        return result
