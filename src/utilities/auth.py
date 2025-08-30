from hashlib import sha256

from src.settings import settings


def hash_password(password: str) -> str:
    return sha256((str(password) + settings.JWT_SECRET).encode("utf-8")).hexdigest()


def validate_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
