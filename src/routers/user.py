from fastapi import APIRouter, Depends

from src.schemes.user import UserCreateResponse, UserCreateRequest
from src.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserCreateResponse)
async def create_user(
    filter_params: UserCreateRequest,
    user_service: UserService = Depends(UserService),
) -> UserCreateResponse:
    return await user_service.create_user(
        filter_params=filter_params,
    )
