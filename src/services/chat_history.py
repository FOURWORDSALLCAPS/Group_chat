from src.dependencies import container
from src.repositories.chat_message import ChatMessageRepository
from src.repositories.user import UserRepository
from src.schemes.base import BaseQueryPathFilters, Pagination
from src.schemes.chat_history import (
    ChatHistoryResponse,
    ChatHistoryRequest,
    ChatMessages,
)


class ChatHistoryService:
    def __init__(self) -> None:
        self.chat_message_repository: ChatMessageRepository = container.resolve(
            ChatMessageRepository
        )
        self.user_repository: UserRepository = container.resolve(UserRepository)

    async def get_chat_history(
        self,
        filter_params: ChatHistoryRequest,
        pagination_params: BaseQueryPathFilters,
    ) -> ChatHistoryResponse | int:
        chat_messages = (
            await self.chat_message_repository.get_chat_history_by_chat_uuid(
                chat_uuid=filter_params.chat_uuid
            )
        )

        user_uuids = {chat_message.user_uuid for chat_message in chat_messages}

        users = await self.user_repository.get_users_by_uuids(user_uuids=user_uuids)

        usernames = {user.uuid: user.username for user in users}

        total = len(chat_messages)
        if pagination_params.count_only:
            return total

        data = []
        for chat_message in chat_messages:
            data.append(
                ChatMessages(
                    username=usernames.get(chat_message.user_uuid),
                    text=chat_message.text,
                    dispatch_date=chat_message.dispatch_date,
                )
            )

        if pagination_params.pagination_on:
            start_index = (pagination_params.page - 1) * pagination_params.page_size
            end_index = start_index + pagination_params.page_size
            data = data[start_index:end_index]

        pagination = Pagination(
            total=total, page_count=-(-total // pagination_params.page_size)
        )
        return ChatHistoryResponse(data=data, pagination=pagination)
