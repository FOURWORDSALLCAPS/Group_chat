import logging
import re

from fastapi import Query
from pydantic import BaseModel, Field

from src.settings import settings

log = logging.getLogger(__name__)


class BaseSanitizedModel(BaseModel):
    def model_post_init(self, __context):
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, str):
                cleaned_value = re.sub(r'<[^>]*?>|["\']', "", field_value)
                setattr(self, field_name, cleaned_value)


class Pagination(BaseSanitizedModel):
    total: int = Field(
        description="Total objects count",
        examples=[100],
    )
    page_count: int = Field(
        description="Total pages count",
        examples=[10],
    )


class PaginationParams(BaseSanitizedModel):
    page: int = Field(
        Query(settings.PAGINATION_PAGE, ge=1, description="Current page number")
    )
    page_size: int = Field(
        Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=1000, description="Page size")
    )


class BaseQueryPathFilters(PaginationParams):
    count_only: bool = Field(Query(False, description="Only count records"))
    pagination_on: bool = Field(Query(True, description="Pagination on or off"))
