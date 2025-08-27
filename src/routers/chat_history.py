from fastapi import APIRouter, Depends

from src.schemes.base import BaseQueryPathFilters
from src.schemes.chat_history import ChatHistoryRequest, ChatHistoryResponse
from src.services.chat_history import ChatHistoryService


router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get("/", response_model=ChatHistoryResponse | int)
async def get_chat_history(
    filter_params: ChatHistoryRequest = Depends(),
    pagination_params: BaseQueryPathFilters = Depends(),
    chat_history_service: ChatHistoryService = Depends(),
) -> ChatHistoryResponse | int:
    return await chat_history_service.get_chat_history(
        filter_params=filter_params,
        pagination_params=pagination_params,
    )
