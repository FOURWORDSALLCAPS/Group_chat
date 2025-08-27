from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.schemes.base import BaseSanitizedModel, Pagination


class ChatHistoryRequest(BaseSanitizedModel):
    chat_uuid: UUID = Field(
        description="UUID чата",
        examples=["a3d8f1e4-7b2c-4e9d-8a5f-1b3c9d7e5f2a"],
    )


class ChatMessages(BaseSanitizedModel):
    username: str = Field(
        description="Имя пользователя",
        examples=["Myname"],
    )
    text: str = Field(
        description="Сообщение",
        examples=["Привет, как погода?"],
    )
    dispatch_date: datetime = Field(
        description="Дата и временя отправки",
        examples=["2025-01-01 14:20:03"],
    )


class ChatHistoryResponse(BaseSanitizedModel):
    data: list[ChatMessages] = Field(description="История сообщений")
    pagination: Pagination = Field(
        title="Данные о пагинации",
        description="Данные о пагинации",
    )
