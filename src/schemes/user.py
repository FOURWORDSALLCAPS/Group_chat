from datetime import date
from uuid import UUID

from pydantic import Field

from src.schemes.base import BaseSanitizedModel


class BaseUser(BaseSanitizedModel):
    user_uuid: UUID = Field(
        description="Уникальный идентификатор пользователя",
        examples=["a3d8f1e4-7b2c-4e9d-8a5f-1b3c9d7e5f2a"],
    )


class UserInfo(BaseSanitizedModel):
    username: str = Field(
        description="Логин",
        examples=["Steve"],
    )
    password: str = Field(
        description="Пароль",
        examples=["Jobs"],
    )
    first_name: str | None = Field(
        description="Имя",
        examples=["Владимир"],
    )
    last_name: str | None = Field(
        description="Фамилия",
        examples=["Зайцев"],
    )
    middle_name: str | None = Field(
        description="Отчество",
        examples=["Олегович"],
    )
    birthday: date | None = Field(
        description="Дата рождения",
        examples=["2001-01-01"],
    )
    phone: str | None = Field(
        description="Номер телефона",
        examples=["79531284192"],
    )
    email: str | None = Field(
        description="Электронная почта",
        examples=["user@example.com"],
    )


class UserCreateRequest(UserInfo): ...


class UserCreateResponse(UserInfo, BaseUser): ...
