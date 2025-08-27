from src.dependencies import container
from src.engines.postgres_storage import PostgresEngine
from src.repositories.chat_message import ChatMessageRepository
from src.repositories.user import UserRepository


def init_container() -> None:
    container.add_instance(PostgresEngine())

    container.add_scoped(ChatMessageRepository)
    container.add_scoped(UserRepository)
