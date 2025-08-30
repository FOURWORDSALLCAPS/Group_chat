from fastapi import status, HTTPException

from src.dependencies import container
from src.repositories.user import UserRepository
from src.schemes.user import (
    UserCreateResponse,
    UserCreateRequest,
)
from src.utilities.auth import hash_password


class UserService:
    def __init__(self) -> None:
        self.user_repository: UserRepository = container.resolve(UserRepository)

    async def create_user(
        self,
        filter_params: UserCreateRequest,
    ) -> UserCreateResponse:
        is_user = await self.user_repository.exist_user(filter_params.username)
        if is_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with name {filter_params.username} already exists.",
            )

        filter_params.password = hash_password(filter_params.password)
        user = await self.user_repository.create(**filter_params.model_dump())

        return UserCreateResponse(**user.__dict__)
