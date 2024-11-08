import jwt
from datetime import timedelta, datetime

from app.config import settings


def hash_password(password: str) -> str:
    return settings.PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    return settings.PWD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
