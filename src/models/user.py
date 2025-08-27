from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import Index
from datetime import date

from src.models.base import Base


class UserDB(Base):
    __tablename__ = "users"
    __table_args__ = (Index(None, "last_name", "first_name", "middle_name"),)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="Уникальный идентификатор пользователя",
    )
    username: Mapped[str] = mapped_column(
        index=True,
        unique=True,
        comment="Логин",
    )
    password: Mapped[str] = mapped_column(
        comment="Пароль",
    )
    first_name: Mapped[str | None] = mapped_column(
        comment="Имя",
    )
    last_name: Mapped[str | None] = mapped_column(
        comment="Фамилия",
    )
    middle_name: Mapped[str | None] = mapped_column(
        comment="Отчество",
    )
    birthday: Mapped[date | None] = mapped_column(
        comment="дата рождения",
    )
    phone: Mapped[int | None] = mapped_column(
        comment="номер телефона",
    )
    email: Mapped[str | None] = mapped_column(
        comment="электронная почти",
    )
    active: Mapped[bool] = mapped_column(
        default=True,
        comment="Вкл/выкл учетная запись",
    )

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name}"
