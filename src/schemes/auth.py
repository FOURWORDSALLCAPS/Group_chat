from uuid import UUID

from pydantic import Field

from src.schemes.base import BaseSanitizedModel


class LoginRequest(BaseSanitizedModel):
    username: str = Field(
        description="Логин",
        examples=["Steve"],
    )
    password: str = Field(
        description="Пароль",
        examples=["Jobs"],
    )


class LoginResponse(BaseSanitizedModel):
    user_uuid: UUID = Field(
        description="Уникальный идентификатор пользователя",
        examples=["a3d8f1e4-7b2c-4e9d-8a5f-1b3c9d7e5f2a"],
    )
