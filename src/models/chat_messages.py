from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.models.base import Base


class ChatMessageDB(Base):
    __tablename__ = "chat_messages"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="Уникальный идентификатор сообщения",
    )
    chat_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chats.uuid", ondelete="CASCADE"),
        nullable=False,
        comment="Идентификатор чата",
    )
    user_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        comment="Идентификатор отправителя",
    )
    text: Mapped[str] = mapped_column(Text, nullable=False, comment="Текст сообщения")
    dispatch_date: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now(), comment="Дата и время отправки"
    )
    is_read: Mapped[bool] = mapped_column(
        default=False, server_default="false", comment="Статус прочтения сообщения"
    )
