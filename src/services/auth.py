from fastapi import status, HTTPException

from src.dependencies import container
from src.repositories.user import UserRepository
from src.schemes.auth import (
    LoginResponse,
    LoginRequest,
)
from src.utilities.auth import validate_password


class AuthService:
    def __init__(self) -> None:
        self.user_repository: UserRepository = container.resolve(UserRepository)

    async def login(
        self,
        filter_params: LoginRequest,
    ) -> LoginResponse:
        user = await self.user_repository.get_by(username=filter_params.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password or username.",
            )
        if not validate_password(filter_params.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password or username.",
            )

        return LoginResponse(user_uuid=user.uuid)
