import logging
import sys
from uuid import UUID
from typing import TypeVar, Generic
from sqlalchemy import insert, select, and_
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    InterfaceError,
)
from sqlalchemy.orm import InstrumentedAttribute

from src.engines.postgres_storage import PostgresEngine
from src.settings import settings

log = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
log.addHandler(stream_handler)

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: PostgresEngine, model: type[T]) -> None:
        self.db = db
        self.model = model

    async def get_by(self, **kwargs: str | UUID | bool | set[UUID] | None) -> T | None:
        if not self.model:
            raise ValueError("Model is not defined for this repository")

        if not kwargs:
            raise ValueError("At least one kwargs must be provided")

        try:
            conditions = []
            for field_name, value in kwargs.items():
                field: InstrumentedAttribute = getattr(self.model, field_name, None)
                if field is None:
                    raise ValueError(
                        f"Field '{field_name}' does not exist in {self.model.__name__}"
                    )
                conditions.append(field == value)

            stmt = select(self.model).where(and_(*conditions))

            result = await self.db.execute(stmt)  # noqa

            return result
        except ValueError as e:
            log.error(f"Value error in get_by for {self.model.__name__}: {e}")
            return None
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            log.error(f"Database error in get_by for {self.model.__name__}: {e}")
            return None
        except SQLAlchemyError as e:
            log.error(f"SQLAlchemy error in get_by for {self.model.__name__}: {e}")
            return None
        except Exception as e:
            log.error(f"Unexpected error in get_by for {self.model.__name__}: {e}")
            return None

    async def create(self, **kwargs: str | UUID | bool | set[UUID] | None) -> T | None:
        if not self.model:
            raise ValueError("Model is not defined for this repository")

        try:
            stmt = insert(self.model).values(**kwargs).returning(self.model)

            result = await self.db.execute(stmt)  # noqa

            if result:
                return result
            else:
                log.error(f"Failed to create {self.model.__name__}: no result returned")
                return None
        except IntegrityError as e:
            log.error(f"Integrity error when creating {self.model.__name__}: {e}")
            return None
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            log.error(f"Database error when creating {self.model.__name__}: {e}")
            return None
        except SQLAlchemyError as e:
            log.error(f"SQLAlchemy error when creating {self.model.__name__}: {e}")
            return None
        except Exception as e:
            log.error(f"Unexpected error when creating {self.model.__name__}: {e}")
            return None
