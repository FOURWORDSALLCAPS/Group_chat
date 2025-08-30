from fastapi import APIRouter, Depends

from src.schemes.auth import LoginResponse, LoginRequest
from src.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login/", response_model=LoginResponse)
async def login(
    filter_params: LoginRequest,
    auth_service: AuthService = Depends(AuthService),
) -> LoginResponse:
    return await auth_service.login(
        filter_params=filter_params,
    )
