from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEVELOP: bool = True
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8080
    TITLE: str = "API"
    VERSION: str = "v1.0"
    DOC_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    LOG_LEVEL: str = "debug"
    LOG_FORMAT: str = '{"time": "%(asctime)s", "level": "%(levelname)s", "file": "%(name)s", "line": "%(lineno)s", "msg": "%(msg)s"}'
    POSTGRES_URI: str = (
        "postgresql+asyncpg://postgres_user:postgres_password@postgres:5432/postgres_db"
    )
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_MAX_OVERFLOW: int = 5

    JWT_SECRET: str = "replace_me"
    JWT_EXPIRES: int = 60
    JWT_ALGORITHM: str = "HS256"
    SEARCH_LIMIT_SIZE: int = 25
    WORKERS: int = 1

    PAGINATION_PAGE: int = 1
    PAGINATION_PAGE_SIZE: int = 25


settings = Settings(
    _env_file="../.env",
    _env_file_encoding="utf-8",
)
